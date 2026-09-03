#!/usr/bin/env python3
"""
Psalms 91 to 96. Six pages, 83 verses. All six outlines are gapless and are folded.

psalms91 carries a difficulty that belongs on the page rather than in a footnote: Satan
quoted verses 11 and 12 at the temptation, and quoted them accurately. The section says so,
because the promise of angelic keeping is the one text in the psalter with a recorded misuse,
and a reader who meets the verses only as comfort has met half of them.

psalms95 is quoted at length in Hebrews 3 and 4, where the argument turns on the word today
still being open. The superscription is silent about authorship and Hebrews 4:7 says in
David; the section notes both without deciding.

psalms96 stands almost word for word in 1 Chronicles 16:23-33, where it is sung at the
bringing up of the ark. That is the ground of the Davidic attribution, and it is also the
clearest case in the psalter of one text serving twice.

Usage:
    python3 fold_psalms_091_096.py [--check]
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
"psalms91": [
 ("He That Dwelleth in the Secret Place (vv.1-2)",
  "He that dwelleth in the secret place of the most High shall abide under the shadow of the Almighty. Two "
  "divine names in one line, Elyon and Shaddai, and the verse is a statement about a place rather than a "
  "promise about an outcome. Then the speaker answers it in his own voice, I will say of the LORD, He is my "
  "refuge and my fortress, which brings in the covenant name and Elohim as well. Four names for God in two "
  "verses is the psalm announcing its scope: shelter from every direction at once."),
 ("The Snare of the Fowler and the Noisome Pestilence (vv.3-8)",
  "Surely he shall deliver thee from the snare of the fowler, and from the noisome pestilence. The dangers "
  "come in pairs and cover the whole clock, terror by night and the arrow that flieth by day, pestilence "
  "that walketh in darkness and destruction that wasteth at noonday. The image of covering is a bird's, he "
  "shall cover thee with his feathers, and under his wings shalt thou trust, and the next clause turns "
  "soft into hard, his truth shall be thy shield and buckler. A thousand shall fall at thy side, and ten "
  "thousand at thy right hand, but it shall not come nigh thee. Read as arithmetic that is a promise of "
  "immunity, and the psalter elsewhere does not keep it; read as the confession of a man inside the shelter "
  "it is a statement about who holds him, not a guarantee about what will not happen."),
 ("Because Thou Hast Made the LORD Thy Habitation (v.9)",
  "Because thou hast made the LORD, which is my refuge, even the most High, thy habitation. One verse, and "
  "it does the work of a hinge by naming the condition on everything around it. Dwelling is the whole "
  "requirement, and the line slips between persons, my refuge and thy habitation in the same breath, as "
  "though the speaker were handing over an address he already lives at."),
 ("He Shall Give His Angels Charge over Thee (vv.10-13)",
  "There shall no evil befall thee, neither shall any plague come nigh thy dwelling. Then the two verses "
  "with a history, for he shall give his angels charge over thee, to keep thee in all thy ways, they shall "
  "bear thee up in their hands, lest thou dash thy foot against a stone. Satan quoted them at the "
  "temptation, in Matthew 4:6, and quoted them correctly; what he removed was the clause in all thy ways, "
  "which fits a man walking a road and not a man jumping off a roof. So the promise of keeping and the "
  "misuse of it stand in the same two verses, and the psalm cannot be read honestly without both. The "
  "section closes with the tread of a victor, thou shalt tread upon the lion and adder, where KJV's dragon "
  "renders tannin, a serpent or sea-creature rather than the beast of later legend."),
 ("Because He Hath Set His Love upon Me (vv.14-16)",
  "Because he hath set his love upon me, therefore will I deliver him. The voice changes for the last three "
  "verses and God speaks in the first person, which is why the psalm reads as a blessing pronounced over "
  "someone rather than a meditation. What is promised is presence before rescue, I will be with him in "
  "trouble, and the order matters: the trouble is not cancelled. With long life will I satisfy him, and "
  "shew him my salvation."),
],
"psalms92": [
 ("It Is a Good Thing to Give Thanks (vv.1-3)",
  "It is a good thing to give thanks unto the LORD, and to sing praises unto thy name, O most High. This is "
  "the only psalm in the psalter titled for the sabbath day, and it opens by calling praise good rather "
  "than required, which is a different claim. The timetable that follows covers the day from both ends, to "
  "shew forth thy lovingkindness in the morning, and thy faithfulness every night. Then the instruments, "
  "the psaltery and the harp with a solemn sound."),
 ("How Great Are Thy Works (vv.4-5)",
  "For thou, LORD, hast made me glad through thy work: I will triumph in the works of thy hands. The "
  "gladness is traced to something done rather than something felt. And the exclamation that follows sets "
  "two things side by side without joining them, O LORD, how great are thy works, and thy thoughts are "
  "very deep, so what can be seen is great and what lies behind it is out of reach."),
 ("A Brutish Man Knoweth Not (vv.6-7)",
  "A brutish man knoweth not, neither doth a fool understand this. The psalm turns abruptly, and what the "
  "fool fails to grasp is stated at once: when the wicked spring as the grass, and when all the workers of "
  "iniquity do flourish, it is that they shall be destroyed for ever. The flourishing is not evidence "
  "against God's justice but the setting for it, which is the wisdom answer to the problem Psalm 73 puts "
  "at length."),
 ("Thine Enemies Shall Perish (vv.8-9)",
  "But thou, LORD, art most high for evermore. The contrast is bare and structural, grass against "
  "permanence, and the psalm makes it by putting the two lines next to each other rather than arguing. "
  "Then the repetition that carries the emphasis, for, lo, thine enemies, O LORD, for, lo, thine enemies "
  "shall perish."),
 ("My Horn Shalt Thou Exalt (vv.10-11)",
  "But my horn shalt thou exalt like the horn of an unicorn: I shall be anointed with fresh oil. The "
  "unicorn is KJV's rendering of re'em, the wild ox, an animal known for strength rather than for legend, "
  "and the horn is the standing figure for a man's standing restored. Mine eye also shall see my desire on "
  "mine enemies. The line is candid about wanting to watch, and the psalm does not soften it."),
 ("The Righteous Shall Flourish like the Palm Tree (vv.12-15)",
  "The righteous shall flourish like the palm tree: he shall grow like a cedar in Lebanon. Two trees, and "
  "the choice answers the grass of verse 7 directly, since both of these last. The planting is located, "
  "those that be planted in the house of the LORD shall flourish in the courts of our God, so the "
  "flourishing is tied to a place and not to a temperament. They shall still bring forth fruit in old age. "
  "And the point of the whole psalm is given as testimony rather than as doctrine, to shew that the LORD is "
  "upright: he is my rock, and there is no unrighteousness in him."),
],
"psalms93": [
 ("The LORD Reigneth, Clothed with Majesty (v.1)",
  "The LORD reigneth, he is clothed with majesty; the LORD is clothed with strength, wherewith he hath "
  "girded himself. Two words in Hebrew open the psalm and they open the whole run that follows, since "
  "Psalms 93 to 99 keep returning to this announcement. The clothing figure is deliberate: majesty is worn "
  "and strength is belted on, which is the dress of a king going to work. And the consequence is stated as "
  "a fact about the world rather than about God, the world also is stablished, that it cannot be moved."),
 ("Thy Throne Is Established of Old (v.2)",
  "Thy throne is established of old: thou art from everlasting. One verse, and it forestalls the obvious "
  "objection to verse 1. A reign announced could be a reign newly seized; this says the throne predates the "
  "world it steadies, so the stability of verse 1 rests on something older than creation."),
 ("The Floods Have Lifted Up Their Voice (vv.3-4)",
  "The floods have lifted up, O LORD, the floods have lifted up their voice; the floods lift up their "
  "waves. Three clauses climbing, and the repetition is the noise itself. In the poetry of the region the "
  "sea is the standing image of what will not be governed, so the threat here is disorder rather than "
  "weather. The answer refuses to describe a fight, the LORD on high is mightier than the noise of many "
  "waters, and mightier is all it claims; there is no combat in the psalm, only a comparison."),
 ("Thy Testimonies Are Very Sure (v.5)",
  "Thy testimonies are very sure: holiness becometh thine house, O LORD, for ever. The turn is unexpected "
  "and it is the psalm's argument. Having set an unshakeable throne against an unruly sea, it ends not with "
  "power but with a word that can be trusted and a house that should match it, which moves the whole matter "
  "from cosmology to conduct in a single line."),
],
"psalms94": [
 ("O LORD God, to Whom Vengeance Belongeth (vv.1-3)",
  "O LORD God, to whom vengeance belongeth; O God, to whom vengeance belongeth, shew thyself. The phrase is "
  "said twice, and the doubling is the point of it: vengeance is claimed as God's property, which is the "
  "same claim Deuteronomy 32:35 makes and Paul repeats in Romans 12:19. The psalm is not asking for "
  "permission to retaliate but for the owner to act. Then the question that runs under every lament of this "
  "kind, LORD, how long shall the wicked triumph."),
 ("The LORD Shall Not See (vv.4-7)",
  "How long shall they utter and speak hard things? and all the workers of iniquity boast themselves? The "
  "charge is specific and it names the defenceless in the order the law names them, they slay the widow and "
  "the stranger, and murder the fatherless. And the motive is given as a theology rather than as greed, yet "
  "they say, The LORD shall not see, neither shall the God of Jacob regard it. What the oppressors have "
  "concluded is that heaven is not watching, which is the belief the next section takes apart."),
 ("He That Planted the Ear, Shall He Not Hear (vv.8-11)",
  "Understand, ye brutish among the people: and ye fools, when will ye be wise? The reply is an argument "
  "from making to capacity, he that planted the ear, shall he not hear, he that formed the eye, shall he "
  "not see, and it is one of the tightest pieces of reasoning in the psalter. A maker is not blinder than "
  "his product. The last line then turns the tables completely, the LORD knoweth the thoughts of man, that "
  "they are vanity, so the ones who assumed God could not see are the ones fully seen."),
 ("Blessed Is the Man Whom Thou Chastenest (vv.12-15)",
  "Blessed is the man whom thou chastenest, O LORD, and teachest him out of thy law. The psalm makes a move "
  "here that a complaint about injustice is not obliged to make: it calls discipline a blessing, and pairs "
  "chastening with teaching so that the one is the method of the other. The purpose is rest, that thou "
  "mayest give him rest from the days of adversity. And the ground of it is covenant, for the LORD will not "
  "cast off his people, neither will he forsake his inheritance."),
 ("My Foot Slippeth, Thy Mercy Held Me Up (vv.16-19)",
  "Who will rise up for me against the evildoers? The question is asked and left without a human answer, "
  "which is how the psalm gets to its own, unless the LORD had been my help, my soul had almost dwelt in "
  "silence. Silence here is the grave. Then the verse that reports a rescue at the moment of failure rather "
  "than before it, when I said, My foot slippeth, thy mercy, O LORD, held me up. And the one line in the "
  "psalm about the inside of a troubled head, in the multitude of my thoughts within me thy comforts "
  "delight my soul."),
 ("The Throne of Iniquity Which Frameth Mischief by a Law (vv.20-21)",
  "Shall the throne of iniquity have fellowship with thee, which frameth mischief by a law? This is the "
  "sharpest question in the psalm and it is about legislation, not crime. Wrong given statutory form is "
  "still wrong, and the psalm denies that such a court can claim God as a partner. The charge that follows "
  "is judicial murder, they gather themselves together against the soul of the righteous, and condemn the "
  "innocent blood."),
 ("The LORD Is My Defence (vv.22-23)",
  "But the LORD is my defence; and my God is the rock of my refuge. The psalm ends where it began, with the "
  "case in God's hands, and the sentence it expects is self-inflicted, he shall bring upon them their own "
  "iniquity, and shall cut them off in their own wickedness. The wickedness is the instrument. That is a "
  "narrower request than the opening cry for vengeance might suggest, and the psalm never does say what it "
  "wants done to anyone by its own hand."),
],
"psalms95": [
 ("O Come, Let Us Sing unto the LORD (vv.1-2)",
  "O come, let us sing unto the LORD: let us make a joyful noise to the rock of our salvation. The psalm is "
  "the Venite of Christian morning prayer, and it opens with a summons in the first person plural, which "
  "means the singer is inside the congregation being called. Joyful noise is a loud word, not a decorous "
  "one. Let us come before his presence with thanksgiving."),
 ("A Great King above All Gods (vv.3-5)",
  "For the LORD is a great God, and a great King above all gods. The grounds for the summons are laid out, "
  "and they are grounds of ownership: in his hand are the deep places of the earth, the strength of the "
  "hills is his also. The list runs from the lowest place to the highest and then to the sea, the sea is "
  "his, and he made it, and his hands formed the dry land, so nothing in the map is left outside the "
  "claim."),
 ("The People of His Pasture (vv.6-7a)",
  "O come, let us worship and bow down: let us kneel before the LORD our maker. The second summons is "
  "bodily where the first was vocal, and the three verbs describe a posture rather than a mood. The reason "
  "given is relation rather than power, for he is our God, and we are the people of his pasture, and the "
  "sheep of his hand, which puts the worshippers inside a flock belonging to someone."),
 ("To Day If Ye Will Hear His Voice (vv.7b-11)",
  "To day if ye will hear his voice, harden not your heart, as in the provocation, and as in the day of "
  "temptation in the wilderness. The psalm breaks off mid-verse and God speaks, and what had been a call to "
  "worship becomes a warning. Provocation and temptation render Meribah and Massah, the two place names "
  "from Exodus 17 where Israel demanded water and asked whether the LORD was among them; KJV translates the "
  "names rather than keeping them. Forty years long was I grieved with this generation. And the sentence is "
  "exclusion from rest, unto whom I sware in my wrath that they should not enter into my rest. Hebrews 3 "
  "and 4 quote this passage at length and build an argument on the single word to day, holding that the "
  "offer is still open and therefore still refusable. Hebrews 4:7 introduces the quotation with the words "
  "in David, which is the only attribution the psalm has, since the Hebrew superscription is silent."),
],
"psalms96": [
 ("O Sing unto the LORD a New Song (vv.1-3)",
  "O sing unto the LORD a new song: sing unto the LORD, all the earth. Nearly this whole psalm stands in 1 "
  "Chronicles 16:23-33, sung when David brought up the ark, which is the ground of the Davidic attribution "
  "even though the psalm itself carries no superscription. The audience is the widest the psalter uses, all "
  "the earth, and the commission is to report abroad, declare his glory among the heathen, his wonders "
  "among all people."),
 ("All the Gods of the Nations Are Idols (vv.4-6)",
  "For the LORD is great, and greatly to be praised: he is to be feared above all gods. Then the line that "
  "settles what above all gods meant, for all the gods of the nations are idols. The Hebrew turns on a "
  "likeness of sound between elohim and elilim, gods and nothings, which no English version reproduces. The "
  "proof offered is not argument but authorship, but the LORD made the heavens, and the section closes "
  "inside the building where that is confessed, strength and beauty are in his sanctuary."),
 ("Worship the LORD in the Beauty of Holiness (vv.7-9)",
  "Give unto the LORD, O ye kindreds of the people, give unto the LORD glory and strength. The imperative "
  "is repeated three times and it is addressed to families of nations, not to Israel, which means foreigners "
  "are told to bring an offering and come into his courts. O worship the LORD in the beauty of holiness. "
  "The phrase can be read as worship in holy attire or as worship in the splendour that holiness is, and "
  "the Hebrew allows both."),
 ("Say among the Heathen That the LORD Reigneth (v.10)",
  "Say among the heathen that the LORD reigneth: the world also shall be established that it shall not be "
  "moved: he shall judge the people righteously. One verse holding the whole message the singers are to "
  "carry, and it is the announcement of Psalm 93 turned into an errand. Stability and judgement arrive "
  "together, which is the psalm's reason for treating a coming assize as good news."),
 ("For He Cometh to Judge the Earth (vv.11-13)",
  "Let the heavens rejoice, and let the earth be glad; let the sea roar, and the fulness thereof. Sky, "
  "land, sea, field and forest are each given a part, and the sea that was chaos in Psalm 93 is here simply "
  "loud. Then the reason, said twice because the repetition is the joy, for he cometh, for he cometh to "
  "judge the earth. Judgement is what creation is glad about, and that is only coherent if the standard is "
  "the one named in the last line, he shall judge the world with righteousness, and the people with his "
  "truth."),
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
