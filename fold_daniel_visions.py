#!/usr/bin/env python3
"""
Completes Daniel: chapters 7, 8, 10, 11 and 12, the vision half.

Three more inherited overlaps, all fixed. The skeletons double-counted a verse in
each case:

    daniel8   "The Goat (vv.5-8)" and "The Great Horn Broken (v.8)"
    daniel10  "Strengthened to Hear (vv.10-14)" and "Spiritual Warfare (vv.13-14)"
    daniel12  "Time Markers (vv.11-12)" and "Blessed Is He That Waiteth (v.12)"

With daniel4 in the previous batch and Lamentations 3 before that, five overlapping
skeletons have now been caught by the guard. The pattern looks like a sub-point being
promoted to a sibling heading, which produces prose that reads fine and a structure
that claims the same verse twice.

Capitals normalised: HEAVEN, BEASTS, HEBREW, DETAILS, CLEARER. All ordinary emphasis.

Usage:
    python3 fold_daniel_visions.py [--check]
"""
import os
import re
import sys

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")

ITEM = ('                    <div class="auth-item">'
        '<span class="auth-label">{label}</span> {body}</div>')

VERSES = {"daniel7": 28, "daniel8": 27, "daniel10": 21, "daniel11": 45,
          "daniel12": 13}

CAPS_OK = {"LORD", "GOD", "YHWH", "OT", "NT", "BC", "AD", "KJV", "ESV", "ASV",
           "AM", "II", "IV", "MENE", "TEKEL", "UPHARSIN"}

KEEP = ["Author:", "Classification:", "Key Themes:", "Historical Context:"]

NORMALISE = {"HEAVEN": "heaven", "BEASTS": "beasts", "HEBREW": "Hebrew",
             "DETAILS": "details", "CLEARER": "clearer"}

