#!/usr/bin/env python3
"""
Completes Amos: all nine chapters.

The skeletons here are clean -- compact verse ranges, no mis-split labels, and the
only headless item on each page is the "Structure:" heading itself, so there are no
continuation paragraphs to merge.

What does need work is the Historical Context bodies, which shout. Sixteen words
across the nine chapters are set in capitals for emphasis: ISRAEL, SOCIAL, CAUSE,
EFFECT, WITNESS, SARCASM, HEART, FUNERAL, JUSTICE, WHILE, VISIONS, HEARING, FINALE,
STANDING, JUDGMENT, RAISE.

Rather than rewrite the paragraphs by hand as Lamentations needed, this applies a
map of exactly those words to their correct casing. The paragraphs are otherwise
preserved byte for byte, which is less risky than a rewrite and keeps the existing
content intact. A map is used rather than a lowercase rule for the reason that keeps
coming up: "II" also appears in capitals, in "Jeroboam II", and a rule would ruin
it. That is the third such case after PE and AYIN in Lamentations and I AM in Mark.

One typo fixed while in there: amos2 had "pledge- taking" with a stray space.

Usage:
    python3 fold_amos.py [--check]
"""
import os
import re
import sys

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")

ITEM = ('                    <div class="auth-item">'
        '<span class="auth-label">{label}</span> {body}</div>')

VERSES = {"amos1": 15, "amos2": 16, "amos3": 15, "amos4": 13, "amos5": 27,
          "amos6": 14, "amos7": 17, "amos8": 14, "amos9": 15}

CAPS_OK = {"LORD", "GOD", "YHWH", "OT", "NT", "BC", "AD", "KJV", "ESV", "ASV",
           "AM", "II"}

KEEP = ["Author:", "Classification:", "Key Themes:", "Historical Context:"]

# Emphatic capitals to normalise, with the casing each should have. Israel is a
# proper noun; the rest are ordinary words. II is deliberately absent -- it is
# Jeroboam II and must stay.
NORMALISE = {
    "ISRAEL": "Israel", "SOCIAL": "social", "CAUSE": "cause", "EFFECT": "effect",
    "WITNESS": "witness", "SARCASM": "sarcasm", "HEART": "heart",
    "FUNERAL": "funeral", "JUSTICE": "justice", "WHILE": "while",
    "VISIONS": "visions", "HEARING": "hearing", "FINALE": "finale",
    "STANDING": "standing", "JUDGMENT": "judgment", "RAISE": "raise",
}

TYPOS = {"pledge- taking": "pledge-taking"}

