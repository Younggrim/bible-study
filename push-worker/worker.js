/**
 * Cloudflare Worker — Daily Devotional Push
 *
 * Handles Web Push subscription storage and sends a daily, payload-less
 * VAPID-authenticated push to every stored subscriber. The actual
 * notification content (today's devotional) is fetched by the client's
 * service worker at delivery time from that site's own devotionals.json —
 * this worker never needs to know which site a subscriber came from.
 *
 * Deploy: npx wrangler deploy
 * Secret: npx wrangler secret put VAPID_PRIVATE_KEY
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

export default {
  async fetch(request, env) {
    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: getCorsHeaders(request) });
    }

    if (request.method !== 'POST') {
      return new Response('Not found', { status: 404 });
    }

    if (!originAllowed(request)) {
      return jsonResponse({ error: 'Forbidden' }, 403, request);
    }

    const url = new URL(request.url);
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
      await env.PUSH_SUBS.put('sub:' + body.endpoint, JSON.stringify(body));
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
    const privateKey = await importVapidPrivateKey(env.VAPID_PUBLIC_KEY, env.VAPID_PRIVATE_KEY);
    const list = await env.PUSH_SUBS.list({ prefix: 'sub:' });

    for (const key of list.keys) {
      const raw = await env.PUSH_SUBS.get(key.name);
      if (!raw) continue;

      let sub;
      try {
        sub = JSON.parse(raw);
      } catch (e) {
        continue;
      }

      let audience;
      try {
        audience = new URL(sub.endpoint).origin;
      } catch (e) {
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
        }
      } catch (e) {
        // Network error reaching this push service — leave the subscription
        // in place and try again on the next scheduled run.
      }
    }
  }
};
