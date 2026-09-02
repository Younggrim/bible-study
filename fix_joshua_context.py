#!/usr/bin/env python3
"""
Adds Historical Context to Joshua 13-24, the twelve chapters that carried only
Author and Purpose.

This is the land-allotment and farewell section, and it is why Joshua averages
2,251 characters of Authorship & Background against Judges' 4,729. The
conquest narrative in chapters 1-12 was written up; the distribution chapters
were not.

Deliberately NOT touched: the other 27 chapters that lack a literal
"Historical Context:" label. They are book-opening pages that already carry the
same substance under more specific headings — 1 Corinthians 1 has "Corinth:",
Galatians 1 has "The Crisis:", Revelation 1 has "Setting:", Titus 1 has
"Crete:". Adding a generic field beside a specific one would be a downgrade.

Usage:
    python3 fix_joshua_context.py [--check]
"""
import os
import re
import sys

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")

CONTEXT = {
13: "The conquest narrative ends at chapter 12; from here Joshua turns from taking "
    "the land to dividing it. The opening verses are candid about unfinished "
    "business — Joshua is old, and substantial territory remains unconquered, "
    "including the Philistine coast and the Geshurite and Sidonian regions (vv.2-6). "
    "God's instruction is nonetheless to allot the land now, by faith, before it is "
    "fully possessed. The chapter then records the inheritance Moses had already "
    "assigned east of the Jordan to Reuben, Gad and half of Manasseh (vv.8-33), "
    "territory taken from Sihon and Og. A pointed note recurs: Levi received no land "
    "inheritance, because \u201cthe sacrifices of the LORD God of Israel are their "
    "inheritance\u201d (v.14). The tribe that served the tabernacle was to live off the "
    "offerings and among the other tribes rather than hold a territory of its own.",
14: "The allotment west of the Jordan begins, and Scripture pauses over one man before "
    "any tribal boundary is drawn. Caleb, now eighty-five, comes to Joshua at Gilgal to "
    "claim Hebron. Forty-five years earlier he and Joshua had been the only two of the "
    "twelve spies to urge Israel forward (Numbers 13-14), and Moses had promised him the "
    "land his feet had walked on. Caleb's speech is the theological centre of the chapter: "
    "three times he says he \u201cwholly followed the LORD\u201d, and he asks not for easy "
    "country but for the hill region still held by the Anakim, the giants that had "
    "frightened the other ten spies into unbelief. Hebron carried patriarchal weight too "
    "\u2014 Abraham, Isaac and Jacob were buried there. The generation that doubted died in "
    "the wilderness; the man who believed receives the very ground they feared.",
15: "Judah is allotted first and most fully, which reflects the tribe's standing rather "
    "than an accident of order: Jacob's blessing had said the sceptre would not depart "
    "from Judah (Genesis 49:10), and David and ultimately Christ would come from this "
    "line. The boundary description is long and precise, the language of a real land "
    "survey rather than a summary. Caleb's conquest of Hebron and Debir is recounted "
    "within Judah's territory, along with the account of his daughter Achsah asking for "
    "springs of water in the dry Negev \u2014 a small domestic scene that shows how "
    "seriously water rights mattered in that country. The chapter closes on an honest "
    "failure: Judah could not drive the Jebusites out of Jerusalem (v.63), a city that "
    "would remain in foreign hands until David took it some four centuries later.",
16: "Ephraim and the western half of Manasseh, the two tribes descended from Joseph, "
    "receive the fertile central highlands. Joseph's double portion, promised when Jacob "
    "adopted his two sons as his own (Genesis 48), is realised here as two distinct "
    "allotments. The territory is agriculturally rich and strategically central, and "
    "Shiloh, Shechem and Bethel all fall within or near it \u2014 which is why Ephraim "
    "would later dominate the northern kingdom and lend its name to it. As with Judah, "
    "the record ends in candour rather than triumph: the Canaanites in Gezer were not "
    "driven out but put to forced labour (v.10). Israel repeatedly chose accommodation "
    "over obedience, and Judges opens by tallying the cost.",
17: "The rest of Manasseh's inheritance is recorded, including the unusual case of the "
    "daughters of Zelophehad, who had no brothers and had successfully petitioned Moses "
    "for the right to inherit (Numbers 27:1-11); they receive their portion here, an "
    "early and concrete protection of women's property rights. The chapter then turns to "
    "complaint. Joseph's descendants say their allotment is too small, and Joshua's reply "
    "is blunt: if the hill country is not enough, clear the forest, and go up against the "
    "Canaanites with their iron chariots in the valleys. They admit the chariots "
    "frighten them (v.16). The land was sufficient; the will to take it was not. It is "
    "the same unbelief that kept their grandparents out of Canaan, surfacing again in a "
    "generation that had already seen the Jordan part.",
18: "Israel's camp moves from Gilgal to Shiloh, where the tabernacle is set up and will "
    "remain for roughly three centuries until the Philistines capture the ark (1 Samuel "
    "4). The move matters: worship is now centred in the land itself rather than at the "
    "point of entry. Seven tribes still have no inheritance, and Joshua's rebuke is "
    "striking \u2014 \u201cHow long are ye slack to go to possess the land?\u201d (v.3). "
    "Inaction, not opposition, is the obstacle. He commissions three men from each tribe "
    "to survey the remaining territory and describe it in writing, then casts lots before "
    "the LORD at Shiloh to divide it. Benjamin's portion is drawn first, a narrow strip "
    "between Judah and Ephraim that includes Jerusalem, Jericho and Bethel.",
19: "The remaining allotments are recorded: Simeon, whose towns lie inside Judah's "
    "territory, fulfilling Jacob's word that Simeon and Levi would be scattered in Israel "
    "(Genesis 49:7); then Zebulun, Issachar, Asher, Naphtali and Dan. Much of this land "
    "would become Galilee, where Jesus spent most of His ministry \u2014 Nazareth sat in "
    "Zebulun, and Isaiah's promise that Galilee of the nations would see a great light "
    "(Isaiah 9:1-2) attaches to these boundaries. Dan's portion proves too confined and "
    "the tribe later migrates north, an unsettled episode Judges 18 records without "
    "approval. The chapter ends with Joshua receiving his own inheritance last of all, "
    "Timnath-serah in Ephraim. The leader who apportioned the land to everyone else took "
    "his share only when the work was done.",
20: "The six cities of refuge are designated, three east of the Jordan and three west, "
    "spaced so that no one in Israel was more than a day's journey from one. The law "
    "behind them is in Numbers 35 and Deuteronomy 19: a person who killed accidentally "
    "could flee there and receive a hearing at the gate rather than be cut down by the "
    "victim's family. In a culture where blood vengeance was the norm and a kinsman "
    "redeemer was expected to avenge a death, this was a remarkable legal protection, "
    "distinguishing manslaughter from murder and requiring due process before either "
    "punishment or acquittal. The accused stayed until the death of the high priest, at "
    "which point he could return home free \u2014 a detail Christian readers have long "
    "connected to release secured through the death of a priest.",
21: "Forty-eight towns with their surrounding pasture are assigned to the Levites, "
    "distributed among every tribe rather than gathered in one place. The tribe that "
    "received no territory of its own is instead placed throughout the whole nation, so "
    "that priestly instruction was never more than a short walk away for any Israelite. "
    "Thirteen of the towns go to the priestly line of Aaron and sit within Judah, Simeon "
    "and Benjamin, close to where the temple would eventually stand. The six cities of "
    "refuge are among the forty-eight, which places the administration of that mercy in "
    "the hands of the Levites. The chapter closes with one of the strongest summary "
    "statements in the book: not one word of all the LORD's good promises to Israel had "
    "failed; everything came to pass (v.45).",
22: "The eastern tribes are released to go home, commended for keeping their word to "
    "fight alongside their brothers until the land was subdued (Numbers 32). On the way "
    "they build a large altar by the Jordan, and the western tribes mobilise for civil "
    "war, reading it as rival worship \u2014 a reasonable fear, since Deuteronomy 12 "
    "restricted sacrifice to the place the LORD would choose, and Israel had already been "
    "punished at Peor for exactly this kind of drift. Phinehas leads a delegation to ask "
    "before attacking, and the answer is that the altar is a witness, not a place of "
    "sacrifice \u2014 a monument declaring that the tribes across the river still belong "
    "to Israel and to the LORD. The crisis dissolves because someone asked a question "
    "before drawing a sword.",
23: "Joshua, \u201cold and stricken in age\u201d, gathers Israel's leaders for a farewell "
    "charge. The tone is not celebration but warning. He reminds them that the LORD has "
    "fought for them and that not one promise has failed, then presses the condition: "
    "love the LORD, cling to Him, do not intermarry with the remaining nations or adopt "
    "their gods. The unconquered peoples, he says, will become \u201csnares and traps\u201d "
    "and \u201cscourges in your sides\u201d if Israel makes peace with their worship (v.13). "
    "He is explicit that the same God who kept every good promise will also bring the "
    "threatened judgment. Judges reads as the record of this warning going unheeded, "
    "which makes chapter 23 the hinge between the conquest and the long decline.",
24: "Joshua assembles the tribes at Shechem, a site heavy with covenant memory: Abraham "
    "built his first altar in Canaan there, Jacob buried the foreign gods of his household "
    "there, and Joseph's bones are interred there at the chapter's end. Joshua rehearses "
    "Israel's history from Abraham's calling out of pagan Mesopotamia through the exodus "
    "and the conquest, framing all of it as God's initiative rather than Israel's "
    "achievement. Then he calls for decision \u2014 \u201cchoose you this day whom ye will "
    "serve\u201d \u2014 and declares his own household's allegiance regardless of theirs. "
    "When the people readily agree, Joshua challenges the ease of it: \u201cYe cannot serve "
    "the LORD\u201d (v.19), pushing them past sentiment to counted cost. A stone is set up "
    "as witness. Joshua dies at 110, and the book ends with three burials \u2014 Joshua, "
    "Joseph and Eleazar \u2014 closing the generation that entered the land.",
}


