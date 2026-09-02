#!/usr/bin/env python3
"""
Finishes 1 Corinthians. Ten pages.

The pattern in this book is different again. The pages are not missing narrative,
they are missing the second half of arguments. Paul states a position, and the
inherited sections describe the statement and stop before the application.

  1corinthians7 kept marriage and singleness and divorce, vv.1-16, and lost vv.17-40:
  abide in the calling you were called in, the passage on virgins, and the whole of
  Paul's reasoning about the present distress. Twenty-four of forty verses.
  1corinthians16 kept 'The Collection (vv.1-4)' and lost vv.5-24, which is the travel
  plan, the instruction about receiving Timothy without contempt, the household of
  Stephanas, and the closing greeting Paul writes in his own hand.
  1corinthians15 had the gospel defined, the necessity of resurrection, the body and
  the victory, and nothing for vv.20-34, which is Christ the firstfruits, the reign
  handed back to the Father, and 'why stand we in jeopardy every hour'.

Two structural repairs come with it. 1corinthians10's warning from Israel's history
ran vv.1-13 with a separate section for v.13, describing that verse twice, so the
warning becomes vv.1-12 and verse 13 keeps its own. 1corinthians5's opening section
covered only v.1, leaving v.2 uncovered between it and the discipline section, so it
takes both.

Usage:
    python3 finish_1corinthians.py [--check]
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
"1corinthians2": [
 ("insert", "God's Hidden Wisdom", "The Natural and the Spiritual Man (vv.11-16)",
  "The argument moves from what God has revealed to who can receive it, and the analogy is "
  "drawn from ordinary privacy: what man knoweth the things of a man, save the spirit of man "
  "which is in him? even so the things of God knoweth no man, but the Spirit of God. Then the "
  "distinction that has been argued over ever since, the natural man receiveth not the things "
  "of the Spirit of God, for they are foolishness unto him, neither can he know them, for they "
  "are spiritually discerned. The chapter closes on a claim that sounds arrogant until you "
  "notice what it rests on, we have the mind of Christ, which is the gift described in verse "
  "12 rather than an achievement."),
],
"1corinthians3": [
 ("insert", "The Building", "All Things Are Yours (vv.18-23)",
  "Paul turns the Corinthians' party slogans inside out. They had been saying I am of Paul and "
  "I of Apollos as though attachment to a teacher were a possession, and the answer is that the "
  "ownership runs the other way: all things are yours, whether Paul, or Apollos, or Cephas, or "
  "the world, or life, or death. The teachers belong to the church, not the church to the "
  "teachers. Before that comes the warning that makes it possible, let no man deceive himself, "
  "if any man among you seemeth to be wise in this world, let him become a fool, that he may "
  "be wise. Two quotations are used to close it, he taketh the wise in their own craftiness, "
  "and the LORD knoweth the thoughts of the wise, that they are vain."),
],
"1corinthians4": [
 ("insert", "The Corinthians' Pride", "As My Beloved Sons I Warn You (vv.14-21)",
  "The irony stops here and the tone changes in one sentence: I write not these things to shame "
  "you, but as my beloved sons I warn you. Then the claim to a standing nobody else in Corinth "
  "has, for though ye have ten thousand instructors in Christ, yet have ye not many fathers, "
  "for in Christ Jesus I have begotten you through the gospel. Timothy is being sent, and Paul "
  "is coming himself. The chapter ends with a question that leaves the choice with them, shall "
  "I come unto you with a rod, or in love, and in the spirit of meekness? and a line about "
  "the party leaders, the kingdom of God is not in word, but in power."),
],
"1corinthians5": [
 ("extend", "The Sin", "(vv.1-2)",
  "What Paul objects to first is not the offence but the mood surrounding it: and ye are "
  "puffed up, and have not rather mourned. A church that should be grieving is pleased with "
  "itself, and that is the condition the rest of the chapter addresses."),
 ("insert", "The Leaven Principle", "Not to Keep Company (vv.9-13)",
  "Paul corrects a misreading of something he had written earlier. I wrote unto you not to "
  "company with fornicators, and then the clarification, yet not altogether with the "
  "fornicators of this world, for then must ye needs go out of the world. The instruction was "
  "never about withdrawing from society, it was about a man that is called a brother. Then the "
  "line that fixes the jurisdiction, what have I to do to judge them also that are without? do "
  "not ye judge them that are within? The church is told to deal with its own members and to "
  "leave the outside world to God, which is the reverse of how the passage is usually quoted."),
],
"1corinthians7": [
 ("insert", "Divorce", "Abide in the Calling (vv.17-24)",
  "The section is a digression that turns out to be the principle: as God hath distributed to "
  "every man, so let him walk. It is argued twice over, once from circumcision and once from "
  "slavery, and the conclusion is the same both times, let every man abide in the same calling "
  "wherein he was called. The point is not that circumstances do not matter, it is that they "
  "are not what makes a Christian. The clause about the slave is deliberately balanced, art "
  "thou called being a servant? care not for it, but if thou mayest be made free, use it "
  "rather, and the reason given is ownership, ye are bought with a price."),
 ("insert", "Abide in the Calling", "Concerning Virgins (vv.25-35)",
  "Paul is careful to label what follows as advice rather than command, I have no commandment "
  "of the Lord, yet I give my judgment. The advice is to stay as you are, and the reason "
  "offered is circumstance rather than principle, for the present distress. He grants "
  "immediately that marriage is not sin, if thou marry, thou hast not sinned, and states his "
  "concern plainly, I would spare you, because he that is married careth for the things that "
  "are of the world, how he may please his wife. The stated aim of the whole passage is "
  "attention rather than asceticism, that ye may attend upon the Lord without distraction."),
 ("insert", "Concerning Virgins", "Let Him Do What He Will (vv.36-40)",
  "The chapter ends by handing the decision back. He that giveth her in marriage doeth well, "
  "but he that giveth her not in marriage doeth better, and the difference between well and "
  "better is left as a difference of degree rather than of right and wrong. Widows are free to "
  "remarry, only in the Lord, with the same qualified preference attached. Then a closing "
  "phrase that has been read both ways for two thousand years, and I think also that I have "
  "the Spirit of God, which is either modesty or irony depending on who is arguing."),
],
"1corinthians9": [
 ("insert", "Paul's Voluntary Surrender", "All Things to All Men (vv.19-23)",
  "Though I be free from all men, yet have I made myself servant unto all. What follows is a "
  "list of accommodations, to the Jews I became as a Jew, to them that are under the law as "
  "under the law, to the weak I became as weak, and it has been quoted as an excuse for having "
  "no convictions ever since. The passage guards itself twice. The stated aim each time is "
  "that I might gain them, and the whole list sits inside a chapter about surrendering rights "
  "rather than principles. The summary is I am made all things to all men, that I might by all "
  "means save some, where the some is as honest as the all."),
],
"1corinthians10": [
 ("retitle", "Israel's Warning", "(vv.1-12)"),
 ("insert", "The Faithfulness of God", "Flee from Idolatry (vv.14-22)",
  "The argument returns to idol meat with a command rather than a concession, flee from "
  "idolatry. Then the reasoning, and it runs through the Lord's supper: the cup of blessing "
  "is the communion of the blood of Christ, and the bread the communion of his body, and "
  "because there is one bread, we being many are one body. If eating together makes a body, "
  "then eating at an idol's table does the same thing there. Paul is careful about what he is "
  "not saying, the idol is nothing, but he identifies what is actually present, the things "
  "which the Gentiles sacrifice, they sacrifice to devils. The closing question is about "
  "loyalty rather than about digestion, ye cannot be partakers of the Lord's table, and of the "
  "table of devils."),
 ("insert", "Flee from Idolatry", "All to the Glory of God (vv.23-33)",
  "The practical guidance is set out with two liberties and one limit. All things are lawful "
  "for me, but all things edify not, and the limit is somebody else, let no man seek his own, "
  "but every man another's wealth. Meat in the market may be eaten without asking questions, "
  "for the earth is the Lord's, and the fulness thereof. Meat at a private dinner may be eaten "
  "until somebody points out where it came from, and then it may not, and the reason given is "
  "not the eater's conscience but the other man's. Then the sentence that sets the standard "
  "for the whole discussion, whether therefore ye eat, or drink, or whatsoever ye do, do all "
  "to the glory of God."),
],
"1corinthians12": [
 ("insert", "", "Jesus Is Lord (vv.1-3)",
  "Before any list of gifts, a test. Paul reminds them what they were, ye were Gentiles, "
  "carried away unto these dumb idols, and the word dumb is doing work: their old gods could "
  "not speak. So the question about any spiritual utterance is what it says. No man speaking "
  "by the Spirit of God calleth Jesus accursed, and no man can say that Jesus is the Lord, but "
  "by the Holy Ghost. The test of a spiritual gift is put in terms of its content rather than "
  "its intensity, which is the framework the next two chapters need."),
 ("insert", "The Body Metaphor", "God Hath Set Some in the Church (vv.28-31)",
  "The list is numbered for the first three, first apostles, secondarily prophets, thirdly "
  "teachers, and then the rest are ordered without numbers. That the numbering stops is the "
  "point in a church arguing about rank. The rhetorical questions that follow all expect the "
  "answer no, are all apostles? are all prophets? do all speak with tongues? which is the "
  "body argument applied to the thing they were most excited about. Then the pivot into "
  "chapter 13, covet earnestly the best gifts, and yet I shew you a more excellent way."),
],
"1corinthians15": [
 ("insert", "The Necessity of Resurrection", "Christ the Firstfruits (vv.20-28)",
  "But now is Christ risen from the dead, and become the firstfruits of them that slept. The "
  "word firstfruits carries the argument: the first sheaf is not a separate event from the "
  "harvest, it is the beginning of it. Then the ordering, Christ the firstfruits, afterward "
  "they that are Christ's at his coming, then the end. The last enemy that shall be destroyed "
  "is death. The passage closes on a submission that has troubled readers since Arius, then "
  "shall the Son also himself be subject unto him that put all things under him, that God may "
  "be all in all."),
 ("insert", "Christ the Firstfruits", "Why Stand We in Jeopardy (vv.29-34)",
  "Paul argues from behaviour rather than doctrine, and one of his examples is famously "
  "obscure: else what shall they do which are baptized for the dead? He does not explain it "
  "and does not endorse it, he uses it. His own case is clearer, why stand we in jeopardy "
  "every hour? I die daily, and if the dead rise not, the sensible conclusion is the one he "
  "quotes, let us eat and drink, for tomorrow we die. Then a warning about company rather than "
  "argument, evil communications corrupt good manners, and awake to righteousness, and sin "
  "not."),
],
"1corinthians16": [
 ("insert", "The Collection", "Travel Plans, Timothy and Apollos (vv.5-12)",
  "The letter turns to logistics and the logistics are revealing. Paul will stay at Ephesus "
  "until Pentecost, and the reason he gives for staying is not comfort, for a great door and "
  "effectual is opened unto me, and there are many adversaries, both in the same breath. Then "
  "an instruction about Timothy that says something about Corinth, let no man therefore despise "
  "him, and a note about Apollos declining to come at present, his will was not at all to come "
  "at this time. The man the Corinthians had formed a party around would not take the "
  "invitation."),
 ("insert", "Travel Plans, Timothy and Apollos",
  "Watch Ye, Stand Fast, and the Greeting in His Own Hand (vv.13-24)",
  "Five imperatives in one verse, watch ye, stand fast in the faith, quit you like men, be "
  "strong, and then a sixth that governs them, let all your things be done with charity. The "
  "household of Stephanas is commended in terms of work rather than status, they have addicted "
  "themselves to the ministry of the saints. Aquila and Priscilla send greetings with the "
  "church that is in their house. Then the letter's own signature, the salutation of me Paul "
  "with mine own hand, which means the rest was dictated, followed by the Aramaic prayer left "
  "untranslated, Maranatha, and the last line, my love be with you all in Christ Jesus."),
],
}


def find(items, prefix):
    for i, (label, _) in enumerate(items):
        if H.unescape(label).strip().startswith(prefix):
            return i
    return -1


def first_section(items):
    for i, (label, _) in enumerate(items):
        if re.search(r"\(vv?\.[^)]*\)\s*:?\s*$", H.unescape(label).strip()):
            return i
    return len(items)


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
        for op in ops:
            kind = op[0]
            if kind in ("extend", "retitle"):
                prefix, rng = op[1], op[2]
                i = find(items, prefix)
                if i < 0:
                    problems.append(f"{page}: {kind} target {prefix!r} not found")
                    continue
                new_label, n = RANGE_IN_LABEL.subn(rng, items[i][0])
                if not n:
                    problems.append(f"{page}: no range in label {prefix!r}")
                    continue
                items[i][0] = new_label
                if kind == "extend":
                    items[i][1] += " " + op[3]
                notes.append(f"{page}: {kind} {prefix!r} to {rng}")
            else:
                _, after, label, prose = op
                at = first_section(items) if after == "" else find(items, after) + 1
                if after and at == 0:
                    problems.append(f"{page}: insert anchor {after!r} not found")
                    continue
                items.insert(at, [label + ":", prose])
                notes.append(f"{page}: inserted {label!r}")
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
