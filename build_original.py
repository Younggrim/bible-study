#!/usr/bin/env python3
"""Build docs/bible/ORIG/: the Hebrew Old Testament and Greek New Testament,
word by word, for the original-languages panel and reading pane
(docs/site/original.js).

Sources (download, do not commit them):

    STEPBible-Data   https://github.com/STEPBible/STEPBible-Data         CC BY 4.0
        Translators Amalgamated OT+NT/TAHOT *.txt   Hebrew OT (Leningrad, following the Qere)
        Translators Amalgamated OT+NT/TAGNT *.txt   Greek NT (Nestle-Aland text)
        Lexicons/TBESH *.txt   Hebrew brief lexicon: headword, transliteration, gloss
        Lexicons/TBESG *.txt   Greek brief lexicon: Abbott-Smith definitions
    HebrewLexicon    https://github.com/openscriptures/HebrewLexicon     CC BY 4.0
        HebrewStrong.xml       Strong's Hebrew Dictionary, used for Hebrew definitions

The TBESH "Meaning" column is NOT used: it is the Abridged BDB from Online
Bible, which needs separate permission. Hebrew definitions come from Strong's
dictionary instead.

STEPBible asks that their data is reformatted for an application rather than
redistributed as is, so only these built files are committed. Changes made:
cantillation marks and meteg are removed from the Hebrew for readability
(vowel points are kept), and the Greek follows the Nestle-Aland text, falling
back to the KJV's Greek only for verses Nestle-Aland leaves out. This is noted
in the credit line on every page.

Output:
    docs/bible/ORIG/<page>.json   {"l": "he"|"grc", "v": [[verse, [word, ...]], ...],
                                   "t": [word, ...]   psalm title (shown with verse 1),
                                   "k": [verse, ...]  verses only in later manuscripts}
        Hebrew word: [text, translit, gloss, strongs, morph, lemma, punct, flag]
                     text, gloss, strongs and morph use "/" between prefix, root and
                     suffix; the root's Strong's number is in {braces}.
        Greek word:  [text, translit, gloss, strong, morph, lemma]
    docs/bible/ORIG/lex/<H|G><n>.json   lexicon entries for Strong's numbers n*100 .. n*100+99
    docs/bible/ORIG/occ/<H|G><n>.json   every verse each of those words appears in,
                                        as book*1000000 + chapter*1000 + verse (book 1 = Genesis)

    python3 build_original.py <STEPBible-Data dir> <HebrewLexicon dir> --check   # report only
    python3 build_original.py <STEPBible-Data dir> <HebrewLexicon dir>           # write

--check compares every chapter's verse numbers with the site's BSB text.
"""
import glob
import html
import json
import os
import re
import shutil
import sys
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.abspath(__file__))
DOCS = os.path.join(ROOT, "docs")
OUT = os.path.join(DOCS, "bible", "ORIG")

BOOKS = [("Gen", "genesis"), ("Exo", "exodus"), ("Lev", "leviticus"), ("Num", "numbers"), ("Deu", "deuteronomy"),
         ("Jos", "joshua"), ("Jdg", "judges"), ("Rut", "ruth"), ("1Sa", "1samuel"), ("2Sa", "2samuel"),
         ("1Ki", "1kings"), ("2Ki", "2kings"), ("1Ch", "1chronicles"), ("2Ch", "2chronicles"), ("Ezr", "ezra"),
         ("Neh", "nehemiah"), ("Est", "esther"), ("Job", "job"), ("Psa", "psalms"), ("Pro", "proverbs"),
         ("Ecc", "ecclesiastes"), ("Sng", "songofsolomon"), ("Isa", "isaiah"), ("Jer", "jeremiah"),
         ("Lam", "lamentations"), ("Ezk", "ezekiel"), ("Dan", "daniel"), ("Hos", "hosea"), ("Jol", "joel"),
         ("Amo", "amos"), ("Oba", "obadiah"), ("Jon", "jonah"), ("Mic", "micah"), ("Nam", "nahum"),
         ("Hab", "habakkuk"), ("Zep", "zephaniah"), ("Hag", "haggai"), ("Zec", "zechariah"), ("Mal", "malachi"),
         ("Mat", "matthew"), ("Mrk", "mark"), ("Luk", "luke"), ("Jhn", "john"), ("Act", "acts"), ("Rom", "romans"),
         ("1Co", "1corinthians"), ("2Co", "2corinthians"), ("Gal", "galatians"), ("Eph", "ephesians"),
         ("Php", "philippians"), ("Col", "colossians"), ("1Th", "1thessalonians"), ("2Th", "2thessalonians"),
         ("1Ti", "1timothy"), ("2Ti", "2timothy"), ("Tit", "titus"), ("Phm", "philemon"), ("Heb", "hebrews"),
         ("Jas", "james"), ("1Pe", "1peter"), ("2Pe", "2peter"), ("1Jn", "1john"), ("2Jn", "2john"),
         ("3Jn", "3john"), ("Jud", "jude"), ("Rev", "revelation")]
