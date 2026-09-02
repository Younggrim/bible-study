#!/usr/bin/env python3
"""
Completes Micah: all seven chapters.

Three things needed handling beyond the usual fold.

Spaced verse ranges. Micah's inherited skeletons write "(vv. 1-2)" with a space.
Only 27 pages in the repo do that against 395 using the compact "(vv.1-2)", and the
compact form is what the progress query matches, so the section labels here use
compact. The other 20 spaced pages are Psalms 31 onward and can be normalised when
those are folded.

Emphatic capitals in the inherited headings. micah5 had "the BETHLEHEM PROPHECY"
and micah6 "the ANSWER", both also starting with a lowercase word mid-heading. Both
are rewritten in sentence case, which is the third and fourth capitals fix in these
skeletons after Malachi's and Lamentations'.

A mis-split label on micah4. One field was labelled "This passage (4:" with a body
beginning "1-3) is nearly identical to Isaiah 2:2-4". The label had been cut at the
colon of a chapter-and-verse reference, exactly as mark13's "Mark 13:" was. Its
substance -- the near-identity with Isaiah 2:2-4 and the swords-into-plowshares
image -- is folded into the section covering vv.1-5.

Usage:
    python3 fold_micah.py [--check]
"""
import os
import re
import sys

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")

ITEM = ('                    <div class="auth-item">'
        '<span class="auth-label">{label}</span> {body}</div>')

VERSES = {"micah1": 16, "micah2": 13, "micah3": 12, "micah4": 13,
          "micah5": 15, "micah6": 16, "micah7": 20}

CAPS_OK = {"LORD", "GOD", "YHWH", "OT", "NT", "BC", "AD", "KJV", "ESV", "ASV", "AM"}

KEEP = ["Author:", "Classification:", "Key Themes:", "Historical Context:"]

DROP = {"micah4": ["This passage (4:"]}

