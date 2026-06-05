/**
 * ThreadGrab Profile API - Pages Function
 * GET /api/profile/{username}
 *
 * 替代原 CF Worker 部署，统一用 GitHub → Pages 部署
 * 内置 in-memory Rate Limiting（防 RapidAPI 爆账单）
 */

const RATE_LIMIT = 10;          // 每 IP 窗口内最多 10 次
const RATE_WINDOW_MS = 60_000;  // 60 秒窗口
const rateLimitMap = new Map();

function checkRateLimit(ip) {
  const now = Date.now();
  const entry = rateLimitMap.get(ip) || { count: 0, resetAt: now + RATE_WINDOW_MS };

  if (now > entry.resetAt) {
    // 窗口过期，重置
    entry.count = 0;
    entry.resetAt = now + RATE_WINDOW_MS;
  }

  entry.count++;
  rateLimitMap.set(ip, entry);

  return {
    success: entry.count <= RATE_LIMIT,
    remaining: Math.max(0, RATE_LIMIT - entry.count),
    resetAt: entry.resetAt,
  };
}

function corsHeaders() {
  return {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '86400',
  };
}

export const onRequestGet = async (context) => {
  const { request, env, params } = context;
  const username = params.username;

  if (request.method === 'OPTIONS') {
    return new Response(null, { headers: corsHeaders() });
  }

  // Rate Limiting - 按 client IP（in-memory，简单实现）
  const clientIp = request.headers.get('cf-connecting-ip') || 'unknown';
  const rl = checkRateLimit(clientIp);
  if (!rl.success) {
    return new Response(JSON.stringify({
      error: 'Rate limit exceeded. Max 10 requests per minute per IP.',
      retry_after: Math.ceil((rl.resetAt - Date.now()) / 1000),
    }), {
      status: 429,
      headers: {
        ...corsHeaders(),
        'Content-Type': 'application/json',
        'Retry-After': String(Math.ceil((rl.resetAt - Date.now()) / 1000)),
      },
    });
  }

  // 参数校验
  if (!username || !/^[a-zA-Z0-9._]{1,30}$/.test(username)) {
    return new Response(JSON.stringify({ error: 'Invalid username' }), {
      status: 400,
      headers: { ...corsHeaders(), 'Content-Type': 'application/json' },
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
        headers: { ...corsHeaders(), 'Content-Type': 'application/json' },
      });
    }

    const data = await upstream.json();

    // 提取 user 对象，扁平化返回（前端期望的格式）
    if (data?.data?.user) {
      return new Response(JSON.stringify(data.data.user), {
        status: 200,
        headers: { ...corsHeaders(), 'Content-Type': 'application/json' },
      });
    } else if (data?.error) {
      return new Response(JSON.stringify({ error: data.error.message || 'User not found' }), {
        status: 404,
        headers: { ...corsHeaders(), 'Content-Type': 'application/json' },
      });
    } else {
      return new Response(JSON.stringify(data), {
        status: 200,
        headers: { ...corsHeaders(), 'Content-Type': 'application/json' },
      });
    }
  } catch (err) {
    return new Response(JSON.stringify({ error: 'Internal server error', detail: err.message }), {
      status: 500,
      headers: { ...corsHeaders(), 'Content-Type': 'application/json' },
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
