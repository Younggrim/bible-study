#!/usr/bin/env python3
"""
Ezekiel 33 to 39: the news arrives, the shepherds, the dry bones, and Gog. Seven pages,
197 verses. All seven inherited sublists are folded.

ezekiel36's outline had a gap in it, covering verse 22 and then jumping to verse 25 and
leaving 23 and 24 undescribed. Those two verses carry the motive clause for the most
quoted promise in the book, so the block is written here as one section, verses 22 to 24,
rather than papering over the hole.

The turn in the book happens at 33:21-22. A fugitive reaches Babylonia with the news that
Jerusalem has fallen, and the dumbness imposed at 3:26 ends the evening before he arrives,
so the prophet's mouth was opened before he was told. Everything after it is addressed to
people for whom the worst has already happened, which is why chapters 34 to 39 are the
most hopeful stretch of the book.

Usage:
    python3 fold_ezekiel_restoration.py [--check]
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
KEEP = ("Author:", "Date:", "Classification:", "Key Themes:", "Historical Context:",
        "Notable:")
REPAIRS = {}

SECTIONS = {
"ezekiel33": [
 ("The Watchman Recommissioned (vv.1-9)",
  "The commission of 3:16-21 is given again, at length, and the timing is everything: it is restated "
  "immediately before the news of Jerusalem's fall arrives. The illustration is civic rather than "
  "religious, when I bring the sword upon a land, and the people take one man of their coasts and set "
  "him for their watchman. Two cases follow and they are both about liability. If the watchman sees "
  "the sword and blows not the trumpet, the man who dies dies in his iniquity, but his blood will I "
  "require at the watchman's hand. If he blows and is ignored, he that heareth shall take warning and "
  "the watchman has delivered his soul. What the office controls is whether the warning was given."),
 ("I Have No Pleasure in the Death of the Wicked (vv.10-20)",
  "The section is built around a quotation from the audience, and it is the voice of people who have "
  "given up rather than of people arguing, our transgressions and our sins are upon us, and we pine "
  "away in them, how should we then live. The answer is put under oath, as I live, saith the Lord "
  "GOD, I have no pleasure in the death of the wicked, but that the wicked turn from his way and "
  "live, turn ye, turn ye from your evil ways. Then the cases of chapter 18 in compressed form, "
  "cutting both ways: the righteousness of the righteous shall not deliver him in the day of his "
  "transgression, and the wickedness of the wicked shall not fall on him in the day that he turns. "
  "And the same objection is quoted again, yet ye say, The way of the Lord is not equal."),
 ("The Fugitive Arrives (vv.21-22)",
  "Two verses, and they are the hinge of the book. The twelfth year, tenth month, fifth day, one that "
  "had escaped out of Jerusalem came unto me, saying, The city is smitten. Then a note about timing "
  "that is easy to read past, now the hand of the LORD was upon me in the evening before he that was "
  "escaped came, and had opened my mouth. The dumbness imposed at 3:26 had lasted about seven and a "
  "half years, and it lifted the night before the messenger arrived, so he was able to speak before "
  "he was told what had happened."),
 ("Those Left in the Ruins (vv.23-29)",
  "Attention turns to the people still in Judah, and their claim is quoted as an argument from "
  "arithmetic, Abraham was one, and he inherited the land, but we are many, the land is given us for "
  "inheritance. The reply does not dispute the premise, it disputes their standing to use it, and "
  "lists what they are doing while they say it: ye eat with the blood, and lift up your eyes toward "
  "your idols, and shed blood, and ye stand upon your sword, ye work abomination, and ye defile every "
  "one his neighbour's wife, and shall ye possess the land. Occupancy is not treated as title."),
 ("Hearers Who Treat It as Entertainment (vv.30-33)",
  "Now that the city has actually fallen, the prophet has an audience, and the problem has changed "
  "from hostility to appreciation. The children of thy people still are talking against thee by the "
  "walls and in the doors of the houses, and what they say to one another is an invitation, come, I "
  "pray you, and hear what is the word that cometh forth from the LORD. Then the diagnosis, they hear "
  "thy words, but they do them not, and the image that makes the point better than any accusation "
  "could, thou art unto them as a very lovely song of one that hath a pleasant voice, and can play "
  "well on an instrument. Being enjoyed turns out to be a harder problem than being resisted."),
],
"ezekiel34": [
 ("Woe to the Shepherds Who Feed Themselves (vv.1-6)",
  "Shepherd was the ordinary ancient title for a king, so this is an oracle against Judah's rulers "
  "and everyone hearing it knew that. The charge is stated as a reversal of function, woe be to the "
  "shepherds of Israel that do feed themselves, should not the shepherds feed the flocks. What "
  "follows is a job description read backwards: the diseased ye have not strengthened, neither have "
  "ye healed that which was sick, neither have ye bound up that which was broken, neither have ye "
  "brought again that which was driven away, neither have ye sought that which was lost. And the "
  "manner is named as well as the omissions, but with force and with cruelty have ye ruled them."),
 ("God Against the Shepherds (vv.7-10)",
  "Behold, I am against the shepherds, and I will require my flock at their hand, and cause them to "
  "cease from feeding the flock. The removal is total, neither shall the shepherds feed themselves any "
  "more, and I will deliver my flock from their mouth, that they may not be meat for them. What is "
  "being described is not reform of the office but its confiscation."),
 ("God Himself Will Shepherd (vv.11-16)",
  "I will both search my sheep, and seek them out, and the actions listed are the omissions of verse "
  "4 performed one by one: I will seek that which was lost, and bring again that which was driven "
  "away, and will bind up that which was broken, and will strengthen that which was sick. The "
  "conditions are named too, delivered out of all places where they have been scattered in the cloudy "
  "and dark day, fed upon the mountains of Israel, lying in a good fold. Both Luke 15 and John 10 "
  "draw on this passage directly. The last clause keeps it from being only comfort, but I will "
  "destroy the fat and the strong, I will feed them with judgment."),
 ("Judgment Between Sheep (vv.17-22)",
  "The oppression in this section is not by rulers, which is why it needs its own place: it is by "
  "other members of the flock, and I judge between cattle and cattle. The questions put are about "
  "waste rather than about consumption, is it a small thing unto you to have eaten up the good "
  "pasture, but ye must tread down with your feet the residue of your pastures, and to have drunk of "
  "the deep waters, but ye must foul the residue with your feet. Then the physical picture, ye push "
  "with side and with shoulder, and push all the diseased with your horns, therefore will I save my "
  "flock, and they shall no more be a prey."),
 ("My Servant David, One Shepherd (vv.23-24)",
  "I will set up one shepherd over them, and he shall feed them, even my servant David. David had "
  "been dead about four hundred years when this was said, so the name is being used dynastically, and "
  "the arrangement is stated in two halves that are held together everywhere in this book, and I the "
  "LORD will be their God, and my servant David a prince among them. Jesus takes up the whole chapter "
  "when he calls himself the good shepherd, and the contrast he draws with the hireling is the "
  "contrast this chapter opened with."),
 ("A Covenant of Peace, and Showers of Blessing (vv.25-31)",
  "I will make with them a covenant of peace, and the safety described is concrete rather than "
  "spiritual, the evil beasts caused to cease out of the land, and they shall dwell safely in the "
  "wilderness, and sleep in the woods. The agricultural promise contains a phrase that has passed "
  "into ordinary speech, I will cause the shower to come down in his season, there shall be showers "
  "of blessing. The chapter ends by stating the relationship twice, once from each side, thus shall "
  "they know that I the LORD their God am with them, and that they, even the house of Israel, are my "
  "people, and then in the second person, ye my flock, the flock of my pasture, are men, and I am "
  "your God."),
],
"ezekiel35": [
 ("Against Mount Seir (vv.1-4)",
  "An oracle against Edom sits in the middle of the restoration chapters, and the placement is "
  "deliberate. Chapter 36 is addressed to the mountains of Israel, and this one is addressed to mount "
  "Seir, so the two form a matched pair, one range cursed and the other blessed, with the same "
  "opening formula and opposite outcomes. Behold, O mount Seir, I am against thee, and I will stretch "
  "out mine hand against thee, and I will make thee most desolate."),
 ("Perpetual Hatred, and the Blood Shed at the Calamity (vv.5-9)",
  "Because thou hast had a perpetual hatred, and hast shed the blood of the children of Israel by the "
  "force of the sword in the time of their calamity, in the time that their iniquity had an end. The "
  "charge is opportunism at the exact moment of collapse, which is what Obadiah is entirely about and "
  "what puts the sting into Psalm 137. The sentence answers in kind, I will prepare thee unto blood, "
  "and blood shall pursue thee, sith thou hast not hated blood, therefore blood shall pursue thee."),
 ("The Claim on Two Nations (vv.10-13)",
  "Because thou hast said, These two nations and these two countries shall be mine, and we will "
  "possess it, that is, both Israel and Judah, both now empty. The refutation is four words long and "
  "is attached to the end of the quotation, whereas the LORD was there. The land was not vacant, "
  "whatever it looked like. And the closing charge is about speech, thou shalt know that I am the "
  "LORD, and that I have heard all thy blasphemies which thou hast spoken against the mountains of "
  "Israel."),
 ("Edom's Desolation, and Israel's (vv.14-15)",
  "The sentence is stated as an exact exchange, as thou didst rejoice at the inheritance of the house "
  "of Israel, because it was desolate, so will I do unto thee, thou shalt be desolate, O mount Seir, "
  "and all Idumea, even all of it. Rejoicing over an empty land is answered with an empty land, which "
  "sets up the opening of the next chapter, where the same mountains Edom expected to inherit are "
  "told they will be full of people again."),
],
"ezekiel36": [
 ("To the Mountains of Israel, You Shall Yield Again (vv.1-15)",
  "The address is to terrain, as at 6:2, but with the message reversed: the same mountains that were "
  "told their shrines would be filled with corpses are now told they will be filled with people. The "
  "occasion is again something the neighbours said, because the enemy said, Aha, even the ancient "
  "high places are ours in possession. What is promised is entirely material and is listed as such, I "
  "will multiply men upon you, all the house of Israel, and the cities shall be inhabited, and the "
  "wastes shall be builded, and ye shall yield your fruit to my people Israel. One clause treats the "
  "land as having a reputation of its own to recover, thou shalt no more bereave them of men."),
 ("They Profaned My Name Among the Nations (vv.16-21)",
  "The exile is explained first, they defiled the land, wherefore I poured my fury upon them, and I "
  "scattered them among the heathen. Then the unintended consequence, and it is the problem this "
  "whole chapter is written to solve: when they were come, they profaned my holy name, when they said "
  "to them, These are the people of the LORD, and are gone forth out of his land. A defeated people "
  "is taken as evidence against its God, so the punishment itself became a slander. But I had pity "
  "for mine holy name, which the house of Israel had profaned among the heathen."),
 ("Not for Your Sakes (vv.22-24)",
  "These three verses are the motive clause for what follows, and they are blunt about it, not for "
  "your sakes do I this, O house of Israel, but for mine holy name's sake, which ye have profaned "
  "among the heathen. The restoration is a matter of God's reputation rather than Israel's "
  "improvement, and I will sanctify my great name, and the heathen shall know that I am the LORD, "
  "when I shall be sanctified in you before their eyes. Only then comes the gathering, I will take "
  "you from among the heathen, and gather you out of all countries, and will bring you into your own "
  "land. Any reading of the famous promise in the next section that leaves these verses out has "
  "removed its stated reason."),
 ("Clean Water, a New Heart, a New Spirit (vv.25-27)",
  "Three verses, and they are the fullest form of the promise first made at 11:19. The sequence runs "
  "cleansing, then replacement, then indwelling: then will I sprinkle clean water upon you, and ye "
  "shall be clean, from all your filthiness, and from all your idols, will I cleanse you. A new heart "
  "also will I give you, and a new spirit will I put within you, and I will take away the stony heart "
  "out of your flesh, and I will give you an heart of flesh. And I will put my spirit within you, and "
  "cause you to walk in my statutes. The obedience is produced rather than required, which is the "
  "difference between this and every warning in the first half of the book, and the water and the "
  "spirit together are what Jesus puts to Nicodemus in John 3."),
 ("Land, Crops, Cities, and a Flock of Men (vv.28-38)",
  "The rest of the chapter works the promise out in ordinary things, ye shall dwell in the land that "
  "I gave to your fathers, I will call for the corn, and will increase it, and I will multiply the "
  "fruit of your trees. Two notes keep it from turning into simple prosperity. The response to being "
  "restored is again shame rather than relief, then shall ye remember your own evil ways, and shall "
  "lothe yourselves in your own sight. And the motive clause is repeated so it cannot be mislaid, not "
  "for your sakes do I this, saith the Lord GOD, be it known unto you. The comparison drawn is the "
  "highest available, this land that was desolate is become like the garden of Eden, and the closing "
  "image is of crowds, as the flock of Jerusalem in her solemn feasts, so shall the waste cities be "
  "filled with flocks of men."),
],
"ezekiel37": [
 ("Can These Bones Live (vv.1-3)",
  "The hand of the LORD carried me out in the spirit, and set me down in the midst of the valley "
  "which was full of bones. Two details are given before anything happens, and both are observations "
  "made on foot: he caused me to pass by them round about, so the extent was walked, and there were "
  "very many in the open valley, and lo, they were very dry. Unburied and long dead. Then the "
  "question, Son of man, can these bones live, and the answer, which neither claims nor denies, O "
  "Lord GOD, thou knowest."),
 ("Bone to His Bone (vv.4-8)",
  "The command is to preach to the bones, which is the vision's comment on what preaching is for, and "
  "the reassembly is described in anatomical order, I will lay sinews upon you, and will bring up "
  "flesh upon you, and cover you with skin. The sound comes first, there was a noise, and behold a "
  "shaking, and the bones came together, bone to his bone. Then the section stops one stage short and "
  "says so, but there was no breath in them. Splitting the work into two commands is deliberate: a "
  "restored body is not yet a living one."),
 ("Prophesy unto the Wind (vv.9-10)",
  "The second command is addressed to the wind, come from the four winds, O breath, and breathe upon "
  "these slain, that they may live. The Hebrew word behind wind, breath and spirit in this chapter is "
  "one word, ruach, and the passage uses all three senses of it within two verses, which no "
  "translation can reproduce. The result is military rather than merely biological, and they lived, "
  "and stood up upon their feet, an exceeding great army."),
 ("The Interpretation (vv.11-14)",
  "The vision is explained as an answer to something the exiles were saying, and the quotation is the "
  "key to the whole chapter, they say, Our bones are dried, and our hope is lost, we are cut off for "
  "our parts. It is a response to despair rather than a lesson in doctrine. The promise is put in the "
  "vocabulary of burial, I will open your graves, and cause you to come up out of your graves, and "
  "bring you into the land of Israel, with the same clause as 36:27 attached, and shall put my spirit "
  "in you, and ye shall live. The immediate reference is national, and the language of opened graves "
  "went on to shape later hope of resurrection."),
 ("The Two Sticks Made One (vv.15-23)",
  "A sign-act, and a simple one. Write upon one stick, For Judah, and upon another, For Joseph, the "
  "stick of Ephraim, and join them one to another into one stick, and they shall become one in thine "
  "hand. What is being promised had looked impossible for a very long time: the kingdoms had split in "
  "930 BC and the northern one had ceased to exist in 722, its population dispersed beyond recovery. "
  "They shall be no more two nations, neither shall they be divided into two kingdoms any more at "
  "all, and the cleansing is named as part of it, neither shall they defile themselves any more with "
  "their idols."),
 ("One King, One Shepherd, One Everlasting Covenant (vv.24-28)",
  "The promises of the preceding chapters are gathered into five verses: David my servant shall be "
  "king over them, and they all shall have one shepherd, from chapter 34; a covenant of peace, and an "
  "everlasting covenant; and then the one thing not yet promised, I will set my sanctuary in the "
  "midst of them for evermore, my tabernacle also shall be with them, and I will be their God, and "
  "they shall be my people. Revelation 21:3 quotes that last pair of clauses of the new Jerusalem. "
  "The sanctuary announced here in a sentence is what the last nine chapters of the book then "
  "describe wall by wall."),
],
"ezekiel38": [
 ("Gog, and the Coalition (vv.1-6)",
  "Set thy face against Gog, the land of Magog, the chief prince of Meshech and Tubal, and then the "
  "allies, Persia, Ethiopia, Libya, Gomer, and the house of Togarmah of the north quarters. No Gog "
  "has ever been identified in any record, and the names that can be placed are peoples on the far "
  "rim of the known world in every direction at once, north, south and east. That is generally taken "
  "to be deliberate: the enemy here is not a current political threat with a policy, but everything "
  "outside, gathered. The opening gesture is the same one used on Pharaoh at 29:4, I will put hooks "
  "into thy jaws."),
 ("After Many Days (vv.7-9)",
  "The timing is stated twice and it matters for reading the whole passage, after many days thou shalt "
  "be visited, in the latter years thou shalt come into the land. And the land is described as already "
  "restored, brought back from the sword, gathered out of many people, and they shall dwell safely all "
  "of them. So this invasion comes after the promises of chapters 36 and 37 have been kept, not "
  "before. Thou shalt ascend and come like a storm, thou shalt be like a cloud to cover the land."),
 ("The Thought That Comes into His Heart (vv.10-13)",
  "The motive is quoted as an internal monologue, and what attracts the attack is precisely the peace "
  "just promised: I will go up to the land of unwalled villages, I will go to them that are at rest, "
  "that dwell safely, all of them dwelling without walls, and having neither bars nor gates. The aim "
  "is plunder, to take a spoil, and to take a prey. Then an odd and very human detail, Sheba, and "
  "Dedan, and the merchants of Tarshish stand off and ask, art thou come to take a spoil, hast thou "
  "gathered thy company to take a prey. Trading nations working out whether there is a share in it "
  "for them."),
 ("That the Heathen May Know Me (vv.14-16)",
  "Thou shalt come from thy place out of the north parts, thou, and many people with thee, all of them "
  "riding upon horses, a great company and a mighty army. The purpose given is not military and not "
  "punitive, and it is put in the first person, I will bring thee against my land, that the heathen "
  "may know me, when I shall be sanctified in thee, O Gog, before their eyes. The invasion is "
  "described as being arranged for what it will demonstrate."),
 ("Earthquake, Sword, Pestilence and Fire (vv.17-23)",
  "The battle is not a battle. Israel takes no part in it, and the agents named are geological and "
  "epidemiological: a great shaking in the land of Israel, so that the mountains shall be thrown "
  "down, and the steep places shall fall, and every wall shall fall to the ground. Then every man's "
  "sword shall be against his brother, which is the coalition destroying itself, and I will plead "
  "against him with pestilence and with blood, and I will rain upon him an overflowing rain, and "
  "great hailstones, fire, and brimstone. The section closes on the same purpose the previous one "
  "gave, thus will I magnify myself, and sanctify myself, and I will be known in the eyes of many "
  "nations."),
],
"ezekiel39": [
 ("The Destruction Restated (vv.1-8)",
  "The oracle begins again from the top, which is this book's normal method, and adds figures and "
  "specifics, I will turn thee back, and leave but the sixth part of thee, I will smite thy bow out "
  "of thy left hand, thou shalt fall upon the mountains of Israel. The fire reaches the homeland too, "
  "I will send a fire on Magog. And the purpose is stated a third time with one clause added about "
  "Israel's own conduct, so will I make my holy name known in the midst of my people Israel, and I "
  "will not let them pollute my holy name any more. The section ends with a sentence in the perfect "
  "tense, behold, it is come, and it is done."),
 ("Seven Years of Fuel (vv.9-10)",
  "The aftermath is described domestically, which is what makes it effective. They that dwell in the "
  "cities of Israel shall go forth, and shall burn the weapons, both the shields and the bucklers, "
  "the bows and the arrows, and they shall burn them with fire seven years. The consequence given is "
  "an economic one, so that they shall take no wood out of the field, neither cut down any out of the "
  "forests. An invasion's entire equipment ends as household firewood, and the supply lasts long "
  "enough that nobody needs to go logging."),
 ("Seven Months of Burial, and Hamon-gog (vv.11-16)",
  "The concern in this section is cleanness of the land, which is a priest's concern and explains why "
  "the procedure is set out in such detail. A burial ground is assigned, the valley of the "
  "passengers, renamed the valley of Hamon-gog. Seven months shall the house of Israel be burying of "
  "them, that they may cleanse the land. Then a systematic search, men appointed to pass through the "
  "land, and when any seeth a man's bone, then shall he set up a sign by it, till the buriers have "
  "buried it. Not a mass grave and a moving on, but a survey."),
 ("The Feast for the Birds and Beasts (vv.17-20)",
  "Sacrificial language is used with the army as the victim, and it is one of the grimmest inversions "
  "in the prophets. Speak unto every feathered fowl, and to every beast of the field, gather "
  "yourselves to my sacrifice that I do sacrifice for you, even a great sacrifice upon the mountains "
  "of Israel, that ye may eat flesh, and drink blood. The excess is stated deliberately, ye shall eat "
  "fat till ye be full, and drink blood till ye be drunken, and ye shall be filled at my table. "
  "Revelation 19 takes up the same summons to the birds almost word for word."),
 ("My Glory Among the Nations (vv.21-24)",
  "And I will set my glory among the heathen, and all the heathen shall see my judgment that I have "
  "executed. What these verses do is answer the slander of 36:20, where the exile was taken abroad as "
  "proof that Israel's God had failed. Here the nations are given the correct account of it, and the "
  "heathen shall know that the house of Israel went into captivity for their iniquity, because they "
  "trespassed against me, therefore hid I my face from them. The record is corrected in public."),
 ("Restoration, and the Spirit Poured Out (vv.25-29)",
  "The last five verses of the section return from the far future to the readers in front of the "
  "prophet, now will I bring again the captivity of Jacob, and have mercy upon the whole house of "
  "Israel, and will be jealous for my holy name. The safety promised is described in terms of what "
  "will be absent, they shall dwell safely in their land, and none shall make them afraid. And the "
  "final clause is the reversal of the whole first half of the book, neither will I hide my face any "
  "more from them, for I have poured out my spirit upon the house of Israel. Joel 2 states the same "
  "promise in the same words, and Acts 2 applies it to Pentecost."),
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
                notes.append(f"{page}: dropped inherited item {label!r}, "
                             f"its content is folded into the sections")
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