SECTIONS = {
"micah1": [
  ("Superscription: The Word to Samaria and Jerusalem (v.1)",
   "The heading dates Micah to Jotham, Ahaz and Hezekiah, roughly 735 to 700 BC, and "
   "names both capitals as its subject. Addressing Samaria and Jerusalem together is "
   "unusual and sets the book's method: the northern kingdom is judged first and the "
   "southern kingdom is meant to be watching."),
  ("The LORD Comes Down: A Theophany (vv.2-5)",
   "The scene is a courtroom on a cosmic scale, with all peoples summoned and God "
   "coming out of his holy temple as witness against them. Mountains melt like wax "
   "under him and valleys cleave. Then the accusation narrows abruptly from the earth "
   "to two cities: for the transgression of Jacob is all this, and the high places of "
   "Judah are named alongside Samaria."),
  ("Judgment on Samaria (vv.6-7)",
   "Samaria will be made a heap of the field and a place for planting vineyards, its "
   "stones poured down into the valley and its foundations uncovered. The sentence is "
   "specific about the idols: the graven images beaten to pieces and the hires burned. "
   "Samaria fell to Assyria in 722 BC, within Micah's lifetime, so this was a "
   "prediction his hearers lived to check."),
  ("The Prophet's Lament, Stripped and Wailing (vv.8-9)",
   "Micah's response to his own message is not satisfaction but mourning. He will wail "
   "and howl, go stripped and naked, and make a wailing like the dragons and a "
   "mourning like the owls. The reason given in v.9 is that the wound has reached "
   "Judah and come to the gate of Jerusalem, so what began as the north's judgment is "
   "now at his own door."),
  ("Wordplay on the Towns of the Lowlands (vv.10-16)",
   "The closing lament runs through the towns of the Judean lowlands, and each name is "
   "played on in Hebrew: tell it not in Gath, roll in the dust at Beth-le-aphrah, "
   "Lachish and Achzib and Mareshah each turned into a pun on their own name. The "
   "effect is largely lost in translation. These were Micah's own neighbours -- he was "
   "from Moresheth in that district, not a court prophet like Isaiah -- which is why "
   "the geography is this precise and the grief this local."),
],
"micah2": [
  ("Woe to Those Who Devise Iniquity in Bed (vv.1-2)",
   "The charge is premeditation: they work evil upon their beds and perform it in the "
   "morning because it is in their power. What they take is fields and houses, and in "
   "Israel's covenant law land was not property to be traded freely but an inheritance "
   "tied to a family in perpetuity. This was the age of estate-building, and the courts "
   "were run by the same class doing the seizing. Isaiah names the identical evil, woe "
   "to them that join house to house and lay field to field."),
  ("I Devise an Evil Against You (vv.3-5)",
   "The sentence answers the crime in its own words: they devised, and now God devises "
   "against this family. What they took by measuring line will be measured out to "
   "someone else, and v.5 says they will have no one to cast a cord in the assembly "
   "-- the very land-allotment procedure they abused is withdrawn from them. The "
   "punishment is the mechanism of the offence turned round."),
  ("Prophesy Not: The Silencing of Micah (vv.6-7)",
   "Verse 6 quotes the audience telling him to stop: prophesy ye not. What they wanted "
   "instead is stated at v.11 -- a man who would prophesy of wine and strong drink "
   "would be accepted as a prophet. The reply asks whether the Spirit of the LORD is "
   "straitened, and whether his words do not do good to him that walks uprightly, "
   "which puts the fault in the hearer rather than the message."),
  ("Stripping the Robe, Casting Out Women and Children (vv.8-11)",
   "The indictment turns to who is being hurt: the robe pulled off men passing by "
   "securely, the women of God's people cast out of their pleasant houses, and the "
   "children stripped of God's glory for ever. The victims named are those with no "
   "legal standing to resist. Verse 10's \u201carise ye, and depart\u201d turns the "
   "eviction back on the evictors, since the land is polluted and will not hold them."),
  ("The Breaker Goes Before Them (vv.12-13)",
   "The chapter ends where nothing in it prepared for: God gathering Jacob, putting "
   "them together as sheep in a fold, and going up before them as the one who breaks "
   "open the way. The abruptness is characteristic of Micah, whose judgment and mercy "
   "sections sit next to each other without transition. The shepherd image answers the "
   "chapter's opening picture of a flock being fleeced by its own leaders."),
],
"micah3": [
  ("Rulers Who Eat the Flesh of My People (vv.1-4)",
   "The guilty are named by office rather than left general: the heads of Jacob and "
   "princes of Israel, whose job was to know judgment. The imagery is cannibalism "
   "-- they pluck off the skin, break the bones, chop them in pieces as for the pot -- "
   "which is as violent as the prophets get about economic exploitation. The sentence "
   "in v.4 is silence: they will cry to the LORD and he will not hear them, because "
   "they have behaved ill in their doings."),
  ("Prophets Who Divine for Money (vv.5-7)",
   "The second class indicted are prophets who bite with their teeth and cry peace, "
   "and who declare war against anyone who does not put something in their mouths. "
   "The message follows the payment. Their punishment fits the trade: night instead of "
   "vision, darkness instead of divination, the sun going down on them, and they shall "
   "cover their lips because there is no answer from God."),
  ("But I Am Full of Power by the Spirit (v.8)",
   "Against the hired prophets Micah sets himself in a single verse: truly I am full "
   "of power by the Spirit of the LORD, and of judgment, and of might, to declare to "
   "Jacob his transgression. The contrast is content rather than sincerity -- what "
   "marks him is willingness to name the sin, which is precisely what the paid "
   "prophets would not do."),
  ("Building Zion with Blood (vv.9-11)",
   "The summary indictment gathers all three classes: heads who judge for reward, "
   "priests who teach for hire, prophets who divine for money. The line that condemns "
   "them is their confidence -- they lean on the LORD and say is not the LORD among "
   "us, none evil can come upon us. The offence is not unbelief but a belief in "
   "protection held while doing all of this."),
  ("Zion Shall Be Plowed as a Field (v.12)",
   "The verdict is one verse and it names the temple: Zion plowed as a field, "
   "Jerusalem become heaps, the mountain of the house as the high places of the "
   "forest. It was remembered. A century later the elders quoted this verse to save "
   "Jeremiah's life in Jeremiah 26:18, recalling that Hezekiah had answered Micah with "
   "repentance rather than execution -- which is the only recorded case of a king "
   "responding to a prophecy this severe by changing course."),
],
"micah4": [
  ("The Mountain of the LORD in the Last Days (vv.1-5)",
   "Placed immediately after Zion plowed as a field, the reversal is deliberate: the "
   "same mountain becomes established above the hills with all nations flowing to it. "
   "This passage is nearly identical to Isaiah 2:2-4, and since the two prophets were "
   "contemporaries the shared text most likely reflects one revelation given to both. "
   "Swords beaten into plowshares and spears into pruninghooks has become the most "
   "widely recognised image in prophetic literature. Verse 4's addition, every man "
   "under his vine and fig tree, makes the peace domestic rather than merely "
   "political."),
  ("The LORD Shall Reign in Zion (vv.6-8)",
   "The gathering is described in terms of who is collected: her that halteth and her "
   "that was driven out, made a remnant and a strong nation. God reigning over them in "
   "mount Zion is stated as from henceforth even for ever. The tower of the flock in "
   "v.8 keeps the shepherd image running, and dominion is said to come to it -- the "
   "first kingdom shall come to the daughter of Jerusalem."),
  ("Why Dost Thou Cry Out? Babylon Foretold (vv.9-10)",
   "The vision drops back to the present without warning: why dost thou cry out aloud, "
   "is there no king in thee? The pangs are those of a woman in travail, and the "
   "destination named is Babylon -- notable because in Micah's day Assyria was the "
   "threat and Babylon was not yet the power that would take Judah. Even here the "
   "sentence carries its own reversal: there shalt thou be delivered, there the LORD "
   "shall redeem thee."),
  ("Many Nations Gathered, and a Threshing (vv.11-13)",
   "The nations assemble expecting to see Zion defiled and to feast their eyes on her, "
   "and the chapter says they do not know the thoughts of the LORD, who has gathered "
   "them as sheaves to the floor. The daughter of Zion is then told to thresh, with "
   "horn of iron and hoofs of brass. The gain is to be devoted to the LORD rather than "
   "kept, which distinguishes this from ordinary conquest."),
],
"micah5": [
  ("The Judge Smitten on the Cheek (v.1)",
   "The chapter opens in humiliation, not glory: troops gathered against her, and the "
   "judge of Israel struck with a rod upon the cheek. A blow to the face was a public "
   "insult rather than a battlefield wound, so the picture is of leadership disgraced "
   "before it is replaced. Everything that follows is set against this verse."),
  ("Bethlehem Ephratah: The Ruler from Everlasting (v.2)",
   "The most consequential verse in the book, and it turns on smallness -- Bethlehem "
   "is called little among the thousands of Judah, a village rather than a centre. "
   "Ephratah distinguishes it from the other Bethlehem in Zebulun. The claim in the "
   "second half is what makes the verse extraordinary: the one who comes forth to be "
   "ruler has goings forth from of old, from everlasting. Written some seven centuries "
   "before the event, it is the passage the chief priests quote to Herod in Matthew 2 "
   "without needing to look it up."),
  ("Given Up Until She Travails (v.3)",
   "Between the promise and its fulfilment the verse places an interval: therefore "
   "will he give them up, until the time that she which travaileth hath brought forth. "
   "The abandonment is real and bounded, and the birth is what ends it. The remnant of "
   "his brethren returning to the children of Israel closes the verse, so the birth "
   "gathers rather than merely arrives."),
  ("He Shall Stand and Feed, and He Shall Be Peace (vv.4-6)",
   "The ruler's work is described in shepherd terms: he shall stand and feed in the "
   "strength of the LORD, and they shall abide, for now shall he be great unto the ends "
   "of the earth. Then the flat statement of v.5, this man shall be the peace -- not "
   "bring peace but be it. What follows about the Assyrian and the seven shepherds "
   "keeps the promise attached to the actual threat of Micah's own century rather than "
   "floating free of it."),
  ("Dew and Lion, and the Purging of False Securities (vv.7-15)",
   "The remnant is given two images at once: dew from the LORD that waits for no man, "
   "and a lion among the flocks of sheep. Refreshment and danger in the same paragraph. "
   "The chapter closes with God cutting off what Israel had relied on -- horses, "
   "chariots, cities, strongholds, witchcrafts, graven images, groves -- so the list "
   "of things removed is a list of substitutes. Purification here means having "
   "alternatives taken away."),
],
"micah6": [
  ("The LORD's Case: Hear, O Mountains (vv.1-2)",
   "The chapter takes the form of a covenant lawsuit, and the mountains and the strong "
   "foundations of the earth are summoned as witnesses. Calling on cosmic witnesses to "
   "a treaty violation was standard practice in ancient Near Eastern agreements, so "
   "the form would have been recognised at once. God is both plaintiff and the one "
   "with a controversy with his people."),
  ("What Have I Done to Thee? The Saving Acts Rehearsed (vv.3-5)",
   "The opening question is not an accusation but an invitation: O my people, what have "
   "I done unto thee, and wherein have I wearied thee? testify against me. Then the "
   "evidence for the prosecution turns out to be a list of kindnesses -- brought up out "
   "of Egypt, redeemed from the house of servants, sent Moses, Aaron and Miriam, and "
   "what happened with Balak and Balaam. Against that record the unfaithfulness has no "
   "explanation left."),
  ("Shall I Come with Burnt Offerings? (vv.6-7)",
   "The people's reply escalates absurdly: burnt offerings, calves of a year old, then "
   "thousands of rams, then ten thousand rivers of oil, then a firstborn child. Each "
   "bid raises the price on the assumption that quantity is the problem. The last "
   "offer, my firstborn for my transgression, was something the surrounding nations "
   "actually did and Israel was expressly forbidden, so the question has gone badly "
   "wrong before it is answered."),
  ("He Hath Shewed Thee What Is Good (v.8)",
   "The answer is one verse and it asks for less rather than more: do justly, love "
   "mercy, and walk humbly with thy God. The middle term is hesed, covenant loyalty, "
   "so it is love owed rather than felt. Nothing in the list is a ritual, which is the "
   "point after two verses of escalating sacrifice -- what was already shown to them "
   "did not need buying."),
  ("Wicked Balances, and the Futility Curses (vv.9-16)",
   "The specifics return to commerce: the scant measure, the wicked balances, the bag "
   "of deceitful weights. Then a series of curses shaped as futility -- eat and not be "
   "satisfied, sow and not reap, tread olives and not anoint, make wine and not drink. "
   "Effort without result, which is the covenant sanction of Deuteronomy 28. The "
   "chapter ends by naming the statutes of Omri and the works of Ahab's house, so "
   "Judah is being told it has adopted the north's playbook."),
],
"micah7": [
  ("Woe Is Me: No Upright Man Remains (vv.1-6)",
   "The prophet compares himself to someone gleaning after the harvest and finding no "
   "cluster to eat. What he cannot find is a good man: the best of them is as a brier, "
   "the prince asks for a bribe, the judge is for reward. Then the breakdown reaches "
   "the household -- trust no friend, put no confidence in a guide, the son dishonours "
   "the father, a man's enemies are the men of his own house. Jesus quotes v.6 in "
   "Matthew 10 when describing what following him will cost."),
  ("Therefore I Will Look unto the LORD (v.7)",
   "The turn of the whole book, and it is a decision rather than a change of "
   "circumstances: therefore I will look unto the LORD, I will wait for the God of my "
   "salvation, my God will hear me. Nothing in vv.1-6 has improved. The word "
   "\u201ctherefore\u201d reasons from the collapse to the looking, which is the "
   "opposite of what it should do."),
  ("Rejoice Not Against Me, O Mine Enemy (vv.8-10)",
   "The voice becomes the city's, addressing a gloating enemy: when I fall, I shall "
   "arise; when I sit in darkness, the LORD shall be a light unto me. The confession "
   "in v.9 is unusual in that it accepts the sentence as deserved -- I will bear the "
   "indignation of the LORD, because I have sinned against him -- while still "
   "expecting vindication. Both at once, rather than one instead of the other."),
  ("The Day for Building Thy Walls (vv.11-13)",
   "A short passage on reversal of scale: the day for building the walls, the decree "
   "far removed, and people coming from Assyria, Egypt, the river and the sea. "
   "Boundaries that had shut Judah in are described as widening. Verse 13 keeps it "
   "honest by leaving the land desolate in the meantime, for the fruit of their "
   "doings, so the promise does not cancel the judgment already pronounced."),
  ("Feed Thy People with Thy Rod (vv.14-17)",
   "A prayer rather than an oracle: feed thy people with thy rod, the flock of thine "
   "heritage. The request is for shepherding in Bashan and Gilead as in the days of "
   "old, and the answer promises marvels as in the day of coming out of Egypt. The "
   "nations are described licking the dust and coming with fear, which is the counter "
   "to the enemy gloating in v.8."),
  ("Who Is a God Like unto Thee? (vv.18-20)",
   "The book ends in a question that is also a pun. Micah's own name means who is like "
   "the LORD, so the closing doxology plays on it -- his identity and his last words "
   "are the same claim. What follows is the reason: a God who pardons iniquity, does "
   "not retain his anger for ever, delights in mercy, subdues iniquities and casts all "
   "their sins into the depths of the sea. A book that opened with mountains melting "
   "closes with sins sunk out of reach."),
],
}

