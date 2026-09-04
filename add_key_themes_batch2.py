#!/usr/bin/env python3
"""Batch 2: James 2-5, 1 John 2-5. See add_key_themes_batch1.py for the
mechanism (chapter 1 of each book already carries the Classification / Key
Themes pair, so only later chapters are listed here).

    python3 add_key_themes_batch2.py [--check]
"""
import sys

from add_key_themes_batch1 import process

DATA = {
    "james2": (
        "Epistle — General, Wisdom",
        "Favoritism toward the wealthy tried as a case in the royal law's own "
        "court, mercy set against judgment as the standard a merciless person "
        "will be judged by, faith without works pronounced dead rather than "
        "merely incomplete, Abraham and Rahab paired as an unlikely couple to "
        "prove the same point, and a distinction from Paul that argues before "
        "men rather than against him",
    ),
    "james3": (
        "Epistle — General, Wisdom",
        "Teachers warned of a stricter judgment before the tongue is even "
        "mentioned, six images stacked on top of each other for one small "
        "member, a spring pressed to explain how it yields both sweet and "
        "bitter water, wisdom split into two kinds identified by their fruit "
        "rather than their claims, and envy and strife named devilish "
        "alongside a wisdom that is first pure and only then peaceable",
    ),
    "james4": (
        "Epistle — General, Wisdom",
        "Wars traced to lusts warring within before any external cause is "
        "named, friendship with the world called enmity with God without "
        "qualification, ten commands fired in succession with no elaboration "
        "between them, judging a brother diagnosed as usurping the one "
        "Lawgiver's seat, and boasting about tomorrow corrected by a life "
        "called a vapour",
    ),
    "james5": (
        "Epistle — General, Wisdom",
        "Wages kept back from laborers described as crying out on their own, "
        "patience commended by a farmer's wait rather than a soldier's "
        "discipline, oaths reduced to a plain yes and no, sickness answered "
        "with elders, oil and the prayer of faith rather than only sympathy, "
        "and a wanderer's rescue valued as saving a soul from death",
    ),
    "1john2": (
        "Epistle — General",
        "An advocate supplied for the sin John has just written to prevent, "
        "obedience treated as proof of knowledge rather than a separate "
        "requirement, an old commandment restated as new because it is now "
        "true in Christ and in the reader, three groups addressed by what is "
        "already true of them before anything is asked of them, and "
        "antichrists whose departure is offered as evidence they never "
        "belonged",
    ),
    "1john3": (
        "Epistle — General",
        "A love that gives the name children of God before it explains what "
        "that will finally mean, sin defined as lawlessness rather than left "
        "undefined, Cain set up as the counter-example to a command to love, "
        "love proved in deed and truth rather than word and tongue, and a "
        "heart's condemnation answered by a God who is greater than the "
        "heart",
    ),
    "1john4": (
        "Epistle — General",
        "Spirits tested by one confession rather than by their eloquence, "
        "love traced back to its origin in God rather than treated as a "
        "human achievement, propitiation defined by whose love moved first, "
        "perfect love cast out against fear rather than coexisting with it, "
        "and love for God and hatred of a brother declared impossible to "
        "hold together",
    ),
    "1john5": (
        "Epistle — General",
        "Faith named as the victory that overcomes the world rather than "
        "only the means to it, water and blood joined as one witness against "
        "a Christ reduced to water alone, three witnesses agreeing where "
        "human testimony would need only two, assurance stated as the "
        "letter's declared purpose rather than an incidental comfort, and a "
        "final warning to keep from idols placed at the very end without "
        "transition",
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
