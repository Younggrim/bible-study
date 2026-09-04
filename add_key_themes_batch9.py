#!/usr/bin/env python3
"""Batch 9: 2 Corinthians 1-13 (the whole book, including chapter 1, which
had no Classification/Key Themes pair at all). See add_key_themes_batch1.py.

    python3 add_key_themes_batch9.py [--check]
"""
import sys

from add_key_themes_batch1 import process

CLS = "Epistle — Pauline"

DATA = {
    "2corinthians1": (CLS,
        "Comfort received explicitly so it can be passed to others in "
        "trouble, a trouble in Asia named only by its effect, a clear "
        "conscience offered as the one boast Paul allows himself, yea "
        "and amen argued from Paul's own reliability up to God's, and an "
        "explicit refusal to have dominion over their faith"),
    "2corinthians2": (CLS,
        "A visit cancelled to avoid the very scene a letter was meant to "
        "prevent, tears named as the letter's true composition rather "
        "than its rebuke, forgiveness commanded for a repentant man lest "
        "sorrow swallow him whole, a sentence left broken off at Troas "
        "and not resumed until chapter seven, and a triumphal procession "
        "where the same fragrance means life to one and death to "
        "another"),
    "2corinthians3": (CLS,
        "Changed lives offered as a letter of commendation written "
        "without ink, an old covenant of glory that still brought "
        "condemnation set against a new covenant that brings "
        "righteousness, sufficiency for the ministry located outside the "
        "minister before any comparison begins, a veil removed only when "
        "a heart turns to the Lord, and believers changed from glory to "
        "glory by beholding rather than by effort"),
    "2corinthians4": (CLS,
        "A ministry held without resorting to craftiness or a deceitful "
        "use of the word, a god of this world blinding minds rather than "
        "an argument simply failing to persuade, treasure deliberately "
        "kept in earthen vessels so the power is credited to God, four "
        "pairs of pressures each conceded and each denied the last word, "
        "and a light and momentary affliction weighed against a weight "
        "of glory"),
    "2corinthians5": (CLS,
        "A body compared to a tent groaning for a building not made "
        "with hands, love constraining a ministry between only two "
        "possible motives, a new creature declared rather than an old "
        "one merely improved, reconciliation described twice in three "
        "verses as both a ministry and a message not of Paul's own "
        "invention, and Christ made sin for those who never sinned so "
        "they could be made righteousness they never earned"),
    "2corinthians6": (CLS,
        "Grace that can be received in vain if the moment it is offered "
        "is allowed to pass, ministry credentials built from suffering "
        "rather than comfort, paradoxes stacked one after another as "
        "though the world's verdict and reality can both be spoken at "
        "once, an enlarged heart met by a restriction Paul locates on "
        "their side rather than his, and light and darkness declared "
        "incompatible in the same yoke"),
    "2corinthians7": (CLS,
        "A sentence broken off in chapter two picked up again with an "
        "honest account of no rest and fears within, comfort arriving by "
        "an arrival rather than an insight, godly sorrow distinguished "
        "from worldly sorrow by what each one produces, seven results of "
        "genuine repentance listed as active rather than passive, and "
        "Titus returning refreshed with a report Paul was not ashamed of"),
    "2corinthians8": (CLS,
        "Macedonian churches giving beyond their power out of deep "
        "poverty rather than surplus, giving themselves to the Lord "
        "named as the act that precedes giving their money, Christ's own "
        "poverty offered as the pattern for a collection rather than as "
        "an illustration, willingness measured against ability rather "
        "than against a fixed amount, and a delegation of several men "
        "arranged so no one could blame Paul over money he never touched "
        "alone"),
    "2corinthians9": (CLS,
        "A chapter written to say a letter was unnecessary, sowing "
        "bountifully and sparingly set against each other as the whole "
        "of the principle, a cheerful giver preferred to a grudging one "
        "regardless of the amount given, five alls describing a "
        "sufficiency so complete it can always abound to every good "
        "work, and thanksgiving named as a second harvest the collection "
        "produces beside meeting the need"),
    "2corinthians10": (CLS,
        "Critics quoted before they are answered rather than "
        "paraphrased, weapons of warfare declared not carnal though "
        "mighty enough to pull down strongholds, authority claimed for "
        "building up and immediately limited against tearing down, an "
        "accusation about a weak presence and a contemptible speech met "
        "without denial, and boasting measured by another man's line "
        "rejected as unwise however common it was"),
    "2corinthians11": (CLS,
        "A fool's speech Paul names as folly before he ever begins it, "
        "jealousy compared to a father guarding a bride's purity rather "
        "than a rival defending territory, refusing payment turned from "
        "an insult into a boast about robbing other churches instead, "
        "Satan transformed into an angel of light offered as the reason "
        "false apostles are dangerous precisely because they look good, "
        "and a catalogue of beatings and shipwrecks that ends with being "
        "lowered from a wall in a basket"),
    "2corinthians12": (CLS,
        "A vision of paradise told in the third person by a man "
        "reluctant to boast even about what is true, a thorn in the "
        "flesh refused removal three times and answered with sufficient "
        "grace instead, signs of an apostle claimed once and briefly "
        "rather than dwelt on, a fear of finding envyings and strife "
        "rather than the welcome he was hoping for, and love that goes "
        "unanswered named plainly rather than hidden"),
    "2corinthians13": (CLS,
        "A third visit announced under the same rule of two or three "
        "witnesses used for legal testimony, self-examination turned "
        "back onto the readers instead of onto Paul's own credentials, a "
        "willingness to appear disapproved himself so long as the "
        "Corinthians do what is right, four short imperatives offered as "
        "a summary of the whole letter, and a Trinitarian benediction "
        "naming grace, love and fellowship as three distinct gifts from "
        "three persons"),
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
