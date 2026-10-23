/* Finds an official recording of one chapter, so the reader's play button
   can stream it. Called from docs/site/audio.js as

       GET /functions/v1/bible-audio?t=<translation>&page=<book><chapter>

   and answers with one of

       { source: "esv",  url, credit }                       ESV API audio
       { source: "fcbh", url, timings, fileset, credit }     Bible Brain
       { source: "none", reason }                            no recording: use the device voice

   Keys are read from function secrets and never reach the browser:
   ESV_API_TOKEN (the same token the esv-proxy Cloudflare Worker uses) and
   BIBLE_BRAIN_KEY. With BIBLE_BRAIN_KEY unset, every translation but the ESV
   answers "none", which the page turns into the device voice.

   Only URLs are returned, never audio bytes. The ESV endpoint redirects to an
   MP3 and Bible Brain hands out signed CDN URLs; neither carries our key, so
   the browser streams the recording straight from its publisher. Nothing is
   generated and nothing is stored.

   Kept free of Deno globals so it can be tested under Node (see
   handler.test.mjs); index.ts is the Deno entry point.                       */

export type Env = { get(name: string): string | undefined };
type Fetch = typeof fetch;

const ALLOWED_ORIGINS = [
  "https://bible.macdwellings.com",
  "https://bible.nrc.macdwellings.com",
  "http://localhost",
  "http://127.0.0.1",
];

// USFM book codes (Bible Brain's book_id) by page slug, in canon order.
export const BOOKS: [string, string, number][] = [
  ["genesis", "GEN", 50], ["exodus", "EXO", 40], ["leviticus", "LEV", 27], ["numbers", "NUM", 36],
  ["deuteronomy", "DEU", 34], ["joshua", "JOS", 24], ["judges", "JDG", 21], ["ruth", "RUT", 4],
  ["1samuel", "1SA", 31], ["2samuel", "2SA", 24], ["1kings", "1KI", 22], ["2kings", "2KI", 25],
  ["1chronicles", "1CH", 29], ["2chronicles", "2CH", 36], ["ezra", "EZR", 10], ["nehemiah", "NEH", 13],
  ["esther", "EST", 10], ["job", "JOB", 42], ["psalms", "PSA", 150], ["proverbs", "PRO", 31],
  ["ecclesiastes", "ECC", 12], ["songofsolomon", "SNG", 8], ["isaiah", "ISA", 66], ["jeremiah", "JER", 52],
  ["lamentations", "LAM", 5], ["ezekiel", "EZK", 48], ["daniel", "DAN", 12], ["hosea", "HOS", 14],
  ["joel", "JOL", 3], ["amos", "AMO", 9], ["obadiah", "OBA", 1], ["jonah", "JON", 4], ["micah", "MIC", 7],
  ["nahum", "NAM", 3], ["habakkuk", "HAB", 3], ["zephaniah", "ZEP", 3], ["haggai", "HAG", 2],
  ["zechariah", "ZEC", 14], ["malachi", "MAL", 4],
  ["matthew", "MAT", 28], ["mark", "MRK", 16], ["luke", "LUK", 24], ["john", "JHN", 21], ["acts", "ACT", 28],
  ["romans", "ROM", 16], ["1corinthians", "1CO", 16], ["2corinthians", "2CO", 13], ["galatians", "GAL", 6],
  ["ephesians", "EPH", 6], ["philippians", "PHP", 4], ["colossians", "COL", 4], ["1thessalonians", "1TH", 5],
  ["2thessalonians", "2TH", 3], ["1timothy", "1TI", 6], ["2timothy", "2TI", 4], ["titus", "TIT", 3],
  ["philemon", "PHM", 1], ["hebrews", "HEB", 13], ["james", "JAS", 5], ["1peter", "1PE", 5], ["2peter", "2PE", 3],
  ["1john", "1JN", 5], ["2john", "2JN", 1], ["3john", "3JN", 1], ["jude", "JUD", 1], ["revelation", "REV", 22],
];
const OT_BOOKS = 39;

/* The Bible Brain Bible that is the same translation as the text on the page.
   Audio of a different translation from the text would be worse than the
   device voice, so a translation with no entry here gets no recording.

   `iso` is checked against what Bible Brain reports for the Bible, so an ID
   that turns out to be another language is refused at run time rather than
   played. Every ID below is a candidate until confirmed with a real key:
   run `python3 find_bible_brain_audio.py` and correct this table from its
   output. Translations it finds that are missing here can be added the same
   way. Codes are the site's (docs/site/translations.js).                     */
export const BIBLE_BRAIN: Record<string, { bible: string; iso: string }> = {
  KJV: { bible: "ENGKJV", iso: "eng" },
  WEB: { bible: "ENGWEB", iso: "eng" },
  FRA: { bible: "FRALSG", iso: "fra" },
  ARA: { bible: "ARBVDV", iso: "arb" },
  ZHS: { bible: "CHNUNV", iso: "cmn" },
  ZHT: { bible: "CHNUNV", iso: "cmn" },
  HIN: { bible: "HINIRV", iso: "hin" },
};

