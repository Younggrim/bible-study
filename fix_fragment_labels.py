#!/usr/bin/env python3
"""
Merges sentence-fragment labels back into the field they were cut out of.

The defect is a sentence split at a colon, with the first half promoted into a
heading:

    <span class="auth-label">The chapter divides into two movements:</span>
    an account of Hezekiah's reform and then Sennacherib's invasion...

Read on the page it produces a heading that is half a sentence and a paragraph that
begins mid-thought. There is nothing to write here and nothing to decide: the two
halves are rejoined in place, in the field immediately above, which is where the
sentence was before somebody put a label around its opening clause.

ezekiel29 is the clearest case of what went wrong. Its label is 'The first oracle
(29:' because the colon that got split on was the one between chapter and verse.

Two pages carry two fragments each, and the rejoining is done from the bottom of
the pane upward so that merging one does not move the other.

Detection is shared with audit_authorship.label_fault, so the check that reports
the defect and the pass that repairs it cannot disagree about what counts as one.

Usage:
    python3 fix_fragment_labels.py [--check]
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
        bad = [i for i, (label, _) in enumerate(items)
               if A.label_fault(H.unescape(label).strip())]
        if not bad:
            continue
        for i in reversed(bad):
            if i == 0:
                problems.append(f"{page}: fragment is the first field, nothing above it")
                continue
            label = items[i][0].rstrip()
            joined = label + " " + items[i][1]
            # A label cut inside a verse reference has no space after its colon.
            sep = "" if label.endswith(":") and re.search(r"\(\w*\s*\d+:$", label) else " "
            items[i - 1][1] = (items[i - 1][1].rstrip() + " " + label + sep
                               + items[i][1]).strip()
            del items[i]
            notes.append(f"{page}: merged {H.unescape(label).strip()!r} upward")
        parts = ["\n                <h3>Authorship &amp; Background</h3>\n"]
        for label, body in items:
            parts.append(ITEM.format(label=label, body=body) + "\n")
        new_body = "".join(parts) + "            </div>\n\n            "
        new = html[:pane.start(2)] + new_body + html[pane.end(2):]
        o, c = len(re.findall(r"<div\b", new)), len(re.findall(r"</div>", new))
        if o != c:
            problems.append(f"{page}: div imbalance {o} vs {c}")
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
    print(f"{'would merge' if check else 'merged'} {len(notes)} fragment(s) "
          f"across {len(planned)} pages")
    return 0


if __name__ == "__main__":
    sys.exit(main())