CODE = {c: (i + 1, s) for i, (c, s) in enumerate(BOOKS)}

# English (NRSV) reference first; the Hebrew, NA or KJV reference in brackets after it is ignored.
REF = re.compile(r"^(\w{3})\.(\d+)\.(\d+)((?:[\(\[\{][^)\]\}]*[\)\]\}])*)#(\d+)=([^\t]*)$")
# Three places where the site's English text (BSB) numbers the Greek the KJV way, not the NRSV way:
# 2 Cor 13:12-14, 3 John 14, and Rev 12:18, which the KJV and BSB print as the start of 13:1.
KJV_NUMBERING = {("2Co", 13), ("3Jn", 1), ("Rev", 12)}
ACCENTS = re.compile("[\u0591-\u05AF\u05BD]")          # cantillation and meteg; vowel points stay


def hebrew_words(step):
    """(slug, chapter) -> {verse: [word]}  plus psalm titles under verse 0."""
    out = {}
    for path in sorted(glob.glob(os.path.join(step, "Translators Amalgamated OT+NT", "TAHOT *.txt"))):
        for line in open(path, encoding="utf-8-sig"):
            f = line.rstrip("\n").split("\t")
            m = REF.match(f[0])
            if not m or len(f) < 12:
                continue
            book, ch, vs, kind = m.group(1), int(m.group(2)), int(m.group(3)), m.group(6)
            text = ACCENTS.sub("", f[1])
            word, _, punct = text.partition("\\")
            punct = "".join(c for c in punct if c in "׃־")          # sof pasuq and maqaf; paseq is left out
            strongs = re.sub(r"\\[^/]*", "", f[4]).replace("+", "")
            lemma = ""
            lm = re.search(r"\{H\d+[A-Za-z]?=([^=}]*)=", f[11])
            if lm:
                lemma = ACCENTS.sub("", lm.group(1))
            flag = kind[0] if kind[:1] in ("Q", "X", "R") else ""
            w = [word, f[2].replace("/", ""), f[3].strip(), strongs, f[5], lemma, punct, flag]
            while w and w[-1] == "":
                w.pop()
            out.setdefault((CODE[book][1], ch), {}).setdefault(vs, []).append(w)
    return out


def greek_words(step):
    """(slug, chapter) -> ({verse: [word]}, set of verses taken from the KJV's Greek)"""
    na, tr = {}, {}
    for path in sorted(glob.glob(os.path.join(step, "Translators Amalgamated OT+NT", "TAGNT *.txt"))):
        for line in open(path, encoding="utf-8-sig"):
            f = line.rstrip("\n").split("\t")
            m = REF.match(f[0])
            if not m or len(f) < 5:
                continue
            book, ch, vs, kind = m.group(1), int(m.group(2)), int(m.group(3)), m.group(6)
            kjv = re.search(r"\[(\d+)\.(\d+)\]", m.group(4))
            if kjv and (book, ch) in KJV_NUMBERING:
                ch, vs = int(kjv.group(1)), int(kjv.group(2))
            tm = re.match(r"^(.*?)\s*\(([^)]*)\)\s*$", f[1])
            text, translit = (tm.group(1), tm.group(2)) if tm else (f[1].strip(), "")
            text = re.sub(r"[¶¬\[\]]", "", text).strip()        # paragraph marks and editorial brackets
            strong, _, morph = f[3].partition("=")
            lemma = f[4].split("=")[0].split(",")[-1].strip()
            w = [text, translit, f[2].strip(), strong.strip(), morph.strip(), lemma]
            key = (CODE[book][1], ch)
            if kind[:1] in ("N", "n"):
                na.setdefault(key, {}).setdefault(vs, []).append(w)
            elif "K" in kind or "k" in kind:
                tr.setdefault(key, {}).setdefault(vs, []).append(w)
    out, fallback = {}, {}
    for key in set(na) | set(tr):
        verses = dict(na.get(key, {}))
        for vs, words in tr.get(key, {}).items():
            if vs not in verses:                       # a verse the older manuscripts leave out
                verses[vs] = words
                fallback.setdefault(key, set()).add(vs)
        out[key] = verses
    return out, fallback


