#!/usr/bin/env python3
"""Batch 14: 1 Kings 1-22, the whole book. See add_key_themes_batch1.py.

    python3 add_key_themes_batch14.py [--check]
"""
import sys

from add_key_themes_batch1 import process

CLS = "Historical Narrative"

DATA = {
    "1kings1": (CLS,
        "A power vacuum created by a king too old even to keep warm, "
        "Adonijah exalting himself the same way Absalom once did and "
        "inviting only allies who would not object, Nathan and "
        "Bathsheba timing two independent reports to force a decision "
        "before a coup becomes irreversible, Solomon anointed publicly "
        "at Gihon on David's own mule so the succession could not be "
        "disputed, and Adonijah's submission made conditional rather "
        "than unconditional, if he prove himself a worthy man"),
    "1kings2": (CLS,
        "A deathbed charge that pairs be strong and shew thyself a man "
        "with instructions for settling old scores, forty years of "
        "reign summarized in one transitional sentence, a request for "
        "Abishag read by Solomon as a claim on the kingdom itself, a "
        "priest exiled rather than executed because his sanctuary "
        "claim outweighs his complicity, and Joab denied the same "
        "altar-horn mercy Adonijah received because murder disqualifies "
        "sanctuary"),
    "1kings3": (CLS,
        "A foreign marriage alliance and a genuine love for the LORD "
        "held in the same breath without resolution, an open-ended "
        "offer answered with a request for a listening heart rather "
        "than knowledge or riches, wisdom granted alongside riches and "
        "honor that were never actually requested, two prostitutes and "
        "an impossible case used to prove the wisdom is real, and a "
        "verdict that never intends the child's death but depends on "
        "knowing what a mother would rather lose"),
    "1kings4": (CLS,
        "A sophisticated bureaucracy listed office by office including "
        "the man who will matter again in chapter twelve, twelve "
        "administrative districts drawn deliberately across rather "
        "than along the old tribal boundaries, provisions for a single "
        "day's court described in numbers that read as staggering, "
        "every man under his vine and his fig tree standing as the "
        "chapter's picture of peace, and wisdom measured against the "
        "sages of the east and the wisdom of Egypt and found to exceed "
        "both"),
    "1kings5": (CLS,
        "A Phoenician alliance initiated by Hiram before Solomon even "
        "asks for it, rest named as the precondition for building "
        "rather than an incidental blessing, a workforce of over one "
        "hundred eighty thousand men mobilized for a single national "
        "project, Adoniram named as the overseer who will be stoned "
        "when the same labor becomes a grievance, and cedar and stone "
        "quarried and cut before ever reaching the site so the temple "
        "rose without hammer or axe being heard there"),
    "1kings6": (CLS,
        "A date anchored to four hundred eighty years after the Exodus "
        "rather than left as an undated year of Solomon's reign, "
        "dimensions exactly double the tabernacle's signaling "
        "continuity rather than replacement, a conditional promise "
        "interrupting the construction narrative in its own middle, "
        "cherubim fifteen feet tall with wings meeting at the center "
        "of a room shaped as a perfect cube, and glory made entirely "
        "dependent on obedience rather than guaranteed by the building "
        "itself"),
    "1kings7": (CLS,
        "A palace complex that took thirteen years against the "
        "temple's seven, a second Hiram, a craftsman rather than a "
        "king, described in the same language once used of Bezalel, "
        "two named pillars proclaiming He establishes and In Him is "
        "strength rather than serving as structural supports, a bronze "
        "sea holding some twelve thousand gallons set on twelve oxen "
        "facing the four directions, and a final inventory whose "
        "weight the writer declines to record at all"),
    "1kings8": (CLS,
        "An ark carried into the Most Holy Place until a cloud fills "
        "the house and drives the priests out from ministering, a "
        "question that undercuts the whole building project before "
        "the prayer continues, will God indeed dwell on the earth, "
        "seven petitions offered for seven different kinds of national "
        "crisis, a prayer that even the desire to obey the LORD would "
        "have to be given by Him, and twenty-two thousand oxen and a "
        "hundred twenty thousand sheep offered across a fourteen-day "
        "dedication"),
    "1kings9": (CLS,
        "A second appearance to Solomon bookending twenty years of "
        "building the way the first appearance opened his reign, a "
        "promise and a warning delivered in the same conditional "
        "sentence, twenty cities in Galilee handed to Hiram and "
        "rejected as Cabul in an awkward diplomatic moment, a building "
        "program reaching Hazor, Megiddo and Gezer far beyond "
        "Jerusalem, and a fleet to Ophir returning with sixteen tons "
        "of gold from a location scholars still debate"),
    "1kings10": (CLS,
        "A queen who travels thousands of miles with hard questions "
        "and finds the half was not told her, wealth catalogued in "
        "numbers deliberately excessive, six hundred sixty-six talents "
        "of gold in a single year, silver counted so common it was "
        "nothing accounted of, horses imported from Egypt and sold on "
        "to Hittite and Syrian kings, and a violation of the law of "
        "the king recorded without a single word of explicit "
        "condemnation"),
    "1kings11": (CLS,
        "The same verb once used of Solomon loving the LORD now "
        "describing his love for many strange women, seven hundred "
        "wives and three hundred concubines each a small compromise "
        "accumulated over decades, judgment tempered by mercy for "
        "David's sake so the kingdom is rent but not in Solomon's own "
        "lifetime, adversaries raised up on two borders as God "
        "withdraws the rest he once granted, and a torn garment "
        "handing Jeroboam ten pieces while Solomon's response is to "
        "try to kill him"),
    "1kings12": (CLS,
        "A reasonable request for lighter labor answered with a crude "
        "boast about scorpions instead of whips, elders counseling "
        "service rejected for the counsel of peers who had grown up "
        "with the king, an old rebellion cry revived word for word, "
        "what portion have we in David, a prophet's this thing is from "
        "me obeyed by a king who otherwise rarely listens, and two "
        "golden calves declared in Aaron's exact words from Sinai, "
        "behold thy gods which brought thee up out of Egypt"),
    "1kings13": (CLS,
        "A king named three hundred years before his birth as the "
        "prophecy against Bethel's altar, a hand withered and restored "
        "in the same scene as the sign that confirms the word, an old "
        "prophet's lie stated plainly by the narrator before the man "
        "of God ever believes it, a lion that kills without eating the "
        "body or harming the donkey, proof the death is judgment "
        "rather than accident, and a king who witnesses every sign and "
        "still returns not from his evil way"),
    "1kings14": (CLS,
        "A disguise sent to a prophet who already knows she is coming "
        "before she arrives, heavy tidings delivered to a queen still "
        "standing at the door in her costume, a child's death timed to "
        "the exact moment her feet cross the threshold, Judah "
        "descending into the same abominations the Canaanites were "
        "displaced for practicing, and gold shields replaced with "
        "bronze after Shishak's invasion, kept up with the same "
        "ceremony but none of the substance"),
    "1kings15": (CLS,
        "A lamp preserved in Jerusalem for David's sake regardless of "
        "which king currently holds the throne, Asa's own grandmother "
        "deposed from the queen mother's position for making an idol, "
        "silver and gold taken from the temple treasury to bribe Syria "
        "rather than trusted to the LORD, a prophecy against Jeroboam's "
        "house fulfilled to the letter by a king who then adopts the "
        "very sin he was used to punish, and reigns evaluated one "
        "after another against a single standard, as did David his "
        "father"),
    "1kings16": (CLS,
        "A prophecy against Baasha delivered in language almost "
        "identical to the one once spoken against Jeroboam, a king "
        "found drinking himself drunk while his own army is in the "
        "field, a seven-day reign ending in a burned palace and a name "
        "that becomes proverbial for treachery, Ahab's evaluation "
        "topping every king before him by treating Jeroboam's sin as "
        "too light on its own, and Jericho rebuilt at the cost of two "
        "sons exactly as Joshua cursed it three centuries earlier"),
    "1kings17": (CLS,
        "A prophet erupting onto the scene with no genealogy and no "
        "introduction before pronouncing a drought by his own word, "
        "ravens, unclean birds by the law's own definition, commanded "
        "to feed him morning and evening, God's provision found in "
        "enemy territory through a Gentile widow rather than among "
        "Israel's own, a jar of meal that does not waste and a jug of "
        "oil that does not fail for as long as the promise holds, and "
        "the first recorded resurrection in scripture answering a "
        "mother's accusation that the prophet's presence brought her "
        "sin to remembrance"),
    "1kings18": (CLS,
        "A famine so severe the king himself searches for grass to "
        "keep his horses alive, a governor who hid a hundred prophets "
        "at personal risk introduced alongside the one prophet everyone "
        "is hunting, a question that names Israel's condition exactly, "
        "how long halt ye between two opinions, mockery aimed at "
        "exposing a god who might be asleep or on a journey rather "
        "than merely taunting his prophets, and twelve barrels of "
        "water poured out in a drought before any fire falls at all"),
    "1kings19": (CLS,
        "A prophet who called fire from heaven fleeing in terror from "
        "a single messenger's threat, an angel's answer to despair "
        "given as food and sleep rather than rebuke, forty days and "
        "nights of strength drawn from one meal echoing Moses at the "
        "same mountain, wind, earthquake and fire all passing before "
        "the LORD is found in a still small voice instead, and seven "
        "thousand faithful revealed to a man convinced he alone was "
        "left"),
    "1kings20": (CLS,
        "Total submission demanded and then a second demand for "
        "anything pleasant in the king's own eyes going further "
        "still, victory granted through two hundred thirty-two young "
        "servants against a massive coalition so Ahab would know that "
        "I am the LORD, Syrian advisors reducing God to a deity of the "
        "hills and God answering to vindicate His sovereignty over the "
        "valleys too, a condemned enemy called brother and elevated "
        "into Ahab's own chariot, and a self-disguised prophet's "
        "parable that gets Ahab to pronounce his own verdict before he "
        "realizes it"),
    "1kings21": (CLS,
        "A refusal grounded in covenant law rather than stubbornness "
        "or bargaining, a king who sulks in bed over land he cannot "
        "legally buy, a plot built on a false fast and two witnesses "
        "accusing an innocent man of cursing God and the king, arise "
        "take possession given without any explanation of how Naboth "
        "died and none asked for, and a harsh verdict followed "
        "immediately by a real reprieve granted to a repentance nobody "
        "expected"),
    "1kings22": (CLS,
        "Four hundred prophets unanimous in one voice against "
        "Micaiah's single dissent, a coaching note asking Micaiah to "
        "agree before he is even questioned, a vision of a lying "
        "spirit sent to persuade Ahab's prophets, offered as the "
        "reason four hundred voices could all be wrong together, a "
        "disguise that reveals more fear than the king was willing to "
        "admit, and a random arrow finding the one joint in his armor "
        "that no disguise could protect"),
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
