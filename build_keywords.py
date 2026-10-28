#!/usr/bin/env python3
"""Build docs/bible/ORIG/keys/<book>.json: the Key words strip shown above the
Scripture on every chapter page (docs/site/original.js).

Reads the data build_original.py wrote (docs/bible/ORIG/) and the hand-picked
word list in keywords_data.py. Run build_original.py first.

How a chapter's words are chosen (at most MAX per chapter):
  1. Words from keywords_data.py that occur in the chapter, scored by how often
     they occur there against how many chapters of that Testament use them
     (so a word that runs through a chapter, or rarely appears at all, ranks
     higher than one found everywhere). A word pinned to a chapter is always shown.
  2. If the chapter still has room, one New Testament word that is used only
     in that verse in the whole New Testament.

Output: {"<chapter>": [[strong, lemma, translit, gloss, verse, note], ...]}
  strong is the exact tag in the text, so the lexicon and word list load directly.

    python3 build_keywords.py --check   # report only
    python3 build_keywords.py           # write
"""
import glob
import json
import math
import os
import re
import sys
from collections import defaultdict

import keywords_data

ROOT = os.path.dirname(os.path.abspath(__file__))
ORIG = os.path.join(ROOT, "docs", "bible", "ORIG")
OUT = os.path.join(ORIG, "keys")
MAX = 5
MIN_SCORE = 2.2          # below this a hand-picked word is too common in the chapter's Testament to be worth a chip
RARE_NOTE = "Used only here in the whole New Testament."

SLUGS = ["genesis", "exodus", "leviticus", "numbers", "deuteronomy", "joshua", "judges", "ruth", "1samuel", "2samuel",
         "1kings", "2kings", "1chronicles", "2chronicles", "ezra", "nehemiah", "esther", "job", "psalms", "proverbs",
         "ecclesiastes", "songofsolomon", "isaiah", "jeremiah", "lamentations", "ezekiel", "daniel", "hosea", "joel",
         "amos", "obadiah", "jonah", "micah", "nahum", "habakkuk", "zephaniah", "haggai", "zechariah", "malachi",
         "matthew", "mark", "luke", "john", "acts", "romans", "1corinthians", "2corinthians", "galatians", "ephesians",
         "philippians", "colossians", "1thessalonians", "2thessalonians", "1timothy", "2timothy", "titus", "philemon",
         "hebrews", "james", "1peter", "2peter", "1john", "2john", "3john", "jude", "revelation"]


def base(s):
    return re.sub(r"[A-Za-z]$", "", s)


def root_of(w, greek):
    if greek:
        return w[3]
    m = re.search(r"\{([HA]?\d+[A-Za-z]?)\}", w[3])
    return m.group(1).replace("A", "H", 1) if m and m.group(1).startswith("A") else (m.group(1) if m else None)


def greek_translit(lemma, tr):
    # The lexicon writes a rough breathing after the first vowel ("ohutō", "ahima"); put the h in front.
    m = re.match(r"^([aeiouēō]{1,2})h(.*)$", tr)
    return "h" + m.group(1) + m.group(2) if m else tr


