#!/usr/bin/env python3
"""Build the data files behind site search (search.html, site/search.js).

Writes three files into docs/site/search/:

    topics.json   Stories & Topics: the hand-picked names in search_topics.py
                  (parables, miracles, Bible stories, well-known teachings),
                  each resolved to a chapter page and verse. Small; loaded first.
    site.json     Studies: every section of the topical and life studies, every
                  chapter's summary, section titles, key themes and Deep Dive
                  headings, and the devotionals. Loaded when a search runs.
    bible.json    Verses: the Berean Standard Bible text, read out of the BSB
                  block already baked into every chapter page. BSB is public
                  domain, so unlike the ESV it can be stored and searched on
                  the device, offline, with no API quota.

Every reference and study link in search_topics.py is checked against the real
pages; the build fails, writing nothing, if any does not resolve.

    python3 build_search.py           # write
    python3 build_search.py --check   # report only

Run it after adding chapters, Deep Dives, study pages, devotionals or topics,
then sync New River as usual (the files mirror like anything under docs/site/).
"""
import hashlib
import html
import json
import os
import re
import sys

from search_topics import TOPICS

ROOT = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(ROOT, "docs")
OUT = os.path.join(DOCS, "site", "search")

BOOKS = [("genesis", "Genesis", 50), ("exodus", "Exodus", 40), ("leviticus", "Leviticus", 27), ("numbers", "Numbers", 36),
         ("deuteronomy", "Deuteronomy", 34), ("joshua", "Joshua", 24), ("judges", "Judges", 21), ("ruth", "Ruth", 4),
         ("1samuel", "1 Samuel", 31), ("2samuel", "2 Samuel", 24), ("1kings", "1 Kings", 22), ("2kings", "2 Kings", 25),
         ("1chronicles", "1 Chronicles", 29), ("2chronicles", "2 Chronicles", 36), ("ezra", "Ezra", 10),
         ("nehemiah", "Nehemiah", 13), ("esther", "Esther", 10), ("job", "Job", 42), ("psalms", "Psalms", 150),
         ("proverbs", "Proverbs", 31), ("ecclesiastes", "Ecclesiastes", 12), ("songofsolomon", "Song of Solomon", 8),
         ("isaiah", "Isaiah", 66), ("jeremiah", "Jeremiah", 52), ("lamentations", "Lamentations", 5),
         ("ezekiel", "Ezekiel", 48), ("daniel", "Daniel", 12), ("hosea", "Hosea", 14), ("joel", "Joel", 3),
         ("amos", "Amos", 9), ("obadiah", "Obadiah", 1), ("jonah", "Jonah", 4), ("micah", "Micah", 7),
         ("nahum", "Nahum", 3), ("habakkuk", "Habakkuk", 3), ("zephaniah", "Zephaniah", 3), ("haggai", "Haggai", 2),
         ("zechariah", "Zechariah", 14), ("malachi", "Malachi", 4), ("matthew", "Matthew", 28), ("mark", "Mark", 16),
         ("luke", "Luke", 24), ("john", "John", 21), ("acts", "Acts", 28), ("romans", "Romans", 16),
         ("1corinthians", "1 Corinthians", 16), ("2corinthians", "2 Corinthians", 13), ("galatians", "Galatians", 6),
         ("ephesians", "Ephesians", 6), ("philippians", "Philippians", 4), ("colossians", "Colossians", 4),
         ("1thessalonians", "1 Thessalonians", 5), ("2thessalonians", "2 Thessalonians", 3),
         ("1timothy", "1 Timothy", 6), ("2timothy", "2 Timothy", 4), ("titus", "Titus", 3), ("philemon", "Philemon", 1),
         ("hebrews", "Hebrews", 13), ("james", "James", 5), ("1peter", "1 Peter", 5), ("2peter", "2 Peter", 3),
         ("1john", "1 John", 5), ("2john", "2 John", 1), ("3john", "3 John", 1), ("jude", "Jude", 1),
         ("revelation", "Revelation", 22)]
NAME_TO_SLUG = {name.lower(): slug for slug, name, _ in BOOKS}
NAME_TO_SLUG["psalm"] = "psalms"

# Pages that are tools or legal text rather than study content.
SKIP_PAGES = {"index.html", "search.html", "contact.html", "privacy.html", "offline.html", "404.html",
              "notes.html", "friends.html", "plans.html", "memory.html", "devotional.html", "about.html"}

TAG = re.compile(r"<[^>]+>")
WS = re.compile(r"\s+")


def text_of(fragment):
    fragment = re.sub(r"<(script|style)\b.*?</\1>", " ", fragment, flags=re.S | re.I)
    return WS.sub(" ", html.unescape(TAG.sub(" ", fragment))).strip()


def clip(s, n):
    if len(s) <= n:
        return s
    cut = s[:n].rsplit(" ", 1)[0]
    return cut.rstrip(",;:") + "…"


def read(name):
    with open(os.path.join(DOCS, name), encoding="utf-8") as f:
        return f.read()


