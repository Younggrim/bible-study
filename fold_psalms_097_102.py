#!/usr/bin/env python3
"""
Psalms 97 to 102. Six pages, 71 verses. All six outlines are gapless and are folded.

psalms100 turns on a textual question the English cannot show. Verse 3 reads it is he that
hath made us, and not we ourselves, which follows one of the two Hebrew readings; the other,
differing by a single letter that sounds the same, gives and we are his. The section states
both, because the verse is quoted constantly and almost never with the alternative attached.

psalms101 is the psalm most likely to be misread as boasting. It is a king's list of
commitments, not a report, and David's own recorded conduct fails several items on it. The
section says that rather than smoothing it over, since the gap between the vow and the life is
the honest subject of the page.

psalms102 supplies Hebrews 1:10-12 with its proof that the Son is the maker of the world.
Verses 25 to 27 are addressed to the LORD in the psalm and to Christ in the epistle, and the
section names the move rather than assuming it.

Usage:
    python3 fold_psalms_097_102.py [--check]
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
"psalms97": [
 ("The LORD Reigneth, Let the Earth Rejoice (v.1)",
  "The LORD reigneth; let the earth rejoice; let the multitude of isles be glad thereof. The same two words "
  "that open Psalms 93 and 99, and the response asked for is gladness rather than fear, which is worth "
  "noticing before the fire arrives in verse 3. Isles means the far coasts, the edge of the known map, so "
  "the summons reaches the places least likely to have heard."),
 ("Clouds and Darkness Round About Him (vv.2-6)",
  "Clouds and darkness are round about him: righteousness and judgment are the habitation of his throne. "
  "The two halves of the verse pull against each other on purpose, since what cannot be seen is said to "
  "rest on what can be stated. Then a theophany assembled from Sinai and from the storm, a fire goeth "
  "before him, his lightnings enlightened the world, the hills melted like wax at the presence of the LORD. "
  "The melting of hills is the strongest form of the figure the psalter has: the things that do not move "
  "are the things that give way. And the whole display is treated as testimony, the heavens declare his "
  "righteousness, and all the people see his glory."),
 ("Confounded Be All They That Serve Graven Images (v.7)",
  "Confounded be all they that serve graven images, that boast themselves of idols: worship him, all ye "
  "gods. One verse, and its second half is the difficulty. The Septuagint renders the last clause with "
  "angels rather than gods, and Hebrews 1:6 uses that kind of wording of the Son, though its quotation is "
  "usually traced to Deuteronomy 32:43. What the Hebrew does is address whatever the nations counted as "
  "divine and order it to bow, which is a sharper insult than denying its existence."),
 ("Zion Heard, and Was Glad (vv.8-9)",
  "Zion heard, and was glad; and the daughters of Judah rejoiced because of thy judgments, O LORD. The "
  "judgements that made the hills melt are received in Jerusalem as good news, and the psalm offers no "
  "transition between the terror and the gladness because it does not think one is needed. For thou, LORD, "
  "art high above all the earth: thou art exalted far above all gods."),
 ("Ye That Love the LORD, Hate Evil (vv.10-12)",
  "Ye that love the LORD, hate evil. The psalm has been cosmic for nine verses and here it issues a "
  "domestic instruction, and it makes love and hatred two sides of one disposition rather than opposites. "
  "The promise attached is preservation, not exemption, he delivereth them out of the hand of the wicked, "
  "which assumes the hand. Then the image that has outlasted the rest of the psalm, light is sown for the "
  "righteous, and gladness for the upright in heart, where sowing means the light is planted now and "
  "gathered later."),
],
"psalms98": [
 ("His Right Hand Hath Gotten Him the Victory (vv.1-3)",
  "O sing unto the LORD a new song; for he hath done marvellous things. The new song is asked for because "
  "something new has happened, and the psalm is careful to leave no human agent in it, his right hand, and "
  "his holy arm, hath gotten him the victory. Then the audience widens past Israel twice over, his "
  "righteousness hath he openly shewed in the sight of the heathen, and all the ends of the earth have seen "
  "the salvation of our God. Isaac Watts took this psalm as the basis of Joy to the World, which is why a "
  "Christmas carol has no manger in it and a great deal about judgement."),
 ("Make a Joyful Noise, All the Earth (vv.4-6)",
  "Make a joyful noise unto the LORD, all the earth: make a loud noise, and rejoice, and sing praise. Volume "
  "is asked for plainly, and the instruments named are the temple's, the harp, the trumpets and the sound "
  "of cornet. The title given to God at the end of the list is the one the psalm has been arguing for, "
  "before the LORD, the King."),
 ("Let the Floods Clap Their Hands (vv.7-9)",
  "Let the sea roar, and the fulness thereof; the world, and they that dwell therein. The invitation passes "
  "from the congregation to the landscape, and the metaphor stops being decorous, let the floods clap their "
  "hands, let the hills be joyful together. Then the reason, and it is the same one Psalm 96 gives, for he "
  "cometh to judge the earth. Equity is the last word of the psalm, and the psalm's whole case is that a "
  "world which has seen unequal judgement would greet a fair one with noise."),
],
"psalms99": [
 ("He Sitteth Between the Cherubims (vv.1-3)",
  "The LORD reigneth; let the people tremble: he sitteth between the cherubims. The response demanded here "
  "is the opposite of Psalm 97's, which asked the earth to rejoice, and the difference is the subject: this "
  "psalm is about holiness rather than about righteous rule. Sitting between the cherubim places the throne "
  "on the ark in the holy of holies, so the reign is located in one room. Let them praise thy great and "
  "terrible name; for it is holy. Terrible carries its older sense, fear-inspiring, and holy closes verses "
  "3, 5 and 9 in a threefold refrain that gives the psalm its shape."),
 ("The King's Strength Loveth Judgment (vv.4-5)",
  "The king's strength also loveth judgment; thou dost establish equity, thou executest judgment and "
  "righteousness in Jacob. The line is awkward in English and the awkwardness is in the Hebrew too, which "
  "moves between speaking of the king and speaking to him. What it claims is that the power and the "
  "fairness are the same thing, not two policies held in balance. Exalt ye the LORD our God, and worship at "
  "his footstool; for he is holy."),
 ("Moses and Aaron Among His Priests (vv.6-7)",
  "Moses and Aaron among his priests, and Samuel among them that call upon his name; they called upon the "
  "LORD, and he answered them. Three names, all of them intercessors, and the psalm produces them as "
  "evidence that the holiness it has been describing is approachable. Moses is counted among priests here "
  "though he held no priestly office, which is the psalm reading his role by function rather than by title. "
  "He spake unto them in the cloudy pillar."),
 ("Thou Wast a God That Forgavest Them (vv.8-9)",
  "Thou answeredst them, O LORD our God: thou wast a God that forgavest them, though thou tookest vengeance "
  "of their inventions. The verse holds two things most treatments of forgiveness separate, since the "
  "pardon is real and the consequence still falls, and the psalm sets them in one sentence without "
  "explaining how they fit. Moses was forgiven and still died outside the land. Then the refrain a third "
  "time, for the LORD our God is holy, which is the psalm's answer to why both halves are true at once."),
],
"psalms100": [
 ("Serve the LORD with Gladness (vv.1-2)",
  "Make a joyful noise unto the LORD, all ye lands. Five verses, and it is the best known psalm of praise "
  "in the psalter, standing behind All People That on Earth Do Dwell. The superscription calls it a psalm "
  "of praise, or of thanksgiving, which in temple use meant it accompanied an offering. Serve the LORD with "
  "gladness: come before his presence with singing. Service and gladness are put in the same clause, so the "
  "psalm does not treat duty and pleasure as rivals."),
 ("Know Ye That the LORD He Is God (v.3)",
  "Know ye that the LORD he is God: it is he that hath made us, and not we ourselves; we are his people, "
  "and the sheep of his pasture. The middle clause rests on a textual choice. Two Hebrew readings differ by "
  "one letter and sound identical, one giving not we ourselves and the other giving and we are his, and "
  "the margins of the old English Bibles record both. KJV took the first. Either way the verse denies "
  "self-origin and asserts belonging; the second reading simply says it positively."),
 ("Enter into His Gates with Thanksgiving (v.4)",
  "Enter into his gates with thanksgiving, and into his courts with praise: be thankful unto him, and bless "
  "his name. The geography is the temple's, gates then courts, so the verse describes a movement inward "
  "rather than a state of mind. Thanksgiving is named as the thing carried in, which is what an offering "
  "psalm would say."),
 ("His Mercy Is Everlasting (v.5)",
  "For the LORD is good; his mercy is everlasting; and his truth endureth to all generations. The last verse "
  "supplies the reason for the four commands before it, and all three grounds are about durability rather "
  "than intensity. That is the psalm's quiet argument: praise is owed not because God is impressive but "
  "because he does not run out."),
],
"psalms101": [
 ("I Will Sing of Mercy and Judgment (v.1)",
  "I will sing of mercy and judgment: unto thee, O LORD, will I sing. The two words name the pair a ruler "
  "has to hold together, and the psalm that follows is a king's own account of how he intends to. Every "
  "main clause from here to the end is first person future, which makes this a vow rather than a report."),
 ("I Will Walk Within My House with a Perfect Heart (vv.2-4)",
  "I will behave myself wisely in a perfect way. Perfect renders tamim, whole or undivided, not flawless, "
  "and the distinction matters for reading the rest. Then an interruption that sits oddly in a list of "
  "resolutions, O when wilt thou come unto me, as though the vow needed help to keep. The commitments "
  "narrow to the private house and to the eyes, I will set no wicked thing before mine eyes, and end with "
  "the inner disposition, a froward heart shall depart from me."),
 ("He That Worketh Deceit Shall Not Dwell Within My House (vv.5-7)",
  "Whoso privily slandereth his neighbour, him will I cut off. The vow turns outward to the court and to "
  "appointments, and the offences singled out are all offences of speech and bearing rather than violence, "
  "the secret slanderer, the high look and proud heart, the worker of deceit, the teller of lies. The "
  "positive side is a hiring policy, mine eyes shall be upon the faithful of the land, that they may dwell "
  "with me. Read against the record this is the psalm's real difficulty, since David kept Joab in office "
  "for a lifetime and himself arranged Uriah's death by letter. The vow is not therefore insincere; it is a "
  "standard the man who wrote it did not meet, and the psalter puts several of his failures on record "
  "elsewhere without withdrawing this."),
 ("The City of the LORD (v.8)",
  "I will early destroy all the wicked of the land; that I may cut off all wicked doers from the city of the "
  "LORD. Early can mean promptly or morning by morning, and the second sense fits a king holding court at "
  "daybreak. The last phrase gives the reason for the whole psalm: the city belongs to someone else, and "
  "the king is stating the terms he thinks its owner requires."),
],
"psalms102": [
 ("Hide Not Thy Face from Me (vv.1-2)",
  "Hear my prayer, O LORD, and let my cry come unto thee. The superscription is unlike any other in the "
  "psalter, a prayer of the afflicted, when he is overwhelmed, and poureth out his complaint before the "
  "LORD, and it names no author, which has the effect of lending the psalm to anyone in that condition. "
  "Hide not thy face from me in the day when I am in trouble. It is counted among the seven penitential "
  "psalms, though it confesses no particular sin."),
 ("My Days Are Consumed like Smoke (vv.3-11)",
  "For my days are consumed like smoke, and my bones are burned as an hearth. Nine verses of physical "
  "description, and the figures are all of things drying, burning or thinning out, withered like grass, "
  "bones cleaving to the skin, ashes eaten instead of bread. Three birds carry the loneliness, and KJV's "
  "identifications are uncertain guesses at rare Hebrew words: I am like a pelican of the wilderness, I am "
  "like an owl of the desert, I watch, and am as a sparrow alone upon the house top. Then the cause is "
  "named, and it is not the enemies, because of thine indignation and thy wrath: for thou hast lifted me "
  "up, and cast me down. The psalm holds God responsible for the trouble it is asking God to end, and does "
  "not soften either half."),
 ("Thou Shalt Arise, and Have Mercy upon Zion (vv.12-22)",
  "But thou, O LORD, shalt endure for ever; and thy remembrance unto all generations. The turn comes on a "
  "contrast rather than on a change in circumstances: the days that were smoke are set against years that "
  "do not end. And the hope that follows is not the speaker's recovery but the city's, thou shalt arise, and "
  "have mercy upon Zion: for the time to favour her, yea, the set time, is come. The affection is oddly "
  "specific, thy servants take pleasure in her stones, and favour the dust thereof, which suits people "
  "looking at rubble. What the section expects from that restoration is publicity, so the heathen shall "
  "fear the name of the LORD. Then a line written with later readers in view, this shall be written for the "
  "generation to come, followed by the reason God is said to have looked down, to hear the groaning of the "
  "prisoner, to loose those that are appointed to death."),
 ("But Thou Art the Same (vv.23-28)",
  "He weakened my strength in the way; he shortened my days. The psalm returns to the individual and makes "
  "its one request, take me not away in the midst of my days, set against thy years are throughout all "
  "generations. Then the passage the New Testament uses, of old hast thou laid the foundation of the earth, "
  "and the heavens are the work of thy hands, they shall perish, but thou shalt endure, as a vesture shalt "
  "thou change them. Hebrews 1:10-12 quotes these verses and applies them to the Son, so words addressed to "
  "the LORD by a dying man become the epistle's evidence that Christ made the world; the psalm gives no "
  "hint of that reading, and the argument depends on the identification rather than on anything in the "
  "Hebrew. But thou art the same, and thy years shall have no end. The last verse asks nothing for the "
  "speaker and everything for those after him, the children of thy servants shall continue."),
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
