#!/usr/bin/env python3
"""
Folds Jonah 1-4 onto the target Authorship & Background format.

This is the pattern book. Whatever ships here is what the remaining 633
chapters should copy, so the shape matters more than the fact it is only four
chapters.

Target field order:

    Author:              book level, unchanged, identical across the book
    Classification:      genre only, one line
    Key Themes:          split out of Classification, where it had been jammed
                         onto the end of the genre label
    Historical Context:  chapter level, unchanged
    <verse-range sections>   one per movement of the chapter, each a full
                             paragraph, replacing the bulleted Structure outline

The verse-range sections are the substance and the reason Ruth 1 runs 5,697
characters against Jonah 1's 1,612. The existing Structure bullets already
name each movement and its verses, so they serve as the skeleton and the
headings carry over unchanged.

Usage:
    python3 fold_jonah.py [--check]
"""
import os
import re
import sys

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")

# chapter -> (genre, key themes, [(section heading with verses, exposition)])
CHAPTERS = {
1: (
 "Prophetic Narrative",
 "Running from God&#x27;s call, the futility of flight, God&#x27;s sovereignty over "
 "nature, pagan sailors more responsive than God&#x27;s prophet, and a descent "
 "traced downward \u2014 into the ship, into sleep, into the sea",
 [
  ("The Call: Go to Nineveh (vv.1-2)",
   "The book opens without preamble: the word of the LORD comes to Jonah and sends "
   "him to Nineveh. No commissioning vision, no protest recorded yet, just the "
   "commission and the city. Nineveh is called \u201cthat great city\u201d, and the "
   "phrase is not flattery \u2014 it was the Assyrian capital, and Assyria was the "
   "empire Israel feared most. Its own royal inscriptions boast of flaying "
   "prisoners and stacking heads. God's stated reason for sending Jonah is that "
   "their wickedness \u201chas come up before me\u201d, the same language used of "
   "Sodom (Genesis 18:21). A prophet is being sent to a place Israel would have "
   "been glad to see destroyed."),
  ("The Flight: Down to Tarshish (v.3)",
   "Jonah's response is one verse and entirely physical: he rose, he went down, he "
   "paid, he went down again. Nineveh lay some five hundred miles northeast, "
   "overland. Tarshish is generally placed at the far western end of the "
   "Mediterranean, probably Spain \u2014 as close to the opposite direction as the "
   "known world allowed. The narrator repeats that he went \u201cdown\u201d to Joppa "
   "and \u201cdown\u201d into the ship, beginning a pattern the chapter sustains. The "
   "phrase \u201cfrom the presence of the LORD\u201d does not mean Jonah thought God "
   "was local; it is the language of a servant walking out on his post."),
  ("The Storm: God Pursues (vv.4-6)",
   "The LORD \u201churls\u201d a great wind onto the sea, the first of several times "
   "in this book that God directly commands the natural world. The sailors, "
   "seasoned Phoenician crew, are terrified enough to throw cargo overboard and each "
   "cries to his own god. Jonah meanwhile is asleep in the hold, having gone "
   "\u201cdown\u201d once more. The captain's rebuke is one of the sharper ironies in "
   "Scripture: a pagan sailor wakes the Hebrew prophet and tells him to pray. Those "
   "who do not know the LORD are doing what the man who does know Him will not."),
  ("The Lots: Jonah Exposed (vv.7-10)",
   "The crew cast lots to identify who has provoked this, and the lot falls on "
   "Jonah. Their questions come in a rush \u2014 occupation, country, people \u2014 "
   "and his answer is a confession of faith he is actively contradicting: \u201cI am "
   "a Hebrew; and I fear the LORD, the God of heaven, which hath made the sea and the "
   "dry land.\u201d He names the God who made the very sea now trying to kill him. "
   "When he admits he is fleeing, the sailors are \u201cexceedingly afraid\u201d, and "
   "their question is the reasonable one: why would you do this?"),
  ("The Sacrifice: Thrown Overboard (vv.11-16)",
   "Jonah tells them to throw him into the sea, and their reluctance is worth "
   "noticing. Rather than take him at his word, they row harder for shore, and only "
   "when that fails do they pray to the LORD by name, asking not to be held guilty "
   "for innocent blood. Pagan sailors show more concern for one Hebrew life than the "
   "Hebrew prophet showed for a hundred and twenty thousand Ninevites. The sea calms "
   "the moment he goes in, and the crew respond by sacrificing to the LORD and making "
   "vows. Jonah's disobedience has produced converts anyway \u2014 which is the "
   "book's argument in miniature."),
  ("The Fish: God Provides (v.17)",
   "The chapter's last verse turns the whole story: the LORD \u201cprepared\u201d a "
   "great fish. The verb is provision, not punishment. The sea was going to kill "
   "Jonah; the fish is what saves him. Three days and three nights is the detail "
   "Jesus takes up as a sign of His own burial and resurrection (Matthew 12:39-40), "
   "which is why this verse carries weight far beyond the narrative. Note also what "
   "the text does not say: it names no species, and speculating about which fish "
   "could swallow a man misses that the point is who commanded it."),
 ]),
2: (
 "Prophetic Poetry",
 "Prayer from the depths, deliverance from death, the temple as an orientation "
 "point, remembering God when the soul faints, and the confession that salvation "
 "belongs to the LORD",
 [
  ("Crying from the Depths (vv.1-2)",
   "Jonah prays from inside the fish, and the tense matters: he thanks God for a "
   "rescue already accomplished rather than begging for one still needed. He is "
   "praying from the place of deliverance, not the place of danger. He calls it "
   "\u201cthe belly of hell\u201d \u2014 sheol, the realm of the dead \u2014 because "
   "from his side of it, drowning had already begun. This is thanksgiving offered "
   "from a situation most people would still call a catastrophe."),
  ("God Cast Me Down; God Will Bring Me Up (vv.3-4)",
   "\u201cThou hadst cast me into the deep\u201d \u2014 Jonah attributes it to God, "
   "not to the sailors who physically threw him. He is right: the storm was hurled "
   "by the LORD and the lot fell where God directed. The waves are called "
   "\u201cthy billows\u201d. Then comes the turn: cast out of God's sight, he "
   "nonetheless says he will look again toward the holy temple. Facing Jerusalem in "
   "prayer was Solomon's provision for exiles (1 Kings 8:46-49), and Jonah, as far "
   "from the temple as a man can be, uses it."),
  ("The Waters of Death (vv.5-6a)",
   "The imagery closes in: waters compassed him, weeds wrapped his head, he went "
   "down to the bottoms of the mountains. The descent that began in chapter 1 "
   "reaches its floor here \u2014 he can go no lower. \u201cThe earth with her bars "
   "was about me\u201d reads like a prison door shutting. The poetry is drawn from "
   "Israel's psalms of distress; Psalms 18, 42, 69 and 142 all echo through this "
   "prayer, which tells us Jonah prayed in the vocabulary of his people's worship "
   "rather than inventing words of his own."),
  ("Deliverance: Thou Hast Brought Up My Life (v.6b)",
   "The hinge of the psalm, and it is one clause: \u201cyet hast thou brought up my "
   "life from corruption, O LORD my God.\u201d Everything before it goes down; "
   "everything after it looks up. The verb is the same direction Jonah has spent two "
   "chapters refusing. He did not climb out and he did not swim; he was brought. "
   "Notice too that he says \u201cmy God\u201d \u2014 the relationship survived the "
   "rebellion."),
  ("Remembering the LORD (vv.7-8)",
   "\u201cWhen my soul fainted within me I remembered the LORD.\u201d Remembering is "
   "not recalling a fact he had forgotten but turning back toward someone he had "
   "walked away from. Then a line that will read very differently by chapter 4: "
   "\u201cThey that observe lying vanities forsake their own mercy.\u201d Jonah "
   "means idolaters, and he is not wrong. But a man who resents God for showing "
   "mercy to Nineveh is himself forsaking mercy, and the book will make sure the "
   "reader notices."),
  ("The Confession: Salvation Is of the LORD (v.9)",
   "\u201cSalvation is of the LORD\u201d is the theological centre of the whole book. "
   "Jonah says it while being carried by a fish he did not summon, after a rescue he "
   "did not arrange, from a death he had chosen. He cannot claim any part of it. What "
   "he has not yet grasped is the scope of what he has just confessed: if salvation "
   "belongs to the LORD, then the LORD may give it to whomever He pleases \u2014 "
   "including Nineveh. Chapter 4 is Jonah discovering he meant it more narrowly than "
   "God does."),
  ("The Fish Obeys God&#x27;s Command (v.10)",
   "\u201cThe LORD spake unto the fish.\u201d The wind obeyed, the sea obeyed, the "
   "lot obeyed, the fish obeys, and in the chapters ahead a plant, a worm and a wind "
   "will each do the same. Everything in this book does what God says immediately, "
   "with a single exception, and that exception is the prophet. The contrast is the "
   "narrator's quiet argument."),
 ]),
3: (
 "Prophetic Narrative",
 "The second chance, obedience after failure, the shortest sermon and the largest "
 "revival, corporate repentance from king to cattle, and God relenting from "
 "declared judgment",
 [
  ("The Second Call: God Speaks Again (vv.1-2)",
   "\u201cAnd the word of the LORD came unto Jonah the second time.\u201d The "
   "commission is not withdrawn and not given to someone else. The wording nearly "
   "repeats 1:2, as though the intervening chapters had not happened \u2014 grace "
   "that resumes rather than grace that renegotiates. One phrase does shift: Jonah is "
   "now to preach \u201cthe preaching that I bid thee\u201d, the message specified as "
   "God's rather than the prophet's. After Tarshish, the terms are clearer."),
  ("Obedience: Jonah Goes (v.3)",
   "\u201cSo Jonah arose, and went unto Nineveh, according to the word of the "
   "LORD.\u201d The same verb that began his flight now begins his obedience. The "
   "narrator adds that Nineveh was \u201can exceeding great city of three days' "
   "journey\u201d, which most likely describes the greater administrative district "
   "rather than a walled circumference. Whatever the measure, it is large enough that "
   "the response recorded next is genuinely remarkable."),
  ("The Sermon: Eight Words (v.4)",
   "Jonah's sermon is five words in Hebrew and eight in English: \u201cYet forty "
   "days, and Nineveh shall be overthrown.\u201d No mention of the LORD by name, no "
   "call to repent, no offer of terms, no appeal. It is an announcement of demolition "
   "with a date on it. Whether Jonah preached it hoping to be believed or hoping to "
   "be ignored, the text does not say. The word translated \u201coverthrown\u201d is "
   "the one used of Sodom, and it can also carry the sense of being turned around "
   "\u2014 which is what actually happens."),
  ("The Response: Total Repentance (vv.5-9)",
   "The city believes God, and the repentance moves upward from the people to the "
   "king rather than being imposed from the throne down. The king leaves his seat, "
   "removes his robe, sits in ashes and issues a decree extending the fast to the "
   "animals \u2014 a detail that sounds strange until you realise it is how the "
   "ancient world expressed grief that admitted no exceptions. His reasoning is "
   "careful and theologically humble: \u201cWho can tell if God will turn and "
   "repent?\u201d He claims no promise. He orders his people to turn from violence, "
   "naming the specific sin Assyria was known for, and leaves the outcome with God."),
  ("God&#x27;s Response: Judgment Averted (v.10)",
   "\u201cGod saw their works, that they turned from their evil way; and God repented "
   "of the evil.\u201d God's relenting is not a change of character but the "
   "consistent application of it \u2014 Jeremiah 18:7-8 states the principle plainly: "
   "a declared judgment answers to repentance. What God saw was not their sackcloth "
   "but their turning. This one verse is what will send Jonah into the fury of "
   "chapter 4, and it is worth sitting with the fact that the prophet's complaint is "
   "about a successful mission."),
 ]),
4: (
 "Prophetic Narrative",
 "A prophet angry at mercy, God&#x27;s freedom to show compassion, the object "
 "lesson of gourd and worm, comfort valued above souls, and a book that ends on an "
 "unanswered question",
 [
  ("Jonah&#x27;s Anger: I Knew You Were Merciful (vv.1-4)",
   "Now the real reason for Tarshish comes out. Jonah is not afraid of Nineveh and "
   "was never worried the mission would fail \u2014 he fled because he was afraid it "
   "would succeed. His prayer quotes Israel's own creed back at God: gracious, "
   "merciful, slow to anger, of great kindness (Exodus 34:6). He knows the theology "
   "exactly and resents its application. He would rather die than watch his nation's "
   "enemies forgiven. God's reply is not a rebuke but a question: \u201cDoest thou "
   "well to be angry?\u201d It is the first of three questions that carry the rest of "
   "the book."),
  ("Jonah Watches and Waits (v.5)",
   "Jonah leaves the city, builds a shelter east of it and sits down to see what "
   "will happen. The posture is telling: he has not accepted the outcome and is "
   "waiting for the destruction to arrive after all. Having preached to the city, he "
   "positions himself where he can watch it burn. He is outside the community God has "
   "just spared, which is exactly where his theology has placed him."),
  ("The Object Lesson: Gourd, Worm, and Wind (vv.6-8)",
   "God prepares three things in succession, the same verb used of the fish: a plant "
   "for shade, a worm to kill it, and a scorching east wind. Jonah is \u201cexceeding "
   "glad\u201d of the plant \u2014 the only time in the book he is described as "
   "happy, and it is about his own comfort rather than a city's rescue. When it "
   "withers he again asks to die. The lesson is constructed rather than argued: God "
   "gives Jonah something to lose that cost him nothing, so that his grief over it "
   "can be held up beside his indifference to Nineveh."),
  ("God&#x27;s Final Question: Should I Not Spare Nineveh? (vv.9-11)",
   "God draws the comparison plainly: Jonah pitied a plant he neither planted nor "
   "grew, which lived and died in a day. Should God not pity a city of more than a "
   "hundred and twenty thousand people who \u201ccannot discern between their right "
   "hand and their left\u201d \u2014 most naturally read as the morally untaught, "
   "though some take it as young children \u2014 and also much cattle. The animals "
   "get one last mention, and it is not comic; God's compassion runs wider than the "
   "prophet's. Then the book simply stops. There is no verse recording Jonah's "
   "answer, because the question is no longer only his."),
 ]),
}

