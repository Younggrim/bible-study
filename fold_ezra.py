#!/usr/bin/env python3
"""
Completes Ezra: all ten chapters.

The cleanest input of any book so far -- only Author and Historical Context on every
page, no sublists, no headless paragraphs, no fragment labels, no emphatic capitals.
Sections are written from the text.

Two chapters are largely lists: ezra2 is a 70-verse register of returnees and
ezra10 ends with 113 names. Those are sectioned by the register's own organising
principle rather than by narrative, since that is what the chapter is.

Usage:
    python3 fold_ezra.py [--check]
"""
import os
import re
import sys

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")

ITEM = ('                    <div class="auth-item">'
        '<span class="auth-label">{label}</span> {body}</div>')

VERSES = {"ezra1": 11, "ezra2": 70, "ezra3": 13, "ezra4": 24, "ezra5": 17,
          "ezra6": 22, "ezra7": 28, "ezra8": 36, "ezra9": 15, "ezra10": 44}

CAPS_OK = {"LORD", "GOD", "YHWH", "OT", "NT", "BC", "AD", "KJV", "ESV", "ASV",
           "AM", "II"}

KEEP = ["Author:", "Historical Context:"]

GENRE = "Historical Narrative \u2014 Post-Exilic"

THEMES = {
"ezra1": "Jeremiah's seventy years reaching their term, a pagan emperor's spirit "
  "stirred to issue the decree, willing returnees rather than conscripts, and stolen "
  "vessels handed back by the hands that held them",
"ezra2": "A register kept by name and family, organisation by clan and then by town, "
  "a shortage of Levites that will recur, those unable to prove their descent, and "
  "giving offered before anything is built",
"ezra3": "An altar rebuilt before any walls or houses, the festival calendar restored "
  "before the building exists, cedar fetched from Lebanon as Solomon had, and weeping "
  "and shouting that could not be told apart",
"ezra4": "An offer of partnership refused on theological rather than ethnic grounds, "
  "hands deliberately weakened, true facts assembled into a misleading letter, and "
  "sixteen years of silence",
"ezra5": "Two prophets restarting what politics had stopped, a governor's enquiry that "
  "turns into vindication, an unusually fair official report, and elders who name their "
  "fathers' sin as part of their defence",
"ezra6": "A decree found in the wrong archive, a hostile enquiry producing state "
  "funding, a temple finished seventy years after its destruction, twelve goats for "
  "twelve tribes when only two had returned, and a Passover kept",
"ezra7": "A genealogy traced to Aaron, a scribe who studied and did and then taught, "
  "royal authority granted beyond anything asked for, the hand of God named three "
  "times as the explanation, and a response that is doxology rather than triumph",
"ezra8": "A nine-hundred-mile journey with no escort, Levites recruited because none "
  "had volunteered, a fast called because asking for soldiers would contradict a public "
  "testimony, and treasure weighed out in front of witnesses",
"ezra9": "Intermarriage found among the leaders first, a prohibition about covenant "
  "loyalty rather than ancestry, a prayer that identifies with sin it did not commit, "
  "and a confession that asks for nothing",
"ezra10": "A remedy proposed by the people rather than imposed, a covenant made in the "
  "rain, cases examined one at a time over three months, 113 names recorded, and a book "
  "that stops without a conclusion",
}

