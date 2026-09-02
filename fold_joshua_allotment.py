#!/usr/bin/env python3
"""
Completes Joshua: chapters 13 to 24, the allotment of the land and the farewells.

Clean input -- Author, Purpose and Historical Context on every page, no sublists, no
headless paragraphs, no fragment labels, no emphatic capitals. Sections are written
from the text.

Half of these chapters are boundary surveys. joshua15 is 63 verses of Judah's borders
and town lists, joshua19 is 51 of the remaining tribes, joshua21 is 45 of Levitical
cities. Those are sectioned by the survey's own divisions -- border, then region, then
town list -- because that is what the chapter is. Forcing narrative shape onto a land
register would misdescribe it.

Usage:
    python3 fold_joshua_allotment.py [--check]
"""
import os
import re
import sys

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")

ITEM = ('                    <div class="auth-item">'
        '<span class="auth-label">{label}</span> {body}</div>')

VERSES = {"joshua13": 33, "joshua14": 15, "joshua15": 63, "joshua16": 10,
          "joshua17": 18, "joshua18": 28, "joshua19": 51, "joshua20": 9,
          "joshua21": 45, "joshua22": 34, "joshua23": 16, "joshua24": 33}

CAPS_OK = {"LORD", "GOD", "YHWH", "OT", "NT", "BC", "AD", "KJV", "ESV", "ASV",
           "AM", "II"}

KEEP = ["Author:", "Purpose:", "Historical Context:"]

GENRE = "Historical Narrative \u2014 Land Allotment"

THEMES = {
"joshua13": "An old leader and a great deal of unconquered ground, land allotted by "
  "faith before it is held, the eastern tribes' inheritance recorded from Moses' day, "
  "and one tribe given no territory at all",
"joshua14": "A pause over one man before any boundary is drawn, forty-five years "
  "between a promise and its keeping, an eighty-five-year-old asking for hill country "
  "rather than easy land, and a phrase repeated three times",
"joshua15": "Judah allotted first and most fully, a boundary described like a survey "
  "rather than a summary, a daughter who asks for springs, town lists by region, and a "
  "city left unconquered in the last verse",
"joshua16": "Joseph's double portion realised as two allotments, the fertile central "
  "highlands, Shiloh and Shechem and Bethel inside the territory, and Canaanites left "
  "in place under tribute",
"joshua17": "Daughters who inherit because they asked and were granted, a tribe "
  "complaining its portion is too small, an answer that points at uncleared forest, and "
  "iron chariots offered as the reason it cannot be done",
"joshua18": "The tabernacle set up at Shiloh where it stayed three centuries, seven "
  "tribes still holding nothing, a rebuke about slackness rather than opposition, "
  "surveyors sent out to write a description, and Benjamin's small portion between "
  "Judah and Ephraim",
"joshua19": "Simeon's towns inside Judah's territory, the northern tribes that would "
  "become Galilee, Dan's portion and later migration, and Joshua receiving his own "
  "inheritance last of anyone",
"joshua20": "Six cities spaced so nobody was more than a day from one, a hearing at the "
  "gate instead of pursuit, protection that ends at the death of the high priest, and a "
  "distinction drawn between accident and intent",
"joshua21": "Forty-eight towns for the tribe with no territory, distributed through "
  "every other tribe rather than gathered, thirteen for the priestly line near where the "
  "temple would stand, and a summary that not one promise failed",
"joshua22": "Eastern tribes released after keeping their word, an altar built by the "
  "Jordan, nine tribes mustering for civil war, a delegation sent to ask before "
  "attacking, and an answer that satisfies everyone",
"joshua23": "A farewell that warns rather than celebrates, not one promise failed, "
  "intermarriage named as the danger, and remaining nations described as snares and "
  "scourges",
"joshua24": "A covenant renewal at Shechem where Abraham built an altar, history retold "
  "as God's initiative throughout, a choice put to the people, an answer Joshua tells "
  "them they cannot keep, and three burials to close the book",
}