const ESV_CREDIT =
  "Scripture quotations are from the ESV® Bible (The Holy Bible, English Standard Version®), " +
  "© 2001 by Crossway, a publishing ministry of Good News Publishers. ESV audio used by permission. All rights reserved.";

export function parsePage(page: string | null): { slug: string; usfm: string; chapter: number; ot: boolean } | null {
  const m = /^(\d?[a-z]+?)(\d{1,3})$/.exec(page || "");
  if (!m) return null;
  const i = BOOKS.findIndex((b) => b[0] === m[1]);
  const chapter = parseInt(m[2], 10);
  if (i < 0 || chapter < 1 || chapter > BOOKS[i][2]) return null;
  return { slug: m[1], usfm: BOOKS[i][1], chapter, ot: i < OT_BOOKS };
}

// "1samuel" -> "1 Samuel", "songofsolomon" -> "Song of Solomon"
export function esvName(slug: string): string {
  if (slug === "songofsolomon") return "Song of Solomon";
  const m = /^(\d?)([a-z]+)$/.exec(slug)!;
  return (m[1] ? m[1] + " " : "") + m[2][0].toUpperCase() + m[2].slice(1);
}

function cors(req: Request): Record<string, string> {
  const origin = req.headers.get("Origin") || "";
  return {
    "Access-Control-Allow-Origin": ALLOWED_ORIGINS.some((o) => origin.startsWith(o)) ? origin : ALLOWED_ORIGINS[0],
    "Access-Control-Allow-Methods": "GET, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Max-Age": "86400",
    Vary: "Origin",
  };
}

function json(req: Request, body: unknown, status = 200, maxAge = 0): Response {
  return new Response(JSON.stringify(body), {
    status,
    headers: {
      "Content-Type": "application/json",
      // private: the answer is gated by the origin check, so no shared cache may hold it
      "Cache-Control": maxAge ? `private, max-age=${maxAge}` : "no-store",
      ...cors(req),
    },
  });
}

// Same rule as esv-proxy-worker: the Origin, or failing that the Referer, must be one of ours.
function allowed(req: Request): boolean {
  const origin = req.headers.get("Origin") || "";
  const referer = req.headers.get("Referer") || "";
  if (origin) return ALLOWED_ORIGINS.some((o) => origin.startsWith(o));
  return !!referer && ALLOWED_ORIGINS.some((o) => referer.startsWith(o));
}

/* ---------- ESV ---------- */

async function esv(env: Env, f: Fetch, slug: string, chapter: number) {
  const token = env.get("ESV_API_TOKEN");
  if (!token) return { source: "none", reason: "esv-not-configured" };
  const q = `${esvName(slug)} ${chapter}`;
  const url = `https://api.esv.org/v3/passage/audio/?q=${encodeURIComponent(q)}`;
  // The endpoint answers with a redirect to the MP3. Read the redirect target
  // rather than following it, so the browser streams the MP3 itself and this
  // function never downloads audio.
  const res = await f(url, { headers: { Authorization: `Token ${token}` }, redirect: "manual" });
  const location = res.headers.get("Location");
  await res.body?.cancel();
  if (res.status >= 300 && res.status < 400 && location) {
    return { source: "esv", url: new URL(location, url).href, credit: { text: ESV_CREDIT, link: "https://www.esv.org" } };
  }
  return { source: "none", reason: `esv-${res.status}` };
}

/* ---------- Bible Brain ---------- */

const BB = "https://4.dbt.io/api";
// Bible metadata and copyright change rarely; keep them for the life of the isolate.
const memo = new Map<string, Promise<unknown>>();

async function bb(f: Fetch, key: string, path: string, params: Record<string, string> = {}) {
  const qs = new URLSearchParams({ v: "4", key, ...params });
  const res = await f(`${BB}${path}?${qs}`, { headers: { Accept: "application/json" } });
  if (!res.ok) {
    await res.body?.cancel();
    throw new Error(`bible-brain ${res.status} ${path}`);
  }
  return res.json();
}

function remembered(k: string, load: () => Promise<unknown>): Promise<any> {
  if (!memo.has(k)) memo.set(k, load().catch((e) => { memo.delete(k); throw e; }));
  return memo.get(k)!;
}

type Fileset = { id: string; type: string; size: string };