def site_verses():
    """page -> set of verse numbers in the site's BSB text."""
    res = {}
    for path in glob.glob(os.path.join(DOCS, "*.html")):
        t = open(path, encoding="utf-8").read()
        m = re.search(r'data-translation="BSB">(.*?)</div>', t, re.S)
        if m:
            res[os.path.basename(path)[:-5]] = {int(n) for n in re.findall(r'<span class="verse-num">(\d+)', m.group(1))}
    return res


def root_strong(word, greek):
    if greek:
        return word[3]
    m = re.search(r"\{([HA]?\d+[A-Za-z]?)\}", word[3])
    return m.group(1) if m else None


def bucket(strong):
    m = re.match(r"^([HG])0*(\d+)", strong)
    return m.group(1) + str(int(m.group(2)) // 100) if m else None


# ---------- lexicons ----------

TAG = re.compile(r"<(/?)([a-zA-Z]+)((?:\s*=\s*|\s)[^>]*)?>")


def clean_html(s):
    """Escape everything except <b>, <i>, <br> and references, which become <a data-r="Book.C.V">."""
    out, pos, depth = [], 0, 0
    for m in TAG.finditer(s):
        out.append(html.escape(s[pos:m.start()], quote=False))
        pos = m.end()
        close, name = m.group(1), m.group(2).lower()
        if name in ("b", "i"):
            out.append(f"<{close}{name}>")
        elif name == "br":
            out.append("<br>")
        elif name == "ref":
            if close:
                depth -= 1
                if depth == 0:
                    out.append("</a>")
            else:
                depth += 1
                r = re.search(r"'([^']*)'", m.group(3) or "")
                if depth == 1:
                    out.append(f'<a data-r="{html.escape(r.group(1) if r else "")}">')
    out.append(html.escape(s[pos:], quote=False))
    text = "".join(out)
    text = re.sub(r"(<br>\s*){2,}", "<br>", text).strip()
    return re.sub(r"^(<br>\s*)+|(<br>\s*)+$", "", text)


def strong_dictionary(lexdir):
    """Hebrew Strong's number (H7225) -> definition HTML from Strong's Hebrew Dictionary."""
    ns = "{http://openscriptures.github.com/morphhb/namespace}"
    tree = ET.parse(os.path.join(lexdir, "HebrewStrong.xml"))
    res = {}

    def inner(e):
        if e is None:
            return ""
        parts = [html.escape(e.text or "", quote=False)]
        for c in e:
            tag = c.tag.replace(ns, "")
            body = inner(c)
            if tag == "def":
                parts.append(f"<b>{body}</b>")
            elif tag == "w" and c.get("src"):
                parts.append(f'<a data-s="{html.escape(c.get("src"))}">{body}</a>')
            else:
                parts.append(body)
            parts.append(html.escape(c.tail or "", quote=False))
        return "".join(parts)

    for e in tree.getroot().iter(ns + "entry"):
        sid = e.get("id")
        meaning, usage, source = inner(e.find(ns + "meaning")), inner(e.find(ns + "usage")), inner(e.find(ns + "source"))
        bits = [b.strip() for b in (meaning, source) if b and b.strip()]
        d = "; ".join(bits)
        if usage.strip():
            d += ("<br>" if d else "") + "<i>KJV:</i> " + usage.strip()
        res[sid] = re.sub(r"\s+", " ", d)
    return res


def lexicon(step, lexdir):
    """dStrong -> entry.  Hebrew: [lemma, translit, morph, gloss, strongs_def];  Greek: [lemma, translit, morph, gloss, def]"""
    res = {}
    strongs = strong_dictionary(lexdir)
    for path in glob.glob(os.path.join(step, "Lexicons", "TBESH *.txt")):
        for line in open(path, encoding="utf-8-sig"):
            f = line.rstrip("\n").split("\t")
            if len(f) < 7 or not re.match(r"^[HA]\d+", f[0]):
                continue
            d = f[1].split("=")[0].strip()
            if not re.match(r"^H\d+[A-Za-z]?$", d) or d in res:
                continue
            num = "H" + str(int(re.match(r"^H(\d+)", d).group(1)))
            res[d] = [ACCENTS.sub("", f[3]), f[4], f[5], f[6].strip(), strongs.get(num, "")]
    for path in glob.glob(os.path.join(step, "Lexicons", "TBESG *.txt")):
        for line in open(path, encoding="utf-8-sig"):
            f = line.rstrip("\n").split("\t")
            if len(f) < 8 or not re.match(r"^G\d+", f[0]):
                continue
            d = f[1].split("=")[0].strip()
            if not re.match(r"^G\d+[A-Za-z]?$", d) or d in res:
                continue
            res[d] = [f[3], f[4], f[5], f[6].strip(), clean_html(f[7].replace("__", ""))]
    return res


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    if len(args) != 2:
        sys.exit(__doc__)
    step, lexdir = args
    check = "--check" in sys.argv

    heb = hebrew_words(step)
    grk, fallback = greek_words(step)
    site = site_verses()
    print(f"Hebrew chapters {len(heb)}, Greek chapters {len(grk)}, site chapters {len(site)}")

    pages, problems, occ = {}, [], {}
    for idx, (code, slug) in enumerate(BOOKS):
        greek = idx >= 39
        src = grk if greek else heb
        for (s, ch), verses in src.items():
            if s != slug:
                continue
            page = f"{slug}{ch}"
            want = site.get(page)
            title = verses.pop(0, None)
            have = set(verses)
            if want is None:
                problems.append(f"{page}: no page on the site")
                continue
            if have != want:
                extra, missing = sorted(have - want), sorted(want - have)
                problems.append(f"{page}: " + (f"not on site {extra} " if extra else "") + (f"missing {missing}" if missing else ""))
            data = {"l": "grc" if greek else "he", "v": [[v, verses[v]] for v in sorted(verses)]}
            if title:
                data["t"] = title
            if greek and fallback.get((slug, ch)):
                data["k"] = sorted(fallback[(slug, ch)])
            pages[page] = data
            book_n = idx + 1
            for v, words in list(verses.items()) + ([(1, title)] if title else []):
                for w in words:
                    r = root_strong(w, greek)
                    if not r:
                        continue
                    if r.startswith("A"):
                        r = "H" + r[1:]
                    lst = occ.setdefault(r, [])
                    vid = book_n * 1000000 + ch * 1000 + v
                    if not lst or lst[-1] != vid:
                        lst.append(vid)
    missing_pages = sorted(set(site) - set(pages))
    for p in missing_pages:
        problems.append(f"{p}: no {'Greek' if p else ''} data")
    print(f"chapters built {len(pages)}, words {sum(len(w) for d in pages.values() for _, w in d['v'])}, "
          f"lexical forms indexed {len(occ)}")
    print(f"verse numbering differences: {len(problems)}")
    for p in problems:
        print("  " + p)

    lex = lexicon(step, lexdir)
    # A few tags in the texts use a sub-meaning letter the lexicon does not list (H0430J);
    # give them the entry for the same Strong's number.
    by_num = {}
    for k in sorted(lex):
        by_num.setdefault(re.sub(r"[A-Za-z]$", "", k), k)
    unknown = []
    for s in sorted(occ):
        if s in lex:
            continue
        alt = by_num.get(re.sub(r"[A-Za-z]$", "", s))
        if alt:
            lex[s] = lex[alt]
        else:
            unknown.append(s)
    print(f"lexicon entries {len(lex)}, words with no lexicon entry {len(unknown)}: {unknown}")

    if check:
        return
    if os.path.isdir(OUT):
        shutil.rmtree(OUT)
    os.makedirs(os.path.join(OUT, "lex"))
    os.makedirs(os.path.join(OUT, "occ"))
    for page, data in pages.items():
        with open(os.path.join(OUT, page + ".json"), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, separators=(",", ":"))
    for name, table in (("lex", lex), ("occ", occ)):
        buckets = {}
        for k, v in table.items():
            b = bucket(k)
            if b:
                buckets.setdefault(b, {})[k] = v
        for b, d in buckets.items():
            with open(os.path.join(OUT, name, b + ".json"), "w", encoding="utf-8") as f:
                json.dump(d, f, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
    total = sum(os.path.getsize(os.path.join(dp, fn)) for dp, _, fns in os.walk(OUT) for fn in fns)
    print(f"wrote {OUT}: {total / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
