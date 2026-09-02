#!/usr/bin/env python3
"""
Completes Song of Solomon: all eight chapters.

These are the eight pages flagged in WORKFLOW.md as carrying non-outline sublists,
and the flag was right for a reason better than the one recorded. Their lists are
not structural outlines at all -- they are speaker attributions:

    The Bride (Shulamite): vv.2-7, 12-14, 16
    The Bridegroom (Solomon): vv.8-11, 15
    The Daughters of Jerusalem: v.4 (partial), v.11

For this book that is the most useful information on the page. The Song switches
voice without any marker in the text, and readers lose the thread constantly. A
naive fold would have deleted it on all eight chapters.

It is not replaceable by the sections either. The attributions carry half-verse
precision -- v.13a against v.13b in chapter 6, vv.9b-13 in chapter 7 -- and note
where one speaker is being quoted inside another's speech. Sections work at
whole-verse granularity and cannot express that. So the list becomes a "Speakers:"
field rather than being folded into prose, which is the Joshua 12 lesson applied:
verse references in a list do not make it redundant with the sections.

Sections then run in verse order and name the speaker for each block, so the pages
gain the exposition without losing the map.

A finding worth recording rather than acting on. The Author field on these pages
ends with "Key themes:" followed by book-level themes, and it is identical on all
eight chapters. 386 pages repo-wide do this, 123 of them already folded. It is not
duplication: the embedded themes are book-level while a separate Key Themes field
is chapter-specific, and 151 pages already carry both scopes coherently. Splitting
it out would mean inventing a "Book Themes:" label across a third of the site, which
is a decision to take deliberately rather than as a side effect of this batch.
Author is therefore preserved verbatim here.

Usage:
    python3 fold_songofsolomon.py [--check]
"""
import os
import re
import sys

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")

ITEM = ('                    <div class="auth-item">'
        '<span class="auth-label">{label}</span> {body}</div>')

VERSES = {"songofsolomon1": 17, "songofsolomon2": 17, "songofsolomon3": 11,
          "songofsolomon4": 16, "songofsolomon5": 16, "songofsolomon6": 13,
          "songofsolomon7": 13, "songofsolomon8": 14}

CAPS_OK = {"LORD", "GOD", "YHWH", "OT", "NT", "BC", "AD", "KJV", "ESV", "ASV",
           "AM", "II"}

KEEP = ["Author:", "Historical Context:"]

GENRE = "Wisdom Literature \u2014 Love Poetry"

THEMES = {
"songofsolomon1":
  "A working woman rather than a princess, longing stated before the beloved appears, "
  "self-consciousness about her sun-darkened skin, and admiration that begins at once "
  "and runs both ways",
"songofsolomon2":
  "Spring as the reason to come away, a banner of love over the banqueting house, a "
  "beloved compared to a gazelle on the mountains, and small foxes named as the threat "
  "to a vineyard in bloom",
"songofsolomon3":
  "A search through the streets at night, the watchmen met on the way, a charge laid "
  "on the daughters of Jerusalem, and a royal procession out of the wilderness",
"songofsolomon4":
  "Praise catalogued feature by feature in the manner of a wasf, an unqualified \u201cno "
  "spot in thee\u201d, a garden described as enclosed and a fountain as sealed, and an "
  "invitation that answers the praise",
"songofsolomon5":
  "A knock at the door answered too late, a search that ends in being struck by the "
  "watchmen, a question from the daughters that invites the answer, and a description "
  "of the beloved from head to feet",
"songofsolomon6":
  "A question about where the beloved has gone, beauty called terrible as an army with "
  "banners, one singled out from sixty queens, and a return to the garden and the nut "
  "trees",
"songofsolomon7":
  "Praise running from feet upward, the reverse of chapter 4, a stature likened to a "
  "palm tree, mutual belonging stated plainly, and an invitation out to the vineyards "
  "and villages",
"songofsolomon8":
  "A wish for affection that need not hide, love declared strong as death and jealousy "
  "cruel as the grave, a price that cannot be paid, a younger sister to be guarded, and "
  "a closing call to make haste",
}

