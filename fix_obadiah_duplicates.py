#!/usr/bin/env python3
"""
Repairs two artifacts the first fold batch left in obadiah1.

That script appended its own Classification and Key Themes without checking
whether the page already had them. Obadiah did, inside the merged Classification
field, so the page carried two of each once split_classification.py separated them.
It also dropped Obadiah's sublist while leaving the headless "Structure:" heading
that introduced it.

  Author:              kept
  Classification:      "Prophetic Oracle - Judgment on Edom"   kept, more specific
  Classification:      "Prophetic Oracle"                      removed
  Key Themes:          two variants                            merged into one
  Historical Context:  kept
  (headless)           "Structure:"                            removed, list is gone
  five sections        kept

Obadiah is the only page in either repo with a duplicated Classification or Key
Themes field, and the only one with an orphaned heading whose list is missing.
exodus20 and deuteronomy33 also have headless headings, but those legitimately
introduce the items below them, the ten commandments and the twelve tribes.

Usage:
    python3 fix_obadiah_duplicates.py [--check]
"""
import os
import re
import sys

PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    "docs", "obadiah1.html")

# The two Key Themes lists each carried something the other lacked: the first had
# Zion's deliverance and the kingdom, the second the terrain and the recompense.
MERGED_THEMES = (
    "Pride before a fall, betrayal of brotherhood, gloating over a brother&#x27;s "
    "ruin, the folly of trusting inaccessible terrain, measure-for-measure "
    "recompense, the day of the LORD reaching every nation, and the kingdom "
    "belonging to the LORD")

DROP_CLASSIFICATION = "Prophetic Oracle"          # keep the "- Judgment on Edom" one
KEEP_CLASSIFICATION = "Prophetic Oracle \u2014 Judgment on Edom"


def main():
    check = "--check" in sys.argv
    html = open(PATH, encoding="utf-8").read()
    pane = re.search(r'(id="tab-authorship">)(.*?)(?=<div class="tab-content")',
                     html, re.S)
    if not pane:
        sys.exit("no authorship pane")
    body = pane.group(2)

    items = re.findall(r'<div class="auth-item">.*?</div>', body, re.S)
    seen_cls = seen_themes = 0
    kept, notes = [], []

    for item in items:
        lab = re.search(r'class="auth-label">([^<]+)</span>', item)
        name = lab.group(1).strip() if lab else None
        text = re.sub(r"<[^>]+>", "", item).strip()

        if name is None and text == "Structure:":
            notes.append("removed orphaned 'Structure:' heading, its list is gone")
            continue

        if name == "Classification:":
            seen_cls += 1
            if DROP_CLASSIFICATION in item and KEEP_CLASSIFICATION not in item:
                notes.append(f"removed duplicate Classification {DROP_CLASSIFICATION!r}")
                continue

        if name == "Key Themes:":
            seen_themes += 1
            if seen_themes == 1:
                kept.append('<div class="auth-item">'
                            '<span class="auth-label">Key Themes:</span> '
                            f"{MERGED_THEMES}</div>")
                notes.append("merged the two Key Themes lists into one")
            else:
                notes.append("removed the second Key Themes")
            continue

        kept.append(item)

    problems = []
    if seen_cls != 2:
        problems.append(f"expected 2 Classification fields, found {seen_cls}")
    if seen_themes != 2:
        problems.append(f"expected 2 Key Themes fields, found {seen_themes}")

    labels = [re.search(r'class="auth-label">([^<]+)</span>', k) for k in kept]
    names = [m.group(1).strip() for m in labels if m]
    for want in ("Classification:", "Key Themes:"):
        if names.count(want) != 1:
            problems.append(f"{want} appears {names.count(want)} times after fix")

    new_body = ("\n                <h3>Authorship &amp; Background</h3>\n"
                + "".join(f"                {k}\n" for k in kept)
                + "            </div>\n\n            ")
    new = html[:pane.start(2)] + new_body + html[pane.end(2):]

    o, c = len(re.findall(r"<div\b", new)), len(re.findall(r"</div>", new))
    if o != c:
        problems.append(f"div imbalance {o} vs {c}")

    for n in notes:
        print(f"    note: {n}")
    if problems:
        print(f"refusing to write, {len(problems)} problem(s)")
        for p in problems:
            print(f"    {p}")
        return 1
    if not check:
        open(PATH, "w", encoding="utf-8").write(new)
    print(f"{'would fix' if check else 'fixed'} obadiah1, "
          f"{len(items)} items -> {len(kept)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