def main():
    check = "--check" in sys.argv
    lex = {}
    for f in glob.glob(os.path.join(ORIG, "lex", "*.json")):
        lex.update(json.load(open(f, encoding="utf-8")))
    occ = {}
    for f in glob.glob(os.path.join(ORIG, "occ", "*.json")):
        occ.update(json.load(open(f, encoding="utf-8")))

    # chapter -> list of (verse, root)
    chapters = {}
    for slug_i, slug in enumerate(SLUGS):
        for path in glob.glob(os.path.join(ORIG, slug + "[0-9]*.json")):
            page = os.path.basename(path)[:-5]
            if not re.fullmatch(re.escape(slug) + r"\d+", page):
                continue
            d = json.load(open(path, encoding="utf-8"))
            greek = d["l"] == "grc"
            rows = []
            for v, words in d["v"]:
                for w in words:
                    r = root_of(w, greek)
                    if r:
                        rows.append((v, r))
            for w in d.get("t", []):
                r = root_of(w, greek)
                if r:
                    rows.append((1, r))
            chapters[page] = (slug_i, int(page[len(slug):]), greek, rows)

    entries = []
    for testament, lst in (("he", keywords_data.HEBREW), ("grc", keywords_data.GREEK)):
        for i, (strong, gloss, note, pins) in enumerate(lst):
            entries.append({"strong": strong, "gloss": gloss, "note": note, "pins": set(pins),
                            "greek": testament == "grc", "prio": 1.25 - 0.5 * i / max(1, len(lst) - 1)})
    problems = []
    for e in entries:
        tags = e["strong"].split("|")
        e["match"] = (lambda s, tags=tags: any(s == t if re.search(r"[A-Za-z]$", t) else base(s) == t for t in tags))
        if not any(e["match"](k) for k in lex):
            problems.append(f"{e['strong']}: not in the lexicon")

    # document frequency per entry
    n_ch = {False: 0, True: 0}
    df = defaultdict(int)
    hits = defaultdict(dict)      # page -> {entry index: [verses, roots]}
    for page, (_, _, greek, rows) in chapters.items():
        n_ch[greek] += 1
        for idx, e in enumerate(entries):
            if e["greek"] != greek:
                continue
            found = [(v, r) for v, r in rows if e["match"](r)]
            if found:
                df[idx] += 1
                hits[page][idx] = found

    for idx, e in enumerate(entries):
        for p in e["pins"]:
            if p not in hits or idx not in hits[p]:
                problems.append(f"{e['strong']} is pinned to {p} but does not occur there")

    # New Testament words found in a single verse
    nt_rare = {}
    for s, ids in occ.items():
        if s.startswith("G") and len(ids) == 1 and s in lex:
            l = lex[s]
            if l[2].startswith("N:") or "-P" in l[2] or "-L" in l[2] or l[0][:1].isupper():
                continue                              # names of people and places
            if not re.match(r"^G:(N|V|A)", l[2]):
                continue
            nt_rare[s] = ids[0]

    out = defaultdict(dict)
    sizes = defaultdict(int)
    for page, (slug_i, ch, greek, rows) in sorted(chapters.items()):
        scored = []
        for idx, found in hits.get(page, {}).items():
            e = entries[idx]
            tf = len(found)
            score = (1 + math.log(tf)) * math.log(n_ch[greek] / df[idx]) * e["prio"]
            if page in e["pins"]:
                score += 100
            if score >= MIN_SCORE:
                scored.append((score, idx, found))
        scored.sort(key=lambda x: (-x[0], x[1]))
        chosen = []
        for score, idx, found in scored[:MAX]:
            e = entries[idx]
            v, r = min(found)
            l = lex.get(r) or next((lex[k] for k in lex if e["match"](k)), None)
            tr = greek_translit(l[0], l[1]) if greek else l[1]
            chosen.append([r, l[0], tr, e["gloss"], v, e["note"]])
        if greek and len(chosen) < MAX:
            rare = [(vid % 1000, s) for s, vid in nt_rare.items()
                    if vid // 1000000 == slug_i + 1 and (vid // 1000) % 1000 == ch]
            if rare:
                v, s = sorted(rare)[0]
                l = lex[s]
                gloss = re.sub(r"^.*?:\s*", "", l[3]) if ":" in l[3] else l[3]
                chosen.append([s, l[0], greek_translit(l[0], l[1]), gloss, v, RARE_NOTE])
        chosen.sort(key=lambda c: c[4])
        sizes[len(chosen)] += 1
        if chosen:
            out[SLUGS[slug_i]][str(ch)] = chosen

    print(f"chapters {len(chapters)}; words per chapter: " + ", ".join(f"{k}: {sizes[k]}" for k in sorted(sizes)))
    print(f"hand-picked words {len(entries)}, single-verse New Testament words available {len(nt_rare)}")
    for p in problems:
        print("  problem: " + p)
    for page in ("genesis1", "exodus34", "psalms23", "isaiah53", "john3", "romans8", "philippians2", "1chronicles3"):
        slug = re.match(r"^(\d?[a-z]+)", page).group(1)
        ch = page[len(slug):]
        print(f"  {page}: " + "; ".join(f"{c[1]} {c[3]} v{c[4]}" for c in out.get(slug, {}).get(ch, [])))
    if check:
        sys.exit(1 if problems else 0)
    os.makedirs(OUT, exist_ok=True)
    for f in glob.glob(os.path.join(OUT, "*.json")):
        os.remove(f)
    for slug, d in out.items():
        with open(os.path.join(OUT, slug + ".json"), "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, separators=(",", ":"))
    print(f"wrote {len(out)} books to {OUT}")


if __name__ == "__main__":
    main()
