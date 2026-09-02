#!/usr/bin/env python3
"""
Finishes 2 Corinthians. Twelve pages, and a pattern that has not appeared before.

These pages were not summaries with gaps. They were collections of memory verses.
2corinthians9 had three sections and all three were single verses: the sowing
principle at v.6, the cheerful giver at v.7, God's sufficiency at v.8. Twelve of
fifteen verses had nothing. 2corinthians7 had v.10 and v.11 and nothing else, so
fourteen of sixteen were missing, including the reason Paul is writing about sorrow
at all, which is Titus arriving in Macedonia with news. 2corinthians13 had v.5 and
v.14, the self-examination and the benediction, and nothing between or before them.

What consistently went missing is the argument that produced the famous line. Paul's
thorn is described and the signs of an apostle that follow it are not. The great
exchange at 5:21 is described and the ministry of reconciliation that leads to it is
not. The suffering catalogue at 11:23-28 is described and the sarcasm it sits inside,
where Paul says he speaks as a fool and boasts about being let down a wall in a
basket, is not.

One structural repair: 2corinthians6 had 'The Marks of Authentic Ministry (vv.3-10)'
with a nested 'The Paradoxes (vv.8-10)' inside it, so three verses were described
twice. The marks become vv.3-7 and the paradoxes keep their own.

Usage:
    python3 finish_2corinthians.py [--check]
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
"2corinthians1": [
 ("insert", "", "Greeting to the Church and All Achaia (vv.1-2)",
  "Paul, an apostle of Jesus Christ by the will of God, and Timothy our brother. The address "
  "is wider than the city, unto the church of God which is at Corinth, with all the saints "
  "which are in all Achaia, which means the letter was written expecting to be passed around "
  "the province."),
 ("insert", "The God of All Comfort", "The Trouble in Asia (vv.8-11)",
  "We would not have you ignorant of our trouble which came to us in Asia. Paul never says "
  "what it was, and the description is of its effect rather than its nature: we were pressed "
  "out of measure, above strength, insomuch that we despaired even of life. Then the sentence "
  "that explains why he is telling them, we had the sentence of death in ourselves, that we "
  "should not trust in ourselves, but in God which raiseth the dead. The deliverance is put in "
  "three tenses, who delivered us, doth deliver, and will yet deliver, and the last of them is "
  "credited partly to them, ye also helping together by prayer for us."),
 ("insert", "The Trouble in Asia", "Our Rejoicing Is This (vv.12-14)",
  "The one boast Paul allows himself here is a clear conscience, our rejoicing is this, the "
  "testimony of our conscience, that in simplicity and godly sincerity we have had our "
  "conversation in the world. The point being defended is transparency, we write none other "
  "things unto you, than what ye read or acknowledge, because the accusation in Corinth was "
  "that his letters said one thing and his conduct another."),
 ("insert", "Our Rejoicing Is This", "Yea and Amen (vv.15-22)",
  "The charge is inconstancy: he said he would come and did not. His defence is first "
  "practical, I came not as yet unto Corinth to spare you, and then theological, and this is "
  "where the passage lifts. Was I light minded? do I purpose according to the flesh, that with "
  "me there should be yea yea, and nay nay? The answer moves from his reliability to God's, as "
  "God is true, our word toward you was not yea and nay, for the Son of God was not yea and "
  "nay, but in him was yea. All the promises of God in him are yea, and in him Amen. The "
  "seal is named, who hath also sealed us, and given us the earnest of the Spirit, where "
  "earnest is a deposit against the rest."),
 ("insert", "Yea and Amen", "Not Lords Over Your Faith (vv.23-24)",
  "The chapter closes with a correction about his own office that the rest of the letter keeps "
  "returning to. Not for that we have dominion over your faith, but are helpers of your joy. "
  "The reason given for not coming is the same one, to spare you, and it is offered under oath, "
  "I call God for a record upon my soul."),
],
"2corinthians2": [
 ("insert", "", "I Wrote With Many Tears (vv.1-4)",
  "I determined this with myself, that I would not come again to you in heaviness. The visit "
  "was cancelled to avoid a scene, and the letter sent instead is described in terms nobody "
  "would use of a rebuke they enjoyed writing: out of much affliction and anguish of heart I "
  "wrote unto you with many tears. The stated purpose is not to wound but to disclose, not that "
  "ye should be grieved, but that ye might know the love which I have to you."),
 ("insert", "Restoration After Discipline", "No Rest in My Spirit at Troas (vv.12-13)",
  "Two verses that break off mid-thought and are not resumed until chapter 7. When I came to "
  "Troas to preach Christ's gospel, and a door was opened unto me of the Lord, and then the "
  "admission, I had no rest in my spirit, because I found not Titus my brother. An open door "
  "left unused because he was waiting for news about a church. He goes on into Macedonia to "
  "find him, and the sentence stops there."),
],
"2corinthians4": [
 ("insert", "", "We Faint Not (vv.1-3)",
  "Therefore seeing we have this ministry, we faint not. The ministry is the one described at "
  "the end of chapter 3, and the first thing said about holding it is a renunciation: we have "
  "renounced the hidden things of dishonesty, not walking in craftiness, nor handling the word "
  "of God deceitfully. What replaces manipulation is exposure, by manifestation of the truth "
  "commending ourselves to every man's conscience in the sight of God."),
 ("insert", "The God of This World", "Light Out of Darkness (vv.5-6)",
  "We preach not ourselves, but Christ Jesus the Lord, and ourselves your servants for Jesus' "
  "sake. Then the creation image that answers the blindness of verse 4, for God, who commanded "
  "the light to shine out of darkness, hath shined in our hearts, to give the light of the "
  "knowledge of the glory of God in the face of Jesus Christ. The same voice that spoke at "
  "Genesis 1 is described as the one that lights a mind."),
 ("insert", "Treasure in Earthen Vessels", "Always Delivered Unto Death (vv.8-15)",
  "Four pairs, each conceding the pressure and denying the collapse: troubled on every side, "
  "yet not distressed, perplexed, but not in despair, persecuted, but not forsaken, cast down, "
  "but not destroyed. Then the theology under them, always bearing about in the body the dying "
  "of the Lord Jesus, that the life also of Jesus might be made manifest in our body. The "
  "arrangement is stated without softening, death worketh in us, and life in you. And the "
  "reason he keeps speaking is a quotation from Psalm 116, I believed, and therefore have I "
  "spoken."),
],
"2corinthians5": [
 ("insert", "The Resurrection Body", "The Love of Christ Constraineth Us (vv.11-16)",
  "Knowing therefore the terror of the Lord, we persuade men. Paul is answering the charge that "
  "he commends himself, and his reply is that the motives are only two and both are outside "
  "him: whether we be beside ourselves, it is to God, or whether we be sober, it is for your "
  "cause. Then the sentence that gives the section its name, for the love of Christ "
  "constraineth us, with the logic set out plainly, if one died for all, then were all dead, "
  "and he died for all, that they which live should not henceforth live unto themselves. The "
  "consequence is a change in how people are assessed, henceforth know we no man after the "
  "flesh."),
 ("insert", "The New Creation", "The Ministry of Reconciliation (vv.18-20)",
  "All things are of God, who hath reconciled us to himself by Jesus Christ, and hath given to "
  "us the ministry of reconciliation. The same thing is said twice in three verses, once as a "
  "ministry and once as a word committed, and the content is stated in a clause easy to read "
  "past, not imputing their trespasses unto them. Then the office described in terms of "
  "diplomacy, we are ambassadors for Christ, as though God did beseech you by us, and the "
  "appeal itself, be ye reconciled to God. An ambassador does not invent the message and "
  "cannot alter it."),
],
"2corinthians6": [
 ("insert", "", "Now Is the Accepted Time (vv.1-2)",
  "We then, as workers together with him, beseech you also that ye receive not the grace of "
  "God in vain. Then Isaiah 49 quoted and applied to the present moment, I have heard thee in "
  "a time accepted, and in the day of salvation have I succoured thee, with Paul's own "
  "insistence on the timing, behold, now is the accepted time, behold, now is the day of "
  "salvation."),
 ("retitle", "The Marks of Authentic Ministry", "(vv.3-7)"),
 ("insert", "The Paradoxes", "Our Heart Is Enlarged (vv.11-13)",
  "O ye Corinthians, our mouth is open unto you, our heart is enlarged. It is the most direct "
  "address in the letter and it names its own difficulty, ye are not straitened in us, but ye "
  "are straitened in your own bowels. The restriction is on their side, not his. The request "
  "that follows is put as a family matter rather than an apostolic instruction, now for a "
  "recompence in the same, I speak as unto my children, be ye also enlarged."),
],
"2corinthians7": [
 ("insert", "", "Ye Are in Our Hearts (vv.1-4)",
  "Having therefore these promises, let us cleanse ourselves from all filthiness of the flesh "
  "and spirit. Then a defence in three denials, we have wronged no man, we have corrupted no "
  "man, we have defrauded no man, and immediately a disclaimer so it cannot be read as attack, "
  "I speak not this to condemn you. What follows is as warm as anything Paul writes, ye are in "
  "our hearts, to die and live with you, and great is my glorying of you, I am filled with "
  "comfort."),
 ("insert", "Ye Are in Our Hearts", "Comforted by the Coming of Titus (vv.5-9)",
  "The sentence broken off at 2:13 is picked up here, and the honesty of it is the point: when "
  "we were come into Macedonia, our flesh had no rest, but we were troubled on every side, "
  "without were fightings, within were fears. The comfort came by an arrival rather than an "
  "insight, God comforted us by the coming of Titus, and by the news he brought of their "
  "longing and their mourning. Paul then says something few writers admit, I do not repent, "
  "though I did repent, about the severe letter, because the sorrow it caused turned out to be "
  "the right kind."),
 ("insert", "The Fruit of Godly Sorrow", "Titus Refreshed by You All (vv.12-16)",
  "The purpose of the earlier letter is restated, not for his cause that had done the wrong, "
  "nor for his cause that suffered wrong, but that our care for you might appear. Then the "
  "detail that matters to Paul most in the chapter: Titus went with a good report of them and "
  "came back with it confirmed, his spirit was refreshed by you all, and I was not ashamed. "
  "The letter that risked the relationship ended with the man carrying it vindicated."),
],
"2corinthians8": [
 ("insert", "The Macedonian Example", "Proving the Sincerity of Your Love (vv.6-8)",
  "Titus is sent to finish what was started, that he would also finish in you the same grace. "
  "The appeal is framed as consistency rather than duty, as ye abound in every thing, in faith, "
  "and utterance, and knowledge, see that ye abound in this grace also. Then a careful "
  "disclaimer that shapes the whole chapter, I speak not by commandment, but by occasion of the "
  "forwardness of others, and to prove the sincerity of your love. Giving is treated as "
  "evidence, and it is not being ordered."),
 ("insert", "Principles of Giving", "Titus and the Two Brethren (vv.16-24)",
  "The end of the chapter is administrative and unusually careful. Titus goes, and with him a "
  "brother whose praise is in the gospel throughout all the churches, chosen by the churches "
  "themselves to travel with the money, and a third man besides. The reason is given without "
  "embarrassment: avoiding this, that no man should blame us in this abundance, providing for "
  "honest things, not only in the sight of the Lord, but also in the sight of men. A collection "
  "is handled by a committee nobody appointed from Paul's own circle, and he says plainly why."),
],
"2corinthians9": [
 ("insert", "", "Sent Ahead, That It Be Not of Necessity (vv.1-5)",
  "Paul says he needs no words for it, as touching the ministering to the saints, it is "
  "superfluous for me to write to you, and then writes a chapter. The reason for sending the "
  "brethren ahead is stated as protection of everyone's dignity: lest our boasting of you "
  "should be in vain, and lest, if any of Macedonia come with me and find you unprepared, we "
  "should be ashamed. The aim is that the gift be ready as a matter of bounty, and not as of "
  "covetousness, meaning given willingly rather than extracted on the day."),
 ("insert", "God's Sufficiency", "Thanksgiving Unto God (vv.9-15)",
  "Psalm 112 is quoted of the generous man, he hath dispersed abroad, he hath given to the "
  "poor, and then the agricultural image is extended, he that ministereth seed to the sower "
  "both minister bread for your food, and multiply your seed sown. What the collection produces "
  "is described in two directions: the wants of the saints are supplied, and it is abundant "
  "also by many thanksgivings unto God. The chapter ends by putting the whole thing beside its "
  "original, thanks be unto God for his unspeakable gift."),
],
"2corinthians10": [
 ("insert", "", "Base in Presence, Bold When Absent (vv.1-2)",
  "Paul quotes his critics before answering them, who in presence am base among you, but being "
  "absent am bold toward you. The plea is made by the meekness and gentleness of Christ, and "
  "then the warning attached to it, that I may not be bold when I am present with that "
  "confidence wherewith I think to be bold against some. He is asking them to make the "
  "confrontation unnecessary."),
 ("insert", "Spiritual Warfare", "The Authority the Lord Hath Given (vv.6-9)",
  "The weapons of the previous verses are aimed inward first, having in a readiness to revenge "
  "all disobedience, when your obedience is fulfilled. Then the claim to authority is stated "
  "and immediately limited, though I should boast somewhat more of our authority, which the "
  "Lord hath given us for edification, and not for destruction, I should not be ashamed. And "
  "the reason for the letter rather than a visit, that I may not seem as if I would terrify you "
  "by letters."),
 ("insert", "The Accusation", "Measuring by Another Man's Line (vv.11-18)",
  "The answer to the charge of being bold only at a distance is that his conduct will match his "
  "writing, such will we be also in deed when we are present. Then the argument about measure, "
  "and it is aimed at rivals who had come into a church he founded: we dare not make ourselves "
  "of the number of some that commend themselves, for they measuring themselves by themselves "
  "are not wise. Paul's own rule is territorial, not boasting of things without our measure, "
  "that is, of other men's labours, and the aim stated is expansion rather than takeover, to "
  "preach the gospel in the regions beyond you. The close is a quotation, he that glorieth, let "
  "him glory in the Lord, and a test, not he that commendeth himself is approved, but whom the "
  "Lord commendeth."),
],
"2corinthians11": [
 ("insert", "", "Espoused to One Husband (vv.1-6)",
  "Would to God ye could bear with me a little in my folly. The word folly is Paul's own label "
  "for what he is about to do, and the reason he does it is jealousy of a particular kind, I "
  "have espoused you to one husband, that I may present you as a chaste virgin to Christ. The "
  "fear named is not doctrinal drift but seduction, lest by any means, as the serpent beguiled "
  "Eve through his subtilty, so your minds should be corrupted. Then the phrase he uses of his "
  "rivals throughout the chapter, sarcastically, the very chiefest apostles, and one concession "
  "about himself, though I be rude in speech, yet not in knowledge."),
 ("insert", "Espoused to One Husband", "I Robbed Other Churches (vv.7-12)",
  "The complaint against Paul was that he took no money, which in that culture implied his "
  "teaching was worth none. His answer is deliberately blunt, I robbed other churches, taking "
  "wages of them, to do you service, and when I wanted, I was chargeable to no man, for that "
  "which was lacking to me the brethren which came from Macedonia supplied. He then swears to "
  "keep it that way, as the truth of Christ is in me, no man shall stop me of this boasting, "
  "and gives his motive in one clause, that I may cut off occasion from them which desire "
  "occasion."),
 ("insert", "False Apostles", "Speaking as a Fool (vv.16-22)",
  "Let no man think me a fool, if otherwise, yet as a fool receive me. He labels the whole "
  "performance in advance, I speak it not after the Lord, but as it were foolishly, and then "
  "explains why it is necessary: seeing that many glory after the flesh, I will glory also. "
  "What follows is the sharpest thing in the letter, a list of what the Corinthians had put up "
  "with from others, ye suffer, if a man bring you into bondage, if a man devour you, if a man "
  "take of you, if a man exalt himself, if a man smite you on the face. Then the credentials, "
  "are they Hebrews? so am I, and the refrain, are they Israelites? are they the seed of "
  "Abraham? so am I."),
 ("insert", "Paul's Suffering Catalog", "Let Down in a Basket (vv.29-33)",
  "The catalogue ends not with a beating but with a sympathy, who is weak, and I am not weak? "
  "and then a statement of policy, if I must needs glory, I will glory of the things which "
  "concern mine infirmities. What he chooses as the climax of a boasting contest is the most "
  "undignified thing that ever happened to him: the governor under Aretas watching the gates of "
  "Damascus, and through a window in a basket was I let down by the wall, and escaped his "
  "hands. A man arguing about apostolic credentials finishes with being lowered out of a city in "
  "a laundry basket."),
],
"2corinthians12": [
 ("insert", "The Thorn in the Flesh", "The Signs of an Apostle (vv.11-13)",
  "I am become a fool in glorying, ye have compelled me. The responsibility for the whole "
  "passage is put on the readers, for I ought to have been commended of you. Then the claim, "
  "made once and briefly, truly the signs of an apostle were wrought among you in all patience, "
  "in signs, and wonders, and mighty deeds. And the closing sarcasm about the one thing he did "
  "differently from the rival teachers, wherein was I inferior, except it be that I myself was "
  "not burdensome to you? forgive me this wrong."),
 ("insert", "The Signs of an Apostle", "I Seek Not Yours, But You (vv.14-18)",
  "Behold, the third time I am ready to come to you, and I will not be burdensome to you. The "
  "reason is put in one clause, for I seek not yours, but you, and then in an image, the parents "
  "should lay up for the children, and the children ought not to be paying the parent. What "
  "follows is a sentence with real hurt in it, though the more abundantly I love you, the less "
  "I be loved. He also answers a suspicion about the collection directly, did Titus make a gain "
  "of you? walked we not in the same spirit?"),
 ("insert", "I Seek Not Yours, But You", "Lest I Find You Not Such As I Would (vv.19-21)",
  "Paul denies that any of this is self-defence, think ye that we excuse ourselves unto you? we "
  "speak before God in Christ, and states the object again, for your edifying. Then the fear "
  "that closes the chapter, and it is a list rather than a doctrine: lest there be debates, "
  "envyings, wraths, strifes, backbitings, whisperings, swellings, tumults. And a second fear "
  "for himself, lest my God will humble me among you, and that I shall bewail many which have "
  "sinned already. He expects the visit to be painful and says so."),
],
"2corinthians13": [
 ("insert", "", "The Third Time I Come (vv.1-4)",
  "This is the third time I am coming to you, and the Deuteronomy rule is quoted to set the "
  "terms, in the mouth of two or three witnesses shall every word be established. The warning "
  "is direct, I will not spare, and it answers a demand they had made, since ye seek a proof of "
  "Christ speaking in me. Then the argument he uses to explain what strength through weakness "
  "means, and it is christological rather than personal, though he was crucified through "
  "weakness, yet he liveth by the power of God, for we also are weak in him, but we shall live "
  "with him by the power of God toward you."),
 ("insert", "The Call to Self-Examination", "We Pray That Ye Do No Evil (vv.6-10)",
  "The stated hope is that the confrontation will be unnecessary, we pray to God that ye do no "
  "evil, not that we should appear approved, but that ye should do that which is honest, though "
  "we be as reprobates. Paul is willing to look wrong if they are right, which is the reverse "
  "of the accusation against him. Then the sentence that gives the letter its purpose, "
  "therefore I write these things being absent, lest being present I should use sharpness, "
  "according to the power which the Lord hath given me to edification, and not to destruction."),
 ("insert", "We Pray That Ye Do No Evil", "Be Perfect, Be of Good Comfort (vv.11-13)",
  "Finally, brethren, farewell. Four imperatives that read as a summary of the whole "
  "correspondence: be perfect, be of good comfort, be of one mind, live in peace. The promise "
  "attached is a title used nowhere else quite this way, and the God of love and peace shall be "
  "with you. Then the ordinary close, greet one another with an holy kiss, all the saints salute "
  "you."),
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
            if op[0] == "retitle":
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
