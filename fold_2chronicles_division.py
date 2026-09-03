#!/usr/bin/env python3
"""
2 Chronicles 10 to 20: the kingdom divides, and four kings of Judah. Eleven pages,
215 verses, two book fields each and no sublists, so the fields are kept and the
sections are written new.

From chapter 10 the Chronicler stops following the northern kingdom. Kings tells both
stories in parallel; Chronicles keeps Judah and lets Israel appear only when it walks
into Judah's story, as Jeroboam does at chapter 13 and Ahab at chapter 18. That is why
these pages read as a sequence of reigns tested one at a time.

Several of these chapters have material that exists nowhere else, and the sections say
where. Abijah's speech from mount Zemaraim, the priests and Levites migrating south
from Jeroboam's shrines, Jehoshaphat's circuit of teachers carrying the book of the
law, his court system with its explicit separation of the LORD's matters from the
king's, and the singers sent out in front of the army at Berachah are all Chronicles
alone. The same writer also supplies the sharpest reversals in the book: Asa prays at
Mareshah and wins, then buys Syrian help and imprisons the seer who says so.

Usage:
    python3 fold_2chronicles_division.py [--check]
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
"2chronicles10": [
 ("The Petition at Shechem, and the Two Counsels (vv.1-11)",
  "Rehoboam goes to Shechem to be made king and is met with a negotiation instead of an "
  "acclamation. Jeroboam comes back from Egypt for it, and the request is economic, ease thou "
  "somewhat the grievous servitude of thy father, and his heavy yoke, and we will serve thee. "
  "Rehoboam takes three days and asks twice. The old men who had stood before Solomon tell him to "
  "be kind to this people and please them, and they will be thy servants for ever, which treats "
  "loyalty as something bought with concession. The men he grew up with tell him to escalate, and "
  "give him the line he will use, my little finger shall be thicker than my father's loins."),
 ("The Rough Answer, and the Break (vv.12-19)",
  "He answers with the young men's words, and the Chronicler stops the narrative to say who is "
  "behind it, so the king hearkened not unto the people, for the cause was of God, that the LORD "
  "might perform his word which he spake by the hand of Ahijah the Shilonite to Jeroboam. The "
  "reply Israel gives is a formal renunciation, What portion have we in David, and none inheritance "
  "in the son of Jesse, every man to your tents, O Israel. Rehoboam's last miscalculation is to "
  "send Hadoram, who was over the levy, to collect it; he is stoned to death, and the king leaves "
  "for Jerusalem in a chariot. The division is stated as permanent, unto this day."),
],
"2chronicles11": [
 ("The War Called Off, and the Cities Fortified (vv.1-12)",
  "Rehoboam musters a hundred and eighty thousand chosen men to take the north back by force, and "
  "is stopped by a word from Shemaiah the man of God, Ye shall not go up, nor fight against your "
  "brethren, return every man to his house, for this thing is done of me. They obey, which is the "
  "one thing this reign does well. What he builds instead is a defensive ring, and the Chronicler "
  "names all fifteen cities, Bethlehem, Etam, Tekoa, Beth-zur, Shoco, Adullam, Gath, Mareshah, "
  "Ziph, Adoraim, Lachish, Azekah, Zorah, Aijalon and Hebron, each with a captain, stores of "
  "victual, oil and wine, and shields and spears. Judah is settling for being a small state that "
  "can hold its ground."),
 ("The Priests and Levites Move South (vv.13-17)",
  "This is Chronicles' own account of how legitimate worship ended up concentrated in Judah, and it "
  "is a story of migration rather than of policy. Jeroboam had cast the Levites off from executing "
  "the priest's office and appointed his own priests for the high places, for the calves he had "
  "made. So the priests and Levites out of all Israel resorted to Rehoboam, leaving their suburbs "
  "and their possession, and with them everyone out of the northern tribes who set his heart to "
  "seek the LORD God of Israel. The effect is stated in political terms, they strengthened the "
  "kingdom of Judah for three years, because a state gains something when the people who care most "
  "about its religion move into it."),
 ("The Household, and the Naming of an Heir (vv.18-23)",
  "The chapter closes with a register of the family: the wives Mahalath and Maachah, then eighteen "
  "wives and threescore concubines, twenty-eight sons and threescore daughters. The last verses "
  "describe a deliberate succession policy. Abijah is made chief among his brethren and marked out "
  "to be king, and the rest of the sons are dispersed throughout all the countries of Judah and "
  "Benjamin, given fenced cities, victual in abundance and many wives. Distributing the potential "
  "rivals across the kingdom with enough comfort to keep them content is a working solution to the "
  "problem that had destroyed the united monarchy."),
],
"2chronicles12": [
 ("Shishak Comes Up, and Shemaiah's Word (vv.1-8)",
  "The verdict is given before the invasion, and the order matters: when Rehoboam had established "
  "the kingdom and strengthened himself, he forsook the law of the LORD. In the fifth year Shishak "
  "of Egypt comes with twelve hundred chariots, sixty thousand horsemen and troops out of Libya, "
  "Sukkiim and Ethiopia, takes the fenced cities and reaches Jerusalem. Shishak is generally "
  "identified with Shoshenq I, whose campaign into Palestine is recorded on a relief at Karnak, "
  "which makes this one of the earliest points where the biblical narrative and Egyptian records "
  "touch. Shemaiah states the principle in one line, Ye have forsaken me, and therefore have I also "
  "left you. The princes and the king humble themselves and say, The LORD is righteous, and the "
  "sentence is reduced rather than cancelled: they will be Shishak's servants, that they may know "
  "the difference between the two services."),
 ("The Golden Shields Replaced with Brass (vv.9-16)",
  "Shishak takes the treasures of the house of the LORD and the treasures of the king's house, "
  "including the shields of gold Solomon had made, and Rehoboam replaces them with shields of "
  "brass. Everything else in the chapter is summary; that one substitution is the picture. Judah "
  "keeps the ceremony, the guard still carries the shields when the king goes into the house of the "
  "LORD, and the metal has changed. The rest is the formal close of the reign: he did evil, for he "
  "prepared not his heart to seek the LORD, the acts are in the book of Shemaiah the prophet and "
  "Iddo the seer, there was war with Jeroboam continually, seventeen years, and Abijah reigned in "
  "his stead."),
],
"2chronicles13": [
 ("Abijah's Speech from Mount Zemaraim (vv.1-12)",
  "Kings gives Abijah three verses and says his heart was not perfect with the LORD. Chronicles "
  "gives him a battlefield address, standing on mount Zemaraim with four hundred thousand men "
  "against Jeroboam's eight hundred thousand, and the speech is the most compact statement of the "
  "book's own theology anywhere in it. The kingdom was given to David and his sons for ever by a "
  "covenant of salt. Jeroboam took his opportunity while Rehoboam was young and tenderhearted. And "
  "the charge that carries the most weight is about worship rather than about politics: the north "
  "cast out the sons of Aaron and made priests of anyone who turned up with a young bullock and "
  "seven rams. As for us, the LORD is our God, and we have not forsaken him, and behold, God himself "
  "is with us for our captain."),
 ("The Ambush, the Cry and the Rout (vv.13-22)",
  "Jeroboam answers the speech by sending men around behind, so Judah is attacked from both sides "
  "at once, and the outcome turns on two actions taken in that moment. Judah cried unto the LORD, "
  "and the priests sounded with the trumpets. The Chronicler states the causation without hedging, "
  "God smote Jeroboam and all Israel before Abijah and Judah, and the children of Judah prevailed, "
  "because they relied upon the LORD God of their fathers. The casualty figure of five hundred "
  "thousand chosen men is of the order that has led many readers to treat the Chronicler's large "
  "numbers as conventional rather than as a count. Bethel, Jeshanah and Ephrain change hands, and "
  "Jeroboam never recovers strength."),
],
"2chronicles14": [
 ("Asa's Reforms, and the Quiet Years (vv.1-8)",
  "Asa inherits a land at rest and spends the peace on two things. The first is demolition, and the "
  "list is specific: the altars of the strange gods, the high places, the images broken, the groves "
  "cut down, with a positive instruction beside it, he commanded Judah to seek the LORD God of "
  "their fathers, and to do the law and the commandment. The second is construction, and the "
  "Chronicler puts the causation in the king's own mouth, let us build these cities while the land "
  "is yet before us, because we have sought the LORD our God, and he hath given us rest. The "
  "chapter ends by counting the army, three hundred thousand of Judah with targets and spears and "
  "two hundred and eighty thousand of Benjamin with shields and bows."),
 ("Zerah the Ethiopian, and the Prayer at Mareshah (vv.9-15)",
  "Zerah comes up with a host the text puts at a thousand thousand and three hundred chariots, and "
  "the battle is set in the valley at Mareshah. Verse 11 is the centre of the chapter and the "
  "reason it is remembered, and it argues from God's indifference to odds, LORD, it is nothing with "
  "thee to help, whether with many, or with them that have no power. Then it makes the fight "
  "God's own rather than Judah's, we rest on thee, and in thy name we go against this multitude, "
  "let not man prevail against thee. The rout runs as far as Gerar, and the spoil is livestock, "
  "tents of cattle and sheep and camels in abundance. This prayer is the measure that chapter 16 "
  "will be judged against."),
],
"2chronicles15": [
 ("Azariah's Word to Asa (vv.1-7)",
  "The Spirit of God comes on Azariah the son of Oded, and he meets the returning army with a "
  "conditional rather than a congratulation, The LORD is with you, while ye be with him, and if ye "
  "seek him, he will be found of you, but if ye forsake him, he will forsake you. What follows is a "
  "description of what the alternative looks like, drawn in the language of the period of the "
  "judges: no peace to him that went out, nor to him that came in, nation against nation and city "
  "against city. The word ends as an instruction rather than a threat, be ye strong therefore, and "
  "let not your hands be weak, for your work shall be rewarded."),
 ("The Covenant at the Feast, and Maachah Deposed (vv.8-19)",
  "Asa takes courage from the word and goes further than his first reform, clearing the abominable "
  "idols out of Judah, Benjamin and the cities he had taken from Ephraim, and renewing the altar "
  "before the porch. Then, in the third month of the fifteenth year, seven hundred oxen and seven "
  "thousand sheep are offered and the assembly enters a covenant to seek the LORD with all their "
  "heart and all their soul, sworn with a loud voice, with shouting, trumpets and cornets. Two "
  "measured results follow, all Judah rejoiced at the oath, and the LORD gave them rest round "
  "about. The reform then reaches his own household: Maachah is removed from being queen because of "
  "her idol, which he cuts down and burns at the brook Kidron. The verdict is qualified, the high "
  "places were not all taken away, nevertheless the heart of Asa was perfect all his days."),
],
"2chronicles16": [
 ("The League with Ben-hadad (vv.1-6)",
  "Baasha of Israel fortifies Ramah to close the road into Judah, and Asa's answer this time is "
  "purchased rather than prayed for. He takes silver and gold out of the treasures of the house of "
  "the LORD and out of the king's house and sends it to Ben-hadad of Syria with an instruction, "
  "break thy league with Baasha king of Israel, that he may depart from me. It works exactly as "
  "intended. Syria strikes Ijon, Dan, Abel-maim and the store cities of Naphtali, Baasha abandons "
  "the building work, and Asa carries away the stones and timber Baasha had gathered and uses them "
  "to build Geba and Mizpah. Nothing in the account suggests the policy failed, which is what makes "
  "the next section sharp."),
 ("Hanani's Rebuke, and the Diseased Feet (vv.7-14)",
  "Hanani the seer arrives to say the successful policy was a loss, because thou hast relied on the "
  "king of Syria, and not on the LORD thy God, therefore is the host of the king of Syria escaped "
  "out of thine hand. His argument is the king's own history, were not the Ethiopians and the "
  "Lubims a huge host, and the outcome then rested on a different reliance. The sentence that "
  "generalises it is the best known line in Chronicles after 7:14, the eyes of the LORD run to and "
  "fro throughout the whole earth, to shew himself strong in the behalf of them whose heart is "
  "perfect toward him. Asa puts him in the stocks. Three years before his death he is diseased in "
  "his feet, and the Chronicler's note is not against physicians but about order, he sought not to "
  "the LORD, but to the physicians. He is buried with a very great burning."),
],
"2chronicles17": [
 ("Jehoshaphat Strengthened (vv.1-6)",
  "The reign opens with garrisons in the cities of Judah and in the cities of Ephraim which Asa had "
  "taken, and with a verdict given early, the LORD was with Jehoshaphat, because he walked in the "
  "first ways of David his father. The qualifier first is doing work: it is Asa before the Syrian "
  "league and David before Bathsheba that are being held up. He sought not unto Baalim, and he took "
  "away the high places and groves out of Judah, which is stated here and qualified again at "
  "20:33, where they are back. The last clause of verse 6 is the one the Chronicler uses for this "
  "king throughout, his heart was lifted up in the ways of the LORD."),
 ("The Teaching Circuit, and the Fear on the Nations (vv.7-13)",
  "In the third year he sends out a commission of five princes, nine Levites and two priests, and "
  "the detail that matters is what they carry, they had the book of the law of the LORD with them, "
  "and went about throughout all the cities of Judah, and taught the people. No other king in the "
  "Old Testament organises public instruction in the law as a programme, and the Chronicler treats "
  "it as the foundation of everything that follows in the reign. What follows is quiet borders: the "
  "fear of the LORD fell on the kingdoms round about so that they made no war, the Philistines "
  "brought presents and tribute silver, and the Arabians brought seven thousand seven hundred rams "
  "and as many goats."),
 ("The Muster Roll (vv.14-19)",
  "The chapter ends as a register, counted by houses. Of Judah, Adnah with three hundred thousand "
  "mighty men, Jehohanan with two hundred and eighty thousand, and Amasiah, of whom the text says "
  "he willingly offered himself unto the LORD, with two hundred thousand. Of Benjamin, Eliada with "
  "two hundred thousand armed with bow and shield and Jehozabad with a hundred and eighty thousand, "
  "beside the men the king put in the fenced cities throughout all Judah. The figures are of the "
  "same order as the Chronicler's other musters and are read by many as conventional. What they are "
  "placed here to show is a kingdom secure enough that its king had no need of the alliance he "
  "makes in the next chapter."),
],
"2chronicles18": [
 ("The Alliance, and the Four Hundred Prophets (vv.1-11)",
  "Jehoshaphat joins affinity with Ahab and goes down to Samaria, and when he is asked to help take "
  "Ramoth-gilead he commits before he enquires, I am as thou art, and my people as thy people. Only "
  "then does he ask for a word from the LORD. Four hundred prophets are assembled and all say go "
  "up, and Jehoshaphat's question tells the reader what he thinks of them, Is there not here a "
  "prophet of the LORD besides, that we might enquire of him. Ahab names Micaiah the son of Imla "
  "and gives his own reason for disliking him, he never prophesied good unto me, but always evil. "
  "The scene is set with the two kings on their thrones in a void place at the entering in of the "
  "gate of Samaria, and Zedekiah wearing iron horns."),
 ("Micaiah, the Lying Spirit and the Prison (vv.12-27)",
  "The messenger sent to fetch Micaiah tells him what the other prophets have said and what is "
  "expected of him, and Micaiah answers first with mimicry, Go ye up, and prosper, until Ahab "
  "himself demands the truth. Then two things. A picture, I did see all Israel scattered upon the "
  "mountains, as sheep that have no shepherd, which says the king will not come back. And an "
  "explanation of where the four hundred got their message, the LORD on his throne with the host of "
  "heaven around him, and a spirit that volunteers to be a lying spirit in the mouth of his "
  "prophets. It is one of the hardest passages in the Old Testament and it is offered as an answer "
  "to a question, not as a doctrine. Zedekiah strikes him, and he goes to prison on bread and water "
  "of affliction, with a condition attached, if thou certainly return in peace, then hath not the "
  "LORD spoken by me."),
 ("Ramoth-gilead, the Disguise and the Random Arrow (vv.28-34)",
  "Ahab's precaution is to disguise himself and let Jehoshaphat go into battle in his robes, and it "
  "nearly works. The Syrian chariot captains had orders to fight with none but the king of Israel, "
  "so they surround the wrong man, and Chronicles adds what Kings does not, Jehoshaphat cried out, "
  "and the LORD helped him, and God moved them to depart from him. What kills Ahab is the least "
  "targeted event on the field, a certain man drew a bow at a venture, and smote the king of Israel "
  "between the joints of the harness. He is propped up in his chariot facing the Syrians until "
  "evening and dies about the time of the sun going down. The prophecy is fulfilled by an archer "
  "who was not aiming."),
],
"2chronicles19": [
 ("Jehu's Rebuke on the Road Home (vv.1-3)",
  "Jehoshaphat gets back to Jerusalem in peace and is met by Jehu the son of Hanani with a "
  "question, Shouldest thou help the ungodly, and love them that hate the LORD, therefore is there "
  "wrath upon thee from before the LORD. It is the Chronicler's standing objection to this reign, "
  "and it will be made once more at the end of chapter 20. What follows the rebuke is the shape "
  "this book's verdicts usually take, nevertheless there are good things found in thee, in that "
  "thou hast taken away the groves out of the land, and hast prepared thine heart to seek God. The "
  "assessment is mixed on purpose, and the good is named as specifically as the fault."),
 ("The Courts Set in Order (vv.4-11)",
  "The reply to the rebuke is a reform, and it produces the fullest description of a judicial "
  "system anywhere in the Old Testament. Judges are set in the fenced cities with a charge about "
  "whose court they are sitting in, Take heed what ye do, for ye judge not for man, but for the "
  "LORD, and a standard drawn from God's own conduct, there is no iniquity with the LORD our God, "
  "nor respect of persons, nor taking of gifts. In Jerusalem a higher bench of Levites, priests and "
  "heads of families is appointed, and the jurisdictions are separated explicitly: Amariah the "
  "chief priest over all matters of the LORD, and Zebadiah the ruler of the house of Judah for all "
  "the king's matters, with the Levites as officers before them."),
],
"2chronicles20": [
 ("The Invasion, the Fast and Jehoshaphat's Prayer (vv.1-13)",
  "Moab and Ammon come with others from beyond the sea, and the Chronicler records the king's first "
  "reaction honestly, Jehoshaphat feared, and set himself to seek the LORD, and proclaimed a fast "
  "throughout all Judah. The prayer he makes in the new court is built as a legal argument. It "
  "begins from jurisdiction, rulest not thou over all the kingdoms of the heathen. It cites the "
  "grant of the land to Abraham's seed and the house built for the name, with the promise attached "
  "to it. It points out the irony that these are the very nations Israel was not permitted to "
  "invade on the way in, now come to cast Judah out. And it ends by conceding everything except the "
  "one thing it is asking for, we have no might against this great company that cometh against us, "
  "neither know we what to do, but our eyes are upon thee. All Judah is standing there, with their "
  "little ones, their wives and their children."),
 ("Jahaziel's Answer (vv.14-19)",
  "The Spirit of the LORD comes on Jahaziel in the middle of the congregation, and the answer "
  "reassigns the battle, be not afraid nor dismayed by reason of this great multitude, for the "
  "battle is not yours, but God's. Then it gets specific enough to be acted on: tomorrow go down "
  "against them, they will come up by the cliff of Ziz, and ye shall find them at the end of the "
  "brook before the wilderness of Jeruel. The instruction attached is the hardest part of it, ye "
  "shall not need to fight in this battle, set yourselves, stand ye still, and see the salvation of "
  "the LORD. Jehoshaphat and the people bow to the ground, and the Kohathite and Korhite Levites "
  "stand up to praise with a loud voice on high."),
 ("The Singers Sent Out First, and the Valley of Berachah (vv.20-30)",
  "Early in the morning Jehoshaphat gives the army a sentence to march on, Believe in the LORD your "
  "God, so shall ye be established, believe his prophets, so shall ye prosper. Then he does the "
  "thing no other commander in the Old Testament does, he appoints singers to go out before the "
  "army, praising the beauty of holiness, and saying, Praise the LORD, for his mercy endureth for "
  "ever. The timing is the point, and when they began to sing and to praise, the LORD set "
  "ambushments. The invaders destroy one another, the spoil takes three days to gather, and the "
  "place is named for what happened there, the valley of Berachah, which is to say blessing. They "
  "come home to Jerusalem with psalteries, harps and trumpets, and the fear of God falls on the "
  "surrounding kingdoms."),
 ("The Reign Summed Up, and the Ships Broken (vv.31-37)",
  "The summary is favourable with the usual qualification, he did that which was right in the sight "
  "of the LORD, howbeit the high places were not taken away, for the people had not yet prepared "
  "their hearts unto the God of their fathers. The Chronicler names his source, the book of Jehu "
  "the son of Hanani. And then the reign ends where chapter 18 began, with an alliance. Jehoshaphat "
  "joins himself with Ahaziah of Israel to build ships to go to Tarshish, and Eliezer the son of "
  "Dodavah prophesies against it in one sentence, because thou hast joined thyself with Ahaziah, "
  "the LORD hath broken thy works. The ships were broken and never sailed. The best reign in this "
  "block of chapters closes on the fault it was warned about twice."),
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
