#!/usr/bin/env python3
"""
Jeremiah 37 to 45: the fall of Jerusalem, the murder of Gedaliah, and the flight into
Egypt. Nine pages, 171 verses.

Eight of the nine sublists are folded as they stand. jeremiah45's is not: it divided a
five-verse chapter into four sections by splitting verse 5 three ways, into 5a, 5b and
5c. The corpus format recognises half verses and not thirds, so that split would have
covered verse 5 twice over. The chapter is written here as two sections, Baruch's
complaint and the answer to it, which is what the text actually divides into.

This is the narrative spine of the book and the sections follow the people rather than
the oracles. Zedekiah appears four times and behaves identically each time: he believes
Jeremiah enough to protect him, never enough to obey him, and at 38:5 tells his own
officials that the king is not he that can do any thing against you. The one act of
plain kindness in the whole stretch comes from a foreign court official who thought to
pad the ropes before hauling a man out of a cistern.

Chapter 44 contains the most articulate rejection of a prophet anywhere in scripture,
and it is an argument from evidence: things went wrong after Josiah's reform stopped the
incense, therefore the reform caused the disaster. The same data, read exactly
backwards.

Usage:
    python3 fold_jeremiah_fall.py [--check]
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
"jeremiah37": [
 ("Egypt Comes Up, and the Chaldeans Depart (vv.1-5)",
  "Zedekiah was made king by Nebuchadrezzar, and the verdict on him is the same one 2 Chronicles 36 "
  "gives, he humbled not himself before Jeremiah the prophet speaking from the mouth of the LORD. He "
  "sends two officials with a request, pray now unto the LORD our God for us. Then the military "
  "position, and it is the hinge of the chapter: Pharaoh's army was come forth out of Egypt, and when "
  "the Chaldeans that besieged Jerusalem heard tidings of them, they departed from Jerusalem. The siege "
  "lifts. This is the moment when everything the peace-prophets had been saying appeared to be coming "
  "true, and it is almost certainly the moment the slaves freed in chapter 34 were taken back."),
 ("They Shall Come Again (vv.6-10)",
  "The reply refuses the reprieve in its first sentence, Pharaoh's army, which is come forth to help "
  "you, shall return to Egypt into their own land. And the Chaldeans shall come again, and fight "
  "against this city, and take it, and burn it with fire. Then a warning put in deliberately extreme "
  "terms, deceive not yourselves, for though ye had smitten the whole army of the Chaldeans that fight "
  "against you, and there remained but wounded men among them, yet should they rise up and burn this "
  "city with fire. Even a beaten Babylon would be sufficient, which is a claim about who is actually "
  "conducting the siege."),
 ("Arrested as a Deserter (vv.11-15)",
  "With the siege lifted he sets out for Benjamin to see to his property, which is presumably the field "
  "he bought in chapter 32. He is stopped at the gate by Irijah and accused, thou fallest away to the "
  "Chaldeans. He denies it flatly, then said Jeremiah, It is false, I fall not away to the Chaldeans, "
  "but he hearkened not to him. The arrest is intelligible on its face, and the book does not pretend "
  "otherwise: a man who had publicly told the garrison that the way of life was to surrender, walking "
  "out through the gate the moment the besiegers withdrew."),
 ("In the Dungeon Many Days (v.16)",
  "One verse. When Jeremiah was entered into the dungeon, and into the cabins, and Jeremiah had "
  "remained there many days. The word rendered dungeon is a cistern and the cabins are vaulted cells. "
  "No duration is given, no conditions are described, and there is no prayer and no complaint, which "
  "in a book this full of both is itself worth noticing."),
 ("Zedekiah Sends Secretly (vv.17-21)",
  "Then Zedekiah the king sent, and took him out, and asked him secretly in his house, Is there any "
  "word from the LORD. The answer is one sentence with nothing added to soften it, there is, for thou "
  "shalt be delivered into the hand of the king of Babylon. Then the prophet uses the private audience "
  "for something practical, cause me not to return to the house of Jonathan the scribe, lest I die "
  "there. It is granted, along with a ration, they gave him daily a piece of bread out of the bakers' "
  "street. So the king believes him enough to keep him alive and not enough to act, which is Zedekiah's "
  "whole character in four verses."),
],
"jeremiah38": [
 ("The Princes Demand His Death (vv.1-4)",
  "Four named officials report what he has been saying, he that remaineth in this city shall die by the "
  "sword, by the famine, and by the pestilence, but he that goeth forth to the Chaldeans shall live. "
  "Their charge is not that it is untrue. It is that it is destructive, we beseech thee, let this man be "
  "put to death, for he weakeneth the hands of the men of war. That is a morale charge, and on its own "
  "terms it is accurate, which is what makes this chapter uncomfortable."),
 ("Into the Cistern (vv.5-6)",
  "Zedekiah's reply is the most revealing line about him in the book, behold, he is in your hand, for "
  "the king is not he that can do any thing against you. A king informing his own officials that he is "
  "powerless to stop them. Then they let him down into the dungeon of Malchiah, and the detail is "
  "specific, there was no water in the dungeon, but mire, so Jeremiah sunk in the mire. He is left to "
  "die of hunger and exposure rather than executed, which leaves everyone's hands technically clean."),
 ("Ebed-melech's Rescue (vv.7-13)",
  "Ebed-melech the Ethiopian, one of the eunuchs which was in the king's house, hears of it, goes to "
  "the king at the gate of Benjamin, and makes an argument, these men have done evil in all that they "
  "have done to Jeremiah the prophet, and he is like to die for hunger in the place where he is. "
  "Zedekiah, who has just said he could do nothing, immediately authorises thirty men. And the rescue "
  "contains a detail the narrative did not need, put now these old cast clouts and rotten rags under "
  "thine armholes under the cords, so the ropes would not cut him as he was hauled up. The one act of "
  "plain kindness in this stretch of the book comes from a foreign court official and includes padding "
  "for the ropes."),
 ("The Last Secret Interview (vv.14-23)",
  "The king sends for him again, and Jeremiah's first response is about his own survival, if I declare "
  "it unto thee, wilt thou not surely put me to death. The counsel he then gives is specific and "
  "personal, if thou wilt assuredly go forth unto the king of Babylon's princes, then thy soul shall "
  "live, and this city shall not be burned, and thou shalt live, and thine house. And then the king's "
  "real objection comes out, and it is not theological at all, I am afraid of the Jews that are fallen "
  "to the Chaldeans, lest they deliver me into their hand, and they mock me. Told that his life and his "
  "city turn on one decision, he refuses it because of what the defectors already in the enemy camp "
  "might say about him."),
 ("Let No Man Know (vv.24-28)",
  "The interview ends with the king arranging a cover story and supplying the exact words to use, let "
  "no man know of these words, and thou shalt not die. Jeremiah uses them, so Jeremiah said unto them "
  "according to all these words that the king had commanded. The last thing Zedekiah does in this "
  "narrative is manage the appearance of a conversation he had no intention of acting on. And the "
  "chapter closes on a location that quietly dates everything, so Jeremiah abode in the court of the "
  "prison until the day that Jerusalem was taken."),
],
"jeremiah39": [
 ("The Breach (vv.1-3)",
  "The ninth year, tenth month, and then the eleventh year, fourth month, ninth day, the city was "
  "broken up. Eighteen months of siege in two verses. Then the officers of the victorious army are "
  "listed by name and title, Nergal-sharezer, Samgar-nebo, Sarsechim, Rabsaris, Rabmag, and they sat in "
  "the middle gate. The naming is the point. The gate where the elders of Jerusalem had sat to judge "
  "cases now has a foreign administration sitting in it, doing the same work."),
 ("The Flight and the Capture (vv.4-7)",
  "Zedekiah goes out by night by the way of the king's garden and is overtaken in the plains of "
  "Jericho. What is done to him reconciles two earlier oracles that had looked incompatible, 32:4 said "
  "he would see the king of Babylon eye to eye and Ezekiel 12:13 said he would not see Babylon. They "
  "slew the sons of Zedekiah before his eyes, then he put out the eyes of Zedekiah. He saw the king of "
  "Babylon face to face, and then he never saw the city."),
 ("The City Burned, and the Poor Given the Fields (vv.8-10)",
  "The Chaldeans burned the king's house and the houses of the people, and brake down the walls of "
  "Jerusalem, and the remnant was carried away. Then a clause easy to read past, which is where "
  "chapter 40's whole problem begins: Nebuzar-adan the captain of the guard left of the poor of the "
  "people, which had nothing, in the land of Judah, and gave them vineyards and fields. The people with "
  "no property are given property. A land redistribution at the very bottom of the society is the one "
  "constructive thing the catastrophe produces, and it is done by the invading general."),
 ("Nebuchadrezzar's Order Concerning Jeremiah (vv.11-14)",
  "Nebuchadrezzar gave charge concerning Jeremiah, saying, Take him, and look well to him, and do him "
  "no harm, but do unto him even as he shall say unto thee. Standing orders from the emperor to protect "
  "a prophet of the nation he has just destroyed. That is what forty years of telling Judah to submit "
  "looked like from the other side of the siege line, and it is also why his own people had thought him "
  "a traitor. He is committed to Gedaliah and dwelt among the people."),
 ("Ebed-melech's Reward (vv.15-18)",
  "The chapter closes with a word dated back to the time in the prison and addressed to the man who "
  "pulled him out of the cistern. Behold, I will bring my words upon this city for evil, and not for "
  "good, but I will deliver thee in that day, and thou shalt not be given into the hand of the men of "
  "whom thou art afraid. And the ground of it is not the rescue but what produced the rescue, because "
  "thou hast put thy trust in me, saith the LORD."),
],
"jeremiah40": [
 ("Released at Ramah (vv.1-6)",
  "This account overlaps chapter 39 and reads as the fuller of the two. He is found among the deportees, "
  "bound in chains among all that were carried away captive of Jerusalem, which means the protective "
  "order had not reached whoever was doing the sorting. The captain of the guard's speech is remarkable "
  "in the mouth of a Babylonian officer, the LORD thy God hath pronounced this evil upon this place, "
  "now the LORD hath brought it, because ye have sinned against the LORD, and have not obeyed his "
  "voice. Then a choice, come with me to Babylon and be looked after, or stay. He stays, which after "
  "forty years of insisting that Babylon was where God's hand was, is a decision worth pausing over."),
 ("Gedaliah at Mizpah (vv.7-12)",
  "The captains still in the field hear that the king of Babylon has made Gedaliah the son of Ahikam "
  "governor. His family is why he is trustworthy in this book: Ahikam is the man who protected Jeremiah "
  "from the mob at 26:24, and one of Shaphan's sons. The policy he announces under oath is the counsel "
  "Jeremiah had been giving for decades, fear not to serve the Chaldeans, dwell in the land, and serve "
  "the king of Babylon, and it shall be well with you. And it worked. Refugees came back from Moab, "
  "Ammon and Edom, and gathered wine and summer fruits very much. One good harvest under a competent "
  "administration."),
 ("Johanan's Warning (vv.13-16)",
  "Johanan brings intelligence and names the sponsor, knowest thou certainly that Baalis the king of "
  "the Ammonites hath sent Ishmael the son of Nethaniah to slay thee, and then offers to handle it "
  "quietly, let me go, and I will slay Ishmael, and no man shall know it. Gedaliah refuses and calls "
  "the report a fabrication, thou shalt not do this thing, for thou speakest falsely of Ishmael. The "
  "warning was accurate and the remedy offered was a political murder, and refusing it is the last "
  "decision the last competent government in Judah ever takes."),
],
"jeremiah41": [
 ("The Assassination (vv.1-3)",
  "Ishmael the son of Nethaniah, of the seed royal, came with ten men, and they did eat bread together "
  "in Mizpah, and rose up and smote Gedaliah with the sword. Two details in that sentence make it "
  "worse than a coup. Of the seed royal, so this is a Davidic claimant removing a commoner appointed "
  "over him. And they did eat bread together, so it is a breach of hospitality, which in that culture "
  "is close to the worst thing a guest can do. The Chaldean garrison is killed with him, which "
  "guarantees a reprisal."),
 ("The Pilgrims Killed at the Pit (vv.4-9)",
  "And it came to pass the second day, and nobody outside Mizpah yet knows. Eighty men arrive from "
  "Shechem, Shiloh and Samaria with offerings and incense to bring to the house of the LORD, and that "
  "detail is a piece of information in itself: the temple is burned and people are still walking to the "
  "site with offerings, and they are coming from the northern towns. Ishmael goes out weeping to meet "
  "them, brings them inside, and kills them. Ten buy their lives with a hidden food store, and the "
  "bodies go into the pit that Asa the king had made for fear of Baasha, a cistern three centuries old, "
  "dug for a war nobody remembered."),
 ("The Captives Taken Toward Ammon (v.10)",
  "One verse. Then Ishmael carried away captive all the residue of the people that were in Mizpah, even "
  "the king's daughters, and departed to go over to the Ammonites. The entire surviving population of "
  "the province, the royal women included, taken as hostages toward the state that had commissioned the "
  "murder."),
 ("Overtaken at Gibeon (vv.11-15)",
  "Johanan and the captains pursue and find him by the great waters that are in Gibeon, and the detail "
  "worth keeping is the captives' reaction, when all the people which were with Ishmael saw Johanan, "
  "then they were glad. They change sides on sight, which says what the march to Ammon had been like. "
  "Ishmael escapes with eight men to the Ammonites. The rescue succeeds in everything except the one "
  "thing it was for."),
 ("Toward Egypt (vv.16-18)",
  "Johanan takes the recovered people and starts moving south, and the reason is stated without "
  "editorial comment, because they were afraid of them, because Ishmael had slain Gedaliah, whom the "
  "king of Babylon made governor in the land. The fear is entirely reasonable: the imperial appointee "
  "and his garrison have been murdered, and reprisal is the obvious next event. They halt at the "
  "habitation of Chimham by Bethlehem, on the road, intending to go into Egypt. Everything in the next "
  "three chapters follows from a decision that has in practice already been taken here."),
],
"jeremiah42": [
 ("Pray for Us, and We Will Obey (vv.1-6)",
  "The whole company comes to Jeremiah with a request that could hardly be better put, pray for us, "
  "that the LORD thy God may shew us the way wherein we may walk, and the thing that we may do. And "
  "they attach an undertaking with no escape clause in it, whether it be good, or whether it be evil, "
  "we will obey the voice of the LORD our God, and they call God to witness the undertaking, the LORD "
  "be a true and faithful witness between us. Chapter 43 is the reason this section has to be read "
  "carefully. There is nothing wrong with any of the wording. The next chapter shows what it was worth."),
 ("Ten Days (v.7)",
  "One verse, and it came to pass after ten days, that the word of the LORD came unto Jeremiah. It is "
  "the only interval of its kind recorded in the book. A column of frightened refugees waiting on a "
  "road with a reprisal expected behind them, and the answer takes ten days to arrive, which says "
  "something about how these words were understood to come. Not on request."),
 ("If Ye Abide in This Land (vv.8-12)",
  "The answer is to stay, and it is put in the verbs of the commission in chapter 1 used constructively "
  "for once, if ye will still abide in this land, then will I build you, and not pull you down, and I "
  "will plant you, and not pluck you up. What it asks them to surrender is a fear rather than a plan, "
  "be not afraid of the king of Babylon, of whom ye are afraid, for I am with you to save you. And then "
  "a promise about the enemy's disposition, I will shew mercies unto you, that he may have mercy upon "
  "you, and cause you to return to your own land."),
 ("If Ye Say, We Will Go into Egypt (vv.13-18)",
  "The alternative is set out with the people's own reasoning quoted inside it, we will go into the land "
  "of Egypt, where we shall see no war, nor hear the sound of the trumpet, nor have hunger of bread. "
  "The reply follows the logic of their sentence rather than contradicting it, the sword which ye feared "
  "shall overtake you there in the land of Egypt, and the famine whereof ye were afraid shall follow "
  "close after you. Everything they are running from is described as waiting at the destination."),
 ("Ye Dissembled in Your Hearts (vv.19-22)",
  "The tone changes before anyone has answered, and this is the sharpest thing in the chapter. Know "
  "certainly that I have admonished you this day, for ye dissembled in your hearts, when ye sent me "
  "unto the LORD your God, saying, Pray for us. He tells them, ahead of their reply, that the question "
  "had been settled before it was asked. Now therefore know certainly that ye shall die by the sword. "
  "He is not taken in by the excellent wording of verses 1 to 6, and he says so before the disobedience "
  "rather than after it."),
],
"jeremiah43": [
 ("Thou Speakest Falsely (vv.1-3)",
  "Azariah and Johanan and all the proud men answer, thou speakest falsely, the LORD our God hath not "
  "sent thee to say, Go not into Egypt to sojourn there. Then they supply a motive, and it is an "
  "accusation of being handled, but Baruch the son of Neriah setteth thee on against us, for to deliver "
  "us into the hand of the Chaldeans. It is the only place in scripture where Baruch is accused of "
  "anything, and one of very few where a prophet is charged with being someone else's mouthpiece."),
 ("They Went into Egypt, and Took Jeremiah (vv.4-7)",
  "So they came into the land of Egypt, for they obeyed not the voice of the LORD, and the roll of who "
  "went is complete, the men, and the women, and the children, and the king's daughters, and every "
  "person that Nebuzar-adan had left with Gedaliah, and Jeremiah the prophet, and Baruch the son of "
  "Neriah. He is taken along, and this is the last recorded fact about his movements: a man who spent "
  "forty years telling his people not to lean on Egypt, carried into Egypt against his will by the "
  "people he was sent to. They arrive at Tahpanhes, the frontier garrison town on the eastern delta."),
 ("The Stones Hid in the Clay (vv.8-13)",
  "The last sign-act in the book, and it is performed on foreign soil. Take great stones, and hide them "
  "in the clay in the brickkiln, which is at the entry of Pharaoh's house in Tahpanhes. Then the "
  "interpretation, I will set his throne upon these stones, so Nebuchadrezzar will place his throne on "
  "the pavement of the very courtyard they have fled into. The oracle runs on to the temple of the sun "
  "at Heliopolis and the images there. Forty years of saying that Babylon was where the hand of God "
  "was, said once more, in Egypt, at the door of Pharaoh's own residence."),
],
"jeremiah44": [
 ("Remember What Happened to Jerusalem (vv.1-10)",
  "The sermon is addressed to the Jewish community now at Migdol, Tahpanhes, Noph and Pathros, which "
  "shows they had spread the length of Egypt. The argument is entirely from recent memory, ye have seen "
  "all the evil that I have brought upon Jerusalem, behold, they are a desolation, and no man dwelleth "
  "therein, because of their wickedness which they have committed to provoke me to anger. And the "
  "charge is that the practice has been resumed in the new country, wherefore commit ye this great evil "
  "against your souls, in that ye burn incense unto other gods in the land of Egypt whither ye be gone "
  "to dwell. Not one conclusion drawn from the destruction they had just walked away from."),
 ("None Shall Return (vv.11-14)",
  "I will set my face against you for evil, and to cut off all Judah. The sentence is careful about its "
  "own exception, and none of the remnant of Judah, which are gone into the land of Egypt to sojourn "
  "there, shall escape or remain, that they should return into the land of Judah, save such as shall "
  "escape. The two clauses look contradictory and are not: the community as a community will not come "
  "back, and individual fugitives will."),
 ("We Will Certainly Burn Incense to the Queen of Heaven (vv.15-19)",
  "The reply is the most articulate rejection of a prophet anywhere in scripture, and it is delivered "
  "by the men whose wives had burned the incense, with the women standing there. As for the word that "
  "thou hast spoken unto us in the name of the LORD, we will not hearken unto thee. Then the reasoning, "
  "and it is empirical rather than defiant, for then had we plenty of victuals, and were well, and saw "
  "no evil, but since we left off to burn incense to the queen of heaven, we have wanted all things, "
  "and have been consumed by the sword and by the famine. They have read the same century of history "
  "and drawn the opposite conclusion: the trouble started when Josiah's reform stopped the practice, "
  "therefore the reform caused the disaster. It is a coherent argument from evidence, exactly inverted."),
 ("Whose Words Shall Stand (vv.20-28)",
  "The reply accepts their timeline and reverses the causation, did not the LORD remember the incense "
  "that ye burned in the cities of Judah, and came it not into his mind, so that the LORD could no "
  "longer bear, because of the abominations which ye have committed. Their oath is met with an oath and "
  "with a bleak permission, ye will surely accomplish your vows. And then, behold, I have sworn by my "
  "great name, that my name shall no more be named in the mouth of any man of Judah in all the land of "
  "Egypt. The section ends by naming what the whole argument is actually about, that all the remnant "
  "may know whose words shall stand, mine, or theirs."),
 ("The Sign of Pharaoh Hophra (vv.29-30)",
  "A falsifiable sign is attached to it, and this shall be a sign unto you, behold, I will give "
  "Pharaoh-hophra king of Egypt into the hand of his enemies. Hophra is the pharaoh the Greeks called "
  "Apries, and he was overthrown and killed in about 570 BC in a revolt led by Amasis, an episode "
  "Herodotus records. It is the last dated prophecy in the book and the last thing Jeremiah is recorded "
  "as saying to his own people. After this chapter he appears only in the appendix about Baruch and in "
  "the borrowed history of chapter 52."),
],
"jeremiah45": [
 ("Baruch's Complaint (vv.1-3)",
  "Dated the fourth year of Jehoiakim, which places it with chapter 36, the year of the burned scroll, "
  "and it has been set here instead at the close of the biographical section. Baruch gets five verses "
  "of his own, which is more than any other prophet's assistant gets in the whole Bible, and what they "
  "record is a complaint, woe is me now, for the LORD hath added grief to my sorrow, I fainted in my "
  "sighing, and I find no rest. The man who wrote the book down says that writing it wore him out."),
 ("Seek Not Great Things for Thyself (vv.4-5)",
  "The answer offers no comfort of the ordinary kind. It begins by putting his trouble beside a larger "
  "one, behold, that which I have built will I break down, and that which I have planted I will pluck "
  "up, even this whole land. Then the instruction, seekest thou great things for thyself, seek them "
  "not. And then what he is given in place of the great things, which is precisely what Jeremiah "
  "himself was promised and nothing more, for behold, I will bring evil upon all flesh, but thy life "
  "will I give unto thee for a prey. Your life, and no more than that. It is the last word spoken to "
  "any individual in the book before the oracles against the nations begin."),
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
        notes.append(f"{page}: kept {len(keep)} book field(s), dropped the sublist")
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
