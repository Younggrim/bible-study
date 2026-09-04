#!/usr/bin/env python3
"""Batch 16: 1 Samuel 1-14, 16-31 (chapter 15 already had the pair;
otherwise the whole book). See add_key_themes_batch1.py.

    python3 add_key_themes_batch16.py [--check]
"""
import sys

from add_key_themes_batch1 import process

CLS = "Historical Narrative"

DATA = {
    "1samuel1": (CLS,
        "Renewal beginning not with a warrior or a political revolution "
        "but with a barren woman's prayer, the LORD stated twice to "
        "have shut up her womb rather than left it to chance, lips "
        "moving with no voice heard mistaken by the priest for "
        "drunkenness, a name explained by a wordplay, because I have "
        "asked him of the LORD, and a vow kept by lending the child "
        "back to the very God who gave him"),
    "1samuel2": (CLS,
        "A song that moves from one woman's relief to a cosmic "
        "declaration about how God reverses every human condition, "
        "sons called worthless men who knew not the LORD despite "
        "serving as priests in His own house, meat stolen from "
        "sacrifices before the fat could even be burned to God, a "
        "rebuke that is verbal but toothless because Eli never removes "
        "his sons from office, and a prophecy naming the exact day both "
        "sons will die as its confirming sign"),
    "1samuel3": (CLS,
        "A rare and precious word of the LORD opening the chapter as a "
        "statement of spiritual famine rather than mere quiet, three "
        "calls mistaken for Eli before a fourth is finally recognized "
        "as God's own voice, speak, LORD, for thy servant heareth "
        "answered by a message that will make both ears of anyone who "
        "hears it tingle, a boy afraid to deliver a death sentence to "
        "the mentor who raised him, and Eli's own response, it is the "
        "LORD, let him do what seemeth him good, submission without any "
        "accompanying repentance"),
    "1samuel4": (CLS,
        "An ark fetched into battle as equipment rather than sought "
        "after in repentance, Philistines more theologically alert than "
        "Israel in recognizing these are the Gods that smote the "
        "Egyptians, four pieces of news delivered in ascending severity "
        "with only the last one killing Eli, a name given at birth, "
        "Ichabod, the glory is departed, spoken by a mother who dies in "
        "the act of naming him, and forty years of judging ended by a "
        "fall backward off a seat rather than in glory"),
    "1samuel5": (CLS,
        "An idol found fallen on its face before the ark and set back "
        "up only to fall again, this time dismembered at the threshold, "
        "a war trophy that turns out to defend itself without any human "
        "army, the hand of the LORD named as the keyword of a plague "
        "that moves city to city with the ark itself, Ashdod, Gath and "
        "Ekron suffering in increasing severity as the ark is passed "
        "along, and a captured object treated as a spoil of war "
        "revealing itself as something no one actually wants to keep"),
    "1samuel6": (CLS,
        "Philistine priests knowing the Exodus story well enough to "
        "warn their own people against hardening their hearts like "
        "Pharaoh, cows overriding every natural instinct toward their "
        "calves to walk straight toward Israel, a town that rejoices at "
        "the ark's arrival in one verse and asks to be rid of it eight "
        "verses later, five golden emerods and five golden mice "
        "itemized one for each Philistine city, and a question that "
        "closes the chapter, who is able to stand before this holy LORD "
        "God, answered by nobody"),
    "1samuel7": (CLS,
        "Twenty years summarized as a nation lamenting after the LORD "
        "before any revival actually begins, a condition set rather "
        "than a rally led, if ye do return unto the LORD with all your "
        "hearts, thunder from heaven doing the fighting while Israel "
        "only pursues what is already routed, a memorial stone named "
        "Ebenezer at the very place Israel was once defeated, and "
        "Samuel's circuit judgeship covering Bethel, Gilgal and Mizpah "
        "from a home base at Ramah"),
    "1samuel8": (CLS,
        "Samuel's own sons repeating Eli's failure by turning aside "
        "after dishonest gain, a demand for a king named by God as "
        "rejection of Himself rather than of Samuel, a warning built "
        "entirely on the repeated word take, sons, daughters, fields, a "
        "tenth of everything, until you yourselves are servants, a "
        "people who refuse to obey even after hearing exactly what it "
        "will cost them, and God's own instruction, hearken unto their "
        "voice, granting a request He has just finished warning against"),
    "1samuel9": (CLS,
        "A search for lost donkeys turning out to be God's chosen route "
        "to a royal appointment, Saul described as taller than anyone "
        "else in Israel, the kind of king appearance alone would "
        "choose, girls at a well giving the future king his walking "
        "directions without knowing who he is, a word, captain, used "
        "instead of king because even Israel's king serves under God's "
        "own kingship, and a chief seat and a reserved portion of meat "
        "prepared for a guest who has no idea a feast was arranged "
        "around him"),
    "1samuel10": (CLS,
        "Oil poured and a kiss given as the formal acts of an anointing "
        "kept private before it is ever made public, three confirming "
        "signs all fulfilled the same day exactly as Samuel described "
        "them, a proverb born from bewilderment, is Saul also among the "
        "prophets, rather than from reverence, a king found only after "
        "hiding himself among the baggage at his own selection, and a "
        "manner of the kingdom written down and deposited before the "
        "LORD as a witness over the very throne it describes"),
    "1samuel11": (CLS,
        "A demand to gouge out every right eye designed as a calculated "
        "insult to the whole nation, seven days granted by an enemy "
        "confident enough in Israel's helplessness to allow the delay, "
        "oxen cut in pieces and sent throughout Israel echoing the "
        "Levite's dismembered concubine, three companies attacking at "
        "the dawn watch until two of the enemy were not left together, "
        "and Saul refusing to let a military victory become the "
        "occasion for a political purge, not a man shall be put to "
        "death this day"),
    "1samuel12": (CLS,
        "A public challenge to name any ox or ass Samuel ever took, "
        "answered by the people's unanimous acquittal, deliverers named "
        "one after another to prove God provided leaders long before "
        "any king was demanded, the demand for a king traced to a "
        "specific crisis rather than to genuine necessity, thunder "
        "called down in the dry season of wheat harvest as a sign that "
        "cannot be mistaken for coincidence, and a promise never to sin "
        "by ceasing to pray for the very people who asked for a king "
        "against his warning"),
    "1samuel13": (CLS,
        "Credit for Jonathan's attack claimed by Saul in the same "
        "breath as the trumpet blast, a nation dissolving into caves "
        "and pits rather than a battle actually being fought, seven "
        "days waited to the letter before a sacrifice offered one day "
        "too soon, thou hast done foolishly answered not with removal "
        "from the throne but with the end of a dynasty, and a monopoly "
        "on iron so complete that Israel must go to Philistine smiths "
        "even to sharpen farm tools"),
    "1samuel14": (CLS,
        "A declaration of faith made without presuming on the outcome, "
        "there is no restraint to the LORD to save by many or by few, "
        "an attack by two men producing an earthquake and an army "
        "turning its swords on itself, an oath interrupting the very "
        "pursuit it was meant to secure, honey untouched on the ground "
        "until a son who never heard the oath tastes it and calls his "
        "father's rashness by name, and an army overruling its own king "
        "to save the son the lot had condemned"),
    "1samuel16": (CLS,
        "Grief rebuked as something that must not paralyze obedience "
        "any longer, man looking on the outward appearance while the "
        "LORD looks on the heart stated as the chapter's own thesis, "
        "seven older sons passed over before the youngest is even sent "
        "for from the sheep, a father who did not think to bring his "
        "own youngest son to the sacrifice, and the Spirit departing "
        "from Saul in the same verse an evil spirit begins to trouble "
        "him"),
    "1samuel17": (CLS,
        "Forty days of a champion's defiance met by silence from every "
        "man in Saul's army including the king who stands head and "
        "shoulders above them all, an errand to deliver provisions "
        "placing David at the battlefield by nothing more than an "
        "ordinary chore, a reward asked about only after the "
        "theological question, who is this uncircumcised Philistine, "
        "royal armor offered and refused because I have not proved "
        "them, and a declaration of faith answered by a single stone "
        "before the sword is ever needed"),
    "1samuel18": (CLS,
        "A crown prince's soul knit to David's and royal robe and armor "
        "handed over as though the throne itself is being surrendered, "
        "a celebration song turned into a threat the moment Saul starts "
        "counting thousands against ten thousands, a spear hurled twice "
        "at a man playing the harp for the very king who throws it, a "
        "bride price of a hundred Philistine foreskins set as a trap "
        "that David survives by doubling, and success that keeps "
        "multiplying no matter how many ways Saul tries to redirect it "
        "toward the Philistines instead"),
    "1samuel19": (CLS,
        "An oath sworn in the LORD's name broken within verses of being "
        "made, the same spear-and-harp scene repeated until David "
        "finally does not return to it, an idol placed in a bed as a "
        "decoy revealing spiritual compromise even inside David's own "
        "household, three companies of messengers overcome by the "
        "Spirit and made to prophesy instead of arresting anyone, and "
        "Saul himself stripped and lying prophesying naked before "
        "Samuel, restrained rather than worshiping"),
    "1samuel20": (CLS,
        "Three anguished questions, what have I done, what is mine "
        "iniquity, what is my sin, opening a chapter neither man can "
        "yet fully believe needs asking, a New Moon feast turned into a "
        "deliberate test of a father's intentions, a prince who already "
        "knows David will be king and asks only that his own "
        "descendants be shown mercy afterward, an insult to Jonathan's "
        "mother revealing exactly how far Saul's rage has gone, and a "
        "farewell where David is said to weep the most of the two "
        "before they part for good"),
    "1samuel21": (CLS,
        "A lie told to a trembling priest to obtain bread reserved only "
        "for those who serve at the altar, Doeg the Edomite noted in a "
        "single ominous verse that plants a detail for later, Goliath's "
        "own sword taken from behind the ephod and carried by the very "
        "man who once used a sling against it, madness feigned in Gath, "
        "Goliath's home city, to survive a recognition that names David "
        "king of the land, and a fugitive who arrives alone, hungry and "
        "unarmed at the very place meant to provide safety"),
    "1samuel22": (CLS,
        "Four hundred men in distress, in debt and discontented "
        "gathering to a rejected king in a cave rather than to any "
        "court, Saul's paranoia appealing to tribal loyalty before it "
        "ever appeals to evidence, a priest's entirely reasonable "
        "defense ignored the moment it is given, royal guards refusing "
        "to kill God's priests while one Edomite alone carries out the "
        "order, and David's own admission that he occasioned the death "
        "of an entire household by a lie he told to save himself"),
    "1samuel23": (CLS,
        "A fugitive doing the king's actual job, saving a city from "
        "Philistine raiders while the king hunts him instead, David "
        "inquiring of the LORD before every move in deliberate contrast "
        "to Saul's paranoid impulse, a city just rescued willing to "
        "hand its rescuer over the moment Saul asks, Jonathan's last "
        "recorded visit strengthening David's hand in God rather than "
        "in politics, and a chase broken off only by a message about "
        "the Philistines that has nothing to do with either man"),
    "1samuel24": (CLS,
        "A king entering a cave to relieve himself with no idea his "
        "hunted enemy is hiding in its recesses, a conscience troubled "
        "even by cutting a robe's corner when killing was the option "
        "every man around him urged, judgment deliberately left to the "
        "LORD rather than taken by David's own hand, Saul's own "
        "admission, thou art more righteous than I, conceding a truth "
        "his pursuit has never once acted on, and a king who already "
        "knows David will be king asking only that his descendants be "
        "spared afterward"),
    "1samuel25": (CLS,
        "Samuel's death marking the end of an era in one brief, almost "
        "passing notice, a wealthy fool's contempt echoing Saul's own "
        "dismissive language toward the son of Jesse, Abigail's "
        "intervention arriving as the thing that restrains David from "
        "bloodguilt where his own conscience had restrained him with "
        "Saul, a heart that dies within a man the moment he learns what "
        "nearly happened while he feasted like a king, and God striking "
        "Nabal ten days later so David never has to avenge the insult "
        "himself"),
    "1samuel26": (CLS,
        "A second betrayal by the Ziphites leading to a second chance "
        "David again refuses, a deep sleep sent by God over an entire "
        "army rather than mere carelessness, Abishai's offer to end it "
        "with one spear-thrust turned down on the same principle as the "
        "cave, Saul's missing spear and water jug serving as evidence "
        "rather than trophies, and a final parting blessing, thou shalt "
        "both do great things and also shalt still prevail, spoken by "
        "the very man who spent years hunting him"),
    "1samuel27": (CLS,
        "A statement of despair rather than faith, I shall now perish "
        "one day by the hand of Saul, opening a chapter where David's "
        "plan actually works precisely because it is human rather than "
        "divine, Ziklag requested specifically to avoid the constant "
        "surveillance of living in Gath's royal city, raids conducted "
        "with no survivors left to contradict the story told to Achish, "
        "and a deception that succeeds strategically while raising "
        "exactly the moral question the text leaves open"),
    "1samuel28": (CLS,
        "God's silence answering Saul through no channel at all, "
        "dreams, Urim or prophets, after years of Saul ignoring every "
        "channel God actually used, a ban on mediums broken by the very "
        "king who once enforced it, a disguise and a night journey "
        "concealing a king from his own kingdom rather than from an "
        "enemy, Samuel's message repeating exactly what was already "
        "said years earlier with a death sentence now attached, and a "
        "condemned king fed his last meal by the medium he should have "
        "executed"),
    "1samuel29": (CLS,
        "A dilemma David's own deception created resolved by Philistine "
        "commanders rather than by any plan of his own, a pagan king "
        "swearing by the LORD to testify that David has been upright, "
        "the women's song of thousands and ten thousands remembered at "
        "exactly the moment it becomes dangerous rather than "
        "celebratory, David's protest deliberately worded so that my "
        "lord the king could mean either Achish or Saul, and God "
        "extracting David from a battle he could never have fought "
        "without ruin either way"),
    "1samuel30": (CLS,
        "A homecoming to a burned city and captured families discovered "
        "only after three days of marching, David encouraging himself "
        "in the LORD his God at the exact moment his own men speak of "
        "stoning him, an abandoned Egyptian slave, left to die by his "
        "own master, becoming the guide who leads David straight to the "
        "raiders, spoil divided equally between those who fought and "
        "those too exhausted to continue, made a permanent statute "
        "rather than a one-time concession, and gifts sent to Judah's "
        "elders that read as gratitude and as preparation for a throne "
        "at once"),
    "1samuel31": (CLS,
        "A battle whose outcome Samuel had already named years before "
        "it is fought, Jonathan dying alongside a father whose "
        "rebellion was never his own, a king asking his armor-bearer to "
        "finish what the archers could not before falling on his own "
        "sword, a head cut off and armor displayed in a temple exactly "
        "as Goliath's death was once displayed in Israel, and one act "
        "of loyalty from Jabesh-gilead redeeming the chapter, a debt "
        "repaid decades after the king who incurred it saved them "
        "first"),
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
