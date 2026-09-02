#!/usr/bin/env python3
"""
Rejoins hyphenated words that were split by a stray space inside the Authorship &
Background pane.

These are line-wrap artifacts, not choices: 'post- exilic', 'Kiriath- jearim',
'Beth- shan', 'Merodach- baladan', 'self- righteousness', 'seven- day'. Every one
of them is a single compound word or a single place name that acquired a space
after its hyphen.

The one construction that must not be joined is the suspended hyphen, as in
'pre- and post-exilic', where the space is correct. The script refuses to run if
it finds a candidate whose second word is 'and', 'or' or 'to', so a suspended
hyphen introduced later cannot be silently destroyed.

Every replacement is printed, because the safety of this pass rests on the list
being readable rather than on the pattern being clever.

Usage:
    python3 normalize_hyphen_breaks.py [--check]
"""
import os
import re
import sys

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")
PANE = re.compile(r'(id="tab-authorship">)(.*?)(?=<div class="tab-content")', re.S)
BREAK = re.compile(r"\b([A-Za-z]{2,})- ([a-z]{2,})\b")
SUSPENDED = {"and", "or", "to", "nor", "but"}


def main():
    check = "--check" in sys.argv
    planned, found, refuse = {}, [], []
    for name in sorted(os.listdir(DOCS)):
        if not name.endswith(".html"):
            continue
        path = os.path.join(DOCS, name)
        html = open(path, encoding="utf-8").read()
        pane = PANE.search(html)
        if not pane:
            continue
        old = pane.group(2)
        hits = BREAK.findall(old)
        if not hits:
            continue
        for first, second in hits:
            if second in SUSPENDED:
                refuse.append(f"{name[:-5]}: suspended hyphen {first}- {second}")
            else:
                found.append(f"{name[:-5]}: {first}- {second}  ->  {first}-{second}")
        new = BREAK.sub(lambda m: f"{m.group(1)}-{m.group(2)}", old)
        full = html[:pane.start(2)] + new + html[pane.end(2):]
        o, c = len(re.findall(r"<div\b", full)), len(re.findall(r"</div>", full))
        if o != c:
            refuse.append(f"{name[:-5]}: div imbalance {o} vs {c}")
            continue
        planned[path] = full
    for f in found:
        print(f"    {f}")
    if refuse:
        print(f"refusing to write, {len(refuse)} problem(s)")
        for r in refuse:
            print(f"    {r}")
        return 1
    if not check:
        for path, full in planned.items():
            open(path, "w", encoding="utf-8").write(full)
    print(f"{'would rejoin' if check else 'rejoined'} {len(found)} words "
          f"across {len(planned)} pages")
    return 0


if __name__ == "__main__":
    sys.exit(main())
