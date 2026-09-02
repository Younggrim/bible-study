#!/usr/bin/env python3
"""
Finishes Romans. Twelve pages.

The omissions here are the largest in proportion to the book's importance. romans8
had one section, 'The Golden Chain (vv.29-30)', for thirty-nine verses. No
condemnation, the mind of the flesh, the Spirit of adoption, the creation groaning,
the Spirit making intercession with groanings which cannot be uttered, and 'who
shall separate us from the love of Christ' were all undescribed on the page the
project's own Historical Context calls the greatest chapter in the Bible.

romans3 was missing vv.21-31, which is the passage the whole letter turns on: the
righteousness of God without the law, justified freely by his grace, and the
propitiation. It also carried the last cut label in the corpus, 'Romans 3:' with its
body opening '23-26 is arguably the most theologically dense passage'. The colon that
was split on was the one between chapter and verse. That sentence is restored to
Historical Context where general remarks live, and the passage gets sections of its
own.

romans4 was missing vv.9-25, so Abraham's faith was described and the argument built
on it, that the promise came before circumcision and therefore does not depend on it,
was not. romans6 was missing vv.11-23, which is every imperative in the chapter.

One structural repair: romans9 ran 'God's Sovereign Election (vv.6-29)' with a nested
'The Potter and the Clay (vv.19-23)' inside it, describing five verses twice. The
election section becomes vv.6-18 and two new sections carry vv.24-29 and vv.30-33.

romans14 needed a decision. Five of the six translations on the page end the chapter
at verse 23. WEB alone runs to 26, because it places the doxology of 16:25-27 at the
end of chapter 14, following a different manuscript tradition. It is the only page in
the corpus where translations disagree about chapter length. Rather than leave three
verses undescribed for anyone reading in WEB, they get a section that says what they
are and why they move.

Usage:
    python3 finish_romans.py [--check]
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
"romans1": [
 ("insert", "", "Called to Be an Apostle (vv.1-7)",
  "One sentence in the Greek, and it does a great deal of work before it reaches a greeting. "
  "Paul introduces himself as a servant and an apostle, then puts the gospel before himself: "
  "promised afore by his prophets in the holy scriptures, so it is not new. Then the two "
  "clauses about Jesus that have been argued over ever since, made of the seed of David "
  "according to the flesh, and declared to be the Son of God with power by the resurrection "
  "from the dead. The purpose named is obedience among all nations, which tells the Romans why "
  "a man they have never met is writing to them, and the address is warm, beloved of God, "
  "called to be saints."),
 ("insert", "Called to Be an Apostle", "I Long to See You (vv.8-15)",
  "Paul explains why he has not come and states plainly that he has tried, oftentimes I "
  "purposed to come unto you, but was let hitherto. The reason for wanting to is put twice and "
  "the second version corrects the first: he wants to impart some spiritual gift, and then "
  "immediately makes it mutual, that I may be comforted together with you by the mutual faith "
  "both of you and me. Then the debt, I am debtor both to the Greeks and to the Barbarians, "
  "and the readiness, I am ready to preach the gospel to you that are at Rome also, which sets "
  "up the thesis in the next verse."),
],
"romans3": [
 ("merge_into", "Romans 3:", "Historical Context"),
 ("insert", "", "What Advantage Then Hath the Jew (vv.1-8)",
  "Chapter 2 has just levelled the Jew with the Gentile, so the objections come thick and Paul "
  "raises them himself. What advantage then hath the Jew? and the answer is not none, it is "
  "much every way, chiefly because unto them were committed the oracles of God. Then a harder "
  "one: if their unbelief shows God's faithfulness by contrast, is God unjust to judge them? "
  "God forbid, let God be true, but every man a liar. The last objection is the one Paul is "
  "evidently tired of, that his gospel amounts to let us do evil, that good may come, and he "
  "does not argue with it, he says the people who report him as teaching it are slanderers "
  "whose damnation is just."),
 ("insert", "The Universal Indictment",
  "The Righteousness of God Without the Law (vv.21-26)",
  "But now. Two words that turn the letter, after three chapters of indictment. The "
  "righteousness of God without the law is manifested, being witnessed by the law and the "
  "prophets, so it is new in disclosure and not in intention. Then the sentence that is the "
  "hinge of the whole argument, for all have sinned, and come short of the glory of God, being "
  "justified freely by his grace through the redemption that is in Christ Jesus. The vocabulary "
  "is drawn from three worlds at once: the courtroom in justified, the slave market in "
  "redemption, and the temple in propitiation. And the stated purpose is God's own consistency, "
  "that he might be just, and the justifier of him which believeth."),
 ("insert", "The Righteousness of God Without the Law",
  "Where Is Boasting Then (vv.27-31)",
  "Where is boasting then? It is excluded. Not moderated or redirected, excluded, and the "
  "reason given is the mechanism rather than the manners: by what law? of works? nay, but by "
  "the law of faith. Then the argument is pressed on monotheism, which is the last thing a "
  "Jewish reader would dispute, is he the God of the Jews only? is he not also of the "
  "Gentiles? seeing it is one God which shall justify the circumcision by faith, and the "
  "uncircumcision through faith. The chapter closes by answering the obvious charge before "
  "chapter 4 makes the case, do we then make void the law through faith? God forbid, yea, we "
  "establish the law."),
],
"romans4": [
 ("insert", "David's Testimony", "Before or After Circumcision (vv.9-12)",
  "Paul makes the argument turn on a date. Abraham was counted righteous in Genesis 15 and "
  "circumcised in Genesis 17, so how was it then reckoned? when he was in circumcision, or in "
  "uncircumcision? Not in circumcision, but in uncircumcision. The sign came afterward, and "
  "Paul defines what it therefore was, a seal of the righteousness of the faith which he had "
  "yet being uncircumcised. The consequence is the point of the chapter: Abraham is the father "
  "of believing Gentiles first and of the circumcised only insofar as they also walk in the "
  "steps of that faith."),
 ("insert", "Before or After Circumcision", "The Promise Is of Faith (vv.13-17)",
  "The promise that he should be heir of the world was not to Abraham through the law. The "
  "reasoning is that the two cannot occupy the same ground, for if they which are of the law be "
  "heirs, faith is made void, and the promise made of none effect. Then the function of law "
  "stated flatly, the law worketh wrath, for where no law is, there is no transgression. The "
  "purpose of grounding it in faith is inclusion, to the end the promise might be sure to all "
  "the seed, and the chapter reaches for Genesis 17 to name the God involved, who quickeneth "
  "the dead, and calleth those things which be not as though they were."),
 ("insert", "The Promise Is of Faith", "Against Hope, Believed in Hope (vv.18-25)",
  "The portrait of Abraham's faith is not of a man untroubled. He considered not his own body "
  "now dead, when he was about an hundred years old, and the passage says he was not weak in "
  "faith while conceding exactly what there was to be weak about. Being fully persuaded that, "
  "what he had promised, he was able also to perform. Then the application is made explicit "
  "and the object of faith is named, it was imputed to him for righteousness, and it shall be "
  "to us, if we believe on him that raised up Jesus our Lord from the dead. The closing verse "
  "splits the work in two, who was delivered for our offences, and was raised again for our "
  "justification."),
],
"romans6": [
 ("insert", "Union with Christ", "Reckon Yourselves Dead Indeed (vv.11-14)",
  "The first imperative in the chapter arrives at verse 11, and it is a command to do "
  "arithmetic rather than to try harder: likewise reckon ye also yourselves to be dead indeed "
  "unto sin, but alive unto God. What follows are three more, and they concern the body, let "
  "not sin therefore reign in your mortal body, neither yield ye your members as instruments "
  "of unrighteousness, but yield yourselves unto God. Then the ground offered, and it is a "
  "statement of fact rather than encouragement, for ye are not under the law, but under grace."),
 ("insert", "Reckon Yourselves Dead Indeed", "Servants of Whom Ye Obey (vv.15-19)",
  "The objection of verse 1 returns in a new form, shall we sin, because we are not under the "
  "law? and the answer is an argument about ownership. His servants ye are to whom ye obey, so "
  "there is no third option in which a man belongs to nobody. God be thanked, that ye were the "
  "servants of sin, but ye have obeyed from the heart that form of doctrine which was delivered "
  "you. Paul then apologises for the metaphor, I speak after the manner of men because of the "
  "infirmity of your flesh, which is a rare admission that the image is imperfect."),
 ("insert", "Servants of Whom Ye Obey", "The Wages of Sin (vv.20-23)",
  "The two services are compared by their outcomes rather than their conditions. What fruit had "
  "ye then in those things whereof ye are now ashamed? for the end of those things is death. "
  "Now being made free from sin, ye have your fruit unto holiness, and the end everlasting "
  "life. Then the closing verse, and the asymmetry inside it is deliberate: the wages of sin is "
  "death, but the gift of God is eternal life. Wages are earned and a gift is not, and the two "
  "halves of the sentence are not parallel on purpose."),
],
"romans8": [
 ("insert", "", "No Condemnation (vv.1-4)",
  "There is therefore now no condemnation to them which are in Christ Jesus. The therefore "
  "reaches back over the whole of chapter 7, and what the verse denies is not the guilt but the "
  "sentence. Then the mechanism, because the law could not do it, for what the law could not "
  "do, in that it was weak through the flesh, God sending his own Son in the likeness of sinful "
  "flesh, and for sin, condemned sin in the flesh. The condemnation has not been cancelled, it "
  "has been relocated. And the purpose clause is about conduct, that the righteousness of the "
  "law might be fulfilled in us."),
 ("insert", "No Condemnation", "The Flesh and the Spirit (vv.5-11)",
  "Two ways of being are set side by side and described by what they attend to, they that are "
  "after the flesh do mind the things of the flesh. Then the summary that has been quoted out "
  "of context for centuries, to be carnally minded is death, but to be spiritually minded is "
  "life and peace. The distinction is not between two classes of Christian, because the test "
  "given is possession of the Spirit itself, if any man have not the Spirit of Christ, he is "
  "none of his. And the section ends where the chapter will end, with resurrection: he that "
  "raised up Christ from the dead shall also quicken your mortal bodies by his Spirit that "
  "dwelleth in you."),
 ("insert", "The Flesh and the Spirit", "The Spirit of Adoption (vv.12-17)",
  "Ye have not received the spirit of bondage again to fear, but ye have received the Spirit of "
  "adoption, whereby we cry, Abba, Father. The Aramaic word is left standing in a Greek letter "
  "to a Latin city, which is why it carries the weight it does. Then two witnesses to the same "
  "fact, the Spirit itself beareth witness with our spirit, that we are the children of God. "
  "The inheritance follows from the status, and if children, then heirs, and the last clause "
  "attaches a condition nobody quotes as often, if so be that we suffer with him, that we may "
  "be also glorified together."),
 ("insert", "The Spirit of Adoption", "The Whole Creation Groaneth (vv.18-25)",
  "The sufferings of this present time are not worthy to be compared with the glory which shall "
  "be revealed in us. Then the argument widens past human beings entirely: the creature was "
  "made subject to vanity, not willingly, and waits for the manifestation of the sons of God. "
  "The whole creation groaneth and travaileth in pain together until now, and the metaphor is "
  "childbirth rather than decay, which makes the groaning productive. We groan too, waiting for "
  "the adoption, to wit, the redemption of our body, and the section closes on a definition, "
  "for we are saved by hope, but hope that is seen is not hope."),
 ("insert", "The Whole Creation Groaneth", "The Spirit Maketh Intercession (vv.26-28)",
  "Likewise the Spirit also helpeth our infirmities, for we know not what we should pray for as "
  "we ought. The admission is unusual in a letter this confident, and the remedy is not "
  "instruction in prayer but substitution for it: the Spirit itself maketh intercession for us "
  "with groanings which cannot be uttered. The same verb as the creation's groaning, three "
  "verses later. Then the sentence most often quoted from the chapter, and it is a claim about "
  "arrangement rather than about outcomes being pleasant, all things work together for good to "
  "them that love God, to them who are the called according to his purpose."),
 ("insert", "The Golden Chain", "Who Shall Separate Us (vv.31-39)",
  "The chapter ends in a courtroom that finds nothing to try. Five questions, and each is put "
  "so that the answer is a person rather than an argument: who can be against us, if God be "
  "for us? how shall he not with him also freely give us all things, seeing he spared not his "
  "own Son? who shall lay anything to the charge of God's elect? it is God that justifieth. who "
  "is he that condemneth? it is Christ that died. Then the list, and its point is exhaustion "
  "rather than eloquence: tribulation, distress, persecution, famine, nakedness, peril, sword, "
  "death, life, angels, principalities, powers, things present, things to come, height, depth. "
  "Nor any other creature, which closes the category. Nay, in all these things we are more than "
  "conquerors through him that loved us."),
],
"romans9": [
 ("retitle", "God's Sovereign Election", "(vv.6-18)"),
 ("insert", "The Potter and the Clay", "Vessels of Mercy, Called from the Gentiles (vv.24-29)",
  "The vessels of mercy are identified, and the identification is the surprise: not of the Jews "
  "only, but also of the Gentiles. Two prophets are then made to say it. Hosea is quoted on the "
  "reversal of the judgment names, I will call them my people, which were not my people, and in "
  "the place where it was said unto them, Ye are not my people, there shall they be called the "
  "children of the living God. Then Isaiah on the remnant, though the number of the children of "
  "Israel be as the sand of the sea, a remnant shall be saved, with the harder line following "
  "it, except the Lord of Sabaoth had left us a seed, we had been as Sodoma."),
 ("insert", "Vessels of Mercy, Called from the Gentiles",
  "Israel Stumbled at That Stumblingstone (vv.30-33)",
  "The chapter closes by stating the outcome as a paradox and then explaining it in one clause. "
  "The Gentiles, which followed not after righteousness, have attained to righteousness, and "
  "Israel, which followed after the law of righteousness, hath not attained. Wherefore? Because "
  "they sought it not by faith, but as it were by the works of the law. The image chosen is a "
  "stone in the road rather than a wall, for they stumbled at that stumblingstone, and Isaiah "
  "is quoted to make the stone a person, whosoever believeth on him shall not be ashamed."),
],
"romans10": [
 ("insert", "Israel's Problem", "The Word Is Nigh Thee (vv.5-7)",
  "Two ways of righteousness are quoted rather than argued, and both come from Moses. Leviticus "
  "gives the first, the man which doeth those things shall live by them. Then Deuteronomy 30 is "
  "taken up for the second and applied in a way that has occupied commentators ever since: say "
  "not in thine heart, who shall ascend into heaven? which Paul glosses as bringing Christ down, "
  "or who shall descend into the deep? which he glosses as bringing him up from the dead. The "
  "point is that neither errand is needed, because the word is already near."),
 ("insert", "The Necessity of Preaching", "Have They Not Heard (vv.18-21)",
  "The chain of questions in the previous verses ends in a defence of God rather than an excuse "
  "for Israel. Have they not heard? and Psalm 19 answers, their sound went into all the earth. "
  "Then Deuteronomy 32 on provocation by a foolish nation, and Isaiah twice. The last "
  "quotation is the most affecting thing in the chapter and it is an image of posture: all day "
  "long I have stretched forth my hands unto a disobedient and gainsaying people. The argument "
  "about election closes with God standing with his arms out."),
],
"romans11": [
 ("insert", "The Remnant", "Salvation Come to the Gentiles (vv.11-15)",
  "Have they stumbled that they should fall? God forbid. What follows is Paul's account of his "
  "own mission as a deliberately indirect strategy: through their fall salvation is come unto "
  "the Gentiles, for to provoke them to jealousy. He then says something about his motives that "
  "few missionaries would put in writing, I magnify mine office, if by any means I may provoke "
  "to emulation them which are my flesh, and might save some of them. The escalating argument "
  "ends in a question left as a question, if the casting away of them be the reconciling of the "
  "world, what shall the receiving of them be, but life from the dead?"),
 ("insert", "The Olive Tree", "All Israel Shall Be Saved (vv.25-32)",
  "Paul labels what he is about to say a mystery and gives the reason for telling them, lest ye "
  "should be wise in your own conceits. The shape is temporal: blindness in part is happened to "
  "Israel, until the fulness of the Gentiles be come in, and so all Israel shall be saved. What "
  "the passage rests on is not Israel's merit and says so twice, as concerning the gospel, they "
  "are enemies for your sakes, but as touching the election, they are beloved for the fathers' "
  "sakes, and then the clause that has kept the question open, for the gifts and calling of God "
  "are without repentance. The section closes on symmetry, God hath concluded them all in "
  "unbelief, that he might have mercy upon all."),
],
"romans13": [
 ("insert", "The Debt of Love", "The Night Is Far Spent (vv.11-14)",
  "The ethics of the chapter are given a deadline. Knowing the time, that now it is high time "
  "to awake out of sleep, for now is our salvation nearer than when we believed. The night is "
  "far spent, the day is at hand. Then the clothing image that runs through the passage, cast "
  "off the works of darkness, put on the armour of light, and finally put ye on the Lord Jesus "
  "Christ, and make not provision for the flesh. These are the verses Augustine read in the "
  "garden at Milan, which he says ended the argument he had been having with himself for years."),
],
"romans14": [
 ("insert", "The \"Weak\" and \"Strong\"", "He That Regardeth the Day (vv.5-6)",
  "The second example after food is the calendar, one man esteemeth one day above another, "
  "another esteemeth every day alike. Paul declines to rule on it, let every man be fully "
  "persuaded in his own mind, and then gives the test that governs both disputes: he that "
  "regardeth the day, regardeth it unto the Lord, and he that eateth, eateth to the Lord, for "
  "he giveth God thanks. The same act done with thanksgiving is acceptable whichever way it "
  "goes, which moves the question from the practice to the intention behind it."),
 ("insert", "The Principle of Love",
  "The Doxology as Some Manuscripts Place It (vv.24-26)",
  "Readers using WEB on this page will find three more verses here, and they are the doxology "
  "that most translations print at 16:25-27: now to him who is able to establish you according "
  "to my gospel, to the only wise God be glory for ever. A group of manuscripts places it at "
  "the end of chapter 14 rather than the end of chapter 16, and a few carry it in both places. "
  "The five other translations on this page end the chapter at verse 23. Nothing in the text "
  "changes, only where it sits, and the description of it belongs with the doxology on the "
  "romans16 page."),
],
"romans15": [
 ("insert", "Christ's Example", "A Minister of the Circumcision (vv.8-12)",
  "The argument for bearing with one another is grounded in whom Christ served, and the order "
  "is careful: Jesus Christ was a minister of the circumcision for the truth of God, to confirm "
  "the promises made unto the fathers, and that the Gentiles might glorify God for his mercy. "
  "Promise to the one, mercy to the other. Then four quotations stacked to make the same point "
  "from every part of the Hebrew Bible, from the law, the writings and the prophets, each one "
  "putting Gentiles and Israel in the same sentence: I will confess to thee among the Gentiles, "
  "rejoice, ye Gentiles, with his people, praise the Lord, all ye Gentiles, and in him shall "
  "the Gentiles trust."),
 ("insert", "The Benediction", "A Minister to the Gentiles (vv.14-17)",
  "Paul softens before he explains himself, I myself also am persuaded of you, that ye also are "
  "full of goodness, filled with all knowledge, and able to admonish one another. Then the "
  "reason he has written anyway, as putting you in mind, because of the grace that is given to "
  "me of God. The description of his own work is priestly and deliberate, ministering the "
  "gospel of God, that the offering up of the Gentiles might be acceptable, sanctified by the "
  "Holy Ghost. He is describing converts as a sacrifice he presents rather than a result he "
  "achieved."),
 ("insert", "Paul's Ministry Philosophy", "Purposing to Come by You (vv.23-29)",
  "The travel plan is the most concrete statement of Paul's ambition in the New Testament: now "
  "having no more place in these parts, whensoever I take my journey into Spain, I will come to "
  "you. Rome is a stop on the way to somewhere further west. But first Jerusalem, with the "
  "collection, and the reason he gives for it is an argument about debt rather than charity, "
  "for if the Gentiles have been made partakers of their spiritual things, their duty is to "
  "minister unto them in carnal things. He expects the visit to Rome to be good, I shall come "
  "in the fulness of the blessing of the gospel of Christ, which is worth reading beside how he "
  "actually arrived, under guard, in Acts 28."),
 ("insert", "Purposing to Come by You", "Strive Together in Prayer (vv.30-33)",
  "The request is urgent and the word is a wrestling term, that ye strive together with me in "
  "your prayers to God for me. Two things are asked and both concern Jerusalem rather than "
  "Spain: that I may be delivered from them that do not believe in Judaea, and that my service "
  "may be accepted of the saints. He is as worried about the collection being refused as about "
  "being attacked. The hoped-for outcome is stated modestly, that I may come unto you with joy, "
  "and may with you be refreshed, and the section closes with a blessing, now the God of peace "
  "be with you all."),
],
"romans16": [
 ("insert", "The Warning", "Timotheus, Tertius and Gaius (vv.21-24)",
  "The final greetings come from Paul's companions rather than from Paul, and one of them "
  "interrupts to speak for himself: I Tertius, who wrote this epistle, salute you in the Lord. "
  "The secretary signs his own name inside the letter, which is the plainest evidence in the "
  "New Testament of how these documents were physically made. Gaius is named as Paul's host and "
  "the host of the whole church, and Erastus as the chamberlain of the city, a municipal "
  "official. Verse 24 is a grace benediction present in the KJV and ASV and omitted by BSB, "
  "which numbers straight from 23 to 25, because the earliest manuscripts do not carry it."),
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
            if kind == "retitle":
                prefix, rng = op[1], op[2]
                i = find(items, prefix)
                if i < 0:
                    problems.append(f"{page}: retitle target {prefix!r} not found")
                    continue
                new_label, n = RANGE_IN_LABEL.subn(rng, items[i][0])
                if not n:
                    problems.append(f"{page}: no range in label {prefix!r}")
                    continue
                items[i][0] = new_label
                notes.append(f"{page}: retitled {prefix!r} to {rng}")
            elif kind == "merge_into":
                _, frag, target = op
                i, j = find(items, frag), find(items, target)
                if i < 0 or j < 0:
                    problems.append(f"{page}: merge {frag!r} into {target!r} not found")
                    continue
                label = items[i][0].rstrip()
                items[j][1] = (items[j][1].rstrip() + " " + label + items[i][1]).strip()
                del items[i]
                notes.append(f"{page}: merged {frag!r} into {target!r}")
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
