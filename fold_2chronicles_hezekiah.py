#!/usr/bin/env python3
"""
2 Chronicles 29 to 36: Hezekiah to the fall, and the decree of Cyrus. Eight pages,
225 verses, two book fields each and no sublists.

The proportions here are the clearest evidence of what the Chronicler is doing. 2 Kings
gives Hezekiah's religious reform half a verse and spends its length on Sennacherib;
Chronicles gives the reform three chapters and Sennacherib part of one. Manasseh's
repentance at 33:12-13 appears in no other book, and without it Kings leaves the longest
reign in Judah's history as unbroken apostasy. Both choices follow from 7:14, which this
writer treats as the rule the whole history is testing.

The last chapter is not a lament. In the Hebrew arrangement of the canon Chronicles
stands last, so the Old Testament closes on a Persian king telling the exiles to go
home and rebuild, and on a sentence that stops rather than finishes, let him go up.

Usage:
    python3 fold_2chronicles_hezekiah.py [--check]
"""
import html as H
import os
import re
import sys

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")
PANE = re.compile(r'(id="tab-authorship">)(.*?)(?=<div class="tab-content")', re.S)
ITEM_RE = re.compile(
    r'<div class="auth-item"><span class="auth-label">(.*?)</span>\s*(.*?)</div>', re.S)
ITEM = ('                    <div class="auth-item">'
        '<span class="auth-label">{label}</span> {body}</div>')
KEEP = ("Author:", "Historical Context:")

