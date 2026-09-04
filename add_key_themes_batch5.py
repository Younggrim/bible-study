#!/usr/bin/env python3
"""Batch 5: Ephesians 2-6, 1 Timothy 2-6. See add_key_themes_batch1.py.

    python3 add_key_themes_batch5.py [--check]
"""
import sys

from add_key_themes_batch1 import process

DATA = {
    "ephesians2": (
        "Epistle — Pauline, Prison Epistle",
        "Spiritual death described as a condition by nature rather than a "
        "series of choices, but God interrupting the sentence at its worst "
        "point, salvation by grace through faith set apart from works "
        "while still leading to them, a dividing wall broken down between "
        "Jew and Gentile, and one new man built together into a temple "
        "rather than merely reconciled",
    ),
    "ephesians3": (
        "Epistle — Pauline, Prison Epistle",
        "A sentence begun and abandoned until Paul can explain why his "
        "imprisonment is for the Gentiles, a mystery defined as three "
        "fellow-words — heirs, members, partakers — held in complete "
        "equality, Paul naming himself less than the least of all saints "
        "as his own credential, a prayer for strength and comprehension "
        "rather than for anything new, and a doxology that measures God "
        "by what exceeds asking or thinking",
    ),
    "ephesians4": (
        "Epistle — Pauline, Prison Epistle",
        "A single therefore that turns three chapters of doctrine into a "
        "command to walk worthy, seven ones offered as the ground of "
        "unity rather than uniformity, gifted leaders given to equip the "
        "saints rather than to do the work for them, an old self put off "
        "and a new self put on like changing clothes, and the Spirit "
        "named as something that can be grieved by careless speech",
    ),
    "ephesians5": (
        "Epistle — Pauline, Prison Epistle",
        "Believers called not merely to have been in darkness but to have "
        "been darkness itself, redeeming the time set alongside being "
        "filled with the Spirit as the same command, singing and "
        "thanksgiving and mutual submission offered as evidence rather "
        "than instruction, marriage read backward from Christ and the "
        "church rather than forward from custom, and a great mystery "
        "named rather than fully explained",
    ),
    "ephesians6": (
        "Epistle — Pauline, Prison Epistle",
        "A household code that reaches children and servants before it "
        "reaches armor, obedience commanded of children as the first "
        "command carrying a promise, mutual accountability planted "
        "between masters and servants who share one Master in heaven, "
        "warfare named against principalities rather than people, and "
        "armor listed piece by piece with prayer holding all of it "
        "together",
    ),
    "1timothy2": (
        "Epistle — Pauline, Pastoral Epistle",
        "Prayer urged for all men and specifically for rulers before any "
        "other instruction, one mediator and one ransom stated against a "
        "backdrop of many, modesty in dress set against costly adornment "
        "as the real point of contrast, teaching authority restricted and "
        "grounded in the order of creation rather than culture, and a "
        "disputed final verse that has divided readers for centuries",
    ),
    "1timothy3": (
        "Epistle — Pauline, Pastoral Epistle",
        "Qualifications for overseers built almost entirely from "
        "character rather than skill, a new convert excluded by rule "
        "rather than by suspicion, deacons held to a nearly identical "
        "standard as a second office, the church named the pillar and "
        "ground of the truth, and a hymn of six lines rising out of a "
        "chapter about household order",
    ),
    "1timothy4": (
        "Epistle — Pauline, Pastoral Epistle",
        "Apostasy predicted explicitly by the Spirit rather than merely "
        "feared, asceticism corrected by declaring creation good and "
        "received with thanksgiving, godliness commended as profitable "
        "for this life and not only the next, youth defended by example "
        "rather than by argument, and a charge to watch doctrine and life "
        "together because one drifts without the other",
    ),
    "1timothy5": (
        "Epistle — Pauline, Pastoral Epistle",
        "Correction addressed by age and relation rather than by rank, a "
        "formal list of widows with real qualifications for enrollment, "
        "family responsibility placed ahead of the church's own "
        "resources, elders granted double honour while also held to a "
        "public standard of accountability, and a personal note about "
        "Timothy's stomach dropped into the middle of church polity",
    ),
    "1timothy6": (
        "Epistle — Pauline, Pastoral Epistle",
        "Servants instructed to honour believing masters more rather than "
        "less, gain mistaken for godliness named as the error underneath "
        "the false teaching, contentment paired with godliness as great "
        "gain against a love of money called a root of all evil, a charge "
        "to fight the good fight framed by a doxology to the King of "
        "kings, and a closing command to guard a deposit rather than to "
        "add to it",
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
