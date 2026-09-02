#!/usr/bin/env python3
"""
Completes Luke: chapters 1, 5, 6 and 10.

Luke 5, 6 and 10 are a shape not seen before. Each carries topical fields --
"The Miraculous Catch:", "The Paralytic:", "Levi's Calling:", "Sabbath
Controversies:", "The Twelve Chosen:", "Luke's Beatitudes and Woes:", "The
Seventy:", "The Good Samaritan:", "Mary and Martha:" -- which read like sections
whose verse ranges were never written. They are close to the target format and easy
to mistake for it, but they do not cover their chapters:

    luke5   three fields, leaving the leper (vv.12-16) and the question about
            fasting and wineskins (vv.33-39) with nothing
    luke6   three fields covering vv.1-26, leaving over half the Sermon on the
            Plain unaddressed (vv.27-49)
    luke10  three fields, leaving the woes on Chorazin and Bethsaida (vv.13-16)
            and the return of the seventy (vv.17-24) uncovered

So these are neither a relabelling job nor a blank page. Each field's substance is
carried into the section covering the same verses, and the missing sections are
written to close the gaps.

Luke 1 keeps its book-opening fields including "Unique to Luke:", which names the
Magnificat and the Benedictus. At 80 verses it is the longest chapter in the
Gospel and takes 8 sections.

Usage:
    python3 fold_luke.py [--check]
"""
import os
import re
import sys

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")

ITEM = ('                    <div class="auth-item">'
        '<span class="auth-label">{label}</span> {body}</div>')

VERSES = {"luke1": 80, "luke5": 39, "luke6": 49, "luke10": 42}

CAPS_OK = {"LORD", "GOD", "YHWH", "OT", "NT", "BC", "AD", "KJV", "ESV", "ASV", "AM"}

KEEP = {
    "luke1": ["Author:", "Date Written:", "Audience:", "Purpose:",
              "Chapter 1 Content:", "Unique to Luke:"],
    "luke5": ["Author:", "Historical Context:"],
    "luke6": ["Author:", "Historical Context:"],
    "luke10": ["Author:", "Historical Context:"],
}

# Topical fields whose content moves into the section covering the same verses.
DROP = {
    "luke5": ["The Miraculous Catch:", "The Paralytic:", "Levi&#x27;s Calling:"],
    "luke6": ["Sabbath Controversies:", "The Twelve Chosen:",
              "Luke&#x27;s Beatitudes and Woes:"],
    "luke10": ["The Seventy:", "The Good Samaritan:", "Mary and Martha:"],
}

META = {
"luke1": ("Gospel \u2014 Narrative",
  "The only Gospel to open with a formal preface, two annunciations set against each "
  "other, an old priest silenced for asking and a young girl commended for asking, "
  "two songs preserved nowhere else, and a naming that breaks with the family"),
"luke5": ("Gospel \u2014 Narrative",
  "A fisherman told his trade by a carpenter, conviction rather than delight as the "
  "response to power, a roof opened to reach Jesus, forgiveness offered before "
  "healing, a tax collector who throws a party, and new wine that will not go into "
  "old skins"),
"luke6": ("Gospel \u2014 Narrative and Discourse",
  "Two Sabbath confrontations, a night of prayer before choosing twelve men, "
  "blessings paired with woes found only here, poverty and hunger named without "
  "spiritualising, love of enemies as the distinguishing mark, and two builders "
  "distinguished by what they dug"),
"luke10": ("Gospel \u2014 Narrative and Parable",
  "Seventy sent ahead in pairs, towns held more accountable than Sodom, joy "
  "redirected from success to enrolment, a lawyer&#x27;s question turned back on him, "
  "a Samaritan made the hero, and one thing needful chosen over much serving"),
}

