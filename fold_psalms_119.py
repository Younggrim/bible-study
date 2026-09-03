#!/usr/bin/env python3
"""
Psalm 119 alone. One page, 176 verses, 22 sections. The inherited outline is gapless and is
folded; the only change to its divisions is that the verse range moves from the front of each
label to the end, so that the range sits where every other page in the collection puts it.

One page rather than six because this is the longest chapter in the Bible and its twenty-two
stanzas are the natural sections. The risk with this psalm is twenty-two paragraphs that all
say the same thing, so each section is written from what is actually in its own eight verses.

Two facts belong at the top and are placed in the stanzas where they bite. The psalm uses eight
different words for what God has said, law, testimonies, precepts, statutes, commandments,
judgments, word and ways, and nearly every verse carries one of them. And the psalm ends at
verse 176 with I have gone astray like a lost sheep, which is not a copyist's accident: a poem
of 176 verses in praise of God's instruction closes on a confession of wandering, and any
account of the psalm that leaves that out has described a different poem.

Usage:
    python3 fold_psalms_119.py [--check]
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
"psalms119": [
 ("Aleph: The Undefiled in the Way (vv.1-8)",
  "Blessed are the undefiled in the way, who walk in the law of the LORD. The psalm opens the way Psalm 1 "
  "does and with the same word, and for three verses it describes someone else. Then it changes person and "
  "the description becomes a wish, O that my ways were directed to keep thy statutes, which is the psalm "
  "admitting at verse 5 that it is not describing the writer. Every one of the eight verses in this stanza "
  "begins with aleph in Hebrew, and the same holds for each of the twenty-two stanzas with its own letter; "
  "the psalm is a schoolroom exercise carried out at enormous length. The stanza ends on a fear rather than a "
  "claim, I will keep thy statutes: O forsake me not utterly."),
 ("Beth: Wherewithal Shall a Young Man Cleanse His Way (vv.9-16)",
  "Wherewithal shall a young man cleanse his way? by taking heed thereto according to thy word. The one "
  "question in the psalm answered in the same verse it is asked, and the answer is method rather than effort. "
  "Then the line this stanza is remembered for, thy word have I hid in mine heart, that I might not sin "
  "against thee, where hidden means stored rather than concealed. The comparison at verse 14 is the first of "
  "several with money, I have rejoiced in the way of thy testimonies, as much as in all riches, and the "
  "stanza closes on delight and memory together, I will delight myself in thy statutes: I will not forget thy "
  "word."),
 ("Gimel: I Am a Stranger in the Earth (vv.17-24)",
  "Deal bountifully with thy servant, that I may live, and keep thy word. Living is asked for as the "
  "condition of obedience rather than its reward. Open thou mine eyes, that I may behold wondrous things out "
  "of thy law, which assumes that the text is adequate and the reader is not. I am a stranger in the earth: "
  "hide not thy commandments from me. The stranger's request is for directions, and that is what the whole "
  "stanza is. Then the first mention of opposition from above, princes also did sit and speak against me, met "
  "with the oddest word in the psalm, thy testimonies also are my delight and my counsellors, so a written "
  "text is called a privy council."),
 ("Daleth: My Soul Cleaveth unto the Dust (vv.25-32)",
  "My soul cleaveth unto the dust: quicken thou me according to thy word. The lowest point so far, and the "
  "figure is of something flattened rather than merely sad. My soul melteth for heaviness: strengthen thou me "
  "according unto thy word. Twice in eight verses the request is for life or strength and twice the "
  "instrument named is the word, which is this stanza's whole argument. And it ends in movement, I will run "
  "the way of thy commandments, when thou shalt enlarge my heart, where the enlarging has to come first."),
 ("He: Incline My Heart unto Thy Testimonies (vv.33-40)",
  "Teach me, O LORD, the way of thy statutes; and I shall keep it unto the end. Every verse in this stanza is "
  "a petition, which makes it the most sustained prayer in the psalm: teach, give, make, incline, turn, "
  "stablish, turn, quicken. What is asked for is not information but redirection, incline my heart unto thy "
  "testimonies, and not to covetousness, and turn away mine eyes from beholding vanity. The writer treats his "
  "own attention as something outside his control and asks for it to be moved."),
 ("Vav: I Will Walk at Liberty (vv.41-48)",
  "Let thy mercies come also unto me, O LORD, even thy salvation, according to thy word. The stanza is about "
  "having something to say, so shall I have wherewith to answer him that reproacheth me, and it asks that the "
  "supply not be cut off, take not the word of truth utterly out of my mouth. Then the psalm's central "
  "paradox stated in five words, and I will walk at liberty: for I seek thy precepts, which claims that the "
  "law is where freedom is found and not what it is taken from. And the audience widens, I will speak of thy "
  "testimonies also before kings, and will not be ashamed."),
 ("Zayin: This Is My Comfort in My Affliction (vv.49-56)",
  "Remember the word unto thy servant, upon which thou hast caused me to hope. The hope is attributed to God "
  "rather than mustered, and the stanza then says what it is worth, this is my comfort in my affliction: for "
  "thy word hath quickened me. Derision is met by not moving, the proud have had me greatly in derision: yet "
  "have I not declined from thy law. Horror hath taken hold upon me because of the wicked that forsake thy "
  "law, and horror is not too strong a word for the Hebrew. Then the loveliest line in the psalm, thy "
  "statutes have been my songs in the house of my pilgrimage, which makes the law a hymnbook and this life a "
  "lodging."),
 ("Cheth: Thou Art My Portion, O LORD (vv.57-64)",
  "Thou art my portion, O LORD: I have said that I would keep thy words. Portion is the word used of the "
  "Levites, who received no land because the LORD was their inheritance, and the writer applies it to himself. "
  "The obedience described is prompt, I made haste, and delayed not to keep thy commandments, and it survives "
  "robbery, the bands of the wicked have robbed me: but I have not forgotten thy law. At midnight I will rise "
  "to give thanks unto thee. And the stanza notices other people, which the psalm rarely does, I am a "
  "companion of all them that fear thee."),
 ("Teth: It Is Good for Me That I Have Been Afflicted (vv.65-72)",
  "Thou hast dealt well with thy servant, O LORD, according unto thy word. This stanza contains the psalm's "
  "most difficult claim and makes it twice. Before I was afflicted I went astray: but now have I kept thy "
  "word, and then plainly, it is good for me that I have been afflicted; that I might learn thy statutes. The "
  "affliction is called good for what it taught, not in itself, and the writer is speaking about his own case "
  "rather than laying down a rule to be applied to anyone else's. Their heart is as fat as grease; but I "
  "delight in thy law. Then the money comparison again, and higher than before, the law of thy mouth is "
  "better unto me than thousands of gold and silver."),
 ("Yod: Thy Hands Have Made Me and Fashioned Me (vv.73-80)",
  "Thy hands have made me and fashioned me: give me understanding, that I may learn thy commandments. The "
  "argument is from manufacture to maintenance, and it is the same reasoning Psalm 94 uses about the ear and "
  "the eye. Then the sentence that goes further than the stanza before it, I know, O LORD, that thy judgments "
  "are right, and that thou in faithfulness hast afflicted me. Faithfulness is named as the motive of the "
  "affliction, which is the hardest thing said in the psalm and is said without hedging. What follows are "
  "requests, and one of them is for reputation among the right people, let those that fear thee turn unto "
  "me."),
 ("Kaph: Like a Bottle in the Smoke (vv.81-88)",
  "My soul fainteth for thy salvation: but I hope in thy word. The most exhausted stanza in the psalm, and "
  "the question in it is impatient, mine eyes fail for thy word, saying, When wilt thou comfort me. The image "
  "at verse 83 is a wineskin left hanging over a fire until it is black and stiff, for I am become like a "
  "bottle in the smoke, which describes a man dried out rather than in pain. How many are the days of thy "
  "servant. They had almost consumed me upon earth; but I forsook not thy precepts. Almost is doing a great "
  "deal of work, and the stanza ends still asking, quicken me after thy lovingkindness."),
 ("Lamed: Thy Word Is Settled in Heaven (vv.89-96)",
  "For ever, O LORD, thy word is settled in heaven. After eight verses of a man nearly finished, the psalm "
  "looks at something that does not change, and it grounds the claim in the ordinary persistence of the world, "
  "thou hast established the earth, and it abideth. Unless thy law had been my delights, I should then have "
  "perished in mine affliction, which is a plain statement that the text kept him alive. And the stanza ends "
  "on the psalm's best epigram, I have seen an end of all perfection: but thy commandment is exceeding broad, "
  "where everything finished turns out to have a limit and this one does not."),
 ("Mem: O How Love I Thy Law (vv.97-104)",
  "O how love I thy law! it is my meditation all the day. The one exclamation of affection in the psalm, and "
  "the three verses after it sound like boasting, wiser than mine enemies, more understanding than all my "
  "teachers, I understand more than the ancients. Each is immediately grounded in something outside the "
  "speaker, for thy testimonies are my meditation, because I keep thy precepts, so the claim is about what he "
  "has been given rather than what he is. Then the taste image, how sweet are thy words unto my taste, yea, "
  "sweeter than honey to my mouth, which Ezekiel and John both repeat when they eat a scroll."),
 ("Nun: A Lamp unto My Feet (vv.105-112)",
  "Thy word is a lamp unto my feet, and a light unto my path. The best known verse in the psalm, and the "
  "light it describes is small and local: a lamp at the feet shows the next step and not the destination. I "
  "have sworn, and I will perform it. My soul is continually in my hand, which is an idiom for living at "
  "risk. And the stanza ends with the language of property, thy testimonies have I taken as an heritage for "
  "ever, so a man with no security treats the text as his estate."),
 ("Samekh: Thou Art My Hiding Place and My Shield (vv.113-120)",
  "I hate vain thoughts: but thy law do I love. Love and hatred are set as one disposition, which the psalm "
  "does several times. Thou art my hiding place and my shield: I hope in thy word. Then a dismissal, depart "
  "from me, ye evildoers, and two requests for support that concede the writer cannot stand alone, uphold me, "
  "hold thou me up. The judgement described is metallurgical, thou puttest away all the wicked of the earth "
  "like dross. And the stanza ends where a psalm about loving the law is not expected to, my flesh trembleth "
  "for fear of thee; and I am afraid of thy judgments."),
 ("Ayin: It Is Time for Thee, LORD, to Work (vv.121-128)",
  "I have done judgment and justice: leave me not to mine oppressors. The stanza opens with a claim of "
  "innocence, which the psalm makes sparingly, and follows it with a legal request, be surety for thy servant "
  "for good, asking God to stand as guarantor. Mine eyes fail for thy salvation. Then the sharpest line in "
  "the psalm, it is time for thee, LORD, to work: for they have made void thy law. It is a summons, and the "
  "ground given is not the writer's suffering but the law's disrepute. Therefore I love thy commandments above "
  "gold; yea, above fine gold."),
 ("Pe: The Entrance of Thy Words Giveth Light (vv.129-136)",
  "Thy testimonies are wonderful: therefore doth my soul keep them. The entrance of thy words giveth light; "
  "it giveth understanding unto the simple, so the light arrives with the words rather than being wrung out "
  "of them, and the beneficiary is the untrained reader. The longing is physical, I opened my mouth, and "
  "panted. Order my steps in thy word: and let not any iniquity have dominion over me. And the stanza ends "
  "with the psalm's only tears, and they are not for himself, rivers of waters run down mine eyes, because "
  "they keep not thy law."),
 ("Tsade: Thy Word Is Very Pure (vv.137-144)",
  "Righteous art thou, O LORD, and upright are thy judgments. The stanza is about the quality of the text "
  "rather than the state of the writer, and the words used are words for metal and for permanence, thy word "
  "is very pure, thy righteousness is an everlasting righteousness. My zeal hath consumed me, because mine "
  "enemies have forgotten thy words, and consumed is the word John 2:17 applies to Jesus in the temple. "
  "Against all that the writer sizes himself honestly, I am small and despised: yet do not I forget thy "
  "precepts. Trouble and anguish have taken hold on me: yet thy commandments are my delights."),
 ("Qoph: Thou Art Near, O LORD (vv.145-152)",
  "I cried with my whole heart; hear me, O LORD. The stanza is about hours, and the writer keeps getting "
  "there first, I prevented the dawning of the morning, and cried, mine eyes prevent the night watches, where "
  "prevented means came before. Then two lines set deliberately against each other. They draw nigh that "
  "follow after mischief: they are far from thy law. And immediately, thou art near, O LORD, so the same word "
  "is used of the threat and of the rescue, and the psalm lets the second cancel the first without further "
  "comment."),
 ("Resh: Plead My Cause, and Deliver Me (vv.153-160)",
  "Consider mine affliction, and deliver me: for I do not forget thy law. The language is courtroom language, "
  "plead my cause, and deliver me, and the request repeated four times in eight verses is the same one, "
  "quicken me, which is the psalm's word for being kept alive. Many are my persecutors and mine enemies; yet "
  "do I not decline from thy testimonies. The grief is again for other people, I beheld the transgressors, "
  "and was grieved. And the stanza closes on the ground of the whole psalm, thy word is true from the "
  "beginning."),
 ("Shin: Great Peace Have They Which Love Thy Law (vv.161-168)",
  "Princes have persecuted me without a cause: but my heart standeth in awe of thy word. The second mention "
  "of hostile princes, and the answer is not defiance but attention directed elsewhere. I rejoice at thy word, "
  "as one that findeth great spoil, which is the money comparison a third time and the most extravagant of "
  "them. Seven times a day do I praise thee, the verse the monastic hours were built on. Then the promise the "
  "stanza is known for, great peace have they which love thy law: and nothing shall offend them, where offend "
  "carries its older sense of causing a stumble."),
 ("Tav: I Have Gone Astray like a Lost Sheep (vv.169-176)",
  "Let my cry come near before thee, O LORD: give me understanding according to thy word. The last stanza "
  "asks for the same things as the first and adds nothing new, which is itself the psalm's report on 176 "
  "verses of prayer: the requests were not answered in a way that ends them. My lips shall utter praise, when "
  "thou hast taught me thy statutes. Let thine hand help me; for I have chosen thy precepts. And then the last "
  "verse, which is the most important line in the psalm for reading the rest of it, I have gone astray like a "
  "lost sheep; seek thy servant; for I do not forget thy commandments. A poem in praise of God's instruction, "
  "longer than most books of the Bible, ends by admitting the writer is lost and asking to be looked for. The "
  "two halves of the verse are both true at once, and the psalm's whole claim is in holding them together: he "
  "has not forgotten a word of it, and he still needs fetching."),
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