def pane(page, tab):
    """Inner HTML of a chapter page's study tab, or ''."""
    m = re.search(r'<div class="tab-content[^"]*" id="tab-%s">' % tab, page)
    if not m:
        return ""
    i, depth = m.end(), 1
    for t in re.finditer(r"<(/?)div\b", page[i:]):
        depth += -1 if t.group(1) else 1
        if depth == 0:
            return page[i:i + t.start()]
    return ""


# ---------------------------------------------------------------- Bible text

def bsb_verses(page):
    m = re.search(r'<div class="translation-block" data-translation="BSB">(.*?)</div>', page, re.S)
    if not m:
        return None
    out = {}
    for n, body in re.findall(r'<p class="verse"><span class="verse-num">(\d+)</span>(.*?)</p>', m.group(1), re.S):
        out[int(n)] = text_of(body)
    return [out.get(i, "") for i in range(1, max(out) + 1)] if out else None


def build_bible(problems):
    books = []
    verses = {}
    for slug, name, chapters in BOOKS:
        chs = []
        for c in range(1, chapters + 1):
            fn = f"{slug}{c}.html"
            v = bsb_verses(read(fn)) if os.path.exists(os.path.join(DOCS, fn)) else None
            if not v:
                problems.append(f"no BSB text on {fn}")
                v = []
            chs.append(v)
            verses[(slug, c)] = len(v)
        books.append(chs)
    return {"t": "BSB", "b": [n for _, n, _ in BOOKS], "s": [s for s, _, _ in BOOKS], "v": books}, verses


# ---------------------------------------------------------------- Stories & Topics

REF = re.compile(r"^(.+?)\s+(\d+)(?::(\d+))?(?:-(\d+)(?::(\d+))?)?$")


def resolve(ref, verses):
    m = REF.match(ref.strip())
    if not m:
        return None, f"cannot read reference '{ref}'"
    slug = NAME_TO_SLUG.get(m.group(1).lower())
    if not slug:
        return None, f"unknown book in '{ref}'"
    ch, v = int(m.group(2)), m.group(3)
    n = verses.get((slug, ch))
    if not n:
        return None, f"no chapter page for '{ref}'"
    if v and int(v) > n:
        return None, f"'{ref}' starts past the end of the chapter ({n} verses)"
    return {"r": ref.strip(), "u": f"{slug}{ch}.html" + (f"#v{v}" if v and int(v) > 1 else "")}, None


def study_ok(link):
    page, _, frag = link.partition("#")
    path = os.path.join(DOCS, page)
    if not os.path.exists(path):
        return False
    return not frag or f'id="{frag}"' in read(page)


def build_topics(verses, problems):
    out = []
    seen = set()
    for line in TOPICS.strip().splitlines():
        if not line.strip():
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) != 5:
            problems.append(f"topic line needs 5 fields: {line}")
            continue
        kind, name, aliases, refs, study = parts
        if name.lower() in seen:
            problems.append(f"duplicate topic '{name}'")
        seen.add(name.lower())
        rs = []
        for r in refs.split(";"):
            got, err = resolve(r, verses)
            if err:
                problems.append(f"{name}: {err}")
            else:
                rs.append(got)
        if study and not study_ok(study):
            problems.append(f"{name}: study link '{study}' does not resolve")
        e = {"k": kind, "n": name, "r": rs}
        a = [x.strip() for x in aliases.split(",") if x.strip()]
        if a:
            e["a"] = a
        if study:
            e["s"] = study
        out.append(e)
    return out


# ---------------------------------------------------------------- Studies

SECTION = re.compile(r'<div class="section-block"(?: id="([^"]+)")?[^>]*>')


def sections(page):
    """(id, h2, inner html) for each top-level section block."""
    for m in SECTION.finditer(page):
        i, depth = m.end(), 1
        for t in re.finditer(r"<(/?)div\b", page[i:]):
            depth += -1 if t.group(1) else 1
            if depth == 0:
                yield m.group(1), page[i:i + t.start()]
                break


def strip_media(fragment):
    # Video captions and article lists are other people's titles, not this
    # page's teaching; they would make every page match "video".
    fragment = re.sub(r'<div class="(?:video-grid|yt-facade)[^"]*".*?</div>\s*</div>', " ", fragment, flags=re.S)
    fragment = re.sub(r"<!-- articles -->.*?<!-- /articles -->", " ", fragment, flags=re.S)
    return fragment


def title_of(page):
    m = re.search(r"<h1[^>]*>(.*?)</h1>", page, re.S) or re.search(r"<title>(.*?)</title>", page, re.S)
    return text_of(m.group(1)).split(" — ")[0] if m else ""


def kind_of(name, page):
    if 'class="topic-hero' not in page and 'section-block' not in page:
        return None
    life = {"addiction", "anger", "anxiety-and-fear", "depression-and-hopelessness", "doubt-and-unbelief",
            "greed-and-materialism", "grief-and-loss", "identity-and-self-worth", "loneliness",
            "lust-and-sexual-sin", "pride", "suffering", "temptation", "unforgiveness-and-bitterness", "life-studies"}
    return "Life study" if name[:-5] in life else "Topical study"