CAPS = re.compile(r"\b[A-Z]{2,}\b")


def main():
    check = "--check" in sys.argv
    problems, notes, planned = [], [], {}

    for page in sorted(VERSES):
        path = os.path.join(DOCS, f"{page}.html")
        html = open(path, encoding="utf-8").read()
        pane = re.search(r'(id="tab-authorship">)(.*?)(?=<div class="tab-content")',
                         html, re.S)
        if not pane:
            problems.append(f"{page}: no authorship pane")
            continue

        want_drop = DROP.get(page, [])
        fields, dropped, extra = {}, [], []
        for m in re.finditer(r'<div class="auth-item">(.*?)</div>', pane.group(2), re.S):
            inner = m.group(1)
            lab = re.match(r'<span class="auth-label">([^<]*)</span>\s*', inner)
            name = lab.group(1).strip() if lab else None
            rest = inner[lab.end():].strip() if lab else inner.strip()
            if name in KEEP:
                fields[name] = rest
            elif name is not None and name in want_drop:
                dropped.append(name)
            elif name is None and rest == "Structure:":
                pass
            elif name is None:
                extra.append(rest)
            else:
                problems.append(f"{page}: unexpected field {name!r}")

        for want in KEEP:
            if want not in fields:
                problems.append(f"{page}: missing {want}")
        for want in want_drop:
            if want not in dropped:
                problems.append(f"{page}: expected to drop {want!r}, not found")
        if extra:
            fields["Historical Context:"] = " ".join(
                [fields["Historical Context:"]] + extra).strip()
            notes.append(f"{page}: {len(extra)} headless paragraph(s) merged into "
                         f"Historical Context")
        if dropped:
            notes.append(f"{page}: mis-split label {dropped[0]!r} folded into "
                         f"section prose")

        sections = SECTIONS[page]
        covered = set()
        for label, body in [(f"section {h!r}", p) for h, p in sections]:
            stray = sorted({w for w in CAPS.findall(body) if w not in CAPS_OK})
            if stray:
                problems.append(f"{page}: emphatic capitals {stray} in {label}")
            if "*" in body:
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
