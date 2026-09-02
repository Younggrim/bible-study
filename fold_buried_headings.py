#!/usr/bin/env python3
"""
Relabels six chapters whose verse-range sections were already written but whose
headings sat in the body text instead of the auth-label span.

    1samuel15  numbers23  exodus8  exodus9  exodus10  joshua12

These pages read correctly but were invisible to every progress query, because
those match on the label. The exposition already exists and is not rewritten
here; the heading is moved into the label and Classification and Key Themes are
added.

Shapes handled:

    labelled + buried, exodus and the first item of 1samuel15 and numbers23
        <span class="auth-label">Second Plague:</span> Frogs (vv.1-15): text...
      becomes
        <span class="auth-label">Second Plague: Frogs (vv.1-15):</span> text...

    headless + buried, the rest of 1samuel15 and joshua12
        <div class="auth-item">Samuel's Confrontation (vv.10-21): text...
      becomes
        <span class="auth-label">Samuel's Confrontation (vv.10-21):</span> text...

Verse coverage was checked against each chapter's verse count before this was
written. All six cover their chapter with no gaps, which is why they are treated
as complete. Twelve other pages carry a buried heading that is a single verse
note rather than a chapter outline -- daniel2, ezekiel39, habakkuk2, isaiah59,
john19, john21, lamentations2, luke1, mark14, matthew10, matthew7, proverbs21 --
and those belong in the bulk fold, not here.

joshua12 also carries a sublist. Every item has a verse range, so the guard in
fold_openers_batch5.py would treat it as a droppable outline, but it is a
regional breakdown of the 31-king list that the two sections do not duplicate.
Its substance and the trailing "Total:" field are merged into the prose of the
second section instead of being discarded. Verse ranges on a list do not by
themselves make it redundant.

Follows the format in WORKFLOW.md. Writes nothing if any page fails a check.

Usage:
    python3 fold_buried_headings.py [--check]
"""
import os
import re
import sys

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")

ITEM = ('                    <div class="auth-item">'
        '<span class="auth-label">{label}</span> {body}</div>')

VERSES = {"1samuel15": 35, "numbers23": 30, "exodus8": 32, "exodus9": 35,
          "exodus10": 29, "joshua12": 24}

# Labels that are page or book level and stay above the sections.
HEADER = {"Author:", "Historical Context:", "Title:", "Purpose:", "Theme:",
          "Recipient:", "Date Written:", "Audience:"}

BURIED = re.compile(r'^\s*([^<>]{3,120}?\(vv?\.\s*\d[^)]{0,20}\)\s*:)\s+')

META = {
"1samuel15": ("Historical Narrative",
  "A command given in full and obeyed in part, the bleating that gave it away, "
  "obedience weighed against sacrifice, a robe torn as a sign, and a confession "
  "more concerned with honour than with restoration"),
"numbers23": ("Narrative with Poetic Oracle",
  "A hired curse that keeps emerging as blessing, seven altars as an attempt to "
  "manage God, a word its speaker cannot reverse, a God unlike a man in changing "
  "His mind, and a change of vantage point that changes nothing"),
"exodus8": ("Historical Narrative \u2014 Plague Cycle",
  "Frogs, gnats and flies applied as successive pressure, magicians who imitate "
  "the first and cannot reproduce the second, a distinction drawn between Israel "
  "and Egypt, and a heart hardened again after each reprieve"),
"exodus9": ("Historical Narrative \u2014 Plague Cycle",
  "Livestock, boils and hail escalating from property to persons, Egypt&#x27;s own "
  "magicians struck, a warning issued before the hail so that some could shelter, "
  "and a confession withdrawn as soon as the rain stopped"),
"exodus10": ("Historical Narrative \u2014 Plague Cycle",
  "Locusts and darkness stripping what the hail had left, officials pleading with "
  "Pharaoh before Israel does, negotiation over who is permitted to go, and a "
  "darkness described as something that could be felt"),
"joshua12": ("Historical Narrative \u2014 Conquest Summary",
  "A ledger of victories rather than a narrative, two campaigns under two leaders, "
  "territory described by boundary and terrain, thirty-one kings counted one at a "
  "time, and a tally that closes the conquest account"),
}

