#!/usr/bin/env python3
"""
Completes Mark: chapters 1, 13 and 14.

No Structure: sublists here either, so sections are written from the text. Mark's
own pacing supplies the divisions -- he moves by scene rather than by discourse,
and "straightway" marks most of the joins.

Extra fields folded into section prose rather than dropped:

  mark13  a field labelled "Mark 13:" whose body begins "32 is unique". The label
          was split at the colon of a verse reference, so the intended text was
          "Mark 13:32 is unique". Its point -- that only Mark records "neither the
          Son" -- belongs in the section covering v.32
  mark13  two headless paragraphs: the fourfold "Watch" at vv.5, 9, 33, 37, and the
          doorkeeper parable of vv.34-37 being unique to Mark
  mark14  "Mark includes a unique detail:" on the young man who fled naked, and two
          headless paragraphs on Abba in Gethsemane and the "I am" before the
          Sanhedrin

AM is added to the capitals allow-list. Mark 14:62 answers the high priest with the
divine name of Exodus 3:14, so "I am" set in capitals there is deliberate rather
than the emphatic shouting WORKFLOW.md rules out.

Usage:
    python3 fold_mark.py [--check]
"""
import os
import re
import sys

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")

ITEM = ('                    <div class="auth-item">'
        '<span class="auth-label">{label}</span> {body}</div>')

VERSES = {"mark1": 45, "mark13": 37, "mark14": 72}

CAPS_OK = {"LORD", "GOD", "YHWH", "OT", "NT", "BC", "AD", "KJV", "ESV", "ASV", "AM"}

KEEP = {
    "mark1": ["Author:", "Date Written:", "Audience:", "Purpose:",
              "Chapter 1 Content:"],
    "mark13": ["Author:", "Historical Context:"],
    "mark14": ["Author:", "Historical Context:"],
}

DROP = {
    "mark13": ["Mark 13:"],
    "mark14": ["Mark includes a unique detail:"],
}

META = {
"mark1": ("Gospel \u2014 Narrative",
  "A gospel that starts without a genealogy or a nativity, John in the wilderness, "
  "baptism and temptation compressed into five verses, four fishermen called at "
  "once, authority recognised before it is explained, and a healed leper whose "
  "talking shuts Jesus out of the towns"),
"mark13": ("Gospel \u2014 Prophetic Discourse",
  "A question prompted by admiration of the temple, deception named as the first "
  "danger, tribulation described as birth pangs rather than the end, the Son of Man "
  "coming in clouds, a day the Son himself does not know, and watchfulness as the "
  "whole practical application"),
"mark14": ("Gospel \u2014 Passion Narrative",
  "An anointing framed by a plot, betrayal named at the table, a cup and a covenant, "
  "Gethsemane prayed in Aramaic, a disciple who runs out of his clothes, the plainest "
  "claim to deity in the Gospel, and Peter warming himself at the enemy&#x27;s fire"),
}