def main():
    check = "--check" in sys.argv
    changed = 0
    problems = []
    for ch, text_ctx in sorted(CONTEXT.items()):
        name = f"joshua{ch}.html"
        path = os.path.join(DOCS, name)
        if not os.path.isfile(path):
            problems.append(f"{name}: missing")
            continue
        html = open(path, encoding="utf-8").read()
        if "Historical Context:" in html:
            problems.append(f"{name}: already has Historical Context, skipped")
            continue

        # insert after the Purpose item, keeping the existing markup shape
        m = re.search(r'(<div class="auth-item"><span class="auth-label">Purpose:'
                      r'</span>.*?</div>)', html, re.S)
        if not m:
            problems.append(f"{name}: no Purpose item to anchor against")
            continue
        block = ('\n                    <div class="auth-item">'
                 '<span class="auth-label">Historical Context:</span> '
                 f'{text_ctx}</div>')
        new = html[:m.end(1)] + block + html[m.end(1):]

        o, c = len(re.findall(r"<div\b", new)), len(re.findall(r"</div>", new))
        if o != c:
            problems.append(f"{name}: would unbalance divs ({o} vs {c})")
            continue
        changed += 1
        if not check:
            open(path, "w", encoding="utf-8").write(new)

    verb = "would add" if check else "added"
    print(f"{verb} Historical Context to {changed} Joshua chapters")
    for p in problems:
        print(f"    {p}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
