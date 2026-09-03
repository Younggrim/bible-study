#!/usr/bin/env python3
"""
2 Chronicles 21 to 28: from Jehoram to Ahaz. Eight pages, 167 verses, two book fields
each and no sublists.

This is the worst stretch of Judah's history and the Chronicler tells it as a sequence
of reigns that begin one way and end another. Joash repairs the temple and then has the
son of the priest who saved him stoned in its court. Amaziah dismisses hired troops on
a prophet's word and then brings home the gods of the people he beat. Uzziah is
marvellously helped until he is strong, and then walks into the holy place with a
censer. The pattern is not incidental; it is the argument of the book, and the section
labels follow the turn rather than smoothing it over.

Two things in these chapters exist nowhere else in scripture. Elijah writes a letter,
at 21:12, his only appearance in Chronicles. And at 28:9-15 a northern prophet stops a
victorious army and sends its captives home clothed, fed and carried, which is the
passage in the Old Testament that stands closest in shape to the parable of the good
Samaritan. The block ends with the doors of the temple shut, which is what gives
Hezekiah's first act in chapter 29 its force.

Usage:
    python3 fold_2chronicles_kings.py [--check]
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
"2chronicles21": [
 ("Jehoram Kills His Brothers, and Judah Follows Israel (vv.1-11)",
  "Jehoshaphat had given his younger sons silver, gold, precious things and fenced cities, and given "
  "the kingdom to Jehoram as the firstborn. The first thing Jehoram does when he is strengthened is "
  "kill all of them, and divers of the princes of Israel with them. The marriage explains the "
  "direction of the reign, he had the daughter of Ahab to wife, and he walked in the way of the "
  "kings of Israel. Set against that is the sentence that keeps the book from being simply a ledger "
  "of deserts, howbeit the LORD would not destroy the house of David, because of the covenant that "
  "he had made, and as he promised to give a light to him and to his sons for ever. What follows is "
  "loss of territory, Edom revolting and setting up its own king, Libnah revolting, and high places "
  "built in the mountains of Judah."),
 ("Elijah's Letter, and a Death Without Mourning (vv.12-20)",
  "A writing comes to Jehoram from Elijah the prophet. It is Elijah's only appearance in Chronicles "
  "and the only letter attributed to him anywhere, and it is an indictment in two counts: he has "
  "not walked in the ways of Jehoshaphat or Asa but in the way of the kings of Israel, and he has "
  "killed his brothers. The sentence names what will be taken in the order it will be taken, the "
  "people, the children, the wives and the goods, and then a great sickness in his own bowels. Both "
  "halves arrive. The Philistines and Arabians carry off his substance, his sons and his wives, "
  "leaving only the youngest. Then the disease, incurable, and after two years his bowels fell out. "
  "The Chronicler measures the reign by the funeral, his people made no burning for him like the "
  "burning of his fathers, and he was buried in the city of David but not in the sepulchres of the "
  "kings."),
],
"2chronicles22": [
 ("Ahaziah, and the House of Ahab's Counsel (vv.1-9)",
  "Ahaziah reigns because there is nobody older left; the raiders had killed his elder brothers. "
  "The Chronicler gives his age at accession as forty-two where 2 Kings 8:26 gives twenty-two, one "
  "of the clearest numerical differences between the two books and generally treated as a copying "
  "error in one or the other. His mother Athaliah is named as his counsellor to do wickedly, so the "
  "line from Ahab now runs through the palace itself. He rides out with Jehoram of Israel against "
  "Hazael, and the visit is where his reign ends: the destruction of Ahaziah was of God, in that he "
  "went to Joram, because Jehu had been anointed to cut off the house of Ahab and Ahaziah was "
  "standing in it. He is found hiding in Samaria and killed, and given a burial only because he is "
  "the son of Jehoshaphat."),
 ("Athaliah Destroys the Seed Royal, and Joash Is Hidden (vv.10-12)",
  "Three verses hold the narrowest point in the whole book. Athaliah destroys all the seed royal of "
  "the house of Judah, which is an attempt to end the line the covenant of chapter 21 was made "
  "with. What survives it is one infant, taken by Jehoshabeath, the king's daughter and the wife of "
  "Jehoiada the priest, and hidden in a bedchamber and then in the house of God for six years while "
  "Athaliah reigns over the land. The Davidic promise spends six years as a child concealed inside "
  "the temple, and the two institutions this book cares about most are keeping each other alive."),
],
"2chronicles23": [
 ("The Covenant with the Captains, and the Crowning in the Temple (vv.1-11)",
  "In the seventh year Jehoiada moves, and Chronicles describes the operation differently from "
  "2 Kings 11. Kings has a palace-guard coup. Here the five captains of hundreds are brought into "
  "covenant and then sent round the cities of Judah to gather the Levites and the chief of the "
  "fathers, so what assembles in Jerusalem is a national religious body, and the agreement it makes "
  "cites the promise, behold, the king's son shall reign, as the LORD hath said of the sons of "
  "David. The deployment is by priestly courses, with porters at the doors and a rule enforced "
  "throughout, none to come into the house of the LORD but the priests and the ministering Levites, "
  "for they are holy. Then the crown is put on the boy, the testimony given into his hand, and the "
  "shout, God save the king."),
 ("Athaliah's Cry, and the Covenant Renewed (vv.12-21)",
  "Athaliah hears the noise, comes into the house of the LORD, sees the king standing by his pillar "
  "with the captains and the trumpeters and the singers, and calls it what it is from where she "
  "stands, Treason, treason. Jehoiada's order is careful about place, take her out of the ranges, "
  "and she is killed at the entering of the horse gate rather than in the temple. What follows is "
  "reconstruction on three fronts. A covenant that the king and the people should be the LORD's "
  "people. The house of Baal pulled down, its altars and images broken and its priest killed before "
  "them. And the offices of the house of the LORD restored to the priests and Levites as it is "
  "written in the law of Moses, with porters set at the gates. The chapter ends on the result rather "
  "than the drama, all the people of the land rejoiced, and the city was quiet."),
],
"2chronicles24": [
 ("The Chest at the Gate, and the House Repaired (vv.1-14)",
  "Joash is seven when he begins, and the verdict on him is bounded by a lifetime, he did that which "
  "was right in the sight of the LORD all the days of Jehoiada the priest. His project is the "
  "temple, and the reason it needs one is given plainly: the sons of Athaliah had broken up the "
  "house of God and spent the dedicated things on Baalim. His first method fails, an instruction to "
  "the Levites to collect from the cities yearly, and the text says why without excusing anyone, the "
  "Levites hastened it not. The second method works, and it works because it removes the "
  "intermediary. A chest is set outside at the gate, the tax that Moses laid on Israel in the "
  "wilderness is proclaimed, and the princes and all the people cast in willingly until they had "
  "made an end. Masons, carpenters and workers in iron and brass set the house in its state, and "
  "what is left over is made into vessels."),
 ("Jehoiada Dies, and Zechariah Is Stoned in the Court (vv.15-22)",
  "Jehoiada dies at a hundred and thirty and is buried among the kings, because he had done good in "
  "Israel, the only man in Chronicles who is not a king given a royal burial. What the previous "
  "section's careful phrasing was pointing at now happens. The princes come and make obeisance, the "
  "king hearkens to them, and Judah leaves the house of the LORD for groves and idols. Prophets are "
  "sent and are not heard. Then the Spirit of God comes on Zechariah, Jehoiada's son, who states the "
  "principle and is killed for it: because ye have forsaken the LORD, he hath also forsaken you. He "
  "is stoned in the court of the house of the LORD at the king's own commandment, and the "
  "Chronicler adds the detail that makes it unbearable, Joash remembered not the kindness which "
  "Jehoiada his father had done to him. His dying words are not forgiveness, the LORD look upon it, "
  "and require it. When Jesus speaks in Matthew 23 of a Zechariah killed between the temple and the "
  "altar, this is the murder most readers take him to mean, and since Chronicles stands last in the "
  "Hebrew order, naming it reaches from one end of the canon to the other."),
 ("The Syrian Raid, and the King Killed in His Bed (vv.23-27)",
  "The reckoning is quick and the Chronicler makes the disproportion the point: the host of Syria "
  "came up with a small company of men, and the LORD delivered a very great host into their hand, "
  "because they had forsaken the LORD God of their fathers. They leave Joash in great diseases, and "
  "his own servants finish it, and the motive is stated, for the blood of the sons of Jehoiada the "
  "priest. He is killed on his bed and buried in the city of David but not in the sepulchres of the "
  "kings, the same distinction drawn over Jehoram three chapters earlier."),
],
"2chronicles25": [
 ("The Hired Israelites Sent Home, and the Valley of Salt (vv.1-13)",
  "Amaziah gets the book's most exact verdict, he did that which was right in the sight of the LORD, "
  "but not with a perfect heart, and the chapter is a demonstration of what that means. He begins "
  "well twice over. He executes his father's murderers but not their children, and the Chronicler "
  "cites the statute he is obeying, every man shall die for his own sin. And when a man of God tells "
  "him to send home the hundred thousand Israelite troops he has hired, he obeys, though his "
  "objection is entirely about the money already spent, but what shall we do for the hundred "
  "talents. The answer is the chapter's best line, the LORD is able to give thee much more than "
  "this. He wins in the valley of salt. The dismissed troops, meanwhile, sack the cities of Judah on "
  "their way north, so obedience costs something and the text does not hide it."),
 ("The Gods of Edom, and the Challenge to Joash (vv.14-28)",
  "What he brings back from the victory is the difficulty: he sets up the gods of the children of "
  "Seir and bows to them, which is worship of the losing side's deities and is left standing as "
  "absurd without comment. The prophet who says so is cut off mid-sentence, Art thou made of the "
  "king's counsel, forbear, and answers with a diagnosis rather than a threat, I know that God hath "
  "determined to destroy thee, because thou hast not hearkened unto my counsel. The war with Israel "
  "that follows is provoked by Amaziah, and Joash's reply is a fable about a thistle sending to a "
  "cedar, with the reading attached, thine heart lifteth thee up to boast, abide now at home. Judah "
  "is beaten at Beth-shemesh, the king is captured, four hundred cubits of Jerusalem's wall are "
  "broken down and the temple vessels carried to Samaria. He is finally killed at Lachish by his own "
  "people, and the Chronicler dates the conspiracy from the turn, after the time that Amaziah did "
  "turn away from following the LORD."),
],
"2chronicles26": [
 ("The Reign That Prospered, and the Engines on the Towers (vv.1-15)",
  "Uzziah's fifty-two years are the most prosperous in the book after Solomon's, and the condition "
  "is stated as a duration rather than a character trait, as long as he sought the LORD, God made "
  "him to prosper. The prosperity is itemised in a way that reads like a state record. Gath, Jabneh "
  "and Ashdod broken down and Judean towns built in Philistine territory. Ammonite tribute. Towers "
  "in Jerusalem and towers in the desert, wells dug for large herds, vine dressers in the mountains, "
  "and a note that explains the interest, for he loved husbandry. An army of three hundred and seven "
  "thousand five hundred under twenty-six hundred officers, with armouries stocked to match. And "
  "engines devised by skilful men and mounted on the towers to shoot arrows and great stones, which "
  "is the earliest description of artillery in the Bible. The section ends on the hinge, his name "
  "spread far abroad, for he was marvellously helped, till he was strong."),
 ("The Censer in the Temple, and the Leprosy (vv.16-23)",
  "But when he was strong, his heart was lifted up to his destruction. The offence is specific and "
  "the Chronicler treats it as a boundary violation rather than as unbelief: he goes into the temple "
  "to burn incense on the altar of incense, which is priestly work. Azariah and fourscore priests go "
  "in after him and say so, it appertaineth not unto thee, Uzziah, to burn incense unto the LORD, "
  "but to the priests the sons of Aaron. He is standing there angry with the censer in his hand when "
  "the leprosy rises in his forehead, and the rest of his life is the sentence: thrust out, a leper "
  "until the day of his death, living in a several house, cut off from the house of the LORD he had "
  "tried to serve in, with his son running the kingdom. Isaiah wrote the record of his reign, and it "
  "is in the year of Uzziah's death that Isaiah sees the LORD sitting on a throne in the temple. He "
  "is buried in the field belonging to the kings rather than in their sepulchres, for they said, He "
  "is a leper."),
],
"2chronicles27": [
 ("Jotham's Accession, and the Line He Did Not Cross (vv.1-4)",
  "Jotham's summary is written against his father's, and one clause carries the whole comparison, he "
  "did that which was right in the sight of the LORD, according to all that his father Uzziah did, "
  "howbeit he entered not into the temple of the LORD. He built where his father had built, the high "
  "gate of the house of the LORD, a great deal on the wall of Ophel, cities in the mountains of "
  "Judah, castles and towers in the forests. The one qualification in the section is not about him, "
  "and the Chronicler puts it in the same breath as the praise, the people did yet corruptly, which "
  "is his standing observation that a good king does not by himself make a faithful nation."),
 ("The Ammonite Tribute, and a Verdict Without Qualification (vv.5-9)",
  "He fights the king of the Ammonites and wins, and the tribute is specified for three years "
  "running, a hundred talents of silver, ten thousand measures of wheat and ten thousand of barley. "
  "Then the verdict, and it is the only one in this whole block of chapters with nothing subtracted "
  "from it, so Jotham became mighty, because he prepared his ways before the LORD his God. Sixteen "
  "years, buried in the city of David, and Ahaz his son reigns. The brevity is itself worth "
  "noticing: this book spends its length on collapse and recovery, so the king with the cleanest "
  "record gets nine verses while the king who fails in the next chapter gets twenty-seven."),
],
"2chronicles28": [
 ("Ahaz, the Defeats, and Oded's Word at Samaria (vv.1-15)",
  "Ahaz is the low point. He walks in the ways of the kings of Israel, makes molten images for "
  "Baalim, burns incense in the valley of the son of Hinnom, and burnt his children in the fire, "
  "which is the practice the law had named as the reason the previous inhabitants were expelled. The "
  "losses come from both directions, Syria and Israel, and the figures are given with a cause "
  "attached, Pekah slew in Judah a hundred and twenty thousand in one day, because they had forsaken "
  "the LORD God of their fathers, along with the king's son and the two chief officers of his "
  "household. Then two hundred thousand captives are marched north, and the section turns "
  "completely. Oded the prophet meets the victorious army at Samaria and stops it with an argument "
  "about proportion and about their own record, ye have slain them in a rage that reacheth up unto "
  "heaven, and are there not with you also sins against the LORD your God. Four named men of Ephraim "
  "stand up, and the captives are clothed, shod, fed, anointed, the feeble set on asses, and taken "
  "to their brethren at Jericho. It is Chronicles' own episode, and no passage in the Old Testament "
  "stands nearer to the parable of the good Samaritan."),
 ("The Appeal to Assyria, and the Altar from Damascus (vv.16-27)",
  "Ahaz's answer to being attacked from two sides is to send for a third party, and the Chronicler's "
  "assessment of the result is four words long, but he helped him not. Tilgath-pilneser comes and "
  "distresses him, and Ahaz strips the house of the LORD and the houses of the king and the princes "
  "to pay for it. The reasoning that follows is the clearest statement of pagan logic in the book, "
  "and it is offered as the king's own: because the gods of the kings of Syria help them, therefore "
  "will I sacrifice to them, that they may help me. He is sacrificing to the gods of the army that "
  "beat him, and the verdict is immediate, but they were the ruin of him, and of all Israel. The "
  "chapter closes with the temple vessels cut in pieces, altars in every corner of Jerusalem, high "
  "places in every city, and the doors of the house of the LORD shut. That is where Hezekiah finds "
  "it in the next chapter, and it is why his first act is to open it."),
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
