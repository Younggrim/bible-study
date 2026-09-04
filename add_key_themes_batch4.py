#!/usr/bin/env python3
"""Batch 4: Ruth 1-4 (whole book, chapter 1 included), Galatians 2-6.
See add_key_themes_batch1.py.

    python3 add_key_themes_batch4.py [--check]
"""
import sys

from add_key_themes_batch1 import process

DATA = {
    "ruth1": (
        "Historical Narrative",
        "A famine that sends a family from the house of bread to the "
        "country of Israel's enemy, three burials that empty Naomi of "
        "husband and both sons, a blessing offered to daughters-in-law "
        "from a woman with nothing left to give, Ruth's vow that moves "
        "from geography to God to death itself, and a name changed from "
        "Naomi to Mara before either woman knows what God is doing",
    ),
    "ruth2": (
        "Historical Narrative",
        "Gleaning laws that provide dignity through labor rather than "
        "charity, a chance encounter the narrator names as providence, "
        "Boaz's instructions that each exceed what the law required, an "
        "ephah of barley too large to be accidental, and Naomi's "
        "bitterness giving way the moment she hears the word redeemer",
    ),
    "ruth3": (
        "Historical Narrative",
        "A threshing floor plan that is bold without being improper, feet "
        "uncovered at midnight and a startled question in the dark, "
        "kindness named greater the second time than the first, a nearer "
        "kinsman acknowledged before any promise is made, and six measures "
        "of barley sent to Naomi by name",
    ),
    "ruth4": (
        "Historical Narrative",
        "A legal transaction conducted in public at the gate with ten "
        "witnesses, land offered before the obligation that comes with it "
        "is disclosed, a nearer kinsman who saves his own name by losing "
        "it from the record, a sandal ceremony the narrator has to explain "
        "to his own readers, and a genealogy that runs from Perez through "
        "Boaz to David in ten generations",
    ),
    "galatians2": (
        "Epistle — Pauline",
        "A private meeting in Jerusalem that adds nothing to Paul's "
        "gospel, right hands of fellowship extended by men called pillars, "
        "Peter withdrawn from Gentile believers out of fear rather than "
        "conviction, a public rebuke delivered to an apostle's face, and a "
        "confession that it is no longer I who live but Christ who lives "
        "in me",
    ),
    "galatians3": (
        "Epistle — Pauline",
        "Experience of the Spirit cited as evidence before any argument "
        "from scripture, Abraham believing God 430 years before the law "
        "existed, a curse and a promise both quoted from the law against "
        "itself, the law described as a schoolmaster rather than a "
        "permanent guardian, and neither Jew nor Greek, bond nor free, "
        "male nor female left standing as a basis for standing before God",
    ),
    "galatians4": (
        "Epistle — Pauline",
        "An heir no different from a slave until the appointed time, "
        "adoption sealed by the Spirit crying Abba, Father, a personal "
        "appeal that recalls eyes the Galatians would once have plucked "
        "out for him, weak and beggarly elements traded back for days and "
        "months and years, and two women read as two covenants, Hagar for "
        "bondage and Sarah for promise",
    ),
    "galatians5": (
        "Epistle — Pauline",
        "Liberty declared before any instruction on how to use it, "
        "circumcision accepted as salvation shown to obligate the whole "
        "law, freedom fulfilled in serving one another rather than the "
        "flesh, works of the flesh and fruit of the Spirit listed as two "
        "harvests rather than two rule-books, and a flesh already "
        "crucified alongside its affections and lusts",
    ),
    "galatians6": (
        "Epistle — Pauline",
        "A fallen brother restored gently by those aware of their own "
        "vulnerability, burdens borne as the law of Christ rather than an "
        "optional kindness, sowing to the flesh or to the Spirit named as "
        "the whole of the choice, Paul's own large handwriting offered as "
        "proof he wrote this closing himself, and marks of persecution "
        "claimed as the only credentials that matter",
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