def build_studies(problems):
    out = []
    for name in sorted(os.listdir(DOCS)):
        if not name.endswith(".html") or name in SKIP_PAGES or re.match(r"^\d?[a-z]+\d+\.html$", name):
            continue
        page = read(name)
        kind = kind_of(name, page)
        if not kind:
            continue
        ptitle = title_of(page)
        md = re.search(r'<meta name="description" content="([^"]*)"', page)
        out.append({"k": kind, "t": ptitle, "u": name, "x": clip(html.unescape(md.group(1)) if md else "", 300)})
        for sid, inner in sections(page):
            h = re.search(r"<h2[^>]*>(.*?)</h2>", inner, re.S)
            if not h:
                continue
            h2 = text_of(h.group(1))
            if h2.lower() in {"videos", "video resources", "articles"}:
                continue
            body = text_of(strip_media(inner[h.end():]))
            heads = [text_of(x) for x in re.findall(r"<h3[^>]*>(.*?)</h3>", inner, re.S)]
            heads = [x for x in heads if x.lower() not in {"videos", "key verses", "articles"}]
            e = {"k": kind, "t": h2, "p": ptitle, "u": name + (f"#{sid}" if sid else ""), "x": clip(body, 900)}
            if heads:
                e["h"] = heads
            out.append(e)
    return out


def build_chapters(problems):
    out = []
    for slug, name, chapters in BOOKS:
        for c in range(1, chapters + 1):
            fn = f"{slug}{c}.html"
            page = read(fn)
            summ = text_of(re.sub(r"<h3>.*?</h3>", " ", pane(page, "summary"), flags=re.S))
            heads, themes = [], ""
            for label, body in re.findall(r'<span class="auth-label">(.*?)</span>(.*?)</div>', pane(page, "authorship"), re.S):
                label = text_of(label).rstrip(":")
                if label.lower() == "key themes":
                    themes = text_of(body)
                elif re.search(r"\(vv?\.?\s*\d", label):
                    heads.append(label)
            dd = pane(page, "deepdive")
            dd_heads = [text_of(x) for x in re.findall(r"<h4[^>]*>(.*?)</h4>", dd, re.S)]
            e = {"k": "Chapter", "t": f"{name} {c}", "u": fn, "x": clip(summ, 900)}
            if heads:
                e["h"] = heads
            if themes:
                e["m"] = clip(themes, 300)
            if dd_heads and "Coming soon" not in dd[:600]:
                e["d"] = dd_heads
            out.append(e)
    return out


def build_devotionals(problems):
    data = json.loads(read("devotionals.json"))
    out = []
    for i, d in enumerate(data):
        out.append({"k": "Devotional", "t": d.get("verse", ""), "u": f"devotional.html?d={i}",
                    "x": clip(" ".join(filter(None, [d.get("reflection"), d.get("application")])), 500)})
    return out


# ---------------------------------------------------------------- main

def dump(obj):
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))


def main():
    check = "--check" in sys.argv
    problems = []
    bible, verses = build_bible(problems)
    topics = build_topics(verses, problems)
    site = build_studies(problems) + build_chapters(problems) + build_devotionals(problems)
    files = {"topics.json": dump(topics), "site.json": dump(site), "bible.json": dump(bible)}
    for p in problems:
        print("PROBLEM:", p)
    if problems:
        print(f"{len(problems)} problem(s); nothing written.")
        sys.exit(1)
    changed = 0
    os.makedirs(OUT, exist_ok=True)
    for fn, body in files.items():
        path = os.path.join(OUT, fn)
        old = open(path, encoding="utf-8").read() if os.path.exists(path) else None
        if old != body:
            changed += 1
            if not check:
                open(path, "w", encoding="utf-8").write(body)
        print(f"{fn}: {len(body.encode()) // 1024} KB")
    # search.js asks for ?v=<hash> (stamped into search.html) so a rebuild is fetched fresh.
    stamp = hashlib.sha256("".join(files.values()).encode()).hexdigest()[:8]
    spath = os.path.join(DOCS, "search.html")
    shtml = read("search.html")
    new = re.sub(r'(id="bs-search-app" data-v=")[^"]*"', r'\g<1>' + stamp + '"', shtml)
    if new != shtml:
        changed += 1
        if not check:
            open(spath, "w", encoding="utf-8").write(new)
    kinds = {}
    for t in topics:
        kinds[t["k"]] = kinds.get(t["k"], 0) + 1
    print(f"topics {len(topics)} ({', '.join(f'{v} {k.lower()}' for k, v in kinds.items())}), "
          f"site entries {len(site)}, verses {sum(len(c) for b in bible['v'] for c in b)}; "
          f"{'would change' if check else 'changed'} {changed}, data v={stamp}")


if __name__ == "__main__":
    main()