SECTIONS = {
"songofsolomon1": [
  ("The Song of Songs (v.1)",
   "The title is a Hebrew superlative, the song of songs in the way that holy of "
   "holies means the holiest place. Solomon is credited with 1,005 songs at 1 Kings "
   "4:32, and this is presented as the best of them. Nothing else in the verse "
   "prepares a reader for what follows, and the book never mentions God by name."),
  ("The Bride: Draw Me, We Will Run After Thee (vv.2-4)",
   "The Song opens mid-desire, with no introduction and no scene set: let him kiss me "
   "with the kisses of his mouth. The shift between \u201che\u201d and \u201cthou\u201d "
   "within two verses is characteristic and untidy in the way real speech is. "
   "\u201cDraw me, we will run after thee\u201d moves from singular to plural, "
   "bringing the daughters of Jerusalem in as a chorus."),
  ("The Bride: I Am Black, but Comely (vv.5-7)",
   "She addresses her appearance directly and without apology: dark from working in "
   "the vineyards because her mother's children were angry with her, so she kept "
   "vineyards rather than herself. This is a labourer, not a court beauty, which "
   "matters for how the book's praise later lands. Verse 7 asks where he feeds his "
   "flock, so she is looking for him and unwilling to wander among the other "
   "shepherds' companies."),
  ("The Bridegroom: As a Company of Horses (vv.8-11)",
   "His first speech compares her to a company of horses in Pharaoh's chariots, which "
   "sounds odd until one knows that Egyptian chariot horses were the most admired "
   "animals in the region and elaborately ornamented. The compliment is about bearing "
   "rather than size. He then promises jewellery, borders of gold with studs of "
   "silver, spoken in the plural as though by attendants."),
  ("The Bride: A Bundle of Myrrh (vv.12-14)",
   "Three short images in her own voice, all of them scent rather than sight: "
   "spikenard, a bundle of myrrh lying all night between her breasts, a cluster of "
   "camphire from the vineyards of En-gedi. En-gedi is a real oasis by the Dead Sea, "
   "which anchors the poetry in a place someone could walk to."),
  ("Mutual Praise: Our Bed Is Green (vv.15-17)",
   "The chapter ends in exchange rather than monologue: he calls her fair and her "
   "eyes doves, she calls him fair and pleasant. Then \u201cour bed is green\u201d and "
   "the beams of the house are cedar and the rafters fir, so the setting moves outdoors "
   "into a wood. The alternation of voices established here governs the whole book."),
],
"songofsolomon2": [
  ("The Rose of Sharon and the Lily (vv.1-3)",
   "She calls herself the rose of Sharon and the lily of the valleys, and the point is "
   "modesty rather than grandeur -- these are common wildflowers of the coastal plain. "
   "He answers by turning it into distinction: as the lily among thorns, so is my love "
   "among the daughters. Her reply matches it with the apple tree among the trees of "
   "the wood, so the compliments are being traded in the same currency."),
  ("The Bride: His Banner Over Me Was Love (vv.4-7)",
   "The banqueting house and the banner are military images used domestically: a "
   "standard is what an army rallies to, and here it is love. Verse 5's request to be "
   "stayed with flagons and comforted with apples is the language of someone "
   "overwhelmed rather than merely pleased. Verse 7 is the first of three charges to "
   "the daughters of Jerusalem not to stir up love before it pleases, a refrain that "
   "acts as the book's brake."),
  ("The Bridegroom Comes Leaping (vv.8-9)",
   "She hears him before she sees him -- the voice of my beloved, he cometh leaping "
   "upon the mountains, skipping upon the hills. The comparison to a roe or young hart "
   "is speed and lightness. Then the detail that makes it a scene rather than a "
   "description: he stands behind the wall, looking in at the windows, showing himself "
   "through the lattice."),
  ("Rise Up, My Love: The Winter Is Past (vv.10-14)",
   "The longest speech of his so far, and she quotes it rather than reporting it. The "
   "argument is seasonal: the winter is past, the rain over, the flowers appear, the "
   "turtledove is heard, the fig puts forth green figs. Spring is offered as the reason "
   "to come away, which is as close as the book comes to giving a motive for anything. "
   "The clefts of the rock and the secret places of the stairs suggest she is not yet "
   "out."),
  ("Take Us the Little Foxes (vv.15-17)",
   "The chapter turns abruptly to pests: take us the foxes, the little foxes that spoil "
   "the vines, for our vines have tender grapes. Small damage at a vulnerable stage, "
   "and the line has been read as everything from a folk song fragment to a warning "
   "about minor faults in a new relationship. Verse 16's \u201cmy beloved is mine, and "
   "I am his\u201d is the book's most quoted statement of mutual possession, and it "
   "recurs in variations at 6:3 and 7:10."),
],
"songofsolomon3": [
  ("By Night on My Bed I Sought Him (vv.1-3)",
   "A search told in the past tense and possibly a dream, since it begins on her bed "
   "and moves through the city without transition. I sought him, but I found him not "
   "is repeated, which is the point -- the book does not consist only of fulfilment. "
   "The watchmen who find her in v.3 are asked a question they do not answer, and in "
   "chapter 5 the same watchmen will do worse."),
  ("I Found Him: Charge to the Daughters (vv.4-5)",
   "The finding is brief and the holding is emphatic: I held him, and would not let him "
   "go, until I had brought him into my mother's house. Bringing him to her mother's "
   "chamber rather than a private place puts the relationship in a family setting. Then "
   "the refrain again, the charge not to stir up love until it pleases, which arrives "
   "here directly after a scene of urgency."),
  ("Who Is This Coming Out of the Wilderness? (vv.6-8)",
   "The voice changes to an onlooker and the scale changes with it: a pillar of smoke "
   "perfumed with myrrh and frankincense, and Solomon's bed with threescore valiant men "
   "about it, every man with his sword, because of fear in the night. The armed escort "
   "is a wedding procession detail, and the mention of fear keeps the splendour from "
   "being weightless."),
  ("King Solomon's Chariot (vv.9-11)",
   "The chariot or palanquin is described by materials: cedar of Lebanon, pillars of "
   "silver, bottom of gold, covering of purple, the midst paved with love. That last "
   "phrase breaks the inventory deliberately. The chapter closes with the daughters of "
   "Zion called out to see him crowned by his mother on the day of his espousals, so a "
   "wedding is being staged rather than merely felt."),
],
"songofsolomon4": [
  ("The Bridegroom: Thou Art Fair, My Love (vv.1-5)",
   "This is a wasf, a descriptive poem praising the beloved's body in order, and the "
   "images are pastoral rather than delicate: hair like a flock of goats, teeth like "
   "shorn sheep every one bearing twins, temples like a piece of pomegranate, neck like "
   "the tower of David. To modern ears these read strangely; they are drawn from a "
   "world where a matched flock and a defensible tower were the finest things anyone "
   "owned."),
  ("Until the Day Break: No Spot in Thee (vv.6-7)",
   "The list pauses for a line about going to the mountain of myrrh until the day break "
   "and the shadows flee away, an image already used at 2:17. Then the summary that the "
   "whole chapter exists for: thou art all fair, my love, there is no spot in thee. It "
   "is unqualified, which is rare in any love poetry, and Ephesians 5:27 uses the same "
   "idea of the church presented without spot."),
  ("Come with Me from Lebanon (vv.8-11)",
   "The invitation names dangerous country -- Amana, Shenir, Hermon, the lions' dens "
   "and mountains of the leopards -- and asks her to look away from it and come. The "
   "praise that follows shifts from sight to the other senses: honey and milk under the "
   "tongue, the smell of her garments like Lebanon. \u201cThou hast ravished my "
   "heart\u201d in v.9 is a single Hebrew verb that means something closer to made my "
   "heart beat faster."),
  ("A Garden Enclosed, a Fountain Sealed (vv.12-15)",
   "The imagery turns horticultural and the sense is exclusivity: a garden enclosed, a "
   "spring shut up, a fountain sealed. Enclosure here is value rather than restriction "
   "-- the plants named inside are all expensive imports, spikenard, saffron, calamus, "
   "cinnamon, frankincense, myrrh and aloes. The fountain becomes a well of living "
   "waters and streams from Lebanon, so what is sealed is not stagnant."),
  ("The Bride: Let My Beloved Come (v.16)",
   "One verse, and it answers the garden by opening it. She calls the north and south "
   "winds to blow upon it so the spices flow out, and then invites him in: let my "
   "beloved come into his garden. The possessive changes hands within the same sentence, "
   "from her garden to his, which is the chapter's argument completed in a phrase."),
],
"songofsolomon5": [
  ("The Bridegroom: I Am Come into My Garden (v.1)",
   "He answers the invitation directly and in the perfect tense, gathering myrrh, "
   "honeycomb, wine and milk. The verse ends with a third voice telling friends to eat "
   "and drink abundantly, which reads like a wedding blessing spoken over the couple. "
   "It is the high point of the book, and it is one verse long."),
  ("The Bride: I Sleep, but My Heart Waketh (vv.2-6)",
   "The reversal is immediate and unexplained. He knocks and asks to be let in, his "
   "head filled with dew, and her answer is a series of small excuses -- she has put "
   "off her coat, she has washed her feet. By the time she rises and opens, he is gone. "
   "Whether this is a dream is left open, as in chapter 3, and either way the book "
   "records a failure of response rather than of love."),
  ("The Watchmen Found Me (vv.7-8)",
   "The watchmen who merely met her in chapter 3 now smite her and wound her and take "
   "away her veil. Nothing explains it. She turns to the daughters of Jerusalem with a "
   "charge that inverts the earlier refrain -- not do not stir up love, but if you find "
   "my beloved, tell him that I am sick of love."),
  ("The Daughters Ask: What Is Thy Beloved? (v.9)",
   "A single question from the chorus, and it functions as a prompt: what is thy "
   "beloved more than another beloved, that thou dost so charge us? The structure of "
   "the book depends on these interruptions. Being asked to justify her attachment is "
   "what produces the description that fills the rest of the chapter."),
  ("The Bride: My Beloved Is White and Ruddy (vv.10-16)",
   "Her answer is a wasf of her own, the mirror of chapter 4, and the only extended "
   "praise of a man's body in Scripture. It runs head to feet -- hair bushy and black "
   "as a raven, eyes as doves by the rivers of waters, hands as rings of gold, legs as "
   "pillars of marble -- and the materials are architectural, gold and marble and "
   "ivory, as though describing a statue. The closing line is plainer than any of it: "
   "this is my beloved, and this is my friend."),
],
"songofsolomon6": [
  ("Whither Is Thy Beloved Gone? (vv.1-3)",
   "The daughters offer to help look, which is the first cooperative note from the "
   "chorus. Her answer says she already knows where he is -- gone down into his garden "
   "-- so the search of chapter 5 has resolved offstage. Verse 3 repeats the mutual "
   "possession formula from 2:16 with the halves reversed, which is the kind of small "
   "variation the book uses instead of narrative."),
  ("The Bridegroom: Terrible as an Army with Banners (vv.4-9)",
   "He compares her to Tirzah and Jerusalem, two cities, and then twice to an army with "
   "banners -- beauty described as something that overpowers rather than charms. "
   "\u201cTurn away thine eyes from me, for they have overcome me\u201d is the most "
   "direct statement of that in the book. Verse 8's threescore queens and fourscore "
   "concubines set up v.9: my dove, my undefiled, is but one."),
  ("Who Is She That Looketh Forth? (v.10)",
   "A single verse of question, and the images climb: fair as the moon, clear as the "
   "sun, terrible as an army with banners. Coming from the onlookers rather than the "
   "bridegroom, it functions as public confirmation of what he has just said "
   "privately."),
  ("The Bride: I Went Down into the Garden (vv.11-13)",
   "Her closing lines are hard to follow and the versification differs between "
   "translations, which is why the speaker attributions matter here. She goes down "
   "among the nut trees, and something about her soul making her like the chariots of "
   "a willing people is one of the most disputed sentences in the book. Verse 13's "
   "call to return, Shulamite, gives her the only name she is given anywhere."),
],
"songofsolomon7": [
  ("How Beautiful Are Thy Feet with Shoes (vv.1-5)",
   "A third wasf, and this one runs upward from the feet, the reverse of chapter 4's "
   "direction. The images are again drawn from landscape and architecture: a neck as a "
   "tower of ivory, eyes as the fishpools of Heshbon, a nose as the tower of Lebanon, "
   "hair as purple. Calling her a prince's daughter in v.1 is notable for a woman who "
   "introduced herself in chapter 1 as a vineyard labourer."),
  ("This Thy Stature Is Like a Palm Tree (vv.6-9)",
   "The palm tree image is stated and then acted on -- I will go up to the palm tree, "
   "I will take hold of the boughs -- which is the most physically direct passage in "
   "the book. The date palm was valued for its fruit and its height, so the comparison "
   "carries both. Her voice takes over mid-verse at v.9, which is the kind of overlap "
   "the speaker attributions are needed for."),
  ("I Am My Beloved's, and His Desire Is Toward Me (vv.10-11)",
   "The third and final version of the possession formula, and this one adds something "
   "the earlier two did not: his desire is toward me. Where 2:16 and 6:3 stated mutual "
   "belonging, this states mutual wanting. Her invitation follows immediately -- come, "
   "let us go forth into the field."),
  ("Let Us Get Up Early to the Vineyards (vv.12-13)",
   "The closing lines move the relationship outdoors and into ordinary work: rising "
   "early to see whether the vine flourishes and the pomegranates bud. The mandrakes "
   "give a smell, and at the gates are all manner of pleasant fruits, laid up for him. "
   "After three chapters of elaborate praise the book ends this section in a garden "
   "that needs tending."),
],
"songofsolomon8": [
  ("O That Thou Wert as My Brother (vv.1-4)",
   "The wish is social rather than romantic: that she could kiss him in public without "
   "being despised, which a sister could do and a lover could not. It is the only place "
   "the book acknowledges the constraint it has been working around. The refrain to the "
   "daughters appears for the third and last time, and after it the charge is never "
   "repeated."),
  ("Who Is This That Cometh Up? (v.5)",
   "The onlookers' question returns from 3:6, now with the answer walking in view: "
   "leaning upon her beloved, coming up from the wilderness. The second half of the "
   "verse switches speaker again to mention being raised under an apple tree, tying "
   "back to 2:3. This is the kind of half-verse change of voice that a structural "
   "outline cannot record."),
  ("Love Is Strong as Death (vv.6-7)",
   "The theological centre of the book, and the only place it states a thesis: set me "
   "as a seal upon thine heart, for love is strong as death, jealousy cruel as the "
   "grave, the coals thereof a most vehement flame. Then the economics -- many waters "
   "cannot quench it, and if a man gave all the substance of his house for love it "
   "would be utterly contemned. Love is described as unpurchasable and unextinguishable "
   "in the same breath."),
  ("We Have a Little Sister (vv.8-10)",
   "The brothers speak, and their concern is protective and slightly mercantile: what "
   "shall we do for our sister when she is spoken for, shall we build upon her a palace "
   "of silver or enclose her with boards of cedar. Her answer in v.10 claims her own "
   "maturity -- I am a wall, and my breasts like towers -- and states that she found "
   "favour. The exchange gives the book its only glimpse of family negotiation."),
  ("Solomon's Vineyard, and Mine (vv.11-12)",
   "Solomon had a vineyard let out to keepers for a thousand pieces of silver, and she "
   "answers that her vineyard is before her -- her own to give. Read against 1:6, where "
   "her brothers made her keep the vineyards and she could not keep her own, this is "
   "the book quietly resolving something it raised in its opening lines."),
  ("Make Haste, My Beloved (vv.13-14)",
   "The Song ends where it began, in wanting rather than having: he asks to hear her "
   "voice, and she tells him to make haste and be like a roe upon the mountains of "
   "spices -- the same image as 2:17. Nothing is concluded, which appears to be "
   "deliberate. A book about desire ends with the desire still open."),
],
}

