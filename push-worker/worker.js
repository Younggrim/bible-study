/**
 * Cloudflare Worker — Daily Devotional Push
 *
 * Handles Web Push subscription storage and, once an hour, sends a
 * payload-less VAPID-authenticated push to whichever subscribers have
 * that hour (in UTC) as their own chosen reminder time — each subscriber
 * picks their own local time client-side, converts it to a UTC hour, and
 * that's stored alongside their subscription. The actual notification
 * content (today's devotional) is fetched by the client's service worker
 * at delivery time from that site's own devotionals.json — this worker
 * never needs to know which site a subscriber came from.
 *
 * Deploy: npx wrangler deploy
 * Secrets: npx wrangler secret put VAPID_PRIVATE_KEY
 *          npx wrangler secret put ADMIN_SECRET   (for manual /send-now testing)
 */

const ALLOWED_ORIGINS = [
  'https://bible.macdwellings.com',
  'https://bible.nrc.macdwellings.com',
  'http://localhost',
  'http://127.0.0.1'
];

const VAPID_SUBJECT = 'mailto:admin@macdwellings.com';

function getCorsHeaders(request) {
  const origin = request.headers.get('Origin') || '';
  const allowedOrigin = ALLOWED_ORIGINS.find(o => origin.startsWith(o)) ? origin : ALLOWED_ORIGINS[0];
  return {
    'Access-Control-Allow-Origin': allowedOrigin,
    'Access-Control-Allow-Methods': 'POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '86400',
  };
}

function originAllowed(request) {
  const origin = request.headers.get('Origin') || '';
  const referer = request.headers.get('Referer') || '';
  const originOk = origin && ALLOWED_ORIGINS.some(o => origin.startsWith(o));
  const refererOk = !origin && referer && ALLOWED_ORIGINS.some(o => referer.startsWith(o));
  return originOk || refererOk;
}

function jsonResponse(body, status, request) {
  return new Response(JSON.stringify(body), {
    status,
    headers: { 'Content-Type': 'application/json', ...getCorsHeaders(request) }
  });
}

// --- base64url helpers (Workers runtime has atob/btoa but not Buffer) ---

function base64urlToBytes(base64url) {
  const base64 = base64url.replace(/-/g, '+').replace(/_/g, '/');
  const padded = base64 + '='.repeat((4 - (base64.length % 4)) % 4);
  const raw = atob(padded);
  const bytes = new Uint8Array(raw.length);
  for (let i = 0; i < raw.length; i++) bytes[i] = raw.charCodeAt(i);
  return bytes;
}

function bytesToBase64url(bytes) {
  let str = '';
  for (let i = 0; i < bytes.length; i++) str += String.fromCharCode(bytes[i]);
  return btoa(str).replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
}

function stringToBase64url(str) {
  return bytesToBase64url(new TextEncoder().encode(str));
}

// --- VAPID: import the shared keypair, sign a per-request JWT ---

async function importVapidPrivateKey(publicKeyB64url, privateKeyB64url) {
  const pubBytes = base64urlToBytes(publicKeyB64url); // 65 bytes: 0x04 || X(32) || Y(32)
  const jwk = {
    kty: 'EC',
    crv: 'P-256',
    x: bytesToBase64url(pubBytes.slice(1, 33)),
    y: bytesToBase64url(pubBytes.slice(33, 65)),
    d: privateKeyB64url,
    ext: true
  };
  return crypto.subtle.importKey('jwk', jwk, { name: 'ECDSA', namedCurve: 'P-256' }, false, ['sign']);
}

async function buildVapidJWT(privateKey, audience) {
  const header = { typ: 'JWT', alg: 'ES256' };
  const now = Math.floor(Date.now() / 1000);
  const payload = { aud: audience, exp: now + 12 * 3600, sub: VAPID_SUBJECT };
  const unsigned = stringToBase64url(JSON.stringify(header)) + '.' + stringToBase64url(JSON.stringify(payload));
  const signature = await crypto.subtle.sign(
    { name: 'ECDSA', hash: 'SHA-256' },
    privateKey,
    new TextEncoder().encode(unsigned)
  );
  // crypto.subtle ECDSA returns the raw r||s signature — exactly the format
  // JWS/ES256 expects, no DER conversion needed.
  return unsigned + '.' + bytesToBase64url(new Uint8Array(signature));
}

