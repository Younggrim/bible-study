#!/usr/bin/env python3
"""
Repairs markdown-style asterisk emphasis that was written into two authorship
panes during the General Epistles batch.

Asterisks are not markup in HTML, so these rendered as visible characters:
"*charaktēr*" rather than italics. No chapter page uses <em> anywhere, and the
569 already-folded panes cite terms with curly quotes instead, so the fix matches
that convention rather than introducing a new tag.

Refuses to write on div imbalance.

Usage:
    python3 fix_literal_asterisks.py [--check]
"""
import os
import re
import sys

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")

FIXES = {
    "hebrews1": [("*charakt\u0113r*", "\u201ccharakt\u0113r\u201d")],
    "1john1":   [("*Koin\u014dnia*", "\u201cKoin\u014dnia\u201d"),
                 ("*just*",          "\u201cjust\u201d")],
}


def main():
    check = "--check" in sys.argv
    problems = []
    total = 0

    for page, pairs in sorted(FIXES.items()):
        path = os.path.join(DOCS, f"{page}.html")
        html = open(path, encoding="utf-8").read()
        new = html
        for old, repl in pairs:
            n = new.count(old)
            if n != 1:
                problems.append(f"{page}: expected 1 of {old!r}, found {n}")
                continue
            new = new.replace(old, repl)
            total += 1

        if new == html:
            continue
        o, c = len(re.findall(r"<div\b", new)), len(re.findall(r"</div>", new))
        if o != c:
            problems.append(f"{page}: div imbalance {o} vs {c}")
            continue
        if not check:
            open(path, "w", encoding="utf-8").write(new)

    print(f"{'would repair' if check else 'repaired'} {total} asterisk tokens")
    for p in problems:
        print(f"    {p}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
