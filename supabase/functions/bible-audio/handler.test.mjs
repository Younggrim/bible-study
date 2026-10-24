// node --experimental-strip-types --test supabase/functions/bible-audio/handler.test.mjs
// Runs handler.ts against a fake fetch: no keys and no network needed.
import test from "node:test";
import assert from "node:assert/strict";
import { handle, parsePage, esvName, rankFilesets } from "./handler.ts";

const ORIGIN = "https://bible.macdwellings.com";
const env = (vars) => ({ get: (k) => vars[k] });
const req = (qs, headers = { Origin: ORIGIN }) => new Request(`https://x.supabase.co/functions/v1/bible-audio?${qs}`, { headers });
const body = async (res) => [res.status, await res.json()];

function fakeFetch(routes) {
  const calls = [];
  const f = async (url, init = {}) => {
    calls.push({ url: String(url), init });
    for (const [match, reply] of routes) if (String(url).includes(match)) return reply(String(url), init);
    return new Response("not found", { status: 404 });
  };
  f.calls = calls;
  return f;
}
const ok = (data) => () => new Response(JSON.stringify(data), { status: 200, headers: { "Content-Type": "application/json" } });

test("pages and ESV names", () => {
  assert.deepEqual(parsePage("john3"), { slug: "john", usfm: "JHN", chapter: 3, ot: false });
  assert.deepEqual(parsePage("1samuel2"), { slug: "1samuel", usfm: "1SA", chapter: 2, ot: true });
  assert.equal(parsePage("john22"), null);
  assert.equal(parsePage("../etc"), null);
  assert.equal(esvName("songofsolomon"), "Song of Solomon");
  assert.equal(esvName("1samuel"), "1 Samuel");
  assert.equal(esvName("psalms"), "Psalms");
});

test("rejects other origins and bad input", async () => {
  const f = fakeFetch([]);
  assert.equal((await handle(req("t=ESV&page=john3", { Origin: "https://evil.example" }), env({}), f)).status, 403);
  assert.equal((await handle(req("t=ESV&page=john3", { Origin: "https://bible.macdwellings.com.evil.example" }), env({}), f)).status, 403);
  assert.equal((await handle(req("t=ESV&page=john3", { Origin: "http://localhost.evil.example" }), env({}), f)).status, 403);
  assert.equal((await handle(req("t=ESV&page=john3", { Referer: "https://bible.macdwellings.com.evil.example/x" }), env({}), f)).status, 403);
  assert.equal((await handle(req("t=ESV&page=john3", {}), env({}), f)).status, 403);
  assert.equal((await handle(req("t=ESV&page=nope1"), env({}), f)).status, 400);
  assert.equal(f.calls.length, 0);
});

test("ESV: reads the redirect, sends the token, never downloads audio", async () => {
  const f = fakeFetch([["api.esv.org/v3/passage/audio", () => new Response(null, { status: 302, headers: { Location: "https://audio.esv.org/hw/43003001-43003036.mp3" } })]]);
  const [status, out] = await body(await handle(req("t=ESV&page=john3"), env({ ESV_API_TOKEN: "secret" }), f));
  assert.equal(status, 200);
  assert.equal(out.source, "esv");
  assert.equal(out.url, "https://audio.esv.org/hw/43003001-43003036.mp3");
  assert.match(out.credit.text, /Crossway/);
  assert.equal(f.calls[0].init.redirect, "manual");
  assert.equal(f.calls[0].init.headers.Authorization, "Token secret");
  assert.match(f.calls[0].url, /q=John%203$/);
  assert.ok(!JSON.stringify(out).includes("secret"));
});

test("ESV without a token or with an API error answers none, cached briefly", async () => {
  let res = await handle(req("t=ESV&page=john3"), env({}), fakeFetch([]));
  assert.deepEqual(await res.json(), { source: "none", reason: "esv-not-configured" });
  res = await handle(req("t=ESV&page=john3"), env({ ESV_API_TOKEN: "k" }), fakeFetch([["esv.org", () => new Response("", { status: 429 })]]));
  assert.equal((await res.json()).reason, "esv-429");
  assert.equal(res.headers.get("Cache-Control"), "private, max-age=300");
});