SECTIONS = {
"ezra1": [
  ("Jeremiah's Seventy Years Fulfilled (vv.1-2)",
   "The book opens by tying a political event to a prophecy: in the first year of Cyrus, "
   "that the word of the LORD by Jeremiah might be fulfilled. Jeremiah 25:11-12 and "
   "29:10 had set the exile at seventy years, and Cyrus took Babylon in 539 BC. The "
   "explanation given is not diplomatic calculation but that the LORD stirred up the "
   "spirit of Cyrus, and the decree that follows is quoted in the king's own voice "
   "crediting the God of heaven."),
  ("Cyrus's Proclamation (vv.3-4)",
   "The terms are generous and specific: whoever is willing may go up to build the "
   "house of the LORD in Jerusalem, and those who stay are to help with silver, gold, "
   "goods and beasts. Persian policy did favour restoring displaced peoples and their "
   "temples, which is documented outside Scripture, so the decree fits the empire's "
   "practice. The book's claim is about who moved the policy rather than whether it was "
   "characteristic."),
  ("Those Whose Spirit God Had Raised (vv.5-6)",
   "The response is voluntary and comes from Judah, Benjamin, the priests and the "
   "Levites -- and again the wording is that God raised their spirit. The same verb is "
   "used of Cyrus, which sets emperor and returnee under the same action. Their "
   "neighbours strengthen their hands with vessels of silver and gold, an echo of Israel "
   "leaving Egypt with the goods of their neighbours."),
  ("Five Thousand Four Hundred Vessels (vv.7-11)",
   "Cyrus brings out the temple vessels Nebuchadnezzar had taken and put in the house of "
   "his gods, and they are counted -- five thousand four hundred in total, itemised by "
   "type. The detail matters because these are the same objects, not replacements. What "
   "was carried off as trophies of a defeated God is handed back by the treasurer of a "
   "later empire, and the inventory is the proof."),
],
"ezra2": [
  ("The Register of Those Who Returned (vv.1-2)",
   "The chapter is a census, and the list is reproduced almost identically in Nehemiah "
   "7:6-73, which indicates an official document rather than a summary. Eleven leaders "
   "are named with Zerubbabel and Jeshua at the head. What follows is not narrative and "
   "is not meant to be read as one -- it is the community's roll, and the point of "
   "keeping it is that these particular people answered."),
  ("Counted by Family (vv.3-20)",
   "The first grouping is by clan, family by family with numbers attached. The figures "
   "run from thousands down to dozens, so the register does not round or tidy. Reading a "
   "list of household names is the least dramatic passage in the book and the most "
   "concrete evidence of what the return actually consisted of: not a movement, but "
   "these families."),
  ("Counted by Town (vv.21-35)",
   "The organising principle changes halfway through, from descent to place -- the men "
   "of Bethlehem, of Netophah, of Anathoth, of Kirjath-arim. The shift matters because "
   "these people are going back to towns their grandparents left, and identity is being "
   "recorded both by blood and by ground. Both were needed to reclaim an inheritance."),
  ("Priests, Levites, Singers and Servants (vv.36-58)",
   "The temple personnel are counted separately: 4,289 priests, and 74 Levites. That "
   "gap is the most consequential number in the chapter. Priests returned in strength "
   "and Levites did not, and the shortage recurs at 8:15-20 when Ezra finds no Levites "
   "in his own company and has to recruit them. Singers, gatekeepers and the Nethinim "
   "follow, all listed by household."),
  ("Those Who Could Not Prove Their Genealogy (vv.59-70)",
   "Some could not produce their descent, and the priests among them are set aside from "
   "holy things until a priest should arise with Urim and Thummim -- a suspension rather "
   "than a rejection, and one with no stated end. The totals close the register at "
   "42,360 with 7,337 servants. The last verses record giving toward the work and the "
   "people settling in their own cities, so the chapter ends with a community placed on "
   "the ground before anything is built."),
],
"ezra3": [
  ("The Altar Before the Temple (vv.1-3)",
   "In the seventh month the people gather as one man to Jerusalem and build the altar "
   "first -- before walls, before the temple, before their own houses are finished. The "
   "order is the point. Verse 3 adds that they set it on its bases \u201cfor fear was "
   "upon them because of the people of those countries\u201d, so the first act of "
   "worship is performed by people who are afraid, not by people who feel safe."),
  ("Tabernacles Kept, the Calendar Restored (vv.4-6)",
   "The seventh month was chosen deliberately: it held the Feast of Trumpets, the Day of "
   "Atonement and Tabernacles. They keep the feast, offer the daily burnt offerings, and "
   "restore the whole liturgical year. Verse 6 notes plainly that the foundation of the "
   "house was not yet laid. The calendar is running before the building exists, which "
   "reverses the order anyone would expect."),
  ("Cedar from Lebanon, the Foundation Laid (vv.7-11)",
   "Masons and carpenters are hired and cedar is fetched from Lebanon by sea to Joppa, "
   "the same arrangement Solomon made in 1 Kings 5 -- a deliberate link to the first "
   "temple. In the second year the foundation is laid, and the ceremony follows the old "
   "pattern with priests in their apparel, trumpets, and cymbals. The refrain sung is "
   "the one from the Psalms: for he is good, for his mercy endureth for ever."),
  ("Weeping and Shouting Indistinguishable (vv.12-13)",
   "The scene the chapter is remembered for. The young shout for joy at a beginning, "
   "while the old priests and heads of families who had seen Solomon's house weep with a "
   "loud voice at the comparison. The two sounds mix so that the people could not "
   "distinguish the shout of joy from the noise of the weeping, and it was heard far "
   "off. Restoration is recorded as genuinely both things at once, without the text "
   "choosing between them."),
],
"ezra4": [
  ("Let Us Build With You (vv.1-3)",
   "The adversaries open with an offer of partnership: we seek your God as ye do, and "
   "we do sacrifice unto him. These were peoples resettled in Samaria by Assyria, whose "
   "worship 2 Kings 17:24-33 describes as mixing the LORD with their own gods. "
   "Zerubbabel's refusal is not about ancestry -- it is that a temple built in "
   "partnership with syncretistic worship would be compromised in its foundations. He "
   "answers that they have nothing to do with it, which is a hard sentence to say to "
   "neighbours."),
  ("Weakening the Hands of the People (vv.4-5)",
   "Rejected, the same parties change method: they weakened the hands of the people of "
   "Judah and troubled them in building, and hired counsellors against them. The phrase "
   "describes discouragement as a deliberate campaign rather than a mood. It runs from "
   "Cyrus's reign to Darius's, so the opposition outlasts three kings."),
  ("The Letter to Artaxerxes (vv.6-16)",
   "The chapter now groups later episodes with earlier ones thematically rather than "
   "keeping strict order, which is why the kings named jump about. The letter itself is "
   "a study in method: every fact in it is true. Jerusalem had rebelled, it had been "
   "destroyed for it, and a rebuilt city with walls would pay less tribute. Truth "
   "assembled to produce a false conclusion is harder to answer than a lie, and the "
   "writers knew it."),
  ("The King's Answer (vv.17-22)",
   "Artaxerxes has the archives searched, finds the rebellions confirmed, and orders "
   "the work stopped. He is not being unreasonable on the evidence presented. That is "
   "the chapter's uncomfortable point: the machinery of a competent empire, given "
   "accurate but selected information, produced exactly the outcome the accusers "
   "wanted."),
  ("The Work Ceased (vv.23-24)",
   "The decree is carried out by force and arms, and the work on the house of God "
   "ceased until the second year of Darius -- roughly sixteen years of nothing. The "
   "chapter ends there, with no encouragement offered and no explanation given. Haggai "
   "and Zechariah, who restart it, are not mentioned until the next chapter's first "
   "verse."),
],
"ezra5": [
  ("Haggai and Zechariah Prophesied (vv.1-2)",
   "The restart has no political cause. Two prophets speak, and Zerubbabel and Jeshua "
   "rise up and begin to build, with the prophets of God helping them. Haggai's own "
   "book dates this to 520 BC and records what he said -- that the people were "
   "panelling their own houses while God's lay waste. Sixteen years of stoppage ends "
   "with preaching rather than permission."),
  ("Who Commanded You to Build? (vv.3-5)",
   "Tattenai, the governor of the province beyond the river, arrives with the obvious "
   "question, and asks for the names of the builders. Verse 5 gives the chapter's "
   "explanation of what follows: the eye of their God was upon the elders of the Jews, "
   "so they could not cause them to cease. The work continues during the investigation "
   "rather than pausing for it."),
  ("Tattenai's Letter (vv.6-10)",
   "The contrast with chapter 4 is the point of quoting this letter at length. Tattenai "
   "reports what he found without spin, notes that the work goeth fast on and prospereth, "
   "and asks the king to check the record. An honest official is as consequential here as "
   "a dishonest one was there, and the difference is not the law but the man applying it."),
  ("We Are the Servants of the God of Heaven (vv.11-17)",
   "The elders' answer is quoted inside the letter and it is a model of its kind. They "
   "identify themselves as servants of the God of heaven and earth, state that the "
   "temple was built by a great king of Israel, and then concede the hard part without "
   "being asked: our fathers provoked God to wrath, and he gave them into the hand of "
   "Nebuchadnezzar. Then the legal ground, Cyrus's decree, with a request that the "
   "archives be searched. Honesty about the exile is offered as part of the case rather "
   "than hidden from it."),
],
"ezra6": [
  ("The Roll Found at Ecbatana (vv.1-5)",
   "The search succeeds, but not where anyone looked first. The decree turns up at "
   "Achmetha, Ecbatana, the Median summer capital, which is where Cyrus is likely to "
   "have been in his first year rather than Babylon. Its terms exceed what the builders "
   "had claimed: dimensions specified, costs to be paid from the king's house, and the "
   "vessels restored. The archive vindicated them more thoroughly than their own "
   "testimony had."),
  ("Darius Adds His Own Decree (vv.6-12)",
   "Darius not only upholds Cyrus but goes further, ordering Tattenai to leave them "
   "alone and to fund the work from the provincial tribute, with animals for sacrifice "
   "supplied daily. He attaches a penalty for interference and asks the builders to pray "
   "for him and his sons. The enquiry intended to stop the work has produced state "
   "funding and legal protection."),
  ("The House Finished (vv.13-15)",
   "The elders build and prosper, and the house is finished on the third of Adar in "
   "Darius's sixth year -- 12 March 515 BC. Verse 14 credits the prophesying of Haggai "
   "and Zechariah alongside the decrees of Cyrus, Darius and Artaxerxes, putting prophets "
   "and emperors in one sentence. The temple destroyed in 586 BC is standing again "
   "roughly seventy years later."),
  ("The Dedication, and Twelve Goats (vv.16-18)",
   "The dedication offerings are a hundred bulls, two hundred rams and four hundred "
   "lambs -- against Solomon's twenty-two thousand oxen and a hundred and twenty "
   "thousand sheep. The scale is honest about what the remnant was. The detail that "
   "carries weight is the twelve goats for a sin offering, according to the number of "
   "the tribes of Israel, when only Judah and Benjamin had returned. They offer for all "
   "twelve, claiming an identity larger than their own numbers."),
  ("The Passover Kept (vv.19-22)",
   "The Passover is kept in the first month, and those who had separated themselves from "
   "the filthiness of the heathen eat it with them, so the boundary is defined by "
   "separation rather than descent. Seven days of unleavened bread follow with joy. The "
   "final verse says the LORD had turned the heart of the king of Assyria toward them, "
   "which closes the first half of the book where it began -- with God moving a foreign "
   "monarch."),
],
"ezra7": [
  ("Ezra's Priestly Genealogy (vv.1-5)",
   "Nearly sixty years pass between the temple's completion and this chapter, and the "
   "book says nothing about them. Ezra is introduced by descent, traced back through "
   "Zadok and Phinehas to Aaron the chief priest. The line is abbreviated -- comparison "
   "with 1 Chronicles 6 shows names omitted -- which was normal practice. The purpose is "
   "credentials: he is entitled to act as a priest as well as a scholar."),
  ("He Prepared His Heart (vv.6-10)",
   "Verse 10 is the verse Ezra is remembered for, and its order is deliberate: he "
   "prepared his heart to seek the law of the LORD, and to do it, and to teach in Israel "
   "statutes and judgments. Study, practice, then teaching -- with practice between the "
   "other two. He is called a ready scribe in the law of Moses, and the reason given for "
   "the king granting his requests is that the hand of the LORD his God was upon him."),
  ("Artaxerxes' Letter (vv.11-20)",
   "The letter is quoted in Aramaic and its generosity is hard to account for on "
   "political grounds. Any willing Jew may go. Silver and gold are given from the king "
   "and his counsellors. Ezra may draw further funds from the provincial treasury for "
   "whatever the house of God requires. The king's stated motive is fear of divine wrath "
   "against his realm, which is candid about what is in it for him."),
  ("Authority to Appoint Judges (vv.21-26)",
   "The grants go further than funding. Temple personnel are exempted from tribute, "
   "custom and toll, and Ezra is authorised to appoint magistrates and judges to "
   "administer the law of his God throughout the province beyond the river, with "
   "penalties up to death. A Persian king is delegating the enforcement of Jewish law to "
   "a Jewish scribe, which is a remarkable transfer of authority however it is "
   "explained."),
  ("Blessed Be the LORD God of Our Fathers (vv.27-28)",
   "Ezra's own voice takes over for the first time, and his response to unlimited "
   "authority is a blessing rather than a plan: blessed be the LORD, who hath put such a "
   "thing as this in the king's heart. He credits the mercy of God for the favour of the "
   "king and his counsellors, and says he was strengthened as the hand of the LORD was "
   "upon him. Then he gathers chief men to go up with him."),
],
"ezra8": [
  ("Those Who Went Up With Ezra (vv.1-14)",
   "A second register, smaller than chapter 2's -- around 1,500 men with their families, "
   "listed by family head. The journey is roughly nine hundred miles and takes four "
   "months, from the first day of the first month to the first day of the fifth. Naming "
   "them serves the same purpose as the earlier list: the return is made of identifiable "
   "households rather than a movement."),
  ("No Levites Among Them (vv.15-20)",
   "Assembling at the river Ahava, Ezra reviews the company and finds none of the sons "
   "of Levi -- the same shortage as chapter 2, sixty years on. He does not proceed "
   "without them. He sends named men to Casiphia with instructions, and by the good hand "
   "of our God upon us they bring thirty-eight Levites and two hundred and twenty "
   "Nethinim. A delay to fix a staffing problem, recorded as providence."),
  ("I Was Ashamed to Require Soldiers (vv.21-23)",
   "The most revealing passage in the chapter. Ezra proclaims a fast because he was "
   "ashamed to ask the king for soldiers and horsemen, having told him that the hand of "
   "our God is upon all them for good that seek him. His own public testimony has "
   "obligated him. He could have had an escort for the asking and declines it because "
   "accepting would contradict what he had said, which is faith tested by its own "
   "confession rather than by circumstance."),
  ("Weighed Out and Accounted For (vv.24-30)",
   "The treasure is weighed out to twelve named priests in front of witnesses: six "
   "hundred and fifty talents of silver, a hundred talents of gold, and vessels. That is "
   "something like twenty-five tons of silver. Ezra tells them they are holy and so is "
   "the silver, and requires it weighed again on arrival. An unarmed caravan carrying "
   "state treasure through bandit country, with a paper trail."),
  ("Delivered from the Hand of the Enemy (vv.31-36)",
   "They depart on the twelfth day and God delivered them from the hand of the enemy "
   "and of such as lay in wait by the way. On arrival the silver and gold are weighed "
   "again and the numbers recorded, which closes the accountability loop opened before "
   "departure. Offerings are made and the king's commissions delivered to the "
   "governors. The chapter ends in administration, which is how it began."),
],
"ezra9": [
  ("The Princes Chief in This Trespass (vv.1-2)",
   "The report reaching Ezra is that the returned exiles have intermarried with the "
   "surrounding peoples. The prohibition in Deuteronomy 7:3-4 is stated there in terms "
   "of covenant loyalty -- they will turn your sons from following me -- rather than "
   "ancestry, and the same concern is what drives this chapter. The sentence that makes "
   "it worse is the last: the hand of the princes and rulers hath been chief in this "
   "trespass. The leadership is the most compromised part."),
  ("Astonied Until the Evening Sacrifice (vv.3-5)",
   "His reaction is physical and prolonged: he rends his garment and mantle, plucks hair "
   "from his head and beard, and sits down astonied. Those who trembled at the words of "
   "God gather to him, and he sits until the evening sacrifice without speaking. Hours "
   "of silence before any word is said about it, which is unusual in a book that "
   "otherwise moves briskly."),
  ("Our Iniquities Are Increased Over Our Head (vv.6-9)",
   "The prayer begins in shame rather than petition -- I blush to lift up my face to "
   "thee, our iniquities are increased over our head. Ezra says \u201cour\u201d "
   "throughout, though nothing suggests he was among the guilty. He then sets the "
   "present mercy alongside the old sin: for a little space grace hath been shewed, to "
   "leave us a remnant and give us a nail in his holy place. The kindness makes the "
   "situation worse rather than better."),
  ("Shall We Break Thy Commandments Again? (vv.10-15)",
   "The argument's logic is what gives the prayer its force. God punished this before "
   "with exile; we have been graciously restored; and now shall we again break thy "
   "commandments? Verse 13 states it as a question that answers itself. The prayer ends "
   "without a request, without a proposal, and without asking anything specific -- "
   "behold, we are before thee in our trespasses, for we cannot stand before thee "
   "because of this. Ezra leaves the weight of it with God and with the people listening."),
],
"ezra10": [
  ("Shecaniah: Yet Now There Is Hope (vv.1-4)",
   "The initiative comes from the congregation rather than from Ezra, which matters "
   "given that his prayer made no demand. A great assembly gathers weeping, and "
   "Shecaniah speaks: we have trespassed, yet now there is hope in Israel concerning "
   "this thing. He proposes the covenant himself and tells Ezra to arise, this matter "
   "belongeth unto thee, we also will be with thee. The reform is asked for by the "
   "people who will bear its cost."),
  ("The Assembly in the Rain (vv.5-14)",
   "Ezra takes an oath from the leaders and a proclamation gathers everyone to Jerusalem "
   "within three days on pain of forfeiture. They sit in the open street of the house of "
   "God in the ninth month, trembling and in heavy rain, which the text mentions twice. "
   "The people's own reply asks for a slower process -- the matter is great and it is a "
   "time of much rain -- and proposes that officers handle it case by case. The reform "
   "is negotiated rather than decreed."),
  ("The Commission Appointed (vv.15-17)",
   "Four men are named as opposing the plan, and the book records them without comment "
   "or rebuttal, which is a small honesty worth noticing. Chosen heads of families sit "
   "from the tenth month to the first, examining every case individually over three "
   "months. Whatever else this was, it was not summary."),
  ("The Names Recorded (vv.18-43)",
   "The guilty are listed by name: seventeen priests, six Levites, one singer, three "
   "gatekeepers and eighty-six laymen -- a hundred and thirteen men. The priests come "
   "first, which reflects the charge in 9:2 that the leaders were chief in it. Naming "
   "them is the same instinct as chapter 2's register applied to failure rather than "
   "faithfulness."),
  ("The Book Ends Without a Conclusion (v.44)",
   "The last verse states that all these had taken strange wives, and that some of them "
   "had children. Then the book stops. There is no dedication, no celebration, no "
   "summary of what was achieved -- unlike chapter 6, which ended in a Passover. The "
   "text also says nothing about what became of the women and children, and ancient "
   "practice would have required provision for a divorced wife. Whether the silence is "
   "discretion or discomfort, the ending refuses to make the reform feel triumphant."),
],
}

CAPS = re.compile(r"\b[A-Z]{2,}\b")


def main():
    check = "--check" in sys.argv
    problems, notes, planned = [], [], {}

    for page in sorted(VERSES, key=lambda s: int(s[4:])):
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
