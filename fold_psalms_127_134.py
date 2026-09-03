#!/usr/bin/env python3
"""
Psalms 127 to 134. Eight pages, 54 verses. All eight outlines are gapless and are folded.
Eight pages in one script because six of these psalms are six verses or shorter and the sections
are short with them; only psalms132 needs any room.

These are the last eight Songs of Ascents. The collection ends in the temple at night with the
servants on duty blessing God and being blessed back, which is the destination the pilgrimage
was for, and psalms134 says so.

psalms131 is three verses and turns on one word. The image is not a baby wanting to be fed but a
weaned child, which is a child that has stopped wanting, and the whole psalm is in that
distinction. psalms133 makes a comparison that cannot be true geographically, the dew of Hermon
falling on Zion a hundred and twenty miles south, and the section says so, because the
impossibility is the claim rather than a slip.

Usage:
    python3 fold_psalms_127_134.py [--check]
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
"psalms127": [
 ("Except the LORD Build the House (v.1)",
  "Except the LORD build the house, they labour in vain that build it: except the LORD keep the city, the "
  "watchman waketh but in vain. The superscription reads for Solomon, and the Hebrew preposition can mean of, "
  "for or about him, which matters because the two examples are a house and a city and Solomon built both. "
  "The verse does not say the labour is unnecessary. It says it is decisive only if God is in it, which is a "
  "narrower claim and a harder one."),
 ("So He Giveth His Beloved Sleep (v.2)",
  "It is vain for you to rise up early, to sit up late, to eat the bread of sorrows: for so he giveth his "
  "beloved sleep. The three phrases describe overwork exactly: the early start, the late finish, and food "
  "eaten anxiously. The last clause can be read as KJV has it, or as giving to his beloved in sleep, which is "
  "how several older versions took it and which sharpens the contrast with the sleepless work just described. "
  "Either way what is offered is rest rather than a better method."),
 ("Children Are an Heritage of the LORD (vv.3-5)",
  "Lo, children are an heritage of the LORD: and the fruit of the womb is his reward. The psalm moves from a "
  "house that has to be built to a household that is given, and the word heritage is inheritance language, "
  "used of land. As arrows are in the hand of a mighty man; so are children of the youth. The image is "
  "practical rather than sentimental: a large family meant support in a dispute, which the last line spells "
  "out, they shall speak with the enemies in the gate, the gate being where legal cases were heard."),
],
"psalms128": [
 ("Blessed Is Every One That Feareth the LORD (v.1)",
  "Blessed is every one that feareth the LORD; that walketh in his ways. The psalm follows Psalm 127 as its "
  "companion, the one about a household given and this one about a household enjoyed, and it opens with the "
  "beatitude form the psalter uses for its most general statements. Every one is doing real work in the "
  "sentence: nothing here is reserved for kings or priests."),
 ("As a Fruitful Vine by the Sides of Thine House (vv.2-4)",
  "For thou shalt eat the labour of thine hands: happy shalt thou be, and it shall be well with thee. Eating "
  "your own work is not guaranteed in an occupied country, which is why the psalm treats it as a blessing "
  "rather than a baseline. Then the household described in two plants, thy wife shall be as a fruitful vine by "
  "the sides of thine house: thy children like olive plants round about thy table. Both are slow crops that "
  "reward staying put."),
 ("The LORD Shall Bless Thee out of Zion (vv.5-6)",
  "The LORD shall bless thee out of Zion: and thou shalt see the good of Jerusalem all the days of thy life. "
  "The blessing on the private house is routed through the city, which is what makes this a pilgrim psalm "
  "rather than a domestic one. Yea, thou shalt see thy children's children, and peace upon Israel. The longest "
  "view the psalm takes is two generations, and it ends on the same three words as Psalm 125."),
],
"psalms129": [
 ("The Plowers Plowed upon My Back (vv.1-4)",
  "Many a time have they afflicted me from my youth, may Israel now say. The line is written for a "
  "congregation to repeat, and the youth in question is the nation's, which puts Egypt at the start of the "
  "list. Yet they have not prevailed against me. That clause is the psalm's whole argument, and it claims "
  "survival rather than victory. The image of the affliction is agricultural and brutal, the plowers plowed "
  "upon my back: they made long their furrows, which is a flogged back described as a field. Then the reply, "
  "and it is short, the LORD is righteous: he hath cut asunder the cords of the wicked."),
 ("As the Grass upon the Housetops (vv.5-8)",
  "Let them all be confounded and turned back that hate Zion. The curse that follows is the mildest in the "
  "psalter and the most carefully chosen. Let them be as the grass upon the housetops, which withereth afore "
  "it groweth up, since a flat mud roof grows a little grass after rain and it dies in days with no soil to "
  "hold it. What is asked for is not destruction but futility, and the two farming verses spell it out, "
  "wherewith the mower filleth not his hand; nor he that bindeth sheaves his bosom. The last verse withholds "
  "something instead of inflicting it, neither do they which go by say, The blessing of the LORD be upon you. "
  "In a culture where that greeting was said to any harvester, being passed in silence is the sentence."),
],
"psalms130": [
 ("Out of the Depths Have I Cried (vv.1-2)",
  "Out of the depths have I cried unto thee, O LORD. The Latin opening gives the psalm its old name, De "
  "Profundis, and it is one of the seven penitential psalms; Luther turned it into Aus tiefer Not and it has "
  "been sung at funerals in the West for a thousand years. The depths are not named, which is why the psalm "
  "has lent itself to so many situations."),
 ("There Is Forgiveness with Thee (vv.3-4)",
  "If thou, LORD, shouldest mark iniquities, O Lord, who shall stand? The question expects no answer and is "
  "the psalm's assessment of everybody, not just the singer. But there is forgiveness with thee, that thou "
  "mayest be feared. That last clause is the psalm's best line and it runs against the obvious expectation, "
  "since forgiveness might be thought to reduce the fear. What it claims is the opposite: a God who lets "
  "things go is one you take seriously, because you are dealing with a person and not a tariff."),
 ("More Than They That Watch for the Morning (vv.5-6)",
  "I wait for the LORD, my soul doth wait, and in his word do I hope. Waiting is said three times in two "
  "verses and the comparison chosen is a night watchman, my soul waiteth for the Lord more than they that "
  "watch for the morning. Then the line is simply said again, I say, more than they that watch for the "
  "morning, and the repetition is the length of the night."),
 ("With Him Is Plenteous Redemption (vv.7-8)",
  "Let Israel hope in the LORD: for with the LORD there is mercy, and with him is plenteous redemption. The "
  "psalm turns outward at the end, as several of the Ascents do, handing its own conclusion to the "
  "congregation. And the last verse names what is to be redeemed from, and he shall redeem Israel from all his "
  "iniquities, so the depths of verse 1 turn out to have been moral rather than circumstantial."),
],
"psalms131": [
 ("My Heart Is Not Haughty (v.1)",
  "LORD, my heart is not haughty, nor mine eyes lofty: neither do I exercise myself in great matters, or in "
  "things too high for me. Three verses is the whole psalm, and this one is entirely negative: it lists what "
  "the speaker has given up. Coming from David, whose life was nothing but great matters, the claim is about "
  "ambition rather than occupation."),
 ("As a Child That Is Weaned of His Mother (v.2)",
  "Surely I have behaved and quieted myself, as a child that is weaned of his mother: my soul is even as a "
  "weaned child. Everything in the psalm depends on the word weaned. A nursing child at its mother is the "
  "picture of wanting, and that is not the image chosen; a weaned child is one that has stopped demanding and "
  "can be held for its own sake. The quieting is also said to be something the speaker did to himself, which "
  "makes the contentment worked for rather than natural."),
 ("Let Israel Hope in the LORD (v.3)",
  "Let Israel hope in the LORD from henceforth and for ever. The same turn Psalm 130 makes, and in a psalm of "
  "three verses it is a third of the whole. A private settling of the soul is handed to a nation as a "
  "programme, which is the Ascents' habit: nothing in this collection stays personal for long."),
],
"psalms132": [
 ("Until I Find Out a Place for the LORD (vv.1-5)",
  "LORD, remember David, and all his afflictions. The longest of the Songs of Ascents, and it is a processional "
  "for bringing the ark up to the temple. What is recalled is a vow, and the vow is about sleep, I will not "
  "give sleep to mine eyes, or slumber to mine eyelids, until I find out a place for the LORD. No such oath "
  "appears in Samuel or Kings; the psalm preserves a tradition about David that the histories do not record, "
  "and it stands beside 2 Samuel 7, where David proposes a house and is told he will not build it."),
 ("Arise, O LORD, into Thy Rest (vv.6-9)",
  "Lo, we heard of it at Ephratah: we found it in the fields of the wood. Two place names for the search, "
  "Ephratah being the district of Bethlehem and the fields of the wood most likely Kiriath-jearim, where 1 "
  "Samuel 7 leaves the ark for twenty years. The congregation then speaks as though present at the "
  "procession, we will go into his tabernacles: we will worship at his footstool. Arise, O LORD, into thy "
  "rest; thou, and the ark of thy strength, which is close to the words Numbers 10:35 gives for setting out "
  "with the ark, turned round for arriving. Solomon prays these verses at the dedication in 2 Chronicles "
  "6:41."),
 ("The LORD Hath Sworn in Truth unto David (vv.10-12)",
  "For thy servant David's sake turn not away the face of thine anointed. The prayer is for a later king on "
  "the strength of an earlier one, which is how the psalm was used long after David. The LORD hath sworn in "
  "truth unto David; he will not turn from it; Of the fruit of thy body will I set upon thy throne. Peter "
  "cites this oath at Pentecost in Acts 2:30. Then the condition, and it is stated plainly, if thy children "
  "will keep my covenant and my testimony that I shall teach them, their children shall also sit upon thy "
  "throne for evermore. The promise is unconditional in its swearing and conditional in its inheritance, "
  "which is the tension Psalm 89 makes its whole subject."),
 ("The LORD Hath Chosen Zion (vv.13-18)",
  "For the LORD hath chosen Zion; he hath desired it for his habitation. God answers in his own voice for the "
  "last six verses, and the first thing said is that the choosing was wanted rather than conceded, here will I "
  "dwell; for I have desired it. What follows is a list of blessings that answers the requests of verses 8 to "
  "10 item by item, the priests clothed, the saints shouting, the anointed provided for, with one addition the "
  "prayer did not ask for, I will satisfy her poor with bread. Then two images for the king's future, there "
  "will I make the horn of David to bud, and I have ordained a lamp for mine anointed, both of which Luke "
  "picks up in the first chapter of his Gospel. His enemies will I clothe with shame: but upon himself shall "
  "his crown flourish."),
],
"psalms133": [
 ("How Good and How Pleasant It Is (v.1)",
  "Behold, how good and how pleasant it is for brethren to dwell together in unity. Three verses, and the "
  "first states the subject without arguing for it. Dwelling together had a literal sense for pilgrims sharing "
  "quarters at a feast, and a national sense for tribes that spent much of their history at odds; the psalm "
  "does not choose between them."),
 ("The Precious Ointment upon the Head (v.2)",
  "It is like the precious ointment upon the head, that ran down upon the beard, even Aaron's beard: that went "
  "down to the skirts of his garments. The comparison is the anointing of a high priest, and the whole force "
  "of it is in the running down: the oil is poured at one point and arrives everywhere, so unity is described "
  "as something that starts at the head and reaches the hem. It is an extravagant amount of oil, and the "
  "extravagance is intended."),
 ("As the Dew of Hermon (v.3a)",
  "As the dew of Hermon, and as the dew that descended upon the mountains of Zion. Hermon is in the far north "
  "and Zion is a hundred and twenty miles south, so dew from one does not fall on the other. The "
  "impossibility is the point rather than a mistake: the psalm is claiming that the moisture of the wettest "
  "mountain in the land arrives on the driest hill, which is what unity between distant parties would be."),
 ("There the LORD Commanded the Blessing (v.3b)",
  "For there the LORD commanded the blessing, even life for evermore. The last clause tells the reader where "
  "the two images were heading. There means the place where brethren dwell together, and what is said to be "
  "there is not a good atmosphere but a command already issued. The psalm ends by making unity the address at "
  "which a blessing was left."),
],
"psalms134": [
 ("Which by Night Stand in the House of the LORD (vv.1-2)",
  "Behold, bless ye the LORD, all ye servants of the LORD, which by night stand in the house of the LORD. The "
  "last of the fifteen Songs of Ascents, three verses long, and it is addressed to the men on the night watch "
  "in the temple. After a collection that began in exile among people who hated peace, the pilgrimage ends "
  "inside the building after dark. Lift up your hands in the sanctuary, and bless the LORD."),
 ("Bless Thee out of Zion (v.3)",
  "The LORD that made heaven and earth bless thee out of Zion. The last verse answers the first two: the "
  "servants are told to bless God and the reply blesses them. It is addressed to one person, not the group, "
  "which reads as the priest turning to each pilgrim in turn. And the credential is the one Psalms 121 and 124 "
  "used on the road, so the collection ends with the same maker it started out trusting."),
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
