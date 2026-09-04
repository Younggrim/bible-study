#!/usr/bin/env python3
"""Batch 21: Leviticus 1, 6-27 (chapters 2-5 already have Key Themes).

    python3 add_key_themes_batch21.py [--check]
"""
import sys

from add_key_themes_batch1 import process

CLS = "Historical Narrative"

DATA = {
    "leviticus1": (CLS,
        "three tiers of animal, cattle, flock and birds, set side by "
        "side so that wealth never determines whether a worshipper "
        "can approach, a hand laid on the animal's head transferring "
        "identification before a single cut is made, an offering "
        "consumed entirely rather than shared with anyone, blood "
        "handled by priests while the worshipper does the killing "
        "himself, and the same verdict, a sweet savour unto the LORD, "
        "repeated no matter which tier is brought"),
    "leviticus6": (CLS,
        "a guilt offering for fraud that treats lying to a neighbor "
        "as a trespass against God, restitution required at a fifth "
        "above the value before the sacrifice is even offered, a fire "
        "on the altar commanded three times over never to go out, a "
        "priest's own daily grain offering being the one offering in "
        "the whole book he is forbidden to eat any of, and holiness "
        "described as something that spreads by contact rather than "
        "staying contained to the altar"),
    "leviticus7": (CLS,
        "a peace offering distinguished from every other sacrifice by "
        "being the one meal the worshipper himself gets to eat, a "
        "thanksgiving offering that must be eaten the very day it is "
        "brought while a vow offering may stretch to a second, a "
        "third day's leftovers declared not an oversight but an "
        "abomination, fat and blood alike forbidden to any Israelite "
        "because both already belong to God, and a summary verse "
        "tying every offering in the first seven chapters back to the "
        "single mountain where they were all given"),
    "leviticus8": (CLS,
        "seven separate movements, washing, clothing, anointing, sin "
        "offering, burnt offering, ram of consecration and week-long "
        "seclusion, assembled into a single ordination, oil poured "
        "rather than sprinkled on Aaron's head, an ear, a thumb and a "
        "great toe each marked with blood, priests requiring their "
        "own atonement before they can administer anyone else's, and "
        "a warning to keep the charge of the LORD, that ye die not, "
        "hanging over the entire seven days"),
    "leviticus9": (CLS,
        "an eighth day arriving only after seven of confinement, "
        "exactly the order Moses gives Aaron, offer for thyself first "
        "and then for the people, divine fire descending to consume "
        "the offering, the same fire that will consume Nadab and "
        "Abihu one chapter later, a blessing pronounced before the "
        "people are told to shout, and a chapter that ends with faces "
        "on the ground rather than words in reply"),
    "leviticus10": (CLS,
        "the identical fire that validated the sacrifice in the "
        "previous chapter now consuming two priests for offering what "
        "they were never commanded, a father forbidden the ordinary "
        "signs of mourning for his own sons while the rest of Israel "
        "is permitted to grieve, a wine prohibition following "
        "immediately after the deaths with no explanation offered "
        "beyond the reader's own suspicion, a job description reduced "
        "to two clauses, distinguishing holy from unholy and teaching "
        "the statutes, and Moses backing down once he actually hears "
        "Aaron's explanation for the untouched sin offering"),
    "leviticus11": (CLS,
        "two criteria required together rather than either alone for "
        "a land animal to be called clean, a short list of named "
        "exceptions including a pig that looks clean on the outside "
        "while failing the inward test, unclean birds identified not "
        "by a rule but by their diet of carrion and death, insects "
        "permitted only if their legs let them leap rather than "
        "merely crawl, and a repeated refrain, be ye holy, for I am "
        "holy, turning every meal into a small act of identity"),
    "leviticus12": (CLS,
        "the shortest chapter in the book covering one of the most "
        "universal human experiences, an eight-day interruption for "
        "circumcision inserted into a forty-day period of "
        "uncleanness, an unexplained doubling of both stages for a "
        "daughter compared to a son, one offering required regardless "
        "of the child's sex, and a poverty provision that turns out, "
        "centuries later, to describe the very sacrifice Mary and "
        "Joseph could afford for Jesus"),
    "leviticus13": (CLS,
        "the longest chapter in the book built entirely around "
        "diagnosis rather than cure, a priest rather than a physician "
        "deciding what counts as disease, a paradox in which a "
        "partial outbreak is unclean but a body covered head to foot "
        "is pronounced clean, quarantine periods measured in matched "
        "sets of seven days, and a sufferer sent outside the camp "
        "calling out his own uncleanness rather than being announced "
        "by anyone else"),
    "leviticus14": (CLS,
        "a two-bird ceremony in which one bird dies and the other is "
        "dipped in its blood before being released alive, a total "
        "shaving of every hair on the body marking the start of a new "
        "eighth day, blood applied to the same ear, thumb and toe "
        "once marked at a priest's own ordination, a poverty "
        "provision that still requires the guilt offering's blood "
        "even when everything else is scaled down, and legislation "
        "for leprosy in a house that only takes effect once Israel is "
        "already living in the land"),
    "leviticus15": (CLS,
        "four separate sources of bodily uncleanness gathered into "
        "one chapter, a chronic discharge that renders unclean "
        "anything the sufferer sits or lies upon, an ordinary "
        "seminal emission requiring nothing more than washing and a "
        "wait until evening, an unspecified length given to chronic "
        "bleeding that echoes, centuries later, in a woman who "
        "touches a hem in the Gospels, and a closing statement naming "
        "the reason for the whole chapter as one of life and death, "
        "that they die not in their uncleanness"),
    "leviticus16": (CLS,
        "a warning against entering freely into the most holy place "
        "placed immediately after the deaths of Nadab and Abihu, "
        "simple white linen worn instead of the usual golden garments "
        "for the one day the veil is actually crossed, two goats "
        "drawn by lot so that one dies and the other is sent alive "
        "into the wilderness, blood brought within the veil with no "
        "witnesses present for the one act on which the whole nation "
        "depends, and a perpetual statute fixed to a single day of "
        "the year that anticipates something done once for all"),
    "leviticus17": (CLS,
        "a law confining every slaughter to the Tabernacle so that no "
        "sacrifice is ever offered in an open field, blood forbidden "
        "to eat on the ground that it is life itself, given by God "
        "for the altar rather than for the table, the single verse "
        "tying every sacrifice in the book back to one principle, the "
        "life of the flesh is in the blood, an animal found dead or "
        "torn treated as unclean because its blood was never properly "
        "drained, and the same rule applied without distinction to "
        "native Israelite and resident stranger alike"),
    "leviticus18": (CLS,
        "a chapter framed by two nations Israel is told not to "
        "imitate, the Egypt just left and the Canaan about to be "
        "entered, a list of prohibited relationships built around the "
        "single phrase uncover their nakedness, child sacrifice to "
        "Molech placed in the middle of purely sexual prohibitions "
        "rather than set off on its own, a land personified as "
        "vomiting out its own inhabitants for these very practices, "
        "and a closing warning that the same fate awaits Israel if it "
        "repeats what the nations did"),
    "leviticus19": (CLS,
        "a single command, ye shall be holy for I the LORD your God "
        "am holy, spelled out across nearly every area of daily life, "
        "gleaning laws that leave the edges of every field for the "
        "poor and the stranger, four and five-word prohibitions on "
        "stealing, lying and false dealing packed one after another "
        "with no elaboration, a climactic command to love thy "
        "neighbour as thyself embedded in the middle of civil law "
        "rather than set apart, and honest weights and measures tied "
        "directly back to the memory of the Exodus"),
    "leviticus20": (CLS,
        "penalties assigned to the very acts chapter eighteen only "
        "prohibited, Molech worship carrying a death sentence that "
        "falls on the community too if it looks away, cursing a "
        "parent treated as capital while some of the incest laws "
        "instead carry childlessness or being cut off, a scale of "
        "consequence that grades offenses rather than leveling them, "
        "and a closing appeal to the same holiness formula that "
        "opened the Holiness Code three chapters earlier"),
    "leviticus21": (CLS,
        "a graduated scale of holiness rising from ordinary Israelite "
        "to priest to high priest, priests forbidden the mourning "
        "customs common to their culture, the high priest denied even "
        "those small exceptions for his own father or mother, "
        "marriage restrictions narrowing further the higher the "
        "office climbs, and a blemished priest permitted to eat the "
        "priestly food while still barred from the altar itself"),
    "leviticus22": (CLS,
        "uncleanness disqualifying a priest from holy food until "
        "evening rather than permanently, a household member's "
        "status, whether slave, guest or married-out daughter, "
        "determining who may eat what belongs to the priest alone, "
        "sacrificial animals held to the same standard of wholeness "
        "demanded of the priests who offer them, a mother and her "
        "young forbidden to be killed on the same day even within the "
        "sacrificial system, and a closing tie between God's holiness "
        "and the God who redeemed Israel from Egypt"),
    "leviticus23": (CLS,
        "seven appointed times named the LORD's rather than Israel's "
        "own, a long gap in the calendar between Pentecost and "
        "Trumpets left conspicuously unfilled, feasts falling into "
        "two clusters, spring and fall, that later readers line up "
        "against a first and second coming, a wave sheaf offered the "
        "very day after the Sabbath during Unleavened Bread, and "
        "worshippers commanded to dwell in booths for seven days as a "
        "standing memory of a wilderness no living Israelite had "
        "experienced"),
    "leviticus24": (CLS,
        "a lamp kept burning continually just outside the same veil "
        "the previous chapters described from the inside, twelve "
        "loaves of showbread replaced every Sabbath and eaten only by "
        "the priests, a blasphemer of mixed Israelite and Egyptian "
        "parentage held in custody until Moses can inquire of God "
        "directly, a law of exact retaliation, eye for eye and tooth "
        "for tooth, framed as a ceiling on vengeance rather than a "
        "license for it, and one law repeated for stranger and native "
        "alike in the very case where a stranger's parentage is what "
        "triggered it"),
    "leviticus25": (CLS,
        "a seventh year of complete rest for the land itself, not "
        "merely for the people working it, a fiftieth year in which "
        "liberty is proclaimed and every family returns to its "
        "original inheritance, a theological claim, the land is mine, "
        "underlying every regulation on buying, selling and redeeming "
        "it, a promise of a triple harvest in the sixth year "
        "answering the obvious question of what to eat in the "
        "seventh, and a law that treats an Israelite who sells "
        "himself into service not as property but as a hired worker "
        "awaiting release"),
    "leviticus26": (CLS,
        "two commands, no idols and keep my sabbaths, standing in for "
        "the whole of the law before any blessing or curse is named, "
        "blessings for obedience listed before five escalating cycles "
        "of discipline for continued refusal to listen, the phrase "
        "seven times more recurring at each new stage of judgment, "
        "horrors reserved for the final cycle that history records "
        "were literally fulfilled during later sieges of Jerusalem, "
        "and a promise of restoration that survives every curse, "
        "reaching back through Jacob, Isaac and Abraham to a covenant "
        "God will not finally abandon"),
    "leviticus27": (CLS,
        "a system of fixed valuations substituting money for a person "
        "no one could actually lay on an altar, an animal already fit "
        "for sacrifice forbidden from ever being exchanged once "
        "vowed, redemption of a house or field always costing a fifth "
        "more than the original valuation, a firstborn animal "
        "excluded from vows altogether because it already belonged to "
        "God before anyone thought to dedicate it, and a tithe "
        "measured by whatever animal passes tenth under the counting "
        "rod rather than by the owner's own selection"),
}


def main():
    check = "--check" in sys.argv
    for book, (cls, themes) in DATA.items():
        result = process(book, cls, themes, check)
        print(f"{book}: {result}")


if __name__ == "__main__":
    main()
