#!/usr/bin/env python3
"""
leviticus27 was the last pane outside Psalms still carrying an <ul class="auth-sublist">,
and it survived because the prose depended on it. The vv.1-8 section ended on a colon,
"a monetary equivalent is established:", and handed the eight shekel figures to the list.
A headless auth-item then continued the same discussion after the list. Coverage checks
could not see any of this, because the label itself is well formed.

This folds the figures and the continuation into the one section as prose and drops both
the list and the headless item. It is the Joshua 12 case from WORKFLOW.md: every list item
carried a verse range, so the mechanical test cleared it for deletion, yet the sections
never restated the content and deleting it would have removed every figure in the chapter.

Two factual claims in the old text are corrected rather than carried over.

  1. It said thirty shekels was "the price of a female slave or a male between 5-20".
     A male between five and twenty is valued at twenty shekels in v.5, not thirty.
  2. It said the thirty was "the price of the least valuable category of adult".
     It is not. A male over sixty is fifteen and a female over sixty is ten, in v.7.

What is true is that thirty shekels is the valuation of a woman between twenty and sixty
in v.4, that Exodus 21:32 sets the same sum as compensation when an ox kills a slave, and
that Zechariah 11:12-13 uses it for a wage offered in contempt, which is the text Matthew
27:9-10 cites over Judas.

Usage:
    python3 fix_leviticus27_valuation.py [--check]
"""
import os
import re
import sys

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")
PAGE = os.path.join(DOCS, "leviticus27.html")

# The section body, the sublist and the headless continuation, as one run.
OLD = re.compile(
    r'<div class="auth-item"><span class="auth-label">'
    r'Valuation of Persons Dedicated by Vow \(vv\.1-8\):</span>.*?'
    r'</ul>\s*<div class="auth-item">If the person is too poor.*?</div>',
    re.S)

NEW = (
    '<div class="auth-item"><span class="auth-label">'
    'Valuation of Persons Dedicated by Vow (vv.1-8):</span> When someone makes a '
    '&quot;singular vow&quot; in KJV&#x27;s phrase, a &quot;special vow&quot; in '
    'ESV&#x27;s, dedicating a person to the LORD&#x27;s service (v.2), that person '
    'cannot be laid on an altar, so the law fixes a monetary equivalent instead. The '
    'scale runs by age and by sex, in sanctuary shekels of silver: a male between '
    'twenty and sixty is valued at fifty and a female of the same years at thirty '
    '(vv.3-4); from five to twenty the figures are twenty and ten (v.5); from one '
    'month to five years, five and three (v.6); and above sixty, fifteen and ten '
    '(v.7). Read as a price on people the list is offensive, and that is not what it '
    'is. The amounts track what a person&#x27;s labour was worth in an agricultural '
    'economy, which is why they peak in the working years and drop at both ends of '
    'life, and nothing in the chapter offers them as a measure of worth. Verse 8 '
    'settles the point by breaking the scale altogether: if the man is too poor for '
    'the valuation, the priest sets a figure he can actually pay, so no one is shut '
    'out of vowing by being unable to afford it. One number here has a long echo. '
    'Thirty shekels is the valuation of a woman between twenty and sixty, it is what '
    'Exodus 21:32 requires of an owner whose ox has killed another man&#x27;s slave, '
    'and it is the sum Judas took in Matthew 26:15 — which Matthew 27:9-10 reads '
    'against Zechariah 11:12-13, where thirty pieces of silver are a wage offered in '
    'contempt and thrown back.</div>')


def main():
    check = "--check" in sys.argv
    html = open(PAGE, encoding="utf-8").read()
    m = OLD.search(html)
    if not m:
        if 'class="auth-sublist"' in html:
            print("leviticus27: sublist present but the expected run did not match")
            return 1
        print("leviticus27: already repaired, nothing to do")
        return 0
    new = html[:m.start()] + NEW + html[m.end():]
    for bad, why in (('class="auth-sublist"', "sublist survived"),
                     ("is established:", "section still ends on a colon")):
        if bad in new:
            print(f"refusing to write, {why}")
            return 1
    for figure in ("fifty", "thirty", "twenty and ten", "five and three",
                   "fifteen and ten"):
        if figure not in new:
            print(f"refusing to write, lost the figure {figure!r}")
            return 1
    print(f"    leviticus27: folded 8 sublist figures and the headless "
          f"continuation into the vv.1-8 section")
    print(f"    leviticus27: dropped the sublist")
    print(f"    leviticus27: corrected the thirty-shekel claim")
    if not check:
        open(PAGE, "w", encoding="utf-8").write(new)
    print(f"{'would repair' if check else 'repaired'} 1 page")
    return 0


if __name__ == "__main__":
    sys.exit(main())