test("no Bible Brain key: none without calling anything", async () => {
  const f = fakeFetch([]);
  const [, out] = await body(await handle(req("t=KJV&page=john3"), env({}), f));
  assert.deepEqual(out, { source: "none", reason: "bible-brain-not-configured" });
  assert.equal(f.calls.length, 0);
});

test("translation with no Bible Brain match: none", async () => {
  const [, out] = await body(await handle(req("t=BSB&page=john3"), env({ BIBLE_BRAIN_KEY: "k" }), fakeFetch([])));
  assert.equal(out.reason, "no-bible-brain-match");
});

test("Bible Brain: prefers non-drama MP3, returns timings and copyright", async () => {
  const f = fakeFetch([
    ["/bibles/ENGKJV/copyright", ok([{ id: "ENGKJVN1DA", copyright: { copyright: "Audio ℗ Hosanna" } }])],
    ["/bibles/ENGKJV?", ok({ data: { abbr: "ENGKJV", iso: "eng", filesets: { "dbp-prod": [
      { id: "ENGKJVN2DA", type: "audio_drama", size: "NT" },
      { id: "ENGKJVN1DA-opus16", type: "audio", size: "NT" },
      { id: "ENGKJVO1DA", type: "audio", size: "OT" },
      { id: "ENGKJVN1DA", type: "audio", size: "NT" },
      { id: "ENGKJVN1SA", type: "audio_stream", size: "NT" },
    ] } } })],
    ["/bibles/filesets/ENGKJVN1DA/JHN/3", ok({ data: [{ book_id: "JHN", path: "https://d1.cloudfront.net/JHN3.mp3?Signature=x" }] })],
    ["/timestamps/ENGKJVN1DA/JHN/3", ok({ data: [{ verse_start: "2", timestamp: 9.5 }, { verse_start: "1", timestamp: 0 }] })],
  ]);
  const [status, out] = await body(await handle(req("t=KJV&page=john3"), env({ BIBLE_BRAIN_KEY: "bbkey" }), f));
  assert.equal(status, 200);
  assert.equal(out.source, "fcbh");
  assert.equal(out.fileset, "ENGKJVN1DA");
  assert.equal(out.drama, false);
  assert.deepEqual(out.timings, [[1, 0], [2, 9.5]]);
  assert.match(out.credit.text, /Hosanna.*Faith Comes By Hearing/);
  assert.ok(!JSON.stringify(out).includes("bbkey"));
  assert.ok(!f.calls.some((c) => c.url.includes("ENGKJVO1DA")), "OT fileset not tried for John");
});

test("Bible Brain: falls back to drama, skips HLS, refuses another language", async () => {
  const filesets = { data: { iso: "eng", filesets: { "dbp-prod": [
    { id: "ENGWEBN1DA", type: "audio", size: "NTP" },
    { id: "ENGWEBN2DA", type: "audio_drama", size: "NT" },
  ] } } };
  let f = fakeFetch([
    ["/bibles/ENGWEB?", ok(filesets)],
    ["/bibles/filesets/ENGWEBN1DA/", ok({ data: [{ path: "https://cdn/x.m3u8" }] })],
    ["/bibles/filesets/ENGWEBN2DA/", ok({ data: [{ path: "https://cdn/x.mp3" }] })],
  ]);
  let [, out] = await body(await handle(req("t=WEB&page=mark1"), env({ BIBLE_BRAIN_KEY: "k" }), f));
  assert.equal(out.fileset, "ENGWEBN2DA");
  assert.equal(out.drama, true);
  assert.deepEqual(out.timings, []);

  f = fakeFetch([["/bibles/FRALSG?", ok({ data: { iso: "deu", filesets: {} } })]]);
  [, out] = await body(await handle(req("t=FRA&page=mark1"), env({ BIBLE_BRAIN_KEY: "k" }), f));
  assert.equal(out.reason, "bible-brain-language-mismatch");
});

test("rankFilesets ordering", () => {
  const ids = rankFilesets([
    { id: "A2DA", type: "audio_drama", size: "C" },
    { id: "A1DA", type: "audio", size: "NTP" },
    { id: "B1DA", type: "audio", size: "C" },
  ], false).map((f) => f.id);
  assert.deepEqual(ids, ["B1DA", "A1DA", "A2DA"]);
});