// Every MP3 fileset that covers this testament, best first: non-drama before
// drama, complete before portions, MP3 before Opus.
export function rankFilesets(filesets: Fileset[], ot: boolean): Fileset[] {
  const covers = (size: string) => size === "C" || size.includes(ot ? "OT" : "NT");
  const score = (fs: Fileset) =>
    (fs.type === "audio" ? 0 : 10) + (/P/.test(fs.size) ? 1 : 0) + (fs.id.includes("-") ? 5 : 0);
  return filesets
    .filter((fs) => (fs.type === "audio" || fs.type === "audio_drama") && covers(fs.size || ""))
    .sort((a, b) => score(a) - score(b));
}

function allFilesets(bible: any): Fileset[] {
  const out: Fileset[] = [];
  const groups = (bible && bible.filesets) || {};
  for (const k of Object.keys(groups)) {
    for (const fs of groups[k] || []) if (fs && fs.id) out.push({ id: fs.id, type: fs.type || "", size: fs.size || "" });
  }
  return out;
}

async function fcbh(env: Env, f: Fetch, trans: string, usfm: string, chapter: number, ot: boolean) {
  const key = env.get("BIBLE_BRAIN_KEY");
  if (!key) return { source: "none", reason: "bible-brain-not-configured" };
  const entry = BIBLE_BRAIN[trans];
  if (!entry) return { source: "none", reason: "no-bible-brain-match" };

  const bible = (await remembered(`bible:${entry.bible}`, () => bb(f, key, `/bibles/${entry.bible}`))).data;
  if (!bible || (bible.iso && bible.iso !== entry.iso)) return { source: "none", reason: "bible-brain-language-mismatch" };

  for (const fs of rankFilesets(allFilesets(bible), ot)) {
    const chap = await bb(f, key, `/bibles/filesets/${fs.id}/${usfm}/${chapter}`).catch(() => null);
    const file = chap && (chap.data || []).find((d: any) => d && typeof d.path === "string");
    // Section-segmented filesets answer with an HLS playlist, which only Safari plays natively.
    if (!file || /\.m3u8(\?|$)/.test(file.path)) continue;

    const [stamps, rights] = await Promise.all([
      bb(f, key, `/timestamps/${fs.id}/${usfm}/${chapter}`).catch(() => null),
      remembered(`copyright:${entry.bible}`, () => bb(f, key, `/bibles/${entry.bible}/copyright`, { iso: "eng" })).catch(() => null),
    ]);
    const timings = ((stamps && stamps.data) || [])
      .map((t: any) => [parseInt(t.verse_start, 10), Number(t.timestamp)])
      .filter((t: number[]) => t[0] > 0 && isFinite(t[1]))
      .sort((a: number[], b: number[]) => a[1] - b[1]);
    const row = (Array.isArray(rights) ? rights : (rights && rights.data) || []).find((r: any) => r && r.id === fs.id);
    const copyright = (row && row.copyright && row.copyright.copyright) || "";

    return {
      source: "fcbh",
      url: file.path,
      fileset: fs.id,
      drama: fs.type === "audio_drama",
      timings,
      credit: {
        text: (copyright ? copyright.trim() + " " : "") + "Audio provided by Faith Comes By Hearing through Bible Brain.",
        link: "https://www.faithcomesbyhearing.com",
      },
    };
  }
  return { source: "none", reason: "no-audio-for-chapter" };
}

/* ---------- entry ---------- */

// Bible Brain's signed URLs expire, so its answers are kept briefly; the
// ESV's redirect target is stable. A settled "no recording" is kept a day, so
// such a translation costs one lookup per chapter per day rather than one per
// tap. Anything that might change soon (a key not yet set, an ESV rate limit)
// is kept five minutes.
const SETTLED_NONE = new Set(["no-bible-brain-match", "bible-brain-language-mismatch", "no-audio-for-chapter"]);
function maxAge(out: { source: string; reason?: string }): number {
  if (out.source === "fcbh") return 1800;
  if (out.source === "esv") return 86400;
  return SETTLED_NONE.has(out.reason || "") ? 86400 : 300;
}

export async function handle(req: Request, env: Env, f: Fetch = fetch): Promise<Response> {
  if (req.method === "OPTIONS") return new Response(null, { status: 204, headers: cors(req) });
  if (req.method !== "GET") return json(req, { error: "Method not allowed" }, 405);
  if (!allowed(req)) return json(req, { error: "Forbidden" }, 403);

  const params = new URL(req.url).searchParams;
  const trans = (params.get("t") || "").toUpperCase();
  const where = parsePage(params.get("page"));
  if (!/^[A-Z0-9]{2,5}$/.test(trans) || !where) return json(req, { error: "Expected ?t=<translation>&page=<book><chapter>" }, 400);

  try {
    const out = trans === "ESV"
      ? await esv(env, f, where.slug, where.chapter)
      : await fcbh(env, f, trans, where.usfm, where.chapter, where.ot);
    return json(req, out, 200, maxAge(out));
  } catch (e) {
    console.error(e);
    return json(req, { source: "none", reason: "lookup-failed" }, 502);
  }
}
