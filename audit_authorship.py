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

Labels are also checked for two faults that verse coverage cannot see, because a
page can cover every verse and still carry a broken heading:

  Sentence fragments. Prose cut at a colon and promoted into a label, as in
  'The chapter divides into two movements:' or "2chronicles29"'s "The chapter's
  theological climax is verse 36:". These read as headings and are not.
  Labels cut inside a verse reference, as in ezekiel29's 'The first oracle (29:',
  where the colon that was split on belonged to chapter and verse.

Quoted material is removed before the fragment test, so a genuine topical heading
that contains a quotation is not mistaken for prose. matthew5's 'The Six Antitheses
("You have heard... but I say")' is a heading, and the verb inside its quotation
must not condemn it.

CLEAN means every verse in the chapter is covered by exactly one section, no range
runs past the end of the chapter, and no label carries emphatic capitals, a
sentence fragment, or a truncated verse reference.

Usage:
    python3 audit_authorship.py              summary and per-book table
    python3 audit_authorship.py <book>       per-chapter detail for one book
    python3 audit_authorship.py --defects    every non-clean page with its reason
    python3 audit_authorship.py --labels     every fragment or truncated label
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
ITEM_PAIR = re.compile(
    r'<div class="auth-item"><span class="auth-label">(.*?)</span>\s*(.*?)</div>', re.S)
TAIL = re.compile(r'\(vv?\.([\d]+[a-z]?(?:[-,:\s]+[\d]+[a-z]?)*)\)\s*:\s*$')
PART = re.compile(r'(\d+)([ab]?)(?:\s*-\s*(\d+)([ab]?))?')
CAPS = re.compile(r"\b[A-Z]{2,}\b")
CAPS_OK = {"LORD", "GOD", "YHWH", "OT", "NT", "BC", "AD", "KJV", "ESV", "ASV",
           "AM", "II", "BRANCH", "HOLINESS", "PE", "AYIN", "MENE", "TEKEL",
           "UPHARSIN"}

# Fields that belong to the book or the chapter as a whole rather than to a span of
# verses. These are expected to carry no range and are exempt from the label checks.
BOOK_FIELDS = {
    "Author:", "Historical Context:", "Classification:", "Key Themes:", "Purpose:",
    "Date Written:", "Audience:", "Recipient:", "Theme:", "Prologue:", "Notable:",
    "Speakers:", "Date:", "Subscription:", "The Issue:",
}
# A finite verb in a label means a sentence was cut at a colon rather than a heading
# being written. Participles and gerunds are deliberately absent, since headings use
# them freely: 'Sowing the Wind', 'The Filthy Garments Removed'.
# Matching is deliberately case-sensitive on lowercase forms. Headings here are
# title-cased, so a noun that doubles as a verb ('The Share of the Levites', 'The
# Form of Godliness') cannot trip the check, while a verb inside a sentence can.
FINITE_VERB = re.compile(
    r"\b(is|are|was|were|has|have|had|divides|moves|reveals|represent|represents|"
    r"debate|debates|debated|respond|responds|contains|begins|ends|breaks|matters|"
    r"shows|makes|comes|form|forms|reads|opens|closes|follows|amounts|becomes|records|"
    r"tells|says|asks|answers|stands|sits|runs|leads|points|hangs|turns|gives|"
    r"takes|holds|carries|marks|pivots|requires|wonders|seems|appears|means|"
    r"unfolds|share|shares|operates|operate|describes|presents|offers|covers|traces|"
    r"focuses|concerns|consists|functions|serves|falls|splits|alternates|builds|"
    r"culminates|progresses|develops|expands|parallels|echoes|recalls|quotes|cites|"
    r"notes|adds|omits|lacks|raises|poses|demands|implies|suggests|indicates|"
    r"confirms|proves|explains|illustrates|demonstrates|emphasizes|stresses|"
    r"repeats|returns|shifts|narrows|widens|centers|centres|works)\b")
QUOTED = re.compile(r"\"[^\"]*\"|\u201c[^\u201d]*\u201d|\u2018[^\u2019]*\u2019")
TRUNC_REF = re.compile(r"\((?:\w+\s+)?\d+:\s*$")
# A label ending in a chapter number, as in 'Romans 3:', is only evidence of a cut
# reference if the body then opens with the verse number. Requiring both keeps
# ordinary numbered headings such as 'Feast 1:' out of it.
CHAPTER_TAIL = re.compile(r"\b[1-3]?\s*[A-Z][A-Za-z]+\s+\d+:\s*$")


def label_fault(label, body=None):
    """Return a reason string if a label is a cut sentence, else None.

    body is optional. It is only needed to recognise a label that was cut between
    a chapter number and its verse number.
    """
    if label in BOOK_FIELDS or TAIL.search(label):
        return None
    if label.startswith("Chapter ") or label.startswith("Purpose of"):
        return None
    if TRUNC_REF.search(label.rstrip(":") + ":"):
        return "cut inside a verse reference"
    if body is not None and CHAPTER_TAIL.search(label) and re.match(r"\s*\d", body):
        return "cut between chapter and verse"
    bare = QUOTED.sub(" ", label)
    if len(bare.split()) >= 4 and FINITE_VERB.search(bare):
        return "sentence fragment"
    return None


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
        pairs = [(H.unescape(a).strip(), H.unescape(re.sub(r"<.*?>", "", b)).strip())
                 for a, b in ITEM_PAIR.findall(pane.group(2))]
        faults = [(l, label_fault(l, b)) for l, b in pairs] if pairs else \
                 [(l, label_fault(l)) for l in labels]
        pages[name] = {
            "verses": total,
            "sections": len(sections),
            "missing": missing,
            "repeated": sorted({v for v, _ in repeated}),
            "beyond": over,
            "caps": sorted(stray),
            "labels": [(l, f) for l, f in faults if f],
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
    if d["labels"]:
        kinds = sorted({f for _, f in d["labels"]})
        bits.append(f"{len(d['labels'])} label(s) {' and '.join(kinds)}")
    return ", ".join(bits)


def main():
    pages = scan()
    clean = {n for n, d in pages.items()
             if d["sections"] and not (d["missing"] or d["repeated"] or d["beyond"]
                                      or d["caps"] or d["labels"])}
    arg = sys.argv[1] if len(sys.argv) > 1 else None

    if arg == "--labels":
        total = 0
        for n in sorted(pages, key=lambda x: (re.sub(r"\d+$", "", x),
                                              int(re.search(r"\d+$", x).group()))):
            for label, fault in pages[n]["labels"]:
                print(f"  {n:18s} {fault:28s} {label}")
                total += 1
        print(f"\n{total} broken label(s) on "
              f"{len([n for n in pages if pages[n]['labels']])} page(s)")
        return 0

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
