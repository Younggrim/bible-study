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

// Streak reminders: at this local hour, anyone with reminders on whose study
// streak ends tonight (they studied yesterday but not yet today) gets one
// nudge. The page reports the streak to /studied each time a chapter is
// marked; the worker never sees what was read, only the date and the count.
const STREAK_HOUR = 19;

// Friend notifications. A device that has reminders on and is signed in is
// linked to its Supabase account (/link), so when a friend sends a request
// or shares a verse or note (/notify), their friends' devices get a push.
// Both endpoints prove who is calling with the person's own Supabase access
// token, checked against Supabase itself; the worker holds no secret for it.
// These two values are public by design (the site's own account.js has them).
const SUPABASE_URL = 'https://vqgumrfjxlhkzzzfgejl.supabase.co';
const SUPABASE_KEY = 'sb_publishable_pG2kmWU11t4FShA7JpiHFQ_kpxBoRbW';
const QUEUE_TTL = 3 * 3600 * 1000;

async function supabase(path, jwt, init) {
  const resp = await fetch(SUPABASE_URL + path, Object.assign({}, init, {
    headers: Object.assign({ apikey: SUPABASE_KEY, Authorization: 'Bearer ' + jwt, 'Content-Type': 'application/json' }, (init && init.headers) || {})
  }));
  if (!resp.ok) return null;
  return resp.json();
}
async function userFromJwt(jwt) {
  if (typeof jwt !== 'string' || jwt.length < 20 || jwt.length > 4096) return null;
  const u = await supabase('/auth/v1/user', jwt);
  return u && typeof u.id === 'string' ? u.id : null;
}

// Each subscription keeps a short queue of what its next pushes are about;
// the service worker reads the front of it through /message.
function enqueue(sub, item) {
  const now = Date.now();
  const q = (Array.isArray(sub.queue) ? sub.queue : []).filter(x => now - x.at < QUEUE_TTL);
  q.push(Object.assign({ at: now }, item));
  sub.queue = q.slice(-5);
}
const DAY_RE = /^\d{4}-\d{2}-\d{2}$/;

// The calendar date (YYYY-MM-DD) in an IANA timezone, offsetDays from now.
function localDate(tz, offsetDays) {
  try {
    return new Intl.DateTimeFormat('en-CA', { timeZone: tz, year: 'numeric', month: '2-digit', day: '2-digit' })
      .format(new Date(Date.now() + (offsetDays || 0) * 86400000));
  } catch (e) {
    return null;
  }
}

function streakDue(sub, hour) {
  if (hour !== STREAK_HOUR || sub.streakReminders === false) return false;
  if (!Number.isInteger(sub.streak) || sub.streak < 2 || !sub.lastStudied) return false;
  const today = localDate(sub.timezone, 0), yesterday = localDate(sub.timezone, -1);
  return sub.lastStudied === yesterday && sub.streakNotified !== today;
}

// Fields a subscriber's record carries beyond the push subscription itself,
// kept when they change their reminder time or the browser rotates endpoints.
function carryOver(old) {
  const out = {};
  if (!old) return out;
  for (const k of ['lastStudied', 'streak', 'streakNotified', 'streakReminders', 'streakText', 'userId', 'friendAlerts']) {
    if (old[k] !== undefined) out[k] = old[k];
  }
  return out;
}

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
async function deliver(env, privateKey, keyName, sub) {
  let audience;
  try {
    audience = new URL(sub.endpoint).origin;
  } catch (e) {
    return 'failed';
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
      await env.PUSH_SUBS.delete(keyName);
      return 'expired';
    }
    return (resp.ok || resp.status === 201) ? 'sent' : 'failed';
  } catch (e) {
    // Network error reaching this push service — leave the subscription
    // in place and try again on the next scheduled run.
    return 'failed';
  }
}