# joshua12: the sublist and the trailing Total: field, folded into the prose of
# the second section rather than dropped.
JOSHUA_APPEND = (
    " The order of the list is roughly geographical, working outward from the "
    "first conquests: Jericho and Ai (v.9), then the southern coalition of "
    "chapter 10 at Jerusalem, Hebron, Jarmuth, Lachish and Eglon (vv.10-12), "
    "then further southern cities including Gezer, Debir, Hormah, Arad, Libnah, "
    "Adullam and Makkedah (vv.12-16), the central region around Bethel, Tappuah, "
    "Hepher, Aphek and Lasharon (vv.16-18), the northern coalition of chapter 11 "
    "at Madon, Hazor, Shimron-meron and Achshaph (vv.19-20), and additional "
    "northern and central conquests from Taanach and Megiddo through to Tirzah "
    "(vv.21-24). The chapter closes with the sum rather than a comment on it: "
    "&quot;all the kings thirty and one&quot; (v.24).")

RANGE = re.compile(r'\(vv?\.\s*(\d+)[a-z]?(?:\s*[-\u2013]\s*(\d+)[a-z]?)?')


def main():
    check = "--check" in sys.argv
    problems, notes, planned = [], [], {}

    for page in sorted(VERSES):
        path = os.path.join(DOCS, f"{page}.html")
        html = open(path, encoding="utf-8").read()
        pane = re.search(r'(id="tab-authorship">)(.*?)(?=<div class="tab-content")',
                         html, re.S)
        if not pane:
            problems.append(f"{page}: no authorship pane")
            continue
        body = pane.group(2)

        header, sections = [], []
        for it in re.finditer(r'<div class="auth-item">(.*?)</div>', body, re.S):
            inner = it.group(1)
            lab = re.match(r'<span class="auth-label">([^<]*)</span>\s*', inner)
            name = lab.group(1).strip() if lab else None
            rest = inner[lab.end():] if lab else inner
            b = BURIED.match(rest)
            if b:
                head = b.group(1).strip()
                if name and name not in HEADER:
                    head = f"{name} {head}"
                sections.append((head, rest[b.end():].strip()))
            elif name in HEADER:
                header.append(inner)
            elif name == "Total:" and page == "joshua12":
                notes.append(f"{page}: Total: merged into the second section")
            elif name is None and rest.rstrip().endswith(":"):
                notes.append(f"{page}: dropping sublist heading "
                             f"{re.sub(r'<[^>]+>', '', rest).strip()[:48]!r}")
            else:
                problems.append(f"{page}: unclassified item "
                                f"{re.sub(r'<[^>]+>', '', inner).strip()[:60]!r}")

        if not sections:
            problems.append(f"{page}: no buried headings found")
            continue

        if page == "joshua12":
            head, txt = sections[-1]
            sections[-1] = (head, txt.rstrip().rstrip(":") + "." + JOSHUA_APPEND)

        # Sections must still cover the chapter with no gaps.
        covered = set()
        for head, _ in sections:
            for m in RANGE.finditer(head):
                a = int(m.group(1))
                z = int(m.group(2) or m.group(1))
                if z > VERSES[page]:
                    problems.append(f"{page}: {head!r} exceeds {VERSES[page]} verses")
                covered |= set(range(a, z + 1))
        gaps = sorted(set(range(1, VERSES[page] + 1)) - covered)
        if gaps:
            problems.append(f"{page}: sections leave {len(gaps)} verse(s) uncovered")

        genre, themes = META[page]
        parts = ["\n                <h3>Authorship &amp; Background</h3>\n"]
        for item in header:
            parts.append(f'                <div class="auth-item">{item}</div>\n')
        parts.append(ITEM.format(label="Classification:", body=genre) + "\n")
        parts.append(ITEM.format(label="Key Themes:", body=themes) + "\n")
        for head, prose in sections:
            parts.append(ITEM.format(label=head, body=prose) + "\n")
        new_body = "".join(parts) + "            </div>\n\n            "

        new = html[:pane.start(2)] + new_body + html[pane.end(2):]
        o, c = len(re.findall(r"<div\b", new)), len(re.findall(r"</div>", new))
        if o != c:
            problems.append(f"{page}: div imbalance {o} vs {c}")
            continue
        if "auth-sublist" in new:
            problems.append(f"{page}: sublist survived into output")
            continue
        planned[path] = new
        notes.append(f"{page}: {len(header)} header field(s), "
                     f"{len(sections)} section(s) relabelled")

    for n in notes:
        print(f"    note: {n}")
    if problems:
        print(f"refusing to write, {len(problems)} problem(s)")
        for p in problems:
            print(f"    {p}")
        return 1
    if not check:
        for path, new in planned.items():
            open(path, "w", encoding="utf-8").write(new)
    print(f"{'would relabel' if check else 'relabelled'} {len(planned)} pages")
    return 0


if __name__ == "__main__":
    sys.exit(main())