// Shared by the hourly cron and the manual /send-now debug endpoint.
// If targetHour (0-23, UTC) is given, only subscriptions whose stored
// hourUTC matches are sent to — this is what lets each subscriber pick
// their own reminder time rather than everyone getting one fixed time.
// Passing null/undefined sends to everyone regardless of their chosen hour
// (used by /send-now for on-demand testing).
async function sendPush(env, targetHour) {
  const privateKey = await importVapidPrivateKey(env.VAPID_PUBLIC_KEY, env.VAPID_PRIVATE_KEY);
  const list = await env.PUSH_SUBS.list({ prefix: 'sub:' });
  const summary = { total: 0, matched: 0, sent: 0, expired: 0, failed: 0 };

  for (const key of list.keys) {
    const raw = await env.PUSH_SUBS.get(key.name);
    if (!raw) continue;
    summary.total++;

    let sub;
    try {
      sub = JSON.parse(raw);
    } catch (e) {
      summary.failed++;
      continue;
    }

    if (typeof targetHour === 'number' && sub.hourUTC !== targetHour) continue;
    summary.matched++;

    let audience;
    try {
      audience = new URL(sub.endpoint).origin;
    } catch (e) {
      summary.failed++;
      continue;
    }

    try {
      const jwt = await buildVapidJWT(privateKey, audience);
      const resp = await fetch(sub.endpoint, {
        method: 'POST',
        headers: {
          'Authorization': `vapid t=${jwt}, k=${env.VAPID_PUBLIC_KEY}`,
          'TTL': '86400',
          'Content-Length': '0'
        }
      });
      if (resp.status === 404 || resp.status === 410) {
        await env.PUSH_SUBS.delete(key.name);
        summary.expired++;
      } else if (resp.ok || resp.status === 201) {
        summary.sent++;
      } else {
        summary.failed++;
      }
    } catch (e) {
      // Network error reaching this push service — leave the subscription
      // in place and try again on the next scheduled run.
      summary.failed++;
    }
  }

  return summary;
}

export default {
  async fetch(request, env) {
    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: getCorsHeaders(request) });
    }

    if (request.method !== 'POST') {
      return new Response('Not found', { status: 404 });
    }

    const url = new URL(request.url);

    // Manual trigger for testing — not origin-gated (it's not called from a
    // browser), gated instead by a shared secret header only the operator
    // knows. By default sends to everyone regardless of their configured
    // hour (useful for an immediate test); pass {"hourUTC": n} in the body
    // to instead test a specific hour bucket the way the cron would see it.
    if (url.pathname === '/send-now') {
      const provided = request.headers.get('X-Admin-Secret') || '';
      if (!env.ADMIN_SECRET || provided !== env.ADMIN_SECRET) {
        return new Response(JSON.stringify({ error: 'Forbidden' }), {
          status: 403, headers: { 'Content-Type': 'application/json' }
        });
      }
      let targetHour = null;
      try {
        const testBody = await request.json();
        if (testBody && Number.isInteger(testBody.hourUTC)) targetHour = testBody.hourUTC;
      } catch (e) { /* no body, or not JSON — fine, send to everyone */ }
      const summary = await sendPush(env, targetHour);
      return new Response(JSON.stringify(summary), {
        status: 200, headers: { 'Content-Type': 'application/json' }
      });
    }

    if (!originAllowed(request)) {
      return jsonResponse({ error: 'Forbidden' }, 403, request);
    }

    let body;
    try {
      body = await request.json();
    } catch (e) {
      return jsonResponse({ error: 'Invalid JSON' }, 400, request);
    }

    if (url.pathname === '/subscribe') {
      if (!body || !body.endpoint || !body.keys || !body.keys.p256dh || !body.keys.auth) {
        return jsonResponse({ error: 'Invalid subscription' }, 400, request);
      }
      // hourUTC (0-23) is the subscriber's own chosen reminder time,
      // converted to UTC client-side. Falls back to 12:00 UTC (~8am
      // Eastern) if the client didn't send one.
      let hourUTC = Number.isInteger(body.hourUTC) ? body.hourUTC : 12;
      if (hourUTC < 0 || hourUTC > 23) hourUTC = 12;
      const record = { endpoint: body.endpoint, keys: body.keys, hourUTC };
      await env.PUSH_SUBS.put('sub:' + body.endpoint, JSON.stringify(record));
      return jsonResponse({ ok: true }, 200, request);
    }

    if (url.pathname === '/unsubscribe') {
      if (!body || !body.endpoint) {
        return jsonResponse({ error: 'Missing endpoint' }, 400, request);
      }
      await env.PUSH_SUBS.delete('sub:' + body.endpoint);
      return jsonResponse({ ok: true }, 200, request);
    }

    return jsonResponse({ error: 'Not found' }, 404, request);
  },

  async scheduled(controller, env, ctx) {
    await sendPush(env, new Date().getUTCHours());
  }
};
