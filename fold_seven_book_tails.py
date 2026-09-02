#!/usr/bin/env python3
"""
Finishes the seven books that the conformance audit leaves one to five pages short:
Job, 2 Samuel, Ruth, Titus, Colossians, 1 Peter and 1 Thessalonians. Twelve pages,
each missing between four and ten verses.

The gaps are not random. They fall in three places:

  Speech openings. job34 vv.1-4 and job35 vv.1-4 are Elihu clearing his throat,
  'Hear my words, O ye wise men', which an earlier pass skipped as preamble. They
  are part of the speech and are taken into the first section.

  The middle of an argument. job22 vv.15-20 on the way of the wicked, job33
  vv.12-13 and vv.29-33, job34 vv.31-33, 2samuel12 vv.7-12 which is the whole
  point of Nathan's visit, 2samuel22 vv.8-16 which is the theophany the psalm is
  built around, ruth4 vv.9-12 where the witnesses answer. These get sections of
  their own.

  Letter closings. titus3 vv.12-15, 1peter5 vv.12-14, 1thessalonians5 vv.25-28.
  Greetings and travel arrangements are easy to treat as filler, and they carry
  the names of the people the letters actually moved through: Artemas, Tychicus,
  Zenas, Silvanus, Mark.

job19 vv.23-27 is the largest omission of the twelve and the least defensible. It
is 'I know that my redeemer liveth', the high point of the book.

colossians2 needed a different repair. It carried four fields all labelled
'Warning:', with the real heading buried at the start of each body, so the page
had one label repeated four times and eight verses uncovered. The four are
relabelled from their own text (Philosophy v.8, Legalism vv.16-17, Mysticism
vv.18-19, Asceticism vv.20-23) and the duplicated lead is taken off each body.
Because the philosophy warning is verse 8, the sufficiency section that spanned
vv.1-15 is narrowed to vv.1-7 and vv.9-15 so the verse is not described twice.

Usage:
    python3 fold_seven_book_tails.py [--check]
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
RANGE_IN_LABEL = re.compile(r"\(vv?\.[^)]*\)(?=\s*:?\s*$)")

OPS = {
"job19": [
 ("insert", "Total Abandonment", "I Know That My Redeemer Lives (vv.23-27)",
  "Job asks for his words to be written, printed in a book, graven with an iron pen and "
  "lead in the rock for ever. He wants a record that will outlast the argument, because he "
  "expects to lose it. Then, from a man who has just said God has put his brethren far "
  "from him, the sentence the whole book is remembered for: I know that my redeemer "
  "liveth, and that he shall stand at the latter day upon the earth. The word is goel, the "
  "kinsman whose duty is to buy back what his relative has lost, the office Boaz takes up "
  "in Ruth. And though after my skin worms destroy this body, yet in my flesh shall I see "
  "God. He does not argue for it and does not explain how it fits what he has just said "
  "about being abandoned. He simply knows it."),
],
"job22": [
 ("insert", "Eliphaz's Accusation of Deism",
  "The Way of the Wicked and the Righteous Who Watch (vv.15-20)",
  "Hast thou marked the old way which wicked men have trodden? Eliphaz turns to precedent, "
  "and the men he cites are the generation of the flood, which was cut down out of time, "
  "whose foundation was overflown with a flood. Their words are quoted, Depart from us, and "
  "what can the Almighty do for them? and then answered by the fact that he had filled "
  "their houses with good things. The passage ends somewhere ugly, the righteous see it, "
  "and are glad, and the innocent laugh them to scorn. Eliphaz is describing what he "
  "expects to feel when Job's ruin is complete."),
],
"job33": [
 ("insert", "Elihu Quotes Job", "God Is Greater Than Man (vv.12-13)",
  "Behold, in this thou art not righteous, I will answer thee, that God is greater than "
  "man. Elihu has quoted Job accurately and now gives his one-line refutation, and it is "
  "not an argument so much as a statement of scale. Then the question he thinks Job's "
  "complaint amounts to, why dost thou strive against him? for he giveth not account of "
  "any of his matters."),
 ("insert", "The Mediating Angel", "Twice, Even Three Times (vv.29-33)",
  "Lo, all these things worketh God oftentimes with man. The dream, the pain and the "
  "messenger are gathered up as one repeated method rather than three separate ones, and "
  "the purpose is stated, to bring back his soul from the pit, that he may be enlightened "
  "with the light of the living. Then Elihu turns from theology to procedure and offers Job "
  "the floor: mark well, O Job, hearken unto me, hold thy peace, and I will speak. If thou "
  "hast anything to say, answer me, speak, for I desire to justify thee. Of the four "
  "speakers in the book he is the only one who says that."),
],
"job34": [
 ("extend", "Elihu Quotes Job", "(vv.1-9)",
  "Furthermore Elihu answered and said, Hear my words, O ye wise men, and give ear unto me, "
  "ye that have knowledge. He addresses the three friends rather than Job for these opening "
  "verses, and the standard he proposes is a good one: for the ear trieth words, as the "
  "mouth tasteth meat. Let us choose to us judgment, let us know among ourselves what is "
  "good."),
 ("insert", "God's Sovereignty Over All", "Should God Repay on Your Terms (vv.31-33)",
  "Elihu puts a speech in the mouth of a repentant man, I have borne chastisement, I will "
  "not offend any more, that which I see not teach thou me. It is a model confession, and "
  "it is offered as what Job has not said. Then the question, should it be according to thy "
  "mind? and the challenge with it, thou refusedst, therefore choose thou what thou wilt "
  "speak. He is telling Job that asking God to answer on Job's terms is the refusal, not the "
  "remedy."),
],
"job35": [
 ("extend", "God's Self-Sufficiency", "(vv.1-8)",
  "Elihu spake moreover, and the section opens with the position he intends to demolish, "
  "put in Job's mouth: thou saidst, My righteousness is more than God's. Then the second "
  "quotation, what profit shall I have if I be cleansed from my sin? He undertakes to answer "
  "both, and thy companions with thee, which keeps the friends inside the reply."),
],
"2samuel12": [
 ("insert", "Nathan's Parable", "Thou Art the Man (vv.7-12)",
  "Nathan has told a story about a stolen lamb and David has passed sentence on the man in "
  "it. Then four words turn the sentence around, thou art the man. What follows is the "
  "indictment in God's own voice and it begins with gifts rather than accusations: I "
  "anointed thee king, I delivered thee out of the hand of Saul, I gave thee thy master's "
  "house, and if that had been too little, I would moreover have given unto thee such and "
  "such things. Then the charge, wherefore hast thou despised the commandment of the LORD? "
  "with Uriah named twice. The sentence has two halves and both are about the house rather "
  "than the man: the sword shall never depart from thine house, and I will raise up evil "
  "against thee out of thine own house. Thou didst it secretly, but I will do this thing "
  "before all Israel. Absalom is in that sentence before he has done anything."),
],
"2samuel22": [
 ("insert", "Distress and Cry for Help", "The Theophany (vv.8-16)",
  "David has described drowning and calling out, and the answer is not described as help "
  "arriving but as the world coming apart. The earth shook and trembled, the foundations of "
  "heaven moved. Then smoke out of his nostrils and fire out of his mouth, and he bowed the "
  "heavens and came down, and darkness was under his feet. He rode upon a cherub, and did "
  "fly, and he was seen upon the wings of the wind. Thunder, arrows, lightning, and then the "
  "sea itself pulled back, the channels of the sea appeared, the foundations of the world "
  "were discovered. Nine verses of storm for one man in trouble, which is the psalm's way "
  "of saying what the rescue cost the one who came."),
],
"ruth4": [
 ("insert", "The Sandal Ceremony", "Ye Are Witnesses (vv.9-12)",
  "Boaz states the transaction aloud so that it cannot be undone. Ye are witnesses this "
  "day, that I have bought all that was Elimelech's, and Chilion's, and Mahlon's. Then Ruth "
  "is named in the same legal breath as the field, and the purpose is given, to raise up the "
  "name of the dead upon his inheritance, that the name of the dead be not cut off from "
  "among his brethren. The elders answer with a blessing, and the three women they choose "
  "are pointed: Rachel and Leah, who between them built the house of Israel, and Tamar, who "
  "bore Perez to Judah by a levirate claim she had to force. A Moabite widow is being placed "
  "in that line by the town that had every reason to exclude her."),
],
"titus3": [
 ("insert", "Good Works and Divisive People", "Travel Plans and Final Greeting (vv.12-15)",
  "The letter ends in logistics, which is where the shape of the work shows. Artemas or "
  "Tychicus will be sent so that Titus can leave Crete and come to Nicopolis for the "
  "winter, meaning the man is not being left there permanently. Zenas the lawyer and Apollos "
  "are to be sent on their journey diligently, that nothing be wanting unto them. Then the "
  "instruction that ties the arrangements back to the letter's argument, let ours also learn "
  "to maintain good works for necessary uses, that they be not unfruitful. Grace be with you "
  "all."),
],
"colossians2": [
 ("fix_body", "Historical Context", "you are COMPLETE in Christ",
  "you are complete in Christ"),
 ("extend", "Christ's Sufficiency", "(vv.1-7,9-15)",
  "The verse on philosophy inside this passage is taken up on its own below, because Paul "
  "makes it the first of four named threats."),
 ("relabel_nth", "Warning", 0, "Philosophy (v.8)", "Philosophy (v.8): "),
 ("relabel_nth", "Warning", 0, "Legalism (vv.16-17)", "Legalism (vv.16-17): "),
 ("relabel_nth", "Warning", 0, "Mysticism (vv.18-19)", "Mysticism (vv.18-19): "),
 ("relabel_nth", "Warning", 0, "Asceticism (vv.20-23)", "Asceticism (vv.20-23): "),
],
"1peter5": [
 ("extend", "Promise of Restoration", "(vv.10-11)",
  "The promise closes with a doxology of six words, to him be glory and dominion for ever "
  "and ever, amen. It is put immediately after a sentence about suffering a while, which is "
  "how the letter has handled the pairing throughout."),
 ("insert", "Promise of Restoration", "Silvanus, Babylon, and a Kiss of Love (vv.12-14)",
  "By Silvanus, a faithful brother unto you, as I suppose, I have written briefly. The "
  "letter names its carrier, and Silvanus is the Silas who travelled with Paul, which places "
  "this letter inside a network rather than at the end of one man's desk. The purpose is "
  "stated in one clause, testifying that this is the true grace of God wherein ye stand. The "
  "church that sendeth greeting is at Babylon, which almost certainly means Rome under a "
  "name borrowed from the exile, and Marcus my son is with him, the Mark of the second "
  "Gospel. Greet ye one another with a kiss of charity. Peace be with you all that are in "
  "Christ Jesus."),
],
"1thessalonians5": [
 ("extend", "Final Prayer", "(vv.23-28)",
  "Then four short requests that are easy to read past. Brethren, pray for us, which is the "
  "apostle asking rather than instructing. Greet all the brethren with an holy kiss. Then an "
  "unusual one, I charge you by the Lord that this epistle be read unto all the holy "
  "brethren, put under oath, because a letter left with the leadership is not the same thing "
  "as a letter read to the congregation. And the closing line, the grace of our Lord Jesus "
  "Christ be with you."),
],
}


def find(items, prefix, skip=0):
    for i, (label, _) in enumerate(items):
        if H.unescape(label).strip().startswith(prefix):
            if skip == 0:
                return i
            skip -= 1
    return -1


def main():
    check = "--check" in sys.argv
    planned, problems, notes = {}, [], []
    for page, ops in OPS.items():
        path = os.path.join(DOCS, page + ".html")
        html = open(path, encoding="utf-8").read()
        pane = PANE.search(html)
        if not pane:
            problems.append(f"{page}: no authorship pane")
            continue
        items = [[a, b.strip()] for a, b in ITEM_RE.findall(pane.group(2))]
        used = 0
        for op in ops:
            kind = op[0]
            if kind == "extend":
                _, prefix, rng, prose = op
                i = find(items, prefix)
                if i < 0:
                    problems.append(f"{page}: extend target {prefix!r} not found")
                    continue
                new_label, n = RANGE_IN_LABEL.subn(rng, items[i][0])
                if not n:
                    problems.append(f"{page}: no range in label {prefix!r}")
                    continue
                items[i][0] = new_label
                items[i][1] += " " + prose
                notes.append(f"{page}: extended {prefix!r} to {rng}")
            elif kind == "insert":
                _, after, label, prose = op
                at = find(items, after)
                if at < 0:
                    problems.append(f"{page}: insert anchor {after!r} not found")
                    continue
                items.insert(at + 1, [label + ":", prose])
                notes.append(f"{page}: inserted {label!r}")
            elif kind == "relabel_nth":
                _, prefix, skip, label, strip = op
                i = find(items, prefix, skip)
                if i < 0:
                    problems.append(f"{page}: relabel {prefix!r} #{used} not found")
                    continue
                body = items[i][1]
                plain = H.unescape(re.sub(r"<.*?>", "", body))
                if not plain.startswith(strip):
                    problems.append(f"{page}: body does not start with {strip!r}")
                    continue
                items[i][0] = label + ":"
                items[i][1] = body[body.index(strip.rstrip()) + len(strip.rstrip()):].lstrip(": ").strip()
                used += 1
                notes.append(f"{page}: relabelled a Warning to {label!r}")
            elif kind == "fix_body":
                _, prefix, old_s, new_s = op
                i = find(items, prefix)
                if i < 0 or old_s not in items[i][1]:
                    problems.append(f"{page}: fix_body target {old_s!r} not found")
                    continue
                items[i][1] = items[i][1].replace(old_s, new_s)
                notes.append(f"{page}: repaired {old_s!r}")
        parts = ["\n                <h3>Authorship &amp; Background</h3>\n"]
        for label, body in items:
            parts.append(ITEM.format(label=label, body=body) + "\n")
        new_body = "".join(parts) + "            </div>\n\n            "
        new = html[:pane.start(2)] + new_body + html[pane.end(2):]
        o, c = len(re.findall(r"<div\b", new)), len(re.findall(r"</div>", new))
        if o != c:
            problems.append(f"{page}: div imbalance {o} vs {c}")
            continue
        planned[path] = new
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
    print(f"{'would touch' if check else 'touched'} {len(planned)} pages, "
          f"{len(notes)} change(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
