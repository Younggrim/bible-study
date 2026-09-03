#!/usr/bin/env python3
"""
Ezekiel 20 to 23: the history of rebellion, the sword song, and the two sisters. Four
pages, 161 verses. ezekiel24 is already folded, which is why this block stops at 23.

All four inherited sublists are gapless outlines and are folded. Three of these chapters
are among the hardest in the book to write notes for honestly. 20:25 says God gave
statutes that were not good, and the section on it names the standard reading without
pretending the difficulty is thereby removed. 21:8-17 is a poem celebrating a sword, and
saying so is more useful than paraphrasing it into something calmer. Chapter 23 is the
second of the two extended marital metaphors and it is coarser than chapter 16; the note
says what the imagery is doing and where the political history sits underneath it.

Chapter 22 ends on the sentence the whole first half of the book has been building
toward, I sought for a man among them that should make up the hedge, and stand in the
gap before me for the land, but I found none.

Usage:
    python3 fold_ezekiel_history.py [--check]
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
"ezekiel20": [
 ("The Elders Come, and Get No Answer (vv.1-4)",
  "The date is the seventh year, fifth month, tenth day, and the occasion is a delegation, certain of "
  "the elders of Israel came to enquire of the LORD, and sat before me. The refusal is put under "
  "oath, as I live, saith the Lord GOD, I will not be enquired of by you. What they get instead of "
  "an oracle is a history of their own nation told as a sequence of rebellions, cause them to know "
  "the abominations of their fathers, and that history is the rest of the chapter."),
 ("Rebellion in Egypt (vv.5-9)",
  "The account starts earlier than Exodus does. In the day when I chose Israel, before the exodus, "
  "the instruction given was cast away every man the abominations of his eyes, and defile not "
  "yourselves with the idols of Egypt, and the response was refusal, they rebelled against me, and "
  "would not hearken. No such episode appears in Exodus, which begins the story of Israel's "
  "unfaithfulness at the golden calf. What restrains the judgment is stated here and repeated at "
  "every stage of the chapter, but I wrought for my name's sake, that it should not be polluted "
  "before the heathen. God's reputation, not Israel's merit, is the chapter's actual subject."),
 ("The First Wilderness Generation (vv.10-17)",
  "The statutes are given with a purpose attached, which if a man do, he shall even live in them, and "
  "one sign is singled out and named three times in this chapter, also I gave them my sabbaths, to "
  "be a sign between me and them. The rebellion is described in the same terms, they walked not in "
  "my statutes, and they polluted my sabbaths. Sentence is announced and then withheld, nevertheless "
  "mine eye spared them from destroying them, neither did I make an end of them in the wilderness, "
  "and again the reason given is the name and not the people."),
 ("The Second Generation, and Statutes That Were Not Good (vv.18-26)",
  "The children are told walk ye not in the statutes of your fathers, and they rebel in the same way, "
  "so the pattern is shown to be generational rather than accidental. Then verses 25 and 26, which "
  "are the hardest in the chapter: wherefore I gave them also statutes that were not good, and "
  "judgments whereby they should not live, and I polluted them in their own gifts, in that they "
  "caused to pass through the fire all the firstborn. The reading most commentators take is that "
  "they were handed over to the practices they had already chosen, in the way Romans 1 describes God "
  "giving people up to what they wanted. That reading is reasonable and the text still says it more "
  "starkly than the reading does, and it is better to leave the difficulty visible than to "
  "paraphrase it away."),
 ("Rebellion in the Land (vv.27-29)",
  "The last of the four rebellions happens after the promise is kept, when I had brought them into "
  "the land, and it is described as opportunistic, they saw every high hill, and all the thick trees, "
  "and they offered there their sacrifices. The closing question carries a pun that survives "
  "translation only if it is pointed out, what is the high place whereunto ye go, and the name "
  "whereof is called Bamah unto this day. Bamah is simply the Hebrew word for high place, so the "
  "shrine is named after the thing it is, which is the chapter's way of saying the practice never "
  "had a better justification than itself."),
 ("And Ye Do the Same (vv.30-32)",
  "The history closes by turning on the delegation that prompted it, are ye polluted after the manner "
  "of your fathers, and shall I be enquired of by you. The last verse quotes something the exiles "
  "were evidently prepared to say out loud, and it is the most candid line in the chapter, ye say, "
  "We will be as the heathen, as the families of the countries, to serve wood and stone. Assimilation "
  "is being proposed as a policy, not drifted into."),
 ("The Second Exodus, and the Purge (vv.33-38)",
  "The reply borrows the vocabulary of the exodus and turns it toward the future, with a mighty hand, "
  "and with a stretched out arm, and with fury poured out, will I rule over you. The route is the "
  "same as the first time, out from the people, gathered out of the countries, and into the "
  "wilderness of the people, where there will I plead with you face to face. The image for the "
  "sorting is a shepherd's, I will cause you to pass under the rod, and the outcome is stated in two "
  "directions at once, I will bring you into the bond of the covenant, and I will purge out from "
  "among you the rebels."),
 ("Accepted on the Holy Mountain (vv.39-44)",
  "Verse 39 reads as a dismissal, go ye, serve ye every one his idols, and then the chapter reverses "
  "completely, for I will accept you with your sweet savour in the mountain of the height of Israel. "
  "What that acceptance produces is not relief but recognition, and the order matters, ye shall "
  "remember your ways, and all your doings, wherein ye have been defiled, and ye shall lothe "
  "yourselves in your own sight. And the ground of the whole thing is stated one last time in the "
  "same words the chapter has used at every stage, when I have wrought with you for my name's sake, "
  "not according to your wicked ways."),
 ("The Fire in the Forest of the South (vv.45-49)",
  "A short separate oracle, and in the Hebrew Bible it is numbered as the opening of chapter 21, "
  "which is why chapter divisions differ here between translations. Set thy face toward the south, "
  "and prophesy against the forest of the south field, and the fire in it will devour every green "
  "tree in thee, and every dry tree, which makes no distinction at all. Then the only recorded "
  "reaction of Ezekiel's audience to his manner, reported by the prophet himself as a complaint, Ah "
  "Lord GOD, they say of me, Doth he not speak parables. Chapter 21 answers it by saying the same "
  "thing again with the metaphor removed."),
],
"ezekiel21": [
 ("A Sword Drawn Out of Its Sheath (vv.1-7)",
  "This is the previous chapter's fire restated without the figure, which is a direct answer to the "
  "complaint that closed it. Set thy face toward Jerusalem, and prophesy against the land of Israel, "
  "and the instrument is named, I will draw forth my sword out of his sheath. The clause that gives "
  "the oracle its edge refuses any sorting, and will cut off from thee the righteous and the wicked. "
  "The prophet is then given a sign to perform with his body, sigh with the breaking of thy loins, "
  "and with bitterness, and a line to use when he is asked why, for the tidings, because it cometh."),
 ("The Song of the Sword (vv.8-17)",
  "What follows is a poem, and recognising the genre is the only way to read it. A sword, a sword is "
  "sharpened, and also furbished, it is sharpened to make a sore slaughter, it is furbished that it "
  "may glitter. The lines repeat with variation the way a chant does, and the prophet is told to "
  "perform it, cry and howl, smite therefore upon thy thigh, smite thine hands together, and let the "
  "sword be doubled the third time. It is among the most violent passages in the prophets and its "
  "violence is formal as well as descriptive: judgment set to music, which is harder to sit through "
  "than judgment announced."),
 ("Nebuchadnezzar at the Parting of the Way (vv.18-23)",
  "The prophet is told to mark out two roads from one starting point and let the sword of the king of "
  "Babylon come, one road to Rabbath of the Ammonites and one to Jerusalem. What happens at the "
  "junction is the fullest account of Babylonian divination anywhere in the Bible: he made his arrows "
  "bright, that is, belomancy, marking and casting arrows; he consulted with images; and he looked in "
  "the liver, hepatoscopy, reading the markings of a sacrificial animal's liver. The divination comes "
  "up Jerusalem. The oracle's judgment on the method is dismissive and its judgment on the outcome is "
  "not, it shall be as a false divination unto them, but he will call to remembrance the iniquity."),
 ("The Crown Removed (vv.24-27)",
  "Addressed to the reigning king as thou profane wicked prince of Israel, whose day is come, and the "
  "order given is dismantling, remove the diadem, and take off the crown, this shall not be the same. "
  "Then the line the passage is known for, I will overturn, overturn, overturn it, and it shall be no "
  "more, three times, matching the doubled and tripled sword of the earlier song. And a clause that "
  "leaves the office vacant rather than abolished, until he come whose right it is, and I will give "
  "it him, which picks up the wording of Genesis 49:10 and has been read in both Jewish and Christian "
  "tradition as pointing past the monarchy to a legitimate claimant."),
 ("The Sword Against Ammon (vv.28-32)",
  "The sword that chose the Jerusalem road at the crossroads is not thereby finished with Ammon. The "
  "charge against them is their reproach, that is, what they said about Judah's fall, which is the "
  "accusation chapter 25 opens the foreign oracles with. Their sentence is stated in the currency "
  "this book uses for nations, thou shalt be no more remembered, and it is set against Judah's, which "
  "leaves an office standing empty for someone to fill."),
],
"ezekiel22": [
 ("The Bloody City, and Her Sins Catalogued (vv.1-16)",
  "Wilt thou judge the bloody city, yea, thou shalt shew her all her abominations. What follows is "
  "the most systematic indictment in Ezekiel, and it is organised by relationship rather than by "
  "severity: princes shedding blood, father and mother set light by, the stranger oppressed, the "
  "fatherless and the widow vexed, holy things despised, sabbaths profaned, men carrying tales in "
  "order to get someone killed, eating upon the mountains, a father's nakedness uncovered, a woman "
  "approached in her separation, a neighbour's wife, a sister, a daughter-in-law, gifts taken to shed "
  "blood, usury and increase. Nearly every item corresponds to a specific statute in Leviticus 18 to "
  "20, so the passage reads as a charge sheet drawn point by point from the law. The summary is one "
  "clause, and thou hast forgotten me, saith the Lord GOD."),
 ("The Furnace, and Israel as Dross (vv.17-22)",
  "The house of Israel is to me become dross, all they are brass, and tin, and iron, and lead, in the "
  "midst of the furnace, they are even the dross of silver. The metallurgy is exact: these are the "
  "base metals that separate out and are skimmed off, and silver is the thing they are not. Then the "
  "gathering, as they gather silver, and brass, and iron, and lead, and tin into the midst of the "
  "furnace, to blow the fire upon it, to melt it, so will I gather you in mine anger. What is missing "
  "from the end of the image is the point of it. The refining process is described in full and no "
  "purified metal is named as coming out of it."),
 ("Every Class Indicted, and No Man in the Gap (vv.23-31)",
  "The last oracle in the chapter takes the leadership apart by function. The prophets are like a "
  "roaring lion, daubing with untempered mortar as in chapter 13. The priests have violated my law, "
  "and the charge against them is a failure of discrimination, they have put no difference between "
  "the holy and profane, neither have they shewed difference between the unclean and the clean, which "
  "is precisely the job. The princes are wolves ravening the prey. The people of the land have used "
  "oppression, and vexed the poor and needy. Then the closing verse, which is the bleakest sentence "
  "in the first half of the book, I sought for a man among them, that should make up the hedge, and "
  "stand in the gap before me for the land, that I should not destroy it, but I found none. Abraham "
  "stood in that position for Sodom and Moses for Israel at Sinai. The office is described as vacant."),
],
"ezekiel23": [
 ("Two Sisters, One Mother (vv.1-4)",
  "There were two women, the daughters of one mother, and they committed whoredoms in Egypt, so the "
  "allegory begins where chapter 20 began, before the exodus. The names are then given and decoded, "
  "Samaria is Aholah, and Jerusalem Aholibah, spelled Oholah and Oholibah in most modern "
  "translations. Both are built on the Hebrew word for tent, and the usual reading is she has a tent "
  "of her own for the northern kingdom and my tent is in her for Jerusalem, which draws the "
  "distinction the chapter will work with: one sister had an unauthorised sanctuary and the other had "
  "the real one and used it no better."),
 ("Aholah and Her Assyrian Lovers (vv.5-10)",
  "The northern kingdom's history is told in one paragraph. She doted on the Assyrians her "
  "neighbours, and they are described the way an ally looks when you want one, captains and rulers "
  "clothed with blue, all of them desirable young men, horsemen riding upon horses. The judgment is "
  "handed to the same parties, wherefore I delivered her into the hand of her lovers, and it is "
  "reported as completed, they took her sons and her daughters, and slew her with the sword. Samaria "
  "fell to Assyria in 722 BC, over a century before this was written, so this section is not a "
  "prediction. It is the precedent the rest of the chapter argues from, and it is stated in the past "
  "tense for that reason."),
 ("Aholibah, Worse Than Her Sister (vv.11-21)",
  "She saw all this, and the verdict on what she did with the knowledge is comparative, she was more "
  "corrupt in her inordinate love than she, and in her whoredoms more than her sister. The "
  "attachments are listed in order: the Assyrians, then the Chaldeans, whose images she saw portrayed "
  "upon the wall with vermilion, girded with girdles and dyed attire, and to whom she sent messengers "
  "into Chaldea, and then back to Egypt again. Underneath the metaphor is Judah's actual foreign "
  "policy from Ahaz to Zedekiah, swinging between Assyria, Babylon and Egypt as each looked stronger, "
  "and the book treats every swing as the same act: a small state buying security from whoever has "
  "it, having been told where its security was."),
 ("The Sentence on Aholibah (vv.22-35)",
  "I will raise up thy lovers against thee, and the list of them is deliberately long, the "
  "Babylonians, and all the Chaldeans, Pekod, and Shoa, and Koa, and all the Assyrians with them, so "
  "that every ally appears as an attacker. They shall judge thee after their judgments, and what "
  "follows includes the mutilations that Assyrian and Babylonian practice used on captives, and the "
  "stripping of the garments and jewels that chapter 16 had listed as gifts. The section closes on "
  "the image that becomes standard prophetic shorthand, thou shalt drink of thy sister's cup, deep "
  "and large, the cup of astonishment and desolation. That cup runs through Jeremiah 25, Isaiah 51, "
  "and the Psalms, and stands behind the cup Jesus asks to be spared in Gethsemane."),
 ("Both Sisters Judged Together (vv.36-49)",
  "The final oracle addresses them jointly, and the charges named here are more cultic than "
  "political, they have committed adultery, and blood is in their hands, and with their idols have "
  "they committed adultery, and have also caused their sons to pass for them through the fire. The "
  "aggravation is a matter of timing and it is the sharpest thing in the chapter, for when they had "
  "slain their children to their idols, then they came the same day into my sanctuary to profane it. "
  "The sentence is delivered by an assembly rather than by an army, and they shall judge them after "
  "the manner of adulteresses. And the purpose stated at the very end is didactic rather than "
  "punitive, that all women may be taught not to do after your lewdness, which is what an allegory "
  "this graphic is finally for."),
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
        keep = [[l, b.strip()] for l, b in ITEM_RE.findall(body_html)
                if H.unescape(l).strip() in KEEP]
        if not keep:
            problems.append(f"{page}: no book fields found to preserve")
            continue
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
