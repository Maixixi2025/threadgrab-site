/**
 * ThreadGrab Profile API - Pages Function
 * GET /api/profile/{username}
 *
 * 替代原 CF Worker 部署，统一用 GitHub → Pages 部署
 * 加 Rate Limiting 防 RapidAPI 被刷爆
 */

export const onRequestGet = async (context) => {
  const { request, env, params } = context;
  const username = params.username;
  const url = new URL(request.url);

  // CORS（同域不需要，但留兜底以防外部调用）
  const corsHeaders = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '86400',
  };

  if (request.method === 'OPTIONS') {
    return new Response(null, { headers: corsHeaders });
  }

  // Rate Limiting - 按 client IP 限流（每 IP 每分钟 10 次）
  const clientIp = request.headers.get('cf-connecting-ip') || 'unknown';
  if (env.THREADGRAB_RATELIMIT) {
    const { success } = env.THREADGRAB_RATELIMIT.limit({ key: clientIp });
    if (!success) {
      return new Response(JSON.stringify({
        error: 'Rate limit exceeded. Max 10 requests per minute per IP.',
        retry_after: 60,
      }), {
        status: 429,
        headers: {
          ...corsHeaders,
          'Content-Type': 'application/json',
          'Retry-After': '60',
        },
      });
    }
  }

  // 参数校验
  if (!username || !/^[a-zA-Z0-9._]{1,30}$/.test(username)) {
    return new Response(JSON.stringify({ error: 'Invalid username' }), {
      status: 400,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
    });
  }

  // 调 RapidAPI
  try {
    const upstream = await fetch(`https://${env.RAPIDAPI_HOST}/user/infobyusername`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'x-rapidapi-host': env.RAPIDAPI_HOST,
        'x-rapidapi-key': env.RAPIDAPI_KEY,
      },
      body: JSON.stringify({ username }),
    });

    if (!upstream.ok) {
      return new Response(JSON.stringify({ error: 'Upstream error', status: upstream.status }), {
        status: upstream.status,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      });
    }

    const data = await upstream.json();

    // 提取 user 对象，扁平化返回（前端期望的格式）
    if (data?.data?.user) {
      return new Response(JSON.stringify(data.data.user), {
        status: 200,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      });
    } else if (data?.error) {
      return new Response(JSON.stringify({ error: data.error.message || 'User not found' }), {
        status: 404,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      });
    } else {
      return new Response(JSON.stringify(data), {
        status: 200,
        headers: { ...corsHeaders, 'Content-Type': 'application/json' },
      });
    }
  } catch (err) {
    return new Response(JSON.stringify({ error: 'Internal server error', detail: err.message }), {
      status: 500,
      headers: { ...corsHeaders, 'Content-Type': 'application/json' },
    });
  }
};

export const onRequestOptions = async () => {
  return new Response(null, {
    headers: {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
      'Access-Control-Max-Age': '86400',
    },
  });
};
