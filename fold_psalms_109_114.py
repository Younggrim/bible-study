#!/usr/bin/env python3
"""
Psalms 109 to 114. Six pages, 75 verses. All six outlines are gapless and are folded.

psalms109 is the harshest of the imprecatory psalms and carries a real interpretive question
that changes what the page means. Verses 6 to 19 may be the psalmist's own curse, or they may
be him quoting back what his accusers said about him, which several modern versions mark with
quotation marks the Hebrew does not supply. The section states the question and states what
each reading costs, rather than choosing quietly.

psalms110 is quoted or alluded to in the New Testament more than any other psalm, and Jesus
argues from verse 1 in Matthew 22 that David's Lord cannot simply be David's son. Verse 3 is
one of the most damaged verses in the psalter and the Greek reads it quite differently; the
section says so instead of expounding an English line that may not be what was written.

psalms111 and psalms112 are a deliberate pair, both alphabet acrostics of twenty-two lines,
the first about God and the second about the man who fears him, sharing whole phrases so that
what is said of God is said of the man. Neither section can be read properly alone and both
say so.

Usage:
    python3 fold_psalms_109_114.py [--check]
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
KEEP = ("Author:", "Date:", "Attributed Author:", "Classification:", "Key Themes:",
        "Historical Context:")
REPAIRS = {}

SECTIONS = {
"psalms109": [
 ("Hold Not Thy Peace, O God of My Praise (v.1)",
  "Hold not thy peace, O God of my praise. One verse, and the whole psalm hangs on the contrast in it: "
  "everyone else is talking and the only one worth hearing is silent. The title given to God is the psalm's "
  "own claim on him, since a God of my praise is a God already owed something."),
 ("They Have Rewarded Me Evil for Good (vv.2-5)",
  "For the mouth of the wicked and the mouth of the deceitful are opened against me: they have spoken "
  "against me with a lying tongue. The attack is verbal throughout, and the setting looks judicial, since "
  "the charge is false testimony rather than violence. They compassed me about also with words of hatred; "
  "and fought against me without a cause. What the speaker says he did in return is one clause long, but I "
  "give myself unto prayer, and the imbalance is the grievance, and they have rewarded me evil for good, and "
  "hatred for my love."),
 ("Let Satan Stand at His Right Hand (vv.6-20)",
  "Set thou a wicked man over him: and let Satan stand at his right hand. Fifteen verses of curse follow, "
  "the longest and severest in the psalter, and they reach past the man to his wife, his children, his "
  "parents and his memory, let his children be fatherless, and his wife a widow, let his posterity be cut "
  "off, let not the sin of his mother be blotted out. Satan here is the ordinary Hebrew word for accuser and "
  "may mean a hostile prosecutor standing where a defence counsel should be. The passage carries a serious "
  "interpretive question. On one reading it is the psalmist cursing, and verse 20 collects it, let this be "
  "the reward of mine adversaries from the LORD. On another it is the psalmist quoting the curse his accusers "
  "have laid on him, which is why several modern versions open a quotation mark at verse 6 and close it at "
  "verse 19; Hebrew has no quotation marks, so nothing in the text settles it. The first reading leaves a "
  "believer praying for a man's children to beg. The second removes that but has to explain verse 20, which "
  "reads most naturally as the psalmist's own summary. This page states the question rather than resolving "
  "it. The one anchor either way is the reason given at verse 16, because that he remembered not to shew "
  "mercy, but persecuted the poor and needy man. Acts 1:20 quotes verse 8, let another take his office, and "
  "applies it to Judas."),
 ("I Am Gone like the Shadow When It Declineth (vv.21-25)",
  "But do thou for me, O GOD the Lord, for thy name's sake. The psalm turns from the enemy to itself and the "
  "ground it offers is God's reputation and God's mercy, not the speaker's innocence. The condition described "
  "is physical, my knees are weak through fasting; and my flesh faileth of fatness, and the images are of "
  "something thinning out, I am gone like the shadow when it declineth: I am tossed up and down as the "
  "locust. Then the public part of it, when they looked upon me they shaked their heads, the gesture the "
  "crowd makes at the cross in Matthew 27:39."),
 ("Let Them Curse, but Bless Thou (vv.26-29)",
  "Help me, O LORD my God: O save me according to thy mercy. What the speaker wants from the rescue is that "
  "it be legible, that they may know that this is thy hand; that thou, LORD, hast done it. Then the sentence "
  "that shows what the psalm actually asks for, let them curse, but bless thou, which asks God to override "
  "their words rather than to silence them. The shame requested is of the same fabric as the curse in verse "
  "18, let mine adversaries be clothed with shame, so the punishment fits the crime by wearing it."),
 ("He Shall Stand at the Right Hand of the Poor (vv.30-31)",
  "I will greatly praise the LORD with my mouth; yea, I will praise him among the multitude. The mouth that "
  "has been outnumbered for thirty verses gets the last word, and it is used in public. Then the closing "
  "line, and it answers verse 6 exactly, for he shall stand at the right hand of the poor, to save him from "
  "those that condemn his soul. An accuser was asked for at the wicked man's right hand; a defender is "
  "declared at the poor man's. That inclusio is the psalm's own summary of what it wanted."),
],
"psalms110": [
 ("Sit Thou at My Right Hand (v.1)",
  "The LORD said unto my Lord, Sit thou at my right hand, until I make thine enemies thy footstool. Two "
  "different words stand behind the two Lords, the covenant name and a term of address for a superior, and "
  "the whole New Testament use of the psalm turns on that difference. Jesus quotes the verse in Matthew "
  "22:44 and asks how David can call his own descendant Lord, which is the question the Gospels leave "
  "hanging. It is the most quoted verse of the psalter in the New Testament, standing behind the session at "
  "God's right hand in Acts 2:34, 1 Corinthians 15:25, Hebrews 1:13 and Hebrews 10:12. Sitting is the point: "
  "the enemies are subdued by someone else's action while the one addressed is seated."),
 ("The Rod of Thy Strength out of Zion (vv.2-3)",
  "The LORD shall send the rod of thy strength out of Zion: rule thou in the midst of thine enemies. The rule "
  "is exercised among the enemies rather than after their removal, which fits the until of verse 1. Verse 3 "
  "is another matter. Thy people shall be willing in the day of thy power, in the beauties of holiness from "
  "the womb of the morning: thou hast the dew of thy youth. The Hebrew here is among the most difficult in "
  "the psalter, the words for holiness, womb and dew can be divided more than one way, and the Septuagint "
  "reads a line about begetting before the morning star that the Latin fathers used for the eternal "
  "generation of the Son. No English rendering of this verse should be leaned on hard, and this one is not."),
 ("A Priest for Ever After the Order of Melchizedek (v.4)",
  "The LORD hath sworn, and will not repent, Thou art a priest for ever after the order of Melchizedek. The "
  "second decree, and it does something the law forbids, since a king of Judah could not be a priest and "
  "Uzziah was struck for trying in 2 Chronicles 26. The way round it is Melchizedek, who appears for three "
  "verses in Genesis 14 as both king of Salem and priest of the most high God, with no genealogy and no "
  "successor. Hebrews 5 to 7 builds its entire argument on this one verse, arguing from the oath that the "
  "priesthood cannot be revoked and from the silence about Melchizedek's parents that it has no term."),
 ("He Shall Judge Among the Heathen (vv.5-7)",
  "The Lord at thy right hand shall strike through kings in the day of his wrath. The positions have "
  "reversed from verse 1, and the psalm ends in a battlefield described without any softening, he shall fill "
  "the places with the dead bodies; he shall wound the heads over many countries. Then a last verse that has "
  "puzzled every commentator, he shall drink of the brook in the way: therefore shall he lift up the head. It "
  "reads most simply as a pursuing king pausing to drink and pressing on, an image of a campaign not yet "
  "finished, which leaves the psalm where verse 1 left it, with the outcome certain and the work in "
  "progress."),
],
"psalms111": [
 ("I Will Praise the LORD with My Whole Heart (v.1)",
  "Praise ye the LORD. I will praise the LORD with my whole heart, in the assembly of the upright, and in the "
  "congregation. This psalm and the next are a matched pair, each an acrostic of twenty-two lines running "
  "the Hebrew alphabet, and they are meant to be read together: this one describes God and Psalm 112 "
  "describes the man who fears him, in some of the same words. The praise is private in resolve and public "
  "in setting."),
 ("The Works of the LORD Are Great (vv.2-4)",
  "The works of the LORD are great, sought out of all them that have pleasure therein. The line is engraved "
  "over the entrance to the Cavendish Laboratory in Cambridge, which is a fair use of it, since it makes "
  "investigation the natural response of anyone who enjoys the subject. His work is honourable and glorious: "
  "and his righteousness endureth for ever. Then a claim about deliberate memory, he hath made his wonderful "
  "works to be remembered, which is what the festivals and this psalm are both for."),
 ("He Will Ever Be Mindful of His Covenant (vv.5-6)",
  "He hath given meat unto them that fear him: he will ever be mindful of his covenant. Food and covenant in "
  "one verse, the daily and the permanent held together. And the works are given a purpose beyond display, "
  "he hath shewed his people the power of his works, that he may give them the heritage of the heathen, "
  "which reads the conquest as evidence rather than as reward."),
 ("All His Commandments Are Sure (vv.7-8)",
  "The works of his hands are verity and judgment; all his commandments are sure. The psalm moves from what "
  "God does to what God says and applies the same words to both, which is its quiet argument: the commands "
  "are as reliable as the creation. They stand fast for ever and ever, and are done in truth and "
  "uprightness."),
 ("The Fear of the LORD Is the Beginning of Wisdom (vv.9-10)",
  "He sent redemption unto his people: he hath commanded his covenant for ever: holy and reverend is his "
  "name. This is the only place KJV uses the word reverend, and the clerical title comes from it, which is a "
  "curious afterlife for a line about the name of God. Then the psalm's last verse states the proverb that "
  "Proverbs 1:7 and Proverbs 9:10 also carry, the fear of the LORD is the beginning of wisdom, and adds the "
  "test, a good understanding have all they that do his commandments. Understanding is measured by conduct "
  "and not by comprehension."),
],
"psalms112": [
 ("Blessed Is the Man That Feareth the LORD (v.1)",
  "Praise ye the LORD. Blessed is the man that feareth the LORD, that delighteth greatly in his "
  "commandments. Psalm 111 ended on the fear of the LORD and this psalm begins there, taking up the same "
  "acrostic form for twenty-two lines and turning it on the man instead of on God. Delight rather than "
  "compliance is what is said of his relation to the commandments."),
 ("His Righteousness Endureth for Ever (vv.2-3)",
  "His seed shall be mighty upon earth: the generation of the upright shall be blessed. Wealth and riches "
  "shall be in his house: and his righteousness endureth for ever. That last clause was said of God in Psalm "
  "111:3, word for word, and here it is said of the man, which is the point of pairing the two psalms. The "
  "promise of wealth is the kind of statement Job's friends made and Job disproved, and the psalter itself "
  "questions it at length in Psalm 37 and Psalm 73; this psalm gives the rule and the others give the "
  "exceptions."),
 ("Light in the Darkness (v.4)",
  "Unto the upright there ariseth light in the darkness: he is gracious, and full of compassion, and "
  "righteous. The three adjectives were used of God in Psalm 111:4, and here it is ambiguous whether they "
  "describe God or the upright man; the Hebrew allows either and the pairing of the psalms suggests the "
  "ambiguity is intended. Darkness is assumed, not denied, and what is promised is light inside it."),
 ("A Good Man Sheweth Favour, and Lendeth (v.5)",
  "A good man sheweth favour, and lendeth: he will guide his affairs with discretion. Lending in Israel meant "
  "lending without interest to a fellow Israelite, so the verse describes a transfer that is not an "
  "investment. Discretion keeps it from becoming sentimental: the generosity is managed rather than "
  "impulsive."),
 ("His Heart Is Fixed, Trusting in the LORD (vv.6-8)",
  "Surely he shall not be moved for ever: the righteous shall be in everlasting remembrance. Against the "
  "grass and the forgotten place of Psalm 103:16, this promises that a life is remembered. He shall not be "
  "afraid of evil tidings: his heart is fixed, trusting in the LORD. Fixed is the same word Psalm 108 uses of "
  "the heart set on praise, and the fearlessness is located in what the heart is attached to rather than in "
  "temperament. The last clause is harder to like, until he see his desire upon his enemies, and the psalm "
  "leaves it standing."),
 ("He Hath Dispersed, He Hath Given to the Poor (v.9)",
  "He hath dispersed, he hath given to the poor; his righteousness endureth for ever; his horn shall be "
  "exalted with honour. Paul quotes this verse in 2 Corinthians 9:9 while raising money for the Jerusalem "
  "collection, and he quotes it as the description of the giver he wants his readers to be. Dispersed is a "
  "scattering word, used of sowing, which fits the argument he builds around it."),
 ("The Desire of the Wicked Shall Perish (v.10)",
  "The wicked shall see it, and be grieved; he shall gnash with his teeth, and melt away: the desire of the "
  "wicked shall perish. The acrostic ends on the alternative, and what the wicked man loses is not his goods "
  "but his wanting, which is the sharpest thing in the psalm. Seeing it is part of the grief; the blessing of "
  "the upright is visible to the one who does not share it."),
],
"psalms113": [
 ("From the Rising of the Sun unto the Going Down (vv.1-3)",
  "Praise ye the LORD. Praise, O ye servants of the LORD, praise the name of the LORD. This opens the "
  "Egyptian Hallel, Psalms 113 to 118, sung at Passover, which means these are among the psalms Jesus and "
  "the disciples would have sung at the last supper, since Matthew 26:30 records a hymn. The praise is "
  "unbounded in time twice over, from this time forth and for evermore, and then from the rising of the sun "
  "unto the going down of the same."),
 ("Who Is Like unto the LORD Our God (vv.4-5)",
  "The LORD is high above all nations, and his glory above the heavens. The psalm builds height deliberately "
  "so that it has somewhere to fall from, and the question it asks at the top is the one Exodus 15:11 asks at "
  "the sea, who is like unto the LORD our God, who dwelleth on high."),
 ("He Raiseth Up the Poor out of the Dust (vv.6-9)",
  "Who humbleth himself to behold the things that are in heaven, and in the earth. The turn is the psalm's "
  "whole point: stooping is listed among the marvels, and even heaven is something God has to look down at. "
  "Then the direction of the stoop, he raiseth up the poor out of the dust, and lifteth the needy out of the "
  "dunghill, that he may set him with princes. The last case is domestic and particular, he maketh the barren "
  "woman to keep house, and to be a joyful mother of children, which is Hannah's situation in 1 Samuel 1 and "
  "the substance of her song in 1 Samuel 2, and Mary's in Luke 1. Praise ye the LORD."),
],
"psalms114": [
 ("When Israel Went Out of Egypt (vv.1-2)",
  "When Israel went out of Egypt, the house of Jacob from a people of strange language. Eight verses, and "
  "the whole exodus is compressed into the first two. Strange language marks Egypt as foreign by sound "
  "rather than by border. Judah was his sanctuary, and Israel his dominion, so what came out of Egypt is "
  "described as a place God lives rather than a nation God owns."),
 ("The Sea Saw It, and Fled (vv.3-4)",
  "The sea saw it, and fled: Jordan was driven back. Two water crossings forty years apart are set in one "
  "line, and both are told as flight rather than as parting. Then the mountains, and the psalm gives them "
  "animals to imitate, the mountains skipped like rams, and the little hills like lambs. Sinai is the "
  "mountain in question and the picture is closer to a startled flock than to an earthquake."),
 ("What Ailed Thee, O Thou Sea (vv.5-6)",
  "What ailed thee, O thou sea, that thou fleddest? thou Jordan, that thou wast driven back? The psalm turns "
  "and interrogates the landscape, repeating its own four images back at them as questions, which is the most "
  "confident piece of rhetoric in the Hallel. The answer is withheld for a verse, and the delay is the joke."),
 ("The Flint into a Fountain of Waters (vv.7-8)",
  "Tremble, thou earth, at the presence of the Lord, at the presence of the God of Jacob. That is the answer, "
  "and it is given as a command rather than an explanation. The last verse chooses the least likely of the "
  "wilderness miracles to end on, which turned the rock into a standing water, the flint into a fountain of "
  "waters, so a psalm about seas fleeing closes on water coming out of the one substance that holds none."),
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
        if len(set(labels)) != len(labels):
            dup = sorted({l for l in labels if labels.count(l) > 1})
            found.append(f"{page}: duplicate label(s) {dup}")
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
