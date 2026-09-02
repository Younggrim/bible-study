#!/usr/bin/env python3
"""
Reports how far each Authorship & Background pane has been folded onto the standard
shape, and what is wrong with the ones that have not.

Why this exists. Progress was being tracked by asking whether a page had at least
one field label ending in a verse range. That test is too generous. A page carrying
an inherited topical note like 'The Leper (vv.1-4):' passes it while leaving thirty
verses undescribed, so 765 pages looked folded when only 527 actually were. This
script uses verse coverage instead, which is the thing that was actually wanted.

Half-verse ranges are read as halves. A page split at 'vv.5-7a' and 'vv.7b-9' is
covering verse 7 once, not twice, and an earlier version of this check reported
five folded pages as overlapping because it could not see the difference.

Verse totals come from each page's own scripture markup rather than from a table,
so the count cannot drift out of step with the text on the page.

CLEAN means every verse in the chapter is covered by exactly one section.

Usage:
    python3 audit_authorship.py              summary and per-book table
    python3 audit_authorship.py <book>       per-chapter detail for one book
    python3 audit_authorship.py --defects    every non-clean page with its reason
"""
import collections
import glob
import html as H
import os
import re
import sys

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")
PANE = re.compile(r'(id="tab-authorship">)(.*?)(?=<div class="tab-content")', re.S)
LABEL = re.compile(r'<span class="auth-label">(.*?)</span>', re.S)
TAIL = re.compile(r'\(vv?\.([\d]+[a-z]?(?:[-,:\s]+[\d]+[a-z]?)*)\)\s*:\s*$')
PART = re.compile(r'(\d+)([ab]?)(?:\s*-\s*(\d+)([ab]?))?')
CAPS = re.compile(r"\b[A-Z]{2,}\b")
CAPS_OK = {"LORD", "GOD", "YHWH", "OT", "NT", "BC", "AD", "KJV", "ESV", "ASV",
           "AM", "II", "BRANCH", "HOLINESS", "PE", "AYIN", "MENE", "TEKEL",
           "UPHARSIN"}


def halves(spec):
    """Expand a range spec into half-verse tokens, so 7a and 7b stay distinct."""
    out = set()
    for m in PART.finditer(spec):
        a, ah, z, zh = int(m.group(1)), m.group(2), m.group(3), m.group(4)
        z = int(z) if z else a
        zh = zh or ""
        if a == z:
            out |= {(a, ah)} if ah else {(a, "a"), (a, "b")}
            continue
        for v in range(a, z + 1):
            if v == a and ah:
                out.add((v, ah if ah == "b" else "a"))
                if ah == "a":
                    out.add((v, "b"))
            elif v == z and zh:
                out.add((v, zh))
                if zh == "b":
                    out.add((v, "a"))
            else:
                out |= {(v, "a"), (v, "b")}
    return out


def scan():
    pages = {}
    for path in sorted(glob.glob(os.path.join(DOCS, "*.html"))):
        name = os.path.basename(path)[:-5]
        html = open(path, encoding="utf-8").read()
        pane = PANE.search(html)
        if not pane:
            continue
        nums = {int(x) for x in re.findall(r'class="verse-num"[^>]*>(\d+)', html)}
        total = max(nums) if nums else 0
        labels = [H.unescape(x).strip() for x in LABEL.findall(pane.group(2))]
        sections = [(l, TAIL.search(l)) for l in labels]
        sections = [(l, m.group(1)) for l, m in sections if m]
        covered, repeated, over = set(), set(), []
        for label, spec in sections:
            got = halves(spec)
            repeated |= got & covered
            covered |= got
            top = max(v for v, _ in got) if got else 0
            if total and top > total:
                over.append(label)
        want = {(v, h) for v in range(1, total + 1) for h in ("a", "b")}
        missing = sorted({v for v, _ in (want - covered)})
        stray = set()
        for label, _ in sections:
            stray |= {w for w in CAPS.findall(label) if w not in CAPS_OK}
        pages[name] = {
            "verses": total,
            "sections": len(sections),
            "missing": missing,
            "repeated": sorted({v for v, _ in repeated}),
            "beyond": over,
            "caps": sorted(stray),
        }
    return pages


def reason(d):
    if not d["sections"]:
        return "no verse-range sections"
    bits = []
    if d["missing"]:
        bits.append(f"{len(d['missing'])} verse(s) uncovered")
    if d["repeated"]:
        bits.append(f"verses described twice {d['repeated']}")
    if d["beyond"]:
        bits.append(f"range past end of chapter {d['beyond']}")
    if d["caps"]:
        bits.append(f"capitals in label {d['caps']}")
    return ", ".join(bits)


def main():
    pages = scan()
    clean = {n for n, d in pages.items()
             if d["sections"] and not (d["missing"] or d["repeated"] or d["beyond"]
                                      or d["caps"])}
    arg = sys.argv[1] if len(sys.argv) > 1 else None

    if arg == "--defects":
        for n in sorted(pages, key=lambda x: (re.sub(r"\d+$", "", x),
                                              int(re.search(r"\d+$", x).group()))):
            if n not in clean:
                print(f"  {n:18s} {reason(pages[n])}")
        print(f"\n{len(pages) - len(clean)} page(s) not clean")
        return 0

    if arg:
        rows = [(n, pages[n]) for n in pages if re.sub(r"\d+$", "", n) == arg]
        if not rows:
            print(f"no book named {arg!r}")
            return 1
        for n, d in sorted(rows, key=lambda x: int(re.search(r"\d+$", x[0]).group())):
            mark = "clean" if n in clean else reason(d)
            print(f"  {n:18s} {d['verses']:3d}v {d['sections']:2d} sections   {mark}")
        return 0

    print(f"CLEAN      {len(clean):5d} of {len(pages)}")
    print(f"remaining  {len(pages) - len(clean):5d}")
    buckets = collections.Counter()
    for n, d in pages.items():
        if n in clean:
            continue
        if not d["sections"]:
            buckets["no verse-range sections at all"] += 1
        elif d["missing"] and len(d["missing"]) <= 3:
            buckets["1 to 3 verses uncovered"] += 1
        elif d["missing"] and len(d["missing"]) <= 10:
            buckets["4 to 10 verses uncovered"] += 1
        elif d["missing"]:
            buckets["more than 10 verses uncovered"] += 1
        else:
            buckets["overlap or label defect only"] += 1
    print()
    for k, v in buckets.most_common():
        print(f"   {k:34s} {v}")
    books = collections.defaultdict(lambda: [0, 0])
    for n in pages:
        books[re.sub(r"\d+$", "", n)][0 if n in clean else 1] += 1
    done = sorted(k for k, v in books.items() if not v[1])
    print(f"\ncomplete books ({len(done)}):")
    print("   " + ", ".join(done))
    print(f"\nincomplete books ({len(books) - len(done)}):")
    for k, v in sorted(books.items(), key=lambda x: (-x[1][1], x[0])):
        if v[1]:
            print(f"   {k:16s} clean={v[0]:3d} remaining={v[1]:3d}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
