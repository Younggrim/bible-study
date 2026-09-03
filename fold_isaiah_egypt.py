#!/usr/bin/env python3
"""
Isaiah 29 to 33: Ariel, the Egyptian alliance, and the king in his beauty. Five pages,
110 verses.

Four of the five outlines fold as they stand. isaiah33's does not: it opened with a woe
covering verses 1 to 4 and then a prayer covering verses 2 to 6, so verses 2, 3 and 4
were described twice. The woe is given verse 1, which is where it actually sits, and the
prayer takes verses 2 to 6, which is where the second person plural begins.

These five chapters are the most political in the book. The subject running under all of
them is a single policy question: whether Judah should buy Egyptian help against Assyria.
Isaiah's answer is at 30:15, in returning and rest shall ye be saved, in quietness and in
confidence shall be your strength, and the verse ends with the government's reply, and ye
would not.

Usage:
    python3 fold_isaiah_egypt.py [--check]
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
"isaiah29": [
 ("Woe to Ariel (vv.1-4)",
  "Woe to Ariel, to Ariel, the city where David dwelt. The name is used of Jerusalem and it means either "
  "lion of God or, more likely here, altar hearth, since verse 2 puts the two senses together, and it "
  "shall be unto me as Ariel, that is, the city becomes the place where things are burned. The siege is "
  "described as an encampment, I will camp against thee round about, and will lay siege against thee "
  "with a mount. And the voice of the city afterwards is put underground, thy voice shall be as of one "
  "that hath a familiar spirit, out of the ground, and thy speech shall whisper out of the dust."),
 ("Enemies Vanish Like a Dream (vv.5-8)",
  "And the multitude of thy terrible ones shall be as chaff that passeth away, yea, it shall be at an "
  "instant suddenly. The deliverance is described twice by the same figure and the figure is the "
  "interesting part: it shall be as when a hungry man dreameth, and behold, he eateth, but he awaketh, "
  "and his soul is empty. The besieging army is compared to a man who dreams of a meal and wakes still "
  "hungry, so the whole campaign is described as an appetite that never gets satisfied. Given what "
  "happens to Sennacherib's army in chapter 37, this reads as a description of that night."),
 ("A Sealed Book (vv.9-12)",
  "For the LORD hath poured out upon you the spirit of deep sleep, and hath closed your eyes. Then the "
  "chapter's best image for a failure of understanding, and it comes in two halves so that no excuse is "
  "left standing. The book is handed to a man who can read and it is sealed, and he says, I cannot, for "
  "it is sealed. Then it is handed to a man who cannot read and he says, I am not learned. Literacy and "
  "illiteracy fail in the same way, which locates the problem somewhere other than in the ability to "
  "read."),
 ("This People Draw Near with Their Mouth (vv.13-14)",
  "Wherefore the Lord said, Forasmuch as this people draw near me with their mouth, and with their lips "
  "do honour me, but have removed their heart far from me, and their fear toward me is taught by the "
  "precept of men. Jesus quotes this verse against the Pharisees in Matthew 15 and Mark 7, and the "
  "phrase taught by the precept of men is the part he presses. And the consequence is aimed at the "
  "professionally clever, therefore the wisdom of their wise men shall perish, which Paul quotes in "
  "1 Corinthians 1."),
 ("Woe to Those Who Hide Their Counsel (vv.15-16)",
  "Woe unto them that seek deep to hide their counsel from the LORD, and their works are in the dark, "
  "and they say, Who seeth us. What is being described is the secret diplomacy of the Egyptian "
  "negotiations, conducted without consulting the prophets. The reply is the potter figure Jeremiah 18 "
  "and Romans 9 also use, and here it is put as an absurdity rather than a doctrine, shall the work say "
  "of him that made it, He made me not, or shall the thing framed say of him that framed it, He had no "
  "understanding."),
 ("The Deaf Shall Hear (vv.17-24)",
  "Is it not yet a very little while, and Lebanon shall be turned into a fruitful field. Then the "
  "reversal of the sealed book and the closed eyes of verses 9 to 12, and in that day shall the deaf "
  "hear the words of the book, and the eyes of the blind shall see out of obscurity. The beneficiaries "
  "are named and they are not the wise men, the meek also shall increase their joy, and the poor among "
  "men shall rejoice in the Holy One of Israel. And what is removed is legal rather than military, the "
  "terrible one is brought to nought, and they that make a man an offender for a word, and turn aside "
  "the just for a thing of nought. Corrupt courts, ended by name."),
],
"isaiah30": [
 ("Woe to the Rebellious Children (vv.1-7)",
  "Woe to the rebellious children, that take counsel, but not of me, and that cover with a covering, but "
  "not of my spirit. The policy is named in the next line, that walk to go down into Egypt, and have not "
  "asked at my mouth. What is objected to is not the diplomacy but the sequence: the treaty was "
  "negotiated and then, at most, prayed about. Then a note about the paperwork, in that they trust in "
  "the shadow of Egypt, and the caravan is described going south through dangerous country with its "
  "cargo, their riches upon the shoulders of young asses, through the land of trouble and anguish, from "
  "whence come the young and old lion, the viper and fiery flying serpent. And Egypt is given a name "
  "for the occasion, and it is the most dismissive in the book, therefore have I cried concerning this, "
  "Their strength is to sit still."),
 ("Write It in a Book (vv.8-14)",
  "Now go, write it before them in a table, and note it in a book, that it may be for the time to come "
  "for ever and ever. The instruction is archival: the refusal is to be documented so that it can be "
  "produced later. Then what they had asked for is quoted, and it is a request for editorial control, "
  "prophesy not unto us right things, speak unto us smooth things, prophesy deceits. And the sentence "
  "is delivered as two pieces of masonry and pottery, this iniquity shall be to you as a breach ready to "
  "fall, swelling out in a high wall, whose breaking cometh suddenly at an instant, and he shall break "
  "it as the breaking of the potters' vessel that is broken in pieces, he shall not spare."),
 ("In Returning and Rest (v.15)",
  "One verse, and it is the alternative to the whole policy stated in six words. For thus saith the Lord "
  "GOD, the Holy One of Israel, In returning and rest shall ye be saved, in quietness and in confidence "
  "shall be your strength. Four nouns, all of them passive, offered to a government drafting a military "
  "treaty. And the verse ends with the answer it received, which is why it stands alone here, and ye "
  "would not."),
 ("Ye Shall Flee (vv.16-17)",
  "But ye said, No, we will flee upon horses, therefore shall ye flee. The judgment is the policy carried "
  "to its conclusion: they wanted cavalry and they will use it to run away. Then the arithmetic of the "
  "rout, one thousand shall flee at the rebuke of one, at the rebuke of five shall ye flee, which is the "
  "exact inversion of the promise in Deuteronomy 32:30 that one should chase a thousand."),
 ("Therefore Will the LORD Wait (v.18)",
  "One verse, and it turns the chapter without warning. And therefore will the LORD wait, that he may be "
  "gracious unto you, and therefore will he be exalted, that he may have mercy upon you. The waiting of "
  "18:4 reappears here with a stated purpose. And the closing line names who benefits, blessed are all "
  "they that wait for him, so both parties in the verse are waiting."),
 ("Thine Ears Shall Hear a Voice Behind Thee (vv.19-22)",
  "He will be very gracious unto thee at the voice of thy cry, when he shall hear it, he will answer "
  "thee. The bread of adversity and the water of affliction are not withdrawn; what changes is the "
  "presence of a teacher, and thine eyes shall see thy teachers. Then the sentence the section is best "
  "known for, and thine ears shall hear a word behind thee, saying, This is the way, walk ye in it, when "
  "ye turn to the right hand, and when ye turn to the left. Guidance from behind rather than in front, "
  "which means it arrives after the wrong turn has begun. And the response is disposal, ye shall defile "
  "the covering of thy graven images, thou shalt cast them away as a menstruous cloth."),
 ("Rain, Bread, and Broad Pastures (vv.23-26)",
  "Then shall he give the rain of thy seed, that thou sowest the ground withal, and bread of the "
  "increase of the earth. The prosperity described is agricultural and specific, the oxen and the young "
  "asses eating clean provender, and rivers of waters in the day of the great slaughter. And the closing "
  "verse turns the sky up rather than out, moreover the light of the moon shall be as the light of the "
  "sun, and the light of the sun shall be sevenfold, which is the reverse of the darkened luminaries of "
  "13:10."),
 ("Tophet Prepared for the King (vv.27-33)",
  "Behold, the name of the LORD cometh from far, burning with his anger, and his tongue as a devouring "
  "fire. Then a striking pairing: the same night that destroys the Assyrian army is described as a "
  "festival for Judah, ye shall have a song, as in the night when a holy solemnity is kept, and gladness "
  "of heart, as when one goeth with a pipe to come into the mountain of the LORD. Music and slaughter in "
  "the same sentence. And the chapter ends at Tophet, the burning ground in the valley of Hinnom that "
  "Jeremiah 7 and 19 spend so long on, prepared here for a king, for Tophet is ordained of old, yea, for "
  "the king it is prepared. The place where Judah's children had been burned is made ready for the "
  "emperor."),
],
"isaiah31": [
 ("Woe to Them That Go Down to Egypt (vv.1-3)",
  "Woe to them that go down to Egypt for help, and stay on horses, and trust in chariots because they "
  "are many, and in horsemen because they are very strong, but they look not unto the Holy One of "
  "Israel. Then a line that answers the assumption that this is naive, yet he also is wise, and will "
  "bring evil, and will not call back his words, which claims competence for the position the "
  "government has dismissed as unrealistic. And the argument closes on a physiological fact rather than "
  "a theological one, now the Egyptians are men, and not God, their horses flesh, and not spirit. The "
  "objection to the alliance is that the ally is mortal."),
 ("As a Lion, and as Birds Flying (vv.4-5)",
  "Two similes in two verses and they pull in opposite directions, which is the point. Like as the lion "
  "and the young lion roaring on his prey, when a multitude of shepherds is called forth against him, he "
  "will not be afraid of their voice, so shall the LORD of hosts come down to fight for mount Zion. Then "
  "immediately, as birds flying, so will the LORD of hosts defend Jerusalem, defending also he will "
  "deliver it, and passing over he will preserve it. A lion standing over a carcass and a bird hovering "
  "over a nest, offered together as the same protection. And the word rendered passing over is the "
  "Passover verb."),
 ("Turn Ye unto Him (vv.6-7)",
  "Turn ye unto him from whom the children of Israel have deeply revolted. What that turning looks like "
  "in practice is stated as disposal rather than as feeling, for in that day every man shall cast away "
  "his idols of silver, and his idols of gold, which your own hands have made unto you for a sin. The "
  "phrase which your own hands have made is doing the same work here as at 17:8: the disqualifying fact "
  "about the object is who manufactured it."),
 ("A Sword Not of Man (vv.8-9)",
  "Then shall the Assyrian fall with the sword, not of man, and the sword, not of man, shall devour him. "
  "The repetition is deliberate and it settles the argument of the whole chapter: if the enemy is not "
  "beaten by soldiers then Egyptian cavalry was never the relevant question. The rout is described from "
  "the officers down, and his princes shall be afraid of the ensign. And the last verse names where God "
  "keeps his equipment, whose fire is in Zion, and his furnace in Jerusalem, which is the Ariel of 29:1 "
  "read the other way round."),
],
"isaiah32": [
 ("A King Shall Reign in Righteousness (vv.1-2)",
  "Behold, a king shall reign in righteousness, and princes shall rule in judgment. What follows is the "
  "definition of what such a government is for, and every image in it is about shelter, and a man shall "
  "be as an hiding place from the wind, and a covert from the tempest, as rivers of water in a dry "
  "place, as the shadow of a great rock in a weary land. Three of the four are things that make a "
  "difference in a hot, dry country to a person out in the open. Good government described as shade."),
 ("The Vile Person Shall No More Be Called Liberal (vv.3-8)",
  "And the eyes of them that see shall not be dim, and the ears of them that hear shall hearken, which "
  "reverses 6:10 and 29:10. Then the chapter's real subject, which is vocabulary. The vile person shall "
  "no more be called liberal, nor the churl said to be bountiful, that is, flattering titles will stop "
  "matching the wrong people. And the definitions are then given plainly, for the vile person will speak "
  "villany, and his heart will work iniquity, to make empty the soul of the hungry. Against him, the "
  "liberal soul deviseth liberal things. It is the same concern as 5:20, where evil was called good, "
  "answered here by the words going back onto the right men."),
 ("Ye Careless Women (vv.9-14)",
  "Rise up, ye women that are at ease, hear my voice, ye careless daughters. The word is at ease rather "
  "than wicked, and the charge in this section is complacency rather than crime, which is why the "
  "audience is chosen as it is. Then a timetable, yet in a year shall ye be troubled, and what is lost "
  "is stated in agricultural terms, the vintage shall fail, the gathering shall not come. And the city "
  "is described afterwards as pasture, because the palaces shall be forsaken, the multitude of the city "
  "shall be left, and the forts and towers shall be for dens for ever, a joy of wild asses, a pasture of "
  "flocks."),
 ("Until the Spirit Be Poured (vv.15-20)",
  "Until the spirit be poured upon us from on high, and the wilderness be a fruitful field, and the "
  "fruitful field be counted for a forest. The word until is the hinge of the chapter: the desolation of "
  "the previous section has a terminus. Then the result stated as a chain, and the work is done by "
  "righteousness rather than by prosperity, and the work of righteousness shall be peace, and the effect "
  "of righteousness quietness and assurance for ever. And the closing picture is ordinary and domestic, "
  "my people shall dwell in a peaceable habitation, and in quiet resting places, with the cattle turned "
  "loose to graze anywhere, blessed are ye that sow beside all waters, that send forth thither the feet "
  "of the ox and the ass."),
],
"isaiah33": [
 ("Woe to Thee That Spoilest (v.1)",
  "Woe to thee that spoilest, and thou wast not spoiled, and dealest treacherously, and they dealt not "
  "treacherously with thee. One verse, and it is addressed to a power that has broken faith without "
  "having been wronged first, which is what Assyria did to Hezekiah after the tribute of 2 Kings 18 was "
  "paid. The sentence is stated as a turn-taking, when thou shalt cease to spoil, thou shalt be spoiled, "
  "and when thou shalt make an end to deal treacherously, they shall deal treacherously with thee."),
 ("O LORD, Be Gracious unto Us (vv.2-6)",
  "The oracle becomes a prayer in the first person plural, O LORD, be gracious unto us, we have waited "
  "for thee, be thou their arm every morning, our salvation also in the time of trouble. Then the enemy "
  "dispersing and the spoil being collected in a picture drawn from insects, as the running to and fro "
  "of locusts shall he run upon them. And the section ends on a list of what the LORD supplies, and it "
  "is arranged as a treasury, wisdom and knowledge, the stability of thy times, and the fear of the LORD "
  "is his treasure. Stability listed as an asset, which for a small state under siege is exactly what it "
  "was."),
 ("The Highways Lie Waste (vv.7-9)",
  "Behold, their valiant ones shall cry without, the ambassadors of peace shall weep bitterly. The "
  "diplomats are weeping because the diplomacy has failed, and the failure is described as a breach of "
  "agreement, he hath broken the covenant, he hath despised the cities, he regardeth no man. Then the "
  "effect on ordinary movement, which is the most concrete measure of a country under occupation, the "
  "highways lie waste, the wayfaring man ceaseth. And the land is named region by region, Lebanon, "
  "Sharon, Bashan and Carmel, all of them proverbial for fertility and all of them listed as failing."),
 ("Now Will I Rise (vv.10-13)",
  "Now will I rise, saith the LORD, now will I be exalted. The enemy's effort is dismissed as producing "
  "nothing usable, ye shall conceive chaff, ye shall bring forth stubble. Then the fire, and the people "
  "shall be as the burnings of lime, as thorns cut up shall they be burned in the fire, which is "
  "material that burns fast and leaves nothing. And the audience is widened at the end, hear, ye that "
  "are far off, what I have done, and ye that are near, behold my might."),
 ("Who Shall Dwell with Everlasting Burnings (vv.14-16)",
  "The sinners in Zion are afraid, fearfulness hath surprised the hypocrites, and they ask the question "
  "the section turns on, who among us shall dwell with the devouring fire, who among us shall dwell with "
  "everlasting burnings. The answer is unusual in this book for being a list of ordinary conduct rather "
  "than of belief: he that walketh righteously, and speaketh uprightly, he that despiseth the gain of "
  "oppressions, that shaketh his hands from holding of bribes, that stoppeth his ears from hearing of "
  "blood, and shutteth his eyes from seeing evil. Four of the six are things a person declines to do. "
  "And the promise attached is domestic, bread shall be given him, his waters shall be sure."),
 ("The King in His Beauty (vv.17-24)",
  "Thine eyes shall see the king in his beauty, they shall behold the land that is very far off. Then a "
  "backward glance at the occupation which is one of the sharpest things in the book, thine heart shall "
  "meditate terror, where is the scribe, where is the receiver, where is he that counted the towers. The "
  "men remembered from the worst years are the tax assessors and the surveyors, not the soldiers. And "
  "the language is named as the thing that made them frightening, thou shalt not see a fierce people, of "
  "a stammering tongue, that thou canst not understand. The city is then described as permanent "
  "camping, a tabernacle that shall not be taken down, not one of the stakes thereof shall ever be "
  "removed. And the last verse settles two things at once, and the inhabitant shall not say, I am sick, "
  "for the people that dwell therein shall be forgiven."),
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