SECTIONS = {
"mark1": [
  ("The Beginning of the Gospel (vv.1-8)",
   "Mark opens with a headline rather than a story: the beginning of the gospel of "
   "Jesus Christ, the Son of God. There is no genealogy and no nativity, which for a "
   "Roman audience removes exactly the material that would have mattered least. The "
   "quotation in vv.2-3 is a composite of Malachi and Isaiah although only Isaiah is "
   "named, a normal practice when citing a collection by its major prophet. John "
   "arrives already preaching, dressed like Elijah, and his own summary of himself is "
   "that he is not worthy to untie a sandal."),
  ("Baptism and Temptation in Five Verses (vv.9-13)",
   "What Matthew and Luke give paragraphs to, Mark gives sentences. The heavens are "
   "torn open \u2014 the verb is violent, the same one used of the temple veil at "
   "15:38 \u2014 the Spirit descends, the voice speaks. Then forty days of temptation "
   "in two verses with no dialogue reported, no three exchanges, no scripture quoted. "
   "Mark alone adds that he was \u201cwith the wild beasts\u201d, a detail that says "
   "wilderness rather than desert retreat."),
  ("The Time Is Fulfilled (vv.14-15)",
   "The first words of Jesus in this Gospel are a summary of everything after them: "
   "the time is fulfilled, the kingdom of God is at hand, repent ye, and believe the "
   "gospel. Two statements followed by two commands. Mark notes that this begins "
   "after John is put in prison, so the ministry starts as its forerunner's ends."),
  ("Calling Four Fishermen (vv.16-20)",
   "Two pairs of brothers, called in the middle of a working day. \u201cStraightway "
   "they forsook their nets\u201d is the first of the forty-odd uses of that word "
   "which give the book its pace. James and John leave their father in the boat with "
   "the hired servants, a detail Mark includes without comment. Nothing is said about "
   "prior acquaintance, though John 1 supplies it; Mark's interest is in the response "
   "rather than the reasoning."),
  ("Authority in the Synagogue (vv.21-28)",
   "The reaction in Capernaum is to the manner rather than the content: he taught as "
   "one having authority, and not as the scribes. Then a man with an unclean spirit "
   "identifies him correctly \u2014 the Holy One of God \u2014 which in Mark is a "
   "recurring irony, since the demons know what the disciples will spend fourteen "
   "chapters failing to grasp. He is silenced rather than thanked, the first instance "
   "of the pattern often called the messianic secret."),
  ("A Whole City at the Door (vv.29-34)",
   "The scene moves to Simon's house and his wife's mother, mentioned in passing and "
   "healed by being lifted up by the hand. By evening the whole city is gathered at "
   "the door, and Mark says he healed many, which is more careful than saying all. "
   "The demons are again forbidden to speak because they knew him."),
  ("Praying Before Day (vv.35-39)",
   "\u201cA great while before day\u201d he goes out to a solitary place to pray. "
   "Simon's report that everyone is looking for him reads like a summons back to a "
   "success, and the answer refuses it \u2014 let us go into the next towns, for "
   "therefore came I forth. Momentum in this chapter is repeatedly away from the "
   "crowd that has just formed."),
  ("The Leper Who Would Not Keep Quiet (vv.40-45)",
   "The leper's request is framed as a question of willingness, not ability, and the "
   "answer touches him before speaking. The instruction afterwards is emphatic, "
   "\u201csee thou say nothing to any man\u201d, and he publishes it everywhere. The "
   "consequence closes the chapter with an inversion: the man who was outside the "
   "town can now enter it, and Jesus can no more openly enter the city and stays in "
   "desert places."),
],
"mark13": [
  ("Not One Stone Upon Another (vv.1-2)",
   "The discourse begins with a disciple admiring the masonry, and Herod's temple "
   "genuinely was worth admiring \u2014 some of its stones weigh over forty tons. The "
   "reply concedes nothing to the architecture: not one stone shall be left upon "
   "another. Jerusalem fell in AD 70, within the lifetime of many who heard it, and "
   "the temple has never been rebuilt."),
  ("The Question on the Mount of Olives (vv.3-4)",
   "Mark alone names the four who ask \u2014 Peter, James, John and Andrew \u2014 and "
   "notes that it was private. Their question has two halves, when shall these things "
   "be and what shall be the sign, and the answer that follows addresses both without "
   "separating them cleanly. Much of the difficulty in reading this chapter comes from "
   "that, and the difficulty is in the text rather than in the interpreters."),
  ("Take Heed: Deceivers, Wars, and Birth Pangs (vv.5-13)",
   "The first instruction is not about signs but about being misled: take heed that "
   "no man deceive you. Wars, earthquakes and famines are explicitly labelled as not "
   "the end \u2014 they are \u201cthe beginnings of sorrows\u201d, a word for birth "
   "pangs, which implies something arriving rather than something collapsing. The "
   "warning turns personal in vv.9-13: councils, floggings, betrayal by family, and "
   "the promise that the Spirit will supply what to say."),
  ("The Abomination and the Flight (vv.14-23)",
   "\u201cWhen ye shall see the abomination of desolation\u201d carries a parenthesis "
   "addressed to the reader rather than the hearer \u2014 let him that readeth "
   "understand \u2014 one of the few places a Gospel breaks frame. The instructions "
   "are practical and urgent: do not go back for anything, pray it is not winter, and "
   "the specific compassion of v.17 for pregnant and nursing women. False christs "
   "will show signs, and the safeguard offered is that they have been told beforehand."),
  ("The Son of Man Coming in Clouds (vv.24-27)",
   "Sun darkened, moon without light, stars falling, powers shaken. The language is "
   "drawn from Isaiah and Joel, where it regularly accompanies the fall of nations, "
   "which is part of why readers differ over whether this describes AD 70, the end, or "
   "both. The Son of Man coming in clouds with great power is from Daniel 7, and the "
   "angels gather the elect from the four winds."),
  ("The Fig Tree and This Generation (vv.28-31)",
   "The fig tree's leaves indicate nearness, not a date, which is the point of the "
   "illustration. \u201cThis generation shall not pass\u201d is the hardest sentence "
   "in the chapter, and how it reads depends on whether \u201call these things\u201d "
   "means the fall of Jerusalem or the whole sequence. Verse 31 sets the reliability "
   "of the words above the permanence of heaven and earth."),
  ("No Man Knows the Day: Watch (vv.32-37)",
   "Mark 13:32 is unique in going as far as it does \u2014 not the angels, "
   "\u201cneither the Son, but the Father\u201d. It is among the strongest statements "
   "of genuine humanity in the Gospels, describing knowledge voluntarily not held in "
   "the incarnate state. What follows is the doorkeeper parable of vv.34-37, also "
   "found only in Mark: the master leaves, assigns work, and tells the doorkeeper to "
   "watch. \u201cWatch\u201d is the chapter's own word, at vv.5, 9, 33 and 37, and "
   "v.37 widens it past the four who asked \u2014 what I say unto you I say unto all."),
],
"mark14": [
  ("The Plot, and the Anointing at Bethany (vv.1-11)",
   "Mark frames the anointing between two halves of a conspiracy, a technique he uses "
   "repeatedly. The chief priests want him taken by craft but not during the feast; a "
   "woman breaks an alabaster box of spikenard worth a year's wages; Judas goes to the "
   "priests immediately afterwards. Some present call the act waste, and the defence "
   "given is that she has done what she could and has anointed him for burial "
   "beforehand \u2014 the only person in the chapter who acts as though he is really "
   "going to die."),
  ("The Passover Prepared (vv.12-21)",
   "The arrangements are oddly clandestine: a man carrying a pitcher of water, a "
   "signal rather than an address, since a man carrying water would have stood out "
   "where women normally did it. At the table the betrayal is announced without "
   "naming anyone, and the disciples respond one by one, \u201cis it I?\u201d. Verse "
   "21 holds both halves of the difficulty together \u2014 the Son of man goes as it "
   "is written of him, and woe to that man by whom he is betrayed."),
  ("This Is My Body (vv.22-26)",
   "Mark's account is the barest of the four: he took bread, blessed, broke, gave, "
   "and said take, eat, this is my body. The cup is called the blood of the new "
   "covenant shed for many, and they all drink of it before being told what it means. "
   "The last thing recorded before Gethsemane is that they sang a hymn, the Passover "
   "Hallel, on the way out."),
  ("Peter's Denial Predicted (vv.27-31)",
   "The scattering is quoted from Zechariah and the promise to go before them into "
   "Galilee is given in the same breath, so the prediction of failure comes attached "
   "to a plan for afterwards. Mark alone records the cock crowing twice, a detail his "
   "source would have remembered precisely. Peter's answer is emphatic and the others "
   "all say the same, which spreads the failure evenly across the room."),
  ("Gethsemane: Abba, Father (vv.32-42)",
   "\u201cSore amazed\u201d and \u201cvery heavy\u201d are unusually strong words, and "
   "Mark does not soften them. Only Mark preserves the Aramaic address: Abba, the "
   "family word a child used, kept in the original by a writer who translates almost "
   "everything else. The prayer asks for the cup to pass and then submits, and it is "
   "made three times. The disciples sleep three times, and the reason offered for them "
   "is that the spirit is willing while the flesh is weak."),
  ("The Arrest, and the Young Man Who Fled (vv.43-52)",
   "A kiss as the sign, a drawn sword and a severed ear, and a question about being "
   "taken as a thief when he sat daily teaching in the temple. Then the detail found "
   "only here: a young man following in a linen cloth who leaves the cloth in their "
   "hands and runs naked. It is widely taken as Mark's own signature in the "
   "narrative, an eyewitness placing himself at the scene in the least flattering way "
   "available."),
  ("Before the Sanhedrin: I Am (vv.53-65)",
   "The witnesses do not agree, which by their own law should have ended the "
   "proceedings, so the high priest asks directly: art thou the Christ, the Son of the "
   "Blessed? Mark's answer is the plainest in any Gospel \u2014 \u201cI am\u201d, the "
   "words of Exodus 3:14, where Matthew has the more oblique \u201cthou hast "
   "said\u201d. The torn robe and the charge of blasphemy follow at once. Through "
   "fourteen chapters of silencing demons and warning the healed, this is the moment "
   "the claim is made openly, and it is made to the men who will use it."),
  ("Peter Denies Him Three Times (vv.66-72)",
   "The two scenes are set side by side deliberately: inside, Jesus confessing under "
   "oath; outside, Peter denying while warming himself at the fire of the men holding "
   "him. The denials escalate from evasion to disavowal to cursing, and it is the "
   "second cockcrow that breaks him. \u201cHe went out, and wept\u201d closes the "
   "chapter, and Mark gives him nothing further here \u2014 the restoration waits "
   "until the young man at the tomb sends word to the disciples and Peter by name."),
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

        keep_order = KEEP[page]
        want_drop = DROP.get(page, [])
        fields, dropped, headless = {}, [], 0
        for m in re.finditer(r'<div class="auth-item">(.*?)</div>', pane.group(2), re.S):
            inner = m.group(1)
            lab = re.match(r'<span class="auth-label">([^<]*)</span>\s*', inner)
            name = lab.group(1).strip() if lab else None
            rest = inner[lab.end():].strip() if lab else inner.strip()
            if name in keep_order:
                fields[name] = rest
            elif name is not None and name in want_drop:
                dropped.append(name)
            elif name is None:
                headless += 1
            else:
                problems.append(f"{page}: unexpected field {name!r}")

        for want in keep_order:
            if want not in fields:
                problems.append(f"{page}: missing {want}")
        for want in want_drop:
            if want not in dropped:
                problems.append(f"{page}: expected to drop {want!r}, not found")
        if headless:
            notes.append(f"{page}: {headless} headless paragraph(s) folded into "
                         f"section prose")

        genre, themes = META[page]
        sections = SECTIONS[page]
        covered = set()
        for label, body in [("Key Themes", themes)] + \
                           [(f"section {h!r}", p) for h, p in sections]:
            stray = sorted({w for w in CAPS.findall(body) if w not in CAPS_OK})
            if stray:
                problems.append(f"{page}: emphatic capitals {stray} in {label}")
            if "*" in body:
                problems.append(f"{page}: markdown asterisk in {label}")
        for head, _ in sections:
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
        for want in keep_order:
            parts.append(ITEM.format(label=want, body=fields[want]) + "\n")
        parts.append(ITEM.format(label="Classification:", body=genre) + "\n")
        parts.append(ITEM.format(label="Key Themes:", body=themes) + "\n")
        for head, prose in sections:
            parts.append(ITEM.format(label=head + ":", body=prose) + "\n")
        new_body = "".join(parts) + "            </div>\n\n            "

        new = html[:pane.start(2)] + new_body + html[pane.end(2):]
        o, c = len(re.findall(r"<div\b", new)), len(re.findall(r"</div>", new))
        if o != c:
            problems.append(f"{page}: div imbalance {o} vs {c}")
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
