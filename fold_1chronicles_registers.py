#!/usr/bin/env python3
"""
1 Chronicles 1 to 9: the genealogies. Nine pages, 407 verses, no existing sections.

These chapters are a register, not a narrative, and they are sectioned by the
register's own divisions: by line of descent, by tribe, by settlement. Forcing a
story shape onto a list of names would misdescribe what the reader is looking at.
The same decision was made for Joshua's boundary surveys and Leviticus' feast
calendar.

Two things are worth saying about a nine-chapter list of names, and the sections say
them where they apply. First, the Chronicler is writing after the exile for people
who need to prove who they are, so the lists are legal documents about land,
priesthood and the throne rather than antiquarian interest. Second, he interrupts
himself. Jabez gets a prayer in the middle of Judah's families at 4:9-10, Reuben gets
an explanation of a forfeited birthright at 5:1-2, and Ephraim gets a note about sons
killed raiding Gath at 7:21-22. Those interruptions get their own sections because
they are the only places the register stops to explain itself.

Usage:
    python3 fold_1chronicles_registers.py [--check]
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

OPS = {
"1chronicles1": [
 ("", "From Adam to Noah (vv.1-4)",
  "Four verses to cover ten generations, and the Chronicler gives no dates, no ages and no "
  "narrative, only the names. Adam, Sheth, Enosh, and so on to Noah, Shem, Ham and Japheth. "
  "Genesis took five chapters over the same ground. Starting at Adam rather than at Abraham is "
  "the book's opening claim: the people he is writing for belong to a line that runs back to "
  "the first man, not merely to a national founder."),
 ("From Adam to Noah", "The Sons of Japheth, Ham and Shem (vv.5-23)",
  "The table of nations, and the order is deliberately the reverse of the one that matters. "
  "Japheth comes first and is dealt with in four verses, Ham next with the note about Nimrod "
  "and the Philistine and Canaanite peoples, and Shem last and at greatest length. The lines "
  "that lead away from Israel are cleared out of the way before the line that leads to it. "
  "Every people the later chapters fight is placed on this map before any of them appears in a "
  "battle."),
 ("The Sons of Japheth, Ham and Shem", "From Shem to Abraham (vv.24-27)",
  "The narrowing is abrupt. Ten names in four verses, Shem to Abram, with the Chronicler's own "
  "gloss attached to the last of them, Abram, the same is Abraham. From the whole human race in "
  "verse 1 to one man by verse 27, and the method is simply omission: everyone not in the line "
  "has been listed and set aside."),
 ("From Shem to Abraham", "Ishmael and the Sons of Keturah (vv.28-33)",
  "Abraham's other children are recorded in full before Isaac's line is followed, which is the "
  "pattern the whole chapter uses. Ishmael's twelve sons are named, then the six sons of "
  "Keturah with their descendants. The Chronicler is not interested in disputing their claims "
  "or explaining their status. He lists them, and then stops listing them."),
 ("Ishmael and the Sons of Keturah", "Esau, and the Dukes of Edom (vv.34-54)",
  "Twenty-one verses on Edom, which is more than Shem, Ham and Japheth received between them, "
  "and it is the last thing the chapter does before turning to Israel. The sons of Esau, the "
  "sons of Seir, and then a list of kings that reigned in the land of Edom before there reigned "
  "any king over the children of Israel. That clause is doing work: Edom had a monarchy first. "
  "The chapter ends with eleven dukes and then simply stops, and chapter 2 begins with the sons "
  "of Israel."),
],
"1chronicles2": [
 ("", "The Sons of Israel, and the Sons of Judah (vv.1-8)",
  "The twelve sons are listed in one sentence and then eleven of them are set aside for six "
  "chapters. Judah is taken up immediately, and the Chronicler does not tidy the record: Er, "
  "Onan and Shelah are named with the note that Er was evil in the sight of the LORD, and "
  "Pharez and Zerah are recorded as born to Tamar his daughter-in-law. Then Achan appears, "
  "called Achar here, the troubler of Israel, who transgressed in the thing accursed. Two of "
  "the first eight verses of Judah's line record disgrace."),
 ("The Sons of Israel, and the Sons of Judah", "From Ram to David (vv.9-17)",
  "The line the whole book depends on, and it is nine verses long: Ram, Amminadab, Nahshon, "
  "Salma, Boaz, Obed, Jesse. Then the sons of Jesse, and the Chronicler gives seven where "
  "1 Samuel implies eight, with David seventh. His sisters Zeruiah and Abigail are named, which "
  "matters because Joab, Abishai and Asahel are then identified as her sons rather than as "
  "David's officers. The men who run the army for the next twenty chapters are the king's "
  "nephews."),
 ("From Ram to David", "The Sons of Caleb, and Hezron's Line (vv.18-24)",
  "The register turns aside from the royal line to follow Caleb, and the details it keeps are "
  "domestic: wives named, a wife who died, a second marriage at sixty years old. Hur and Uri "
  "and Bezaleel are in this list, and Bezaleel is the craftsman who built the tabernacle in "
  "Exodus. The Chronicler mentions no craft and no tabernacle. He is establishing that the man "
  "belonged to Judah."),
 ("The Sons of Caleb, and Hezron's Line", "The Sons of Jerahmeel (vv.25-41)",
  "Seventeen verses on a branch of Judah that produces nobody famous. The interest is "
  "territorial rather than biographical, because these are the families who held land in the "
  "Negev around Jerahmeel and Jerahmeelite territory that 1 Samuel places on Judah's southern "
  "edge. Two details survive the list: Sheshan had no sons but daughters, and gave one to an "
  "Egyptian servant, which the register records without comment."),
 ("The Sons of Jerahmeel", "Caleb's Families and the Towns (vv.42-55)",
  "The last section of the chapter turns names into places. The sons of Caleb are given as "
  "fathers of towns, the father of Ziph, the father of Hebron, the father of Bethlehem, which is "
  "how a genealogy records settlement rather than parentage. Kirjath-jearim, Bethlehem and "
  "Netophah are all placed here. The closing verse names the families of the scribes which "
  "dwelt at Jabez, and adds that they were Kenites, an outside people written into Judah's "
  "record."),
],
"1chronicles3": [
 ("", "The Sons of David (vv.1-9)",
  "The royal children are divided by where they were born, six at Hebron by six named mothers, "
  "and then the sons born at Jerusalem. Bathsheba is named as Bath-shua the daughter of Ammiel, "
  "and Solomon is fourth in her list of four. The Chronicler adds a summary count and one "
  "clause that keeps the record honest, these were all the sons of David, beside the sons of the "
  "concubines, and Tamar their sister. Amnon, Absalom and Adonijah are all in this list and "
  "nothing about what they did is recorded here."),
 ("The Sons of David", "Solomon to Josiah (vv.10-14)",
  "The line of kings, and it is five verses of names with nothing else attached. Fourteen "
  "reigns, some of them the worst in Judah's history and some the best, and the register makes "
  "no distinction between them at all. Azariah appears where other books use Uzziah. What the "
  "list is doing is proving continuity: one unbroken succession from the temple builder to the "
  "last good king before the collapse."),
 ("Solomon to Josiah", "Josiah to the Captivity (vv.15-16)",
  "Two verses covering the years the throne changed hands four times under Egyptian and then "
  "Babylonian pressure. Josiah's four sons are named, which no other book does in one place, "
  "and then Jeconiah. The register runs straight through the end of the kingdom without marking "
  "it, and the reader is left to notice that the names simply continue."),
 ("Josiah to the Captivity", "The Line of Jeconiah After the Exile (vv.17-24)",
  "Eight verses that only exist because the Chronicler is writing long after the throne is "
  "gone. Jeconiah is labelled Assir, the captive. Then Zerubbabel, who rebuilt the temple in "
  "Ezra, appears here as a name in a family list. The line continues for six more generations "
  "past him, ending with names that appear nowhere else in scripture. That is the point of the "
  "whole chapter: the house of David has no throne and still has a documented heir."),
],
"1chronicles4": [
 ("", "The Families of Judah (vv.1-8)",
  "The register returns to Judah for a set of families it has not yet covered, and the entries "
  "are terse to the point of obscurity. Names are given as fathers of towns, and occupations "
  "appear without explanation. What holds the section together is not descent from a single man "
  "but occupation of a single region."),
 ("The Families of Judah", "The Prayer of Jabez (vv.9-10)",
  "Two verses in which the register stops dead and quotes somebody. Jabez is introduced by the "
  "meaning of his name, because I bare him with sorrow, and then by a prayer: oh that thou "
  "wouldest bless me indeed, and enlarge my coast, and that thine hand might be with me, and "
  "that thou wouldest keep me from evil. God granted him that which he requested. Nothing else "
  "about the man is recorded, no father, no descendants, no dates. Nine chapters of names "
  "contain one prayer, and it is his."),
 ("The Prayer of Jabez", "Further Families of Judah (vv.11-23)",
  "The list resumes and the entries become occupational. Craftsmen are recorded by trade, the "
  "valley of Charashim being the valley of craftsmen, and there are families of linen workers "
  "and potters who dwelt with the king for his work. A genealogy that records who made things "
  "is unusual, and it tells you the register was compiled for a community that needed to know "
  "which families held which trades."),
 ("Further Families of Judah", "The Sons of Simeon (vv.24-43)",
  "Simeon's section is longer than the tribe's later prominence would suggest and it is mostly "
  "about land. The towns are listed, with the note that these were their cities unto the reign "
  "of David, and the Chronicler observes that their families did not multiply like the children "
  "of Judah. Then two raids are recorded, one into the valley of Gedor for pasture and one "
  "against the Amalekites in mount Seir, both dated to the days of Hezekiah. The tribe absorbed "
  "into Judah is given its own record of taking ground."),
],
"1chronicles5": [
 ("", "Reuben's Forfeited Birthright (vv.1-10)",
  "The register interrupts itself in its first two verses to explain a demotion. Reuben was the "
  "firstborn, but forasmuch as he defiled his father's bed, his birthright was given unto the "
  "sons of Joseph, and the Chronicler adds the further complication that the genealogy is not "
  "to be reckoned after the birthright, for Judah prevailed above his brethren. Two tribes "
  "divide what one man lost, Joseph taking the double portion and Judah the rule. Then the "
  "line, ending with Beerah whom Tilgath-pilneser carried away captive."),
 ("Reuben's Forfeited Birthright", "The Sons of Gad (vv.11-17)",
  "Gad is recorded by territory before family, they dwelt over against them in the land of "
  "Bashan unto Salcah, and the list of names is short. The section closes with a note on method "
  "that is worth having: all these were reckoned by genealogies in the days of Jotham king of "
  "Judah. The Chronicler is telling the reader which census he is copying from."),
 ("The Sons of Gad", "The War Against the Hagarites (vv.18-22)",
  "Five verses of narrative in the middle of a list, and they read like an argument. Forty-four "
  "thousand seven hundred and sixty men able to bear buckler and sword, and they made war with "
  "the Hagarites, and they were helped against them, and the Hagarites were delivered into "
  "their hand, because they cried to God in the battle, and he was intreated of them, because "
  "they put their trust in him. The register pauses to record that the outcome was credited to "
  "prayer rather than to the numbers it has just given."),
 ("The War Against the Hagarites", "Half-Manasseh, and the Captivity (vv.23-26)",
  "The eastern half of Manasseh is placed geographically, from Bashan unto Baal-hermon, and its "
  "men described as famous men, and heads of the house of their fathers. Then the section turns "
  "on them: they transgressed against the God of their fathers, and went after the gods of the "
  "people of the land. The consequence is stated with the same causal directness as the victory "
  "four verses earlier, and the God of Israel stirred up the spirit of Pul king of Assyria, and "
  "he carried them away. The three eastern tribes are the first to go, and the register says "
  "why."),
],
"1chronicles6": [
 ("", "The Line of the High Priests (vv.1-15)",
  "Levi's three sons are named and then one line is followed without deviation: Aaron, Eleazar, "
  "Phinehas, down through Zadok to Jehozadak. Twenty-three generations of high priests. The last "
  "verse dates the end of it, Jehozadak went into captivity when the LORD carried away Judah and "
  "Jerusalem by the hand of Nebuchadnezzar. For a post-exilic community arguing about who may "
  "serve at the altar, this list is the credential."),
 ("The Line of the High Priests", "The Three Levitical Families (vv.16-30)",
  "The register restarts from Levi and works through all three families rather than the priestly "
  "line alone, Gershom, Kohath and Merari, each with its descendants. Samuel appears in the "
  "Kohathite list, which is the Chronicler placing the prophet inside Levi rather than in "
  "Ephraim where 1 Samuel locates his home. The genealogy is making a claim about him that the "
  "earlier book does not."),
 ("The Three Levitical Families", "The Singers Appointed by David (vv.31-48)",
  "These are they whom David set over the service of song in the house of the LORD, after that "
  "the ark had rest. Three chief singers are traced back to the three Levite families, Heman "
  "from Kohath, Asaph from Gershom, Ethan from Merari, so the music is distributed across the "
  "whole tribe by design. The names Asaph, Heman and Jeduthun appear in the headings of psalms. "
  "Then the rest of the Levites are assigned to all manner of service of the tabernacle."),
 ("The Singers Appointed by David", "Aaron's Line Repeated (vv.49-53)",
  "A short return to the priests, and the duties are specified rather than the descent: they "
  "offered upon the altar of the burnt offering, and on the altar of incense, and were appointed "
  "for all the work of the place most holy. The line from Aaron to Ahimaaz is then given again "
  "in five verses, more briefly than at the start of the chapter. The repetition marks the "
  "division between who sang and who sacrificed."),
 ("Aaron's Line Repeated", "The Levitical Cities (vv.54-81)",
  "Twenty-eight verses of place names, and the arrangement is the point: Levi has no territory "
  "of its own, so its holdings are forty-eight towns scattered through every other tribe, "
  "assigned by lot with their suburbs for cattle. Hebron and the cities of refuge are in the "
  "list. A tribe with a duty to teach the law is deliberately settled where everybody can reach "
  "it, and the chapter that began with the high priesthood ends with a map of pasture rights."),
],
"1chronicles7": [
 ("", "Issachar and Benjamin (vv.1-12)",
  "Two tribes handled briskly, and both entries are military. Issachar's men are counted as "
  "valiant men of might, reckoned in all by their genealogies fourscore and seven thousand. "
  "Benjamin's are given the same treatment with archers specified. The Chronicler is compiling a "
  "muster roll as much as a family tree, which is why the numbers appear where a genealogy would "
  "not usually carry them."),
 ("Issachar and Benjamin", "Naphtali and Manasseh (vv.13-19)",
  "Naphtali gets one verse, which is the shortest entry for any tribe in the book. Manasseh's is "
  "longer and less tidy, with a concubine named, an Aramean wife, and a daughter Hammoleketh "
  "recorded in her own right. The register keeps the irregularities rather than smoothing them, "
  "because its purpose is to establish descent and an awkward line is still a line."),
 ("Naphtali and Manasseh", "Ephraim, and the Sons Slain at Gath (vv.20-29)",
  "The register stops in the middle of Ephraim's list to tell a story it tells nowhere else. His "
  "sons were slain by the men of Gath, because they came down to take away their cattle, and "
  "Ephraim their father mourned many days, and his brethren came to comfort him. Then he had a "
  "son and called him Beriah, because it went evil with his house. A raid that went wrong, a "
  "funeral, and a child named after the grief. The section then continues into Joshua's line and "
  "the towns Ephraim held, Bethel, Gezer, Shechem."),
 ("Ephraim, and the Sons Slain at Gath", "The Sons of Asher (vv.30-40)",
  "Asher closes the chapter and the entry is conventional: sons, grandsons, and a count of "
  "twenty-six thousand men apt to the war. The description used of them is choice and mighty men "
  "of valour, chief of the princes. Nothing else about the tribe is recorded anywhere in "
  "Chronicles, so these eleven verses are the whole of what the book has to say about it."),
],
"1chronicles8": [
 ("", "The Sons of Benjamin (vv.1-28)",
  "Benjamin gets a second and much longer treatment than in chapter 7, and the reason arrives in "
  "the last section: this chapter exists to reach Saul. Twenty-eight verses of families, with "
  "settlements at Geba, Moab, Ono, Lod and Aijalon, and a note that some drove away the "
  "inhabitants of Gath. The Chronicler is unusually interested in where these families moved "
  "and remarried, which for a tribe nearly destroyed in Judges 20 is a record of survival."),
 ("The Sons of Benjamin", "The House of Saul (vv.29-40)",
  "The list narrows to Gibeon and then to one household: Kish, and Saul, and Saul's four sons, "
  "Jonathan, Malchi-shua, Abinadab and Esh-baal. Jonathan's line is then followed for ten more "
  "generations through Merib-baal, the Mephibosheth of 2 Samuel. Saul is given no reign, no "
  "failure and no death here, only a family. The Chronicler will kill him in chapter 10 and this "
  "is the only place he tells us who he was."),
],
"1chronicles9": [
 ("", "Those Who Returned to Jerusalem (vv.1-9)",
  "The register states its own method and then changes subject: so all Israel were reckoned by "
  "genealogies, and behold, they were written in the book of the kings of Israel and Judah, who "
  "were carried away to Babylon for their transgression. That clause is the pivot of the whole "
  "nine chapters. Everything before it was the old order. What follows is who came back, listed "
  "by tribe, Judah, Benjamin, Ephraim and Manasseh, with numbers of the heads of houses. The "
  "return is documented in the same form as the descent."),
 ("Those Who Returned to Jerusalem", "The Priests and the Levites (vv.10-16)",
  "The priests are listed with a summary of their standing, very able men for the work of the "
  "service of the house of God, and a count of one thousand seven hundred and threescore. Then "
  "the Levites, and among them names that appear in Nehemiah's lists of the same period. The "
  "villages of the Netophathites are mentioned, which places some of them outside the city. A "
  "community rebuilding a temple needed to know exactly this."),
 ("The Priests and the Levites", "The Porters and Their Charge (vv.17-34)",
  "Eighteen verses on gatekeeping, which is more than most tribes received. The four quarters "
  "are assigned, east, west, north and south, and the duty is traced back, these had the "
  "oversight of the gates of the tabernacle, and their fathers over the host of the LORD. "
  "Shifts are described, they came every seventh day, and so are the specific "
  "responsibilities: the chambers, the treasuries, the vessels counted in and out, the fine "
  "flour, the wine, the oil, the frankincense, the spices, and the shewbread prepared every "
  "sabbath. Some lodged round about the house because the charge was on them, and they were "
  "over that business by night."),
 ("The Porters and Their Charge", "The House of Saul Repeated (vv.35-44)",
  "The genealogy of Gibeon and Saul's household is given again, almost word for word from "
  "chapter 8. The repetition is not an error. Nine chapters of names end where the narrative is "
  "about to begin, and the last family listed is the one whose fall in the next chapter makes "
  "room for David. The register closes and chapter 10 opens with the Philistines fighting "
  "against Israel."),
],
}


def find(items, prefix):
    for i, (label, _) in enumerate(items):
        if H.unescape(label).strip().startswith(prefix):
            return i
    return -1


def first_section(items):
    for i, (label, _) in enumerate(items):
        if re.search(r"\(vv?\.[^)]*\)\s*:?\s*$", H.unescape(label).strip()):
            return i
    return len(items)


def main():
    check = "--check" in sys.argv
    planned, problems, notes = {}, [], []
    for page, ops in OPS.items():
        path = os.path.join(DOCS, page + ".html")
        html = open(path, encoding="utf-8").read()
        pane = PANE.search(html)
        if not pane:
            problems.append(f"{page}: no authorship pane")
            continue
        items = [[a, b.strip()] for a, b in ITEM_RE.findall(pane.group(2))]
        for after, label, prose in ops:
            at = first_section(items) if after == "" else find(items, after) + 1
            if after and at == 0:
                problems.append(f"{page}: insert anchor {after!r} not found")
                continue
            items.insert(at, [label + ":", prose])
            notes.append(f"{page}: inserted {label!r}")
        parts = ["\n                <h3>Authorship &amp; Background</h3>\n"]
        for label, body in items:
            parts.append(ITEM.format(label=label, body=body) + "\n")
        new_body = "".join(parts) + "            </div>\n\n            "
        # Compare div counts across the pane only, not the whole file. Another
        # session may be editing other tabs in the same working tree, and its
        # state must not decide whether this splice is sound.
        old_pane, new_pane = pane.group(2), new_body
        d_open = (len(re.findall(r"<div\b", new_pane))
                  - len(re.findall(r"<div\b", old_pane)))
        d_close = (len(re.findall(r"</div>", new_pane))
                   - len(re.findall(r"</div>", old_pane)))
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
    print(f"{'would touch' if check else 'touched'} {len(planned)} pages, "
          f"{len(notes)} change(s)")
    return 0


def verify(planned):
    """Run the audit's own checks against the planned HTML, without writing it.

    The pages cannot be written yet, so the usual sequence of write-then-audit is
    not available. This applies the same rules to the strings in memory, which is
    what makes a --check run meaningful while the tree belongs to someone else.
    """
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import audit_authorship as A
    found = []
    for path, html in planned.items():
        page = os.path.basename(path)[:-5]
        nums = {int(x) for x in re.findall(r'class="verse-num"[^>]*>(\d+)', html)}
        total = max(nums) if nums else 0
        labels = [H.unescape(x).strip() for x in A.LABEL.findall(
            A.PANE.search(html).group(2))]
        secs = [(l, A.TAIL.search(l)) for l in labels]
        secs = [(l, m.group(1)) for l, m in secs if m]
        covered, repeated, starts = set(), set(), []
        for label, spec in secs:
            got = A.halves(spec)
            repeated |= got & covered
            covered |= got
            starts.append(min(v for v, _ in got) if got else 0)
            top = max(v for v, _ in got) if got else 0
            if total and top > total:
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
        for label in labels:
            fault = A.label_fault(label)
            if fault:
                found.append(f"{page}: label {fault}: {label!r}")
            stray = sorted({w for w in A.CAPS.findall(label)
                            if w not in A.CAPS_OK})
            if stray and A.TAIL.search(label):
                found.append(f"{page}: capitals {stray} in {label!r}")
    return found


if __name__ == "__main__":
    sys.exit(main())