SECTIONS = {
"2chronicles29": [
 ("The Doors Opened, and the Charge to the Levites (vv.1-11)",
  "Ahaz had shut the doors of the house of the LORD. The first act of his son's reign, in the first "
  "month of the first year, is to open them and repair them, and the sequence is the Chronicler's "
  "whole assessment of Hezekiah in one detail. He then assembles the priests and Levites in the east "
  "street and gives them an instruction with a diagnosis attached. The instruction is to sanctify "
  "themselves and the house and carry forth the filthiness out of the holy place. The diagnosis is "
  "that the trouble Judah is in is not political, our fathers have trespassed, and turned away their "
  "faces from the habitation of the LORD, therefore the wrath of the LORD was upon Judah. And the "
  "charge closes personally, my sons, be not now negligent, for the LORD hath chosen you to stand "
  "before him."),
 ("Sixteen Days of Carrying Out (vv.12-19)",
  "Fourteen Levites are named by family, from the Kohathites, Merari, the Gershonites and the singing "
  "houses of Asaph, Heman and Jeduthun, and the work is dated to the day. They begin on the first of "
  "the first month, reach the porch on the eighth, and finish on the sixteenth: sixteen days to carry "
  "the accumulated refuse of a closed temple out to the brook Kidron. The report they bring back is "
  "an inventory rather than a claim, we have cleansed all the house of the LORD, and the altar of "
  "burnt offering, and the table of shewbread, and all the vessels thereof, and the phrase attached "
  "to the vessels dates the damage precisely, which king Ahaz in his reign did cast away in his "
  "transgression."),
 ("The Sin Offering for All Israel, and the Song Restored (vv.20-30)",
  "The offering is made in sevens, seven bullocks, seven rams, seven lambs and seven he goats, for "
  "the kingdom, for the sanctuary and for Judah, and the Chronicler slips in a clause at verse 24 "
  "that widens it past the border, the king commanded that the burnt offering and the sin offering "
  "should be made for all Israel. Judah's king is atoning for tribes that are not his subjects. "
  "Then the music is put back, and the authority for it is stacked up carefully, according to the "
  "commandment of David, and of Gad the king's seer, and Nathan the prophet, for so was the "
  "commandment of the LORD by his prophets. The song of the LORD begins with the trumpets, the "
  "congregation worships throughout the burnt offering, and what they sing is the words of David and "
  "of Asaph the seer."),
 ("More Offered Than the Priests Could Handle (vv.31-36)",
  "Hezekiah tells the congregation they are now consecrated and invites them to bring sacrifices, and "
  "the response overruns the staff. Seventy bullocks, a hundred rams and two hundred lambs for burnt "
  "offerings, and six hundred oxen and three thousand sheep as consecrated things. The priests were "
  "too few to flay them, so the Levites did the work until it was finished and until the rest of the "
  "priests had sanctified themselves, and the Chronicler records the comparison without softening "
  "it, for the Levites were more upright in heart to sanctify themselves than the priests. The "
  "chapter ends on a note about pace rather than about scale, Hezekiah rejoiced, and all the people, "
  "that God had prepared the people, for the thing was done suddenly."),
],
"2chronicles30": [
 ("The Letters Sent Through All Israel (vv.1-12)",
  "Hezekiah keeps the passover a month late, and the text gives the reasons, the priests were not "
  "sanctified in sufficient number and the people were not gathered, using the provision Numbers 9 "
  "makes for exactly that case. What is unprecedented is who is invited. Letters go to Ephraim and "
  "Manasseh, that is, into territory Assyria had already annexed, and the appeal in them is built on "
  "the recent catastrophe: turn again unto the LORD, and he will return to the remnant of you that "
  "are escaped out of the hand of the kings of Assyria. Its theological centre is a promise about "
  "God's disposition rather than about Israel's prospects, for the LORD your God is gracious and "
  "merciful, and will not turn away his face from you, if ye return unto him. The reception is "
  "reported honestly, they laughed them to scorn, and mocked them, and then the exception, "
  "nevertheless divers humbled themselves and came to Jerusalem."),
 ("The Passover Kept, and a Prayer for the Unprepared (vv.13-22)",
  "The congregation that assembles is very great, and its first action is demolition, the altars in "
  "Jerusalem taken away and cast into the brook Kidron. Then the problem the whole chapter turns on. "
  "A multitude from Ephraim, Manasseh, Issachar and Zebulun eat the passover otherwise than it was "
  "written, because they had not cleansed themselves, and the penalty in the law is severe. "
  "Hezekiah's response is to pray rather than to exclude, the good LORD pardon every one that "
  "prepareth his heart to seek God, though he be not cleansed according to the purification of the "
  "sanctuary, and the answer is recorded as plainly as the request, and the LORD hearkened to "
  "Hezekiah, and healed the people. No passage in the Old Testament states more clearly that "
  "intention can be accepted where the ritual condition was not met."),
 ("A Second Seven Days (vv.23-27)",
  "The assembly decides it does not want to stop, and takes counsel to keep other seven days, which "
  "has no precedent in the law. The provisioning is itemised, a thousand bullocks and seven thousand "
  "sheep from the king, two thousand bullocks and ten thousand sheep from the princes. The list of "
  "who rejoiced is the widest in the book: the priests, the Levites, all the congregation of Judah, "
  "the strangers that came out of Israel, and the strangers that dwelt in Judah. The comparison "
  "drawn is with the last time the whole nation had gathered, since the time of Solomon the son of "
  "David there was not the like in Jerusalem. The chapter ends with the priests blessing the people "
  "and the note that their voice was heard, and their prayer came up to heaven."),
],
"2chronicles31": [
 ("The Heaps of Firstfruits (vv.1-10)",
  "The festival ends in demolition rather than in dispersal: the people who came for the passover go "
  "out and break the images and throw down the high places, and they do it in Ephraim and Manasseh "
  "as well as in Judah and Benjamin. Then Hezekiah turns to funding, appointing the courses of "
  "priests and Levites and commanding the people to give their portion, with the reason stated, that "
  "they might be encouraged in the law of the LORD. What comes in is more than the system can hold. "
  "Firstfruits of corn, wine, oil and honey, and the tithe of everything, piled in heaps from the "
  "third month to the seventh. When the king asks about the heaps, Azariah's answer is an audit "
  "result, since the people began to bring the offerings into the house of the LORD, we have had "
  "enough to eat, and have left plenty."),
 ("The Storehouses, the Distribution and the Verdict (vv.11-21)",
  "The second half is administration, and the Chronicler gives it the same weight he gives a battle. "
  "Chambers are prepared in the house of the LORD, Cononiah and his brother are set over them with "
  "ten named overseers, and Kore is put over the freewill offerings with six men to distribute in the "
  "cities of the priests. The distribution rules are specified: by course, to every male from three "
  "years old and upward, to the priests by genealogy and to the Levites by their reckoning, and to "
  "those living out in the fields of the suburbs. Then the verdict, and it credits the paperwork as "
  "faithfulness, in every work that he began in the service of the house of God, and in the law, and "
  "in the commandments, to seek his God, he did it with all his heart, and prospered."),
],
"2chronicles32": [
 ("The Invasion, the Water Stopped and the Wall Built (vv.1-8)",
  "Sennacherib comes after all this, which is the Chronicler's way of saying that a reformed kingdom "
  "is not an unthreatened one. Hezekiah's preparations are practical and are listed as such: the "
  "springs outside the city stopped, with the reasoning given in his own words, why should the kings "
  "of Assyria come, and find much water, then the wall raised, another wall built outside it, the "
  "towers strengthened, weapons made and captains appointed. The engineering behind verse 4 is "
  "described again at verse 30 and can still be walked through, the tunnel cut to bring the Gihon "
  "spring inside the walls, with an inscription at its midpoint recording the two teams of quarrymen "
  "meeting. Then the speech, which puts the whole preparation in proportion, with him is an arm of "
  "flesh, but with us is the LORD our God to help us, and to fight our battles."),
 ("The Assyrian Argument at the Wall (vv.9-19)",
  "The Assyrian case is set out at length because it is a good argument, and the Chronicler lets it "
  "run. It begins with the question that matters, whereon do ye trust. It reasons from an unbroken "
  "record, no god of any nation Assyria has taken has delivered his people, so why should this one. "
  "And it turns Hezekiah's reform into evidence against him, hath not the same Hezekiah taken away "
  "his high places and his altars, which is how a religious purge looks to an observer who assumes "
  "more altars mean more help. The flaw is named in the last verse of the section rather than "
  "answered in it, they spake against the God of Jerusalem, as against the gods of the people of the "
  "earth, which are the work of the hands of man. The category mistake is the whole reply."),
 ("The Angel, and the Gifts Brought to Jerusalem (vv.20-23)",
  "Four verses dispose of the campaign. Hezekiah and Isaiah prayed and cried to heaven, and the LORD "
  "sent an angel which cut off all the mighty men of valour, and the leaders and captains, in the "
  "camp of the king of Assyria. Sennacherib goes home with shame of face, and is killed in the house "
  "of his own god by his own sons, which answers the argument of the previous section on its own "
  "terms. The consequence is reputational, many brought gifts unto the LORD to Jerusalem, and "
  "Hezekiah was magnified in the sight of all nations from thenceforth."),
 ("The Sickness, the Envoys, and What God Left Him to Learn (vv.24-33)",
  "Hezekiah's illness, prayer and sign are given in a single verse, and then the difficulty: he "
  "rendered not again according to the benefit done unto him, for his heart was lifted up. The "
  "structure is the same as Uzziah's at 26:16, and the outcome differs only because of what he does "
  "next, notwithstanding Hezekiah humbled himself, so the wrath came not upon them in the days of "
  "Hezekiah. The wealth is then inventoried, the conduit noted again, and the Babylonian ambassadors "
  "arrive to enquire of the wonder that was done in the land. What the Chronicler says about that "
  "visit is the most searching sentence in the chapter, God left him, to try him, that he might know "
  "all that was in his heart. He is buried in the chiefest of the sepulchres of the sons of David, "
  "and all Judah did him honour at his death."),
],
"2chronicles33": [
 ("Manasseh's Fifty-Five Years (vv.1-9)",
  "The longest reign of any king of Judah, and the Chronicler spends nine verses cataloguing what it "
  "restored: the high places Hezekiah had broken down, altars for Baalim, groves, the host of heaven "
  "worshipped, altars built inside the house of the LORD and in both its courts, children passed "
  "through the fire in the valley of the son of Hinnom, and the full range of divination, observing "
  "times, enchantments, witchcraft, a familiar spirit and wizards. The worst of it is placed "
  "precisely, a carved image set in the house of God, the place of which God had said, In Jerusalem "
  "shall my name be for ever. And the verdict is comparative, so Manasseh made Judah and the "
  "inhabitants of Jerusalem to err, and to do worse than the heathen whom the LORD had destroyed "
  "before them."),
 ("The Hooks, the Prayer and the Restoration (vv.10-17)",
  "This section exists only in Chronicles, and it changes the shape of the reign completely. Warnings "
  "are ignored, so the Assyrian captains take Manasseh among the thorns, bind him with fetters and "
  "carry him to Babylon. Then the turn, and the verbs are worth reading in order, when he was in "
  "affliction, he besought the LORD his God, and humbled himself greatly before the God of his "
  "fathers, and prayed unto him. The answer is as unqualified as the offence had been, and he was "
  "intreated of him, and heard his supplication, and brought him again to Jerusalem into his kingdom. "
  "The conclusion drawn is a single clause, then Manasseh knew that the LORD he was God. What "
  "follows is restitution rather than sentiment: the wall built, the strange gods and the image "
  "carried out of the city, the altar repaired, and Judah commanded to serve the LORD. 2 Kings has "
  "none of this, which is why the same reign reads there as apostasy without remedy."),
 ("The Prayer Recorded, and Amon's Two Years (vv.18-25)",
  "The Chronicler notes that Manasseh's prayer and God's answer to it are written among the sayings "
  "of the seers, a document nobody now has. The gap was filled later: the composition known as the "
  "Prayer of Manasseh, preserved in Greek manuscripts and still used liturgically in some traditions, "
  "was written to supply the words this verse says existed. Amon then gets five verses and one "
  "comparison, which is the point of putting him here: he did as his father had done, but humbled not "
  "himself before the LORD, as Manasseh his father had humbled himself, but trespassed more and more. "
  "The difference between the two reigns is not the sinning. His own servants kill him in his house, "
  "the people of the land kill the conspirators, and Josiah is made king."),
],
"2chronicles34": [
 ("The Purge, and the Repair Begun (vv.1-13)",
  "Josiah's reform is dated in stages: he begins to seek God in the eighth year of his reign while he "
  "was yet young, begins to purge in the twelfth, and repairs the temple in the eighteenth. The purge "
  "is described physically, images beaten into powder and strewn on the graves of the men who had "
  "sacrificed to them, and the bones of their priests burnt on their own altars. Its reach is the "
  "detail worth noticing, into Manasseh, Ephraim, Simeon and as far as Naphtali, which is territory "
  "no king of Judah had governed for a century and was only reachable because Assyrian power was "
  "collapsing. The repair is then organised through the Levites, and the Chronicler cannot help "
  "recording where the musicians ended up, all that could skill of instruments of musick were set "
  "over the bearers of burdens."),
 ("The Book Found, and the Clothes Torn (vv.14-21)",
  "While the money is being brought out, Hilkiah finds a book of the law of the LORD given by Moses, "
  "and Shaphan reads it to the king. Which book it was is not stated. The reforms that follow "
  "correspond closely to the requirements of Deuteronomy, which is why many identify it with "
  "Deuteronomy or a part of it. What the passage does record exactly is the reaction, he rent his "
  "clothes, and the reason he gives for sending to enquire, for great is the wrath of the LORD that "
  "is poured out upon us, because our fathers have not kept the word of the LORD. A king in the "
  "middle of the most thorough reform in Judah's history reads the law and concludes that things are "
  "worse than he thought."),
 ("Huldah's Answer, and the Covenant Read to the People (vv.22-33)",
  "The enquiry goes to Huldah the prophetess, one of the few named women in that office in the Old "
  "Testament, and consulted in preference to Jeremiah, who was already prophesying at this date. Her "
  "answer comes in two parts that do not cancel each other. To the place: all the curses written in "
  "the book will come, because they have forsaken me. To the king: because thine heart was tender, "
  "and thou didst humble thyself before God, thine eyes shall not see all the evil. The reform is not "
  "reversing the outcome, and Josiah proceeds anyway. He gathers everyone, great and small, reads all "
  "the words of the book of the covenant in their ears, makes the covenant standing in his place, and "
  "causes all present to stand to it. The result is stated as a duration, and all his days they "
  "departed not from following the LORD God of their fathers."),
],
"2chronicles35": [
 ("The Passover Prepared, and the Provision for It (vv.1-9)",
  "Josiah's passover is organised rather than improvised, and the instructions to the Levites include "
  "one line that quietly marks the end of an era, put the holy ark in the house which Solomon built, "
  "there shall no more be a burden upon your shoulders. The carrying duty that defined the office "
  "since the wilderness is finished, and the Levites are reassigned to serving the people and to "
  "their divisions according to the writing of David and Solomon. Then the provisioning, which is "
  "given as figures because generosity is being measured: thirty thousand lambs and kids and three "
  "thousand bullocks from the king, twenty-six hundred small cattle and three hundred oxen from three "
  "named officials, and five thousand small cattle and five hundred oxen from the chief of the "
  "Levites, all of it given willingly to the people, the priests and their brethren."),
 ("The Service Kept as It Had Not Been Since Samuel (vv.10-19)",
  "The account of the day itself is procedural, and deliberately so: the priests standing in their "
  "place and the Levites in their courses, the flaying, the blood handed along to be sprinkled, the "
  "passover roasted with fire as the law requires and the other offerings boiled in pots and "
  "caldrons and divided out quickly among the people, and the singers, the sons of Asaph, in their "
  "place according to the commandment of David. Everything is where the writing says it should be, "
  "which is the Chronicler's highest praise. Then the assessment, reaching back past the whole "
  "monarchy, there was no passover like to that kept in Israel from the days of Samuel the prophet, "
  "neither did all the kings of Israel keep such a passover as Josiah kept."),
 ("Megiddo, and the Lamentations for Josiah (vv.20-27)",
  "Necho of Egypt marches north to Charchemish and Josiah goes out to intercept him, and the warning "
  "he ignores comes from an unexpected mouth. Necho sends to say he has no quarrel with Judah, and "
  "adds a claim, God commanded me to make haste, forbear thee from meddling with God, who is with me. "
  "The Chronicler endorses it in his own narration, and hearkened not unto the words of Necho from "
  "the mouth of God, so the last good king of Judah dies for refusing a word delivered by a pharaoh. "
  "He is hit by archers, taken out of his chariot and brought to Jerusalem to die. The mourning "
  "becomes institutional: Jeremiah lamented for him, the singing men and singing women spoke of him "
  "in their lamentations, and they made them an ordinance in Israel."),
],
"2chronicles36": [
 ("Four Kings in Twenty-Three Years (vv.1-14)",
  "After Megiddo the throne changes hands at the convenience of whichever empire is nearest. "
  "Jehoahaz is made king by the people and deposed by Necho after three months, taken to Egypt, and "
  "his brother installed under a new name and a tribute. Jehoiakim lasts eleven years and is bound in "
  "fetters by Nebuchadnezzar, who also begins removing the vessels of the house of the LORD. "
  "Jehoiachin lasts three months and ten days; his age is given here as eight where 2 Kings 24:8 has "
  "eighteen, one of several such divergences between the books. Zedekiah is installed by Babylon and "
  "the charge against him is specific about what he would not do, he humbled not himself before "
  "Jeremiah the prophet speaking from the mouth of the LORD, and he broke an oath sworn by God. The "
  "section closes by widening the blame past the palace, the priests and the people trespassed very "
  "much, and polluted the house of the LORD."),
 ("The Messengers Mocked, and the Land Keeping Sabbath (vv.15-21)",
  "Verses 15 and 16 are the Chronicler's summary of the entire history he has been writing, and the "
  "motive he assigns to God is compassion rather than patience running out, the LORD God of their "
  "fathers sent to them by his messengers, rising up betimes and sending, because he had compassion "
  "on his people, and on his dwelling place. What answers it is a sequence of verbs, they mocked the "
  "messengers of God, and despised his words, and misused his prophets, until there was no remedy. "
  "The destruction is then reported without mitigation: no compassion shown to young or old, the "
  "vessels great and small carried to Babylon, the house of God burnt, the wall broken down, the "
  "palaces burnt. And a single verse interprets it, reading Leviticus 26 and Jeremiah together, the "
  "land lay desolate to fulfil the word of the LORD, until the land had enjoyed her sabbaths, to "
  "fulfil threescore and ten years."),
 ("Cyrus, and a Book That Ends on a Command to Go Up (vv.22-23)",
  "The last two verses jump fifty years without transition, to the first year of Cyrus king of "
  "Persia, when the LORD stirred up his spirit to make a proclamation throughout all his kingdom. "
  "Ezra 1 opens with the same decree, and the seam is deliberate: the Chronicler's readers are the "
  "people the decree is addressed to. The wording matters at two points. Cyrus credits his empire to "
  "Israel's God, all the kingdoms of the earth hath the LORD God of heaven given me. And the decree "
  "ends in the second person, who is there among you of all his people, the LORD his God be with "
  "him, and let him go up. Because Chronicles stands last in the Hebrew order, that is the final "
  "sentence of the Old Testament, and it is not a conclusion but an instruction left open."),
],
}


