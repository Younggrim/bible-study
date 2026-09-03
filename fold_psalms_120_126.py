#!/usr/bin/env python3
"""
Psalms 120 to 126. Seven pages, 47 verses. All seven outlines are gapless and are folded.
Seven pages rather than six because these are short psalms and the sections are short with
them, on the same principle applied to Proverbs and to the shorter psalms of Books I to IV.

These are the first seven of the fifteen Songs of Ascents, Psalms 120 to 134, sung by pilgrims
going up to Jerusalem for the feasts. Each page notes where its psalm sits in that sequence when
the position tells the reader something, since the collection moves deliberately from exile
among hostile neighbours in Psalm 120 to the blessing pronounced in the temple at night in Psalm
134.

psalms121 opens with a line KJV punctuates as a statement and the Hebrew leaves open. I will
lift up mine eyes unto the hills, from whence cometh my help may be one sentence or a question
answered in verse 2, and the difference matters, because the hills were where the shrines were.
The section states both readings rather than expounding the punctuation.

Usage:
    python3 fold_psalms_120_126.py [--check]
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
"psalms120": [
 ("In My Distress I Cried unto the LORD (v.1)",
  "In my distress I cried unto the LORD, and he heard me. The first of the fifteen Songs of Ascents, and it "
  "begins the pilgrimage as far from Jerusalem as the collection gets. The hearing is reported in the past "
  "tense before the complaint is made, which sets the whole psalm inside an answer already given."),
 ("Deliver My Soul from Lying Lips (v.2)",
  "Deliver my soul, O LORD, from lying lips, and from a deceitful tongue. The trouble in this psalm is "
  "entirely verbal, and the request is for rescue from speech rather than from violence. That is worth "
  "noticing at the head of a pilgrim collection: what drives the singer toward Jerusalem is not an army."),
 ("What Shall Be Done unto Thee, Thou False Tongue (vv.3-4)",
  "What shall be given unto thee? or what shall be done unto thee, thou false tongue? The psalm addresses the "
  "tongue directly and answers its own question with two images, sharp arrows of the mighty, with coals of "
  "juniper. Juniper renders a desert broom whose wood burns hot and holds its heat, so both pictures are of "
  "something that carries at a distance and does not go out quickly, which is what the psalm thinks slander "
  "is."),
 ("I Am for Peace, but They Are for War (vv.5-7)",
  "Woe is me, that I sojourn in Mesech, that I dwell in the tents of Kedar. The two places are at opposite "
  "ends of the known world, Meshech far to the north and Kedar in the Arabian desert, and nobody lives in "
  "both; the pairing is a way of saying surrounded rather than a report of an address. My soul hath long "
  "dwelt with him that hateth peace. Then the last verse, which states the mismatch without resolving it, I "
  "am for peace: but when I speak, they are for war. The psalm ends there, and the collection's answer is not "
  "an argument but a journey."),
],
"psalms121": [
 ("I Will Lift Up Mine Eyes unto the Hills (v.1)",
  "I will lift up mine eyes unto the hills, from whence cometh my help. KJV reads this as one statement. The "
  "Hebrew has no punctuation and can as easily be read as a question, from whence cometh my help, answered in "
  "verse 2, which is how most modern versions take it. The difference is not small. On the first reading the "
  "hills are where help comes from; on the second they are the problem, since high places were where the "
  "shrines stood, and a traveller looking up at them is looking at the competition. Verse 2 fits the second "
  "reading better, and this page does not pretend the matter is settled."),
 ("My Help Cometh from the LORD (v.2)",
  "My help cometh from the LORD, which made heaven and earth. The answer names a person rather than a place, "
  "and the credential offered is the largest available. If the hills were the question, this is the "
  "correction: the one who made them is not one of them."),
 ("He That Keepeth Israel Shall Neither Slumber nor Sleep (vv.3-4)",
  "He will not suffer thy foot to be moved: he that keepeth thee will not slumber. The psalm changes voice "
  "here and someone else speaks to the traveller, which is why it reads as a blessing pronounced over a "
  "person setting out. A moved foot is what a mountain path threatens. And the promise is stated twice, in "
  "the negative both times, behold, he that keepeth Israel shall neither slumber nor sleep, which is the "
  "opposite of Baal on Carmel in 1 Kings 18:27, who Elijah suggests may be asleep."),
 ("Thy Shade upon Thy Right Hand (vv.5-6)",
  "The LORD is thy keeper: the LORD is thy shade upon thy right hand. Keeper is the word that holds this psalm "
  "together, used six times in eight verses. Shade is what a traveller in that country wants most, and it is "
  "offered at the right hand, the place where a companion walks. The sun shall not smite thee by day, nor the "
  "moon by night, where the moon is included for completeness rather than because it burns."),
 ("Thy Going Out and Thy Coming In (vv.7-8)",
  "The LORD shall preserve thee from all evil: he shall preserve thy soul. The scope widens from sunstroke to "
  "everything, and the last verse covers the whole journey in both directions, thy going out and thy coming "
  "in, and then the whole of time, from this time forth, and even for evermore. The psalm makes no promise "
  "that nothing will happen; what it promises is a keeper who is awake."),
],
"psalms122": [
 ("I Was Glad When They Said unto Me (v.1)",
  "I was glad when they said unto me, Let us go into the house of the LORD. The invitation comes from other "
  "people, which is the point: pilgrimage was a group undertaking and the gladness is at being included. "
  "Parry's setting made this the anthem at English coronations, which has given the verse a grandeur the "
  "original does not need."),
 ("Our Feet Shall Stand Within Thy Gates (v.2)",
  "Our feet shall stand within thy gates, O Jerusalem. One verse, and it is the arrival. The tense is "
  "ambiguous in Hebrew and can be read as standing now or about to stand, which suits a psalm sung both on "
  "the road and at the gate."),
 ("A City That Is Compact Together (vv.3-5)",
  "Jerusalem is builded as a city that is compact together. The compactness is admired as a figure for the "
  "nation, since the next verse is about the tribes arriving from everywhere and fitting inside one place, "
  "whither the tribes go up, the tribes of the LORD. Two things are named as what the city is for, worship "
  "and law, to give thanks unto the name of the LORD, and for there are set thrones of judgment, the thrones "
  "of the house of David. The psalm sees no tension between the temple and the courts."),
 ("Pray for the Peace of Jerusalem (vv.6-9)",
  "Pray for the peace of Jerusalem: they shall prosper that love thee. The Hebrew of these verses plays on the "
  "sound of the city's name and the word shalom over and over, which no English version can carry. Peace be "
  "within thy walls, and prosperity within thy palaces. The motive given is not patriotism but other people, "
  "for my brethren and companions' sakes, I will now say, Peace be within thee, and then the building itself, "
  "because of the house of the LORD our God I will seek thy good. The psalm asks for the city's welfare on "
  "behalf of everyone who has to come there."),
],
"psalms123": [
 ("Unto Thee Lift I Up Mine Eyes (v.1)",
  "Unto thee lift I up mine eyes, O thou that dwellest in the heavens. Psalm 121 lifted its eyes to the hills "
  "and had to ask what they were good for; this one goes straight past them. Four verses is the whole psalm."),
 ("As the Eyes of Servants unto the Hand of Their Masters (v.2)",
  "Behold, as the eyes of servants look unto the hand of their masters, and as the eyes of a maiden unto the "
  "hand of her mistress; so our eyes wait upon the LORD our God. The comparison is exact and worth slowing "
  "down for: a servant watches the hand, not the face, because instructions and provision both come from "
  "there. What is described is attention without any power to hurry the outcome, which the last clause admits, "
  "until that he have mercy upon us."),
 ("Have Mercy upon Us, O LORD (v.3)",
  "Have mercy upon us, O LORD, have mercy upon us: for we are exceedingly filled with contempt. The request "
  "is doubled because the psalm has nothing else to offer, and the ground given is not innocence but "
  "saturation. Filled is a word for being full of food."),
 ("The Scorning of Those That Are at Ease (v.4)",
  "Our soul is exceedingly filled with the scorning of those that are at ease, and with the contempt of the "
  "proud. The psalm's one piece of analysis is in the phrase at ease: the scorn comes from people whose own "
  "position is comfortable, and that is offered as the explanation of how they can afford it. The psalm ends "
  "here, with no reply and no rescue, which is the servant's posture of verse 2 held to the last line."),
],
"psalms124": [
 ("If It Had Not Been the LORD Who Was on Our Side (vv.1-5)",
  "If it had not been the LORD who was on our side, now may Israel say. The psalm is built on a condition it "
  "never completes in the ordinary way, and it repeats the opening clause so the congregation can say it "
  "after the leader. What follows is what did not happen, told as though it had, then they had swallowed us "
  "up quick, where quick means alive. The second picture is water and it rises through three verses, then the "
  "waters had overwhelmed us, the stream had gone over our soul, then the proud waters had gone over our "
  "soul. The whole strength of the psalm is in describing a disaster that was avoided."),
 ("As a Bird out of the Snare of the Fowlers (vv.6-7)",
  "Blessed be the LORD, who hath not given us as a prey to their teeth. The teeth belong to the swallowing of "
  "verse 3, so the psalm keeps its own images in order. Then the change of scale, from flood and beast to "
  "something small, our soul is escaped as a bird out of the snare of the fowlers: the snare is broken, and "
  "we are escaped. Escaped is said twice, and the second time the reason is given: the trap was destroyed "
  "rather than merely survived."),
 ("Our Help Is in the Name of the LORD (v.8)",
  "Our help is in the name of the LORD, who made heaven and earth. The same credential Psalm 121:2 uses, and "
  "it closes this psalm as a formula rather than an argument. The Church has used the verse as the opening "
  "versicle of daily prayer for centuries, which is a reasonable use of a line built to be said by a group."),
],
"psalms125": [
 ("As Mount Zion, Which Cannot Be Removed (v.1)",
  "They that trust in the LORD shall be as mount Zion, which cannot be removed, but abideth for ever. The "
  "comparison is to a hill rather than to a fortress, so what is claimed is permanence and not strength. "
  "Trust is the only condition named."),
 ("As the Mountains Are Round About Jerusalem (v.2)",
  "As the mountains are round about Jerusalem, so the LORD is round about his people from henceforth even for "
  "ever. The psalm looks at the actual geography of the city, which sits in a bowl with higher ground on most "
  "sides, and reads the ring of hills as a picture of protection. Verse 1 made the people a mountain; this "
  "verse puts the mountains around them, and the two figures are not consistent, which is normal in Hebrew "
  "poetry and not a fault."),
 ("The Rod of the Wicked Shall Not Rest (v.3)",
  "For the rod of the wicked shall not rest upon the lot of the righteous. The promise is about duration, not "
  "absence: the rod is real and what is denied is its permanence. And the reason given is the most "
  "psychologically honest line in the Songs of Ascents, lest the righteous put forth their hands unto "
  "iniquity, which says plainly that oppression prolonged past a certain point corrupts the people it falls "
  "on. God is said to shorten it for their sake rather than to spare their feelings."),
 ("Peace Shall Be upon Israel (vv.4-5)",
  "Do good, O LORD, unto those that be good, and to them that are upright in their hearts. The prayer is "
  "frankly discriminating and the psalm makes no apology for it. As for such as turn aside unto their crooked "
  "ways, the LORD shall lead them forth with the workers of iniquity, so those who leave the road are counted "
  "with the people they resemble rather than with the people they came from. Then the last three words, which "
  "belong to the pilgrimage rather than to the argument, but peace shall be upon Israel."),
],
"psalms126": [
 ("We Were like Them That Dream (vv.1-3)",
  "When the LORD turned again the captivity of Zion, we were like them that dream. The return from exile "
  "described as something too good to be credited while it was happening, and the psalm's honesty is in "
  "admitting that it did not feel real. Then was our mouth filled with laughter, and our tongue with singing. "
  "Even the neighbours are quoted, then said they among the heathen, The LORD hath done great things for them, "
  "and the congregation takes the sentence up in its own mouth in the next verse with one word changed, for "
  "us."),
 ("As the Streams in the South (v.4)",
  "Turn again our captivity, O LORD, as the streams in the south. The psalm has just described a restoration "
  "as finished and now asks for one, which is the situation of the returned community: the exile ended and "
  "the conditions did not improve. The south is the Negev, where the watercourses are dry stone most of the "
  "year and fill in an hour when the rain comes, so what is being asked for is a change that arrives all at "
  "once and out of nothing."),
 ("They That Sow in Tears Shall Reap in Joy (vv.5-6)",
  "They that sow in tears shall reap in joy. The psalm ends by turning its own experience into a rule, and "
  "the figure is agricultural rather than emotional: sowing is the part where you give away what you could "
  "have eaten. He that goeth forth and weepeth, bearing precious seed, shall doubtless come again with "
  "rejoicing, bringing his sheaves with him. Doubtless is the psalm's one confident word, and what it is "
  "confident about is a harvest, not a shortcut; the weeping and the going out are not skipped."),
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