SECTIONS = {
"amos1": [
  ("Amos of Tekoa, Two Years Before the Earthquake (v.1)",
   "Amos is introduced by trade rather than office: a herdman of Tekoa, a village in "
   "the Judean hills south of Bethlehem. He is a southerner sent north, and a layman "
   "sent to a state sanctuary, both of which become the issue in chapter 7. The dating "
   "is unusually concrete, two years before the earthquake, an event still remembered "
   "when Zechariah 14:5 refers to it centuries later. Jeroboam II's reign was the "
   "northern kingdom's most prosperous, which is the background to everything that "
   "follows."),
  ("The LORD Roars from Zion (v.2)",
   "The book's thesis in one line: the LORD will roar from Zion and utter his voice "
   "from Jerusalem, and the pastures wither. A shepherd's image and a shepherd's "
   "reference point -- the roar is a lion's, and Amos returns to it at 3:8. That the "
   "voice comes from Zion, in the south, is pointed when the message is for Samaria."),
  ("Damascus and Gaza (vv.3-8)",
   "The oracles begin with a formula repeated eight times: for three transgressions "
   "and for four. It signals a full count rather than a precise one. Damascus is "
   "charged with threshing Gilead with instruments of iron, Gaza with carrying away a "
   "whole captivity to deliver them to Edom -- slave trading. The charges are war "
   "crimes rather than idolatry, so the standard applied to these nations is one they "
   "could recognise."),
  ("Tyre and Edom (vv.9-12)",
   "Tyre is charged with the same slave trade as Gaza and with forgetting the "
   "brotherly covenant, a reference to the old alliance with Israel. Edom's charge is "
   "pursuing his brother with the sword and casting off all pity, the family language "
   "that Obadiah builds a whole book on. Each oracle ends with fire sent on a named "
   "city, so the judgments are specific rather than general."),
  ("Ammon (vv.13-15)",
   "The last oracle of the chapter is the most brutal charge yet: ripping up the women "
   "with child of Gilead in order to enlarge their border. Atrocity for the sake of "
   "territory. An Israelite audience would have approved of every judgment so far, "
   "since all five fell on enemies, which is precisely the response the next chapter "
   "turns against them."),
],
"amos2": [
  ("Moab (vv.1-3)",
   "The sixth foreign oracle, and the charge is unexpected: burning the bones of the "
   "king of Edom into lime. Desecrating a corpse, and the corpse of a third party at "
   "that -- Edom is not Israel's friend. God is presented as holding nations to "
   "account for cruelty that had nothing to do with his own people, which widens the "
   "argument considerably."),
  ("Judah (vv.4-5)",
   "The seventh oracle crosses into the south, and the charge changes character. Where "
   "the nations were indicted for atrocities, Judah is indicted for despising the law "
   "of the LORD and not keeping his commandments. More is expected where more was "
   "given. The northern audience could still applaud this one, since Judah was a "
   "rival."),
  ("The Trap Closes: Israel (vv.6-8)",
   "The eighth oracle is the one the whole sequence was built for, and now the "
   "geography has walked all the way round to the listeners' own doorstep. The charges "
   "are economic and social: selling the righteous for silver and the poor for a pair "
   "of shoes, panting after the dust of the poor, a father and son going in to the "
   "same girl, lying on garments taken in pledge beside the altar. The last detail "
   "matters -- the exploitation is happening in the sanctuary, using pledged clothing "
   "the law required be returned by nightfall."),
  ("I Brought You Up Out of Egypt (vv.9-12)",
   "The indictment turns to history, and every item is something God did for them: "
   "destroying the Amorite, bringing them up from Egypt, leading them forty years, "
   "raising up prophets and Nazirites. Then what they did with it -- they gave the "
   "Nazirites wine to drink and told the prophets not to prophesy. The two gifts named "
   "are the two they neutralised."),
  ("No One Escapes (vv.13-16)",
   "The chapter closes with a list of people who would normally survive a rout and "
   "will not: the swift, the strong, the mighty, the archer, the horseman, the "
   "courageous. Each is named with the thing that usually saves them and told it will "
   "fail. The image in v.13, pressed like a cart full of sheaves, is agricultural "
   "rather than military, which is where Amos keeps returning."),
],
"amos3": [
  ("You Only Have I Known (vv.1-2)",
   "The theological foundation for everything else in the book, and it runs opposite "
   "to how election was being heard. You only have I known of all the families of the "
   "earth, therefore I will punish you for all your iniquities. Being chosen increases "
   "accountability rather than providing exemption. The audience had drawn the "
   "opposite conclusion from the same fact."),
  ("Seven Questions: Can Two Walk Together? (vv.3-6)",
   "A rapid series of rhetorical questions, each with an obvious answer, establishing "
   "that effects have causes: two do not walk together unless agreed, a lion does not "
   "roar without prey, a bird does not fall into a snare without a trap, a trumpet "
   "does not sound in a city without alarm. The point being built is that the "
   "prophecy is not arbitrary. There is a cause, which is Israel's sin, and an "
   "inevitable effect, which is judgment."),
  ("The Lion Roars; the Prophet Speaks (vv.7-8)",
   "Two verses give Amos his own justification. God does nothing without revealing his "
   "secret to his servants the prophets, so the prophet's word is the warning built "
   "into the system. Then the compulsion: the lion hath roared, who will not fear? the "
   "Lord GOD hath spoken, who can but prophesy? He is not describing a career choice."),
  ("Pagan Witnesses Summoned (vv.9-10)",
   "The palaces of Ashdod and Egypt are called to assemble and look at what is "
   "happening in Samaria. Inviting Philistines and Egyptians as witnesses to Israel's "
   "conduct is a calculated insult -- these are the nations Israel considered "
   "unrighteous. The charge in v.10 is that they know not to do right, and store up "
   "violence and robbery in their palaces."),
  ("Two Legs and a Piece of an Ear (vv.11-15)",
   "The sentence is delivered in the shepherd's own idiom: as a shepherd recovers two "
   "legs or a piece of an ear from a lion's mouth, so shall Israel be rescued. What is "
   "salvaged proves the animal is dead. The chapter ends on the property that funded "
   "all of it -- the altars of Bethel with their horns cut off, the winter house and "
   "the summer house, and the houses of ivory perishing."),
],
"amos4": [
  ("The Cows of Bashan (vv.1-3)",
   "One of the most confrontational addresses in Scripture, and it is aimed at the "
   "wealthy women of Samaria: kine of Bashan, well-fed cattle from the best pasture "
   "in the region. The charge is not luxury as such but its source -- they oppress the "
   "poor and crush the needy and then say to their masters, bring and let us drink. "
   "The sentence is being led out through breaches in the wall with hooks."),
  ("Come to Bethel and Transgress (vv.4-5)",
   "God invites them to worship, and the invitation is sarcastic. Come to Bethel and "
   "transgress, bring your sacrifices every morning, offer your tithes, publish your "
   "freewill offerings -- for this liketh you. Their religious enthusiasm is real and "
   "beside the point. The last clause names the actual motive: they enjoy it, which is "
   "why the volume of it proves nothing."),
  ("Yet Have Ye Not Returned unto Me (vv.6-11)",
   "Five escalating disciplines, each closing with the same refrain: famine, drought, "
   "blight and locusts, pestilence and sword, and an overthrow like Sodom. After every "
   "one, yet have ye not returned unto me. The refrain is the point of the passage. "
   "The disciplines were not the punishment but the summons, and each was ignored in "
   "turn."),
  ("Prepare to Meet Thy God (vv.12-13)",
   "Therefore, since none of that worked: prepare to meet thy God, O Israel. The line "
   "is often read as an invitation and in context it is not one. What follows is a "
   "doxology naming the God in question -- he that formeth the mountains and createth "
   "the wind, the LORD of hosts is his name -- which is there to make the encounter "
   "sound as serious as it is."),
],
"amos5": [
  ("A Lamentation: The Virgin of Israel Is Fallen (vv.1-3)",
   "Amos sings a funeral song over a nation still standing. The virgin of Israel is "
   "fallen, she shall no more rise, there is none to raise her up. Using the form of a "
   "dirge for the living is the harshest rhetorical choice available, and it treats the "
   "outcome as settled. Verse 3's arithmetic is bleak: the city that sends out a "
   "thousand will have a hundred left."),
  ("Seek Me and Live (vv.4-6)",
   "Immediately after the funeral song comes an invitation, which is the tension the "
   "chapter runs on. Seek ye me, and ye shall live. What they are told not to seek is "
   "named: Bethel, Gilgal, Beersheba -- the sanctuaries. Seeking God and seeking the "
   "shrines are set in opposition, which for a religious nation is the whole "
   "difficulty."),
  ("Wormwood for Judgment (vv.7-13)",
   "The charge is turning judgment to wormwood and leaving off righteousness. The "
   "specifics are judicial: they hate the one who rebukes in the gate, they take bribes "
   "and turn aside the poor. Verse 11's sentence is futility -- they will build houses "
   "and not live in them, plant vineyards and not drink the wine. Verse 8 interrupts "
   "with a doxology on the maker of Orion and the Pleiades, which is characteristic of "
   "Amos: creation praise dropped into the middle of an indictment."),
  ("Hate the Evil, Love the Good (vv.14-15)",
   "Two verses of instruction, and the order is deliberate: hate the evil, love the "
   "good, establish judgment in the gate. The gate was the courthouse, so the reform "
   "asked for is judicial rather than devotional. The hope offered is qualified in the "
   "same way Zephaniah qualifies his -- it may be that the LORD will be gracious."),
  ("Wailing in the Streets (vv.16-17)",
   "The funeral imagery returns and spreads outward: wailing in all the streets, in "
   "all the highways, in the vineyards. Professional mourners are called for, and "
   "husbandmen are called to wail, which means the harvest is being mourned along with "
   "the people. The reason given is simply that God will pass through the midst of "
   "them."),
  ("The Day of the LORD: Darkness, Not Light (vv.18-23)",
   "The audience apparently looked forward to the day of the LORD, expecting it to go "
   "well for them. Woe unto you that desire it, Amos answers -- it is darkness and not "
   "light, and the image is a man escaping a lion into a bear, and then leaning on a "
   "wall and being bitten by a serpent. Then the worship rejection: I hate, I despise "
   "your feast days, take thou away from me the noise of thy songs. The problem is not "
   "the quality of the music."),
  ("Let Judgment Run Down as Waters (vv.24-27)",
   "The book's most quoted verse follows directly from that rejection: let judgment run "
   "down as waters, and righteousness as a mighty stream. What replaces the sacrifices "
   "is not better sacrifices but justice, and the image is a river rather than a "
   "cistern -- continuous rather than stored. The chapter ends with exile named as "
   "beyond Damascus, which for a northern audience meant Assyria."),
],
"amos6": [
  ("Woe to Them That Are at Ease in Zion (vv.1-3)",
   "The woe is pronounced on both capitals, Zion and Samaria, so Judah is not "
   "exempted. The charge is being at ease and trusting in reputation -- chief of the "
   "nations, as they thought of themselves. Verse 2 tells them to look at Calneh, "
   "Hamath and Gath, cities that had already fallen, and asks whether they were better "
   "than these. Complacency is treated as a failure to read the news."),
  ("Ivory Beds and Bowls of Wine (vv.4-6)",
   "The description is precise and unhurried, which is part of its effect: beds of "
   "ivory, lambs out of the flock, invented music, wine drunk in bowls rather than "
   "cups, the chief ointments. None of it is illegal. The indictment lands in the last "
   "clause of v.6 -- they are not grieved for the affliction of Joseph. Indifference "
   "while comfortable is the sin actually named."),
  ("First to Go Captive (v.7)",
   "One verse, and it inverts their position exactly. Those who are first in luxury go "
   "first into captivity, and the banquet ends. The Hebrew ties the word for their "
   "revelry to the word for the exile's procession, so the party becomes the march."),
  ("The LORD Abhorreth the Excellency of Jacob (vv.8-11)",
   "God swears by himself, which in the prophets marks the most solemn form of oath, "
   "and what he abhors is the excellency of Jacob -- their pride in themselves. The "
   "aftermath in vv.9-10 is domestic and grim: bodies carried out of houses, and "
   "someone telling a survivor to hold his tongue rather than name the LORD. Fear has "
   "replaced worship."),
  ("Horses on Rock, and a Nation Raised Up (vv.12-14)",
   "Two questions about impossibility -- do horses run on rock, does one plough there "
   "with oxen -- answer the absurdity of turning judgment into gall. Then their own "
   "boast is quoted, that they took Karnaim by their own strength, and answered: God "
   "will raise up a nation against them from the entering in of Hamath to the river of "
   "the wilderness, which is the full length of their territory."),
],
"amos7": [
  ("First Vision: Locusts, and God Repents (vv.1-3)",
   "The book turns from oracles to visions, and the first two follow an identical "
   "pattern. Locusts are formed to devour the late growth, Amos intercedes -- cease, I "
   "beseech thee, by whom shall Jacob arise, for he is small -- and the LORD repents of "
   "it. The intercession works, and the ground of it is Jacob's weakness rather than "
   "any merit."),
  ("Second Vision: Fire, and God Repents (vv.4-6)",
   "A fire that devours the great deep and begins to eat up a part. The same plea in "
   "the same words, and the same answer: this also shall not be. Two successful "
   "intercessions establish that the prophet's prayer is genuinely effective, which is "
   "what makes the third vision land as hard as it does."),
  ("Third Vision: The Plumbline (vv.7-9)",
   "The third vision has no intercession recorded, because the measurement is already "
   "taken. A plumbline is a builder's tool for testing whether a wall is true, and the "
   "verdict is I will not again pass by them. Amos does not plead this time, and the "
   "text does not say why. The high places of Isaac and the sanctuaries of Israel are "
   "named, and the house of Jeroboam is threatened with the sword."),
  ("Amaziah: Go, Flee Thou to Judah (vv.10-13)",
   "The only narrative in the book, and it interrupts the visions. Amaziah, priest of "
   "Bethel, reports Amos to the king and then tells him to leave: flee thou away into "
   "the land of Judah, prophesy not again at Bethel, for it is the king's chapel. The "
   "phrase gives the whole problem away -- a sanctuary described as belonging to the "
   "king rather than to God, and a prophet judged on jurisdiction rather than truth."),
  ("I Was No Prophet: The LORD Took Me (vv.14-17)",
   "Amos's answer refuses the professional category entirely: I was no prophet, neither "
   "was I a prophet's son, but a herdman and a gatherer of sycomore fruit, and the LORD "
   "took me as I followed the flock. His authority is a calling rather than a "
   "credential, which is exactly what Amaziah cannot argue with. The reply then turns "
   "on Amaziah personally, and it is the most specific judgment in the book."),
],
"amos8": [
  ("Fourth Vision: A Basket of Summer Fruit (vv.1-3)",
   "The vision is a wordplay that only works in Hebrew: a basket of summer fruit is "
   "qayits, and the end is qets. Ripe fruit means the season is over. The verdict is "
   "the end is come upon my people Israel, I will not again pass by them, repeating the "
   "plumbline's phrase. Verse 3 turns the temple songs into howling."),
  ("When Will the Sabbath Be Gone? (vv.4-6)",
   "The merchants are quoted asking when the new moon and sabbath will be over so they "
   "can resume trading. They keep the holy days and resent them. The methods are "
   "itemised: making the ephah small and the shekel great, falsifying the balances, "
   "selling the refuse of the wheat, and buying the poor for a pair of shoes -- the same "
   "phrase as 2:6, which makes it the book's signature charge."),
  ("Sworn by the Excellency of Jacob (vv.7-8)",
   "God swears by the excellency of Jacob, the same thing he said he abhorred at 6:8, "
   "which gives the oath an edge. Surely I will never forget any of their works. The "
   "land trembling and rising and sinking like the river of Egypt makes the response "
   "geological, and the Nile comparison would be recognised as an annual flood, "
   "something that comes round without fail."),
  ("The Sun Going Down at Noon (vv.9-10)",
   "The imagery goes cosmic: the sun set at noon, the earth darkened in the clear day. "
   "Then the reversals -- feasts turned into mourning, songs into lamentation, "
   "sackcloth on all loins, baldness on every head. Verse 10 ends with it made like "
   "the mourning of an only son, which is the sharpest grief the culture had a word "
   "for."),
  ("A Famine of Hearing the Words of the LORD (vv.11-14)",
   "The chapter's most devastating sentence, and its severity depends on the whole book "
   "having been a stream of words they did not want. A famine not of bread nor thirst "
   "for water, but of hearing the words of the LORD. They will wander from sea to sea "
   "seeking it and not find it. The judgment is the removal of the very thing they had "
   "been telling Amos to stop saying."),
],
"amos9": [
  ("Fifth Vision: The Lord Standing upon the Altar (vv.1-4)",
   "The last vision puts God at the altar, and not to receive worship -- he commands "
   "the lintel struck and the thresholds shaken. What follows is a list of hiding "
   "places, each ruled out: Sheol, heaven, the top of Carmel, the bottom of the sea, "
   "captivity among enemies. The passage is the negative of Psalm 139, the same "
   "inescapable presence with the sign reversed."),
  ("Doxology: He That Buildeth His Stories in the Heaven (vv.5-6)",
   "Another creation doxology dropped into the judgment, the third in the book. He "
   "touches the land and it melts, he builds his upper chambers in the heavens and "
   "calls for the waters of the sea. The refrain that closes it is the one Amos uses "
   "for this purpose throughout: the LORD is his name. The point is that the God doing "
   "the judging is the one who made the place."),
  ("Are Ye Not as the Ethiopians? (vv.7-10)",
   "The hardest verse for the original audience: are ye not as children of the "
   "Ethiopians unto me, O children of Israel? The exodus is set beside God bringing the "
   "Philistines from Caphtor and the Syrians from Kir. Their founding story is not "
   "denied but placed among others. Then the sieve image -- the house of Israel sifted "
   "among the nations, with not the least grain falling to the earth, which cuts both "
   "ways at once."),
  ("The Tabernacle of David Raised Up (vv.11-12)",
   "The turn, and it is abrupt even by Amos's standards. In that day I will raise up "
   "the tabernacle of David that is fallen -- a booth or hut rather than a palace, "
   "which fits a dynasty in ruins. James quotes these two verses at the Jerusalem "
   "council in Acts 15 and reads the remnant of Edom and the heathen called by God's "
   "name as the inclusion of Gentiles, which is a considerable weight to rest on a "
   "sentence in Amos."),
  ("Planted, and No More Pulled Up (vv.13-15)",
   "The book ends in agricultural excess: the ploughman overtaking the reaper, the "
   "treader of grapes overtaking the sower, the mountains dropping sweet wine. For a "
   "farmer-prophet who has spent nine chapters on failed harvests, this is the "
   "reversal that means most. The final clause is permanence -- planted upon their land "
   "and no more pulled up -- which answers a book that began with a nation about to be "
   "uprooted."),
],
}

