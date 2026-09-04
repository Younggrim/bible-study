#!/usr/bin/env python3
"""Batch 12: Joshua 1-11 (the whole book). See add_key_themes_batch1.py.

    python3 add_key_themes_batch12.py [--check]
"""
import sys

from add_key_themes_batch1 import process

CLS = "Historical Narrative"

DATA = {
    "joshua1": (CLS,
        "Moses' death and Joshua's commission delivered in the same "
        "breath, territory promised as far as every place the sole of "
        "the foot will tread, three commands to be strong and "
        "courageous each carrying a different emphasis, meditation on "
        "the law day and night tied directly to prosperity and success, "
        "and the people pledging Joshua the same obedience they gave "
        "Moses"),
    "joshua2": (CLS,
        "Two spies sent quietly after the twelve who failed at "
        "Kadesh a generation earlier, Rahab hiding strangers on her "
        "roof under stalks of flax, a pagan woman's confession that the "
        "LORD is God in heaven above and earth beneath, a scarlet cord "
        "tied in a window as an act of faith before any promise is "
        "fulfilled, and a report of confidence returned in place of the "
        "faithless report of Numbers 13"),
    "joshua3": (CLS,
        "The Jordan crossed at flood stage rather than at a season "
        "that would make it easy, consecration commanded the day before "
        "the miracle rather than after it, the ark going ahead of the "
        "people as the proof the living God is among them, waters cut "
        "off and standing in a heap far upstream, and Joshua magnified "
        "in Israel's sight the same way Moses once was"),
    "joshua4": (CLS,
        "Twelve stones taken from the exact spot where the priests' "
        "feet stood, a question children are expected to ask built "
        "into the memorial's whole purpose, two monuments raised, one "
        "in the riverbed and one at Gilgal, so the miracle is "
        "remembered from two directions, waters returning to their "
        "place the instant the priests' feet reach dry land, and a "
        "stated dual purpose, witness to the nations and fear of the "
        "LORD in Israel forever"),
    "joshua5": (CLS,
        "Canaanite kings' hearts melting before a single battle is "
        "fought, circumcision restoring a covenant sign an entire "
        "generation had gone without, a name, Gilgal, explained as the "
        "rolling away of Egypt's reproach, manna ceasing the day after "
        "the first Passover eaten in the land, and a commander of the "
        "LORD's host who answers Joshua's question about whose side he "
        "is on by declining to take either"),
    "joshua6": (CLS,
        "A battle plan that looks absurd by any military standard, "
        "silence commanded for six days before a single shout on the "
        "seventh, the number seven governing days, priests, trumpets "
        "and circuits alike, Rahab named the one exception to a city "
        "otherwise placed under total destruction, and a curse "
        "pronounced on whoever rebuilds Jericho that scripture later "
        "records being fulfilled exactly"),
    "joshua7": (CLS,
        "A private theft turned into a public defeat at a city Israel "
        "should have easily taken, Joshua's grief answered bluntly with "
        "get thee up rather than more prayer, a lot narrowing tribe by "
        "clan by household until it lands on one man, a confession that "
        "echoes I saw, I coveted, I took, the same progression as Eden, "
        "and a valley named Achor as wordplay on the trouble Achan "
        "brought"),
    "joshua8": (CLS,
        "The same words, fear not, neither be thou dismayed, repeated "
        "to restore confidence after failure, plunder permitted at Ai "
        "that had been forbidden at Jericho, an ambush strategy "
        "directed by God rather than a purely miraculous victory, a "
        "spear held outstretched until the destruction is complete, and "
        "a covenant renewal at Ebal where every word Moses commanded is "
        "read without exception"),
    "joshua9": (CLS,
        "A Canaanite coalition uniting for open war while one city "
        "chooses deception instead, moldy bread and worn sandals used "
        "as evidence Israel examines without ever asking counsel of the "
        "LORD, an oath sworn in God's name that binds Israel even after "
        "the deception is discovered, a congregation murmuring against "
        "leaders bound by a promise they regret, and Gibeonites "
        "sentenced to permanent service rather than destruction because "
        "the oath could not be broken"),
    "joshua10": (CLS,
        "A treaty ally's appeal answered by an all-night march rather "
        "than delay, hailstones killing more of the enemy than Israel's "
        "own swords, a sun commanded to stand still so a day of battle "
        "could be finished, captured kings made to have Israel's "
        "captains put their feet on their necks, and a systematic sweep "
        "of the south closing with because the LORD God of Israel "
        "fought for Israel"),
    "joshua11": (CLS,
        "A northern coalition described as sand on the seashore "
        "complete with a technology Israel has never faced before, "
        "horses hamstrung and chariots burned rather than kept as "
        "captured strength, Hazor alone burned among the northern "
        "cities as the coalition's head, a chain of obedience traced "
        "from God to Moses to Joshua leaving nothing undone, and hearts "
        "hardened by God so that the Canaanites would fight rather than "
        "surrender"),
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
