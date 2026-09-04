#!/usr/bin/env python3
"""Batch 3: 1 Peter 2-5, 1 Thessalonians 2-5. See add_key_themes_batch1.py.

    python3 add_key_themes_batch3.py [--check]
"""
import sys

from add_key_themes_batch1 import process

DATA = {
    "1peter2": (
        "Epistle — General",
        "A stone rejected by builders made the cornerstone of a spiritual "
        "house, a chosen generation and royal priesthood named for people "
        "who were once no people, freedom used as a covering for good "
        "conduct rather than an excuse, submission urged toward government "
        "and masters alike for the Lord's sake, and Christ's silent "
        "endurance offered as the pattern rather than only the payment",
    ),
    "1peter3": (
        "Epistle — General",
        "A wife's conduct trusted to win a husband where words have failed, "
        "an inner adornment of a meek and quiet spirit set against outward "
        "ornament, blessing returned for evil instead of evil for evil, an "
        "answer for one's hope demanded but required to be gentle, and a "
        "disputed descent to spirits in prison tied to baptism as the "
        "answer of a good conscience",
    ),
    "1peter4": (
        "Epistle — General",
        "A former life declared sufficient rather than merely regrettable, "
        "love covering a multitude of sins ranked above every other "
        "instruction, gifts administered as a stewardship of grace rather "
        "than a personal possession, fiery trials met with rejoicing "
        "instead of surprise, and judgment beginning at the house of God "
        "before it reaches anyone else",
    ),
    "1peter5": (
        "Epistle — General",
        "Elders charged to shepherd willingly and for no reward rather than "
        "under compulsion, humility commanded of the young toward elders "
        "and of all before God's mighty hand, anxiety cast wholly onto a "
        "God who cares rather than partly managed, an adversary pictured as "
        "a roaring lion rather than a distant threat, and a letter that "
        "names its carrier, its city and its kiss of charity before it "
        "ends",
    ),
    "1thessalonians2": (
        "Epistle — Pauline",
        "A ministry defended point by point against a slander it never "
        "states outright, boldness claimed despite suffering already "
        "endured at Philippi, gentleness compared to a nursing mother and "
        "burden compared to a father, a word received as God's own rather "
        "than as merely human, and Paul calling himself orphaned by a "
        "separation he did not choose",
    ),
    "1thessalonians3": (
        "Epistle — Pauline",
        "An uncertainty Paul says he could no longer bear, Timothy sent "
        "alone to a church still under the persecution Paul had already "
        "warned them about, good news received as though it were Paul's "
        "own life restored, a prayer for a path back measured alongside a "
        "prayer for their holiness, and love asked to increase and abound "
        "before any specific instruction follows",
    ),
    "1thessalonians4": (
        "Epistle — Pauline",
        "Sanctification named as God's will in so many words rather than "
        "left implied, sexual conduct governed by not defrauding a brother "
        "rather than only personal restraint, ambition redirected toward a "
        "quiet life and working with one's own hands, grief answered with "
        "information rather than only comfort, and the dead in Christ "
        "rising first before the living are caught up to meet them",
    ),
    "1thessalonians5": (
        "Epistle — Pauline",
        "A day arriving as a thief for those who say peace and safety, "
        "children of light distinguished from the day by category rather "
        "than by watchfulness alone, a run of short commands fired with "
        "almost no elaboration between them, the Spirit named as something "
        "that can be quenched by neglect, and a letter placed under oath to "
        "be read to every brother rather than kept with the leadership",
    ),
}


def main():
    check = "--check" in sys.argv
    bad = 0
    for book, (classification, themes) in DATA.items():
        status = process(book, classification, themes, check)
        print(f"{book}: {status}")
        if status not in ("ok", "already-has"):
            bad += 1
    print(f"\n{'checked' if check else 'wrote'} {len(DATA)} pages, {bad} problems")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