CAPS = re.compile(r"\b[A-Z]{2,}\b")


def main():
    check = "--check" in sys.argv
    problems, notes, planned = [], [], {}

    for page in sorted(VERSES, key=lambda s: int(s[13:])):
        path = os.path.join(DOCS, f"{page}.html")
        html = open(path, encoding="utf-8").read()
        pane = re.search(r'(id="tab-authorship">)(.*?)(?=<div class="tab-content")',
                         html, re.S)
        if not pane:
            problems.append(f"{page}: no authorship pane")
            continue
        body = pane.group(2)

        fields, saw_heading = {}, False
        for m in re.finditer(r'<div class="auth-item">(.*?)</div>', body, re.S):
            inner = m.group(1)
            lab = re.match(r'<span class="auth-label">([^<]*)</span>\s*', inner)
            name = lab.group(1).strip() if lab else None
            rest = inner[lab.end():].strip() if lab else inner.strip()
            if name in KEEP:
                fields[name] = rest
            elif name is None and rest == "Speakers:":
                saw_heading = True
            else:
                problems.append(f"{page}: unexpected item {(name or rest)[:40]!r}")

        for want in KEEP:
            if want not in fields:
                problems.append(f"{page}: missing {want}")
        if not saw_heading:
            problems.append(f"{page}: no 'Speakers:' heading found")

        items = [" ".join(x.split())
                 for x in re.findall(r"<li>(.*?)</li>", body, re.S)]
        if not items:
            problems.append(f"{page}: no speaker attributions to preserve")
            continue
        speakers = "; ".join(items)
        notes.append(f"{page}: {len(items)} speaker attribution(s) kept as a field")

        sections = SECTIONS[page]
        covered = set()
        for label, text in [("Key Themes", THEMES[page]), ("Speakers", speakers)] + \
                           [(f"section {h!r}", p) for h, p in sections]:
            stray = sorted({w for w in CAPS.findall(text) if w not in CAPS_OK})
            if stray:
                problems.append(f"{page}: capitals {stray} in {label}")
            if "*" in text:
                problems.append(f"{page}: markdown asterisk in {label}")
        for head, _ in sections:
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
        parts.append(ITEM.format(label="Author:", body=fields["Author:"]) + "\n")
        parts.append(ITEM.format(label="Classification:", body=GENRE) + "\n")
        parts.append(ITEM.format(label="Key Themes:", body=THEMES[page]) + "\n")
        parts.append(ITEM.format(label="Speakers:", body=speakers) + "\n")
        parts.append(ITEM.format(label="Historical Context:",
                                 body=fields["Historical Context:"]) + "\n")
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