CAPS = re.compile(r"\b[A-Z]{2,}\b")


def normalise(text):
    """Fix the emphatic capitals and typos, leaving everything else alone."""
    hits = []
    for bad, good in NORMALISE.items():
        n = len(re.findall(rf"\b{bad}\b", text))
        if n:
            text = re.sub(rf"\b{bad}\b", good, text)
            hits.append(f"{bad}->{good}")
    for bad, good in TYPOS.items():
        if bad in text:
            text = text.replace(bad, good)
            hits.append(f"{bad!r} typo")
    return text, hits


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
            elif name is None and rest == "Structure:":
                pass
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

        for want in KEEP:
            fields[want], hits = normalise(fields[want])
            if hits:
                notes.append(f"{page}: {want} {', '.join(hits)}")

        sections = SECTIONS[page]
        covered = set()
        for want in KEEP:
            stray = sorted({w for w in CAPS.findall(fields[want]) if w not in CAPS_OK})
            if stray:
                problems.append(f"{page}: capitals {stray} still in {want}")
        for head, body in sections:
            stray = sorted({w for w in CAPS.findall(body) if w not in CAPS_OK})
            if stray:
                problems.append(f"{page}: capitals {stray} in {head!r}")
            if "*" in body:
                problems.append(f"{page}: markdown asterisk in {head!r}")
            if re.search(r"\(vv?\.\s+\d", head):
                problems.append(f"{page}: spaced verse range in {head!r}")
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
        for want in KEEP:
            parts.append(ITEM.format(label=want, body=fields[want]) + "\n")
        for head, prose in sections:
            parts.append(ITEM.format(label=head + ":", body=prose) + "\n")
        new_body = "".join(parts) + "            </div>\n\n            "

        new = html[:pane.start(2)] + new_body + html[pane.end(2):]
        o, c = len(re.findall(r"<div\b", new)), len(re.findall(r"</div>", new))
        if o != c:
            problems.append(f"{page}: div imbalance {o} vs {c}")
            continue
        if "auth-sublist" in new:
            problems.append(f"{page}: sublist survived")
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