SECTIONS = {
"daniel7": [
  ("Four Beasts Out of the Sea (vv.1-8)",
   "The chapter covers the same ground as chapter 2 from the other side. Nebuchadnezzar "
   "saw an impressive statue of precious metals; Daniel sees predators coming up out of "
   "a churning sea. Where a king saw magnificence, heaven shows appetite. The four are "
   "commonly read as Babylon, Medo-Persia, Greece and Rome, and the fourth is not "
   "compared to any animal at all -- dreadful and terrible, with iron teeth and ten "
   "horns, among which a little horn comes up with eyes and a mouth speaking great "
   "things."),
  ("The Ancient of Days Takes His Seat (vv.9-12)",
   "The scene shifts from sea to courtroom without transition. Thrones are set, the "
   "Ancient of Days sits, his garment white as snow and his throne a fiery flame, and "
   "the books are opened. Ten thousand times ten thousand stand before him. The beast "
   "that had been speaking great words is simply dealt with, and the others have their "
   "dominion taken but their lives prolonged for a season. Judgment here is procedural "
   "rather than violent."),
  ("One Like the Son of Man (vv.13-14)",
   "Two verses that carry more weight in the New Testament than almost anything else in "
   "the Old. One like the Son of man comes with the clouds of heaven to the Ancient of "
   "Days and is given dominion, glory and a kingdom that shall not pass away. This is "
   "where Jesus's preferred self-designation comes from, and when he told Caiaphas he "
   "would see the Son of man coming in the clouds he was quoting this verse. The high "
   "priest tore his robes, which shows he recognised the claim exactly."),
  ("Daniel Troubled; the Interpretation Asked (vv.15-18)",
   "Daniel's spirit is grieved and the visions trouble him, so he asks one of those "
   "standing by. The answer given first is the short version: four kings shall arise, "
   "and the saints of the most High shall possess the kingdom for ever. The summary "
   "comes before the detail, which means the outcome is settled before the difficulties "
   "are explained."),
  ("The Fourth Beast and the Little Horn (vv.19-25)",
   "Daniel wants to know about the fourth beast specifically, and the answer is the most "
   "debated passage in the book. The little horn speaks great words against the most "
   "High, wears out the saints, and thinks to change times and laws, and they are given "
   "into his hand for a time and times and the dividing of time -- generally read as "
   "three and a half years. Antiochus Epiphanes and various Roman emperors have been "
   "proposed as partial fulfilments, with many taking the full reference to be the "
   "Antichrist."),
  ("The Kingdom Given to the Saints (vv.26-28)",
   "The judgment sits, the dominion is taken away, and the kingdom under the whole "
   "heaven is given to the people of the saints of the most High. The chapter ends on "
   "Daniel's own condition rather than on triumph: my cogitations much troubled me, my "
   "countenance changed, but I kept the matter in my heart. He has just been told his "
   "side wins and it does not settle him."),
],
"daniel8": [
  ("The Ram with Two Horns (vv.1-4)",
   "The vision comes in Belshazzar's third year, and the language returns to Hebrew "
   "after six chapters of Aramaic. A ram with two horns, one higher than the other, "
   "pushes west, north and south with nothing able to stand before it. The two horns are "
   "Media and Persia, with Persia the later and higher of the two, which the "
   "interpretation confirms at v.20."),
  ("The Goat from the West, and the Broken Horn (vv.5-8)",
   "A he goat comes from the west with a notable horn between his eyes and touches not "
   "the ground -- speed is the whole point of the image, and Alexander crossed from "
   "Macedonia to the Indus in roughly ten years. He breaks the ram's two horns and none "
   "can deliver it. Then the great horn is broken at the height of its strength, "
   "Alexander dying at thirty-two, and four horns come up in its place: Cassander in "
   "Macedonia, Lysimachus in Thrace, Seleucus in Syria and Ptolemy in Egypt."),
  ("The Little Horn and the Trampled Sanctuary (vv.9-12)",
   "Out of one of the four comes a little horn that grows toward the pleasant land, "
   "magnifies itself against the host of heaven, takes away the daily sacrifice and "
   "casts down the place of the sanctuary. From the Seleucid line came Antiochus IV "
   "Epiphanes, who set a statue of Zeus on the altar in Jerusalem, sacrificed a pig "
   "there and banned the Torah. The prophecy's targets are the sanctuary and the "
   "sacrifice rather than the nation's borders."),
  ("How Long? Two Thousand Three Hundred Days (vv.13-14)",
   "The question is asked by one holy one to another rather than by Daniel: how long "
   "shall be the vision concerning the daily sacrifice and the transgression of "
   "desolation? The answer, two thousand three hundred days, then the sanctuary shall be "
   "cleansed. Whether those are days or half-days, and how they map onto the Maccabean "
   "restoration of the temple in 164 BC, is argued -- but the terminus is cleansing "
   "rather than destruction."),
  ("Gabriel Interprets; Daniel Faints (vv.15-27)",
   "Gabriel is named here, one of only two places in the Old Testament, the other being "
   "9:21. He identifies the ram and the goat outright as Media-Persia and Greece, then "
   "describes a king of fierce countenance who destroys by policy and stands up against "
   "the Prince of princes before being broken without hand. That Gabriel says the vision "
   "is for the time of the end while describing a second-century king is why many read "
   "Antiochus as both a historical figure and a pattern. The chapter closes with Daniel "
   "fainting and sick for days, and no one to explain it to."),
],
"daniel10": [
  ("Three Full Weeks of Mourning (vv.1-3)",
   "The setting is the third year of Cyrus, so the first exiles have already gone home. "
   "Daniel mourns and fasts twenty-one days, eating no pleasant bread and no flesh or "
   "wine. Ezra 4 records Persian officials blocking the temple rebuilding around this "
   "time, which is the most likely thing weighing on him. The prayer is sustained rather "
   "than occasional, and the length matters for what v.13 will reveal."),
  ("The Man Clothed in Linen (vv.4-9)",
   "The figure by the Tigris is described in terms that reappear almost item for item in "
   "Revelation 1:13-15 -- linen garment, gold about the loins, body like beryl, face as "
   "lightning, eyes as lamps of fire, voice as a multitude. Whether this is a "
   "Christophany or a high angel is genuinely disputed, partly because the figure in "
   "v.13 needs Michael's help. Daniel's companions see nothing but flee, and he is left "
   "with no strength and his face to the ground."),
  ("From the First Day Thy Words Were Heard (vv.10-14)",
   "A hand touches him and the explanation given is the most striking thing in the "
   "chapter: from the first day thou didst set thine heart to understand, thy words were "
   "heard. The answer left immediately and took twenty-one days to arrive, because the "
   "prince of the kingdom of Persia withstood it until Michael came. So the fast's "
   "length was not God's reluctance but a delay in transit, and territorial powers "
   "opposing God's purposes are introduced almost in passing."),
  ("Strengthened Twice, and Told to Be Strong (vv.15-19)",
   "Daniel is dumb and without strength, and is touched and strengthened twice over. The "
   "words spoken to him are the ones given to frightened people throughout Scripture: "
   "fear not, peace be unto thee, be strong. Only after the second strengthening can he "
   "say speak, for thou hast strengthened me. The passage takes the physical cost of "
   "revelation seriously rather than treating it as incidental."),
  ("The Prince of Persia, and Michael (vv.20-21)",
   "The messenger says he must return to fight with the prince of Persia, and that the "
   "prince of Greece will come after -- so the conflict is ongoing and follows the same "
   "succession of empires the visions describe. Michael is named as Israel's own prince, "
   "and the messenger says none holds with him in this but Michael. Two verses that "
   "reframe everything in chapters 11 and 12 as the visible half of something else."),
],
"daniel11": [
  ("Persia and the Mighty King of Greece (vv.1-4)",
   "The prophecy opens with four more kings of Persia, the fourth far richer than the "
   "rest, and then a mighty king who rules with great dominion -- Alexander, though "
   "unnamed. His kingdom is broken and divided toward the four winds of heaven and not "
   "to his posterity, which is what happened: no heir, four generals. The compression "
   "here is extreme, four verses for two centuries, before the pace slows sharply."),
  ("Kings of the South and North (vv.5-20)",
   "What follows is the most detailed sustained prophecy in the Old Testament, and every "
   "verse from 2 to 35 corresponds to verifiable events between roughly 535 and 164 BC. "
   "The king of the south is Ptolemaic Egypt, the king of the north Seleucid Syria, and "
   "Judah sits between them as a buffer fought over repeatedly. Marriages made as "
   "alliances and then failing, campaigns, betrayals and a daughter given to be "
   "destroyed are all named without names. The precision is why some scholars date the "
   "chapter after the events."),
  ("A Vile Person Rises by Flattery (vv.21-24)",
   "The focus narrows to one figure who obtains the kingdom not by right but by "
   "flatteries, and Antiochus IV Epiphanes did exactly that, taking the Seleucid throne "
   "past the legitimate heir. He works by peaceable means and deceit rather than open "
   "war at first, and scatters spoil among his followers. The description is of political "
   "method rather than military strength."),
  ("Rage Against the Holy Covenant (vv.25-35)",
   "The campaigns against Egypt are described in sequence, including the second one "
   "turned back -- historically by a Roman envoy drawing a line in the sand at "
   "Alexandria -- after which he returns in fury against the holy covenant. The daily "
   "sacrifice is taken away and the abomination that maketh desolate set up. Verses "
   "32-35 note that some are corrupted by flatteries while those who know their God are "
   "strong and instruct many, and that some of them fall, to purge and make them white. "
   "Faithfulness here includes casualties."),
  ("The King Who Magnifies Himself (vv.36-39)",
   "From v.36 the language exceeds anything Antiochus did. This king magnifies himself "
   "above every god, speaks marvellous things against the God of gods, regards neither "
   "the God of his fathers nor the desire of women, and honours a god his fathers knew "
   "not. Where exactly the transition happens is debated, and the text gives no marker. "
   "Most read it as moving from Antiochus to a figure he prefigures."),
  ("The Time of the End (vv.40-45)",
   "The final movement is a campaign at the time of the end: the king of the south "
   "pushing, the king of the north sweeping through countries, entering the glorious "
   "land, and planting the tabernacles of his palace between the seas and the holy "
   "mountain. The last clause is the point of the whole chapter -- yet he shall come to "
   "his end, and none shall help him. Nothing in vv.40-45 matches Antiochus's actual "
   "death in Persia, which is part of the case for reading it as still future."),
],
"daniel12": [
  ("Michael Stands Up (v.1)",
   "Michael, introduced in chapter 10 as Israel's prince, now stands up -- no longer "
   "assisting but acting. What accompanies it is a time of trouble such as never was "
   "since there was a nation. And in the same verse, deliverance: every one found "
   "written in the book shall be delivered. The worst distress and the certainty of "
   "rescue are stated together rather than in sequence."),
  ("Many Shall Awake: Two Eternities (v.2)",
   "The clearest statement of bodily resurrection in the Old Testament. Job hints at it "
   "and Isaiah 26:19 proclaims it, but this verse specifies both outcomes -- some to "
   "everlasting life, some to shame and everlasting contempt -- and both from the dust "
   "of the earth. That it says many rather than all has been read as a selective or "
   "staged resurrection. The Sadducees would later deny the doctrine entirely, which "
   "makes its presence here notable."),
  ("They That Be Wise Shall Shine (v.3)",
   "The wise shine as the brightness of the firmament, and they that turn many to "
   "righteousness as the stars for ever. The word rendered wise is the same used in "
   "11:33 of those who instruct many during the persecution, so the promise is addressed "
   "to the people the previous chapter said would fall. Their reward is described in "
   "terms of light and duration, the two things the persecution took from them."),
  ("Seal the Book Until the Time of the End (v.4)",
   "Daniel is told to shut up the words and seal the book, and that many shall run to "
   "and fro and knowledge shall be increased. The sealing suggests these prophecies "
   "would grow clearer as their fulfilment approached. Revelation 22:10 gives the "
   "deliberate reverse -- seal not the sayings of this book, for the time is at hand. "
   "Daniel seals and John unseals."),
  ("How Long? A Time, Times and an Half (vv.5-13)",
   "Two figures on the riverbanks and the man in linen above the water, and the question "
   "asked again: how long to the end of these wonders? The answer is a time, times and "
   "an half, and that when the scattering of the holy people is finished, all these "
   "things shall be finished. Daniel asks and is told plainly that he will not "
   "understand -- go thy way, for the words are closed up and sealed. The numbers 1,290 "
   "and 1,335 follow without explanation. The book ends personally rather than "
   "cosmically: go thou thy way till the end be, for thou shalt rest, and stand in thy "
   "lot at the end of the days."),
],
}