SECTIONS = {
"joshua13": [
  ("Thou Art Old, and Much Land Remains (vv.1-7)",
   "The chapter opens candidly. Joshua is old and stricken in years, and God's first "
   "words to him name what has not been done -- the Philistine coast, the Geshurites, "
   "the Sidonians, all still unconquered. The instruction is nonetheless to divide the "
   "land now. Allotting territory that is not yet held is an act of faith rather than "
   "bookkeeping, and it sets the tone for a section that mixes achievement with unfinished "
   "business throughout."),
  ("The Eastern Allotment, and Levi's Portion (vv.8-14)",
   "The record turns back to what Moses had already given east of the Jordan, so the "
   "chapter is partly retrospective. Verse 14 states the exception that governs the whole "
   "book's arithmetic: to the tribe of Levi he gave none inheritance, the sacrifices of "
   "the LORD being their inheritance. One tribe is deliberately left landless, and "
   "chapter 21 explains how that worked in practice."),
  ("Reuben (vv.15-23)",
   "Reuben's territory is described by its towns and its southern boundary at the Arnon. "
   "The list includes Heshbon, once Sihon's city, and the passage recalls that Balaam the "
   "soothsayer was killed in the campaign -- a detail dropped into a land register. "
   "Reuben was the firstborn and receives a portion on the far side of the river, which "
   "the tribe had asked for in Numbers 32."),
  ("Gad (vv.24-28)",
   "Gad receives Jazer, Gilead, half the land of the children of Ammon, and territory "
   "running up to the Sea of Chinnereth -- Galilee. The boundaries are given by "
   "landmarks and towns rather than measurements, which is how ancient land descriptions "
   "worked and why some of these places can no longer be located with confidence."),
  ("Half Manasseh, and the LORD as Levi's Inheritance (vv.29-33)",
   "The eastern half of Manasseh gets Bashan and the towns of Jair. Then the chapter "
   "closes by repeating v.14 in different words: unto the tribe of Levi Moses gave not "
   "any inheritance, the LORD God of Israel was their inheritance. Stating it twice in "
   "one chapter makes it a theological point rather than an administrative footnote."),
],
"joshua14": [
  ("The Allotment Begins at Gilgal (vv.1-5)",
   "The western allotment is introduced with its procedure: by lot, through Eleazar the "
   "priest, Joshua, and the heads of the tribes. Casting lots removed human preference "
   "from the distribution, which mattered for a division nobody could later contest. The "
   "opening verses restate that Levi received no portion and that Joseph counted as two "
   "tribes."),
  ("Caleb: Forty-Five Years On (vv.6-12)",
   "Before a single boundary is drawn, Scripture pauses for one man. Caleb is eighty-five "
   "and comes to Gilgal to claim what Moses promised him forty-five years earlier, when "
   "he and Joshua alone of the twelve spies urged Israel forward. Three times in this "
   "speech he says he wholly followed the LORD. What he asks for is not easy land but the "
   "hill country where the Anakim are, and his stated reason is that the LORD will be "
   "with him. \u201cGive me this mountain\u201d is a request for the hardest available "
   "portion."),
  ("Hebron Given (vv.13-15)",
   "Joshua blesses him and gives him Hebron, and v.14 explains the grant in the same "
   "terms Caleb used: because he wholly followed the LORD God of Israel. The chapter's "
   "closing note that the land had rest from war sits oddly beside chapter 13's list of "
   "unconquered territory, and both are true -- organised warfare had ended while the "
   "possession had not."),
],
"joshua15": [
  ("Judah's Southern Border (vv.1-12)",
   "Judah is allotted first and at greatest length, which reflects standing rather than "
   "accident: Jacob's blessing had said the sceptre would not depart from Judah, and "
   "David and ultimately Christ came from this line. The boundary is traced landmark by "
   "landmark -- the Salt Sea, the ascent of Akrabbim, Kadesh-barnea, the river of Egypt. "
   "It reads like a survey document because that is what it is."),
  ("Caleb Takes Hebron and Debir (vv.13-19)",
   "Caleb's grant from chapter 14 is recorded inside Judah's territory, along with the "
   "campaign itself -- he drove out the three sons of Anak. Then Othniel takes Debir and "
   "wins Caleb's daughter Achsah. Her exchange with her father is the human moment in "
   "sixty-three verses of geography: given a field in a dry region, she asks for springs "
   "as well, and gets the upper and the nether."),
  ("Cities of the South (vv.20-32)",
   "The town lists begin, grouped by region, starting with the Negev toward the border of "
   "Edom. Twenty-nine cities are counted with their villages. The lists were legal "
   "records of who held what, which is why the totals are given -- a boundary description "
   "without a count would settle nothing."),
  ("The Lowland Cities (vv.33-47)",
   "The Shephelah and the coastal plain, including Lachish, Eglon and Ekron, with counts "
   "for each group. Some of these towns Judah held and some it did not, and the register "
   "makes no distinction -- which is part of the tension in these chapters between what "
   "was allotted and what was occupied."),
  ("The Hill Country and the Wilderness (vv.48-62)",
   "The mountain region and then the wilderness towns, including Ziph and Maon and "
   "En-gedi, places David would later hide in while fleeing Saul. The final group counts "
   "six cities in the wilderness. Bethlehem is absent from the Hebrew of this list and "
   "appears in some Greek copies, one of the small textual puzzles in the chapter."),
  ("Jerusalem Not Taken (v.63)",
   "The chapter ends on a failure recorded without comment: the children of Judah could "
   "not drive out the Jebusites, and they dwell with the children of Judah at Jerusalem "
   "unto this day. Sixty-two verses of successful allotment close on the one city that "
   "would matter most, still in other hands. David takes it in 2 Samuel 5, some four "
   "centuries later."),
],
"joshua16": [
  ("Joseph's Lot (vv.1-4)",
   "The children of Joseph receive the central highlands, and the double portion promised "
   "when Jacob adopted Ephraim and Manasseh as his own sons is realised here as two "
   "distinct allotments. The territory is agriculturally rich and centrally placed, which "
   "is why Ephraim would later dominate the northern kingdom and lend it its name in the "
   "prophets."),
  ("Ephraim's Border (vv.5-9)",
   "The boundary runs from Ataroth-addar past Beth-horon to the sea, with separate cities "
   "for Ephraim inside Manasseh's inheritance. Shiloh, Shechem and Bethel all fall within "
   "or close to this territory, so the religious centre of gravity sits here for the next "
   "three centuries."),
  ("The Canaanites of Gezer Remained (v.10)",
   "The chapter's last verse is another admission: they drove not out the Canaanites that "
   "dwelt in Gezer, and served under tribute. Taxing an enemy you were told to remove is "
   "a compromise that pays in the short term. Judges opens by listing exactly these "
   "arrangements as the reason for what follows."),
],
"joshua17": [
  ("Manasseh's Portion (vv.1-6)",
   "The western half of Manasseh is recorded, and the chapter pauses on the daughters of "
   "Zelophehad, who had no brothers and successfully petitioned Moses in Numbers 27 for "
   "the right to inherit. They receive their portion here among their father's brethren. "
   "It is an early and concrete protection of a woman's property right, settled by asking "
   "and granted on the merits."),
  ("The Border, and Towns Within Other Tribes (vv.7-13)",
   "The boundary runs from Asher to Michmethah and down to the brook Kanah, with certain "
   "towns belonging to Ephraim inside Manasseh's land and Manasseh holding towns inside "
   "Issachar and Asher. The interleaving is untidy and evidently real. Verses 12-13 add "
   "the familiar note: the Canaanites would dwell in that land, and were put to tribute "
   "rather than driven out."),
  ("Joseph's Complaint (vv.14-15)",
   "The children of Joseph come to Joshua saying their allotment is too small for so "
   "great a people. Joshua's reply is short and unsympathetic: if thou be a great people, "
   "get thee up to the wood country and cut down for thyself. The land they say they lack "
   "is available and uncleared."),
  ("Iron Chariots (vv.16-18)",
   "They press the point and name the real obstacle -- the Canaanites of the valley have "
   "chariots of iron. Joshua's answer concedes the difficulty and refuses the conclusion: "
   "thou art a great people and hast great power, thou shalt drive them out. The exchange "
   "is a small study in how a genuine obstacle becomes a reason not to try."),
],
"joshua18": [
  ("The Tabernacle Set Up at Shiloh (v.1)",
   "The camp moves from Gilgal, the point of entry, to Shiloh, and the tabernacle is set "
   "up there. It stays roughly three centuries until the Philistines capture the ark in 1 "
   "Samuel 4. Worship is now centred inside the land rather than at its edge, which is "
   "the quiet significance of a one-verse relocation."),
  ("How Long Are Ye Slack? (vv.2-10)",
   "Seven tribes still hold nothing, and Joshua's question names the problem precisely: "
   "how long are ye slack to go to possess the land? The obstacle is not opposition but "
   "inaction. His remedy is administrative -- three men from each tribe sent to walk the "
   "land and write a description of it, then lots cast at Shiloh before the LORD. Survey "
   "first, then allotment."),
  ("Benjamin's Border (vv.11-20)",
   "Benjamin's portion is small and sits between Judah and Ephraim, with Jerusalem on its "
   "southern boundary. The description runs by landmark -- the water of En-shemesh, the "
   "stone of Bohan, the ascent of Adummim. A small tribe placed between the two most "
   "powerful, which shapes a good deal of later Israelite politics."),
  ("Benjamin's Cities (vv.21-28)",
   "Twelve cities and then fourteen with their villages, including Jericho, Bethel, "
   "Gibeon, Ramah and Jebusi, which is Jerusalem. Saul's Gibeah is on the list. The "
   "territory is compact and contains a disproportionate number of places that matter "
   "later."),
],
"joshua19": [
  ("Simeon Within Judah (vv.1-9)",
   "Simeon's inheritance lies inside Judah's, because Judah's portion was too much for "
   "them. The arrangement fulfils Jacob's word in Genesis 49 that Simeon and Levi would "
   "be divided in Jacob and scattered in Israel -- a curse pronounced over the massacre "
   "at Shechem, worked out here as a tribe with towns but no separate territory."),
  ("Zebulun (vv.10-16)",
   "Zebulun's border is traced through Sarid, Chisloth-tabor and Japhia, twelve cities "
   "with their villages. Nazareth sits in this territory, though it is not named -- too "
   "small to appear in a register of this kind. Isaiah 9's promise that Galilee of the "
   "nations would see a great light attaches to these boundaries."),
  ("Issachar (vv.17-23)",
   "Issachar receives Jezreel, Shunem and Beth-shemesh among sixteen cities. The Jezreel "
   "valley is the most fertile ground in the country and the most fought over, which is "
   "why Megiddo nearby lends its name to Armageddon in Revelation."),
  ("Asher (vv.24-31)",
   "Asher's territory runs along the coast north to Tyre and Sidon, with twenty-two "
   "cities. Jacob's blessing had said Asher's bread would be fat -- coastal trade rather "
   "than farming. The tribe never fully dispossessed the Phoenician cities on its "
   "border."),
  ("Naphtali (vv.32-39)",
   "Naphtali takes the north-eastern hills and the western shore of the Sea of Galilee, "
   "nineteen cities including Hazor, Kedesh and Chinnereth. Capernaum lies in this "
   "territory, which means most of the Gospels' geography sits in the last three "
   "allotments recorded in this chapter."),
  ("Dan, and Joshua's Own Portion (vv.40-51)",
   "Dan's portion is small and coastal, including Zorah and Eshtaol, and Judges 18 "
   "records the tribe migrating north because it could not hold it -- v.47 already notes "
   "them taking Leshem and renaming it Dan. Then the chapter's last note: Joshua receives "
   "Timnath-serah, and he receives it last, after every tribe has been settled. The "
   "leader takes his portion when the work is finished."),
],
"joshua20": [
  ("Appoint You Cities of Refuge (vv.1-3)",
   "The law behind this chapter is in Numbers 35 and Deuteronomy 19, and its subject is "
   "the person who kills unawares and unwittingly. In a culture where blood vengeance was "
   "the norm and a kinsman was expected to avenge a death, the provision interrupts a "
   "cycle that would otherwise be automatic. The distinction it draws is between accident "
   "and intent."),
  ("A Hearing at the Gate (vv.4-6)",
   "The procedure is judicial rather than merely a sanctuary. The fugitive stands at the "
   "city gate and states his case to the elders, who take him in. He stays until he has "
   "stood before the congregation for judgment, and until the death of the high priest -- "
   "so the protection is temporary and tied to an office rather than to a sentence."),
  ("The Six Cities Named (vv.7-9)",
   "Three west of the Jordan -- Kedesh in Galilee, Shechem, Hebron -- and three east: "
   "Bezer, Ramoth in Gilead, Golan in Bashan. They are spaced so that no one in Israel "
   "was more than a day's journey from one, and v.9 extends the provision to the stranger "
   "sojourning among them. Access is designed rather than incidental."),
],
"joshua21": [
  ("The Levites Come to Claim (vv.1-3)",
   "The tribe given no territory comes to Eleazar and Joshua and asks for what the LORD "
   "commanded by Moses -- cities to dwell in with their suburbs for cattle. They ask "
   "last, after every other tribe has been settled, and they ask on the basis of a "
   "command rather than a claim to land."),
  ("The Lots Cast (vv.4-8)",
   "Lots are cast for four Levitical families, and the arithmetic is set out: thirteen "
   "cities for the priestly sons of Aaron out of Judah, Simeon and Benjamin, ten for the "
   "Kohathites, thirteen for the Gershonites, twelve for Merari. Forty-eight in total, "
   "drawn from every tribe."),
  ("The Priests' Thirteen Cities (vv.9-19)",
   "Aaron's line receives Hebron -- Caleb's city, with the fields around it still Caleb's "
   "-- along with Libnah, Debir and the rest. All thirteen sit in Judah, Simeon and "
   "Benjamin, which places the priesthood close to where the temple would eventually "
   "stand. The concentration is deliberate."),
  ("The Remaining Levitical Cities (vv.20-40)",
   "The other three Levitical families are distributed across Ephraim, Dan, Manasseh, "
   "Issachar, Asher, Naphtali, Zebulun, Reuben and Gad. Scattering the teaching tribe "
   "throughout the nation meant that instruction in the law was never more than a short "
   "walk away for any Israelite, which is the practical answer to their landlessness."),
  ("Not One Thing Failed (vv.41-45)",
   "The section closes with a summary that reaches back over nine chapters: the LORD gave "
   "them rest, there stood not a man of all their enemies before them, and there failed "
   "not ought of any good thing which the LORD had spoken. It is the high-water mark of "
   "the book, and it sits in the same volume as the repeated notes about Canaanites who "
   "were not driven out."),
],
"joshua22": [
  ("The Eastern Tribes Sent Home (vv.1-9)",
   "Reuben, Gad and half Manasseh are released and commended for keeping the promise they "
   "made in Numbers 32 -- to fight west of the Jordan until their brothers had rest before "
   "returning to their own land. Joshua's charge to them is about loyalty rather than "
   "territory, and they go home wealthy with spoil."),
  ("An Altar by the Jordan (vv.10-12)",
   "On the way they build a great altar by the river, and the western tribes gather at "
   "Shiloh to go to war. The reaction is not hysteria. Deuteronomy 12 restricted sacrifice "
   "to the place the LORD would choose, and Israel had already been punished at Peor for "
   "exactly this kind of drift, so a rival altar looked like the beginning of something "
   "they had seen before."),
  ("Phinehas Sent to Ask (vv.13-20)",
   "Before attacking, they send a delegation -- Phinehas the priest and ten princes. That "
   "step is the chapter's real subject. The speech they deliver cites Peor and the "
   "trespass of Achan as precedents for how one group's sin reaches the whole nation, and "
   "offers land west of the Jordan if the eastern tribes think their own is unclean."),
  ("A Witness, Not an Altar (vv.21-29)",
   "The answer is emphatic and specific: the altar was never for sacrifice. It was built "
   "as a witness between the tribes, in case the western tribes should one day tell their "
   "children the easterners had no part in the LORD. They were afraid of being "
   "disinherited by geography. God forbid that we should rebel, they say, and God forbid "
   "that we should build an altar for burnt offering."),
  ("It Pleased Them Well (vv.30-34)",
   "Phinehas is satisfied, reports back, and the war is called off. The children of "
   "Israel bless God, and the altar is named Ed -- a witness. A near-civil-war averted by "
   "sending someone to ask a question first, which the chapter presents as worth thirty "
   "verses."),
],
"joshua23": [
  ("The LORD Hath Fought for You (vv.1-5)",
   "Joshua is old and stricken in age and calls Israel's leaders for a farewell. He "
   "begins with what God has done -- ye have seen all that the LORD hath done, for the "
   "LORD your God is he that hath fought for you. The remaining nations are mentioned as "
   "still to be driven out, so the charge is given with the work unfinished rather than "
   "after it."),
  ("Cleave unto the LORD (vv.6-11)",
   "The instructions are specific: be very courageous to keep the law of Moses, turn not "
   "aside, make no mention of their gods, cleave unto the LORD. Verse 10 recalls that one "
   "man chased a thousand because God fought for them. Verse 11's \u201ctake good heed "
   "therefore unto yourselves that ye love the LORD\u201d makes love a matter of "
   "vigilance."),
  ("Snares and Scourges (vv.12-16)",
   "The warning is concrete about how failure would happen -- not invasion but marriage. "
   "If they make alliances with the remaining nations, those nations become snares and "
   "traps and scourges in their sides and thorns in their eyes. Then the point Joshua "
   "presses hardest: not one thing has failed of all the good God promised, and the same "
   "reliability applies to the warnings. The farewell ends on that symmetry rather than on "
   "encouragement."),
],
"joshua24": [
  ("Your Fathers Served Other Gods (vv.1-13)",
   "The assembly is at Shechem, a site thick with covenant memory -- Abraham built his "
   "first altar in Canaan there, and Jacob buried his household's foreign gods there. "
   "Joshua rehearses the history in God's own voice, and every verb belongs to God: I "
   "took your father Abraham, I sent Moses, I brought you out, I gave you a land for "
   "which ye did not labour. Verse 2's reminder that their fathers served other gods "
   "beyond the river is the least flattering possible opening."),
  ("Choose You This Day (vv.14-15)",
   "The demand follows from the history: fear the LORD and serve him in sincerity, and "
   "put away the gods your fathers served. Then the choice, and it is a real one -- if it "
   "seem evil unto you to serve the LORD, choose you this day whom ye will serve. Joshua's "
   "own position is stated without waiting for theirs: as for me and my house, we will "
   "serve the LORD."),
  ("Ye Cannot Serve the LORD (vv.16-24)",
   "The people answer well, and Joshua rejects the answer -- ye cannot serve the LORD, "
   "for he is an holy God, he is a jealous God. It is the most surprising exchange in the "
   "book. He is not fishing for enthusiasm; he is telling them the commitment is heavier "
   "than they think. They insist, he makes them witnesses against themselves, and only "
   "then does he accept it."),
  ("A Stone as Witness (vv.25-28)",
   "The covenant is made and written in the book of the law of God, and a great stone is "
   "set up under an oak as a witness -- it hath heard all the words of the LORD which he "
   "spake unto us. Physical objects standing in for memory recurs through Joshua, from "
   "the twelve stones at the Jordan to the altar called Ed."),
  ("Three Burials (vv.29-33)",
   "The book ends with three graves. Joshua dies at a hundred and ten and is buried in "
   "his own inheritance. Joseph's bones, carried out of Egypt and kept for the whole "
   "wilderness journey and the conquest, are finally buried at Shechem -- a promise from "
   "Genesis 50 kept several centuries late. And Eleazar the priest is buried in Ephraim. "
   "Verse 31 records that Israel served the LORD all the days of Joshua and of the elders "
   "who outlived him, which is precisely as long as it lasted."),
],
}

