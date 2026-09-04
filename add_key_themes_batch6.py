#!/usr/bin/env python3
"""Batch 6: Hebrews 2-13. See add_key_themes_batch1.py.

    python3 add_key_themes_batch6.py [--check]
"""
import sys

from add_key_themes_batch1 import process

CLS = "Epistle — Sermon or Treatise"

DATA = {
    "hebrews2": (CLS,
        "A first warning naming drifting rather than rebellion as the real "
        "danger, the world to come subjected to man rather than to angels, "
        "a Son made lower than the angels for the specific purpose of "
        "tasting death, brethren claimed rather than merely subjects "
        "addressed, and temptation endured so help could be offered "
        "rather than only judgment avoided"),
    "hebrews3": (CLS,
        "A house compared to its builder to argue for a Son greater than "
        "a servant, Moses honored fully before being surpassed, a second "
        "warning drawn from Israel's forty years rather than from a new "
        "offense, hardening traced to unbelief rather than to "
        "circumstance, and daily exhortation urged as the remedy for a "
        "heart no one notices going wrong"),
    "hebrews4": (CLS,
        "A rest still open though a whole generation failed to enter it, "
        "the good news that profits only when mixed with faith, God's own "
        "rest offered as the pattern rather than Canaan alone, a word "
        "described as living and sharper than a sword before any comfort "
        "is offered, and a throne of grace approached boldly because the "
        "High Priest has already been tempted in every way"),
    "hebrews5": (CLS,
        "Qualifications for a high priest listed before Christ is shown "
        "to exceed them, strong crying and tears placed inside a chapter "
        "about qualification rather than emotion, obedience learned "
        "through suffering by one who was already a Son, an order named "
        "after Melchizedek and left unexplained until later, and a "
        "rebuke for readers who should already be teachers but need milk "
        "again"),
    "hebrews6": (CLS,
        "Elementary teachings named and set aside rather than repeated, a "
        "third warning describing privileges tasted rather than merely "
        "professed, land that drinks the same rain and yields thorns "
        "instead of a crop, an anchor of the soul entering behind the "
        "veil ahead of the one who holds it, and two unchangeable things, "
        "God's promise and God's oath, offered together for strong "
        "consolation"),
    "hebrews7": (CLS,
        "A king of Salem with no recorded genealogy made like the Son of "
        "God, Abraham tithing to a priest he never served under, Levi "
        "paying tithes while still in his own ancestor's body, a "
        "priesthood grounded in an endless life rather than a bloodline, "
        "and a Savior who lives to make intercession because His "
        "priesthood never changes hands"),
    "hebrews8": (CLS,
        "A priest already seated because the work is already finished, an "
        "earthly tabernacle called a shadow of a pattern shown on a "
        "mountain, the longest Old Testament quotation in the New "
        "Testament borrowed to prove a new covenant was always coming, "
        "laws promised for hearts rather than tablets, and an old "
        "covenant declared obsolete by its own prophet"),
    "hebrews9": (CLS,
        "A Most Holy Place entered only once a year and only with blood, "
        "sacrifices unable to perfect the conscience no matter how often "
        "repeated, Christ's own blood offered in a greater and more "
        "perfect tabernacle, a testament requiring the death of the one "
        "who made it, and an appearance promised a second time for "
        "salvation rather than to deal with sin again"),
    "hebrews10": (CLS,
        "Sacrifices repeated endlessly shown incapable of the one thing "
        "they were for, a priest who sat down because one offering "
        "finished what daily offerings could not, sins remembered no "
        "more named as the new covenant's own promise, a fourth warning "
        "aimed at willful sin after the truth is known, and assembling "
        "together urged as a plain defense against drawing back"),
    "hebrews11": (CLS,
        "Faith defined as substance and evidence before a single example "
        "is given, a catalogue of witnesses who acted without seeing what "
        "they hoped for, Abraham leaving and Sarah believing named side "
        "by side, faith's cost counted honestly in torture and death "
        "alongside its triumphs, and every name in the chapter dying "
        "without receiving what was promised"),
    "hebrews12": (CLS,
        "A cloud of witnesses named to explain a race rather than to be "
        "admired for its own sake, discipline read as proof of sonship "
        "rather than evidence of rejection, Esau held up as the warning "
        "for trading a birthright for one meal, Sinai and Zion set "
        "against each other as two mountains for two covenants, and a "
        "fifth and final warning ending in a kingdom that cannot be "
        "shaken"),
    "hebrews13": (CLS,
        "Practical commands fired in short bursts after twelve chapters "
        "of argument, Jesus Christ the same yesterday, today and forever "
        "anchoring a warning against strange doctrines, an appeal to go "
        "outside the camp bearing His reproach rather than staying within "
        "the old system, praise named a sacrifice of the lips rather than "
        "an animal offering, and a request for prayer that is the one "
        "thing the author asks for himself in the whole letter"),
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
