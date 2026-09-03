#!/usr/bin/env python3
"""
Psalms 106 to 108. Three pages, 104 verses. All three outlines are gapless and are folded.

psalms106 closes Book IV with the doxology at verse 48, which is editorial furniture marking
the end of the collection rather than the end of the poem. Verses 1 and 47-48 stand in 1
Chronicles 16:34-36. The section says so, since a reader who takes verse 48 as the psalm's
conclusion will think the prayer of verse 47 was answered.

psalms106 also puts the hardest cross-reference in the psalter at verse 31, where Phinehas
killing a man is counted unto him for righteousness, in the same words Genesis 15:6 uses of
Abraham believing. Paul builds Romans 4 on the Genesis verse. The section names the collision
and leaves it standing, because both texts are in the canon and neither yields.

psalms108 is not a new composition. It is Psalm 57:7-11 followed by Psalm 60:5-12, joined
without a seam, which makes it the clearest case in the psalter of an editor building a psalm
out of two others. The section says which parts came from where.

Usage:
    python3 fold_psalms_106_108.py [--check]
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
"psalms106": [
 ("Remember Me with the Favour Thou Bearest (vv.1-5)",
  "Praise ye the LORD. O give thanks unto the LORD; for he is good: for his mercy endureth for ever. The "
  "psalm opens with the refrain that runs through the whole psalter and then asks a question that concedes "
  "defeat in advance, who can utter the mighty acts of the LORD. Verse 1 stands in 1 Chronicles 16:34. The "
  "request is personal and modest, remember me, O LORD, with the favour that thou bearest unto thy people, "
  "and what the singer wants from it is not rescue but company, that I may rejoice in the gladness of thy "
  "nation."),
 ("We Have Sinned with Our Fathers (v.6)",
  "We have sinned with our fathers, we have committed iniquity, we have done wickedly. One verse, and it "
  "decides how the next forty will read. The confession is first person plural and it refuses the "
  "distinction between the generation that failed and the generation reciting the failure, with our fathers "
  "rather than like them. Psalm 105 told this same history and mentioned no sin in it; this psalm tells it "
  "as nothing else."),
 ("They Provoked Him at the Red Sea (vv.7-12)",
  "Our fathers understood not thy wonders in Egypt; they remembered not the multitude of thy mercies; but "
  "provoked him at the sea, even at the Red sea. The charge is failure of memory before failure of nerve. "
  "And the rescue is credited to God's reputation rather than to their deserving, nevertheless he saved them "
  "for his name's sake, that he might make his mighty power to be known, which is the pattern every section "
  "of this psalm repeats. Then belief arrives, and the psalm dates it precisely and briefly, then believed "
  "they his words; they sang his praise."),
 ("He Gave Them Their Request, but Sent Leanness (vv.13-15)",
  "They soon forgat his works; they waited not for his counsel. Soon is the psalm's own comment on the song "
  "of verse 12. Then the sentence that has outlived the rest of the psalm, and he gave them their request; "
  "but sent leanness into their soul. The prayer was answered and the answer was the judgement, which is a "
  "harder doctrine than refusal, and the psalm offers it without softening."),
 ("They Envied Moses in the Camp (vv.16-18)",
  "They envied Moses also in the camp, and Aaron the saint of the LORD. The revolt of Numbers 16 is "
  "compressed into three verses and read as envy of office. The earth opened and swallowed up Dathan, and "
  "covered the company of Abiram. Korah, who leads the rebellion in Numbers, is not named here, and the "
  "sons of Korah are among the psalter's own singers, with eleven psalms to their name."),
 ("They Made a Calf in Horeb (vv.19-23)",
  "They made a calf in Horeb, and worshipped the molten image. The psalm's verdict on it is an exchange, "
  "thus they changed their glory into the similitude of an ox that eateth grass, and the last clause is the "
  "insult: the animal chosen has to eat. Paul argues the same way about idolatry in Romans 1:23. Then Moses "
  "in the gap, therefore he said that he would destroy them, had not Moses his chosen stood before him in "
  "the breach, to turn away his wrath, which is the psalm's strongest statement about what intercession "
  "does."),
 ("They Despised the Pleasant Land (vv.24-27)",
  "Yea, they despised the pleasant land, they believed not his word. The refusal at Kadesh is read as "
  "contempt for a gift, and the psalm names the mechanism as unbelief rather than fear. But murmured in "
  "their tents. The sentence passed reaches past the wilderness generation, to overthrow their seed also "
  "among the nations, and to scatter them in the lands, which is the exile written into a wilderness story "
  "and is the clearest sign of when this psalm was compiled."),
 ("They Joined Themselves unto Baal-peor (vv.28-31)",
  "They joined themselves also unto Baal-peor, and ate the sacrifices of the dead. Numbers 25, and the "
  "phrase about the dead suggests a cult of the departed rather than ordinary idolatry. The plague is stayed "
  "by an execution, then stood up Phinehas, and executed judgment. And the verdict on him is the difficulty, "
  "and that was counted unto him for righteousness unto all generations for evermore, since the same words "
  "in Genesis 15:6 are said of Abraham believing, and Paul builds the argument of Romans 4 on that verse. "
  "Here the phrase describes a man with a spear. The two texts cannot be flattened into one another, and "
  "this page does not attempt it."),
 ("He Spake Unadvisedly with His Lips (vv.32-33)",
  "They angered him also at the waters of strife, so that it went ill with Moses for their sakes. Meribah, "
  "and the psalm assigns the blame in a direction Numbers 20 does not, because they provoked his spirit, so "
  "that he spake unadvisedly with his lips. Numbers holds Moses responsible and bars him from the land for "
  "it; the psalm reads his outburst as something the people did to him. Both accounts are in the canon and "
  "the psalm is not correcting Numbers so much as pleading for Moses."),
 ("They Were Mingled Among the Heathen (vv.34-39)",
  "They did not destroy the nations, concerning whom the LORD commanded them: but were mingled among the "
  "heathen, and learned their works. The failure named is incomplete obedience, and the consequence is "
  "cultural rather than military. What it ends in is stated without any euphemism, yea, they sacrificed "
  "their sons and their daughters unto devils, and shed innocent blood, and the land was polluted with "
  "blood. This is the psalm's floor. Devils renders shedim, a word for spirits that KJV read through Latin; "
  "the practice it describes is the one 2 Kings 16 and 21 record of Judah's own kings."),
 ("Many Times Did He Deliver Them (vv.40-46)",
  "Therefore was the wrath of the LORD kindled against his people, insomuch that he abhorred his own "
  "inheritance. The strongest word in the psalm is used of God's feeling toward Israel, and the psalm does "
  "not qualify it. What follows is the cycle of Judges stated as policy, many times did he deliver them; but "
  "they provoked him with their counsel. Then the turn on which the whole psalm rests, nevertheless he "
  "regarded their affliction, when he heard their cry, and he remembered for them his covenant, and repented "
  "according to the multitude of his mercies. Repented here means turned from a course, not confessed a "
  "fault. The mercy shown is oddly indirect, he made them also to be pitied of all those that carried them "
  "captives, which is a kindness inside the punishment rather than instead of it."),
 ("Save Us, and Gather Us from Among the Heathen (vv.47-48)",
  "Save us, O LORD our God, and gather us from among the heathen, to give thanks unto thy holy name. That is "
  "the psalm's one request and it is made from exile, which places the singer inside the last stage of the "
  "history he has been reciting. The prayer is left unanswered. What follows it is not a reply but the "
  "closing formula of the collection, blessed be the Lord God of Israel from everlasting to everlasting: and "
  "let all the people say, Amen, which ends Book IV of the psalter, and stands with verse 47 in 1 Chronicles "
  "16:35-36. Verse 48 is editorial furniture rather than part of the poem, and the psalm proper ends on a "
  "petition still outstanding."),
],
"psalms107": [
 ("Let the Redeemed of the LORD Say So (vv.1-3)",
  "O give thanks unto the LORD, for he is good: for his mercy endureth for ever. Book V of the psalter opens "
  "with the same line that closed Book IV, which ties the collections together across the seam. The "
  "instruction is to speak up, let the redeemed of the LORD say so, and the ones addressed are people "
  "brought back from somewhere, gathered them out of the lands, from the east, and from the west, from the "
  "north, and from the south. That points to the return from exile and sets up the four case studies that "
  "follow."),
 ("They Wandered in the Wilderness in a Solitary Way (vv.4-9)",
  "They wandered in the wilderness in a solitary way; they found no city to dwell in. The first of four "
  "vignettes, each built on the same four movements: the trouble, the cry, the rescue, the call to give "
  "thanks. Hungry and thirsty, their soul fainted in them. Then the refrain that marks the turn in all four, "
  "then they cried unto the LORD in their trouble, and he delivered them out of their distresses. No fault "
  "is assigned in this one; the lostness is simply reported. And the response asked for is stated as a wish "
  "rather than a command, oh that men would praise the LORD for his goodness."),
 ("Such as Sit in Darkness and in the Shadow of Death (vv.10-16)",
  "Such as sit in darkness and in the shadow of death, being bound in affliction and iron. The second "
  "vignette is prison, and unlike the first it names a cause, because they rebelled against the words of "
  "God, and contemned the counsel of the most High. So the psalm is willing to say that some trouble is "
  "earned and some is not, and to treat both as grounds for the same cry. The rescue is violent toward the "
  "building rather than the prisoner, he hath broken the gates of brass, and cut the bars of iron in "
  "sunder."),
 ("He Sent His Word, and Healed Them (vv.17-22)",
  "Fools because of their transgression, and because of their iniquities, are afflicted. The third vignette "
  "is illness, and again a cause is named, which the psalm treats as a general pattern and not a rule for "
  "diagnosing any particular case. Their soul abhorreth all manner of meat; and they draw near unto the "
  "gates of death. The cure is verbal, he sent his word, and healed them, and what is asked in return is "
  "specific, let them sacrifice the sacrifices of thanksgiving, which is an offering rather than a mood."),
 ("They That Go Down to the Sea in Ships (vv.23-32)",
  "They that go down to the sea in ships, that do business in great waters. The fourth vignette is the "
  "longest and the only one about people at work, and it is the finest piece of storm writing in the Old "
  "Testament outside Jonah. The storm is God's, for he commandeth, and raiseth the stormy wind. They mount "
  "up to the heaven, they go down again to the depths. And are at their wit's end, which is KJV's rendering "
  "of a phrase about wisdom swallowed up, and it entered English from this verse. The rescue is a stillness, "
  "he maketh the storm a calm, so that the waves thereof are still, the words Mark 4:39 echoes at Galilee."),
 ("He Turneth Rivers into a Wilderness (vv.33-42)",
  "He turneth rivers into a wilderness, and the watersprings into dry ground. The psalm leaves the vignettes "
  "and states the principle behind them as a set of reversals, each one paired with its opposite: fruitful "
  "land into barrenness for the wickedness of them that dwell therein, and then the wilderness into a "
  "standing water. The same power runs both directions. Princes are brought down and the poor lifted, he "
  "poureth contempt upon princes, yet setteth he the poor on high from affliction, which is the theme Hannah "
  "sings in 1 Samuel 2 and Mary in Luke 1. And all iniquity shall stop her mouth."),
 ("Whoso Is Wise Will Observe These Things (v.43)",
  "Whoso is wise, and will observe these things, even they shall understand the lovingkindness of the LORD. "
  "The last verse turns the psalm into a piece of wisdom writing and makes understanding conditional on "
  "paying attention. What is offered is not proof but a pattern visible to anyone who looks, and the thing "
  "to be understood is named as hesed, the covenant kindness the refrain of verse 1 has already claimed "
  "endures for ever."),
],
"psalms108": [
 ("O God, My Heart Is Fixed (vv.1-5)",
  "O God, my heart is fixed; I will sing and give praise, even with my glory. These five verses are Psalm "
  "57:7-11 with almost no change, and the nine that follow are Psalm 60:5-12. Psalm 108 is therefore a psalm "
  "assembled from two others, and the join falls between verses 5 and 6 without a seam. Fixed means settled "
  "or steady, and the psalm makes it a decision rather than a feeling. Awake, psaltery and harp: I myself "
  "will awake early. The praise is aimed outward, I will sing praises unto thee among the nations, and the "
  "measurements are the psalter's largest, thy mercy is great above the heavens."),
 ("That Thy Beloved May Be Delivered (v.6)",
  "That thy beloved may be delivered: save with thy right hand, and answer me. This is where Psalm 60 takes "
  "over, and the mood changes completely: five verses of settled praise are followed by a request from "
  "trouble. The compiler chose to put confidence first and need second, which reverses the usual order of a "
  "lament and is the reason for building the psalm at all."),
 ("Moab Is My Washpot (vv.7-9)",
  "God hath spoken in his holiness; I will rejoice, I will divide Shechem, and mete out the valley of "
  "Succoth. What follows is a survey of the kingdom spoken in God's own voice, and it moves from allotting "
  "Israelite territory to disposing of neighbours. Gilead is mine; Manasseh is mine; Ephraim also is the "
  "strength of mine head; Judah is my lawgiver. Then the insults, Moab is my washpot, over Edom will I cast "
  "out my shoe, over Philistia will I triumph. The washpot is a basin for feet and casting a shoe is a claim "
  "of ownership; these are contemptuous images and the psalm intends them to be."),
 ("Thou, O God, Who Hast Cast Us Off (vv.10-11)",
  "Who will bring me into the strong city? who will lead me into Edom? The confidence of the survey runs "
  "straight into a question it cannot answer on its own. And the psalm says the thing a psalm of national "
  "confidence is not supposed to say, wilt not thou, O God, who hast cast us off. The rejection is stated as "
  "fact and addressed to the one held responsible for it, in the same breath as the request for help."),
 ("Vain Is the Help of Man (vv.12-13)",
  "Give us help from trouble: for vain is the help of man. The psalm ends by ruling out the alternative it "
  "has just been looking for in verse 10, since the strong city needs an army and the psalm says an army "
  "will not do it. Through God we shall do valiantly: for he it is that shall tread down our enemies. "
  "Valiantly is still expected of them; the claim is not that they will be spared the fighting but that the "
  "outcome is not theirs to secure."),
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
