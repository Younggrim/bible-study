/**
 * Cloudflare Worker — Daily Devotional Push
 *
 * Handles Web Push subscription storage and, once an hour, sends a
 * payload-less VAPID-authenticated push to whichever subscribers'
 * chosen local reminder time it currently is. Cloudflare Cron Triggers
 * only run in UTC — there's no way to schedule "fire at each user's
 * local 7am" directly — so instead each subscriber's IANA timezone
 * (e.g. "America/New_York") and chosen local hour (0-23) are stored,
 * and on every hourly tick this worker computes, per subscriber, what
 * the current local hour actually is in their timezone right now
 * (via Intl.DateTimeFormat, which is DST-aware) and compares it to
 * their chosen hour. This is what makes delivery time survive DST
 * transitions automatically instead of drifting by an hour twice a
 * year, which a precomputed-UTC-hour-at-subscribe-time approach would
 * not. The actual notification content (today's devotional) is
 * fetched by the client's service worker at delivery time from that
 * site's own devotionals.json — this worker never needs to know which
 * site a subscriber came from.
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

// Byte-for-byte !== leaks how many leading characters matched via response
// timing — cheap to exploit against a low-traffic worker with no other
// load. Comparing SHA-256 digests instead means every comparison does the
// same fixed amount of work regardless of where (or whether) the inputs
// diverge, and sidesteps the length-leak a naive char-by-char loop would
// still have.
async function timingSafeEqual(a, b) {
  const enc = new TextEncoder();
  const [da, db] = await Promise.all([
    crypto.subtle.digest('SHA-256', enc.encode(a)),
    crypto.subtle.digest('SHA-256', enc.encode(b)),
  ]);
  const va = new Uint8Array(da), vb = new Uint8Array(db);
  let diff = 0;
  for (let i = 0; i < va.length; i++) diff |= va[i] ^ vb[i];
  return diff === 0;
}

// Reuses the PUSH_SUBS KV namespace that's already provisioned rather than
// adding a separate rate-limiting binding — one fewer thing to configure
// in the Cloudflare dashboard. A KV write per request is more overhead
// than a dedicated rate-limiting API, but at this traffic scale that's
// not a real cost, and it keeps deployment to just `wrangler deploy`.
async function isRateLimited(env, ip, bucket, limit, windowSeconds) {
  const key = `ratelimit:${bucket}:${ip}`;
  const raw = await env.PUSH_SUBS.get(key);
  const count = raw ? parseInt(raw, 10) : 0;
  if (count >= limit) return true;
  await env.PUSH_SUBS.put(key, String(count + 1), { expirationTtl: windowSeconds });
  return false;
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

// --- timezone helpers ---

function isValidTimezone(tz) {
  if (typeof tz !== 'string' || !tz) return false;
  try {
    new Intl.DateTimeFormat('en-US', { timeZone: tz });
    return true;
  } catch (e) {
    return false;
  }
}

const DEFAULT_TIMEZONE = 'America/New_York';

// The current local hour (0-23) in an IANA timezone, right now. DST-aware
// by construction — Intl resolves the real tz-database offset for "now" in
// that zone, so this doesn't need any manual DST bookkeeping.
function currentLocalHourInTimezone(tz) {
  try {
    const parts = new Intl.DateTimeFormat('en-US', {
      timeZone: tz,
      hour: 'numeric',
      hourCycle: 'h23'
    }).formatToParts(new Date());
    const hourPart = parts.find(p => p.type === 'hour');
    return hourPart ? parseInt(hourPart.value, 10) : null;
  } catch (e) {
    return null;
  }
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
// mode 'matchNow' (used by the real hourly cron): for each subscription,
// compute the current local hour in ITS OWN stored timezone and only send
// if that equals the subscriber's chosen localHour — this is what lets
// each subscriber pick their own reminder time, correctly, across DST.
// mode 'sendToAll' (used by /send-now for on-demand testing): ignore the
// per-subscriber hour entirely and send to everyone right now.
async function sendPush(env, mode) {
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

    if (mode !== 'sendToAll') {
      const nowLocalHour = currentLocalHourInTimezone(sub.timezone);
      if (nowLocalHour === null || nowLocalHour !== sub.localHour) continue;
    }
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
    // knows. By default sends to everyone right now regardless of their
    // chosen hour (useful for an immediate delivery test); pass
    // {"simulateHourlyMatch": true} to instead run the exact per-subscriber
    // timezone/hour matching logic the real hourly cron uses, without
    // waiting for the top of the hour.
    if (url.pathname === '/send-now') {
      const provided = request.headers.get('X-Admin-Secret') || '';
      if (!env.ADMIN_SECRET || !(await timingSafeEqual(provided, env.ADMIN_SECRET))) {
        return new Response(JSON.stringify({ error: 'Forbidden' }), {
          status: 403, headers: { 'Content-Type': 'application/json' }
        });
      }
      let mode = 'sendToAll';
      try {
        const testBody = await request.json();
        if (testBody && testBody.simulateHourlyMatch) mode = 'matchNow';
      } catch (e) { /* no body, or not JSON — fine, default to sendToAll */ }
      const summary = await sendPush(env, mode);
      return new Response(JSON.stringify(summary), {
        status: 200, headers: { 'Content-Type': 'application/json' }
      });
    }

    if (!originAllowed(request)) {
      return jsonResponse({ error: 'Forbidden' }, 403, request);
    }

    // Origin/Referer checks only stop browser-issued requests — a script
    // can set either header to whatever it likes. Without this, /subscribe
    // is an open write to PUSH_SUBS: unlimited junk KV entries at whatever
    // rate someone wants to send them. 30 writes/hour per IP is generous
    // for a real subscriber changing their reminder time, not for a spammer.
    const clientIp = request.headers.get('CF-Connecting-IP') || 'unknown';
    if (await isRateLimited(env, clientIp, 'sub', 30, 3600)) {
      return jsonResponse({ error: 'Too many requests' }, 429, request);
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
      // localHour (0-23) + timezone (IANA name, e.g. "America/New_York")
      // are the subscriber's own chosen reminder time, exactly as they
      // picked it — no client-side UTC conversion. The worker recomputes
      // what that means in UTC fresh on every hourly tick, so this stays
      // correct across DST without ever needing to be resaved.
      let localHour = Number.isInteger(body.localHour) ? body.localHour : 8;
      if (localHour < 0 || localHour > 23) localHour = 8;
      const timezone = isValidTimezone(body.timezone) ? body.timezone : DEFAULT_TIMEZONE;
      const record = { endpoint: body.endpoint, keys: body.keys, localHour, timezone };
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

    // Fired by the service worker's pushsubscriptionchange handler when the
    // browser/OS silently rotates a subscriber's push endpoint (this does
    // happen periodically, especially on iOS) — without this, the old
    // endpoint eventually starts returning 404/410, sendPush() deletes it,
    // and the subscriber silently stops getting reminders forever with no
    // way to know. This preserves their chosen localHour + timezone instead
    // of resetting to the default.
    if (url.pathname === '/resubscribe') {
      if (!body || !body.endpoint || !body.keys || !body.keys.p256dh || !body.keys.auth) {
        return jsonResponse({ error: 'Invalid subscription' }, 400, request);
      }
      let localHour = 8;
      let timezone = DEFAULT_TIMEZONE;
      if (body.oldEndpoint) {
        const oldRaw = await env.PUSH_SUBS.get('sub:' + body.oldEndpoint);
        if (oldRaw) {
          try {
            const old = JSON.parse(oldRaw);
            if (Number.isInteger(old.localHour)) localHour = old.localHour;
            if (isValidTimezone(old.timezone)) timezone = old.timezone;
          } catch (e) { /* fall back to defaults */ }
          await env.PUSH_SUBS.delete('sub:' + body.oldEndpoint);
        }
      }
      const record = { endpoint: body.endpoint, keys: body.keys, localHour, timezone };
      await env.PUSH_SUBS.put('sub:' + body.endpoint, JSON.stringify(record));
      return jsonResponse({ ok: true }, 200, request);
    }

    return jsonResponse({ error: 'Not found' }, 404, request);
  },

  async scheduled(controller, env, ctx) {
    await sendPush(env, 'matchNow');
  }
};
