#!/usr/bin/env python3
"""Batch 18: 1 Chronicles 1-29, the whole book. See add_key_themes_batch1.py.

Chapters 1-9 are genealogies rather than narrative, so their Classification
reads "Historical Narrative — Genealogy" instead of plain "Historical
Narrative".
"""
import sys

from add_key_themes_batch1 import process

CLS = "Historical Narrative"
CLS_GEN = "Historical Narrative — Genealogy"

DATA = {
    "1chronicles1": (CLS_GEN,
        "Ten generations from Adam to Noah covered in four verses with "
        "no dates and no narrative at all, a table of nations arranged "
        "in reverse order so the line that matters comes last, the "
        "whole human race narrowed to one man by verse twenty-seven "
        "through simple omission, Ishmael and Keturah's sons listed in "
        "full before Isaac's line is ever taken up, and twenty-one "
        "verses given to Edom, more than Shem, Ham and Japheth "
        "combined, because Edom had kings before Israel ever did"),
    "1chronicles2": (CLS_GEN,
        "Eleven tribes named in one sentence and set aside for six "
        "chapters so Judah can be taken up immediately, Er's "
        "wickedness and Tamar's deception recorded without being "
        "smoothed over in the first eight verses, nine verses carrying "
        "the entire line the whole book depends on, from Ram to Jesse "
        "to David, David's own military commanders identified as his "
        "nephews through a sister the text bothers to name, and a "
        "closing list that turns names into towns rather than persons"),
    "1chronicles3": (CLS_GEN,
        "David's sons divided by birthplace, Hebron and Jerusalem, "
        "with nothing recorded about what any of them did, fourteen "
        "reigns from Solomon to Josiah listed with no distinction made "
        "between the worst kings and the best, four sons of Josiah "
        "named in one place found nowhere else in scripture, Jeconiah "
        "labelled the captive as the throne effectively ends, and a "
        "line continued six generations past Zerubbabel to prove a "
        "documented heir survives even without a throne"),
    "1chronicles4": (CLS_GEN,
        "Terse entries naming fathers of towns rather than fathers of "
        "sons throughout most of the chapter, a register that stops "
        "dead for two verses to quote a man's prayer by name, oh that "
        "thou wouldest bless me indeed and enlarge my coast, craftsmen "
        "and linen workers and potters recorded by trade rather than "
        "only by descent, and Simeon's own record of taking ground in "
        "two dated raids despite a tribe absorbed into Judah's larger "
        "territory"),
    "1chronicles5": (CLS_GEN,
        "A birthright forfeited in the opening verses and explained "
        "rather than merely noted, Reuben's line ending with a name "
        "carried away captive by Assyria, a war credited explicitly to "
        "prayer rather than to the numbers the register has just "
        "finished counting, because they put their trust in him, and "
        "the three eastern tribes named first to go into exile with "
        "the reason stated as directly as the earlier victory, they "
        "transgressed against the God of their fathers"),
    "1chronicles6": (CLS_GEN,
        "Eighty-one verses, the longest genealogical chapter in the "
        "book, dedicated entirely to the tribe responsible for "
        "worship, twenty-three generations of high priests traced in "
        "one unbroken line from Aaron to the exile, Samuel placed "
        "inside the Kohathite Levites rather than in Ephraim where an "
        "earlier book locates his home, three chief singers, Heman, "
        "Asaph and Ethan, distributed one from each Levitical family by "
        "design, and forty-eight scattered towns closing the chapter as "
        "the only territory a tribe with no land of its own ever "
        "receives"),
    "1chronicles7": (CLS_GEN,
        "A chapter whose attention swings unevenly from one tribe to "
        "the next, Naphtali given a single verse while others receive "
        "whole genealogies, muster numbers embedded directly into a "
        "family tree as though compiling an army roster alongside a "
        "lineage, sons slain at Gath in a raid gone wrong recorded "
        "nowhere else, a child named Beriah because it went evil with "
        "his house, and eleven verses standing as the entire record "
        "Chronicles keeps of Asher"),
    "1chronicles8": (CLS_GEN,
        "A second and far longer treatment of Benjamin than the tribe "
        "received in the previous chapter, families tracked by where "
        "they resettled and remarried after near destruction in Judges "
        "twenty, a list narrowing at last to one household, Kish and "
        "Saul and his four sons, Jonathan's own line followed ten more "
        "generations through the man 2 Samuel calls Mephibosheth, and "
        "Saul given a family here with no reign, no failure and no "
        "death, since the narrative saves all three for chapter ten"),
    "1chronicles9": (CLS_GEN,
        "A pivot clause turning nine chapters of descent into the "
        "reason for writing them at all, carried away to Babylon for "
        "their transgression, priests and Levites counted by name to "
        "establish exactly who may serve in a temple still being "
        "rebuilt, eighteen verses on gatekeeping alone, more than most "
        "entire tribes received, shifts, chambers and daily provisions "
        "specified for men whose charge required some to lodge around "
        "the house itself, and Saul's household repeated almost word "
        "for word from the chapter before, closing nine chapters of "
        "names right where the narrative is about to begin"),
    "1chronicles10": (CLS,
        "A whole reign compressed into one chapter, the chapter in "
        "which the king dies, no anointing, no jealousy and no pursuit "
        "of David included at all, a body stripped and its head "
        "fastened in the temple of Dagon as a trophy of religious "
        "triumph, Jabesh-gilead's rescue of the bones told exactly as "
        "in the earlier book, and a theological verdict added that "
        "Samuel never gives, Saul died for his transgression, and "
        "turned the kingdom unto David"),
    "1chronicles11": (CLS,
        "Seven years of civil war with the house of Saul omitted "
        "entirely so all Israel anoints David at once, a promotion "
        "offered to whoever takes Jerusalem first turning Joab into "
        "chief before a single battle is fought, three men breaking "
        "through a Philistine garrison for water David only longed for "
        "aloud and then refuses to drink, a growing sentence repeated "
        "throughout the book, David waxed greater and greater for the "
        "LORD of hosts was with him, and a roster of mighty men "
        "extended past the thirty into tribes and nations beyond "
        "Israel itself"),
    "1chronicles12": (CLS,
        "A chapter with no parallel in Samuel added specifically to "
        "prove all Israel, not one tribe, supported David, Benjamites "
        "from Saul's own tribe defecting to the very man Saul was "
        "hunting, warriors of Issachar praised not for strength but "
        "for understanding the times, a host described as like the "
        "host of God rather than merely large, and a coronation closed "
        "out by relatives bringing food on donkeys and camels because "
        "there was joy in Israel"),
    "1chronicles13": (CLS,
        "A decision to move the ark justified as a correction of "
        "Saul's own neglect, for we enquired not at it in the days of "
        "Saul, a new cart chosen anyway, the very method the "
        "Philistines once used and not the one the law prescribed, "
        "celebration described in full, singing, harps, cymbals and "
        "trumpets, right before the paragraph that undoes it, Uzza "
        "struck dead for steadying what stumbling oxen threatened to "
        "spill, and the same ark blessing Obed-edom's household while "
        "it killed the man who touched it"),
    "1chronicles14": (CLS,
        "Hiram's builders read as proof the LORD had confirmed David's "
        "kingdom for the people's sake rather than his own, thirteen "
        "sons listed at Jerusalem including Solomon with no mention at "
        "all of his mother, two Philistine battles both begun by "
        "asking rather than assuming the answer already known, a "
        "commander who had just won once told to do something entirely "
        "different the second time, wait for the sound of a going in "
        "the tops of the trees, and fame that spreads into all lands "
        "as the direct result of obedience rather than mere victory"),
    "1chronicles15": (CLS,
        "A second attempt that begins with research rather than "
        "repetition of the first mistake, the rule stated outright "
        "before it is followed, none ought to carry the ark of God but "
        "the Levites, four thousand priests and Levites gathered by "
        "family so the correction is executed rather than merely "
        "announced, nine verses of musical staffing organizing a "
        "procession like an orchestra, and Michal kept at the window "
        "despising David in her heart while the argument that follows "
        "it in Samuel is cut entirely"),
    "1chronicles16": (CLS,
        "Bread, meat and wine distributed to every man and woman in "
        "Israel before a single note of the psalm is sung, a psalm "
        "delivered into Asaph's hand that readers of the Psalter will "
        "recognize almost word for word as Psalm 105, touch not mine "
        "anointed and do my prophets no harm read by exiles as a "
        "promise still standing over them, creation itself called to "
        "respond, let the heavens be glad, let the sea roar, let the "
        "trees of the wood sing, and two sanctuaries left standing at "
        "once, the ark in Jerusalem and the altar still at Gibeon, "
        "exactly the problem the temple will solve"),
    "1chronicles17": (CLS,
        "An embarrassment about accommodation, I dwell in a house of "
        "cedars while the ark remains under curtains, corrected the "
        "same night Nathan first approved it, a question with a "
        "history attached, did I ever ask any judge why he had not "
        "built me a house of cedars, a wordplay on house turning "
        "David's offer to build into God's promise to build for him "
        "instead, mercy promised never to be taken away as it was from "
        "the one before him, and a prayer that asks for nothing new, "
        "only that the promise already given be established"),
    "1chronicles18": (CLS,
        "Eight verses covering campaigns in four directions with the "
        "Chronicler's attention fixed on what came back rather than "
        "how the fighting went, temple furniture named directly, "
        "brass Solomon will later use for the sea and the pillars, "
        "taken from these very wars, a refrain repeated as the "
        "chapter's own summary, the LORD preserved David whithersoever "
        "he went, tribute from Tou of Hamath dedicated rather than "
        "kept, and a conquest chapter closing on nothing more dramatic "
        "than a list of officers running a civil service"),
    "1chronicles19": (CLS,
        "Condolences sent in genuine kindness reinterpreted by "
        "advisors as espionage before any war is declared, beards "
        "shaved and garments cut as a diplomatic insult severe enough "
        "to trigger a war on its own, a two-front battle answered by "
        "the best speech Joab gives anywhere, let the LORD do that "
        "which is good in his sight, thirty-two thousand hired "
        "chariots still ending in defeat and flight, and Syria's peace "
        "with David leaving Ammon without an ally for the siege the "
        "next chapter opens with"),
    "1chronicles20": (CLS,
        "Three chapters of Bathsheba and Uriah in Samuel compressed to "
        "nothing at all here, the omission louder than anything the "
        "chapter actually records, David tarried at Jerusalem kept "
        "without the sentence that follows it in the other book, a "
        "crown weighing a talent of gold taken from Rabbah's king "
        "rather than any account of what happened while the siege "
        "continued, three giants killed by three named soldiers rather "
        "than by David himself, and credit assigned deliberately to a "
        "reign, they fell by the hand of David and by the hand of his "
        "servants, rather than to any one man"),
    "1chronicles21": (CLS,
        "Satan named outright as the one who provoked the census, a "
        "different opening clause than the parallel account in Samuel, "
        "Joab objecting and overruled anyway before Levi and Benjamin "
        "are quietly left out of his own count, three choices reduced "
        "to a preference about whose hand should hold the sword, let "
        "me fall into the hand of the LORD rather than the hand of "
        "man, a plea to redirect the punishment onto the shepherd "
        "rather than the sheep, and a threshing floor paid for in full "
        "because an offering that costs nothing is refused on "
        "principle"),
    "1chronicles22": (CLS,
        "A site named in one sentence before David starts buying "
        "materials he will never use himself, a reason for the refusal "
        "given in David's own words nowhere else in scripture, thou "
        "hast shed blood abundantly and made great wars, a name "
        "explained as its own argument, Solomon, a man of rest, for a "
        "house built once the fighting is finally over, an inventory "
        "of gold and silver measured without weight because counting "
        "it exactly missed the point, and a charge to the princes that "
        "puts seeking the LORD before the actual building begins"),
    "1chronicles23": (CLS,
        "Thirty-eight thousand Levites numbered and divided by "
        "function rather than by tribe, irregular entries left uneven "
        "rather than rounded because the register is a working duty "
        "roster and not a composition, an age lowered from thirty to "
        "twenty explained by the job itself changing, the Levites "
        "shall no more carry the tabernacle, courts, chambers and "
        "shewbread replacing transport as the new description of the "
        "work, and morning and evening praise fixed as a permanent "
        "duty rather than an occasional one"),
    "1chronicles24": (CLS,
        "Two of Aaron's four sons removed from the record in the first "
        "two verses for dying without children, a rota drawn by lot "
        "specifically to forestall any dispute over precedence, "
        "twenty-four courses established that were still running a "
        "thousand years later when Zacharias served in Luke's Gospel, "
        "seniority explicitly set aside so no elder son received a "
        "better rotation than a younger, and the same lot-casting "
        "method applied to every Levite family, principal fathers "
        "treated the same as their younger brethren"),
    "1chronicles25": (CLS,
        "Musicians described three times in eight verses as "
        "prophesying with harps, psalteries and cymbals rather than "
        "merely playing them, Heman called the king's seer and "
        "credited with children serving under his own direction, two "
        "hundred eighty-eight singers organized into twenty-four "
        "courses mirroring the priestly rota exactly, an impartial lot "
        "cast for the small and the great, the teacher and the "
        "scholar alike, and a run of names that reads in Hebrew as a "
        "fragment of prayer about mercy and visions folded into a "
        "family list"),
    "1chronicles26": (CLS,
        "Gatekeepers organized by family and by reason, one man chosen "
        "specifically because he was a wise counsellor, Obed-edom "
        "returning from chapter thirteen with sons the register "
        "credits directly to God's blessing on his house, a duty "
        "roster for the east, north, south and storehouse gates "
        "settled by lot for a building that does not exist yet, "
        "dedicated spoils from Samuel, Saul, Abner and Joab catalogued "
        "as generations of plunder turned into temple endowment, and "
        "Levites posted outward over Israel's civil affairs, the tribe "
        "with no land administering everybody else's"),
    "1chronicles27": (CLS,
        "An army organized as a rotating militia of twenty-four "
        "thousand a month rather than a standing force, commanders "
        "drawn directly from the mighty men who once took Jerusalem, "
        "two tribes missing from the list of princes with no "
        "explanation offered, a census admitted to have been left "
        "unfinished and deliberately excluded from the official record "
        "because wrath fell on Israel for it, and an inventory of "
        "royal estates naming a man over every vineyard, herd and "
        "storehouse down to the sycomore trees"),
    "1chronicles28": (CLS,
        "An old and full-of-days king standing up on his own feet, a "
        "detail with visible effort in it, to deliver one final public "
        "speech, a refusal and its reason repeated in front of the "
        "whole assembly, thou hast been a man of war and hast shed "
        "blood, two verses to Solomon alone that are the sharpest "
        "thing David says in the entire book, if thou forsake him he "
        "will cast thee off for ever, temple plans described as given "
        "by the Spirit in writing the same way the tabernacle pattern "
        "once was, and an encouragement that admits the size of the "
        "task before it ever promises help"),
    "1chronicles29": (CLS,
        "A personal contribution offered first and described as "
        "proper good rather than royal treasury, willingly repeated "
        "three times in one verse to describe the mood of an entire "
        "assembly's giving, a prayer arguing that nothing given was "
        "ever truly theirs to begin with, all things come of thee and "
        "of thine own have we given thee, an unembarrassed "
        "self-description, strangers and sojourners whose days are as "
        "a shadow, and a succession the Chronicler describes as "
        "untroubled, with Adonijah's earlier attempt on the throne "
        "left entirely unmentioned"),
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
