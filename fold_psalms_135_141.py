#!/usr/bin/env python3
"""
Psalms 135 to 141. Seven pages, 111 verses. All seven outlines are gapless and are folded.

psalms137 ends at verse 9 with a blessing on whoever kills Babylonian infants, and it is the
hardest verse in the psalter. The section states what the verse says, states that it is the
standard atrocity of ancient warfare and that the prophets promise Babylon exactly this in
Isaiah 13:16 and Nahum 3:10, states that the psalm asks God for it rather than doing it, and
states that the Church has commonly omitted the verse from public reading. It does not soften
the verse and it does not pretend the difficulty is settled. The alternative, quietly leaving
verse 9 unexplained on a page that covers every other verse, would be worse.

psalms139 is the psalm most often quoted in arguments about the unborn, and verses 13 to 16 do
say what they are taken to say. The section renders them without trimming and also notes that
the psalm's own subject is God's knowledge of a person rather than a doctrine of when life
begins, which is a distinction worth keeping if the verses are to carry any weight.

Usage:
    python3 fold_psalms_135_141.py [--check]
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
KEEP = ("Author:", "Date:", "Attributed Author:", "Classification:", "Key Themes:",
        "Historical Context:")
REPAIRS = {}

SECTIONS = {
"psalms135": [
 ("Israel for His Peculiar Treasure (vv.1-4)",
  "Praise ye the LORD. Praise ye the name of the LORD; praise him, O ye servants of the LORD. The psalm is "
  "assembled largely out of other scriptures, and the opening borrows from Psalm 134's address to the servants "
  "on duty, ye that stand in the house of the LORD. The reason given for praise is election, for the LORD hath "
  "chosen Jacob unto himself, and Israel for his peculiar treasure, where peculiar renders segullah, a king's "
  "private property as distinct from the treasury of the realm."),
 ("He Bringeth the Wind out of His Treasuries (vv.5-7)",
  "For I know that the LORD is great, and that our Lord is above all gods. Whatsoever the LORD pleased, that "
  "did he in heaven, and in earth, so the greatness is defined as freedom to act. Then a weather report taken "
  "almost word for word from Jeremiah 10:13, he causeth the vapours to ascend from the ends of the earth; he "
  "maketh lightnings for the rain; he bringeth the wind out of his treasuries. In Jeremiah the same lines sit "
  "in a passage mocking idols, which is where this psalm is also heading."),
 ("Sihon King of the Amorites, and Og King of Bashan (vv.8-12)",
  "Who smote the firstborn of Egypt, both of man and beast. The history is compressed to two events, the "
  "plagues and the defeat of the two kings east of the Jordan, and both are told in the words Psalm 136 uses, "
  "which is one of several signs that these two psalms were used together. Sihon king of the Amorites, and Og "
  "king of Bashan, and all the kingdoms of Canaan. The point of the pair is that they were the first "
  "territory actually taken, and gave their land for an heritage, an heritage unto Israel his people."),
 ("Thy Name, O LORD, Endureth for Ever (vv.13-14)",
  "Thy name, O LORD, endureth for ever; and thy memorial, O LORD, throughout all generations. Set against the "
  "kings just listed, the claim is about what outlasts a conquest. Then a verse quoted from the song of Moses "
  "in Deuteronomy 32:36, for the LORD will judge his people, and he will repent himself concerning his "
  "servants, where judging his people means giving them justice and repenting means changing course, not "
  "confessing fault."),
 ("They That Make Them Are like unto Them (vv.15-18)",
  "The idols of the heathen are silver and gold, the work of men's hands. Four verses lifted from Psalm 115 "
  "with one change: the list of useless organs is shorter here and ends with something the earlier psalm did "
  "not say, neither is there any breath in their mouths. Breath is what Genesis 2 gives to the man, so the "
  "statue lacks the one thing that makes a maker. And the warning is repeated unaltered, they that make them "
  "are like unto them: so is every one that trusteth in them."),
 ("Bless the LORD, O House of Israel (vv.19-21)",
  "Bless the LORD, O house of Israel: bless the LORD, O house of Aaron. Psalm 115 called on three groups; this "
  "one adds the house of Levi, which suits a psalm written for temple staff. Blessed be the LORD out of Zion, "
  "which dwelleth at Jerusalem. The last line locates the God who was just said to do whatever he pleases in "
  "heaven and earth at one address, and the psalm sees no difficulty in that."),
],
"psalms136": [
 ("The God of Gods, the Lord of Lords (vv.1-3)",
  "O give thanks unto the LORD; for he is good: for his mercy endureth for ever. The second half of every one "
  "of the twenty-six verses is the same line, which makes this the most obviously antiphonal psalm in the "
  "psalter: a leader sang the first half and the congregation answered. Jewish tradition calls it the Great "
  "Hallel. The three opening titles climb, the LORD, the God of gods, the Lord of lords, and the refrain "
  "attaches the same reason to each."),
 ("To Him That by Wisdom Made the Heavens (vv.4-9)",
  "To him who alone doeth great wonders: for his mercy endureth for ever. The creation is run through in the "
  "order of Genesis 1 and each step is given the same reason, which is the psalm's real argument: the heavens, "
  "the earth above the waters, the great lights, the sun to rule by day, the moon and stars to rule by night. "
  "Ordinary cosmology is being called an act of covenant kindness, which no other creation psalm quite says."),
 ("With a Strong Hand, and with a Stretched Out Arm (vv.10-22)",
  "To him that smote Egypt in their firstborn: for his mercy endureth for ever. Thirteen verses on the exodus "
  "and the conquest, and the refrain does not pause for the difficult ones. But overthrew Pharaoh and his host "
  "in the Red sea: for his mercy endureth for ever. The psalm applies the word hesed to the drowning of an "
  "army and to the killing of Sihon and Og, and it does so deliberately; a reader who finds that hard is "
  "reading it correctly. What the psalm means by it is that these acts delivered a people who could not "
  "deliver themselves, which is stated at the end of the run, and gave their land for an heritage, even an "
  "heritage unto Israel his servant."),
 ("Who Remembered Us in Our Low Estate (vv.23-26)",
  "Who remembered us in our low estate: for his mercy endureth for ever. The psalm leaves ancient history and "
  "changes to the first person plural, which suggests it was still being sung about troubles a long way after "
  "the exodus. Then the widest statement in it, who giveth food to all flesh, where all flesh takes in animals "
  "and foreigners alike, so the covenant kindness of the refrain is finally said of everything that eats. O "
  "give thanks unto the God of heaven."),
],
"psalms137": [
 ("By the Rivers of Babylon (vv.1-4)",
  "By the rivers of Babylon, there we sat down, yea, we wept, when we remembered Zion. The rivers are the "
  "canal system of the Euphrates plain, and the psalm is one of the few in the psalter that can be dated "
  "closely: it is written by people who were there. We hanged our harps upon the willows in the midst thereof. "
  "The instruments are put down rather than broken. What makes the situation unbearable is a request, for "
  "there they that carried us away captive required of us a song, saying, Sing us one of the songs of Zion, "
  "so the captors want the temple repertoire as entertainment. And the question refuses it, how shall we sing "
  "the LORD'S song in a strange land."),
 ("If I Forget Thee, O Jerusalem (vv.5-6)",
  "If I forget thee, O Jerusalem, let my right hand forget her cunning. The oath is a musician's: the right "
  "hand plays and the tongue sings, and the singer stakes both on remembering. If I prefer not Jerusalem above "
  "my chief joy. The refusal of verse 4 is thus not sullenness but a vow, and these two verses are the psalm's "
  "centre."),
 ("O Daughter of Babylon, Who Art to Be Destroyed (vv.7-9)",
  "Remember, O LORD, the children of Edom in the day of Jerusalem; who said, Rase it, rase it, even to the "
  "foundation thereof. Edom is named before Babylon because Edom was kin, and the charge is cheering at the "
  "sack; Obadiah is a whole book about the same grievance. Then the last two verses, which are the hardest in "
  "the psalter. O daughter of Babylon, who art to be destroyed; happy shall he be, that rewardeth thee as thou "
  "hast served us. Happy shall he be, that taketh and dasheth thy little ones against the stones. Several "
  "things are true at once and none of them cancels the rest. The atrocity described was the ordinary "
  "practice of ancient warfare and had been done to Jerusalem's own children, which is what as thou hast "
  "served us means. The prophets promise Babylon precisely this, in Isaiah 13:16 and in Nahum 3:10, so the "
  "psalm is asking for a judgement already announced rather than inventing one. And the psalm asks: it takes "
  "no action, and the verse is a prayer handed to God by people with no power to carry it out. None of that "
  "makes the sentence pleasant to read, and it should not be made to. The Church has largely dealt with the "
  "verse by leaving it out, and the daily offices of several traditions still stop at verse 6. What the psalm "
  "gives, and what an edited version does not, is the sound of grief that has gone past what it can carry, "
  "recorded in scripture without approval and without deletion."),
],
"psalms138": [
 ("Before the Gods Will I Sing Praise (vv.1-3)",
  "I will praise thee with my whole heart: before the gods will I sing praise unto thee. The gods may be the "
  "gods of the nations, before whom the praise is a provocation, or the judges and powers of the earth, which "
  "the same Hebrew word can mean; either way the singing is done in front of rivals. I will worship toward thy "
  "holy temple. Then a clause that reads oddly and is textually disputed, for thou hast magnified thy word "
  "above all thy name, which some read as above all, thy name and thy word, and the Hebrew word order allows "
  "the doubt. The occasion is an answered prayer, in the day when I cried thou answeredst me."),
 ("All the Kings of the Earth Shall Praise Thee (vv.4-5)",
  "All the kings of the earth shall praise thee, O LORD, when they hear the words of thy mouth. One man's "
  "answered prayer becomes the ground for expecting kings to sing, which is a large step and the psalm takes "
  "it without argument. What they are said to respond to is words rather than power."),
 ("He Hath Respect unto the Lowly (v.6)",
  "Though the LORD be high, yet hath he respect unto the lowly: but the proud he knoweth afar off. The verse "
  "turns height into a reason for attention rather than distance, and then reverses the expectation about the "
  "proud, who are the ones held at arm's length. Knowing from afar is not ignorance; it is refusal to come "
  "close."),
 ("The LORD Will Perfect That Which Concerneth Me (vv.7-8)",
  "Though I walk in the midst of trouble, thou wilt revive me. The trouble is granted rather than denied, "
  "which is this psalm's habit, and both of its last two verses begin by conceding something. The LORD will "
  "perfect that which concerneth me, where perfect means finish. And then the last line, which is a prayer "
  "made out of an argument, forsake not the works of thine own hands, so the speaker asks God not to abandon "
  "his own workmanship."),
],
"psalms139": [
 ("Thou Hast Searched Me, and Known Me (vv.1-6)",
  "O LORD, thou hast searched me, and known me. The psalm opens with the fact and spends six verses on how "
  "thorough it is, and the examples chosen are deliberately ordinary, my downsitting and mine uprising, my "
  "path and my lying down. Speech is covered before it happens, for there is not a word in my tongue, but, lo, "
  "O LORD, thou knowest it altogether. Thou hast beset me behind and before, where beset is a siege word and "
  "the being known is not yet obviously comfortable. Such knowledge is too wonderful for me; it is high, I "
  "cannot attain unto it."),
 ("Whither Shall I Go from Thy Spirit (vv.7-12)",
  "Whither shall I go from thy spirit? or whither shall I flee from thy presence? The question is asked as a "
  "man looking for an exit, and the psalm then closes every one. Height and depth first, if I ascend up into "
  "heaven, thou art there: if I make my bed in hell, behold, thou art there, where hell is Sheol, the place of "
  "the dead. Then distance, if I take the wings of the morning, and dwell in the uttermost parts of the sea, "
  "and the answer changes tone, even there shall thy hand lead me, and thy right hand shall hold me, so what "
  "began as pursuit is described as escort. Last, darkness, and the psalm dismisses it in one line, the "
  "darkness and the light are both alike to thee."),
 ("Fearfully and Wonderfully Made (vv.13-18)",
  "For thou hast possessed my reins: thou hast covered me in my mother's womb. The psalm's answer to the "
  "inescapability of God is not resignation but the reason for it, which is that he was there first. I will "
  "praise thee; for I am fearfully and wonderfully made. My substance was not hid from thee, when I was made "
  "in secret, and curiously wrought in the lowest parts of the earth, where curiously wrought is the word used "
  "of embroidery. Then verse 16, thine eyes did see my substance, yet being unperfect; and in thy book all my "
  "members were written, which in continuance were fashioned, when as yet there was none of them. These verses "
  "are the ones most often cited in arguments about the unborn, and they do say that God attended to a person "
  "before that person existed to be seen. It is worth being clear what the psalm is doing with them: the "
  "subject under discussion is God's knowledge of this particular man, and the womb is produced as the "
  "earliest available proof of it rather than as a definition of when life begins. The verses will bear the "
  "weight put on them more steadily if that is kept in view. How precious also are thy thoughts unto me, O "
  "God, and they are counted like sand, and the section ends in the morning, when I awake, I am still with "
  "thee."),
 ("I Hate Them with Perfect Hatred (vv.19-22)",
  "Surely thou wilt slay the wicked, O God: depart from me therefore, ye bloody men. The turn is abrupt and "
  "many readers find it spoils the psalm, arriving four verses after the sand and the waking. The ground given "
  "is not personal injury, for they speak against thee wickedly, and thine enemies take thy name in vain, and "
  "the questions that follow ask whether hating God's enemies is not the right response, do not I hate them, O "
  "LORD, that hate thee. I hate them with perfect hatred, where perfect is the word for complete or whole, so "
  "the claim is of an undivided attitude rather than an intense one. Whether that claim is one a reader should "
  "make is a real question, and the psalm's own next two verses suggest the writer was not certain either."),
 ("Search Me, O God, and Know My Heart (vv.23-24)",
  "Search me, O God, and know my heart: try me, and know my thoughts. This is the same verb the psalm opened "
  "with, and the difference is everything: verse 1 reported that the searching had happened, and verse 23 asks "
  "for it. Between them stand the four verses of hatred, which is very likely why the request is made. And see "
  "if there be any wicked way in me, and lead me in the way everlasting. Having just described his enemies' "
  "way, the writer asks whether he is on it, and the psalm ends with that question open rather than answered."),
],
"psalms140": [
 ("Adders' Poison Is Under Their Lips (vv.1-3)",
  "Deliver me, O LORD, from the evil man: preserve me from the violent man. The danger is described first as "
  "intention, which imagine mischiefs in their heart, and then as speech, they have sharpened their tongues "
  "like a serpent; adders' poison is under their lips. Paul quotes that last clause in Romans 3:13 as part of "
  "his case that everyone is implicated, which turns a psalm about other people into a psalm about the reader."),
 ("They Have Set Gins for Me (vv.4-5)",
  "Keep me, O LORD, from the hands of the wicked; preserve me from the violent man. The request is repeated "
  "from verse 1, and what is added is the method of the attack: a snare, cords, a net by the wayside, and gins, "
  "which is an old English word for a spring trap. Every image is of something hidden on a path, so the psalm "
  "is about walking somewhere and not about being besieged."),
 ("Thou Hast Covered My Head in the Day of Battle (vv.6-7)",
  "I said unto the LORD, Thou art my God: hear the voice of my supplications. The psalm stops describing the "
  "enemy and states a relation, which is the turn. O GOD the Lord, the strength of my salvation, thou hast "
  "covered my head in the day of battle. The evidence offered is past protection in the one place a head most "
  "needs it, and it is offered as ground for expecting more."),
 ("Let the Mischief of Their Own Lips Cover Them (vv.8-11)",
  "Grant not, O LORD, the desires of the wicked: further not his wicked device. The first request is that a "
  "prayer be refused, and the reason given is not the speaker's safety, lest they exalt themselves. Then the "
  "imprecation, and it is the mirror kind, let the mischief of their own lips cover them, so the poison of "
  "verse 3 is asked to return to its source. Let burning coals fall upon them: let them be cast into the fire; "
  "into deep pits, that they rise not up again. The severity is real, and the one restraint in it is that "
  "every clause asks God to do it."),
 ("The Cause of the Afflicted (vv.12-13)",
  "I know that the LORD will maintain the cause of the afflicted, and the right of the poor. The psalm ends by "
  "widening from its own case to a class of people, and what it claims is a legal habit rather than a rescue. "
  "Surely the righteous shall give thanks unto thy name: the upright shall dwell in thy presence. Dwelling is "
  "the reward named, which after five verses of traps is a promise about staying still."),
],
"psalms141": [
 ("Let My Prayer Be Set Forth as Incense (vv.1-2)",
  "LORD, I cry unto thee: make haste unto me. The urgency is in the second clause and the psalm never quite "
  "loses it. Let my prayer be set forth before thee as incense; and the lifting up of my hands as the evening "
  "sacrifice. The comparison is to the daily offering at dusk, which is why this has been the evening psalm of "
  "the Church since at least the fourth century, and it makes a claim worth noticing: private prayer is "
  "offered as the equivalent of the temple ritual, by someone who is not at the temple."),
 ("Keep the Door of My Lips (vv.3-4)",
  "Set a watch, O LORD, before my mouth; keep the door of my lips. Most laments ask for protection from other "
  "people's speech; this one asks for protection from its own, and the images are of a sentry and a gate. "
  "Incline not my heart to any evil thing. Then a request about company and appetite together, let me not eat "
  "of their dainties, since sharing a table was the ordinary way of joining a faction."),
 ("Let the Righteous Smite Me (v.5)",
  "Let the righteous smite me; it shall be a kindness: and let him reprove me; it shall be an excellent oil, "
  "which shall not break my head. The verse asks for correction and calls a blow from the right person a "
  "favour, setting it against the dainties of the previous verse: bad company feeds you and a friend hits you. "
  "Oil that does not break the head is anointing rather than injury, and Proverbs 27:6 makes the same "
  "comparison."),
 ("Let the Wicked Fall into Their Own Nets (vv.6-10)",
  "When their judges are overthrown in stony places, they shall hear my words; for they are sweet. Verses 6 "
  "and 7 are among the most obscure in the psalter and no confident translation exists; our bones are "
  "scattered at the grave's mouth, as when one cutteth and cleaveth wood upon the earth is a literal rendering "
  "of a text whose subject and situation are both unclear, and any smooth version of it has been guessed at. "
  "What is plain is where the psalm goes next, but mine eyes are unto thee, O GOD the Lord. Keep me from the "
  "snares which they have laid for me, and the gins of the workers of iniquity, which is the vocabulary of "
  "Psalm 140. And the last line asks only for the traps to work the other way, let the wicked fall into their "
  "own nets, whilst that I withal escape."),
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
        if "<li>" in pane or "auth-sublist" in pane:
            found.append(f"{page}: sublist survived the fold")
        if len(set(labels)) != len(labels):
            dup = sorted({l for l in labels if labels.count(l) > 1})
            found.append(f"{page}: duplicate label(s) {dup}")
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
        found = [H.unescape(l).strip() for l, _ in ITEM_RE.findall(body_html)]
        keep = [[l, b.strip()] for l, b in ITEM_RE.findall(body_html)
                if H.unescape(l).strip() in KEEP]
        if not keep:
            problems.append(f"{page}: no book fields found to preserve")
            continue
        for label in found:
            if label not in KEEP:
                notes.append(f"{page}: dropped inherited item {label!r}")
        for i, (label, body) in enumerate(keep):
            for old, new in REPAIRS.get(page, []):
                if old in body:
                    keep[i][1] = body = body.replace(old, new)
                    notes.append(f"{page}: repaired {old!r} in {label}")
        parts = ["\n                <h3>Authorship &amp; Background</h3>\n"]
        for label, body in keep:
            parts.append(ITEM.format(label=label, body=body) + "\n")
        notes.append(f"{page}: kept {len(keep)} book field(s)")
        for label, prose in sections:
            parts.append(ITEM.format(label=label + ":", body=prose) + "\n")
            notes.append(f"{page}: {label}")
        new_body = "".join(parts) + "            </div>\n\n            "
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
          f"{sum(len(v) for v in SECTIONS.values())} section(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
