/**
 * ThreadGrab Profile API - Pages Function
 * GET /api/profile/{username}
 *
 * 替代原 CF Worker 部署，统一用 GitHub → Pages 部署
 *
 * Rate Limiting (2026-07-02): KV-backed, works across Pages Functions multi-instance
 *  - Replaces in-memory Map (was ineffective — every request could hit a different instance)
 *  - Uses KV with TTL=60s auto-expiry, no manual cleanup needed
 *  - Free tier: 100k reads/day + 10k writes/day — more than enough
 */

const RATE_LIMIT = 10;          // 每 IP 窗口内最多 10 次
const RATE_WINDOW_SECONDS = 60; // 60 秒窗口

function corsHeaders() {
  return {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '86400',
  };
}

function jsonResponse(body, status = 200, extraHeaders = {}) {
  return new Response(JSON.stringify(body), {
    status,
    headers: {
      ...corsHeaders(),
      'Content-Type': 'application/json',
      ...extraHeaders,
    },
  });
}

/**
 * Rate limiting via KV (2026-07-02: replaced in-memory Map).
 * Strategy: store a per-IP counter with TTL = window length.
 *  - Read counter from KV
 *  - If count >= limit → reject 429
 *  - Else increment + write back with TTL
 *
 * Edge case: if KV read fails, allow the request through (fail-open)
 * to avoid blocking real users on KV outage.
 */
async function checkRateLimit(env, clientIp) {
  const key = `rl:${clientIp}`;
  const limit = RATE_LIMIT;
  const ttl = RATE_WINDOW_SECONDS;

  let current = 0;
  try {
    const stored = await env.RATE_LIMIT.get(key);
    current = stored ? parseInt(stored, 10) : 0;
    if (Number.isNaN(current)) current = 0;
  } catch (err) {
    // KV read failure — fail-open
    return { success: true, remaining: limit, resetAt: Date.now() + ttl * 1000 };
  }

  if (current >= limit) {
    // Compute reset time from metadata.expiration if available, else now + ttl
    let resetAt = Date.now() + ttl * 1000;
    try {
      const meta = await env.RATE_LIMIT.getWithMetadata(key);
      if (meta?.metadata?.resetAt) resetAt = meta.metadata.resetAt;
    } catch (_) { /* ignore */ }
    return { success: false, remaining: 0, resetAt };
  }

  // Increment + write back with TTL
  const next = current + 1;
  const resetAt = Date.now() + ttl * 1000;
  try {
    await env.RATE_LIMIT.put(key, String(next), {
      expirationTtl: ttl,
      metadata: { resetAt },
    });
  } catch (err) {
    // KV write failure — still allow this request (fail-open)
    return { success: true, remaining: Math.max(0, limit - next), resetAt };
  }

  return {
    success: true,
    remaining: Math.max(0, limit - next),
    resetAt,
  };
}

export const onRequestGet = async (context) => {
  const { request, env, params } = context;

  // 1. Rate Limiting (KV-backed, multi-instance safe)
  const clientIp = request.headers.get('cf-connecting-ip') || 'unknown';
  const rl = await checkRateLimit(env, clientIp);
  if (!rl.success) {
    const retryAfter = Math.ceil((rl.resetAt - Date.now()) / 1000);
    return jsonResponse(
      {
        error: 'Rate limit exceeded. Max 10 requests per minute per IP.',
        retry_after: retryAfter,
      },
      429,
      { 'Retry-After': String(retryAfter) }
    );
  }

  // 2. Parameter validation — return JSON 400 (was: leaked through to HTML redirect)
  const username = params.username;
  if (!username || !/^[a-zA-Z0-9._]{1,30}$/.test(username)) {
    return jsonResponse({ error: 'Invalid username' }, 400);
  }

  // 3. Call RapidAPI
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
      return jsonResponse(
        { error: 'Upstream error', status: upstream.status },
        upstream.status
      );
    }

    const data = await upstream.json();

    // 4. Response handling
    //    - User found → 200 with user object
    //    - Explicit error → 404 with message  (NEW: was previously leaking raw upstream)
    //    - Empty/null user → 404 (NEW: was previously 200 + empty, indistinguishable from success)
    if (data?.data?.user) {
      return jsonResponse(data.data.user, 200);
    } else if (data?.data?.user === null) {
      // RapidAPI returns data.user=null when not found
      return jsonResponse({ error: 'User not found' }, 404);
    } else if (data?.error) {
      return jsonResponse(
        { error: data.error.message || 'User not found' },
        404
      );
    } else {
      // Unknown shape — pass through but normalize content-type
      return jsonResponse(data, 200);
    }
  } catch (err) {
    return jsonResponse(
      { error: 'Internal server error', detail: err.message },
      500
    );
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