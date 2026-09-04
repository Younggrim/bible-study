#!/usr/bin/env python3
"""Batch 19: 2 Chronicles 1-36, the whole book. See add_key_themes_batch1.py.

    python3 add_key_themes_batch19.py [--check]
"""
import sys

from add_key_themes_batch1 import process

CLS = "Historical Narrative"

DATA = {
    "2chronicles1": (CLS,
        "Political intrigue from the opening chapters of Kings omitted "
        "entirely so Solomon's very first act is worship rather than "
        "politics, an explanation supplied for why the king sacrifices "
        "at Gibeon rather than in Jerusalem, an open question, ask what "
        "I shall give thee, answered by naming what has already been "
        "inherited before asking for wisdom, riches and wealth granted "
        "though never requested, and a horse trade with Egypt recorded "
        "without comment against a law that told a king not to "
        "multiply horses to himself"),
    "2chronicles2": (CLS,
        "Two houses determined at once, one for the LORD and one for "
        "the king's own kingdom, with the labor counted before a "
        "single stone is cut, a letter to Huram built around a "
        "disclaimer, who is able to build him an house, seeing the "
        "heaven of heavens cannot contain him, a Gentile king's reply "
        "opening with his own confession of Israel's God as creator, a "
        "craftsman's tribal ancestry given differently here than in "
        "Kings without either book explaining the discrepancy, and a "
        "census of resident foreigners numbering over a hundred fifty "
        "thousand put to the work"),
    "2chronicles3": (CLS,
        "A single verse tying three separate moments to one patch of "
        "ground, Moriah, the threshing floor and the temple now rising "
        "on it, a date given to the exact day construction began, "
        "cherubim twenty cubits across spanning the whole width of the "
        "holy place wing to wing, a veil worked with cherubim in blue, "
        "purple, crimson and fine linen, and two free-standing pillars "
        "closing the chapter outside the building itself"),
    "2chronicles4": (CLS,
        "Furnishings listed by function starting in the courtyard, a "
        "bronze altar four times the area of the one it replaced, a "
        "distinction drawn precisely, lavers for washing what is "
        "offered and the sea for the priests to wash themselves, brass "
        "cast in the plain of Jordan in quantities the text declines "
        "to total, and a second half that shifts from bronze to gold "
        "as the inventory moves from the courtyard inside the house"),
    "2chronicles5": (CLS,
        "The one thing the whole building was for finally carried "
        "inside once construction is finished, staves left visible and "
        "an ark holding nothing but the two tables from Horeb offered "
        "as evidence rather than assertion, the division that opened "
        "the book, ark in one place and altar in another, resolved in "
        "this single chapter, a choir placed in front of the cloud "
        "where Kings has only priests, and one refrain sung as the "
        "house fills, for he is good, for his mercy endureth for ever"),
    "2chronicles6": (CLS,
        "A paradox stated to the assembly before the prayer even "
        "begins, the LORD hath said he would dwell in the thick "
        "darkness, yet I have built an house of habitation, a brasen "
        "scaffold supplied only by Chronicles for Solomon to kneel on "
        "before the whole congregation, a question left open rather "
        "than resolved, will God in very deed dwell with men on the "
        "earth, seven cases worked through in the same repeated shape, "
        "when this happens and they pray toward this house, then hear "
        "thou from heaven, and a final petition assuming the worst "
        "case, if they sin, for there is no man which sinneth not, "
        "closing differently than the parallel in Kings"),
    "2chronicles7": (CLS,
        "Fire from heaven reported only by Chronicles, consuming the "
        "offering the moment the prayer ends, twenty-two thousand oxen "
        "and a hundred twenty thousand sheep counted across seven days "
        "of dedication and seven of feasting, a nighttime answer "
        "opening with I have heard thy prayer before it ever reaches "
        "the verse the whole book is built around, if my people, which "
        "are called by my name, shall humble themselves, terms of "
        "judgment stated in language as specific as the blessing, "
        "plucked up by the roots and made a proverb among all nations, "
        "and readers living in the aftermath of exactly that second "
        "half"),
    "2chronicles8": (CLS,
        "Twenty years of building given a hard stop before the account "
        "turns to fortified cities and administration, foreign peoples "
        "made bondservants while Israelites serve only as soldiers and "
        "officers, a scruple only Chronicles keeps, Pharaoh's daughter "
        "moved out of David's own city because it was too holy for her "
        "to remain there, worship organized to a schedule the "
        "Chronicler treats as the real test of any reign, and a voyage "
        "to Ophir returning four hundred fifty talents of gold"),
    "2chronicles9": (CLS,
        "A queen undone not by answers to her hard questions but by "
        "the ordinary arrangements, the seating, the food, the ascent "
        "to the house of the LORD, six hundred sixty-six talents of "
        "gold in one year with silver counted as nothing at all, an "
        "ivory throne with lions on its steps judged like none made in "
        "any kingdom, sources named that no longer exist, the book of "
        "Nathan, the prophecy of Ahijah, the visions of Iddo, and a "
        "whole chapter of apostasy in Kings passed over here in total "
        "silence"),
    "2chronicles10": (CLS,
        "A coronation turned into a negotiation the moment Rehoboam "
        "arrives at Shechem instead of Jerusalem, two counsels "
        "offered, one treating loyalty as something bought with "
        "kindness and one escalating into a boast about scorpions, a "
        "narrator's own aside naming the cause of God behind a king's "
        "foolish choice, an old rebellion cry revived word for word, "
        "what portion have we in David, and a final miscalculation, "
        "sending the very officer over forced labor to collect it, "
        "ending in his death by stoning"),
    "2chronicles11": (CLS,
        "A hundred eighty thousand men mustered for reconquest and "
        "stopped by one prophetic word, this thing is done of me, "
        "fifteen cities fortified and named individually as the "
        "defensive policy chosen instead of war, priests and Levites "
        "migrating south in a story of movement rather than of royal "
        "policy, an heir marked out deliberately while the rest of a "
        "large family is dispersed with enough comfort to keep them "
        "content, and a working solution to the very problem of "
        "rivalry that had just destroyed the united kingdom"),
    "2chronicles12": (CLS,
        "A verdict given before the invasion even starts, when "
        "Rehoboam had strengthened himself he forsook the law of the "
        "LORD, an Egyptian campaign whose record on a relief at Karnak "
        "makes this one of the earliest points where scripture and "
        "outside history touch, a prophetic principle stated plainly, "
        "ye have forsaken me, therefore have I left you to Shishak, "
        "humility acknowledged in one clause, the LORD is righteous, "
        "that triggers partial rather than complete deliverance, and "
        "gold shields replaced by brass kept up with the same ceremony "
        "but none of the substance"),
    "2chronicles13": (CLS,
        "Three verses in Kings expanded here into a full battlefield "
        "address that is the most compact statement of the book's own "
        "theology, a covenant of salt claimed for David's line before "
        "a single argument about the actual battle, an accusation "
        "aimed at worship rather than at politics, the sons of Aaron "
        "cast out for calves of gold, an ambush attacked from both "
        "sides answered by crying unto the LORD and the sound of "
        "trumpets, and a causation stated without hedging, they "
        "prevailed because they relied upon the LORD God of their "
        "fathers"),
    "2chronicles14": (CLS,
        "Ten years of rest spent on demolition and construction at "
        "once, a king's own words supplying the reasoning, let us "
        "build these cities while the land is yet before us because we "
        "have sought the LORD, an invading host counted at a million "
        "met by a prayer that argues from God's indifference to odds, "
        "LORD, it is nothing with thee to help, whether with many or "
        "with them that have no power, a battle made explicitly God's "
        "own rather than Judah's, we rest on thee, and a rout that "
        "runs all the way to Gerar"),
    "2chronicles15": (CLS,
        "A prophet meeting a returning army with a condition rather "
        "than a congratulation, the LORD is with you while ye be with "
        "him, judges-era chaos described as the alternative to seeking "
        "God, an oath sworn with a loud voice, shouting, trumpets and "
        "cornets after seven hundred oxen and seven thousand sheep are "
        "offered, Asa's own reform reaching into his mother's position "
        "and removing her as queen mother, and two measured results "
        "named directly, all Judah rejoiced and the LORD gave them "
        "rest round about"),
    "2chronicles16": (CLS,
        "A blocked road answered by treasury gold sent to buy a "
        "foreign alliance rather than by prayer, a strategy that works "
        "exactly as intended and is condemned anyway, a seer's rebuke "
        "built entirely on the king's own history, the Ethiopians and "
        "Lubims once defeated by a different reliance, the best-known "
        "line in Chronicles after 7:14, the eyes of the LORD run to "
        "and fro throughout the whole earth, a prophet imprisoned for "
        "delivering exactly this message, and a diseased king who "
        "still sought physicians rather than the LORD even in his "
        "final illness"),
    "2chronicles17": (CLS,
        "A verdict given early, the LORD was with Jehoshaphat because "
        "he walked in the first ways of David his father, a qualifier, "
        "first, doing real work by pointing past both kings' later "
        "failures, a teaching circuit with no parallel in Kings, "
        "princes, Levites and priests carrying the book of the law "
        "itself through every city of Judah, quiet borders and "
        "unrequested tribute as the fruit of public instruction rather "
        "than of military threat, and a muster roll closing the "
        "chapter with numbers of the same order the Chronicler uses "
        "throughout"),
    "2chronicles18": (CLS,
        "An alliance committed to before it is ever inquired about, I "
        "am as thou art and my people as thy people, spoken before any "
        "word from the LORD is sought, four hundred prophets unanimous "
        "against Micaiah's single dissent, a lying spirit that "
        "volunteers itself in a heavenly council as the explanation "
        "for why four hundred voices could all agree and still be "
        "wrong, a disguise that nearly works until Jehoshaphat's own "
        "cry turns the pursuers away, and a random arrow finding the "
        "one joint in armor that no disguise could protect"),
    "2chronicles19": (CLS,
        "A chapter with no parallel in Kings recording both a rebuke "
        "and a reform in the same breath, a question that names the "
        "sin directly, shouldest thou help the ungodly and love them "
        "that hate the LORD, a verdict deliberately mixed, "
        "nevertheless there are good things found in thee, judges "
        "charged with a standard drawn from God's own conduct, no "
        "iniquity, no respect of persons, no taking of gifts, and the "
        "fullest description of a judicial system anywhere in the Old "
        "Testament built from that one rebuke"),
    "2chronicles20": (CLS,
        "A king's fear named honestly before his response to it, "
        "Jehoshaphat feared and set himself to seek the LORD, a prayer "
        "built as a legal argument citing jurisdiction, promise and "
        "the irony of nations Israel was once forbidden to invade, an "
        "answer that reassigns the whole battle, the battle is not "
        "yours, but God's, singers sent out before the army rather "
        "than soldiers, praising the beauty of holiness before a shot "
        "is fired, and a reign ending exactly where chapter eighteen "
        "began, with an alliance a prophet condemns in one sentence"),
    "2chronicles21": (CLS,
        "Brothers given wealth and cities by their own father killed "
        "the moment the firstborn is strengthened enough to do it, a "
        "marriage explaining the whole direction of a reign, he had "
        "the daughter of Ahab to wife, a covenant with David alone "
        "keeping the book from reading as a simple ledger of what was "
        "deserved, a letter from Elijah, his only appearance in "
        "Chronicles, naming exactly what will be taken and in what "
        "order, and a death from disease in the bowels ending with no "
        "burning made for him like his fathers and no mourning at all"),
    "2chronicles22": (CLS,
        "A king reigning only because raiders had already killed every "
        "older brother who might have taken the throne first, a "
        "mother named outright as his counsellor to do wickedly, a "
        "numerical difference between this book and Kings that has "
        "never been fully resolved, a destruction credited to God for "
        "the specific reason he went to visit the wrong king at the "
        "wrong time, and an entire royal line reduced to one hidden "
        "infant while Athaliah destroys every other seed of the house "
        "of Judah"),
    "2chronicles23": (CLS,
        "An operation described as a national religious assembly here "
        "rather than the palace-guard coup of the parallel account in "
        "Kings, a covenant cited before any action is taken, the "
        "king's son shall reign as the LORD hath said of the sons of "
        "David, Athaliah's own cry, treason, treason, naming exactly "
        "what she herself had committed six years earlier, an "
        "execution carried out deliberately outside the temple to keep "
        "the sanctuary unstained by her blood, and reconstruction on "
        "three fronts at once, covenant, the house of Baal torn down, "
        "and the temple offices restored"),
    "2chronicles24": (CLS,
        "A verdict bounded explicitly by another man's lifetime, right "
        "all the days of Jehoiada the priest, a first fundraising "
        "method that fails and the text says why without excusing "
        "anyone, the Levites hastened it not, a chest set outside that "
        "works because it removes the human middleman entirely, the "
        "one man in the whole book given a royal burial though he was "
        "never a king, and a mentor's death followed immediately by "
        "the very collapse his life had been holding back, ending in "
        "Zechariah's stoning and Joash's own murder in his bed"),
    "2chronicles25": (CLS,
        "The book's most exact verdict, right in the sight of the LORD "
        "but not with a perfect heart, given before a single event of "
        "the chapter unfolds, murderers' children spared in deliberate "
        "obedience to a statute the text quotes directly, a hundred "
        "talents already spent on hired troops sent home anyway on a "
        "prophet's word, gods of the defeated Edomites brought home "
        "and worshipped in an act the narrator leaves standing as "
        "absurd without comment, and a prophet cut off mid-sentence, "
        "art thou made of the king's counsel, before he finishes his "
        "diagnosis"),
    "2chronicles26": (CLS,
        "Fifty-two years of prosperity tied explicitly to a duration "
        "rather than to a fixed character, as long as he sought the "
        "LORD, God made him to prosper, achievements itemised like a "
        "state record, broken cities, dug wells, an army of over three "
        "hundred thousand and engines invented for the towers, a "
        "boundary violation rather than mere unbelief, a king who was "
        "strong enough to think he could burn incense that belonged "
        "only to the priests, eighty priests confronting him with the "
        "censer still in his hand, and leprosy rising in his forehead "
        "as the sentence that defines the rest of his life"),
    "2chronicles27": (CLS,
        "One clause carrying an entire comparison to his father, right "
        "according to all that Uzziah did, howbeit he entered not into "
        "the temple of the LORD, a standing observation slipped in "
        "even during praise, the people did yet corruptly, Ammonite "
        "tribute specified for three years running as the chapter's "
        "one dramatic achievement, a verdict with nothing subtracted "
        "from it anywhere in this run of chapters, and nine verses "
        "given to the cleanest record in the whole book while collapse "
        "and recovery elsewhere claim entire chapters"),
    "2chronicles28": (CLS,
        "Child sacrifice in the valley of Hinnom named as the exact "
        "practice that once justified expelling the land's previous "
        "inhabitants, casualties given with a cause attached each "
        "time, because they had forsaken the LORD God of their "
        "fathers, an appeal to Assyria answered in four words, but he "
        "helped him not, a king's own reasoning stated plainly as the "
        "clearest statement of pagan logic in the book, because the "
        "gods of Syria help them therefore will I sacrifice to them, "
        "and temple doors shut entirely by the very king meant to keep "
        "them open"),
    "2chronicles29": (CLS,
        "Doors shut by a father reopened as the first act of a son's "
        "reign in its very first month, an instruction to the Levites "
        "paired with a diagnosis, our fathers have trespassed and "
        "turned away their faces from the habitation of the LORD, "
        "sixteen days dated precisely to carry the accumulated refuse "
        "of a closed temple out to the brook Kidron, an offering made "
        "explicitly for all Israel though Judah's king has no "
        "authority over the northern tribes, and a comparison recorded "
        "without softening, the Levites were more upright in heart to "
        "sanctify themselves than the priests"),
    "2chronicles30": (CLS,
        "A Passover kept a month late using a provision Numbers itself "
        "makes for exactly this case, letters sent into territory "
        "Assyria had already annexed inviting a shattered kingdom's "
        "remnant back to Jerusalem, an appeal built on catastrophe "
        "rather than on strength, turn again unto the LORD and he will "
        "return to the remnant of you that escaped, a prayer offered "
        "instead of exclusion for worshippers who came unprepared, the "
        "good LORD pardon every one that prepareth his heart, and a "
        "second seven days added with no precedent in the law because "
        "the assembly did not want the celebration to end"),
    "2chronicles31": (CLS,
        "A festival ending in demolition rather than dispersal, images "
        "broken and high places thrown down as far as Ephraim and "
        "Manasseh, giving encouraged with a stated purpose, that they "
        "might be encouraged in the law of the LORD, contributions "
        "piling in heaps for months faster than the system built to "
        "receive them, chambers, overseers and distribution rules "
        "specified with the same care given to a battle, and a verdict "
        "that credits the paperwork itself as evidence of faithfulness"),
    "2chronicles32": (CLS,
        "An invasion arriving after all Hezekiah's reforms rather than "
        "in place of them, faithfulness proving no immunity from "
        "trial, an Assyrian argument allowed to run at length because "
        "it is a genuinely good one, why should this god succeed where "
        "every other nation's god has failed, a religious reform "
        "turned into evidence against the very king who carried it "
        "out, four verses disposing of the entire siege once Hezekiah "
        "and Isaiah pray, and pride after healing corrected only by "
        "humbling before the wrath actually arrives, the same "
        "structure as Uzziah's fall with a different ending"),
    "2chronicles33": (CLS,
        "Fifty-five years, the longest reign of any king of Judah, "
        "spent cataloguing nine verses of exactly what it restored, a "
        "carved image set in the very house of which God had said, in "
        "Jerusalem shall my name be forever, a section found only in "
        "Chronicles that changes the whole shape of the reign, fetters "
        "and captivity in Babylon followed by affliction driving a "
        "king to beseech the LORD his God, an answer as unqualified as "
        "the offence had been, and a son who does as his father had "
        "done but never humbles himself as his father did, trespassing "
        "more and more instead"),
    "2chronicles34": (CLS,
        "A reform staged deliberately across three ages, seeking at "
        "sixteen, purging at twenty, repairing at twenty-six, a reach "
        "into territory no king of Judah had governed for a century, "
        "only possible because Assyrian power was already collapsing, "
        "a book found by accident during ordinary repair work and read "
        "aloud before its identity is ever confirmed, clothes torn and "
        "an enquiry sent because great is the wrath of the LORD poured "
        "out upon us, and an answer from Huldah that does not cancel "
        "judgment but grants one king's own eyes will not see it"),
    "2chronicles35": (CLS,
        "A single line quietly ending an era, no more shall there be a "
        "burden upon your shoulders, retiring the Levites' carrying "
        "duty for good, provisioning measured in numbers precisely "
        "because generosity is what is being counted, a service so "
        "procedural that everything being exactly where the writing "
        "says is called the Chronicler's highest praise, an assessment "
        "reaching back past the whole monarchy, no passover like it "
        "since Samuel, and a warning from an unexpected mouth, Necho's "
        "own claim to carry a word from God, ignored by the last good "
        "king of Judah to his death"),
    "2chronicles36": (CLS,
        "Four kings compressed into twenty-three years, each installed "
        "and deposed at the convenience of whichever empire is "
        "nearest, an age given differently here than in the parallel "
        "account in Kings with neither book explaining the divergence, "
        "a compassion named as God's motive for sending messenger "
        "after messenger rather than patience simply running out, "
        "mockery and misuse of every prophet sent until there was no "
        "remedy left at all, and a book that ends fifty years later on "
        "a Persian king's own proclamation, crediting his empire to "
        "Israel's God and commanding the exiles to go up"),
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
