#!/usr/bin/env python3
"""Batch 8: Mark 2-12, 15, 16 (the chapters of Mark missing the pair;
1, 13, 14 already had it). See add_key_themes_batch1.py.

    python3 add_key_themes_batch8.py [--check]
"""
import sys

from add_key_themes_batch1 import process

CLS = "Gospel — Narrative"

DATA = {
    "mark2": (CLS,
        "A paralytic's sins forgiven before his legs are healed, scribes "
        "who reason correctly about who can forgive sins and stop short "
        "of the conclusion, a tax collector's table chosen deliberately "
        "over the righteous, new cloth and new wine refused a home in old "
        "containers, and the sabbath declared made for man before the Son "
        "of man claims to be its Lord"),
    "mark3": (CLS,
        "A withered hand used as a trap before it is used as a healing, "
        "the one place in the Gospels where Jesus is described as angry, "
        "Pharisees and Herodians allied against a common threat despite "
        "being natural enemies, twelve chosen to be with Him before being "
        "sent out for Him, and a family standing outside while a house "
        "full of strangers is named mother and brothers"),
    "mark4": (CLS,
        "A sower parable called foundational to understanding every "
        "other parable, four soils sorting hearers by what happens after "
        "the seed lands, a seed that grows while the farmer sleeps and "
        "does not know how, a mustard seed's disproportion between its "
        "start and its finish, and a storm rebuked with two words while "
        "the disciples ask what manner of man this is"),
    "mark5": (CLS,
        "A legion of demons overpowered by a single word after no one "
        "else could help, a synagogue ruler kneeling in public because "
        "his daughter is dying, an interruption on the way that costs "
        "precious time yet ends in a name, daughter spoken to a woman "
        "healed after twelve years of isolation, and Talitha cumi "
        "preserved in Jesus' own Aramaic"),
    "mark6": (CLS,
        "A hometown that cannot see past the carpenter it thinks it "
        "knows, twelve sent in pairs with a packing list that is mostly "
        "prohibitions, John's death told as a flashback about a king "
        "trapped by his own rash promise, five loaves and two fish "
        "stretched to feed a multitude, and hearts still hardened even "
        "after the feeding when Jesus walks on the water"),
    "mark7": (CLS,
        "A hand-washing tradition used to nullify a command Moses "
        "actually gave, honoring God with the lips while the heart stays "
        "far away, thirteen sins traced to what comes out of a man "
        "rather than what goes in, a Gentile woman who accepts the "
        "insult and argues from inside it, and Ephphatha spoken privately "
        "with a sigh Mark leaves unexplained"),
    "mark8": (CLS,
        "A second feeding recorded without embarrassment at its "
        "resemblance to the first, a sign refused to a generation with a "
        "sigh deep in the spirit, a warning about leaven mistaken for a "
        "comment on forgotten bread, a blind man healed in two stages "
        "that mirrors the disciples' own half-understanding, and Peter's "
        "confession answered eight verses later with get thee behind me, "
        "Satan"),
    "mark9": (CLS,
        "Glory breaking through six days after a saying about not "
        "tasting death, a father's confession that he believes and needs "
        "help for his unbelief in the same breath, a second passion "
        "prediction met with fear rather than questions, a child taken "
        "in Jesus' arms as the answer to an argument about greatness, "
        "and salt and peace left standing side by side without an "
        "obvious connection"),
    "mark10": (CLS,
        "Divorce answered by going behind Moses' concession to Genesis "
        "itself, Jesus much displeased that children were being turned "
        "away, a rich man Jesus is said to have loved even as he asks "
        "him to give everything away, a saying about a camel and a "
        "needle's eye repeated because of how it was received, and the "
        "ransom verse that is the only place Mark explains the death in "
        "so many words"),
    "mark11": (CLS,
        "A fig tree cursed and a temple cleansed with one story wrapped "
        "around the other, leaves without fruit read as a verdict on "
        "Israel's worship, a question about authority answered with a "
        "counter-question about John's baptism, both sides caught "
        "reasoning out loud about what answer is safe rather than what "
        "is true, and mountain-moving faith tied directly to a readiness "
        "to forgive"),
    "mark12": (CLS,
        "A vineyard parable told to men who recognize themselves in it "
        "before it ends, render to Caesar drawn from a coin's own image "
        "rather than given as a rule, resurrection defended against two "
        "errors named separately, a scribe told he is not far from the "
        "kingdom which is not the same as being in it, and a widow's two "
        "coins valued above every large gift given from surplus"),
    "mark15": (CLS,
        "A charge that changes from blasphemy to kingship on the way to "
        "Pilate, a governor surprised into silence by a defendant who "
        "will not defend himself, Barabbas released as a failure of "
        "nerve Mark names outright, a mock coronation where kneeling is "
        "recorded as worship, and a centurion's confession that finally "
        "answers the Gospel's opening verse"),
    "mark16": (CLS,
        "Spices bought and a stone already rolled away before the "
        "question about it is finished, an errand that names one "
        "disciple specifically among the rest, the earliest manuscripts "
        "ending on fear and silence rather than resolution, a longer "
        "ending debated for centuries as possibly not Mark's own hand, "
        "and a Gospel that leaves its reader to decide whether they too "
        "will tell"),
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
