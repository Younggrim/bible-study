#!/usr/bin/env python3
"""Batch 15: 2 Kings 1-25, the whole book. See add_key_themes_batch1.py.

    python3 add_key_themes_batch15.py [--check]
"""
import sys

from add_key_themes_batch1 import process

CLS = "Historical Narrative"

DATA = {
    "2kings1": (CLS,
        "A king injured by a fall who sends to a Philistine god before "
        "he ever thinks to ask Israel's own, is it not because there "
        "is not a God in Israel repeated as the question that damns "
        "the inquiry, fire falling twice on captains who command "
        "rather than request, a third captain's plea on his knees "
        "answered differently than arrogance was, and a sentence "
        "delivered to the king's face unchanged from the one sent "
        "through messengers"),
    "2kings2": (CLS,
        "A journey retracing Israel's conquest route in reverse as "
        "though Elijah is walking backward through its history, three "
        "refusals to be left behind answered each time with as the "
        "LORD liveth and as thy soul liveth, a double portion "
        "requested as a firstborn's inheritance rather than as raw "
        "power, a mantle picked up and a question, where is the LORD "
        "God of Elijah, that is invocation rather than doubt, and "
        "water healed with salt from a new bowl standing permanently "
        "unto this day"),
    "2kings3": (CLS,
        "A qualified evaluation, evil, but not like his father and his "
        "mother, describing partial reform that removes excess while "
        "keeping the system, an alliance with Judah echoing the same "
        "yoking Jehoshaphat once made with Ahab, a musician's music "
        "calming the prophet's spirit before any word comes, water "
        "arriving by the way of Edom at the exact hour of the morning "
        "sacrifice, and a king's desperate sacrifice of his own heir "
        "met by an indignation the text never fully explains"),
    "2kings4": (CLS,
        "Two questions, what shall I do for thee and what hast thou in "
        "the house, beginning a miracle with what a widow already owns "
        "rather than what she lacks, a Shunammite woman's hospitality "
        "sustained rather than sporadic, earning a promise she "
        "initially refuses to trust, a boy's death met with as the "
        "LORD liveth, I will not leave thee, the same vow Elisha once "
        "made to Elijah, poison neutralized by meal cast into a pot "
        "that has no natural power to counteract it, and a hundred fed "
        "from twenty loaves with food left over, foreshadowing a "
        "feeding still centuries away"),
    "2kings5": (CLS,
        "A commander introduced with every credential and then one "
        "devastating qualifier, but he was a leper, a captive slave "
        "girl possessing the one thing her master's whole army lacks, "
        "an instruction so simple it insults a man ready to attempt "
        "something difficult instead, seven dips in a muddy river "
        "restoring flesh like a little child's rather than only "
        "improving it, and Gehazi's greed transferring Naaman's "
        "leprosy onto himself and his descendants forever"),
    "2kings6": (CLS,
        "A borrowed axe head recovered because a poor man's integrity "
        "mattered enough for a miracle, a servant's panic at Dothan "
        "answered with eyes opened to horses and chariots of fire "
        "already surrounding the city, more that be with us than that "
        "be with them stated before the servant can even see it, a "
        "famine so severe a donkey's head sells for silver and mothers "
        "eat their own children, and a king's sackcloth revealed under "
        "his royal robes the moment the horror finally reaches him"),
    "2kings7": (CLS,
        "A prophecy of overnight abundance answered with an officer's "
        "cynicism even if the LORD made windows in heaven, four lepers "
        "reasoning their way into the enemy camp because staying "
        "anywhere else guarantees death, an empty Syrian camp "
        "abandoned because God made an army of noise no one actually "
        "needed to fight, the exact prices Elisha named fulfilled to "
        "the shekel within a day, and the doubting officer trampled to "
        "death at the very gate where the abundance he refused to "
        "believe pours through"),
    "2kings8": (CLS,
        "A land restored at the precise moment a king happens to be "
        "asking about the miracle that would prove the claim, Elisha "
        "weeping over Hazael before Hazael has done any of the things "
        "being wept over, a paradoxical answer, he will recover and he "
        "will surely die, describing illness and murder in the same "
        "breath, Judah's kings corrupted through marriage into Ahab's "
        "house rather than through their own choices, and a light "
        "preserved for David's sake even while a Davidic king walks in "
        "the way of the house of Ahab"),
    "2kings9": (CLS,
        "An anointing carried out in secret and fled from immediately "
        "because it amounts to treason against a reigning king, a "
        "watchman's identification made from nothing but the way a "
        "chariot is driven, what peace answered with a question that "
        "names the sin rather than the greeting offered, a body thrown "
        "deliberately onto the very field it was stolen by murder to "
        "obtain, and a queen who paints her face and adorns her head "
        "to die in defiance rather than in fear"),
    "2kings10": (CLS,
        "A challenge to choose a champion from seventy sons that Jehu "
        "already knows will never be answered, two heaps of heads "
        "displayed at the gate as evidence turned into indictment, "
        "forty-two relatives killed simply for traveling toward a "
        "court that no longer exists, a solemn assembly for Baal "
        "announced as devotion and used as a trap, and zeal that "
        "destroys an idol's temple while leaving Jeroboam's golden "
        "calves standing, judged incomplete for exactly that reason"),
    "2kings11": (CLS,
        "A grandmother destroying her own grandchildren's lives to "
        "seize a throne that was never legally hers, one infant hidden "
        "in the temple for six years while the Davidic line hangs by a "
        "single thread, David's own spears and shields brought out of "
        "storage for a coup carried out on the Sabbath, treason cried "
        "out by the one person in the room actually guilty of it, and "
        "a three-way covenant renewed between God, king and people "
        "before the temple of Baal is torn down"),
    "2kings12": (CLS,
        "Righteousness explicitly qualified as lasting only as long as "
        "Jehoiada the priest instructed him, twenty-three years "
        "passing with temple repair money collected but no repairs "
        "made, a chest with a hole in its lid replacing an accounting "
        "system that had failed for decades, temple treasures stripped "
        "to buy off Hazael by the very king who once restored them, "
        "and an assassination motivated, per the fuller account, by "
        "the blood of the priest's own son"),
    "2kings13": (CLS,
        "An army reduced to fifty horsemen and ten chariots yet not "
        "abandoned because of a covenant made centuries earlier with "
        "Abraham, Isaac and Jacob, the chariot of Israel and the "
        "horsemen thereof spoken twice, once at Elijah's departure and "
        "once at Elisha's, an arrow shot eastward named the arrow of "
        "the LORD's deliverance before any battle is fought, a king's "
        "three strikes on the ground rebuked for stopping short of "
        "five or six, and victory measured out exactly as limited as "
        "the king's own half-hearted obedience"),
    "2kings14": (CLS,
        "Justice executed on assassins while their children are "
        "deliberately spared in explicit obedience to the law of "
        "individual responsibility, a challenge to war answered with a "
        "parable about a thistle that asked for a cedar's daughter, "
        "success in Edom souring into the arrogance that provokes "
        "Amaziah's own downfall, a conspiracy that catches him in "
        "Lachish after fifteen surviving years never restore his "
        "standing, and Israel's greatest territorial expansion since "
        "Solomon arriving under a king the text still calls evil"),
    "2kings15": (CLS,
        "A long and mostly faithful reign remembered chiefly for a "
        "leprosy contracted the moment a king tried to burn incense "
        "that belonged only to the priests, four generations promised "
        "to Jehu's dynasty fulfilled exactly and no further, five "
        "kings in rapid succession and four of five transitions "
        "accomplished by assassination, a brutality that rips open "
        "pregnant women in a city that only refused to open its gates, "
        "and storm clouds already gathering over Jotham's otherwise "
        "stable and faithful Judah"),
    "2kings16": (CLS,
        "An evaluation refusing Ahaz even the qualified praise weaker "
        "kings received, his own son made to pass through the fire in "
        "the exact abomination that drove out the Canaanites, an altar "
        "copied from Damascus and installed while the LORD's own altar "
        "is quietly moved aside, temple fittings dismantled piece by "
        "piece to pay Assyrian tribute, and a priest who complies with "
        "every instruction rather than resisting a single one"),
    "2kings17": (CLS,
        "A last king's slight improvement over his predecessors still "
        "not enough to avert judgment, more space given to explaining "
        "why Samaria fell than to describing how, an indictment "
        "unfolding systematically through pillars, Asherah poles and "
        "rejected prophets, foreign settlers sent lions until an "
        "exiled priest is returned to teach them the manner of the God "
        "of the land, and a verdict on the result, they feared the "
        "LORD and served their own gods, that names syncretism rather "
        "than conversion"),
    "2kings18": (CLS,
        "A king praised above every king before or after him for "
        "trusting the LORD, a bronze serpent Moses himself had made "
        "destroyed because it had become an idol under its own name, "
        "tribute paid first and temple doors stripped of their gold "
        "before the real crisis even begins, a rabshakeh's speech "
        "built to attack the reform itself as the reason Assyria is "
        "winning, and officers asking for Aramaic so a threat aimed at "
        "breaking morale would not be understood by the people on the "
        "wall"),
    "2kings19": (CLS,
        "A message sent to Isaiah phrased as labor that cannot be "
        "completed rather than as a request for rescue, a letter "
        "spread out before the LORD rather than merely read, a prayer "
        "that concedes the enemy's own evidence instead of disputing "
        "it, Jerusalem personified as a virgin daughter mocking the "
        "very army besieging her, and a hundred eighty-five thousand "
        "dead in one night without a single Judean sword lifted"),
    "2kings20": (CLS,
        "A death sentence reversed before the prophet who delivered it "
        "has even left the middle court, weeping turned toward the "
        "wall answered with fifteen added years and a shadow moved "
        "backward as the sign, envoys shown every treasure in the "
        "house for no better reason than that they had heard the king "
        "was sick, two procedural questions turning hospitality into "
        "the sentence that would exile his own descendants, and "
        "Babylon named as the danger years before Assyria's threat is "
        "even resolved"),
    "2kings21": (CLS,
        "A fifty-five year reign, the longest of any king of Judah, "
        "judged the most wicked precisely because of what it undid, an "
        "Asherah image placed inside the very temple built to house "
        "the name of the LORD, judgment pronounced as irreversible, "
        "the line of Samaria and the plummet of Ahab's house applied "
        "to Jerusalem itself, a dish wiped and turned upside down as "
        "the image for total destruction, and a son who inherits the "
        "idolatry of Manasseh's reign without any hint of his father's "
        "late repentance"),
    "2kings22": (CLS,
        "A verdict with no qualification attached at all, turned not "
        "aside to the right hand or to the left, accounts left "
        "unaudited because the workmen dealt faithfully without "
        "needing to be checked, a book of the law found by accident in "
        "the middle of ordinary temple repairs, Huldah consulted "
        "rather than Jeremiah or another prophet already active in the "
        "city, and judgment confirmed as unalterable for the nation "
        "while mercy is granted personally because a king's heart was "
        "tender"),
    "2kings23": (CLS,
        "An entire book of the covenant read aloud to elders, priests, "
        "prophets and people together before a single reform begins, "
        "cleansing that starts inside the temple itself before it ever "
        "reaches the countryside, a three-hundred-fifty-year-old "
        "shrine built for Solomon's foreign wives finally torn down, a "
        "prophecy from three centuries earlier fulfilled exactly when "
        "bones are burned on Bethel's altar, and one unnamed prophet's "
        "tomb deliberately left undisturbed in the middle of an "
        "otherwise total purge"),
    "2kings24": (CLS,
        "Rebellion against Babylon after three years of vassalage "
        "triggering raiders sent by the commandment of the LORD rather "
        "than mere political consequence, judgment traced explicitly "
        "back to Manasseh's innocent blood which the LORD would not "
        "pardon, an eighteen-year-old king surrendering along with his "
        "mother and officers rather than resisting, golden vessels "
        "Solomon made cut in pieces in the exact fulfillment of a much "
        "earlier prophecy, and ten thousand deportees leaving behind "
        "only the poorest people in the land"),
    "2kings25": (CLS,
        "An eighteen-month siege ending in a breach and a king's "
        "flight by night through a garden gate, sons killed in front "
        "of Zedekiah as the last thing his own eyes ever see before "
        "they are put out, temple bronze and gold catalogued item by "
        "item in a grief that is almost liturgical in its detail, "
        "leaders executed at Riblah while the poorest of the land are "
        "left to tend the vineyards and fields, and the book's very "
        "last notice, a captive king raised up out of prison and given "
        "a seat above every other captive king in Babylon"),
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