CAPS = re.compile(r"\b[A-Z]{2,}\b")


def main():
    check = "--check" in sys.argv
    problems, notes, planned = [], [], {}

    for page in sorted(VERSES, key=lambda s: int(s[6:])):
        path = os.path.join(DOCS, f"{page}.html")
        html = open(path, encoding="utf-8").read()
        pane = re.search(r'(id="tab-authorship">)(.*?)(?=<div class="tab-content")',
                         html, re.S)
        if not pane:
            problems.append(f"{page}: no authorship pane")
            continue

        fields, extra = {}, []
        for m in re.finditer(r'<div class="auth-item">(.*?)</div>', pane.group(2), re.S):
            inner = m.group(1)
            lab = re.match(r'<span class="auth-label">([^<]*)</span>\s*', inner)
            name = lab.group(1).strip() if lab else None
            rest = inner[lab.end():].strip() if lab else inner.strip()
            if name in KEEP:
                fields[name] = rest
            elif name is None:
                extra.append(rest)
            else:
                problems.append(f"{page}: unexpected field {name!r}")

        for want in KEEP:
            if want not in fields:
                problems.append(f"{page}: missing {want}")
        if extra:
            fields["Historical Context:"] = " ".join(
                [fields["Historical Context:"]] + extra).strip()
            notes.append(f"{page}: {len(extra)} headless paragraph(s) merged")

        sections = SECTIONS[page]
        covered = set()
        for label, text in [("Key Themes", THEMES[page])] + \
                           [(f"section {h!r}", p) for h, p in sections] + \
                           [(w, fields[w]) for w in KEEP]:
            stray = sorted({w for w in CAPS.findall(text) if w not in CAPS_OK})
            if stray:
                problems.append(f"{page}: capitals {stray} in {label}")
            if "*" in text:
                problems.append(f"{page}: markdown asterisk in {label}")
        for head, _ in sections:
            if "\u2013" in head:
                problems.append(f"{page}: en-dash in {head!r}")
            if not re.search(r"\(vv?\.[\d]+[a-z]?(?:[-,:\s]+[\d]+[a-z]?)*\)$", head):
                problems.append(f"{page}: {head!r} does not end with its verse range")
            for m in re.finditer(r"\(vv?\.\s*(\d+)[a-z]?(?:\s*-\s*(\d+)[a-z]?)?\)", head):
                a, z = int(m.group(1)), int(m.group(2) or m.group(1))
                if z > VERSES[page]:
                    problems.append(f"{page}: {head!r} exceeds {VERSES[page]}")
                rng = set(range(a, z + 1))
                if rng & covered:
                    problems.append(f"{page}: {head!r} overlaps at {sorted(rng & covered)}")
                covered |= rng
        gaps = sorted(set(range(1, VERSES[page] + 1)) - covered)
        if gaps:
            problems.append(f"{page}: verses uncovered: {gaps}")

        parts = ["\n                <h3>Authorship &amp; Background</h3>\n"]
        parts.append(ITEM.format(label="Author:", body=fields["Author:"]) + "\n")
        parts.append(ITEM.format(label="Classification:", body=GENRE) + "\n")
        parts.append(ITEM.format(label="Key Themes:", body=THEMES[page]) + "\n")
        parts.append(ITEM.format(label="Purpose:", body=fields["Purpose:"]) + "\n")
        parts.append(ITEM.format(label="Historical Context:",
                                 body=fields["Historical Context:"]) + "\n")
        for head, prose in sections:
            parts.append(ITEM.format(label=head + ":", body=prose) + "\n")
        new_body = "".join(parts) + "            </div>\n\n            "

        new = html[:pane.start(2)] + new_body + html[pane.end(2):]
        o, c = len(re.findall(r"<div\b", new)), len(re.findall(r"</div>", new))
        if o != c:
            problems.append(f"{page}: div imbalance {o} vs {c}")
            continue
        planned[path] = new

    for n in notes:
        print(f"    note: {n}")
    if problems:
        print(f"refusing to write, {len(problems)} problem(s)")
        for p in problems:
            print(f"    {p}")
        return 1
    if not check:
        for path, new in planned.items():
            open(path, "w", encoding="utf-8").write(new)
    print(f"{'would fold' if check else 'folded'} {len(planned)} chapters")
    return 0


if __name__ == "__main__":
    sys.exit(main())