// Shared by the hourly cron and the manual /send-now debug endpoint.
// mode 'matchNow' (used by the real hourly cron): for each subscription,
// compute the current local hour in ITS OWN stored timezone and only send
// if that equals the subscriber's chosen localHour — this is what lets
// each subscriber pick their own reminder time, correctly, across DST.
// The same pass sends the evening streak reminder (see streakDue).
// mode 'sendToAll' (used by /send-now for on-demand testing): ignore the
// per-subscriber hour entirely and send the devotional to everyone right now.
//
// Pushes carry no payload. The service worker asks /message what to show:
// a pending streak reminder if one was just queued, otherwise the devotional.
async function sendPush(env, mode) {
  const privateKey = await importVapidPrivateKey(env.VAPID_PUBLIC_KEY, env.VAPID_PRIVATE_KEY);
  const list = await env.PUSH_SUBS.list({ prefix: 'sub:' });
  const summary = { total: 0, matched: 0, sent: 0, expired: 0, failed: 0, streak: 0 };

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

    const hour = currentLocalHourInTimezone(sub.timezone);
    if (mode === 'sendToAll' || (hour !== null && hour === sub.localHour)) {
      summary.matched++;
      const r = await deliver(env, privateKey, key.name, sub);
      summary[r]++;
      if (r === 'expired') continue;
    }

    if (mode !== 'sendToAll' && streakDue(sub, hour)) {
      enqueue(sub, { type: 'streak' });
      sub.streakNotified = localDate(sub.timezone, 0);
      await env.PUSH_SUBS.put(key.name, JSON.stringify(sub));
      const r = await deliver(env, privateKey, key.name, sub);
      summary[r]++;
      if (r === 'sent') summary.streak++;
    }
  }

  return summary;
}

