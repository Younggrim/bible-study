#!/usr/bin/env python3
"""
Finishes 1 Kings, Deuteronomy and Numbers. Sixteen pages.

Three of these omissions are among the worst found so far, and all three are cases
where the surrounding material was described and the centre was not:

  1kings22 had the alliance and the question of prophecy, then Ahab's death. Missing
  in between were vv.10-28, which is Micaiah: the four hundred prophets agreeing,
  the vision of the LORD on his throne asking who will persuade Ahab, the lying
  spirit volunteering, and Micaiah struck in the face and jailed for saying so.
  Nineteen verses, and the whole reason the chapter is famous.
  numbers4 had one section, the census results at vv.34-49. Missing were vv.1-33,
  the instructions for dismantling and carrying the tabernacle, including the order
  that the holy things be covered before the Kohathites approach so that they do not
  look and die.
  deuteronomy12 had the command to destroy pagan sites and the permission for local
  slaughter, and not vv.8-14, which is the central-sanctuary law itself, nor
  vv.17-28, the tithe and the repeated ban on eating blood.

The rest: 1kings7 vv.40-47 the bronze inventory and Hiram's totals, 1kings21
vv.25-29 where Ahab repents and the sentence is deferred to his son, deuteronomy4
vv.25-31 the exile foretold with a way back attached, deuteronomy19 vv.1-10 the
cities of refuge and the roads to them, deuteronomy29 vv.1-9 the appeal to what
they saw in Egypt, deuteronomy32 vv.1-3 the invocation of the Song and vv.28-33 the
vine of Sodom, numbers3 vv.1-4 the death of Nadab and Abihu recalled and vv.11-13
the firstborn claim and vv.39-51 the redemption count, numbers6 vv.1-8 the Nazarite
vow itself, numbers9 vv.9-14 the second Passover provision, numbers12 vv.1-2 the
complaint that starts it and vv.11-13 Moses' five-word prayer, numbers16 vv.36-40
the censers beaten into altar plates, numbers24 vv.10-13 Balak's fury and Balaam's
answer, numbers35 vv.25-28 the death of the high priest as the term of exile.

Usage:
    python3 finish_three_law_books.py [--check]
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
RANGE_IN_LABEL = re.compile(r"\(vv?\.[^)]*\)(?=\s*:?\s*$)")

OPS = {
"1kings7": [
 ("insert", "The Ten Stands and Lavers",
  "The Bronze Inventory (vv.40-47)",
  "The list closes with a summary of everything Hiram made in brass, the pillars, the bowls, "
  "the network, the pomegranates, the bases, the lavers, the sea and the twelve oxen under "
  "it, the pots and shovels and basins. Two details are worth keeping. The casting was done "
  "in the clay ground between Succoth and Zarthan, on the Jordan, because that is where the "
  "clay for the moulds was, so the temple furniture was made forty miles from the temple. "
  "And the weight was not recorded: the brass of all these vessels was without weight, which "
  "is the writer's way of describing a quantity nobody bothered to total."),
],
"1kings21": [
 ("insert", "Elijah's Confrontation",
  "Ahab Humbles Himself (vv.25-29)",
  "The narrator stops to deliver a verdict, and it is the harshest in Kings: there was none "
  "like unto Ahab, which did sell himself to work wickedness in the sight of the LORD, whom "
  "Jezebel his wife stirred up. Then, immediately after that sentence, Ahab tears his "
  "clothes, puts sackcloth on his flesh, fasts, lies in sackcloth and goes softly. And God "
  "notices. Seest thou how Ahab humbleth himself before me? I will not bring the evil in his "
  "days, but in his son's days will I bring it. The chapter that condemns him most completely "
  "also records a real reprieve, granted to a repentance nobody would call thorough."),
],
"1kings22": [
 ("insert", "The Alliance and the Question of Prophecy",
  "Micaiah and the Lying Spirit (vv.10-28)",
  "The two kings sit in their robes at the gate of Samaria while four hundred prophets "
  "prophesy before them, and Zedekiah makes iron horns and acts out the victory. Micaiah is "
  "sent for, with a coaching note from the messenger, let thy word be like the word of one of "
  "them. His first answer mocks them by repeating it, go, and prosper, and the king who did "
  "not want the truth demands it, how many times shall I adjure thee that thou tell me "
  "nothing but that which is true? So he gives it twice. First a picture, I saw all Israel "
  "scattered upon the hills, as sheep that have not a shepherd. Then the throne room: the "
  "LORD sitting, the host of heaven standing by, and the question who shall persuade Ahab, "
  "and a spirit coming forth and saying, I will be a lying spirit in the mouth of all his "
  "prophets. Zedekiah strikes him in the face, and Micaiah is sent to prison on bread and "
  "water with one sentence to leave behind, if thou return at all in peace, the LORD hath not "
  "spoken by me."),
],
"deuteronomy4": [
 ("insert", "Remember Horeb — No Idols",
  "Exile Foretold, and the Way Back (vv.25-31)",
  "Moses looks past the conquest to a generation not yet born, when thou shalt beget children, "
  "and children's children, and shall have remained long in the land, and describes idolatry, "
  "then scattering. Ye shall be left few in number among the heathen. The description of exile "
  "is unsparing and includes serving gods of wood and stone. But the passage does not end "
  "there. If from thence thou shalt seek the LORD thy God, thou shalt find him, if thou seek "
  "him with all thy heart and with all thy soul. The ground of the return is not their "
  "improvement but his character, for the LORD thy God is a merciful God, he will not forsake "
  "thee, neither destroy thee, nor forget the covenant of thy fathers. Seven hundred years "
  "before the exile, the way out of it is already written down."),
],
"deuteronomy12": [
 ("insert", "The Place God Will Choose",
  "One Place of Worship, Not Every Man His Own (vv.8-14)",
  "Ye shall not do after all the things that we do here this day, every man whatsoever is "
  "right in his own eyes. That sentence is the hinge of the chapter and the phrase Judges will "
  "use as its epitaph. The wilderness arrangement was provisional because ye are not as yet "
  "come to the rest, and once the land is settled the rule changes: bring your offerings unto "
  "the place which the LORD your God shall choose. Not a ban on joy, the passage is emphatic "
  "that they shall rejoice before the LORD with their households and the Levite. A ban on "
  "improvisation, take heed to thyself that thou offer not thy burnt offerings in every place "
  "that thou seest."),
 ("insert", "Permission for Local Slaughter",
  "The Tithe, the Levite, and the Blood (vv.17-28)",
  "The concession of the previous verses is fenced. What may be eaten at home is ordinary "
  "meat, not the tithe, the firstlings or the vows, which are to be eaten before the LORD in "
  "the chosen place. Then a clause easy to read past, take heed that thou forsake not the "
  "Levite as long as thou livest, because the Levite has no land and lives on exactly this. "
  "The prohibition on blood is repeated three times in eleven verses, thou shalt not eat the "
  "blood, for the blood is the life, pour it upon the earth as water. Three repetitions "
  "suggest it was the instruction most often ignored."),
],
"deuteronomy19": [
 ("insert", "", "Cities of Refuge and the Roads to Them (vv.1-10)",
  "Three cities are to be set apart when the land is possessed, and the practical instruction "
  "attached is about infrastructure: thou shalt prepare thee a way, and divide the coasts of "
  "thy land into three parts. Roads and equal spacing, so that no killer is caught by "
  "distance. The case described is deliberately ordinary, two men in the wood and the head "
  "slippeth from the helve and killeth his neighbour, and the danger named is the avenger "
  "pursuing while his heart is hot and overtaking him because the way is long. The law is "
  "protecting a man who is not guilty from a man who is not wrong to be angry. Three more "
  "cities are promised if the borders widen, so that innocent blood be not shed in thy land."),
],
"deuteronomy29": [
 ("insert", "", "Ye Have Seen All That the LORD Did (vv.1-9)",
  "The covenant renewal in Moab opens with evidence rather than with terms. Ye have seen all "
  "that the LORD did before your eyes in the land of Egypt, the signs and the great miracles. "
  "Then the sentence that qualifies it, and it is the strangest in the chapter: yet the LORD "
  "hath not given you an heart to perceive, and eyes to see, and ears to hear, unto this day. "
  "They watched it all and did not understand it. The evidence offered next is domestic "
  "rather than spectacular, your clothes are not waxen old upon you, and thy shoe is not "
  "waxen old upon thy foot, forty years of provision measured in footwear."),
],
"deuteronomy32": [
 ("insert", "", "Give Ear, O Ye Heavens (vv.1-3)",
  "The Song opens by summoning witnesses that outlast the audience, give ear, O ye heavens, "
  "and I will speak, and hear, O earth, the words of my mouth. Then an image for how the "
  "teaching is meant to arrive, my doctrine shall drop as the rain, my speech shall distil as "
  "the dew, which is slow and quiet rather than forceful. And the reason for the whole "
  "performance, because I will publish the name of the LORD, ascribe ye greatness unto our "
  "God."),
 ("insert", "God's Judgment",
  "A Nation Void of Counsel (vv.28-33)",
  "The judgment section pauses to explain the failure, and the explanation is not wickedness "
  "but stupidity: they are a nation void of counsel, neither is there any understanding in "
  "them. O that they were wise, that they would consider their latter end. Then the "
  "arithmetic that gives the passage its force, how should one chase a thousand, and two put "
  "ten thousand to flight, except their Rock had sold them? Defeat on that scale is not "
  "military, it is evidence. The section closes with the vine imagery turned poisonous, their "
  "grapes are grapes of gall, their clusters bitter, their wine the poison of dragons."),
],
"numbers3": [
 ("insert", "", "The Sons of Aaron, and Two Who Died (vv.1-4)",
  "The chapter opens with Aaron's four sons named in order, and then two of them removed in "
  "the same breath: Nadab and Abihu died before the LORD, when they offered strange fire in "
  "the wilderness of Sinai, and they had no children. The census of a priestly family begins "
  "by recording a gap in it. Eleazar and Ithamar are what is left, and the entire later "
  "priesthood descends from those two."),
 ("insert", "The Levites Given to Aaron",
  "The Levites Instead of the Firstborn (vv.11-13)",
  "I have taken the Levites from among the children of Israel instead of all the firstborn. "
  "The substitution is grounded in the night of the exodus, on the day that I smote all the "
  "firstborn in the land of Egypt I hallowed unto me all the firstborn in Israel. God's claim "
  "on every eldest son is real and is being met by a tribe standing in their place, which is "
  "why the Levites are described as given rather than employed."),
 ("insert", "Moses and Aaron — East Side",
  "The Redemption Count (vv.39-51)",
  "The arithmetic is done in public and it does not come out even. Twenty-two thousand "
  "Levites against twenty-two thousand two hundred and seventy-three firstborn, leaving two "
  "hundred and seventy-three unaccounted for. Those are redeemed at five shekels a head, "
  "one thousand three hundred and sixty-five shekels paid to Aaron. A doctrine of "
  "substitution is settled here by counting heads and finding a shortfall, and the shortfall "
  "is paid rather than waived."),
],
"numbers4": [
 ("insert", "", "The Kohathites and the Covered Holy Things (vv.1-20)",
  "The Kohathites carry the ark, the table, the lampstand and the altars, and every one is to "
  "be wrapped before they arrive. Aaron and his sons take down the veil and cover the ark "
  "with it, then badgers' skins, then a cloth of blue, and only then are the staves put in. "
  "The reason is stated twice and it is not ceremonial fussiness: they shall not touch any "
  "holy thing, lest they die, and they shall not go in to see when the holy things are "
  "covered, lest they die. The most privileged carrying duty in Israel is arranged so that "
  "the men doing it never see what they carry. Eleazar is named as personally responsible for "
  "the oil, the incense and the meat offering."),
 ("insert", "The Kohathites and the Covered Holy Things",
  "The Gershonites and the Merarites (vv.21-33)",
  "The other two families get the fabric and the frame. Gershon carries the curtains, the "
  "coverings, the hangings of the court and the cords, under the hand of Ithamar. Merari "
  "carries the boards, the bars, the pillars and the sockets, and the instruction includes "
  "an inventory: ye shall reckon the instruments of all their service by name. Every tent peg "
  "is assigned to a named man. The service age is given for all three families as thirty to "
  "fifty, so the heaviest work in the tabernacle belongs to men in middle life rather than to "
  "the young."),
],
"numbers6": [
 ("insert", "", "The Nazarite Vow (vv.1-8)",
  "A vow available to either sex, when either man or woman shall separate themselves to vow a "
  "vow of a Nazarite, and it consists of three abstentions. No wine or strong drink, and the "
  "prohibition is extended to the whole plant, no vinegar, no liquor of grapes, no moist or "
  "dried grapes, nothing from the kernel to the husk. No razor upon the head, so the hair is "
  "left to grow as the visible sign. And no contact with a dead body, not even for his father "
  "or his mother, which is stricter than the ordinary priesthood and matches the high priest. "
  "The vow is temporary, which is what makes it remarkable: for a set period an ordinary "
  "Israelite takes on a holiness the law otherwise reserves for one man."),
],
"numbers9": [
 ("insert", "The Problem of Uncleanness",
  "The Second Passover Provided (vv.9-14)",
  "The answer to the men who were unclean at Passover is a new provision rather than an "
  "exemption. If any man be unclean by reason of a dead body, or be in a journey afar off, he "
  "shall keep it in the fourteenth day of the second month, a full month late, with the same "
  "rules, unleavened bread and bitter herbs, no bone broken. The concession is fenced at both "
  "ends. A man who is clean and not travelling and does not keep it shall bear his sin and be "
  "cut off, so the second date is for the genuinely prevented and not for the merely "
  "unwilling. And the stranger is admitted on identical terms, one ordinance, both for the "
  "stranger and for him that was born in the land."),
],
"numbers12": [
 ("insert", "", "Miriam and Aaron Speak Against Moses (vv.1-2)",
  "Miriam and Aaron spake against Moses because of the Ethiopian woman whom he had married. "
  "The stated grievance is his wife, and it is dropped after half a verse, because the real "
  "one follows: hath the LORD indeed spoken only by Moses? hath he not spoken also by us? "
  "This is a complaint about authority wearing the clothes of a complaint about marriage. "
  "Miriam is named first, which in Hebrew narrative usually marks who started it, and the "
  "verb is feminine singular."),
 ("insert", "God's Judgment — Miriam's Leprosy",
  "Aaron's Plea and Moses' Prayer (vv.11-13)",
  "Aaron turns to the brother he has just undermined and calls him my lord, alas, my lord, I "
  "beseech thee, lay not the sin upon us. His description of Miriam is unflinching, let her "
  "not be as one dead, of whom the flesh is half consumed. Then Moses prays, and the prayer "
  "is five words in Hebrew and eight in English: heal her now, O God, I beseech thee. The man "
  "described in verse 3 as the meekest on earth makes no comment on the accusation and asks "
  "for nothing except her recovery."),
],
"numbers16": [
 ("insert", "The Test and the Judgment",
  "The Censers Beaten into Plates (vv.36-40)",
  "Two hundred and fifty men are dead and their censers are still on the ground, and the "
  "instruction is to salvage them. Eleazar is to gather them, because they are hallowed, and "
  "have them beaten into broad plates for a covering of the altar. The reasoning is exact: "
  "they offered them before the LORD, therefore they are hallowed, so the objects are holy "
  "even though the men who held them were destroyed. The purpose of the plates is memory, a "
  "sign unto the children of Israel that no stranger come near to offer incense. The altar is "
  "resurfaced with the evidence of what happened to the last men who tried."),
],
"numbers24": [
 ("insert", "Third Oracle",
  "Balak's Fury and Balaam's Answer (vv.10-13)",
  "Balak's anger was kindled, and he smote his hands together. Three times now he has paid "
  "for a curse and been given a blessing. Therefore now flee thou to thy place, I thought to "
  "promote thee unto great honour, but, lo, the LORD hath kept thee back from honour. Balaam's "
  "reply is the one thing he has been consistent about from the beginning: if Balak would give "
  "me his house full of silver and gold, I cannot go beyond the commandment of the LORD, to do "
  "either good or bad. He says it as though it settles the matter, and chapter 31 records what "
  "he did next."),
],
"numbers35": [
 ("insert", "Manslaughter Defined",
  "The Death of the High Priest (vv.25-28)",
  "The term of the killer's confinement is not a number of years. He shall abide in the city "
  "of refuge until the death of the high priest, an event nobody can predict or arrange. If he "
  "leaves before it, the avenger may kill him without guilt. After it, he shall return unto "
  "the land of his possession. The release of an accidental killer is tied to the death of the "
  "man who represents the nation before God, and it is the one detail in the chapter that "
  "later readers have found impossible to leave alone."),
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
        for op in ops:
            kind = op[0]
            if kind == "extend":
                _, prefix, rng, prose = op
                i = find(items, prefix)
                if i < 0:
                    problems.append(f"{page}: extend target {prefix!r} not found")
                    continue
                new_label, n = RANGE_IN_LABEL.subn(rng, items[i][0])
                if not n:
                    problems.append(f"{page}: no range in label {prefix!r}")
                    continue
                items[i][0] = new_label
                items[i][1] += " " + prose
                notes.append(f"{page}: extended {prefix!r} to {rng}")
            elif kind == "insert":
                _, after, label, prose = op
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
        new = html[:pane.start(2)] + new_body + html[pane.end(2):]
        o, c = len(re.findall(r"<div\b", new)), len(re.findall(r"</div>", new))
        if o != c:
            problems.append(f"{page}: div imbalance {o} vs {c}")
            continue
        planned[path] = new
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


if __name__ == "__main__":
    sys.exit(main())
