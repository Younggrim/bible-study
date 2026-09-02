#!/usr/bin/env python3
"""
Completes Exodus: chapters 31 to 40, the last ten.

These pages carry a "Section Summaries:" field rather than a Structure: sublist --
the same information in a different container:

    vv.1-11 - Bezalel and Oholiab appointed; Spirit-given skill for tabernacle work.
    vv.12-17 - The Sabbath command reiterated as a perpetual covenant sign.
    v.18 - God gives Moses the two tablets of stone.

That is a skeleton, so the divisions are taken from it and the summaries expanded
into exposition. The field is then dropped, the same treatment Structure: gets. Note
it uses en-dashes throughout where the site convention is a hyphen, so the section
labels are rewritten with hyphens.

HOLINESS is added to the capitals allow-list. Exodus 39:30 engraves "HOLINESS to the
LORD" on the high priest's golden plate, and the KJV sets it in capitals because it
is an inscription. Fifth protected case, after PE and AYIN, I AM, Jeroboam II, and
MENE TEKEL UPHARSIN.

exodus31 gets three sections rather than the usual four for a chapter under twenty
verses. It has three units -- craftsmen, Sabbath, tablets -- and inventing a fourth
would mean a division the chapter does not have.

Usage:
    python3 fold_exodus_tabernacle.py [--check]
"""
import os
import re
import sys

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")

ITEM = ('                    <div class="auth-item">'
        '<span class="auth-label">{label}</span> {body}</div>')

VERSES = {"exodus31": 18, "exodus32": 35, "exodus33": 23, "exodus34": 35,
          "exodus35": 35, "exodus36": 38, "exodus37": 29, "exodus38": 31,
          "exodus39": 43, "exodus40": 38}

CAPS_OK = {"LORD", "GOD", "YHWH", "OT", "NT", "BC", "AD", "KJV", "ESV", "ASV",
           "AM", "II", "HOLINESS"}

KEEP = ["Author:", "Historical Context:"]

# Dropped: superseded by the sections, exactly as Structure: is.
DROP_ALWAYS = ["Section Summaries:"]

DROP = {
    "exodus32": ["The timing is devastating:"],
    "exodus33": ["The chapter reveals three movements:"],
    "exodus38": ["The materials inventory (vv.21\u201331) is remarkable:"],
    "exodus40": ["The climax comes in verses 34\u201338:"],
}

GENRE = "Law and Narrative \u2014 Tabernacle Construction"

THEMES = {
"exodus31": "The first man in Scripture said to be filled with the Spirit, and filled "
  "for craftsmanship rather than prophecy, the Sabbath set as a limit on even holy "
  "work, and tablets written with the finger of God",
"exodus32": "A covenant broken within weeks of being made, a leader who blames the "
  "people he led, tablets shattered deliberately, an intercession that appeals to God's "
  "reputation rather than Israel's merit, and a mediator offering to be blotted out",
"exodus33": "An offer of an angel instead of God's own presence, a leader who refuses "
  "to move without it, conversation described as between friends, and a request to see "
  "glory answered by a hand over a cleft in the rock",
"exodus34": "New tablets cut by human hands, the self-description of God most quoted "
  "inside the Old Testament itself, a covenant renewed with the same terms that were "
  "broken, and a face that shone and had to be veiled",
"exodus35": "The Sabbath stated before the building begins, offerings taken only from "
  "willing hearts, skill named as a gift rather than a qualification, and craftsmen "
  "announced publicly to the people who will fund them",
"exodus36": "Giving that had to be stopped by proclamation, curtains counted and "
  "measured, frames and bases and bars itemised, and a veil that divides what the rest "
  "of the structure exists to house",
"exodus37": "Furnishings made in the order of their nearness to God, gold beaten rather "
  "than cast, a lampstand from a single talent, and anointing oil and incense prepared "
  "last",
"exodus38": "The altar a worshipper met before anything else, a laver made from donated "
  "mirrors, a courtyard that marks a boundary, accounts published rather than assumed, "
  "and silver traceable to a census of 603,550 men",
"exodus39": "Garments that state doctrine rather than merely cover, twelve names carried "
  "on the shoulders and twelve stones over the heart, an inscription reading HOLINESS to "
  "the LORD, and a completion described in the language of Genesis",
"exodus40": "A tabernacle raised on the first day of the second year, every item placed "
  "as commanded, obedience recorded eight times in one chapter, a cloud that settles, and "
  "a glory so full that even Moses cannot enter",
}

