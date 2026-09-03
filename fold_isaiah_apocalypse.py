#!/usr/bin/env python3
"""
Isaiah 24 to 28: the earth oracle, the feast on the mountain, and the cornerstone. Five
pages, 98 verses. All five outlines are gapless and are folded.

Chapters 24 to 27 are often called the Isaiah apocalypse, and the label is worth
qualifying: the horizon is the whole earth rather than a named nation, but the imagery
stays agricultural and civic rather than becoming visionary in the manner of Daniel or
Revelation. What makes the block unusual in the Old Testament is 25:8 and 26:19, which
are the two clearest statements of resurrection outside Daniel 12.

isaiah28 contains the passage Paul and Peter both quote as the cornerstone, and it also
contains the strangest piece of mimicry in the prophets, at 28:10, where the prophet is
mocked in baby talk and answers by saying the same syllables will come back in a foreign
accent.

Usage:
    python3 fold_isaiah_apocalypse.py [--check]
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
KEEP = ("Author:", "Date:", "Classification:", "Key Themes:", "Historical Context:")
REPAIRS = {}

SECTIONS = {
"isaiah24": [
 ("The Earth Made Empty (vv.1-3)",
  "Behold, the LORD maketh the earth empty, and maketh it waste, and turneth it upside down. What "
  "follows is a levelling stated as a list of pairs, and the point of the list is that no social "
  "position exempts anyone: as with the people, so with the priest, as with the servant, so with his "
  "master, as with the maid, so with her mistress, as with the buyer, so with the seller, as with the "
  "lender, so with the borrower. Six relationships, each of them a difference in standing, and each of "
  "them cancelled."),
 ("The Broken Everlasting Covenant (vv.4-6)",
  "The earth mourneth and fadeth away, the world languisheth and fadeth away, the haughty people of the "
  "earth do languish. Then the cause, and it is stated in three clauses that escalate, because they have "
  "transgressed the laws, changed the ordinance, broken the everlasting covenant. That last phrase is "
  "the interesting one. The covenant named is not Sinai, which was with Israel, but something older and "
  "wider, and the usual reading takes it as the covenant with Noah in Genesis 9, which was made with "
  "all flesh. A charge against the whole earth requires a covenant the whole earth was party to."),
 ("The Joy Is Gone (vv.7-13)",
  "The new wine is dried up, the oil faileth, and what is mourned is measured in sounds that have "
  "stopped, the mirth of tabrets ceaseth, the noise of them that rejoice endeth, the joy of the harp "
  "ceaseth. They shall not drink wine with a song. Then the city, and the detail is architectural, in "
  "the city is left desolation, and the gate is smitten with destruction. And the section closes with "
  "the same gleaning image as 17:6, there shall be as the shaking of an olive tree, and as the gleaning "
  "grapes when the vintage is done, which is this book's standing picture of a remnant: a counted few in "
  "the branches nobody could reach."),
 ("A Remnant Sings, and the Prophet Does Not (vv.14-16a)",
  "They shall lift up their voice, they shall sing for the majesty of the LORD, they shall cry aloud "
  "from the sea. The singing comes from the far edges rather than from the centre, glorify ye the LORD "
  "in the fires, even the name of the LORD God of Israel in the isles of the sea. From the uttermost "
  "part of the earth have we heard songs. The section stops in the middle of verse 16 because the "
  "sentence turns there, and what it turns to is the prophet's own reaction, which is not singing."),
 ("My Leanness, and the Cosmic Collapse (vv.16b-20)",
  "But I said, My leanness, my leanness, woe unto me. The songs of the previous section are still "
  "audible and the prophet is wasting away in the middle of them, which is the same structure as "
  "21:3-4. Then the terror is set out as a trap with three stages nobody escapes, he who fleeth from the "
  "noise of the fear shall fall into the pit, and he that cometh up out of the midst of the pit shall be "
  "taken in the snare, the same figure Jeremiah 48:44 uses of Moab. And the earth is described as drunk "
  "and as a temporary structure, the earth shall reel to and fro like a drunkard, and shall be removed "
  "like a cottage."),
 ("The LORD Shall Reign in Mount Zion (vv.21-23)",
  "And it shall come to pass in that day, that the LORD shall punish the host of the high ones that are "
  "on high, and the kings of the earth upon the earth. Two tiers are named, and the higher one is not "
  "explained; the phrase the host of the high ones is left as it stands. Then a detention with a "
  "duration attached, they shall be gathered together as prisoners are gathered in the pit, and after "
  "many days shall they be visited. And the chapter ends with the sun and moon embarrassed rather than "
  "extinguished, then the moon shall be confounded, and the sun ashamed, for the LORD of hosts shall "
  "reign in mount Zion, and before his ancients gloriously."),
],
"isaiah25": [
 ("O LORD, Thou Art My God (vv.1-5)",
  "The oracle stops and becomes a psalm, O LORD, thou art my God, I will exalt thee, I will praise thy "
  "name. What is praised is planning rather than power, for thou hast done wonderful things, thy "
  "counsels of old are faithfulness and truth. Then the reason given, and it is put in terms of who "
  "benefits, for thou hast been a strength to the poor, a strength to the needy in his distress, a "
  "refuge from the storm, a shadow from the heat. And the image the section closes on is a working one "
  "from that climate, the blast of the terrible ones is as the heat in a dry place, and heat is brought "
  "down with the shadow of a cloud."),
 ("The Feast on the Mountain (vv.6-8)",
  "And in this mountain shall the LORD of hosts make unto all people a feast of fat things, a feast of "
  "wines on the lees, of fat things full of marrow, of wines on the lees well refined. The guest list is "
  "the striking part, all people, in a book that has spent twelve chapters on the failings of the "
  "nations. Then the covering removed, and he will destroy the face of the covering cast over all "
  "people, and the vail that is spread over all nations. And then verse 8, which is one of the two "
  "clearest resurrection statements in the Old Testament outside Daniel: he will swallow up death in "
  "victory, and the Lord GOD will wipe away tears from off all faces. Paul quotes it in 1 Corinthians 15 "
  "and Revelation 21 takes up the wiping away of tears."),
 ("This Is Our God, We Have Waited for Him (v.9)",
  "One verse, and it is what the people say at the feast rather than what is said to them. And it shall "
  "be said in that day, Lo, this is our God, we have waited for him, and he will save us, this is the "
  "LORD, we have waited for him, we will be glad and rejoice in his salvation. The verb waited appears "
  "twice in one sentence, which is the whole content of it: the response to the arrival is a claim about "
  "how long they had expected it."),
 ("Moab Trodden Down (vv.10-12)",
  "The chapter does not end on the feast. And Moab shall be trodden down under him, even as straw is "
  "trodden down for the dunghill, and he shall spread forth his hands in the midst of them, as he that "
  "swimmeth spreadeth forth his hands to swim. A man flailing in a midden is a deliberately undignified "
  "picture, and it is placed three verses after a banquet for all people. The two sit side by side "
  "without being reconciled, which is characteristic of this book, and the fortifications are the last "
  "thing named, the fortress of the high fort of thy walls shall he bring down."),
],
"isaiah26": [
 ("We Have a Strong City (vv.1-4)",
  "In that day shall this song be sung in the land of Judah, We have a strong city, salvation will God "
  "appoint for walls and bulwarks. The defences named are not masonry, which is the point in a book so "
  "concerned with fortification. Then the gates opened for a specific category, open ye the gates, that "
  "the righteous nation which keepeth the truth may enter in. And the two verses the chapter is best "
  "known for, thou wilt keep him in perfect peace, whose mind is stayed on thee, and trust ye in the "
  "LORD for ever, for in the LORD JEHOVAH is everlasting strength. The Hebrew behind perfect peace is "
  "shalom shalom, the word said twice, which is the same emphatic doubling as at 6:3."),
 ("The Lofty City Laid Low (vv.5-6)",
  "For he bringeth down the high, the lofty city he layeth low, he layeth it low, even to the ground, he "
  "bringeth it even to the dust. Two verses set against the strong city of the previous section, so the "
  "chapter puts two cities beside each other and the difference between them is what their walls are "
  "made of. And who does the treading is named, the foot shall tread it down, even the feet of the poor, "
  "and the steps of the needy."),
 ("The Way of the Just Is Uprightness (vv.7-9)",
  "The way of the just is uprightness, thou most upright, dost weigh the path of the just. Then the "
  "posture of waiting, which is this chapter's recurring subject, yea, in the way of thy judgments, O "
  "LORD, have we waited for thee. And a line about when the waiting happens, with my soul have I desired "
  "thee in the night, yea, with my spirit within me will I seek thee early. The reason given for wanting "
  "the judgments is instructional rather than vengeful, for when thy judgments are in the earth, the "
  "inhabitants of the world will learn righteousness."),
 ("The Wicked Learn Nothing from Grace (v.10)",
  "One verse, and it is the hardest sentence in the chapter. Let favour be shewed to the wicked, yet "
  "will he not learn righteousness, in the land of uprightness will he deal unjustly, and will not "
  "behold the majesty of the LORD. It is placed immediately after the claim that judgments teach "
  "righteousness, and it says that kindness does not. The two verses together are the chapter's account "
  "of why the judgments in it are necessary."),
 ("Thou Wilt Ordain Peace for Us (vv.11-15)",
  "LORD, when thy hand is lifted up, they will not see. Then a request and a confession in the same "
  "sentence, LORD, thou wilt ordain peace for us, for thou also hast wrought all our works in us. The "
  "confession about other rulers is unusually candid, O LORD our God, other lords beside thee have had "
  "dominion over us, but by thee only will we make mention of thy name. And the dead of those regimes "
  "are dismissed in a clause that will matter eight verses later, they are dead, they shall not live, "
  "they are deceased, they shall not rise."),
 ("We Have Not Wrought Any Deliverance (vv.16-18)",
  "LORD, in trouble have they visited thee, they poured out a prayer when thy chastening was upon them. "
  "Then an image of effort that produces nothing, and it is the most honest thing in the chapter, we "
  "have been in pain, we have as it were brought forth wind, we have not wrought any deliverance in the "
  "earth. Labour with no birth at the end of it. A nation that prayed under pressure and admits it "
  "achieved nothing."),
 ("Thy Dead Men Shall Live (v.19)",
  "One verse, and it reverses the clause at verse 14 word for word. There the dead of the foreign lords "
  "shall not live and shall not rise; here, thy dead men shall live, together with my dead body shall "
  "they arise, awake and sing, ye that dwell in dust. The imagery is horticultural, for thy dew is as "
  "the dew of herbs, and the earth shall cast out the dead. With 25:8 this is the clearest resurrection "
  "statement in the Old Testament outside Daniel 12, and the fact that it answers verse 14 so exactly is "
  "why it belongs in its own section."),
 ("Hide Thyself Until the Indignation Be Past (vv.20-21)",
  "Come, my people, enter thou into thy chambers, and shut thy doors about thee, hide thyself as it were "
  "for a little moment, until the indignation be overpast. The instruction is domestic and temporary and "
  "it recalls the Passover night in Exodus 12, when the households stayed indoors while something passed "
  "over. And the reason follows, for behold, the LORD cometh out of his place to punish the inhabitants "
  "of the earth for their iniquity, and the earth shall disclose her blood, and shall no more cover her "
  "slain. Ground that has absorbed murder is described as giving it back up."),
],
"isaiah27": [
 ("Leviathan (v.1)",
  "In that day the LORD with his sore and great and strong sword shall punish leviathan the piercing "
  "serpent, even leviathan that crooked serpent, and he shall slay the dragon that is in the sea. "
  "Leviathan appears in Job 41, Psalm 74 and Psalm 104, and the Canaanite texts recovered at Ugarit have "
  "a seven-headed sea monster of a closely related name, which is how the imagery would have been heard "
  "at the time. What the verse does with it is put a sword through it in a single sentence. The monster "
  "of the surrounding mythologies gets one verse and no contest."),
 ("A Vineyard, Kept Night and Day (vv.2-6)",
  "In that day sing ye unto her, A vineyard of red wine. This is chapter 5's vineyard revisited and the "
  "difference is the management: I the LORD do keep it, I will water it every moment, lest any hurt it, "
  "I will keep it night and day. Where the first vineyard's hedge was taken away, this one is watched "
  "continuously. Then an offer made to the briers themselves, the thorns that had overgrown the first "
  "vineyard, let him take hold of my strength, that he may make peace with me. And the outcome is "
  "commercial rather than merely pastoral, Israel shall blossom and bud, and fill the face of the world "
  "with fruit."),
 ("Measured Discipline (vv.7-11)",
  "Hath he smitten him, as he smote those that smote him. The question is about proportion, and the "
  "answer given is that the discipline was measured, in measure, when it shooteth forth, thou wilt debate "
  "with it, he stayeth it with his rough wind. Then the purpose stated as a transaction, by this therefore "
  "shall the iniquity of Jacob be purged, and this is all the fruit, to take away his sin, and what it "
  "costs is named specifically, the altar stones broken as chalkstones and the groves and images "
  "removed. The section ends bleakly though, with a city left to livestock and a people described as "
  "without understanding, therefore he that made them will not have mercy on them."),
 ("The Great Trumpet (vv.12-13)",
  "And it shall come to pass in that day, that the LORD shall beat off from the channel of the river "
  "unto the stream of Egypt, and ye shall be gathered one by one, O ye children of Israel. The verb is "
  "the one used for beating an olive tree, so the gathering is described as harvesting and the phrase one "
  "by one means it is done individually rather than in a mass. Then the trumpet, and the great trumpet "
  "shall be blown, and they shall come which were ready to perish in the land of Assyria, and the "
  "outcasts in the land of Egypt, and shall worship the LORD in the holy mount at Jerusalem. Both "
  "directions of exile, north and south, brought back to one place."),
],
"isaiah28": [
 ("The Fading Crown of Ephraim (vv.1-6)",
  "Woe to the crown of pride, to the drunkards of Ephraim, whose glorious beauty is a fading flower, "
  "which are on the head of the fat valleys. Samaria sat on a hill above a fertile valley, so the crown "
  "is a piece of topography as well as an insult. The city is described as a garland on the head of men "
  "already drunk, and what happens to it is stated in one image, it shall be as the hasty fruit before "
  "the summer, which the eater seeth, and while it is yet in his hand he eateth it up. Then the contrast "
  "held over for the remnant, in that day shall the LORD of hosts be for a crown of glory, and for a "
  "diadem of beauty, unto the residue of his people."),
 ("They Err in Vision (vv.7-13)",
  "But they also have erred through wine, and the list of who is included is what makes this section "
  "sting, the priest and the prophet have erred through strong drink, they err in vision, they stumble "
  "in judgment. Then the mockery, and this is the strangest passage in the prophets: the prophet is "
  "quoted being jeered at in what sounds like baby talk, precept upon precept, line upon line, here a "
  "little, and there a little, which in Hebrew is a string of repeated syllables, tsav latsav, qav "
  "laqav. They are imitating him as though he were teaching toddlers. And his answer takes the same "
  "syllables and gives them back, for with stammering lips and another tongue will he speak to this "
  "people. If they will not hear plain Hebrew they will hear Assyrian, which is the same sound and not "
  "a joke. Paul quotes this passage in 1 Corinthians 14 about tongues."),
 ("The Covenant with Death (vv.14-15)",
  "Hear the word of the LORD, ye scornful men, that rule this people which is in Jerusalem, and the "
  "charge is quoted in their own words, we have made a covenant with death, and with hell are we at "
  "agreement. What is being described is almost certainly a treaty, since the surrounding chapters are "
  "about the Egyptian alliance, and the rest of their sentence gives away what they think of it, we have "
  "made lies our refuge, and under falsehood have we hid ourselves. They know the arrangement is a "
  "fiction and are relying on it anyway."),
 ("The Tried Stone in Zion (v.16)",
  "One verse, and it is the answer to the previous one: against a refuge of lies, a foundation. "
  "Therefore thus saith the Lord GOD, Behold, I lay in Zion for a foundation a stone, a tried stone, a "
  "precious corner stone, a sure foundation, he that believeth shall not make haste. The last clause "
  "means shall not panic, which is exactly the fault of the men who signed the treaty. Paul quotes the "
  "verse in Romans 9 and 10 and Peter in 1 Peter 2, both applying it to Christ, and both keeping the "
  "contrast with haste."),
 ("The Refuge of Lies Swept Away (vv.17-22)",
  "Judgment also will I lay to the line, and righteousness to the plummet, so the builder's tools of the "
  "previous verse are turned into instruments of inspection. Then the treaty fails in its own terms, "
  "your covenant with death shall be disannulled, and your agreement with hell shall not stand. The "
  "image of a bed too short is the most domestic in the chapter, for the bed is shorter than that a man "
  "can stretch himself on it, and the covering narrower than that he can wrap himself in it, which is "
  "inadequate provision rather than active harm. And the closing note is about God's own reluctance, "
  "that he may do his work, his strange work, and bring to pass his act, his strange act."),
 ("The Farmer's Methods (vv.23-29)",
  "The chapter ends with a parable drawn from agriculture, and its subject is the fitting of method to "
  "material. Doth the plowman plow all day to sow, doth he not cast in the fitches, and scatter the "
  "cummin. Then the threshing, and the detail is technical: the fitches are not threshed with a "
  "threshing instrument, nor is the cummin bruised with a wheel, but the bread corn takes the cart wheel "
  "and the horsemen. Different crops take different force, and nobody grinds a delicate seed under a "
  "cart. Applied to the chapter above it, this says that the varying severity of what God does is "
  "expertise rather than inconsistency, and the closing line credits it as such, this also cometh forth "
  "from the LORD of hosts, who is wonderful in counsel, and excellent in working."),
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
