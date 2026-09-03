#!/usr/bin/env python3
"""
Psalms 85 to 90. Six pages, 124 verses. All six outlines are gapless and are folded.

psalms89 closes Book III with the psalter's hardest problem stated at length: thirty-seven
verses rehearsing the covenant with David, then eight verses saying it has been broken, and
no answer. The doxology at verse 52 marks the end of the book rather than resolving the
psalm, and the section says so, because a reader who takes it as the poem's conclusion will
think a question has been answered that has not.

psalms88 is the one lament in the psalter that never turns. Every other complaint reaches
some statement of confidence; this one ends on the word darkness. The section says that
plainly rather than borrowing hope from its neighbours.

psalms90 opens Book IV, and the change of subject at that seam is deliberate: after the
collapse of the Davidic promise the psalter turns to a psalm of Moses about mortality and to
a run of psalms declaring that the LORD reigns.

Usage:
    python3 fold_psalms_085_090.py [--check]
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
"psalms85": [
 ("Thou Hast Been Favourable unto Thy Land (vv.1-3)",
  "LORD, thou hast been favourable unto thy land, thou hast brought back the captivity of Jacob. The psalm "
  "opens in the perfect tense with a restoration already granted, which is why it is usually read after the "
  "return from exile. And what is named as the substance of it is not territory but a closed account, thou "
  "hast forgiven the iniquity of thy people, thou hast covered all their sin."),
 ("Turn Us, O God of Our Salvation (vv.4-7)",
  "Turn us, O God of our salvation, and cause thine anger toward us to cease. The petition sits awkwardly "
  "with the previous section, since the anger was said to be turned away in verse 3, and the awkwardness is "
  "the psalm's actual situation: the return happened and the conditions did not improve. Then the question, "
  "wilt thou be angry with us for ever. And the request that follows is the one the psalm is remembered "
  "for, wilt thou not revive us again, that thy people may rejoice in thee."),
 ("I Will Hear What God the LORD Will Speak (v.8)",
  "I will hear what God the LORD will speak, for he will speak peace unto his people, and to his saints, "
  "but let them not turn again to folly. One verse, and it is the hinge: the psalm stops asking and starts "
  "listening. The last clause is a warning attached to the promise rather than a condition on it."),
 ("Mercy and Truth Are Met Together (vv.9-13)",
  "Surely his salvation is nigh them that fear him, that glory may dwell in our land. Then the verse this "
  "psalm is famous for, and it is four abstractions treated as people meeting, mercy and truth are met "
  "together, righteousness and peace have kissed each other. What the image claims is that qualities which "
  "pull against each other in ordinary government are reconciled here. And the next verse gives them a "
  "geography, truth shall spring out of the earth, and righteousness shall look down from heaven, so one "
  "comes up and the other comes down."),
],
"psalms86": [
 ("Bow Down Thine Ear, O LORD (vv.1-5)",
  "Bow down thine ear, O LORD, hear me, for I am poor and needy. The ground offered for the hearing is need "
  "rather than merit, which is the pattern of the whole psalm, and this is the only psalm in Book III "
  "attributed to David. Then a run of reasons, all of them about God's disposition, for thou, Lord, art "
  "good, and ready to forgive, and plenteous in mercy unto all them that call upon thee."),
 ("In the Day of My Trouble I Will Call (vv.6-7)",
  "Give ear, O LORD, unto my prayer, and attend to the voice of my supplications. Two verses, and the "
  "second states a policy rather than a request, in the day of my trouble I will call upon thee, for thou "
  "wilt answer me. The reason given for calling is the expectation of an answer, which is the psalter's "
  "ordinary logic."),
 ("Among the Gods There Is None Like unto Thee (vv.8-10)",
  "Among the gods there is none like unto thee, O Lord, neither are there any works like unto thy works. "
  "Then the widest claim in the psalm, all nations whom thou hast made shall come and worship before thee, "
  "and shall glorify thy name, which is stated as a future fact rather than a hope. Revelation 15:4 uses "
  "almost the same words."),
 ("Unite My Heart to Fear Thy Name (v.11)",
  "Teach me thy way, O LORD, I will walk in thy truth, unite my heart to fear thy name. One verse, and the "
  "petition in the last clause is the most searching in the psalm: what is asked for is not strength or "
  "rescue but an end to being divided. The Hebrew verb means to make one."),
 ("Thou Hast Delivered My Soul (vv.12-13)",
  "I will praise thee, O Lord my God, with all my heart, and the phrase answers verse 11 directly: a united "
  "heart is what a whole heart requires. Then the reason, for great is thy mercy toward me, and thou hast "
  "delivered my soul from the lowest hell, which reports a past rescue in the strongest available terms."),
 ("The Proud Are Risen Against Me (v.14)",
  "O God, the proud are risen against me, and the assemblies of violent men have sought after my soul, and "
  "have not set thee before them. One verse, and the trouble appears only here in seventeen verses. The "
  "last clause is the diagnosis of Psalm 10:4 and 54:3, and the psalm does not elaborate on the danger "
  "before moving on."),
 ("Full of Compassion, and Gracious (v.15)",
  "But thou, O Lord, art a God full of compassion, and gracious, longsuffering, and plenteous in mercy and "
  "truth. One verse, and it is a near-quotation of Exodus 34:6, the self-description God gives Moses on "
  "Sinai, which is quoted in this form at Psalm 103:8, Joel 2:13, Jonah 4:2 and Nehemiah 9:17. It is the "
  "nearest thing the Old Testament has to a creed, and here it is set against the single verse about the "
  "enemy."),
 ("Shew Me a Token for Good (vv.16-17)",
  "O turn unto me, and have mercy upon me, give thy strength unto thy servant. The last request is for "
  "something visible, shew me a token for good, that they which hate me may see it, and be ashamed. What is "
  "asked for is evidence rather than rescue, and the reason given is the effect on the onlookers of verse "
  "14."),
],
"psalms87": [
 ("His Foundation Is in the Holy Mountains (vv.1-3)",
  "His foundation is in the holy mountains, the LORD loveth the gates of Zion more than all the dwellings of "
  "Jacob. Three verses of civic praise, and the comparison in the middle is with the rest of Israel rather "
  "than with foreign cities. Glorious things are spoken of thee, O city of God."),
 ("This Man Was Born There (vv.4-6)",
  "This is the shortest psalm in the psalter and the strangest, and these three verses are why. I will make "
  "mention of Rahab and Babylon, and the names that follow are Philistia, Tyre and Ethiopia, which is to "
  "say Egypt and Israel's worst enemies. And what is said of them is a registration formula, this man was "
  "born there. Then, the LORD shall count when he writeth up the people, that this man was born there. "
  "Foreign nationals are being entered on Zion's birth register as natives, which is the boldest thing any "
  "psalm says about the nations, and it is said in seven verses without argument or explanation."),
 ("All My Springs Are in Thee (v.7)",
  "As well the singers as the players on instruments shall be there, all my springs are in thee. One verse "
  "to close, and it is textually difficult: the Hebrew is compressed and translators differ over who is "
  "speaking. What is clear is that the psalm ends with music and with water, which for a hill city with one "
  "spring is a claim about sufficiency."),
],
"psalms88": [
 ("O LORD God of My Salvation (vv.1-2)",
  "O LORD God of my salvation, I have cried day and night before thee. The title in the first line is the "
  "only positive thing in the psalm, and everything after it is complaint. Let my prayer come before thee, "
  "incline thine ear unto my cry, which is a request to be heard rather than helped."),
 ("My Life Draweth Nigh unto the Grave (vv.3-5)",
  "For my soul is full of troubles, and my life draweth nigh unto the grave. The condition is described as "
  "already counted among the dead, I am as a man that hath no strength, free among the dead, like the slain "
  "that lie in the grave. And the last clause is the psalm's characteristic note, whom thou rememberest no "
  "more."),
 ("Thou Hast Laid Me in the Lowest Pit (vv.6-8)",
  "Thou hast laid me in the lowest pit, in darkness, in the deeps. The agency is God's throughout this "
  "psalm and it is never softened, thy wrath lieth hard upon me, and thou hast afflicted me with all thy "
  "waves. Then the social consequence, thou hast put away mine acquaintance far from me, thou hast made me "
  "an abomination unto them, so even the isolation is attributed to God rather than to the friends."),
 ("Mine Eye Mourneth by Reason of Affliction (v.9)",
  "Mine eye mourneth by reason of affliction, LORD, I have called daily upon thee, I have stretched out my "
  "hands unto thee. One verse, and the gesture in the last clause is the psalter's standing posture of "
  "prayer, reported here as a daily practice that has not been answered."),
 ("Shall the Dead Arise and Praise Thee (vv.10-12)",
  "Wilt thou shew wonders to the dead, shall the dead arise and praise thee. Three verses of questions and "
  "they are the same argument Psalm 6:5 and Isaiah 38:18 make: a dead worshipper is no use. Shall thy "
  "lovingkindness be declared in the grave, or thy faithfulness in destruction. And the last question names "
  "the place where nothing is remembered, and thy righteousness in the land of forgetfulness."),
 ("Why Castest Thou Off My Soul (vv.13-14)",
  "But unto thee have I cried, O LORD, and in the morning shall my prayer prevent thee. Morning in the "
  "psalter is normally where relief arrives, as at 30:5, and here it is only where the prayer is filed "
  "again. Then the two questions, LORD, why castest thou off my soul, why hidest thou thy face from me."),
 ("I Have Been Afflicted from My Youth Up (vv.15-17)",
  "I am afflicted and ready to die from my youth up, while I suffer thy terrors I am distracted. The "
  "duration is the point: this is not a crisis but a life. And the imagery is of being surrounded, thy "
  "fierce wrath goeth over me, thy terrors have cut me off, they came round about me daily."),
 ("Mine Acquaintance into Darkness (v.18)",
  "Lover and friend hast thou put far from me, and mine acquaintance into darkness. This is the last verse "
  "of the psalm and the last word in the Hebrew is darkness. Every other lament in the psalter turns "
  "somewhere, even Psalm 44 asking for help and Psalm 77 choosing to remember. This one does not, and its "
  "presence in the collection is the psalter's admission that some prayers are recorded without an answer "
  "attached. It should not be read with hope borrowed from the psalms on either side of it."),
],
"psalms89": [
 ("I Will Sing of the Mercies of the LORD (vv.1-4)",
  "I will sing of the mercies of the LORD for ever, with my mouth will I make known thy faithfulness to all "
  "generations. The two words mercy and faithfulness recur through this psalm more than in any other, and "
  "they are the terms the covenant is measured by. Then the covenant is quoted immediately, I have made a "
  "covenant with my chosen, I have sworn unto David my servant, thy seed will I establish for ever. The "
  "psalm puts the promise on the table in its first four verses so that the last eight can be read against "
  "it."),
 ("Who in the Heaven Can Be Compared (vv.5-18)",
  "The heavens shall praise thy wonders, O LORD. Fourteen verses of hymn establishing the credentials of the "
  "one who made the promise, and the argument runs from the divine council down to the sea, who in the "
  "heaven can be compared unto the LORD, thou rulest the raging of the sea, thou hast broken Rahab in "
  "pieces. Then a verse that names the pairing the whole psalm turns on, justice and judgment are the "
  "habitation of thy throne, mercy and truth shall go before thy face. And the section ends on the people's "
  "position, blessed is the people that know the joyful sound."),
 ("I Have Found David My Servant (vv.19-37)",
  "Nineteen verses rehearsing the covenant in God's own voice, and it is the fullest statement of it in "
  "scripture outside 2 Samuel 7. I have found David my servant, with my holy oil have I anointed him. What "
  "is promised is stated in every direction: a hand established, enemies subdued, a father-son relationship, "
  "he shall cry unto me, Thou art my father. And then the clauses that make the next section a genuine "
  "crisis: if his children forsake my law, I will visit their transgression with the rod, nevertheless my "
  "lovingkindness will I not utterly take from him. The discipline is anticipated and the covenant is said "
  "to survive it, my covenant will I not break, nor alter the thing that is gone out of my lips, his seed "
  "shall endure for ever, and his throne as the sun."),
 ("But Thou Hast Cast Off (vv.38-45)",
  "But thou hast cast off and abhorred, thou hast been wroth with thine anointed. Eight verses that state "
  "the opposite of everything above them, and the verbs are all second person: thou hast made void the "
  "covenant of thy servant, thou hast profaned his crown by casting it to the ground, thou hast broken down "
  "all his hedges. The phrase made void the covenant is the sharpest in the psalter, since verse 34 has "
  "just said my covenant will I not break. The psalm sets the promise and its apparent cancellation "
  "twenty-five verses apart and does not reconcile them."),
 ("How Long, LORD (vv.46-51)",
  "How long, LORD, wilt thou hide thyself for ever, shall thy wrath burn like fire. Then the argument from "
  "mortality, remember how short my time is, wherefore hast thou made all men in vain. And the question "
  "that is the psalter's central problem stated in one line, Lord, where are thy former lovingkindnesses, "
  "which thou swarest unto David in thy truth. The psalm ends with the reproach of the enemies and no "
  "answer of any kind."),
 ("The Doxology Closing Book III (v.52)",
  "Blessed be the LORD for evermore, Amen, and Amen. This verse is not the psalm's conclusion. It is the "
  "doxology that closes Book III of the psalter, matching 41:13 and 72:19 at the ends of Books I and II, and "
  "it is editorial furniture rather than an answer. Read as the poem's last line it looks like the crisis "
  "resolving; read as what it is, the question of verse 49 is left open and the psalter's response to it is "
  "the next book, which opens with Moses on human mortality and then declares eleven times over that the "
  "LORD reigns."),
],
"psalms90": [
 ("Thou Hast Been Our Dwelling Place (vv.1-2)",
  "Lord, thou hast been our dwelling place in all generations. This is the only psalm attributed to Moses "
  "and it opens Book IV, immediately after the collapse of the Davidic promise in Psalm 89, which makes its "
  "placement an argument: the psalter answers a failed dynasty by going back past the monarchy altogether. "
  "And the timescale is set in the second verse, before the mountains were brought forth, from everlasting "
  "to everlasting, thou art God."),
 ("Thou Turnest Man to Destruction (vv.3-6)",
  "Thou turnest man to destruction, and sayest, Return, ye children of men. Then the comparison of "
  "durations, for a thousand years in thy sight are but as yesterday when it is past, and as a watch in "
  "the night, which 2 Peter 3:8 quotes. And the images for a human life are all short-lived plants, in the "
  "morning it flourisheth, and groweth up, in the evening it is cut down, and withereth."),
 ("We Spend Our Years as a Tale That Is Told (vv.7-11)",
  "For we are consumed by thine anger, and by thy wrath are we troubled. The psalm connects mortality to "
  "sin rather than treating it as neutral, thou hast set our iniquities before thee, our secret sins in "
  "the light of thy countenance. Then the arithmetic the psalm is best known for, the days of our years are "
  "threescore years and ten, and if by reason of strength they be fourscore years, yet is their strength "
  "labour and sorrow. And the question that follows is not rhetorical, who knoweth the power of thine "
  "anger."),
 ("Teach Us to Number Our Days (v.12)",
  "So teach us to number our days, that we may apply our hearts unto wisdom. One verse, and it is the "
  "psalm's only petition about the singer's own understanding. What is asked for is not more days but the "
  "ability to count the ones there are, which is the practical conclusion of everything above it."),
 ("Establish Thou the Work of Our Hands (vv.13-17)",
  "Return, O LORD, how long, and let it repent thee concerning thy servants. The petitions come in a run "
  "and they ask for satisfaction early rather than eventually, O satisfy us early with thy mercy, that we "
  "may rejoice and be glad all our days. Then a request for symmetry, make us glad according to the days "
  "wherein thou hast afflicted us, so the good years are asked for in the same measure as the bad. And the "
  "psalm ends on the one thing a mortal creature would most want, which is that the work should outlast "
  "the worker, and establish thou the work of our hands upon us, yea, the work of our hands establish thou "
  "it. The sentence is repeated because it is the whole request."),
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
