#!/usr/bin/env python3
"""
Psalms 115 to 118. Four pages, 68 verses. All four outlines are gapless and are folded.
Four pages rather than six because psalms118 needs the room and psalms119 is folded alone.

psalms117 is two verses, the shortest chapter in the Bible, and Paul quotes it in Romans 15:11
as one of four proofs that the Gentiles were always meant to praise God. The outline divides
verse 2 into halves, which the format handles, and the sections are correspondingly short: a
two-verse psalm does not support the exposition a long one does.

psalms118 closes the Egyptian Hallel, so it is the last psalm sung at Passover and therefore
very probably the hymn of Matthew 26:30. Verses 22 and 25 and 26 are quoted at the entry into
Jerusalem and afterwards by Jesus, Peter and Paul; the sections name each use rather than
gesturing at fulfilment in general.

Usage:
    python3 fold_psalms_115_118.py [--check]
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
"psalms115": [
 ("Not unto Us, but unto Thy Name (vv.1-2)",
  "Not unto us, O LORD, not unto us, but unto thy name give glory. The refusal is said twice before the "
  "positive request arrives, which is the psalm's way of insisting on it. And the reason is not modesty but "
  "an argument in progress, wherefore should the heathen say, Where is now their God, so the glory is claimed "
  "for God because a claim is being contested."),
 ("They Have Mouths, but They Speak Not (vv.3-8)",
  "But our God is in the heavens: he hath done whatsoever he hath pleased. The answer to the taunt is "
  "freedom of action, and it is set against images that have every organ and no function. Their idols are "
  "silver and gold, the work of men's hands, and then the inventory: mouths that do not speak, eyes that do "
  "not see, ears that do not hear, noses, hands, feet. The satire runs down a body part by part and finds "
  "nothing working. Then the verse that turns it into a warning about worshippers rather than statues, they "
  "that make them are like unto them; so is every one that trusteth in them, which claims that what a person "
  "worships he comes to resemble."),
 ("O Israel, Trust Thou in the LORD (vv.9-11)",
  "O Israel, trust thou in the LORD: he is their help and their shield. The same sentence is said three times "
  "to three groups, the nation, the house of Aaron, and then a wider circle, ye that fear the LORD, which in "
  "later usage included Gentiles attached to the synagogue. The threefold call and the threefold blessing "
  "that follows suggest this psalm was sung antiphonally, with a leader and a congregation."),
 ("He Will Bless Them That Fear the LORD (vv.12-15)",
  "The LORD hath been mindful of us: he will bless us. The blessing answers the call group for group in the "
  "same order, Israel, Aaron, and them that fear the LORD, both small and great. What is promised is "
  "increase rather than rescue, the LORD shall increase you more and more, you and your children, and the "
  "authority behind it is the widest available, ye are blessed of the LORD which made heaven and earth."),
 ("The Dead Praise Not the LORD (vv.16-18)",
  "The heaven, even the heavens, are the LORD'S: but the earth hath he given to the children of men. The "
  "division is a real one in the psalter's thinking, and it is the ground for what follows. The dead praise "
  "not the LORD, neither any that go down into silence. The Old Testament says this kind of thing more than "
  "once and it is not a doctrine of annihilation but an observation about worship, since praise is something "
  "the living do in a congregation. The psalm's response is therefore about timing, but we will bless the LORD "
  "from this time forth and for evermore, which claims the whole of the available window."),
],
"psalms116": [
 ("I Love the LORD, Because He Hath Heard (vv.1-2)",
  "I love the LORD, because he hath heard my voice and my supplications. The psalm gives a reason for love, "
  "which is unusual, and the reason is a specific answered prayer rather than God's character in general. "
  "Because he hath inclined his ear unto me, therefore will I call upon him as long as I live. One hearing "
  "produces a lifetime policy."),
 ("The Sorrows of Death Compassed Me (vv.3-4)",
  "The sorrows of death compassed me, and the pains of hell gat hold upon me: I found trouble and sorrow. "
  "Hell here renders Sheol, the place of the dead rather than a place of punishment, so what is described is "
  "coming close to dying and not to damnation. The prayer that follows is four words long in effect, O LORD, "
  "I beseech thee, deliver my soul, which is what a man in that condition has breath for."),
 ("The LORD Preserveth the Simple (vv.5-6)",
  "Gracious is the LORD, and righteous; yea, our God is merciful. The psalm generalises from its own case, "
  "and the group it names as protected is not the wise or the strong, the LORD preserveth the simple. Simple "
  "means open and untrained rather than foolish. I was brought low, and he helped me."),
 ("Return unto Thy Rest, O My Soul (vv.7-9)",
  "Return unto thy rest, O my soul; for the LORD hath dealt bountifully with thee. The singer instructs "
  "himself, as Psalm 103 does, and what he orders is a return to a settled state he had left. Three "
  "deliverances are then counted off in one verse, my soul from death, mine eyes from tears, and my feet from "
  "falling. And the conclusion is about where he will live rather than how he will feel, I will walk before "
  "the LORD in the land of the living."),
 ("I Said in My Haste, All Men Are Liars (vv.10-11)",
  "I believed, therefore have I spoken: I was greatly afflicted. Paul quotes the first clause in 2 "
  "Corinthians 4:13 as the pattern of his own preaching under pressure, taking it from the Greek, which reads "
  "it more smoothly than the Hebrew does. Then a confession that the psalm makes no attempt to justify, I "
  "said in my haste, All men are liars. It is recorded as a thing said while panicking, which is why the "
  "clause about haste is there, and the psalm neither endorses it nor deletes it."),
 ("What Shall I Render unto the LORD (vv.12-19)",
  "What shall I render unto the LORD for all his benefits toward me? The last eight verses answer that "
  "question, and every item in the answer is a public act in the temple rather than a private feeling. I will "
  "take the cup of salvation, and call upon the name of the LORD, and I will pay my vows unto the LORD now in "
  "the presence of all his people, which is said twice. Between them stands the verse most often read at "
  "funerals, precious in the sight of the LORD is the death of his saints, and in context it is a statement "
  "that God does not spend their lives cheaply, which is why this man is alive to sing. The self-description "
  "is a servant's, I am thy servant, and the son of thine handmaid: thou hast loosed my bonds. And the place "
  "is named at the end, in the courts of the LORD'S house, in the midst of thee, O Jerusalem."),
],
"psalms117": [
 ("O Praise the LORD, All Ye Nations (v.1)",
  "O praise the LORD, all ye nations: praise him, all ye people. Two verses is the whole psalm, the shortest "
  "chapter in the Bible, and the first of them addresses everyone who is not Israel. Paul quotes it in Romans "
  "15:11 as one of four texts proving that the Gentiles were always in view, and it is his shortest proof and "
  "his plainest."),
 ("His Merciful Kindness Is Great Toward Us (v.2a)",
  "For his merciful kindness is great toward us: and the truth of the LORD endureth for ever. The reason "
  "given to the nations for praising is what God has done for someone else, and the psalm sees no difficulty "
  "in that. The two words are hesed and emet, covenant kindness and reliability, the pair that stands behind "
  "grace and truth in John 1:14."),
 ("Praise Ye the LORD (v.2b)",
  "Praise ye the LORD. The single word hallelujah closes the psalm, and in a poem of two verses it is a "
  "sixth of the whole. It is the same word that opens and closes the last five psalms of the psalter, so this "
  "short psalm ends the way the book will."),
],
"psalms118": [
 ("His Mercy Endureth for Ever (vv.1-4)",
  "O give thanks unto the LORD; for he is good: because his mercy endureth for ever. This is the last psalm "
  "of the Egyptian Hallel, which makes it the last thing sung at a Passover meal and very probably the hymn "
  "of Matthew 26:30, sung on the way to Gethsemane. The opening four verses are built for a congregation, "
  "with a leader calling Israel, then the house of Aaron, then them that fear the LORD, and the same line "
  "answered back each time."),
 ("It Is Better to Trust in the LORD (vv.5-18)",
  "I called upon the LORD in distress: the LORD answered me, and set me in a large place. Fourteen verses of "
  "testimony, and the shape of it is a siege that failed. The refrain of the middle is a comparison, it is "
  "better to trust in the LORD than to put confidence in man, and then in princes, which narrows from people "
  "in general to the people most worth relying on. The enemies are described three times over in the same "
  "words, they compassed me about, and then dismissed in an image of noise without duration, they are "
  "quenched as the fire of thorns. Verse 14 is quoted from the song at the sea in Exodus 15:2, the LORD is my "
  "strength and song. And the section ends by refusing to read the trouble as abandonment, the LORD hath "
  "chastened me sore: but he hath not given me over unto death."),
 ("Open to Me the Gates of Righteousness (vv.19-21)",
  "Open to me the gates of righteousness: I will go into them, and I will praise the LORD. The psalm arrives "
  "somewhere, and from here on it reads as a processional sung at the temple entrance, with the request made "
  "outside and the reply given at the door, this gate of the LORD, into which the righteous shall enter."),
 ("The Stone Which the Builders Refused (vv.22-24)",
  "The stone which the builders refused is become the head stone of the corner. In the psalm this is most "
  "likely the nation, or its king, rejected by the great powers and set in place by God. Jesus quotes it "
  "against the chief priests at the end of the parable of the vineyard in Matthew 21:42, Peter quotes it "
  "before the council in Acts 4:11 and again in 1 Peter 2:7, and Paul works with the same figure in Ephesians "
  "2:20. This is the LORD'S doing; it is marvellous in our eyes. Then the verse that has become a general "
  "sentiment and is not one, this is the day which the LORD hath made, which in context means the day of the "
  "reversal just described rather than any given morning."),
 ("Save Now, I Beseech Thee (vv.25-27)",
  "Save now, I beseech thee, O LORD. Those first two words are hoshiah-na, which comes into Greek and then "
  "English as hosanna, and it is a plea for rescue rather than a shout of praise. The next verse is what the "
  "crowds call out at the entry into Jerusalem in all four Gospels, blessed be he that cometh in the name of "
  "the LORD, and Jesus quotes it back in Matthew 23:39 as something they will say later. The section ends "
  "inside the ritual it belongs to, bind the sacrifice with cords, even unto the horns of the altar."),
 ("Thou Art My God, and I Will Praise Thee (vv.28-29)",
  "Thou art my God, and I will praise thee: thou art my God, I will exalt thee. After the crowd and the "
  "procession the psalm ends in the singular, which is how it began at verse 5. Then the opening line "
  "returns unchanged, O give thanks unto the LORD; for he is good: for his mercy endureth for ever, closing "
  "the Hallel on the sentence it started with."),
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
