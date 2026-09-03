#!/usr/bin/env python3
"""
2 Chronicles 1 to 9: Solomon and the temple. Nine pages, 176 verses, no existing
sections and no sublists to preserve, so the two book fields are kept and the
sections are written new.

These nine chapters are the same events as 1 Kings 1 to 11 told by a writer with a
different purpose, and the sections say so where the difference is measurable rather
than as a general remark. Chronicles adds the brasen scaffold Solomon knelt on, the
singers at the ark's installation, the fire that fell at the dedication, and Pharaoh's
daughter moved out of David's city. It ends Solomon's prayer with words from Psalm 132
where Kings ends it with an exhortation. And it omits the whole of 1 Kings 11, the
foreign wives and the idolatry, which for a book written to a community rebuilding the
temple is a choice about what the reader needs rather than an oversight.

The building chapters, 3 and 4, are an inventory rather than a narrative, and they are
sectioned by what is being described: the structure, then the furnishings. Padding a
list of cubits and talents into narrative exposition would misdescribe the page, the
same reasoning applied to Joshua's boundary surveys and Leviticus' offering manual.

Usage:
    python3 fold_2chronicles_solomon.py [--check]
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
"2chronicles1": [
 ("Solomon at the Tabernacle in Gibeon (vv.1-6)",
  "The book opens with Solomon strengthened in his kingdom and the LORD his God with him, and then "
  "goes straight to worship rather than to politics. The Chronicler stops to explain something "
  "1 Kings 3 leaves unexplained: why the king is sacrificing at Gibeon rather than in Jerusalem. "
  "The answer is that the two halves of Israel's worship had come apart. David had brought the ark "
  "up to Jerusalem, but the tabernacle of the congregation that Moses made and the brasen altar "
  "that Bezaleel made were still at the high place in Gibeon. Solomon goes where the altar is, "
  "with all the assembly, and offers a thousand burnt offerings on it. The temple will exist to end "
  "this division."),
 ("The Request for Wisdom (vv.7-13)",
  "That night God appears to Solomon with an open question, Ask what I shall give thee. Solomon "
  "answers by first naming what he has inherited, thou hast shewed great mercy unto David my "
  "father, and then asking for the one thing his position actually requires, give me now wisdom "
  "and knowledge, that I may go out and come in before this people. The reply names the requests "
  "he did not make, riches, wealth, honour, long life, and the death of his enemies, and grants "
  "the wisdom together with the wealth he had not asked for. Where 1 Kings 3 frames the encounter "
  "as a dream, Chronicles reports it as an appearing."),
 ("Chariots, Silver and the Horse Trade (vv.14-17)",
  "Four verses of inventory close the chapter, and they are the promise of verse 12 being paid out. "
  "Silver and gold in Jerusalem as plenteous as stones, cedar trees as common as the sycomores of "
  "the valley. The last two verses are specific about commerce: horses brought out of Egypt and "
  "Kue by the king's merchants, chariots at six hundred shekels of silver apiece, and resold on to "
  "the kings of the Hittites and Syria. Deuteronomy 17:16 had told a king of Israel not to multiply "
  "horses to himself, nor to send to Egypt for them. The Chronicler records the trade without "
  "comment and leaves the reader holding both texts."),
],
"2chronicles2": [
 ("The Levy and the Letter to Huram (vv.1-10)",
  "Solomon determines to build two houses, one for the name of the LORD and one for his own "
  "kingdom, and the chapter is the procurement that follows. The labour is counted first, seventy "
  "thousand to bear burdens, eighty thousand to hew in the mountain, three thousand six hundred to "
  "oversee them. Then the letter to Huram of Tyre, which trades on an existing relationship, as "
  "thou didst deal with David my father, and even as I send. Its theological centre is a "
  "disclaimer built into the request: the house must be great because our God is great above all "
  "gods, and yet who is able to build him an house, seeing the heaven and heaven of heavens cannot "
  "contain him. Solomon asks for cedar, fir and algum, for a craftsman skilled in metal and dyed "
  "cloth, and offers payment in wheat, barley, wine and oil."),
 ("Huram's Answer and the Foreign Workforce (vv.11-18)",
  "Huram replies in writing, and his first sentence is a Gentile king confessing Israel's God as "
  "creator, blessed be the LORD God of Israel, that made heaven and earth. He sends the craftsman "
  "asked for, a man whose mother was of the daughters of Dan and whose father was a man of Tyre, "
  "able to work in gold, silver, brass, iron, stone, timber, purple, blue, fine linen and crimson. "
  "1 Kings 7:14 gives his mother's tribe as Naphtali, one of the small differences between the two "
  "accounts that neither book explains. The chapter ends with a census of the strangers in the "
  "land, a hundred and fifty-three thousand six hundred, set to the carrying and the hewing. The "
  "Chronicler states plainly that the temple was built by a conscripted foreign workforce."),
],
"2chronicles3": [
 ("The Site, and the Overlaying of the House (vv.1-7)",
  "Verse 1 is the most heavily loaded sentence in the building account. The house is begun in "
  "mount Moriah, where the LORD appeared unto David his father, in the place that David had "
  "prepared in the threshingfloor of Ornan the Jebusite. Three separate moments are tied to one "
  "patch of ground: the mountain of Genesis 22 where Abraham was sent with Isaac, the threshing "
  "floor of 1 Chronicles 21 where the plague stopped, and the temple now going up on it. The date "
  "is given to the day, the second day of the second month in the fourth year. Then the "
  "measurements and the surfaces, the porch, the fir boarding, the gold, the palm trees and chains, "
  "and cherubims graved upon the walls."),
 ("The Most Holy House, the Cherubim and the Two Pillars (vv.8-17)",
  "The inner room is twenty cubits square and overlaid with six hundred talents of gold, a figure "
  "so large that commentators disagree over whether the weight is literal or a scribal convention "
  "for an enormous sum. The two cherubims are the striking feature: not the small figures on the "
  "ark's lid but carvings twenty cubits across, wing touching wing in the middle of the room and "
  "wing touching wall on either side, so the whole width of the holy place is spanned by them. The "
  "veil is blue, purple, crimson and fine linen with cherubims worked into it. The chapter closes "
  "outside, with the two free-standing pillars before the house, and gives their names, Jachin and "
  "Boaz."),
],
"2chronicles4": [
 ("The Brasen Altar, the Sea and the Lavers (vv.1-10)",
  "The furnishings are listed by function, beginning in the courtyard. The brasen altar is twenty "
  "cubits square and ten high, four times the area of the tabernacle altar it replaces. The molten "
  "sea is ten cubits across, standing on twelve oxen, and the text says it held three thousand "
  "baths, a volume in the region of sixty-six thousand litres. The distinction drawn at verse 6 is "
  "the point of the whole arrangement: the ten lavers are for washing what is offered, the sea is "
  "for the priests to wash themselves in. Then ten candlesticks, ten tables, a hundred golden "
  "basons, and the two courts, one for the priests and one great court for everyone else."),
 ("Huram's Work Finished, and the Vessels of Gold (vv.11-22)",
  "The second half is a manifest. Huram's brass work is itemised down to the pots, shovels and "
  "fleshhooks, then the pillars, the pommels, the wreaths and the four hundred pomegranates, the "
  "bases and the lavers, all of bright brass, cast in the clay ground of the plain of Jordan in "
  "quantities the text declines to total, brass without weight. From verse 19 the material changes "
  "to gold and the location moves inside: the golden altar, the tables of shewbread, the "
  "candlesticks and their lamps, the snuffers, basons, spoons and censers of pure gold, and the "
  "doors of the inner house. The chapter is an inventory and reads as one, which is what a reader "
  "should expect from it."),
],
"2chronicles5": [
 ("The Ark Brought Up to the Finished House (vv.1-10)",
  "With the work finished, the one thing the building was for is carried into it. Solomon gathers "
  "the assembly at the feast in the seventh month, and the Levites take up the ark from the city of "
  "David to the oracle prepared for it, under the wings of the great cherubim, with sacrifices "
  "beyond counting on the way. Two details are given the weight of evidence. The staves are left in "
  "place and can be seen from inside the holy place, and the ark contains nothing except the two "
  "tables that Moses put there at Horeb. The division that opened chapter 1, ark in one place and "
  "altar in another, ends here."),
 ("The Singers, the Trumpets and the Cloud (vv.11-14)",
  "This is the passage where the Chronicler's own interest shows most clearly. 1 Kings 8 has the "
  "priests come out and the cloud fill the house. Chronicles keeps that and puts a choir in front "
  "of it: Asaph, Heman and Jeduthun with their sons and brethren in white linen, cymbals, psalteries "
  "and harps, and a hundred and twenty priests with trumpets, all making one sound. What they sing "
  "is the refrain that runs through the whole book, for he is good, for his mercy endureth for "
  "ever. Then the house is filled with a cloud, and the priests cannot stand to minister. The music "
  "is not decoration in this account, it is what the glory arrives during."),
],
"2chronicles6": [
 ("Solomon's Address to the Assembly (vv.1-11)",
  "Solomon turns from the cloud to the people and states the paradox he is standing inside, the "
  "LORD hath said that he would dwell in the thick darkness, but I have built an house of "
  "habitation for thee. The address then rehearses how this came about. From the exodus until now "
  "God had chosen no city and no man; now Jerusalem is chosen, and David. Building the house was "
  "David's own intention, and the answer he received was that he did well to have it in his heart, "
  "but that his son would do the work. Solomon's argument is that the promise has been kept "
  "visibly, the LORD hath performed his word, and the covenant is inside the building behind him."),
 ("The Prayer Begins, at the Brasen Scaffold (vv.12-21)",
  "Only Chronicles supplies the platform. Solomon has had a brasen scaffold made, five cubits by "
  "five and three high, set in the midst of the court, and he kneels on it before the whole "
  "congregation with his hands spread out. The prayer opens on covenant faithfulness, there is no "
  "God like thee in the heaven nor in the earth, which keepest covenant, and asks for the promise "
  "to David to continue. Then, at verse 18, the question that keeps the whole occasion honest, but "
  "will God in very deed dwell with men on the earth. Solomon does not resolve it. He asks instead "
  "for something smaller and more usable, that God's eyes be open toward this place and that prayer "
  "made here be heard and forgiven."),
 ("The Seven Cases Brought to This House (vv.22-35)",
  "The middle of the prayer works through the situations a person or a nation might actually bring, "
  "and each one follows the same shape, when this happens, and they pray toward this house, then "
  "hear thou from heaven. A disputed oath between two men. Defeat by an enemy. Drought. Famine, "
  "pestilence, blasting, mildew, locust, siege, or any sickness, with the stated purpose that they "
  "may fear thee. Armies sent out to battle. The widest of them is at verses 32 and 33, the "
  "stranger who is not of Israel and comes from a far country because he has heard of the great "
  "name, and the reason given for hearing him is that all people of the earth may know thy name. "
  "The temple is being dedicated as a place where foreigners get an answer."),
 ("If They Sin and Are Carried Captive (vv.36-42)",
  "The last petition assumes the worst case, and states its premise without softening it, if they "
  "sin against thee, for there is no man which sinneth not. If they are carried away captive to a "
  "land far off or near, and they bethink themselves and turn and pray toward their land and this "
  "city and this house, then hear from heaven and forgive. For the Chronicler's first readers this "
  "was not a hypothetical, it was their own recent history and the ground of their being back in "
  "Jerusalem at all. The ending differs from 1 Kings 8, which closes with an exhortation to the "
  "people. Chronicles closes with words drawn from Psalm 132, arise, O LORD God, into thy resting "
  "place, and remember the mercies of David thy servant."),
],
"2chronicles7": [
 ("Fire from Heaven, and the Dedication Feast (vv.1-11)",
  "Chronicles alone reports the fire. Solomon finishes praying and fire comes down and consumes the "
  "burnt offering and the sacrifices, and the glory fills the house, which puts this dedication in "
  "a line with the tabernacle's in Leviticus 9 and with David's altar on the threshing floor in "
  "1 Chronicles 21. The people watching bow with their faces to the pavement and say the refrain "
  "again, for his mercy endureth for ever. The scale of what follows is stated in livestock, "
  "twenty-two thousand oxen and a hundred and twenty thousand sheep, and in time, seven days of "
  "dedication and seven days of the feast, with the people sent home on the twenty-third day of the "
  "seventh month glad in heart."),
 ("The Second Appearance, and What Was Promised (vv.12-18)",
  "The LORD appears to Solomon by night with an answer, I have heard thy prayer, and have chosen "
  "this place to myself for an house of sacrifice. Verse 14 is the sentence the whole book is built "
  "around and the most quoted line in Chronicles, if my people, which are called by my name, shall "
  "humble themselves, and pray, and seek my face, and turn from their wicked ways, then will I hear "
  "from heaven, and will forgive their sin, and will heal their land. It is worth reading in place: "
  "it is God's reply to the captivity petition of chapter 6, addressed to a people who will need "
  "it. The promise to David's line is then repeated to Solomon directly."),
 ("The Terms Attached (vv.19-22)",
  "The appearance does not end on the promise. If ye turn away, and forsake my statutes, and go and "
  "serve other gods, then the outcome is stated in the same specific terms as the blessing: I will "
  "pluck them up by the roots out of my land, and this house, which I have sanctified for my name, "
  "will I cast out of my sight, and will make it to be a proverb and a byword among all nations. "
  "Passers-by will ask why the LORD has done this to this land and to this house, and the answer "
  "will be already known. The Chronicler's readers were living in the aftermath of the second half "
  "of this sentence, on the site of the house it describes."),
],
"2chronicles8": [
 ("Cities Built, Peoples Levied, and Pharaoh's Daughter (vv.1-11)",
  "Twenty years after the building began, the account turns to the rest of the reign, and it is "
  "mostly construction and administration: Hamath-zobah, Tadmor, the two Beth-horons fortified with "
  "walls, gates and bars, Baalath, and the store, chariot and horsemen cities. The labour is "
  "accounted for as carefully as in chapter 2. The remnant of the Hittites, Amorites, Perizzites, "
  "Hivites and Jebusites are made bondservants, and of the children of Israel Solomon made no "
  "servants, they were men of war and officers. Verse 11 records a scruple that only Chronicles "
  "keeps: Pharaoh's daughter is moved out of the city of David, because the places are holy "
  "whereunto the ark of the LORD hath come."),
 ("The Ordered Worship, and the Voyage to Ophir (vv.12-18)",
  "The chapter's second half is about worship running to a schedule, which is the Chronicler's "
  "recurring test of a reign. Offerings by the daily rate, on the sabbaths, the new moons and the "
  "three solemn feasts, and the courses of priests and Levites set exactly as David the man of God "
  "had commanded, with the porters at every gate. The verdict is given in a single clause, they "
  "departed not from the commandment of the king. The last verses reach much further out, to "
  "Ezion-geber on the Red Sea, where Huram's sailors and Solomon's servants go to Ophir together "
  "and bring back four hundred and fifty talents of gold."),
],
"2chronicles9": [
 ("The Queen of Sheba (vv.1-12)",
  "She comes with hard questions and a very great train, and what undoes her is not the answers but "
  "the arrangements, the house, the food on the table, the seating of the servants, the dress of "
  "the attendants and the ascent by which the king went up to the house of the LORD. There was no "
  "more spirit in her. Her speech concedes more than a state visit requires, it was a true report, "
  "and behold, the half of the greatness of thy wisdom was not told me, and she credits it where "
  "the Chronicler wants it credited, blessed be the LORD thy God, which delighted in thee to set "
  "thee on his throne, to be king for the LORD thy God. Jesus refers to this visit in Matthew 12 "
  "and makes her the standard against which his own hearers are measured."),
 ("The Weight of Gold and the Ivory Throne (vv.13-21)",
  "The wealth is now given in figures: six hundred threescore and six talents of gold in a single "
  "year, beside what the traders and governors brought. Two hundred targets and three hundred "
  "shields of beaten gold hang in the house of the forest of Lebanon. The throne is the centrepiece, "
  "ivory overlaid with pure gold, six steps with a golden footstool, lions beside the stays and "
  "twelve more on the steps, and the assessment attached to it, there was not the like made in any "
  "kingdom. Silver is nothing accounted of. Every three years the ships of Tarshish come in with "
  "gold, silver, ivory, apes and peacocks."),
 ("Solomon's Renown, His Sources and His Death (vv.22-31)",
  "The summary is superlative throughout, all the kings of the earth sought the presence of "
  "Solomon, and the horses and stalls are counted one more time. Then the Chronicler names his "
  "sources, and they are books nobody now has: the book of Nathan the prophet, the prophecy of "
  "Ahijah the Shilonite, and the visions of Iddo the seer. Forty years, buried in the city of "
  "David, Rehoboam reigns in his place. What is not here is the point. 1 Kings 11 gives a full "
  "chapter to the foreign wives, the high places and the adversaries raised up against Solomon, "
  "and Chronicles passes over all of it. A book written to persuade a small returned community that "
  "the temple and the house of David were worth their loyalty tells the story that serves that "
  "purpose."),
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
        # Compare div counts across the pane only. Another session may be editing
        # other tabs in this working tree and its state must not decide whether
        # this splice is sound.
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
