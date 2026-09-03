#!/usr/bin/env python3
"""
Isaiah 34 to 39: Edom, the highway of holiness, and the Hezekiah narrative. Six pages,
117 verses. All six outlines are gapless and are folded.

Chapters 36 to 39 are prose narrative in a book that is otherwise almost entirely poetry,
and they run parallel to 2 Kings 18 to 20 closely enough that one is drawn from the other
or both from a common source. Two differences are worth noting and the sections note them:
Isaiah omits Hezekiah's payment of tribute, which 2 Kings 18:14-16 records, and Isaiah
includes Hezekiah's psalm at 38:9-20, which Kings does not have.

The four chapters are also placed rather than merely appended. They end with Babylonian
envoys in the palace and a prophecy of exile to Babylon, which is the subject the second
half of the book opens on at chapter 40. The narrative is the bridge between the Assyrian
crisis and the Babylonian one.

Usage:
    python3 fold_isaiah_hezekiah.py [--check]
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
"isaiah34": [
 ("Come Near, Ye Nations (vv.1-4)",
  "Come near, ye nations, to hear, and hearken, ye people, let the earth hear, and all that is therein. "
  "The summons is universal and the scale is deliberately larger than the chapter's actual subject, which "
  "turns out to be Edom. Then the sky, and all the host of heaven shall be dissolved, and the heavens "
  "shall be rolled together as a scroll, and all their host shall fall down, as the leaf falleth off from "
  "the vine. Revelation 6:13-14 takes up both images, the scroll and the falling fruit, in the same "
  "order."),
 ("The Sword Against Edom (vv.5-7)",
  "My sword shall be bathed in heaven, behold, it shall come down upon Idumea, and upon the people of my "
  "curse. The language throughout is sacrificial rather than military, the sword of the LORD is filled "
  "with blood, for the LORD hath a sacrifice in Bozrah, and the animals listed are the ones a sacrifice "
  "would use, lambs, goats, rams, bullocks and unicorns. Edom is described as an offering rather than as "
  "an enemy, which is the same figure Ezekiel 39 uses of Gog's army."),
 ("The Day of Vengeance (v.8)",
  "One verse, and it states the accounting the whole chapter rests on. For it is the day of the LORD's "
  "vengeance, and the year of recompences for the controversy of Zion. The word controversy is a legal "
  "term, so what is described is a case being settled rather than a grudge being satisfied, and the "
  "party bringing it is named."),
 ("Edom's Perpetual Desolation (vv.9-15)",
  "And the streams thereof shall be turned into pitch, and the dust thereof into brimstone, which puts "
  "Edom in the same category as Sodom. The desolation is then measured, as at 13:20-22, by what moves "
  "in: the cormorant and the bittern, the owl and the raven, dragons in the palaces, thorns in the "
  "fortresses. The wild goats and the screech owl take over, and the great owl makes her nest and lays "
  "and hatches there, which is the detail that makes it permanent. Nesting is not passing through."),
 ("Seek It in the Book (vv.16-17)",
  "Seek ye out of the book of the LORD, and read, no one of these shall fail, none shall want her mate. "
  "The instruction is documentary and it is unusual: the reader is told to check the list against a "
  "written record. And the allocation is put in the language of the conquest, they shall possess it for "
  "ever, from generation to generation shall they dwell therein, so the birds and beasts of the previous "
  "section receive Edom by lot the way the tribes received Canaan in Joshua."),
],
"isaiah35": [
 ("The Desert Shall Rejoice (vv.1-2)",
  "The wilderness and the solitary place shall be glad for them, and the desert shall rejoice, and "
  "blossom as the rose. Placed immediately after Edom turned to pitch and brimstone, the reversal is the "
  "point of the chapter's position. And what the desert is given is not merely water but the reputation "
  "of the best country in the region, the glory of Lebanon shall be given unto it, the excellency of "
  "Carmel and Sharon, which are the three places chapter 33 listed as failing."),
 ("Strengthen Ye the Weak Hands (vv.3-4)",
  "Strengthen ye the weak hands, and confirm the feeble knees, which is the physical description of fear "
  "from 13:7 addressed and reversed rather than described. Hebrews 12:12 quotes it as an instruction to a "
  "discouraged church. Then the message to be delivered, and the order of its clauses is the argument, "
  "say to them that are of a fearful heart, Be strong, fear not, behold, your God will come with "
  "vengeance, he will come and save you. The vengeance and the saving are the same arrival."),
 ("The Eyes of the Blind Shall Be Opened (vv.5-6a)",
  "Then the eyes of the blind shall be opened, and the ears of the deaf shall be unstopped, then shall "
  "the lame man leap as an hart, and the tongue of the dumb sing. Four conditions named and reversed, and "
  "the section stops in the middle of verse 6 because the sentence turns there from bodies to landscape. "
  "This is the passage Jesus points to when John's disciples ask whether he is the one, in Matthew 11: he "
  "does not answer the question, he lists these four items and lets the questioner make the "
  "identification."),
 ("Waters in the Wilderness (vv.6b-7)",
  "For in the wilderness shall waters break out, and streams in the desert. Then the specific "
  "transformation, and the parched ground shall become a pool, and the thirsty land springs of water, and "
  "the closing detail is botanical and exact, in the habitation of dragons, where each lay, shall be "
  "grass with reeds and rushes. Reeds need standing water, so naming them is a way of saying the change "
  "is permanent rather than a single storm."),
 ("The Way of Holiness (vv.8-9)",
  "And an highway shall be there, and a way, and it shall be called The way of holiness. What is said "
  "about it is mostly about who cannot be on it, the unclean shall not pass over it, no lion shall be "
  "there, nor any ravenous beast shall go up thereon. And then a clause that has been read two ways for "
  "centuries, the wayfaring men, though fools, shall not err therein. It either means that the road is "
  "so plain that the simplest traveller cannot get lost, or that fools are excluded, and the Hebrew "
  "permits both; the first reading fits the sentence's shape better."),
 ("The Ransomed Shall Return (v.10)",
  "One verse to end the first half of the book's poetry. And the ransomed of the LORD shall return, and "
  "come to Zion with songs and everlasting joy upon their heads, they shall obtain joy and gladness, and "
  "sorrow and sighing shall flee away. Revelation 21:4 says the same thing in different words, and the "
  "verse is the destination of the highway in the previous section: the road exists to be walked home on."),
],
"isaiah36": [
 ("Sennacherib Takes the Fenced Cities (v.1)",
  "Now it came to pass in the fourteenth year of king Hezekiah, that Sennacherib king of Assyria came up "
  "against all the defenced cities of Judah, and took them. One verse, and it is the most heavily "
  "corroborated event in the book. Sennacherib's own annals describe the campaign of 701 BC and claim "
  "forty-six walled cities taken; the Lachish reliefs from his palace at Nineveh show one of those "
  "sieges in detail and are now in the British Museum. What his account does not claim is Jerusalem. And "
  "what this verse does not mention is the tribute Hezekiah paid, which 2 Kings 18:14-16 records and "
  "Sennacherib's annals also record."),
 ("Rabshakeh Sent to Jerusalem (v.2)",
  "And the king of Assyria sent Rabshakeh from Lachish to Jerusalem with a great army. Rabshakeh is a "
  "title rather than a name, roughly chief officer. The meeting place is given precisely, and he stood by "
  "the conduit of the upper pool in the highway of the fuller's field, which is the same spot where "
  "Isaiah had met Ahaz in 7:3. Two kings, two generations apart, are addressed at the same waterworks, "
  "and the parallel is almost certainly deliberate."),
 ("Hezekiah's Representatives (v.3)",
  "Then came forth unto him Eliakim, Hilkiah's son, which was over the house, and Shebna the scribe, and "
  "Joah, Asaph's son, the recorder. Two of those three names are the officials of the oracle at 22:15-25, "
  "where Shebna was demoted and Eliakim promoted, and here Eliakim is over the house and Shebna is "
  "scribe. The prophecy and the narrative in the same book line up on the personnel."),
 ("Whereon Do Ye Trust (vv.4-6)",
  "The speech is a good speech and the book lets it run at length. It opens by naming the question "
  "correctly, what confidence is this wherein thou trustest. Then it dismantles the Egyptian option with "
  "an image the prophet himself had used, lo, thou trustest in the staff of this broken reed, on Egypt, "
  "whereon if a man lean, it will go into his hand, and pierce it. Isaiah had said the same thing at 30:7 "
  "and 31:3. The Assyrian officer's assessment of the alliance is identical to the prophet's, which is "
  "the most uncomfortable fact in the chapter."),
 ("Is It Not the LORD Whose High Places He Has Taken Away (vv.7-10)",
  "The second argument turns Hezekiah's reform into evidence against him, but if thou say, I trust in the "
  "LORD our God, is it not he, whose high places and whose altars Hezekiah hath taken away. To an "
  "observer who assumed more shrines meant more divine support, centralising worship looked like "
  "dismantling the defences. Then a taunt about manpower, I will give thee two thousand horses, if thou "
  "be able on thy part to set riders upon them. And then a theological claim, am I now come up without "
  "the LORD against this land, the LORD said unto me, Go up against this land, and destroy it. He is "
  "claiming Isaiah's own position, and 10:5 had in fact said Assyria was the rod of God's anger."),
 ("Speak in the Syrian Language (vv.11-12)",
  "Then said Eliakim and Shebna and Joah unto Rabshakeh, Speak, I pray thee, unto thy servants in the "
  "Syrian language, for we understand it, and speak not to us in the Jews' language, in the ears of the "
  "people that are on the wall. The officials want the negotiation conducted in Aramaic, the diplomatic "
  "language of the region, so the garrison cannot follow it. The request is a request for privacy and it "
  "concedes that the argument is working. Rabshakeh's answer refuses it and makes plain who the audience "
  "always was: the men on the wall, who will have to eat their own dung and drink their own piss."),
 ("He Cried with a Loud Voice in the Jews' Language (vv.13-20)",
  "Then Rabshakeh stood, and cried with a loud voice in the Jews' language. The speech to the troops is "
  "shrewder than the one to the officials. It offers terms that sound generous, make an agreement with me "
  "by a present, and come out to me, and eat ye every one of his vine, until I come and take you away to "
  "a land like your own land. Then the argument from precedent, and it is the strongest card he holds, "
  "where are the gods of Hamath and Arphad, have they delivered Samaria out of my hand. Every name he "
  "lists is a real defeat. And the conclusion, who are they among all the gods of these lands, that have "
  "delivered their land out of my hand, that the LORD should deliver Jerusalem out of my hand. The flaw "
  "is a category error, which chapter 37 will name, but the reasoning from evidence is sound."),
 ("But They Held Their Peace (vv.21-22)",
  "But they held their peace, and answered him not a word, for the king's commandment was, saying, Answer "
  "him not. The silence is an instruction rather than a failure of nerve, and it is the only recorded "
  "response to the most persuasive speech in the book. Then the officials go back with their clothes "
  "torn, which is the sign of mourning, so the argument had landed even though nobody replied to it."),
],
"isaiah37": [
 ("Hezekiah Sends to Isaiah (vv.1-4)",
  "And it came to pass, when king Hezekiah heard it, that he rent his clothes, and covered himself with "
  "sackcloth, and went into the house of the LORD. Then a message to the prophet, and the image in it is "
  "the most precise description of stalemate in scripture, the children are come to the birth, and there "
  "is not strength to bring forth. What he asks for is modest and carefully worded, wherefore lift up thy "
  "prayer for the remnant that is left, and the ground he offers is the one thing Rabshakeh's speech "
  "exposed, it may be the LORD thy God will hear the words of Rabshakeh, to reproach the living God."),
 ("Be Not Afraid of the Words (vv.5-7)",
  "Thus shall ye say unto your master, Be not afraid of the words that thou hast heard. The reply "
  "addresses the speech rather than the army, which is the right diagnosis of what had actually done the "
  "damage. Then the mechanism, behold, I will send a blast upon him, and he shall hear a rumour, and "
  "shall return to his own land, and I will cause him to fall by the sword in his own land. Three "
  "predictions, and the chapter's last section reports all three."),
 ("The Letter (vv.8-13)",
  "Rabshakeh withdraws to deal with an Ethiopian army and sends a letter instead, which is an escalation "
  "in form: a document rather than a speech. Its argument is the same as before and better organised, let "
  "not thy God, in whom thou trustest, deceive thee, and the list of precedents is longer, Gozan, Haran, "
  "Rezeph, the children of Eden, Hena, Ivah. Where is the king of Hamath, and the king of Arphad. Each "
  "name is a state that had a god and a wall and no longer exists."),
 ("Hezekiah's Prayer (vv.14-20)",
  "And Hezekiah received the letter, and went up unto the house of the LORD, and spread it before the "
  "LORD. The gesture is the whole of the chapter's method: he does not answer the letter, he files it in "
  "the temple. The prayer then does two things. It concedes the evidence, of a truth, LORD, the kings of "
  "Assyria have laid waste all the nations. And it names the category error, for they were no gods, but "
  "the work of men's hands, wood and stone, therefore they have destroyed them. Rabshakeh's argument was "
  "sound about every case in his list and every case in his list was a manufactured god. And the request "
  "is for a public demonstration rather than for rescue as such, that all the kingdoms of the earth may "
  "know that thou art the LORD, even thou only."),
 ("The Poem Against Sennacherib (vv.21-29)",
  "The answer comes as verse, and it opens by giving Jerusalem a voice it has not had in two chapters, "
  "the virgin the daughter of Zion hath despised thee, and laughed thee to scorn. Then the charge, whom "
  "hast thou reproached and blasphemed, even against the Holy One of Israel. Sennacherib's own boasts are "
  "quoted back at him and they are boasts about engineering, by the multitude of my chariots am I come up "
  "to the height of the mountains, I have digged, and drunk water. And the reply is the axe argument of "
  "10:15 in a different figure, hast thou not heard long ago how I have done it, that I should bring it "
  "to pass. And the closing image is stabling, I will put my hook in thy nose, and my bridle in thy lips, "
  "and I will turn thee back by the way by which thou camest."),
 ("The Sign of What Grows by Itself (vv.30-32)",
  "And this shall be a sign unto thee, Ye shall eat this year such as groweth of itself, and the second "
  "year that which springeth of the same, and in the third year sow ye, and reap. The sign is a farming "
  "calendar: two years of living off volunteer growth because the fields were not planted during the "
  "invasion, and normal sowing in the third. It is a promise of ordinary agriculture resuming, measured "
  "in seasons, and it is offered as proof. And the remnant language returns, the remnant that is escaped "
  "of the house of Judah shall again take root downward, and bear fruit upward."),
 ("He Shall Not Come into This City (vv.33-35)",
  "He shall not come into this city, nor shoot an arrow there, nor come before it with shields, nor cast "
  "a bank against it. Four military actions specifically excluded, which is a falsifiable prediction "
  "rather than a general assurance. And the reason given at the end is not Hezekiah's reform or Judah's "
  "merit, for I will defend this city to save it, for mine own sake, and for my servant David's sake."),
 ("The Angel, and Nineveh (vv.36-38)",
  "Then the angel of the LORD went forth, and smote in the camp of the Assyrians a hundred and fourscore "
  "and five thousand. The cause is not stated and the text does not speculate; what it records is that "
  "when they arose early in the morning, behold, they were all dead corpses. So Sennacherib king of "
  "Assyria departed, and went and returned, and dwelt at Nineveh, which is the second of the three "
  "predictions at verse 7. And the third is the last two verses, and it took twenty years: as he was "
  "worshipping in the house of Nisroch his god, Adrammelech and Sharezer his sons smote him with the "
  "sword. Assyrian and Babylonian records confirm that Sennacherib was assassinated by his own sons in "
  "681 BC and that Esarhaddon succeeded him."),
],
"isaiah38": [
 ("Set Thine House in Order (vv.1-3)",
  "In those days was Hezekiah sick unto death, and Isaiah came unto him, and said, Thus saith the LORD, "
  "Set thine house in order, for thou shalt die, and not live. There is no condition attached to it and "
  "no invitation to pray, which is what makes the next verse remarkable. Then he turned his face toward "
  "the wall, and prayed, and the prayer is quoted, remember now, O LORD, I beseech thee, how I have "
  "walked before thee in truth and with a perfect heart. And Hezekiah wept sore. An unconditional "
  "announcement is met with an argument from his record and with tears."),
 ("Fifteen Years Added (vv.4-6)",
  "Then came the word of the LORD to Isaiah, saying, Go, and say to Hezekiah, I have heard thy prayer, I "
  "have seen thy tears, behold, I will add unto thy days fifteen years. The sentence is reversed, which "
  "in a book this concerned with the reliability of God's word raises a real question, and the answer "
  "this narrative gives is that the word had not been given as a decree to be endured but as news to be "
  "responded to. A deliverance from Assyria is attached as well, which dates the illness to the same "
  "period as the siege."),
 ("The Shadow Turned Back (vv.7-8)",
  "And this shall be a sign unto thee from the LORD, behold, I will bring again the shadow of the degrees "
  "which is gone down in the sun dial of Ahaz, ten degrees backward. The instrument named belonged to the "
  "king who had refused a sign in chapter 7, which is a quiet piece of irony: the son gets his sign on "
  "his father's sundial. 2 Kings 20 adds that Hezekiah was offered the choice of forward or backward and "
  "chose backward as the harder."),
 ("Hezekiah's Psalm (vv.9-20)",
  "The writing of Hezekiah king of Judah, when he had been sick, and this is the passage 2 Kings does not "
  "have. It is a psalm, and its most striking quality is how little consolation it takes from death. I "
  "said in the cutting off of my days, I shall go to the gates of the grave, I am deprived of the residue "
  "of my years. The images are all of things ending abruptly, mine age is departed as a shepherd's tent, "
  "I have cut off like a weaver my life. Then the sound he makes, like a crane or a swallow, so did I "
  "chatter, I did mourn as a dove. And the reason he wants to live is stated plainly and is not "
  "sentimental, for the grave cannot praise thee, death cannot celebrate thee, the living, the living, he "
  "shall praise thee. The turn comes at verse 17, thou hast in love to my soul delivered it from the pit "
  "of corruption, for thou hast cast all my sins behind thy back."),
 ("The Fig Poultice (vv.21-22)",
  "For Isaiah had said, Let them take a lump of figs, and lay it for a plaister upon the boil, and he "
  "shall recover. Two verses, placed after the psalm rather than before it, which reads as a note added "
  "to a document already finished. What they record is a treatment: the miracle and the poultice are put "
  "in the same account without any sense that one competes with the other. And the last verse is "
  "Hezekiah's own question, what is the sign that I shall go up to the house of the LORD, which is what "
  "he wanted the fifteen years for."),
],
"isaiah39": [
 ("Babylon's Envoys (v.1)",
  "At that time Merodach-baladan, the son of Baladan, king of Babylon, sent letters and a present to "
  "Hezekiah, for he had heard that he had been sick, and was recovered. Merodach-baladan is a real and "
  "well-documented figure who led Babylonian resistance to Assyria twice, and a get-well delegation from "
  "him to a king who had just survived an Assyrian siege is not a courtesy call. It is a recruitment "
  "approach for an anti-Assyrian alliance, which is the policy Isaiah has opposed for thirty chapters."),
 ("Hezekiah Shows Them Everything (v.2)",
  "And Hezekiah was glad of them, and shewed them the house of his precious things, the silver, and the "
  "gold, and the spices, and the precious ointment, and all the house of his armour, and all that was "
  "found in his treasures, there was nothing among his treasures that he shewed them not. The verse ends "
  "with that clause twice over for emphasis. A king who had prayed his way through a siege gives a "
  "foreign power a full inventory of his assets and his arsenal, and the text records his mood: he was "
  "glad."),
 ("Isaiah's Questions (vv.3-4)",
  "Then came Isaiah the prophet unto king Hezekiah, and said unto him, What said these men, and from "
  "whence came they unto thee. The interrogation is conducted in short questions and the answers get "
  "shorter, and Hezekiah said, They are come from a far country unto me, even from Babylon. Then, what "
  "have they seen in thine house. And the answer is the admission, all that is in mine house have they "
  "seen, there is nothing among my treasures that I have not shewed them."),
 ("Carried to Babylon (vv.5-7)",
  "Then said Isaiah to Hezekiah, Hear the word of the LORD of hosts, Behold, the days come, that all "
  "that is in thine house shall be carried to Babylon, nothing shall be left. The sentence follows the "
  "confession exactly: what was shown will be taken. And it extends to his family, and of thy sons that "
  "shall issue from thee shall they take away, and they shall be eunuchs in the palace of the king of "
  "Babylon. That happened a century later, and the men it happened to include the young captives of "
  "Daniel 1."),
 ("Peace in My Days (v.8)",
  "Then said Hezekiah to Isaiah, Good is the word of the LORD which thou hast spoken. And then the "
  "sentence the chapter is remembered for, and the last words of the book's first half, for he said, For "
  "there shall be peace and truth in my days. Read charitably it is submission to a just verdict. Read as "
  "it stands it is a man calculating that the disaster falls after his own lifetime and finding that "
  "acceptable, which is why the editor put it here. The Assyrian crisis is over, Babylon has been named, "
  "and the next chapter opens speaking to the people the sentence lands on: comfort ye, comfort ye my "
  "people."),
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
