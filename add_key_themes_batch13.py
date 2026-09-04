#!/usr/bin/env python3
"""Batch 13: Judges 1-21, the whole book. See add_key_themes_batch1.py.

    python3 add_key_themes_batch13.py [--check]
"""
import sys

from add_key_themes_batch1 import process

CLS = "Historical Narrative"

DATA = {
    "judges1": (CLS,
        "A prologue explaining the whole book's later cycles by one "
        "repeated verb, did not drive out, Adoni-bezek recognizing "
        "divine justice in his own mutilation, a spy shown mercy the "
        "way Rahab once was but building a pagan city instead of "
        "joining Israel, Asher's reversal recorded in one devastating "
        "clause, the Asherites dwelt among the Canaanites, and a "
        "catalogue of tribal failures that closes the chapter rather "
        "than opens it"),
    "judges2": (CLS,
        "An angel's rebuke delivered at a place later named for the "
        "weeping it caused, a covenant renewed at Gilgal answered by "
        "disobedience rather than gratitude, a generation that knew "
        "not the LORD rising the moment eyewitnesses to His works had "
        "died, a cycle of sin, oppression, crying out, deliverance and "
        "rest introduced as the book's whole shape, and each turn of "
        "the cycle spiraling downward rather than circling back to "
        "where it started"),
    "judges3": (CLS,
        "Nations left deliberately to teach war to a generation that "
        "had never fought one, Othniel's story told as the cycle in "
        "its purest and briefest form, a left-handed weakness turned "
        "into Ehud's actual weapon, a very fat king and a hidden dagger "
        "described in more physical detail than any other assassination "
        "in the book, and Shamgar's entire deliverance told in a single "
        "verse with an ox goad for a weapon"),
    "judges4": (CLS,
        "Deborah alone among the judges shown actually adjudicating "
        "disputes under her palm tree, Barak's condition for going "
        "answered with a prophecy that costs him the honor of the "
        "victory, discomfited used of Sisera's army the same way it is "
        "used of a rout only God can cause, an alliance of convenience "
        "between Jabin and Heber's house that puts Sisera in exactly "
        "the wrong tent, and a tent peg finishing what nine hundred "
        "iron chariots could not prevent"),
    "judges5": (CLS,
        "A victory hymn possibly composed within hours of the battle "
        "it celebrates, the same God who marched from Sinai marshaled "
        "again against Sisera, three classes of listener called to "
        "speak in turn, the wealthy, the magistrates and the ordinary "
        "traveler, tribes praised for fighting and tribes named for "
        "staying home named in the same roll call, Meroz cursed for the "
        "single fact of not turning up, and Sisera's mother imagining "
        "spoils while her son already lies dead at a woman's feet"),
    "judges6": (CLS,
        "A prophet sent to name the sin before any deliverer is sent "
        "to address the suffering, a mighty man of valour found "
        "threshing wheat in a winepress to hide it from raiders, an "
        "objection about being least in the poorest family in the "
        "smallest clan met without correction, a father's own logic "
        "defending a son who tore down his altar, if he be a god let "
        "him plead for himself, and a fleece tested twice though God "
        "had already promised what the first test asked"),
    "judges7": (CLS,
        "An army called too many rather than too few before a single "
        "battle is fought, two rounds of reduction that leave three "
        "hundred out of thirty-two thousand, a barley-cake dream "
        "overheard in the enemy's own camp before Gideon ever gives an "
        "order, an attack carried out with trumpets, empty jars and "
        "torches instead of a single drawn sword, and Midianites "
        "destroying each other in the dark while Israel's three hundred "
        "simply stand and shout"),
    "judges8": (CLS,
        "A diplomatic answer that calls Ephraim's gleanings greater "
        "than Gideon's own vintage, faint yet pursuing describing an "
        "army too exhausted to stop, two Israelite towns punished with "
        "thorns and a broken tower for refusing bread to their own "
        "deliverer, kingship refused in a sentence that gets the "
        "theology exactly right, the LORD shall rule over you, and a "
        "gold ephod built from good intentions that becomes a snare "
        "for Gideon's whole house"),
    "judges9": (CLS,
        "Seventy brothers murdered on one stone to clear a path to a "
        "crown none of them held, the oldest fable in the book handed "
        "to trees that each refuse a throne before a bramble accepts "
        "it, an evil spirit sent by God between conspirators as their "
        "punishment rather than as a mystery, a millstone dropped by a "
        "woman ending a reign built entirely on that one murder, and a "
        "dying request to be finished off by his own armor-bearer so "
        "history could not say a woman killed him"),
    "judges10": (CLS,
        "Two minor judges given forty-five years of unremarked "
        "stability between two chapters of chaos, an idolatry "
        "catalogue naming seven nations' gods as the most "
        "comprehensive in the book, God answering confession by naming "
        "seven past deliverances that match the seven gods just named, "
        "a command to go and cry unto the gods you have chosen "
        "functioning as discipline rather than final rejection, and a "
        "search for a leader left open at the chapter's end for "
        "Jephthah to answer"),
    "judges11": (CLS,
        "An outcast son of a prostitute recalled by the same brothers "
        "who expelled him, diplomatic negotiation with Ammon built on "
        "a careful reading of Israel's own three hundred years of "
        "history, a rash vow made after the Spirit had already come "
        "upon him, not to secure victory but as though it still needed "
        "to be bargained for, a daughter's request for two months "
        "before a vow is fulfilled rather than a request to be spared, "
        "and a debate that has run for centuries over whether that "
        "fulfillment was death or lifelong dedication"),
    "judges12": (CLS,
        "A grievance and a threat delivered in the same breath by a "
        "tribe that arrives only after the fighting is over, force "
        "chosen over the diplomacy Gideon once used for the identical "
        "complaint, a pronunciation Ephraim's dialect could not "
        "produce turned into a password and then a death sentence, "
        "forty-two thousand killed by Israelites over the sound of one "
        "letter, and Jephthah's own six-year tenure ending without the "
        "land had rest formula every judge before him received"),
    "judges13": (CLS,
        "Forty years of oppression recorded with no mention of Israel "
        "crying out at all, an angel's announcement given to an "
        "unnamed woman before her husband ever hears it, Nazirite "
        "restrictions placed on a mother's own diet before her son is "
        "even born, a name refused as secret and wonderful rather than "
        "given, and a wife's faith answering her husband's fear of "
        "having seen God, if the LORD were pleased to kill us he would "
        "not have shown us all these things"),
    "judges14": (CLS,
        "A demand for a Philistine wife justified only afterward as "
        "something of the LORD working an occasion against them, a "
        "lion torn apart bare-handed and its carcass later robbed of "
        "honey in a first, casual violation of a vow Samson never "
        "seems to notice breaking, a riddle wagered on thirty garments "
        "and lost to seven days of a wife's weeping, and vengeance "
        "carried out in a city twenty miles away by a Spirit that "
        "comes and goes without changing the man it empowers"),
    "judges15": (CLS,
        "Three hundred foxes and torches turned into an act of "
        "agricultural warfare, escalating retaliation that burns a "
        "wife for the very threat once made against her, three "
        "thousand men of Judah arriving not to fight the Philistines "
        "but to hand their own deliverer over, a fresh jawbone found "
        "and used before it could dry and crack, and a first recorded "
        "prayer, for water rather than for strength, placed right "
        "before the only time the chapter calls him a judge"),
    "judges16": (CLS,
        "City gates torn out and carried thirty-eight miles as proof "
        "his strength survives his own moral failure, three lies told "
        "to a woman clearly trying to betray him before a fourth "
        "answer finally does, a sentence naming its own tragedy, he "
        "wist not that the LORD was departed from him, hair beginning "
        "to grow again as the only sign anything is being restored, "
        "and a final prayer asking only this once before pillars come "
        "down on captors and captive together"),
    "judges17": (CLS,
        "Stolen silver confessed, cursed and blessed in the same "
        "breath before it is melted into an idol dedicated to the "
        "LORD, a private shrine violating nearly every law it touches "
        "while its owner believes it pleases God, the book's own "
        "thesis stated for the first time, no king in Israel, every "
        "man did that which was right in his own eyes, a wandering "
        "Levite hired for ten shekels a year, clothing and food, and "
        "Micah's mistaken confidence that a Levite legitimizes an "
        "illegitimate system"),
    "judges18": (CLS,
        "Spies sent to find easier prey after Dan failed to conquer "
        "the land it was actually allotted, a peaceful, unsuspecting "
        "people scouted and reported good because they had no ally "
        "near enough to help them, a theft carried out brazenly while "
        "six hundred armed men wait at the gate, my gods which I made "
        "turning Micah's own words into the chapter's verdict on "
        "idolatry, and a city burned and renamed Dan by a tribe that "
        "could not hold its true inheritance"),
    "judges19": (CLS,
        "A refrain, there was no king in Israel, opening a chapter "
        "deliberately built to echo Sodom, four days of hospitality "
        "that delay a departure into exactly the danger it was "
        "avoiding, an old man's warning that reveals he already knows "
        "what Gibeah is, a demand at the door identical to Sodom's "
        "answered by offering women in place of the men, and a body "
        "divided into twelve pieces to summon a nation that had shown "
        "her no help while she was alive"),
    "judges20": (CLS,
        "Four hundred thousand men assembled against one tribe rather "
        "than against a foreign oppressor, a Levite's account that "
        "emphasizes the threat to himself over the crime against her, "
        "a lawful demand for the guilty refused by the whole tribe "
        "protecting them, two defeats costing forty thousand men "
        "before Israel ever asks whether it should stop rather than "
        "only whether it should go up, and a third day's ambush that "
        "only comes once Israel's posture has actually changed"),
    "judges21": (CLS,
        "A rash oath at Mizpah discovered to threaten an entire tribe "
        "with extinction, grief expressed with no apparent awareness "
        "that Israel's own violence caused it, a second oath activated "
        "to justify slaughtering Jabesh-gilead for the sake of finding "
        "brides, an abduction planned at a legitimate feast with an "
        "excuse already prepared for the fathers who will object, and "
        "the book's closing verdict repeated from its introduction to "
        "the appendix, no king in Israel, every man did that which was "
        "right in his own eyes"),
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
