#!/usr/bin/env python3
"""Batch 17: 2 Samuel 1-24, the whole book. See add_key_themes_batch1.py.

    python3 add_key_themes_batch17.py [--check]
"""
import sys

from add_key_themes_batch1 import process

CLS = "Historical Narrative"

DATA = {
    "2samuel1": (CLS,
        "An Amalekite's claim to have killed Saul contradicting the "
        "account already given in the previous book, David unable to "
        "fathom how anyone could stretch out a hand against the LORD's "
        "anointed, mourning that covers Saul, Jonathan, the people of "
        "the LORD and the house of Israel rather than only a personal "
        "loss, a formal lament commanded to be taught to Judah and "
        "preserved in a now-lost book, and how are the mighty fallen "
        "repeated three times as the refrain that structures the whole "
        "song"),
    "2samuel2": (CLS,
        "A kingship begun by inquiry, shall I go up, rather than by "
        "seizure, a rival throne set up at Mahanaim for a puppet king "
        "who lasts two years against David's seven and a half, twelve "
        "champions from each side dying together in a combat meant to "
        "settle nothing and settling nothing, Abner's warnings to "
        "Asahel ignored until a spear butt ends a pursuit that never "
        "needed to happen, and a ceasefire called on the appeal that "
        "Israelites are killing their own brothers"),
    "2samuel3": (CLS,
        "A list of sons at Hebron that reads as a genealogy and a "
        "foreshadowing of every tragedy still to come, Abner's rage "
        "revealing he has always known God's sworn purpose to set "
        "David's throne over all Israel, a defection born of anger "
        "rather than conviction the moment Abner is accused over a "
        "concubine, a murder committed inside a city of refuge by a man "
        "avenging his brother while pretending peace, and David cursing "
        "Joab's own house even while publicly following the bier he "
        "could not have prevented"),
    "2samuel4": (CLS,
        "Hands growing feeble the moment the one man propping up a "
        "puppet kingdom is gone, two captains sneaking in during the "
        "heat of the day pretending to fetch wheat before murdering a "
        "king in his own bed, God's name invoked to frame an "
        "assassination as justice rather than crime, David tracing the "
        "same precedent from the Amalekite of chapter one to condemn "
        "men who thought murder would earn them a reward, and an "
        "innocent man called righteous not for his character but for "
        "having done nothing to deserve his death"),
    "2samuel5": (CLS,
        "A threefold argument, kinship, proven leadership, divine "
        "appointment, made before David is anointed a third time over "
        "the whole nation, a taunt about the blind and the lame "
        "answered by a water shaft climbed to take a supposedly "
        "impregnable city, a name, Zion, replacing Jebus as David makes "
        "the city his own capital rather than any existing tribal "
        "territory, Hiram of Tyre's building materials read as "
        "international recognition rather than mere trade, and a battle "
        "plan changed the second time the Philistines attack in the "
        "same valley"),
    "2samuel6": (CLS,
        "A new cart chosen instead of the poles and Levite shoulders God "
        "had actually commanded, Uzzah struck dead for steadying what "
        "he was never meant to touch, three months of anger and fear "
        "before David tries again, this time correctly, dancing before "
        "the LORD with all his might stripped of royal robes rather "
        "than performed for an audience, and Michal's contempt answered "
        "with it was before the LORD, which chose me before thy father"),
    "2samuel7": (CLS,
        "A king at rest noticing the contrast between his own cedar "
        "house and the curtains the ark still dwells within, Nathan's "
        "initial approval overturned that same night by a message he "
        "never expected to carry, a wordplay on house running through "
        "the whole chapter, David wanting to build God one and God "
        "promising to build David one instead, an unconditional promise "
        "of a throne established forever regardless of what any "
        "individual descendant does, and a prayer that opens with who "
        "am I and closes asking God to do as he has said"),
    "2samuel8": (CLS,
        "A refrain repeated twice, the LORD preserved David whithersoever "
        "he went, framing every conquest in the chapter, Moab's "
        "prisoners measured by a line with two-thirds executed for "
        "reasons the text never fully explains, chariot horses "
        "hamstrung rather than multiplied in deliberate restraint of "
        "Deuteronomy's warning, wealth from Toi of Hamath and every "
        "other conquered nation dedicated to the LORD rather than kept, "
        "and an administration list closing a chapter of victories with "
        "the ordinary business of government"),
    "2samuel9": (CLS,
        "A question no ancient king asked, is there yet any left of the "
        "house of Saul that I may shew him kindness, David seeking "
        "survivors to bless rather than to eliminate, Mephibosheth "
        "falling on his face expecting execution and receiving fear not "
        "instead, land restored and a permanent seat at the king's "
        "table granted on the basis of a covenant rather than merit, "
        "and a closing sentence that names his disability and his "
        "privilege in the same breath, lame on both his feet, eating "
        "continually at the king's table"),
    "2samuel10": (CLS,
        "Ambassadors sent in genuine kindness reinterpreted by advisors "
        "as spies sent to search out the city, beards shaved and "
        "garments cut at the hips as a humiliation calculated to "
        "provoke war rather than merely insult, Joab facing enemies in "
        "front and behind and dividing his best troops toward the "
        "greater threat, a speech to Abishai pairing mutual support "
        "with a trust that leaves the outcome to the LORD, and a Syrian "
        "empire's full reinforcement still ending in defeat that leaves "
        "Ammon isolated for the siege still to come"),
    "2samuel11": (CLS,
        "A king tarrying at home in the season when kings go forth to "
        "battle, the seeds of the whole chapter's disaster planted in "
        "that one detail, a woman's purification noted specifically so "
        "no reader could later doubt whose child she carried, Uriah's "
        "loyalty to the ark and to Israel in the field standing as an "
        "unintended rebuke to the king who summoned him home, a letter "
        "carried by the victim's own hand ordering the position that "
        "would kill him, and a closing verdict, the thing that David "
        "had done displeased the LORD, delivered after everyone else "
        "has been fooled"),
    "2samuel12": (CLS,
        "A parable about a stolen lamb crafted precisely enough to draw "
        "David into pronouncing his own sentence, thou art the man "
        "landing after an indictment that begins by listing gifts "
        "rather than accusations, a confession reduced to five words, I "
        "have sinned against the LORD, with no qualification attached, "
        "a child's death met first with fasting and then, once he is "
        "gone, with worship and food because fasting could no longer "
        "change anything, and a second son given a second name, "
        "Jedidiah, beloved of the LORD, out of the very sin that nearly "
        "destroyed everything"),
    "2samuel13": (CLS,
        "A craftiness that turns a father's love into the very "
        "mechanism that delivers a daughter into a trap, Tamar arguing "
        "on every ground, moral, personal, practical, before being "
        "overpowered anyway, love that turns to hatred greater than the "
        "love itself the instant the sin is finished, a father's anger "
        "that produces no action because his own guilt over Bathsheba "
        "leaves him unable to judge the same sin in his son, and a "
        "murder planned for two years and carried out at a feast, "
        "echoing the way David's own crime was concealed at a "
        "celebration"),
    "2samuel14": (CLS,
        "A king's heart torn between longing for an exiled son and an "
        "inability to act without appearing to excuse murder, a wise "
        "woman's fictional case built to mirror David's own situation "
        "closely enough that he cannot see the trap until it closes, "
        "restoration granted halfway, let him not see my face, "
        "proximity without any actual relationship, Absalom's beauty "
        "and his hair's weight described in loving detail before his "
        "frustration turns to arson, and a barley field set on fire "
        "simply to force a conversation Joab kept refusing to have"),
    "2samuel15": (CLS,
        "A conspiracy that begins with chariots and runners and a seat "
        "at the city gate rather than with any act of violence, every "
        "petitioner's complaint validated and every fault laid at the "
        "king's door before Absalom ever asks to be made judge, a "
        "religious vow used as the pretext to reach Hebron, the very "
        "city of David's own first anointing, an ark sent back into the "
        "city rather than carried along as a talisman, if I find favour "
        "he will bring me again, and a king climbing the Mount of "
        "Olives weeping, barefoot and covered, in a scene later echoed "
        "by a greater Son of David"),
    "2samuel16": (CLS,
        "Provisions offered by Ziba wrapped around a devastating and "
        "unverified accusation against his own master, Shimei's cursing "
        "built on a theology that is wrong about David's guilt yet not "
        "entirely wrong about divine discipline, a king who tells his "
        "men to leave the cursing alone because the LORD hath bidden "
        "him, Hushai's greeting to Absalom deliberately ambiguous about "
        "which king he means, and Ahithophel's counsel treated as "
        "though a man had enquired at the oracle of God before it is "
        "set aside for another"),
    "2samuel17": (CLS,
        "Two counselors offering competing strategies, one militarily "
        "sound and one only flattering, with Absalom choosing the worse "
        "of the two, a narrator's own verdict stated outright, the LORD "
        "had appointed to defeat the good counsel of Ahithophel, a "
        "message relayed through a servant girl and hidden down a well "
        "covered over with scattered grain, a counselor's suicide "
        "calculated the moment his advice is rejected rather than born "
        "of any sudden despair, and three loyal men bringing beds and "
        "food to a king in the wilderness because the people is hungry, "
        "weary and thirsty"),
    "2samuel18": (CLS,
        "A public order given in front of the whole army, deal gently "
        "for my sake with the young man, even with Absalom, a forest "
        "that kills more men than the sword through its own terrain, "
        "hair or branches catching a rider left hanging between the "
        "heaven and the earth, a monument built by a man with no son to "
        "keep his name alive now standing empty over an unmarked pit of "
        "stones, and a father's lament repeating my son five times, "
        "answering a battle his own side had just won"),
    "2samuel19": (CLS,
        "An army ashamed of its own victory because the king's public "
        "grief outweighs any celebration, Judah won back by an offer of "
        "command that creates the deadly rivalry the next chapter will "
        "resolve by murder, a curse-giver spared on a day of "
        "restoration rather than vengeance though a different "
        "instruction waits on David's deathbed, land divided between "
        "master and servant in a judgment that reads as either wisdom "
        "or exhaustion, and an old man's request for nothing in return "
        "standing beside two other men who ask for quite a lot"),
    "2samuel20": (CLS,
        "A cry of secession, we have no part in David, growing directly "
        "out of the tribal jealousy the previous chapter never "
        "resolved, ten concubines left in a widowhood that is neither "
        "marriage nor freedom because of what was done to them in "
        "public, a greeting and a beard grasped as if for a kiss "
        "disguising the sword that kills a newly appointed commander, a "
        "wise woman negotiating a siege by asking why the inheritance "
        "of the LORD should be swallowed up, and an administrative list "
        "closing the chapter as a sign of stability finally restored"),
    "2samuel21": (CLS,
        "A three-year famine traced back to an oath Saul broke against "
        "Gibeonites who had deceived Israel decades earlier, seven "
        "descendants handed over for execution while Mephibosheth alone "
        "is spared because of an oath to Jonathan, Rizpah's vigil over "
        "unburied bodies moving David to give them proper burial at "
        "last, a king rescued by Abishai after nearly falling to a "
        "giant in battle, and men calling him the lamp of Israel as the "
        "reason he must never go to battle again"),
    "2samuel22": (CLS,
        "A cascade of titles opening the song, rock, fortress, "
        "deliverer, shield, horn of salvation, each reflecting a "
        "different way God was actually experienced, nine verses of "
        "cosmic storm and earthquake answering the cry of one man "
        "drowning, rescue attributed to delight rather than merit, he "
        "delivered me because he delighted in me, righteousness claimed "
        "as covenant faithfulness rather than sinless perfection, and a "
        "doxology closing on mercy promised to David's seed for "
        "evermore"),
    "2samuel23": (CLS,
        "Four titles claimed at once, son of Jesse, raised on high, "
        "anointed of the God of Jacob, sweet psalmist of Israel, before "
        "the oracle itself even begins, an admission that his own house "
        "has not perfectly lived up to the ideal he is describing, "
        "three men breaking through enemy lines for water David then "
        "refuses to drink and pours out instead as an offering, "
        "warriors ranked and counted by name down to thirty-seven, and "
        "a roster that ends, deliberately or not, on the name of Uriah "
        "the Hittite"),
    "2samuel24": (CLS,
        "God's anger against Israel never explained before David is "
        "permitted to be tempted into a census Joab himself recognizes "
        "as prideful, numbers that reveal the sin themselves, eight "
        "hundred thousand and five hundred thousand counted as trust "
        "placed in military strength rather than in God, three choices "
        "offered through the prophet Gad and a plea to fall into the "
        "hand of the LORD rather than the hand of man, a shepherd's "
        "prayer offering himself for a flock that has done nothing, and "
        "a threshing floor bought for full price because an offering "
        "that costs nothing is no offering at all"),
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
