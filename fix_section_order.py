#!/usr/bin/env python3
"""
Puts verse-range sections back into the order the chapter runs.

A pane that covers every verse can still read wrongly if its sections are out of
sequence. leviticus25 described the sabbath year at vv.18-22 before the jubilee at
vv.8-17. mark15 put the centurion's confession at v.39 before Simon of Cyrene at
v.21. Coverage checks cannot see this, which is why it survived.

Only the verse-range sections are moved, and they are moved only into the slots
sections already occupy. Book-level fields and inherited topical notes without a
range keep their positions exactly, because their place on the page is a choice
rather than a consequence of the text: Historical Context belongs near the top and
notes like 'Bethany:' or 'Herod the Great:' were put where somebody wanted them.

Sorting is by first verse, and half-verses sort with their verse, so a section at
vv.5-7a stays ahead of one at vv.7b-9.

Usage:
    python3 fix_section_order.py [--check]
"""
import html as H
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import audit_authorship as A

DOCS = A.DOCS
ITEM_RE = re.compile(
    r'<div class="auth-item"><span class="auth-label">(.*?)</span>\s*(.*?)</div>', re.S)
ITEM = ('                    <div class="auth-item">'
        '<span class="auth-label">{label}</span> {body}</div>')


def sort_key(label):
    m = A.TAIL.search(H.unescape(label).strip())
    got = A.halves(m.group(1))
    first = min(got, key=lambda vh: (vh[0], vh[1]))
    return (first[0], 0 if first[1] == "a" else 1)


def main():
    check = "--check" in sys.argv
    planned, problems, notes = {}, [], []
    for name in sorted(os.listdir(DOCS)):
        if not name.endswith(".html"):
            continue
        page = name[:-5]
        path = os.path.join(DOCS, name)
        html = open(path, encoding="utf-8").read()
        pane = A.PANE.search(html)
        if not pane:
            continue
        items = [[a, b.strip()] for a, b in ITEM_RE.findall(pane.group(2))]
        slots = [i for i, (label, _) in enumerate(items)
                 if A.TAIL.search(H.unescape(label).strip())]
        if len(slots) < 2:
            continue
        current = [items[i] for i in slots]
        ordered = sorted(current, key=lambda it: sort_key(it[0]))
        if ordered == current:
            continue
        moved = [H.unescape(it[0]).strip() for a, it in zip(current, ordered)
                 if a is not it]
        for slot, it in zip(slots, ordered):
            items[slot] = it
        notes.append(f"{page}: reordered {len(moved)} section(s), "
                     f"first now {H.unescape(ordered[0][0]).strip()!r}")
        parts = ["\n                <h3>Authorship &amp; Background</h3>\n"]
        for label, body in items:
            parts.append(ITEM.format(label=label, body=body) + "\n")
        new_body = "".join(parts) + "            </div>\n\n            "
        new = html[:pane.start(2)] + new_body + html[pane.end(2):]
        o, c = len(re.findall(r"<div\b", new)), len(re.findall(r"</div>", new))
        if o != c:
            problems.append(f"{page}: div imbalance {o} vs {c}")
            continue
        if len(ITEM_RE.findall(new_body)) != len(items):
            problems.append(f"{page}: field count changed")
            continue
        planned[path] = new
    if problems:
        print(f"refusing to write, {len(problems)} problem(s)")
        for p in problems:
            print(f"    {p}")
        return 1
    for n in notes:
        print(f"    {n}")
    if not check:
        for path, new in planned.items():
            open(path, "w", encoding="utf-8").write(new)
    print(f"{'would reorder' if check else 'reordered'} {len(planned)} page(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