ITEM = ('                    <div class="auth-item">'
        '<span class="auth-label">{label}</span> {body}</div>')


def main():
    check = "--check" in sys.argv
    changed = 0
    problems = []

    for ch, (genre, themes, sections) in sorted(CHAPTERS.items()):
        name = f"jonah{ch}.html"
        path = os.path.join(DOCS, name)
        html = open(path, encoding="utf-8").read()

        m = re.search(r'(<div class="tab-content[^"]*" id="tab-authorship">)'
                      r'(.*?)(?=<div class="tab-content")', html, re.S)
        if not m:
            problems.append(f"{name}: no authorship pane")
            continue
        body = m.group(2)

        author = re.search(r'<div class="auth-item"><span class="auth-label">'
                           r'Author:</span>.*?</div>', body, re.S)
        hist = re.search(r'<div class="auth-item"><span class="auth-label">'
                         r'Historical Context:</span>.*?</div>', body, re.S)
        if not author or not hist:
            problems.append(f"{name}: missing Author or Historical Context")
            continue

        parts = ["\n                <h3>Authorship &amp; Background</h3>\n",
                 "                " + author.group(0) + "\n",
                 ITEM.format(label="Classification:", body=genre) + "\n",
                 ITEM.format(label="Key Themes:", body=themes) + "\n",
                 "                " + hist.group(0) + "\n"]
        for head, expo in sections:
            parts.append(ITEM.format(label=head + ":", body=expo) + "\n")
        # The captured region runs up to the next tab-content div, so it
        # includes this pane's own closing tag. Put it back.
        new_body = "".join(parts) + "            </div>\n\n            "

        new = html[:m.start(2)] + new_body + html[m.end(2):]
        o, c = len(re.findall(r"<div\b", new)), len(re.findall(r"</div>", new))
        if o != c:
            problems.append(f"{name}: div imbalance {o} vs {c}")
            continue
        if "Structure:" in new_body or "<ul" in new_body:
            problems.append(f"{name}: leftover Structure outline")
            continue

        changed += 1
        if not check:
            open(path, "w", encoding="utf-8").write(new)

    verb = "would fold" if check else "folded"
    print(f"{verb} {changed} Jonah chapters onto the target format")
    for p in problems:
        print(f"    {p}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