SECTIONS = {
"exodus31": [
  ("Bezalel and Oholiab Appointed (vv.1-11)",
   "After six chapters of blueprints, God names the builders. Bezalel is the first "
   "person in Scripture explicitly said to be filled with the Spirit of God, and the "
   "filling is for cutting stones, working gold and carving timber -- not for prophecy "
   "or leadership. That the Spirit's first named work is craftsmanship establishes "
   "something about ordinary vocations that the rest of Scripture assumes. Oholiab is "
   "given as his partner, and wisdom is put into the hearts of all the skilled workers."),
  ("The Sabbath Reiterated (vv.12-17)",
   "The Sabbath command is placed deliberately between the instructions and the "
   "construction, and it functions as a limit: even building God's dwelling does not "
   "override God's rest. It is called a sign between God and Israel throughout their "
   "generations, and the penalty attached is severe. Verse 17's reason reaches back to "
   "creation -- in six days the LORD made heaven and earth, and on the seventh he "
   "rested and was refreshed."),
  ("The Two Tablets of Stone (v.18)",
   "One verse ends the section that began at chapter 25: God gives Moses two tables of "
   "testimony, tables of stone, written with the finger of God. It is a moment of "
   "completion, and the placement is devastating in hindsight. While this is being "
   "handed over on the mountain, chapter 32 is already happening at its foot."),
],
"exodus32": [
  ("The Golden Calf (vv.1-6)",
   "Moses has been on the mountain forty days and the people's patience runs out. Their "
   "demand is not for a different god but for something visible -- make us gods which "
   "shall go before us -- and Aaron complies without recorded resistance. The calf was "
   "likely shaped by Egyptian bull worship, which shows how much of Egypt had come out "
   "with them. The timing is the worst part: they had entered the covenant in chapter "
   "24, heard God's voice and agreed to obey, and break the first two commandments "
   "within weeks."),
  ("Moses Intercedes (vv.7-14)",
   "God tells Moses to go down, calls them \u201cthy people, which thou broughtest out "
   "of Egypt\u201d, and proposes to consume them and make a great nation of Moses "
   "instead. The prayer that follows appeals to nothing in Israel. Moses argues from "
   "God's reputation among the Egyptians and from the promises sworn to Abraham, Isaac "
   "and Jacob. Verse 14 records that the LORD repented of the evil he thought to do, "
   "which the text states without softening."),
  ("The Tablets Broken (vv.15-20)",
   "Moses comes down carrying tablets written on both sides by God himself, hears the "
   "singing, and throws them down at the foot of the mountain. Breaking them is not "
   "temper but statement -- the covenant document is destroyed because the covenant has "
   "been. He burns the calf, grinds it to powder, scatters it on water and makes them "
   "drink it, so they consume what they made."),
  ("Aaron's Excuse (vv.21-24)",
   "The exchange is one of the least flattering passages in Scripture about a leader. "
   "Aaron blames the people, blames Moses's absence, and then describes the casting of "
   "the calf as something that happened to him: I cast it into the fire, and there came "
   "out this calf. He does not lie about the facts so much as remove himself from them."),
  ("The Levites Execute Judgment (vv.25-29)",
   "Moses stands in the gate and asks who is on the LORD's side, and the sons of Levi "
   "gather to him. About three thousand die. The passage is hard and the text offers no "
   "commentary on it, only the outcome -- the Levites are said to have consecrated "
   "themselves that day, which is how the tribe's later priestly role is grounded."),
  ("I Will Make Atonement (vv.30-35)",
   "Moses returns up the mountain saying peradventure I shall make an atonement for "
   "your sin, and what he offers is himself: blot me, I pray thee, out of thy book which "
   "thou hast written. The offer is refused -- each will answer for his own sin -- but "
   "it stands as the clearest picture in Exodus of a mediator willing to bear the cost. "
   "A plague follows, and the chapter closes without resolution."),
],
"exodus33": [
  ("An Angel Instead of My Presence (vv.1-6)",
   "God promises the land and an angel to drive out its inhabitants, and then withholds "
   "the one thing that mattered: I will not go up in the midst of thee, lest I consume "
   "thee. The offer is everything except himself. The people mourn and strip off their "
   "ornaments, which is the first sign in the book of grief over the right thing."),
  ("Face to Face, as a Man Speaketh unto His Friend (vv.7-11)",
   "The tent of meeting is pitched outside the camp, and the distance is the point -- "
   "God is accessible but no longer in the middle. When Moses goes out the people stand "
   "at their tent doors and watch, and worship. The description of the conversation is "
   "the most intimate phrase in the Pentateuch: the LORD spake unto Moses face to face, "
   "as a man speaketh unto his friend."),
  ("If Thy Presence Go Not (vv.12-17)",
   "Moses presses the point the chapter turns on. He will not move the nation forward "
   "on the strength of a promise of land: if thy presence go not with me, carry us not "
   "up hence. His argument is that presence is the only thing distinguishing Israel from "
   "every other people, not numbers or strength or territory. God agrees, and the "
   "agreement is granted on the ground that Moses has found grace and is known by name."),
  ("Shew Me Thy Glory (vv.18-23)",
   "Four words that are the deepest request in the book, and the answer holds "
   "accessibility and transcendence together. God will make his goodness pass by and "
   "proclaim his name, but no man shall see his face and live. So Moses is put in a "
   "cleft of the rock with God's hand over him until he has passed by, and sees only his "
   "back. Protection is what makes the encounter survivable."),
],
"exodus34": [
  ("New Tablets Cut (vv.1-4)",
   "The first tablets were made by God and written by God. These Moses must cut himself, "
   "though God still writes on them -- a small difference that says something about "
   "restoration after failure costing the offender something. He goes up alone, early in "
   "the morning, with no one and nothing else allowed on the mountain."),
  ("The LORD Proclaims His Name (vv.5-9)",
   "This is the most quoted passage within the Old Testament itself, echoed in Numbers "
   "14, Nehemiah 9, Psalm 86, Psalm 103, Joel 2 and Jonah 4. The LORD, the LORD God, "
   "merciful and gracious, longsuffering, abundant in goodness and truth, forgiving "
   "iniquity -- and then, without a pause, that will by no means clear the guilty. Mercy "
   "and justice are stated as one self-description rather than two. Moses's response is "
   "to bow his head and worship."),
  ("The Covenant Renewed (vv.10-26)",
   "The terms given are largely the same ones just broken: no covenant with the "
   "inhabitants of the land, no molten gods, the feasts kept, the firstborn redeemed, "
   "the Sabbath observed. Nothing is relaxed because of chapter 32. The renewal is a "
   "restoration to the same obligations rather than a lighter arrangement, which is its "
   "own kind of grace."),
  ("Forty Days Without Bread or Water (vv.27-28)",
   "Moses writes the words and remains forty days and forty nights, neither eating bread "
   "nor drinking water, while God writes the ten commandments on the tablets. It is his "
   "second such fast in the book, the first having ended with the calf waiting for him "
   "below."),
  ("His Face Shone (vv.29-35)",
   "Moses comes down not knowing that his face shines, which is the detail that makes "
   "it credible -- the glory is reflected rather than possessed. The people are afraid "
   "to come near, so he veils himself, unveiling only to speak with God and to deliver "
   "God's words. Paul takes up the image in 2 Corinthians 3, reading the veil as "
   "concealing a fading brightness."),
],
"exodus35": [
  ("The Sabbath First (vv.1-3)",
   "Before a single instruction about building is repeated, the Sabbath is restated with "
   "one addition -- kindle no fire in your dwellings on the sabbath day. Placing it here, "
   "at the head of the construction narrative rather than buried in it, repeats the "
   "guardrail of chapter 31. The work about to begin is holy and still does not override "
   "rest."),
  ("A Willing Heart (vv.4-19)",
   "The offering is defined by disposition rather than amount: whosoever is of a willing "
   "heart. Then the materials are itemised, gold through badgers' skins through oil and "
   "spices, followed by the list of everything to be made. Nothing is levied. A "
   "structure costing this much is funded entirely by people who choose to give."),
  ("The People Respond (vv.20-29)",
   "The response is described at unusual length, and its character matters: they came, "
   "every one whose heart stirred him up, and brought bracelets, earrings, rings and "
   "tablets of gold. Women spun with their hands and brought what they had made. Verse "
   "29 sums it up as a willing offering, and the emphasis on willingness across ten "
   "verses is the chapter's answer to the compulsion of the golden calf collection."),
  ("Bezalel and Oholiab Announced (vv.30-35)",
   "What God told Moses privately in chapter 31 is now announced publicly to the people "
   "who have just funded the work. The description of the gift is expansive -- wisdom, "
   "understanding, knowledge, and all manner of workmanship -- and it ends by saying God "
   "has put it in their hearts to teach. The skill is not only to be used but "
   "transmitted."),
],
"exodus36": [
  ("Too Much Giving (vv.1-7)",
   "The one construction problem recorded in the book is a surplus. The craftsmen report "
   "that the people bring much more than enough, and Moses issues a proclamation to make "
   "them stop. It is the only instance in Scripture of an offering being closed for "
   "excess, and it comes from the same people who weeks earlier melted their jewellery "
   "into an idol."),
  ("Ten Curtains of Fine Linen (vv.8-13)",
   "The measurements are given exactly as instructed, cubit for cubit, with cherubim "
   "worked into the linen and fifty loops joined by fifty gold clasps. The repetition of "
   "chapter 26 is the point of these chapters: instruction and execution are reported "
   "in near-identical language so the correspondence can be checked."),
  ("Goat Hair and Rams' Skins (vv.14-19)",
   "Three further coverings go over the linen -- goats' hair, rams' skins dyed red, and "
   "badgers' skins. The layering runs from beautiful inside to weatherproof outside, so "
   "what a passer-by saw was the plainest material and what a priest saw was the "
   "finest."),
  ("Frames, Bases and Bars (vv.20-34)",
   "The structural work: boards of acacia overlaid with gold, standing in sockets of "
   "silver, held by bars running through gold rings. The silver bases are the heaviest "
   "single use of metal in the tabernacle, and chapter 38 will trace them to the census "
   "tax. The whole thing is designed to be taken apart and carried."),
  ("The Veil and the Screen (vv.35-38)",
   "Two hangings close the chapter, and their difference is the theology of the "
   "building. The veil, with cherubim, divides the most holy place from the holy. The "
   "screen at the entrance separates the courtyard from the holy place. Access is "
   "graded, and the innermost division is the one with guardians woven into it."),
],
"exodus37": [
  ("The Ark of the Covenant (vv.1-5)",
   "The furnishings are made in order of nearness to God, and so the ark comes first. "
   "Acacia wood overlaid with gold inside and out, with a crown of gold and rings and "
   "staves for carrying. Bezalel makes it himself, which the text specifies. It is the "
   "only object in the tabernacle that holds anything -- the testimony."),
  ("The Mercy Seat (vv.6-9)",
   "The lid is made separately and described separately: pure gold, with two cherubim of "
   "beaten work at either end, wings stretched forward and faces toward the mercy seat. "
   "Beaten rather than cast, so the figures are of one piece with the lid. Whatever "
   "happened above it happened between them and over the law inside."),
  ("The Table of Showbread (vv.10-16)",
   "Acacia overlaid with gold, with a border, a crown, rings and staves, and vessels of "
   "pure gold -- dishes, spoons, bowls and covers. Bread was set on it continually. Of "
   "the three items in the holy place this is the one whose function is a meal, and it "
   "stood on the north side."),
  ("The Golden Lampstand (vv.17-24)",
   "Beaten out of one talent of pure gold -- roughly seventy-five pounds -- with a "
   "shaft, six branches, and almond-shaped bowls, knops and flowers. Hammered from a "
   "single piece rather than assembled from parts, which is why the weight is specified "
   "rather than the dimensions. It stood opposite the table and was the only light in "
   "the holy place."),
  ("The Altar of Incense (vv.25-28)",
   "Small, square, acacia overlaid with gold, with horns, a crown, rings and staves. It "
   "stood before the veil, closer to the most holy place than anything else in the holy "
   "place, and what was offered on it was smoke rather than flesh."),
  ("The Anointing Oil and the Incense (v.29)",
   "One verse for the last items, made by the art of the apothecary: the holy anointing "
   "oil and the pure incense of spices. They are consumables rather than furniture, and "
   "chapter 30 forbids either recipe being reproduced for ordinary use. What made the "
   "objects holy could not be bought."),
],
"exodus38": [
  ("The Bronze Altar (vv.1-7)",
   "The chapter moves outdoors and the metal changes from gold to bronze. The altar of "
   "burnt offering is the first thing a worshipper met on entering the courtyard, which "
   "is the point of its position -- before approach comes sacrifice. Acacia overlaid with "
   "bronze, hollow, with horns, a grate and rings, and it too was made to be carried."),
  ("The Laver from Women's Mirrors (v.8)",
   "One verse, and the material is the interesting part. The bronze laver was made from "
   "the mirrors of the women who assembled at the door of the tent. Polished bronze "
   "mirrors were personal and valuable, and what was given up for seeing oneself became "
   "the basin priests washed in before service."),
  ("The Courtyard (vv.9-20)",
   "Hangings of fine linen on pillars with bronze bases and silver hooks, a hundred "
   "cubits by fifty, with a screened gate. The courtyard defines a boundary rather than "
   "housing anything, and its function is to mark where the ordinary stops. Even the "
   "pins are recorded as bronze."),
  ("Record-Keeping (vv.21-23)",
   "The text pauses to name who is accountable: this is the sum, as it was counted, by "
   "the hand of Ithamar. Bezalel and Oholiab are named again with their tribes and their "
   "skills. Publishing who did the work and who counted it is a small thing that the "
   "chapter treats as worth the verses."),
  ("The Materials Inventory (vv.24-31)",
   "The totals are given precisely: 29 talents and 730 shekels of gold, about 2,200 "
   "pounds; 100 talents and 1,775 shekels of silver, about 7,500 pounds; 70 talents and "
   "2,400 shekels of bronze, about 5,300 pounds. The silver's source is stated -- the "
   "half shekel from each of 603,550 men at the census -- and it was cast into the "
   "sockets the whole structure stood in. The foundations of the building were literally "
   "the redemption money of the people who lived around it."),
],
"exodus39": [
  ("The Ephod (vv.1-7)",
   "The priestly garments are made with the same precision as the structure, and the "
   "refrain \u201cas the LORD commanded Moses\u201d runs through the chapter. Gold is "
   "beaten into thin plates and cut into wires to be worked into the blue, purple, "
   "scarlet and linen. Two onyx stones on the shoulders carry the names of the twelve "
   "tribes, so the high priest bore the nation on his shoulders whenever he served."),
  ("The Breastplate (vv.8-21)",
   "Twelve stones in four rows, each engraved with a tribal name, set in gold and bound "
   "to the ephod with chains and rings and a lace of blue. Where the shoulder stones "
   "carried the tribes as a weight, these carried them over the heart. The two placements "
   "together say what the office was for."),
  ("The Robe of the Ephod (vv.22-26)",
   "Woven blue, with an opening bound so it would not tear, and around its hem "
   "pomegranates of blue, purple and scarlet alternating with bells of pure gold. The "
   "bells meant the high priest was audible while he moved in the holy place. Fruit and "
   "sound around the hem of a garment nobody outside would see closely."),
  ("Tunics, Turban and Sash (vv.27-29)",
   "The remaining garments are listed plainly: coats of fine linen, the turban, the "
   "caps, the linen breeches and the embroidered sash. These clothe the ordinary priests "
   "as well as Aaron, and their plainness against the ephod's colour marks the "
   "difference in office without disparaging it."),
  ("HOLINESS to the LORD (vv.30-31)",
   "The golden plate for the turban is engraved with the words HOLINESS to the LORD, "
   "set in capitals in the King James text because it is an inscription. It was tied "
   "with a blue lace to the front of the mitre, so the first thing legible on the man "
   "who entered God's presence was a statement of what that presence required."),
  ("All the Work Finished (vv.32-43)",
   "Everything is brought to Moses and itemised again, and then he looks it over and "
   "blesses them. The language is deliberately that of Genesis: God saw everything he "
   "had made and it was very good; Moses looked upon all the work and blessed them. The "
   "tabernacle is being presented as a small creation, a place where God will dwell with "
   "people, and the echo is the chapter's closing argument."),
],
"exodus40": [
  ("Set Up the Tabernacle (vv.1-8)",
   "God gives the order of assembly, item by item, and the sequence runs from the most "
   "holy outward: the ark and the veil, then the table and lampstand and incense altar, "
   "then the burnt offering altar and the laver, then the courtyard. The building is put "
   "up from the centre out, which is how it was designed and how it is described."),
  ("Anointing and Consecrating (vv.9-11)",
   "The oil is applied to the tabernacle and everything in it, and the objects are said "
   "to become holy by it. The altar is described as most holy. Nothing about the "
   "materials made them so -- gold and acacia are ordinary until designated -- and the "
   "distinction is conferred rather than intrinsic."),
  ("Aaron and His Sons (vv.12-15)",
   "The priests are washed, clothed and anointed, in that order. The anointing is said "
   "to be for an everlasting priesthood throughout their generations, which is stated "
   "here without qualification and is the arrangement Hebrews will later argue has been "
   "superseded. Aaron is the same man who made the calf eight chapters ago."),
  ("Moses Raises It Up (vv.16-33)",
   "Moses erects it personally on the first day of the first month of the second year, "
   "nearly a year after leaving Egypt. The phrase \u201cas the LORD commanded Moses\u201d "
   "appears eight times in this chapter and around fifteen across chapters 39 and 40. "
   "The repetition is a drumbeat, and it is the deliberate answer to chapter 32 -- the "
   "book's last long passage is about a man doing exactly what he was told, item by "
   "item, until the work is finished."),
  ("The Cloud Covers the Tent (vv.34-38)",
   "The cloud covers the tent and the glory of the LORD fills the tabernacle, so full "
   "that even Moses cannot enter. It is the fulfilment of 25:8 -- let them make me a "
   "sanctuary, that I may dwell among them. The book that opened with slaves crying out "
   "in Egypt ends not in the promised land but with God resident among them, the cloud "
   "settling when they were to stay and lifting when they were to move. Presence rather "
   "than arrival is where Exodus chooses to stop."),
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

        want_drop = DROP_ALWAYS + DROP.get(page, [])
        fields, dropped, extra = {}, [], []
        for m in re.finditer(r'<div class="auth-item">(.*?)</div>', pane.group(2), re.S):
            inner = m.group(1)
            lab = re.match(r'<span class="auth-label">([^<]*)</span>\s*', inner)
            name = lab.group(1).strip() if lab else None
            rest = inner[lab.end():].strip() if lab else inner.strip()
            if name in KEEP:
                fields[name] = rest
            elif name is not None and name in want_drop:
                dropped.append(name)
            elif name is None:
                extra.append(rest)
            else:
                problems.append(f"{page}: unexpected field {name!r}")

        for want in KEEP:
            if want not in fields:
                problems.append(f"{page}: missing {want}")
        for want in want_drop:
            if want not in dropped:
                problems.append(f"{page}: expected to drop {want!r}, not found")
        if extra:
            fields["Historical Context:"] = " ".join(
                [fields["Historical Context:"]] + extra).strip()
            notes.append(f"{page}: {len(extra)} headless paragraph(s) merged")
        notes.append(f"{page}: dropped {len(dropped)} superseded field(s)")

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
                problems.append(f"{page}: en-dash in {head!r}, use a hyphen")
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
