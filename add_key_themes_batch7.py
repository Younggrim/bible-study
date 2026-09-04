#!/usr/bin/env python3
"""Batch 7: John 8, 9, 11, 12, 13, 15, 16, 18, 20 (the chapters of John
missing the pair; several others already had it). See
add_key_themes_batch1.py.

    python3 add_key_themes_batch7.py [--check]
"""
import sys

from add_key_themes_batch1 import process

CLS = "Gospel — Narrative and Discourse"

DATA = {
    "john8": (CLS,
        "A trap set by quoting Moses that dismantles itself against the "
        "ground, light of the world declared during the feast where the "
        "great lamps were lit, freedom claimed by people who deny they "
        "were ever in bondage, paternity argued down to the hardest "
        "sentence spoken to anyone in the Gospels, and before Abraham "
        "was, I am, answered with stones"),
    "john9": (CLS,
        "A question about blame refused before the healing even happens, "
        "clay made from spittle on the sabbath turned into the real "
        "charge, a man's answers escalating from a man called Jesus to "
        "the Son of God, parents who answer only what they cannot be "
        "blamed for, and sight and blindness reversed until admitted "
        "blindness cures and claimed sight condemns"),
    "john11": (CLS,
        "A message that states love and is answered with a deliberate "
        "delay, resurrection and life relocated from a doctrine to a "
        "person, the shortest verse in the Bible standing beside a death "
        "Jesus intends to undo, a stone rolled away against Martha's "
        "practical objection, and a council that never disputes the "
        "miracle only its political consequences"),
    "john12": (CLS,
        "An anointing defended as a burial before anyone else "
        "understands it that way, a crowd shouting Hosanna for a king "
        "who arrives on a donkey, Greeks seeking Jesus made the signal "
        "that His hour has finally come, a grain of wheat that must die "
        "to multiply, and Isaiah's throne vision read backward as a "
        "vision of Christ's glory"),
    "john13": (CLS,
        "A towel and basin used by someone who knows all things have "
        "been given into His hands, Peter's refusal reversed to its "
        "opposite extreme in the same breath, a sop handed to Judas as an "
        "honor at the very moment of betrayal, a new commandment measured "
        "by as I have loved you, and a promise of loyalty predicted to "
        "fail before the night is over"),
    "john15": (CLS,
        "A seventh and final I AM saying that places the hearers inside "
        "the image, abide repeated as the word that carries the whole "
        "passage, pruning done by the same hand whether or not a branch "
        "bears fruit, servants reclassified as friends because everything "
        "has been disclosed, and a world's hatred explained as hatred of "
        "Christ passed on to those who follow Him"),
    "john16": (CLS,
        "Departure named as expedient because the Comforter cannot come "
        "otherwise, the Spirit's threefold work of convicting the world "
        "of sin, righteousness and judgment, truth still withheld because "
        "the disciples cannot yet bear it, sorrow compared to labor "
        "forgotten in what it produces, and tribulation and overcoming "
        "held together in the same closing sentence without softening "
        "either"),
    "john18": (CLS,
        "An arrest where Jesus asks the questions and takes the "
        "initiative throughout, Peter's sword answered by a question "
        "about a cup rather than a rebuke, three denials completed "
        "exactly as predicted at the same fire of coals, six trials that "
        "never produce evidence only pressure, and a kingdom defined as "
        "not of this world and proven by the absence of a fight"),
    "john20": (CLS,
        "Grave clothes left folded rather than stripped away, a name "
        "spoken once turning a mistaken gardener into a witness, peace "
        "offered twice with wounds shown between the two greetings, a "
        "condition for belief stated bluntly and met without a single "
        "recorded touch, and a purpose statement naming exactly why the "
        "Gospel was written"),
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
