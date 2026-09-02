#!/usr/bin/env python3
"""
Folds the General Epistle openers onto the target Authorship format:
Hebrews 1, James 1, 1 Peter 1, 2 Peter 1 and 1 John 1.

Grouped because they share a shape. Each is the opening chapter of a letter and
each carried book-introduction fields with no per-passage exposition.

Existing fields are preserved verbatim. Recipient, Purpose, Theme and the
Hebrews-specific "Chapter 1:" all carry book-level substance that a generic
field would not improve on. Added are Classification, Key Themes, and the
verse-range sections these pages lacked.

Follows the format in WORKFLOW.md. Refuses to write on div imbalance.

Usage:
    python3 fold_openers_batch2.py [--check]
"""
import os
import re
import sys

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")

ITEM = ('                    <div class="auth-item">'
        '<span class="auth-label">{label}</span> {body}</div>')

WORK = {
"hebrews1": (
 "Epistle \u2014 Sermon or Treatise",
 "The Son as God&#x27;s final word, seven Old Testament citations establishing His "
 "superiority to angels, creation and inheritance held by the same person, and a "
 "throne that does not pass",
 [
  ("God Has Spoken by His Son (vv.1-2a)",
   "The letter opens without greeting, sender or addressee \u2014 unusual enough "
   "that many read it as a sermon later circulated as a letter. It begins instead "
   "with a contrast of revelation: God spoke \u201cat sundry times and in divers "
   "manners\u201d by the prophets, and has now spoken \u201cby his Son\u201d. The "
   "older revelation is not disparaged; it is described as partial and progressive, "
   "arriving in fragments. What follows is presented as the same God finishing a "
   "sentence He had been speaking for centuries."),
  ("Seven Things True of the Son (vv.2b-3)",
   "In two verses the writer stacks seven claims: heir of all things, agent of "
   "creation, the brightness of God's glory, the express image of His person, "
   "sustainer of all things by His word, the one who purged sins, and the one seated "
   "at the right hand of the Majesty on high. \u201cExpress image\u201d translates "
   "*charakt\u0113r*, the impression a die leaves on a coin \u2014 not a likeness but "
   "an exact stamp. The seated posture matters and will be pressed later in the "
   "letter: priests under the old covenant stood because their work was never "
   "finished."),
  ("Better Than the Angels (vv.4-9)",
   "The comparison with angels is not arbitrary. In Second Temple Judaism angels "
   "were held to have mediated the law at Sinai, so a claim that the Son surpasses "
   "them is a claim about the covenant He brings. The argument is made entirely from "
   "Scripture: Psalm 2:7, 2 Samuel 7:14, Psalm 97:7, Psalm 104:4 and Psalm 45:6-7 "
   "are cited in turn. Verse 6 has angels worshipping Him, and vv.8-9 address Him "
   "directly as God with an everlasting throne \u2014 the letter's boldest "
   "Christological move, and it is made by quotation rather than assertion."),
  ("The Unchanging Creator (vv.10-12)",
   "Psalm 102, addressed in its original setting to the LORD, is applied to the "
   "Son. The heavens are \u201cthe work of thy hands\u201d and will wear out like a "
   "garment to be folded away, while He remains the same. The point is permanence "
   "against transience, and it prepares the letter's recurring pastoral appeal: hold "
   "fast to what does not change, since everything the readers can see will."),
  ("The Question Left Hanging (vv.13-14)",
   "The chapter ends with Psalm 110:1 \u2014 sit at my right hand until I make thine "
   "enemies thy footstool \u2014 and a question no angel could be the answer to. "
   "Angels are then given their actual role, ministering spirits sent to serve those "
   "who will inherit salvation. The rhetorical effect is to leave the readers "
   "holding a comparison they cannot escape, which is exactly the pressure chapter 2 "
   "opens by applying."),
 ]),
"james1": (
 "Epistle \u2014 General, Wisdom",
 "Trials producing endurance, wisdom asked for in faith, the deceptive course from "
 "desire to death, every good gift coming down from above, and a faith measured by "
 "what it does",
 [
  ("Greeting to the Scattered Twelve Tribes (v.1)",
   "James identifies himself only as \u201ca servant of God and of the Lord Jesus "
   "Christ\u201d. Almost certainly the half-brother of Jesus and leader of the "
   "Jerusalem church, he claims no family relationship, exactly as Jude does. The "
   "addressees are \u201cthe twelve tribes which are scattered abroad\u201d, most "
   "naturally Jewish believers dispersed outside Judea, which suits the letter's "
   "assumed familiarity with synagogue life and the law."),
  ("Count It All Joy: Trials and Endurance (vv.2-4)",
   "The letter opens on hardship with no preamble. Joy is commanded not because "
   "trials are pleasant but because of what they produce \u2014 the testing of faith "
   "works patience, and patience left to finish its work produces maturity. The "
   "logic runs forward to an outcome rather than asking anyone to enjoy the process. "
   "Verse 4's \u201cperfect\u201d is completeness rather than flawlessness, the sense "
   "of something having reached its intended end."),
  ("Ask for Wisdom, Without Wavering (vv.5-8)",
   "Wisdom is the thing to ask for in the middle of trials, and the offer is "
   "generous \u2014 God gives \u201cliberally\u201d and without reproach, meaning "
   "without making the asker feel foolish for needing it. The condition is asking in "
   "faith without wavering, and the image for wavering is a wave driven by wind. The "
   "word rendered \u201cdouble minded\u201d in v.8 appears first here in surviving "
   "Greek and describes a person divided in two directions at once, which is the "
   "letter's diagnosis of much that follows."),
  ("Poverty, Riches, and the Withering Flower (vv.9-11)",
   "The low brother is told to glory in being lifted up and the rich in being made "
   "low, a reversal James returns to repeatedly. The grass and flower burned by the "
   "scorching wind is Isaiah 40's image, and the point is not that wealth is wicked "
   "but that it is temporary and a poor foundation for identity. In a letter "
   "addressed to scattered communities where economic pressure was real, this is "
   "pastoral rather than abstract."),
  ("Temptation: Desire, Sin, Death (vv.12-18)",
   "James separates trials that come from outside from temptation that works from "
   "within, and insists God tempts no one. The sequence in vv.14-15 is deliberate and "
   "almost clinical: desire conceives, brings forth sin, and sin brings forth death. "
   "Nothing about it is sudden. Against that he sets v.17, every good and perfect "
   "gift coming down from the Father \u201cwith whom is no variableness, neither "
   "shadow of turning\u201d \u2014 a God who does not shift, set against a desire "
   "that shifts constantly."),
  ("Swift to Hear: Doing the Word (vv.19-27)",
   "The practical turn the letter is known for. Swift to hear, slow to speak, slow "
   "to wrath; receive the word with meekness; and then the mirror \u2014 a man who "
   "hears without doing is like someone who looks at his face and immediately "
   "forgets it. The chapter closes by defining religion God accepts in terms that "
   "sidestep ritual entirely: bridling the tongue, visiting orphans and widows in "
   "their affliction, keeping oneself unspotted from the world. James is not opposing "
   "faith to works but insisting that a faith which changes nothing has not been "
   "described accurately."),
 ]),
"1peter1": (
 "Epistle \u2014 General",
 "A living hope through the resurrection, faith tested like gold, the salvation "
 "prophets searched into, holiness grounded in God&#x27;s character, redemption by "
 "precious blood, and new birth through an enduring word",
 [
  ("Elect Strangers Scattered Abroad (vv.1-2)",
   "Peter writes to believers across five Roman provinces in Asia Minor, calling "
   "them \u201cstrangers\u201d \u2014 resident aliens, people living somewhere they "
   "do not belong. That word governs the whole letter, which is written to "
   "Christians under social pressure and teaches them to understand their "
   "displacement rather than escape it. The greeting names Father, Spirit and Christ "
   "in one breath, tying election, sanctification and obedience together from the "
   "first sentence."),
  ("A Living Hope, an Inheritance Reserved (vv.3-5)",
   "The blessing that follows is one long sentence of confidence: begotten again to "
   "a living hope by the resurrection, to an inheritance incorruptible, undefiled and "
   "unfading, reserved in heaven. Each adjective denies a way earthly inheritance "
   "fails \u2014 it can decay, be polluted, or simply lose its shine. \u201cKept by "
   "the power of God\u201d in v.5 is a military term for a garrison, and it is the "
   "believers who are guarded, not only the inheritance."),
  ("Tested Faith, Inexpressible Joy (vv.6-9)",
   "The trials are conceded as real and grievous, and framed as temporary and "
   "purposeful: faith tried by fire as gold is, and gold perishes while faith does "
   "not. Verse 8 is remarkable for a letter written within living memory of Jesus "
   "\u2014 \u201cwhom having not seen, ye love\u201d. Peter had seen Him; his readers "
   "had not, and he treats their unseeing love as no lesser thing. The joy is called "
   "unspeakable and full of glory, language of something exceeding what can be "
   "reported."),
  ("What Prophets and Angels Longed to See (vv.10-12)",
   "The prophets who spoke of this grace searched their own writings to learn when "
   "and how it would come, testifying beforehand of \u201cthe sufferings of Christ, "
   "and the glory that should follow\u201d. That order \u2014 suffering then glory "
   "\u2014 is the pattern Peter will apply to his readers' own situation. The closing "
   "note that angels desire to look into these things puts the readers, ordinary "
   "people under local hostility, in possession of something the prophets awaited."),
  ("Be Holy, For He Is Holy (vv.13-16)",
   "The first imperative of the letter arrives only now, once the ground has been "
   "laid: gird up the loins of your mind, be sober, hope to the end. Holiness is "
   "commanded on the basis of God's character rather than on threat, quoting "
   "Leviticus \u2014 be holy, for I am holy. \u201cAs obedient children\u201d frames "
   "it as family resemblance. The former ignorance and its lusts are named as a life "
   "already left, not a temptation still being negotiated."),
  ("Redeemed by Precious Blood (vv.17-21)",
   "Redemption is described commercially and then the metaphor is broken: not with "
   "silver or gold, but with the precious blood of Christ, a lamb without blemish "
   "foreordained before the foundation of the world. The vanity of the fathers' "
   "tradition is named plainly, which for readers with deep inherited practice is a "
   "costly claim. Faith and hope are placed in God rather than in circumstance, "
   "because it is God who raised Him."),
  ("Born Again by the Enduring Word (vv.22-25)",
   "The chapter closes on love \u201cwith a pure heart fervently\u201d, grounded in "
   "new birth from incorruptible seed. Isaiah 40 returns \u2014 all flesh is grass, "
   "the flower falls, but the word of the Lord endures for ever. In a letter to "
   "people whose social standing was collapsing, the argument is that they have been "
   "born of the one thing in the passage that does not wither."),
 ]),
"2peter1": (
 "Epistle \u2014 General",
 "Everything needed for life and godliness already given, virtues added in "
 "sequence, a calling made sure, an eyewitness of the transfiguration, and "
 "prophecy that did not originate with its speakers",
 [
  ("Greeting: Like Precious Faith (vv.1-2)",
   "Peter writes as \u201ca servant and an apostle\u201d and addresses those who "
   "have obtained \u201clike precious faith\u201d \u2014 faith of equal standing "
   "with his own. For a letter that will spend chapter 2 attacking false teachers "
   "who claimed superior knowledge, beginning by levelling himself with his readers "
   "is a considered move. Grace and peace are wished \u201cthrough the knowledge of "
   "God\u201d, and knowledge is the word the whole letter contests."),
  ("All Things Given, Great Promises (vv.3-4)",
   "The claim is that divine power has already given everything pertaining to life "
   "and godliness. Nothing further is awaited and nothing secret is missing, which "
   "cuts directly against teachers offering hidden advancement. \u201cPartakers of "
   "the divine nature\u201d is strong language and is bounded by the same verse: it "
   "is the means of escaping corruption, not absorption into deity. The promises are "
   "called \u201cexceeding great and precious\u201d, and they are the mechanism, not "
   "a reward held in reserve."),
  ("Add to Your Faith: The Chain of Virtues (vv.5-9)",
   "Seven qualities are added in sequence \u2014 virtue, knowledge, temperance, "
   "patience, godliness, brotherly kindness, charity \u2014 each supplied on top of "
   "the last, with love at the end. The construction is deliberate: this is growth "
   "with an order rather than a checklist. Verse 8 makes the promise practical, that "
   "these things keep a believer from being barren or unfruitful, and v.9 gives the "
   "alternative bluntly \u2014 whoever lacks them is blind and has forgotten he was "
   "cleansed."),
  ("Make Your Calling Sure (vv.10-15)",
   "\u201cGive diligence to make your calling and election sure.\u201d The certainty "
   "in view is the believer's own assurance, evidenced by the growth just described, "
   "and the promise attached is that such a person will never fall. Peter then says "
   "plainly that he intends to keep reminding them as long as he is in \u201cthis "
   "tabernacle\u201d, and that he knows his death is near \u2014 which reads as a man "
   "deliberately leaving something behind. The letter is being written as a legacy."),
  ("We Were Eyewitnesses (vv.16-18)",
   "Against the charge of following \u201ccunningly devised fables\u201d Peter offers "
   "testimony: he was on the holy mount and heard the voice. The transfiguration is "
   "cited not as a mystical credential but as evidence in a dispute about "
   "reliability. He is a witness rather than a theorist, and the distinction is the "
   "point \u2014 the majesty he speaks of was seen with eyes."),
  ("Prophecy Not of Private Interpretation (vv.19-21)",
   "The written word is called \u201ca light that shineth in a dark place\u201d and "
   "in one sense preferred to his own experience, since it is available to every "
   "reader while the mount was not. Verse 20's \u201cprivate interpretation\u201d is "
   "most naturally about origin rather than reading method, as v.21 explains: "
   "prophecy came not by the will of man but as men spoke moved by the Holy Ghost. "
   "The argument sets a text with a divine source against teachers with only "
   "themselves to appeal to."),
 ]),
"1john1": (
 "Epistle \u2014 General",
 "The Word of life handled and heard, fellowship as the aim of testimony, God as "
 "light with no darkness in Him, walking in light as the ground of fellowship, and "
 "confession met with cleansing",
 [
  ("That Which We Have Heard and Handled (vv.1-2)",
   "Like the Fourth Gospel this letter begins \u201cfrom the beginning\u201d, but "
   "where the Gospel ascends to the Word with God, here the movement is toward the "
   "physical: heard, seen, looked upon, handled. The verbs accumulate deliberately "
   "against those denying that the Son truly came in flesh, the same error 2 John "
   "confronts. \u201cThe Word of life\u201d is both a message and a person, and the "
   "grammar keeps refusing to separate them. Verse 2 states that the life was "
   "manifested \u2014 made visible \u2014 and that the writer bears witness to it."),
  ("Declared So That You May Have Fellowship (vv.3-4)",
   "The purpose of the testimony is stated before any doctrine is argued: that you "
   "may have fellowship with us, and our fellowship is with the Father and with His "
   "Son. *Koin\u014dnia* is partnership and shared life rather than sociability. "
   "Note the direction \u2014 the apostolic witness exists to bring readers into "
   "something, not to establish the writer's standing. Verse 4 adds a second aim, "
   "that \u201cyour joy may be full\u201d, which sits oddly with how sternly the "
   "letter can read until you notice it recurring."),
  ("God Is Light (v.5)",
   "The message is compressed into one clause: God is light, and in Him is no "
   "darkness at all. The double negative in the Greek is emphatic, allowing no "
   "shadow, no mixture, no region of God that is other than what He has revealed. "
   "Everything the letter goes on to say about sin, obedience and love is measured "
   "against this single statement, which is why it is placed before any of it."),
  ("Walking in Light, Not Merely Claiming It (vv.6-7)",
   "Two conditional sentences set claim against conduct. Saying we have fellowship "
   "with Him while walking in darkness is named a lie. Walking in the light produces "
   "two results together \u2014 fellowship with one another, and cleansing by the "
   "blood of Jesus. The second is worth pausing on: walking in the light is not the "
   "state of having no sin to cleanse, but the state in which cleansing is happening. "
   "Light is where sin is dealt with rather than where it is absent."),
  ("If We Confess: Three Claims Answered (vv.8-10)",
   "The chapter closes by refuting three self-assessments. Saying we have no sin is "
   "self-deception. Saying we have not sinned makes God a liar and shows His word is "
   "not in us. Between them stands v.9, the promise: if we confess, He is faithful "
   "and just to forgive and to cleanse. Faithful and *just* is the striking pair "
   "\u2014 forgiveness is presented as God being righteous rather than lenient, "
   "because the ground of it was established elsewhere. Confession is agreement with "
   "what God has already said, which is why it opens the way."),
 ]),
}


def main():
    check = "--check" in sys.argv
    changed = 0
    problems = []

    for page, (genre, themes, sections) in sorted(WORK.items()):
        path = os.path.join(DOCS, f"{page}.html")
        html = open(path, encoding="utf-8").read()

        pane = re.search(r'(id="tab-authorship">)(.*?)(?=<div class="tab-content")',
                         html, re.S)
        if not pane:
            problems.append(f"{page}: no authorship pane")
            continue

        existing = re.findall(r'<div class="auth-item">.*?</div>', pane.group(2), re.S)
        if not existing:
            problems.append(f"{page}: no existing auth-items to preserve")
            continue

        parts = ["\n                <h3>Authorship &amp; Background</h3>\n"]
        for item in existing:
            parts.append("                " + item + "\n")
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

        changed += 1
        if not check:
            open(path, "w", encoding="utf-8").write(new)

    verb = "would fold" if check else "folded"
    print(f"{verb} {changed} General Epistle openers")
    for p in problems:
        print(f"    {p}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