async function unlinkUser(env, uid, endpoint) {
  const list = JSON.parse(await env.PUSH_SUBS.get('user:' + uid) || '[]').filter(e => e !== endpoint);
  if (list.length) await env.PUSH_SUBS.put('user:' + uid, JSON.stringify(list));
  else await env.PUSH_SUBS.delete('user:' + uid);
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
      let prior = null;
      try { prior = JSON.parse(await env.PUSH_SUBS.get('sub:' + body.endpoint) || 'null'); } catch (e) { /* new subscriber */ }
      const record = Object.assign(carryOver(prior), { endpoint: body.endpoint, keys: body.keys, localHour, timezone });
      await env.PUSH_SUBS.put('sub:' + body.endpoint, JSON.stringify(record));
      return jsonResponse({ ok: true }, 200, request);
    }

    if (url.pathname === '/unsubscribe') {
      if (!body || !body.endpoint) {
        return jsonResponse({ error: 'Missing endpoint' }, 400, request);
      }
      const prev = await env.PUSH_SUBS.get('sub:' + body.endpoint);
      if (prev) { try { const p = JSON.parse(prev); if (p.userId) await unlinkUser(env, p.userId, body.endpoint); } catch (e) { /* nothing to unlink */ } }
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
      let kept = {};
      if (body.oldEndpoint) {
        const oldRaw = await env.PUSH_SUBS.get('sub:' + body.oldEndpoint);
        if (oldRaw) {
          try {
            const old = JSON.parse(oldRaw);
            if (Number.isInteger(old.localHour)) localHour = old.localHour;
            if (isValidTimezone(old.timezone)) timezone = old.timezone;
            kept = carryOver(old);
          } catch (e) { /* fall back to defaults */ }
          await env.PUSH_SUBS.delete('sub:' + body.oldEndpoint);
        }
      }
      const record = Object.assign(kept, { endpoint: body.endpoint, keys: body.keys, localHour, timezone });
      await env.PUSH_SUBS.put('sub:' + body.endpoint, JSON.stringify(record));
      return jsonResponse({ ok: true }, 200, request);
    }

    // The page reports the reader's streak after each chapter they mark, so
    // the evening reminder knows whether tonight is the night it would end.
    // Only updates an existing subscription; it never creates one.
    if (url.pathname === '/studied') {
      if (!body || !body.endpoint || !DAY_RE.test(body.day || '') || !Number.isInteger(body.streak) || body.streak < 0 || body.streak > 100000) {
        return jsonResponse({ error: 'Invalid' }, 400, request);
      }
      const raw = await env.PUSH_SUBS.get('sub:' + body.endpoint);
      if (!raw) return jsonResponse({ ok: false, subscribed: false }, 200, request);
      const sub = JSON.parse(raw);
      sub.lastStudied = body.day;
      sub.streak = body.streak;
      if (typeof body.text === 'string') sub.streakText = body.text.slice(0, 200);
      await env.PUSH_SUBS.put('sub:' + body.endpoint, JSON.stringify(sub));
      return jsonResponse({ ok: true }, 200, request);
    }

    // Turn the evening streak reminder or friend alerts on or off without
    // touching the daily devotional reminder.
    if (url.pathname === '/preferences') {
      if (!body || !body.endpoint || (typeof body.streakReminders !== 'boolean' && typeof body.friendAlerts !== 'boolean')) {
        return jsonResponse({ error: 'Invalid' }, 400, request);
      }
      const raw = await env.PUSH_SUBS.get('sub:' + body.endpoint);
      if (!raw) return jsonResponse({ ok: false, subscribed: false }, 200, request);
      const sub = JSON.parse(raw);
      if (typeof body.streakReminders === 'boolean') sub.streakReminders = body.streakReminders;
      if (typeof body.friendAlerts === 'boolean') sub.friendAlerts = body.friendAlerts;
      await env.PUSH_SUBS.put('sub:' + body.endpoint, JSON.stringify(sub));
      return jsonResponse({ ok: true }, 200, request);
    }

    // Asked by the service worker when a push arrives: which notification is
    // this one? A streak reminder queued in the last three hours, or the
    // devotional. Reading it clears it, so it is shown once.
    if (url.pathname === '/message') {
      if (!body || !body.endpoint) return jsonResponse({ type: 'devotional' }, 200, request);
      const raw = await env.PUSH_SUBS.get('sub:' + body.endpoint);
      if (!raw) return jsonResponse({ type: 'devotional' }, 200, request);
      const sub = JSON.parse(raw);
      const now = Date.now();
      const q = (Array.isArray(sub.queue) ? sub.queue : []).filter(x => now - x.at < QUEUE_TTL);
      if (sub.pending && sub.pending.type === 'streak' && now - sub.pending.at < QUEUE_TTL) q.unshift(sub.pending);   // queued before the queue existed
      delete sub.pending;
      const item = q.shift();
      sub.queue = q;
      await env.PUSH_SUBS.put('sub:' + body.endpoint, JSON.stringify(sub));
      if (!item) return jsonResponse({ type: 'devotional' }, 200, request);
      if (item.type === 'streak') return jsonResponse({ type: 'streak', streak: sub.streak || 0, text: sub.streakText || '' }, 200, request);
      return jsonResponse({ type: 'friend', title: item.title, body: item.body, url: item.url || '/friends.html' }, 200, request);
    }

    // Tie this device's subscription to the signed-in account, so friend
    // activity can reach it. Re-sent by the page now and then; harmless.
    if (url.pathname === '/link') {
      if (!body || !body.endpoint) return jsonResponse({ error: 'Invalid' }, 400, request);
      const uid = await userFromJwt(body.jwt);
      if (!uid) return jsonResponse({ error: 'Not signed in' }, 401, request);
      const raw = await env.PUSH_SUBS.get('sub:' + body.endpoint);
      if (!raw) return jsonResponse({ ok: false, subscribed: false }, 200, request);
      const sub = JSON.parse(raw);
      if (sub.userId && sub.userId !== uid) await unlinkUser(env, sub.userId, body.endpoint);
      sub.userId = uid;
      if (typeof body.friendAlerts === 'boolean') sub.friendAlerts = body.friendAlerts;
      await env.PUSH_SUBS.put('sub:' + body.endpoint, JSON.stringify(sub));
      const list = JSON.parse(await env.PUSH_SUBS.get('user:' + uid) || '[]').filter(e => e !== body.endpoint);
      list.push(body.endpoint);
      await env.PUSH_SUBS.put('user:' + uid, JSON.stringify(list.slice(-10)));
      return jsonResponse({ ok: true }, 200, request);
    }

    // Signing out on a device stops friend pushes to it.
    if (url.pathname === '/unlink') {
      if (!body || !body.endpoint) return jsonResponse({ error: 'Invalid' }, 400, request);
      const raw = await env.PUSH_SUBS.get('sub:' + body.endpoint);
      if (raw) {
        const sub = JSON.parse(raw);
        if (sub.userId) await unlinkUser(env, sub.userId, body.endpoint);
        delete sub.userId;
        await env.PUSH_SUBS.put('sub:' + body.endpoint, JSON.stringify(sub));
      }
      return jsonResponse({ ok: true }, 200, request);
    }

    // A friend request was sent, or something was shared: tell the people it
    // concerns. Who they are comes from Supabase, asked as the sender, so a
    // caller can only ever reach their own accepted friends (for a share) or
    // the people they have a pending request with (for a request).
    if (url.pathname === '/notify') {
      if (!body || (body.type !== 'share' && body.type !== 'request')) return jsonResponse({ error: 'Invalid' }, 400, request);
      const uid = await userFromJwt(body.jwt);
      if (!uid) return jsonResponse({ error: 'Not signed in' }, 401, request);
      const [people, me] = await Promise.all([
        supabase('/rest/v1/rpc/friends_list', body.jwt, { method: 'POST', body: '{}' }),
        supabase('/rest/v1/friend_profiles?select=display_name&user_id=eq.' + encodeURIComponent(uid), body.jwt)
      ]);
      const name = (Array.isArray(me) && me[0] && me[0].display_name) || 'A friend';
      if (!Array.isArray(people)) return jsonResponse({ ok: false }, 200, request);
      let targets, item;
      if (body.type === 'share') {
        targets = people.filter(p => p.status === 'accepted').map(p => p.friend);
        const what = body.kind === 'note' ? 'a note' : 'a verse';
        const title = typeof body.title === 'string' ? body.title.slice(0, 80) : '';
        item = { type: 'friend', title: name + ' shared ' + what, body: title || 'Open Friends to see it.', url: '/friends.html' };
      } else {
        targets = [];
        for (const p of people.filter(x => x.status === 'pending' && !x.incoming)) {
          const k = 'notified:' + uid + ':' + p.friend;
          if (await env.PUSH_SUBS.get(k)) continue;
          await env.PUSH_SUBS.put(k, '1', { expirationTtl: 30 * 86400 });
          targets.push(p.friend);
        }
        item = { type: 'friend', title: 'New friend request', body: name + ' wants to study the Bible with you.', url: '/friends.html' };
      }
      const privateKey = await importVapidPrivateKey(env.VAPID_PUBLIC_KEY, env.VAPID_PRIVATE_KEY);
      let sent = 0;
      for (const t of targets.slice(0, 200)) {
        const endpoints = JSON.parse(await env.PUSH_SUBS.get('user:' + t) || '[]');
        for (const ep of endpoints) {
          const raw = await env.PUSH_SUBS.get('sub:' + ep);
          if (!raw) continue;
          const sub = JSON.parse(raw);
          if (sub.friendAlerts === false) continue;
          enqueue(sub, item);
          await env.PUSH_SUBS.put('sub:' + ep, JSON.stringify(sub));
          if ((await deliver(env, privateKey, 'sub:' + ep, sub)) === 'sent') sent++;
        }
      }
      return jsonResponse({ ok: true, sent }, 200, request);
    }

    return jsonResponse({ error: 'Not found' }, 404, request);
  },

  async scheduled(controller, env, ctx) {
    await sendPush(env, 'matchNow');
  }
};