SECTIONS = {
"luke1": [
  ("A Preface Addressed to Theophilus (vv.1-4)",
   "Luke is the only Gospel to open like a work of history, with a formal dedication "
   "in a single long sentence of polished Greek. He acknowledges other accounts "
   "already in circulation, claims to have traced things from the first, and states "
   "his aim: that Theophilus might know the certainty of what he has been taught. The "
   "style changes abruptly at v.5 into something far more Semitic, which reads as "
   "deliberate \u2014 a Greek historian's preface followed by a narrative that sounds "
   "like the Old Testament."),
  ("Gabriel and Zacharias in the Temple (vv.5-25)",
   "The setting is priestly and precise: Zacharias of the course of Abia, chosen by "
   "lot to burn incense, an assignment most priests would receive once in a lifetime "
   "if at all. Both he and Elisabeth are described as righteous and as old, and their "
   "childlessness has already been long. Gabriel's announcement is met with a request "
   "for proof, and the sign given is muteness until it happens. Verse 25's "
   "\u201cthus hath the Lord dealt with me\u201d is Elisabeth's, and what she names is "
   "the removal of reproach rather than the gift of a son."),
  ("The Annunciation to Mary (vv.26-38)",
   "The second announcement is set against the first at every point. A rural town "
   "rather than the temple, a young woman rather than an old priest, and a question "
   "that sounds similar but is answered rather than penalised \u2014 Zacharias asked "
   "how he could know, Mary asks how it shall be. What she is told involves no "
   "precedent she can check. Her reply, \u201cbe it unto me according to thy "
   "word\u201d, is the model the chapter holds up, and Gabriel's closing line is that "
   "nothing shall be impossible."),
  ("Mary Visits Elisabeth (vv.39-45)",
   "Mary travels to the hill country and the recognition happens before she explains "
   "anything: the child leaps, Elisabeth is filled with the Holy Ghost, and she names "
   "Mary's condition without being told. Her blessing in v.45 is precisely aimed "
   "\u2014 blessed is she that believed \u2014 which is the contrast with her own "
   "husband, still unable to speak because he did not."),
  ("The Magnificat (vv.46-56)",
   "Mary's song is one of two passages in this chapter found nowhere else. It leans "
   "heavily on Hannah's prayer in 1 Samuel 2 and on the Psalms, and its subject is "
   "reversal: the proud scattered, the mighty put down, the humble exalted, the hungry "
   "filled and the rich sent away empty. The tenses treat these as already "
   "accomplished. For a girl in an occupied province, singing that thrones have been "
   "emptied is a considerable claim."),
  ("The Birth and Naming of John (vv.57-66)",
   "The neighbours assume the child will carry a family name and Elisabeth overrules "
   "them, which they refuse to accept from her. Zacharias is asked and writes "
   "\u201cHis name is John\u201d, and his speech returns immediately \u2014 the sign "
   "ends when the obedience is complete. The reaction spreads through the hill country "
   "as a question: what manner of child shall this be?"),
  ("The Benedictus (vv.67-79)",
   "The second song, and the first words of a man who has been silent nine months are "
   "not about his son but about God visiting and redeeming his people. Covenant "
   "language dominates \u2014 the oath to Abraham, the horn of salvation, the house of "
   "David. Only at v.76 does he turn to the child, and then only to describe him as "
   "the one going before. The closing image of the dayspring visiting those in darkness "
   "and the shadow of death is the chapter's last word on why any of it matters."),
  ("John in the Desert (v.80)",
   "A single verse covers roughly thirty years: the child grew, waxed strong in "
   "spirit, and was in the deserts till the day of his showing unto Israel. Luke, who "
   "has just spent seventy-nine verses on a few months, passes over three decades "
   "without comment, which says something about what he considers the story to be."),
],
"luke5": [
  ("The Miraculous Catch (vv.1-11)",
   "Peter was a professional who had fished all night and caught nothing, and the "
   "instruction to try again came from a carpenter. His answer \u2014 "
   "\u201cnevertheless at thy word I will let down the net\u201d \u2014 is obedience "
   "against his own experience rather than in the absence of it. The result breaks the "
   "nets and fills two boats, and what it produces in him is not delight but "
   "conviction: depart from me, for I am a sinful man. Encountering the power exposes "
   "him to himself, and only then comes the call to catch men."),
  ("The Leper Cleansed (vv.12-16)",
   "The leper's approach is a breach of the law he lives under, and his request "
   "concerns willingness rather than power. Jesus touches him, which no one else "
   "would, and the instruction afterwards is to tell no one but to go to the priest "
   "as Moses commanded. Luke, a physician, notes the man was \u201cfull of "
   "leprosy\u201d. The chapter then records what the crowds cost: he withdrew into "
   "the wilderness and prayed, which Luke mentions more often than the other Gospels "
   "do."),
  ("The Paralytic Let Down Through the Roof (vv.17-26)",
   "Four men carry a paralysed friend and, unable to get through the crowd, take him "
   "up and open the roof. What v.20 says Jesus saw was \u201ctheir faith\u201d, the "
   "carriers' as much as the patient's. Then the unexpected order of business: sins "
   "forgiven before legs healed, addressing what nobody in the room had asked about. "
   "The healing follows as evidence for the harder claim, and it is the first time in "
   "Luke that the charge of blasphemy is raised."),
  ("Levi Called, and a Party for Sinners (vv.27-32)",
   "Levi collected taxes for an occupying power, which made him wealthy and "
   "despised, and \u201che left all\u201d without recorded hesitation. What he does "
   "next is the part usually passed over: he throws a large feast and fills it with "
   "his own colleagues so they can meet Jesus. The complaint about the company is "
   "answered with the physician image \u2014 they that are whole need no physician "
   "\u2014 which is a statement about who the mission is for rather than a claim that "
   "anyone is well."),
  ("New Wine in Old Bottles (vv.33-39)",
   "The question about fasting is really a question about why his disciples do not "
   "look like John's. The answer is occasion rather than principle: no one fasts at a "
   "wedding while the bridegroom is present. Then two images with the same point "
   "\u2014 a patch from a new garment ruins both, and new wine bursts old skins. "
   "Verse 39's observation that no one who has drunk old wine wants new is a wry "
   "closing note on why the objection was raised at all."),
],
"luke6": [
  ("Sabbath Controversies (vv.1-11)",
   "Two incidents in succession, and both turn on the same claim. The disciples pluck "
   "grain as they walk, and the defence offered is David eating the shewbread "
   "\u2014 an argument from precedent \u2014 followed by something else entirely: the "
   "Son of man is Lord also of the sabbath. The second incident is a withered hand "
   "healed while they watch to see whether he will, and the question put to them first "
   "is whether it is lawful to do good on the sabbath. Verse 11's \u201cfilled with "
   "madness\u201d records the answer they gave."),
  ("A Night of Prayer, and the Twelve Chosen (vv.12-16)",
   "Luke alone notes that he continued all night in prayer before naming the twelve. "
   "The most consequential appointment of the ministry is preceded by the longest "
   "prayer Luke records, and the list that follows includes Simon called Zelotes and "
   "Judas Iscariot, described in the same breath as the man which also was the "
   "traitor. Nothing suggests the night of prayer was meant to avoid that."),
  ("Blessings and Woes (vv.17-26)",
   "Luke sets this sermon on level ground, which is why it is often called the Sermon "
   "on the Plain, and his version is shorter and blunter than Matthew's. \u201cBlessed "
   "be ye poor\u201d, not poor in spirit; hunger and weeping are named without "
   "qualification. The four woes that follow are found only here, aimed at the rich, "
   "the full, the laughing and the well-spoken-of. Pairing them with the blessings "
   "makes the passage a set of contrasts rather than a list of ideals."),
  ("Love Your Enemies (vv.27-38)",
   "The demands are concrete and unhedged: love your enemies, bless them that curse "
   "you, offer the other cheek, lend without expecting return. The reasoning in "
   "vv.32-34 is comparative \u2014 loving those who love you is what everyone does, so "
   "it distinguishes nothing. Mercy is grounded in God's own, and the closing image is "
   "commercial: good measure, pressed down, shaken together, running over. The measure "
   "you use is the measure you receive."),
  ("The Blind Guide, the Beam, and the Tree (vv.39-45)",
   "A short sequence of sayings about qualification to teach. A blind man cannot lead "
   "the blind, and a disciple does not rise above his master, so who does the teaching "
   "matters. The beam and the mote follow, with the order of operations stated plainly "
   "\u2014 remove your own first, and then you will see clearly enough to help. The "
   "tree and its fruit close the section: what a man says comes out of what he is."),
  ("Two Builders and the Rock (vv.46-49)",
   "The sermon ends on the gap between calling him Lord and doing what he says. "
   "Luke's version of the two builders differs from Matthew's in a telling way: the "
   "wise builder digs deep and lays a foundation on rock, so the difference is effort "
   "that is invisible until the flood arrives. Both houses face the same water. Only "
   "the excavation distinguishes them."),
],
"luke10": [
  ("The Seventy Sent Two by Two (vv.1-12)",
   "Seventy are sent ahead in pairs, and manuscripts differ over whether the number "
   "is seventy or seventy-two \u2014 it may echo the seventy nations of Genesis 10 or "
   "the seventy elders of Numbers 11. Either way the mission has widened beyond the "
   "twelve, which is Luke's recurring interest. The instructions are spare: no purse, "
   "no scrip, no shoes, greet no one on the road, stay in one house, eat what is set "
   "before you. The harvest is called great and the labourers few, and what they are "
   "told to pray for is more workers rather than success."),
  ("Woe to Chorazin and Bethsaida (vv.13-16)",
   "The woes are aimed not at notorious cities but at towns that had seen the most "
   "and responded least. Tyre and Sidon would have repented, and Sodom is invoked as "
   "the comparison Capernaum comes out worse against. The principle is that "
   "accountability tracks what was witnessed. Verse 16 ties the messengers to the "
   "sender \u2014 he that despises you despises me \u2014 which is why the reception "
   "of seventy unnamed disciples carries this weight."),
  ("The Seventy Return; Rejoice Rather (vv.17-24)",
   "They come back elated that the devils were subject to them, and the reply "
   "redirects the joy rather than dampening it: rejoice not that the spirits are "
   "subject, but that your names are written in heaven. Success in the work is a worse "
   "foundation for joy than enrolment in it. What follows is one of the few places "
   "Luke records Jesus rejoicing, and its subject is that these things were hidden "
   "from the wise and revealed to babes."),
  ("The Good Samaritan (vv.25-37)",
   "The lawyer's second question, \u201cwho is my neighbour?\u201d, is an attempt to "
   "draw a boundary, and the parable answers by making the question unanswerable in "
   "those terms. A priest and a Levite pass by; the man who stops is a Samaritan, the "
   "most despised figure available to that audience, which is the whole force of the "
   "choice. The care described is expensive and open-ended \u2014 oil, wine, his own "
   "beast, two pence and a promise to return. The closing question reverses the "
   "lawyer's: not who qualifies as my neighbour, but which of these was one."),
  ("Mary and Martha (vv.38-42)",
   "Martha is \u201ccumbered about much serving\u201d and her complaint is "
   "reasonable, which is what makes the passage difficult. The distraction is caused "
   "by good work rather than bad. Mary sat at his feet and heard his word, the posture "
   "of a disciple, which in that setting was not the expected place for a woman. The "
   "answer names one thing needful without condemning service, and Luke places this "
   "immediately after the Samaritan \u2014 a parable about doing, then a scene about "
   "listening, set side by side."),
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
        if dropped:
            notes.append(f"{page}: {len(dropped)} topical field(s) carried into the "
                         f"sections covering the same verses")
        if headless:
            problems.append(f"{page}: {headless} unexpected headless item(s)")

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
