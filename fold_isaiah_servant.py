#!/usr/bin/env python3
"""
Isaiah 49 to 53: the second, third and fourth servant songs. Five pages, 87 verses.

Four of the five outlines fold as they stand. isaiah53's opened with an item labelled
[52:13-15] The Servant Exalted Yet Marred, which is a cross-reference to the previous
chapter rather than a section of this one, and it carried no verse range. It is dropped,
because the material it points at is covered in its proper place on the isaiah52 page,
and a section on this page would leave the reference dangling.

The fourth servant song runs from 52:13 to 53:12 and crosses the chapter break, which is
why the inherited outline tried to reach backwards. The sections keep each page's own
verses and the isaiah52 note says where the song begins.

Usage:
    python3 fold_isaiah_servant.py [--check]
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
"isaiah49": [
 ("Called from the Womb (vv.1-6)",
  "The second servant song, and this time the servant speaks. Listen, O isles, unto me, and hearken, ye "
  "people, from far, the LORD hath called me from the womb. The equipment described is entirely verbal, "
  "he hath made my mouth like a sharp sword, and he hath made me a polished shaft. Then the admission "
  "that makes this song different from the first, I have laboured in vain, I have spent my strength for "
  "nought. And the answer enlarges the job rather than easing it: it is a light thing that thou shouldest "
  "be my servant to raise up the tribes of Jacob, I will also give thee for a light to the Gentiles, that "
  "thou mayest be my salvation unto the end of the earth. Note verse 3 calls the servant Israel and verse "
  "5 gives him the task of bringing Jacob back, which is the tension these songs never fully resolve."),
 ("Kings Shall See and Arise (v.7)",
  "One verse, and it puts the two halves of the servant's position side by side without transition. To "
  "him whom man despiseth, to him whom the nation abhorreth, to a servant of rulers, and then, kings "
  "shall see and arise, princes also shall worship. The despising is stated first and in three forms, so "
  "the honour that follows is not offered as compensation but as an outcome, and the reason given is "
  "external to the servant altogether, because of the LORD that is faithful."),
 ("In an Acceptable Time (vv.8-13)",
  "Thus saith the LORD, In an acceptable time have I heard thee, and in a day of salvation have I helped "
  "thee, which Paul quotes in 2 Corinthians 6:2 and applies to the present. The commission is stated in "
  "the same terms as 42:6, I will give thee for a covenant of the people, and the work is release, that "
  "thou mayest say to the prisoners, Go forth, to them that are in darkness, Shew yourselves. Then the "
  "journey home described as pasture, they shall feed in the ways, and their pastures shall be in all "
  "high places, they shall not hunger nor thirst, neither shall the heat nor sun smite them, which "
  "Revelation 7:16 takes up almost word for word."),
 ("Zion Hath Said, The LORD Hath Forsaken Me (v.14)",
  "One verse, and it is the complaint the rest of the chapter answers. But Zion said, The LORD hath "
  "forsaken me, and my Lord hath forgotten me. Two verbs, forsaken and forgotten, and the second is the "
  "one the following verses take up. It is worth noticing that the objection is given a verse of its own "
  "and quoted without correction before anything is said to it."),
 ("Can a Woman Forget Her Sucking Child (vv.15-16)",
  "Can a woman forget her sucking child, that she should not have compassion on the son of her womb, yea, "
  "they may forget, yet will I not forget thee. The argument is from the strongest natural bond available "
  "and then it concedes that even that bond fails, which is more honest than the comparison required. "
  "Then the image the section is remembered for, behold, I have graven thee upon the palms of my hands, "
  "thy walls are continually before me. Engraving rather than writing, so it cannot be rubbed out, and on "
  "the palms, so it cannot be out of sight."),
 ("Thy Children Shall Come (vv.17-26)",
  "Thy children shall make haste, thy destroyers and they that made thee waste shall go forth of thee. "
  "The city is told to look at a crowd she cannot account for, lift up thine eyes round about, and "
  "behold, and her reaction is quoted, who hath begotten me these, seeing I have lost my children, and am "
  "desolate, who hath brought up these. Then the foreign kings put to work, and kings shall be thy "
  "nursing fathers, and their queens thy nursing mothers. And the closing verses answer the question of "
  "whether a captor can be made to give anything back, shall the prey be taken from the mighty, or the "
  "lawful captive delivered, with the answer that the mighty will be made to hand them over."),
],
"isaiah50": [
 ("Where Is the Bill of Divorce (vv.1-3)",
  "Thus saith the LORD, Where is the bill of your mother's divorcement, whom I have put away. The question "
  "is legal and the point of it is that no such document exists, so the separation was never formalised. "
  "Then the same argument about debt, or which of my creditors is it to whom I have sold you. And the "
  "reason given for the exile is put back on the people, behold, for your iniquities have ye sold "
  "yourselves. The section closes with two questions about capacity, is my hand shortened at all, that it "
  "cannot redeem, or have I no power to deliver."),
 ("The Lord GOD Hath Opened Mine Ear (vv.4-9)",
  "The third servant song, and it is the shortest and most physical. It begins with a trained ear rather "
  "than a trained tongue, he wakeneth morning by morning, he wakeneth mine ear to hear as the learned. "
  "Then what obedience cost, listed as three assaults, I gave my back to the smiters, and my cheeks to "
  "them that plucked off the hair, I hid not my face from shame and spitting. And the response is not "
  "resistance but posture, therefore have I set my face like a flint. The last verses are courtroom "
  "language, he is near that justifieth me, who will contend with me, let us stand together, who is mine "
  "adversary, let him come near to me."),
 ("Who Kindle a Fire (vv.10-11)",
  "Who is among you that feareth the LORD, that obeyeth the voice of his servant, that walketh in "
  "darkness, and hath no light, let him trust in the name of the LORD, and stay upon his God. Walking in "
  "the dark is described as a condition consistent with obedience rather than as evidence against it. "
  "Then the alternative in the last verse, and it is one of the sharpest images in the book, behold, all "
  "ye that kindle a fire, that compass yourselves about with sparks, walk in the light of your fire, and "
  "in the sparks that ye have kindled. Making your own light in the dark is permitted and its outcome is "
  "stated, this shall ye have of mine hand, ye shall lie down in sorrow."),
],
"isaiah51": [
 ("Look unto Abraham (vv.1-3)",
  "Hearken to me, ye that follow after righteousness, look unto the rock whence ye are hewn, and to the "
  "hole of the pit whence ye are digged. Then the rock is identified and it is a person, look unto "
  "Abraham your father, and unto Sarah that bare you, for I called him alone, and blessed him, and "
  "increased him. The argument is arithmetical and it is aimed at a small and discouraged community: the "
  "nation began with one childless couple. And the promise is horticultural, he will make her wilderness "
  "like Eden, and her desert like the garden of the LORD."),
 ("My Righteousness Is Near (vv.4-6)",
  "Hearken unto me, my people, and give ear unto me, O my nation, for I will make my judgment to rest for "
  "a light of the people. Then a comparison of durabilities, lift up your eyes to the heavens, and look "
  "upon the earth beneath, for the heavens shall vanish away like smoke, and the earth shall wax old like "
  "a garment. Against that, my salvation shall be for ever, and my righteousness shall not be abolished. "
  "The two things a person would call permanent are the two things named as temporary."),
 ("Fear Ye Not the Reproach of Men (vv.7-8)",
  "Hearken unto me, ye that know righteousness, the people in whose heart is my law, fear ye not the "
  "reproach of men, neither be ye afraid of their revilings. The threat being dismissed is verbal rather "
  "than military, which suits a community under contempt rather than under siege. And the reason is the "
  "grass argument of 40:6 in a domestic form, for the moth shall eat them up like a garment, and the worm "
  "shall eat them like wool."),
 ("Awake, O Arm of the LORD (vv.9-11)",
  "Awake, awake, put on strength, O arm of the LORD, awake, as in the ancient days. The prayer wakes God "
  "rather than the people, which reverses the imperatives of the next chapter, and the precedent it cites "
  "is mythological and historical at once, art thou not it that hath cut Rahab, and wounded the dragon, "
  "art thou not it which hath dried the sea. Rahab is the sea monster of Job 26 and Psalm 89, and the "
  "same sentence goes straight on to the exodus, so the two are treated as one act. And the section "
  "closes with 35:10 quoted word for word, and sorrow and mourning shall flee away."),
 ("I, Even I, Am He That Comforteth You (vv.12-16)",
  "I, even I, am he that comforteth you, who art thou that thou shouldest be afraid of a man that shall "
  "die, and of the son of man which shall be made as grass. The question is put as a matter of "
  "proportion. Then the diagnosis of what fear does to memory, and forgettest the LORD thy maker, and "
  "hast feared continually every day because of the fury of the oppressor. And a clause that answers the "
  "fear with an absence, where is the fury of the oppressor. The section closes with words put in the "
  "prophet's mouth, I have put my words in thy mouth, and have covered thee in the shadow of mine hand."),
 ("The Cup Taken Out of Thy Hand (vv.17-23)",
  "Awake, awake, stand up, O Jerusalem, which hast drunk at the hand of the LORD the cup of his fury. The "
  "cup of Jeremiah 25 and Ezekiel 23 is here in the hand of Jerusalem herself and she is described as "
  "drunk in the street with nobody to help her up. Then the reversal, and it is a transfer rather than a "
  "cancellation, behold, I have taken out of thine hand the cup of trembling, thou shalt no more drink it "
  "again, and I will put it into the hand of them that afflict thee. And the reason those are named is "
  "quoted, they that have said to thy soul, Bow down, that we may go over, and thou hast laid thy body as "
  "the ground, and as the street, to them that went over."),
],
"isaiah52": [
 ("Awake, Put on Thy Strength (vv.1-2)",
  "Awake, awake, put on thy strength, O Zion, put on thy beautiful garments, O Jerusalem. The imperatives "
  "are the same ones addressed to God's arm at 51:9, now turned round on the city, so the chapter answers "
  "the previous prayer by handing the instruction back. And the two commands are about clothing and "
  "posture, shake thyself from the dust, arise, and sit down, O Jerusalem, loose thyself from the bands "
  "of thy neck."),
 ("Sold for Nothing (vv.3-6)",
  "For thus saith the LORD, Ye have sold yourselves for nothing, and ye shall be redeemed without money. "
  "The transaction is described as worthless in both directions, which is the argument of 50:1 restated. "
  "Then the history is summarised in one verse, my people went down aforetime into Egypt to sojourn "
  "there, and the Assyrian oppressed them without cause. And the reason for acting is the one Ezekiel 36 "
  "gives, for my name continually every day is blasphemed."),
 ("How Beautiful Are the Feet (vv.7-8)",
  "How beautiful upon the mountains are the feet of him that bringeth good tidings, that publisheth "
  "peace, that saith unto Zion, Thy God reigneth. What is being described is a runner arriving in sight "
  "of a city that has been waiting for news, and the beauty is assigned to the feet because they are what "
  "the watchers see first over the ridge. Paul quotes the verse in Romans 10:15 of preaching. And the "
  "watchmen answer with their own voices, with the voice together shall they sing, for they shall see eye "
  "to eye, when the LORD shall bring again Zion."),
 ("Break Forth into Joy (vv.9-10)",
  "Break forth into joy, sing together, ye waste places of Jerusalem, for the LORD hath comforted his "
  "people, he hath redeemed Jerusalem. The ruins are told to sing, which is the same device as 44:23 and "
  "49:13. And the image in the second verse is military and public, the LORD hath made bare his holy arm "
  "in the eyes of all the nations, that is, pushed back the sleeve, and all the ends of the earth shall "
  "see the salvation of our God."),
 ("Depart Ye, Depart Ye (vv.11-12)",
  "Depart ye, depart ye, go ye out from thence, touch no unclean thing, be ye clean, that bear the "
  "vessels of the LORD. Paul quotes the middle clause in 2 Corinthians 6:17. What is unusual is the "
  "contrast drawn with the first exodus in the next verse, for ye shall not go out with haste, nor go by "
  "flight. The escape from Egypt was eaten standing up with the belt fastened; this departure is "
  "described as unhurried, and the reason is that the LORD will go before you, and the God of Israel will "
  "be your rereward, which is the rear guard."),
 ("Behold, My Servant Shall Deal Prudently (vv.13-15)",
  "The fourth and longest servant song begins here rather than at the chapter break, and runs to the end "
  "of chapter 53. Behold, my servant shall deal prudently, he shall be exalted and extolled, and be very "
  "high. Then the disfigurement, stated immediately after the exaltation and in the same breath, his "
  "visage was so marred more than any man, and his form more than the sons of men. And the reaction of "
  "the nations, so shall he sprinkle many nations, the kings shall shut their mouths at him. Paul quotes "
  "the last verse in Romans 15:21 as his reason for preaching where the news had not gone, for that which "
  "they had not heard shall they consider."),
],
"isaiah53": [
 ("Who Hath Believed Our Report (vv.1-3)",
  "Who hath believed our report, and to whom is the arm of the LORD revealed. The chapter opens with a "
  "question about reception rather than about the servant, and John 12:38 and Romans 10:16 both quote it "
  "to explain unbelief. Then the appearance, and there is nothing in it to attract anyone, for he shall "
  "grow up before him as a tender plant, and as a root out of a dry ground, he hath no form nor "
  "comeliness, and when we shall see him, there is no beauty that we should desire him. And the social "
  "position, he is despised and rejected of men, a man of sorrows, and acquainted with grief, with a "
  "final clause about the observers rather than the sufferer, we hid as it were our faces from him."),
 ("He Was Wounded for Our Transgressions (vv.4-6)",
  "Surely he hath borne our griefs, and carried our sorrows, yet we did esteem him stricken, smitten of "
  "God, and afflicted. The correction is in the word yet: the onlookers drew the obvious conclusion, that "
  "the suffering was deserved, and were wrong. Then the substitution stated four ways in one verse, he "
  "was wounded for our transgressions, he was bruised for our iniquities, the chastisement of our peace "
  "was upon him, and with his stripes we are healed. And the verdict on the observers is the widest "
  "sentence in the chapter, all we like sheep have gone astray, we have turned every one to his own way, "
  "and the LORD hath laid on him the iniquity of us all."),
 ("As a Sheep Before Her Shearers (vv.7-9)",
  "He was oppressed, and he was afflicted, yet he opened not his mouth, he is brought as a lamb to the "
  "slaughter, and as a sheep before her shearers is dumb, so he openeth not his mouth. This is the "
  "passage the Ethiopian official is reading in Acts 8 when Philip finds him, and his question is the "
  "obvious one: of whom speaketh the prophet this, of himself, or of some other man. Then the burial, and "
  "he made his grave with the wicked, and with the rich in his death, and the reason it is called unjust "
  "is stated plainly, because he had done no violence, neither was any deceit in his mouth."),
 ("He Shall See His Seed (vv.10-12)",
  "Yet it pleased the LORD to bruise him, he hath put him to grief, which is the hardest clause in the "
  "chapter and it is not softened. Then the term for what the death is, when thou shalt make his soul an "
  "offering for sin, and the word is asham, the guilt offering of Leviticus 5. What follows is stated as "
  "outcome rather than as hope, he shall see his seed, he shall prolong his days, he shall see of the "
  "travail of his soul, and shall be satisfied. And the last verse states the exchange twice, therefore "
  "will I divide him a portion with the great, because he hath poured out his soul unto death, and he was "
  "numbered with the transgressors, and he bare the sin of many, and made intercession for the "
  "transgressors. Jesus quotes the phrase about being numbered with the transgressors of himself in "
  "Luke 22:37."),
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