CAPS = re.compile(r"\b[A-Z]{2,}\b")


def main():
    check = "--check" in sys.argv
    problems, notes, planned = [], [], {}

    for page in sorted(VERSES, key=lambda s: int(s[6:])):
        path = os.path.join(DOCS, f"{page}.html")
        html = open(path, encoding="utf-8").read()
        pane = re.search(r'(id="tab-authorship">)(.*?)(?=<div class="tab-content")',
                         html, re.S)
        if not pane:
            problems.append(f"{page}: no authorship pane")
            continue

        fields, extra = {}, []
        for m in re.finditer(r'<div class="auth-item">(.*?)</div>', pane.group(2), re.S):
            inner = m.group(1)
            lab = re.match(r'<span class="auth-label">([^<]*)</span>\s*', inner)
            name = lab.group(1).strip() if lab else None
            rest = inner[lab.end():].strip() if lab else inner.strip()
            if name in KEEP:
                fields[name] = rest
            elif name is None and rest == "Structure:":
                pass
            elif name is None:
                extra.append(rest)
            else:
                problems.append(f"{page}: unexpected field {name!r}")

        for want in KEEP:
            if want not in fields:
                problems.append(f"{page}: missing {want}")
        if extra:
            fields["Historical Context:"] = " ".join(
                [fields["Historical Context:"]] + extra).strip()
            notes.append(f"{page}: {len(extra)} headless paragraph(s) merged")

        for want in KEEP:
            for bad, good in NORMALISE.items():
                if re.search(rf"\b{bad}\b", fields[want]):
                    fields[want] = re.sub(rf"\b{bad}\b", good, fields[want])
                    notes.append(f"{page}: {want} {bad}->{good}")

        sections = SECTIONS[page]
        covered = set()
        for want in KEEP:
            stray = sorted({w for w in CAPS.findall(fields[want]) if w not in CAPS_OK})
            if stray:
                problems.append(f"{page}: capitals {stray} still in {want}")
        for head, body in sections:
            stray = sorted({w for w in CAPS.findall(body) if w not in CAPS_OK})
            if stray:
                problems.append(f"{page}: capitals {stray} in {head!r}")
            if "*" in body:
                problems.append(f"{page}: markdown asterisk in {head!r}")
            if not re.search(r"\(vv?\.[\d]+[a-z]?(?:[-,:\s]+[\d]+[a-z]?)*\)$", head):
                problems.append(f"{page}: {head!r} does not end with its verse range")
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
