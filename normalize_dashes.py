#!/usr/bin/env python3
"""
Normalises punctuation inside the Authorship & Background pane so every page uses the
same conventions.

Three inconsistencies, all introduced by earlier passes, all against a settled
majority:

  ' -- '  ->  ' \u2014 '   359 occurrences on 113 pages. The rest of the corpus uses a
                      real em dash 8332 times across 1188 pages. A literal '--'
                      renders as two hyphens in the browser.

  digit\u2013digit ->  digit-digit  35 occurrences on 10 pages. Numeric ranges are
                      written with a hyphen 9432 times across 1184 pages.

  '27 BC \u2013 AD 14' -> '27 BC to AD 14'  the only cross-era range in the corpus. A
                      spaced dash between two era labels has no precedent here, and
                      the hyphen convention is for unspaced ranges, so the range is
                      spelled out instead.

Runs of two or more spaces inside a field body collapse to one. HTML collapses them
anyway, so this changes no rendering, it only stops the source from implying an
alignment that does not survive.

Only auth-item bodies are touched. Label text, list markup and the indentation
between items are left exactly as they are.

Usage:
    python3 normalize_dashes.py [--check]
"""
import os
import re
import sys

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")
PANE = re.compile(r'(id="tab-authorship">)(.*?)(?=<div class="tab-content")', re.S)
BODY = re.compile(r'(<div class="auth-item"><span class="auth-label">.*?</span> )(.*?)(</div>)', re.S)


def fix(body):
    body = body.replace(" -- ", " \u2014 ")
    body = body.replace("27 BC \u2013 AD 14", "27 BC to AD 14")
    body = re.sub(r"(?<=\d)\u2013(?=\d)", "-", body)
    body = re.sub(r"(?<=\S) {2,}(?=\S)", " ", body)
    return body


def main():
    check = "--check" in sys.argv
    planned = {}
    counts = {"em": 0, "range": 0, "era": 0}
    for name in sorted(os.listdir(DOCS)):
        if not name.endswith(".html"):
            continue
        path = os.path.join(DOCS, name)
        html = open(path, encoding="utf-8").read()
        pane = PANE.search(html)
        if not pane:
            continue
        old = pane.group(2)
        counts["em"] += old.count(" -- ")
        counts["era"] += old.count("27 BC \u2013 AD 14")
        counts["range"] += len(re.findall(r"(?<=\d)\u2013(?=\d)", old))
        new = BODY.sub(lambda m: m.group(1) + fix(m.group(2)) + m.group(3), old)
        if new == old:
            continue
        full = html[:pane.start(2)] + new + html[pane.end(2):]
        o, c = len(re.findall(r"<div\b", full)), len(re.findall(r"</div>", full))
        if o != c:
            print(f"refusing {name}: div imbalance {o} vs {c}")
            return 1
        if len(full) - len(html) != len(new) - len(old):
            print(f"refusing {name}: splice length mismatch")
            return 1
        planned[path] = full
    print(f"em dash fixes {counts['em']}, numeric ranges {counts['range']}, "
          f"era range {counts['era']}")
    if not check:
        for path, full in planned.items():
            open(path, "w", encoding="utf-8").write(full)
    print(f"{'would touch' if check else 'touched'} {len(planned)} pages")
    return 0


if __name__ == "__main__":
    sys.exit(main())