def verify(planned):
    """Run the audit's own checks against the planned HTML, without writing it."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import audit_authorship as A
    found = []
    for path, html in planned.items():
        page = os.path.basename(path)[:-5]
        nums = {int(x) for x in re.findall(r'class="verse-num"[^>]*>(\d+)', html)}
        total = max(nums) if nums else 0
        pane = A.PANE.search(html).group(2)
        labels = [H.unescape(x).strip() for x in A.LABEL.findall(pane)]
        secs = [(l, A.TAIL.search(l)) for l in labels]
        secs = [(l, m.group(1)) for l, m in secs if m]
        covered, repeated, starts = set(), set(), []
        for label, spec in secs:
            got = A.halves(spec)
            repeated |= got & covered
            covered |= got
            starts.append(min(v for v, _ in got) if got else 0)
            if total and max(v for v, _ in got) > total:
                found.append(f"{page}: {label!r} runs past verse {total}")
        want = {(v, h) for v in range(1, total + 1) for h in ("a", "b")}
        missing = sorted({v for v, _ in (want - covered)})
        if missing:
            found.append(f"{page}: verses uncovered {missing}")
        if repeated:
            found.append(f"{page}: verses described twice "
                         f"{sorted({v for v, _ in repeated})}")
        if starts != sorted(starts):
            found.append(f"{page}: sections out of verse order")
        if "<li>" in pane:
            found.append(f"{page}: unexpected sublist in pane")
        for label in labels:
            fault = A.label_fault(label)
            if fault:
                found.append(f"{page}: label {fault}: {label!r}")
            stray = sorted({w for w in A.CAPS.findall(label)
                            if w not in A.CAPS_OK})
            if stray and A.TAIL.search(label):
                found.append(f"{page}: capitals {stray} in {label!r}")
    return found


def main():
    check = "--check" in sys.argv
    planned, problems, notes = {}, [], []
    for page, sections in SECTIONS.items():
        path = os.path.join(DOCS, page + ".html")
        html = open(path, encoding="utf-8").read()
        pane = PANE.search(html)
        if not pane:
            problems.append(f"{page}: no authorship pane")
            continue
        body_html = pane.group(2)
        keep = [[l, b.strip()] for l, b in ITEM_RE.findall(body_html)
                if H.unescape(l).strip() in KEEP]
        if len(keep) != len(KEEP):
            problems.append(f"{page}: expected {len(KEEP)} book fields, "
                            f"found {len(keep)}")
            continue
        parts = ["\n                <h3>Authorship &amp; Background</h3>\n"]
        for label, body in keep:
            parts.append(ITEM.format(label=label, body=body) + "\n")
        for label, prose in sections:
            parts.append(ITEM.format(label=label + ":", body=prose) + "\n")
            notes.append(f"{page}: {label}")
        new_body = "".join(parts) + "            </div>\n\n            "
        d_open = (len(re.findall(r"<div\b", new_body))
                  - len(re.findall(r"<div\b", body_html)))
        d_close = (len(re.findall(r"</div>", new_body))
                   - len(re.findall(r"</div>", body_html)))
        if d_open != d_close:
            problems.append(f"{page}: pane gains {d_open} open divs "
                            f"and {d_close} closes")
        planned[path] = html[:pane.start(2)] + new_body + html[pane.end(2):]
    problems += verify(planned)
    if problems:
        print(f"refusing to write, {len(problems)} problem(s)")
        for p in problems:
            print(f"    {p}")
        return 1
    for n in notes:
        print(f"    {n}")
    if not check:
        for path, new in planned.items():
            open(path, "w", encoding="utf-8").write(new)
    print(f"{'would fold' if check else 'folded'} {len(planned)} pages, "
          f"{len(notes)} section(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
