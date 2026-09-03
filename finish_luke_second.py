#!/usr/bin/env python3
"""
Luke, second pass: chapters 15 to 24. Ten pages, and this completes the book.

luke22 is the largest single omission left in the project: seventy-one verses carrying
two sections, 'The Dispute About Greatness (vv.24-30)' and 'Jesus' Prayer for Peter
(vv.31-32)'. The Last Supper, Gethsemane, the arrest, the denial and the council
hearing were all undescribed, and what had a heading was the argument about rank at
the table.

luke23 kept the hearing before Herod and the repentant thief and lost the trial, the
crowd, the road to the cross, the crucifixion, the darkness and the burial. luke15
kept the prodigal son and lost the lost sheep and the lost coin, which are the two
parables that set it up and share its structure.

luke19 lost the parable of the pounds and the entry into Jerusalem, keeping Zacchaeus
and the weeping over the city. luke21 lost both halves of the Olivet discourse around
the section on Jerusalem's fall.

Usage:
    python3 finish_luke_second.py [--check]
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

OPS = {
"luke15": [
 ("", "The Lost Sheep and the Lost Coin (vv.1-10)",
  "The chapter opens with the complaint that produced all three parables, this man receiveth "
  "sinners, and eateth with them. The first answer is a question about ordinary practice, what man "
  "of you, having an hundred sheep, if he lose one, doth not leave the ninety and nine, and go "
  "after that which is lost? The second is the same shape in a house rather than a field, a woman "
  "with ten pieces of silver who lights a candle and sweeps. Both end in a party, and both are "
  "given the same interpretation almost word for word, joy shall be in heaven over one sinner "
  "that repenteth. The repetition is deliberate, and the third parable will break the pattern by "
  "giving the lost thing a will of its own."),
],
"luke16": [
 ("The Unjust Steward", "The Law and the Prophets Until John (vv.14-18)",
  "The Pharisees heard all these things, and they derided him, and Luke gives the reason in one "
  "word, they were covetous. The answer is about audience, ye are they which justify yourselves "
  "before men, but God knoweth your hearts, with a sentence that cuts at the whole idea of "
  "reputation, that which is highly esteemed among men is abomination in the sight of God. Then "
  "three verses that sit oddly together and are usually read past: the law and the prophets were "
  "until John, since that time the kingdom of God is preached, it is easier for heaven and earth "
  "to pass than one tittle of the law to fail, and a flat prohibition of divorce and remarriage. "
  "Luke offers no bridge between them and neither should a summary."),
],
"luke17": [
 ("", "Offences, Forgiveness, and Faith as a Grain (vv.1-6)",
  "Three sayings in six verses and each is uncomfortable. The first is a warning to whoever causes "
  "a little one to stumble, better that a millstone were hanged about his neck. The second sets no "
  "limit on forgiveness and no limit on the frequency, if he trespass against thee seven times in "
  "a day, and seven times in a day turn again to thee, saying, I repent, thou shalt forgive him. "
  "The apostles' response to that is the one recorded prayer for more faith in the Gospels, Lord, "
  "increase our faith, and the answer is about size rather than quantity, if ye had faith as a "
  "grain of mustard seed, ye might say unto this sycamine tree, Be thou plucked up by the root."),
],
"luke18": [
 ("The Pharisee and the Tax Collector", "Suffer Little Children (vv.15-17)",
  "The disciples rebuke those bringing infants, and the correction is short and the reason turns "
  "the children into the standard, of such is the kingdom of God. Then the sentence that ties this "
  "paragraph to the two parables before it and the rich ruler after it, whosoever shall not "
  "receive the kingdom of God as a little child shall in no wise enter therein. The widow prayed "
  "without standing, the publican prayed without merit, the child has neither, and the ruler has "
  "both."),
 ("Suffer Little Children", "The Rich Ruler, and the Camel (vv.18-30)",
  "A ruler asks what he must do to inherit eternal life and is first corrected on his opening "
  "word, why callest thou me good? none is good, save one, that is, God. The commandments he "
  "recites are kept from his youth up, and Luke does not dispute it. The one thing lacking is "
  "specific and total, sell all that thou hast, and distribute unto the poor. He was very "
  "sorrowful, for he was very rich. Then the camel and the needle's eye, the question who then can "
  "be saved, and the answer that removes it from human capacity altogether, the things which are "
  "impossible with men are possible with God."),
 ("The Rich Ruler, and the Camel", "The Third Prediction, and the Blind Man (vv.31-43)",
  "The third prediction is the most explicit and Luke adds a note about its reception that is "
  "harder than Mark's, they understood not the things which were spoken. Then the blind man at "
  "Jericho, and what Luke keeps is the persistence: he asks what the noise is, he is told, he "
  "cries out, he is rebuked by them which went before, and he cried so much the more a great deal. "
  "The question put to him is the one nobody asks a beggar, what wilt thou that I shall do unto "
  "thee? and the answer is Lord, that I may receive my sight. The chapter that began with a widow "
  "who would not stop asking ends with a blind man who would not."),
],
"luke19": [
 ("Zacchaeus", "The Parable of the Pounds (vv.11-28)",
  "Luke gives the reason for the parable before telling it, because they thought that the kingdom "
  "of God should immediately appear, so it is aimed at expectation rather than at stewardship. A "
  "nobleman goes into a far country to receive a kingdom, and the detail Luke alone includes is "
  "political, his citizens hated him, and sent a message after him, saying, We will not have this "
  "man to reign over us. Ten servants get a pound each. The accounting rewards the first two and "
  "turns on the third, who kept his in a napkin and explains himself by an accusation, I feared "
  "thee, because thou art an austere man. The answer takes his own premise and uses it, "
  "wherefore then gavest not thou my money into the bank?"),
 ("The Parable of the Pounds", "The Entry into Jerusalem (vv.29-40)",
  "The arrangements for the colt are given in unusual detail, including the password, and if any "
  "man ask you, Why do ye loose him? thus shall ye say unto him, Because the Lord hath need of "
  "him. The descent of the mount of Olives is where the crowd begins, and Luke's version of the "
  "shout is distinctive, peace in heaven, and glory in the highest, which answers the angels' song "
  "at the nativity. Then the Pharisees ask him to rebuke his disciples, and the reply is the line "
  "the passage is remembered for, if these should hold their peace, the stones would immediately "
  "cry out."),
 ("Jesus Weeping Over Jerusalem", "The Temple Cleansed (vv.45-48)",
  "Luke's account of the cleansing is four verses and has no whip and no tables overturned, only "
  "the action and the quotation, my house is the house of prayer, but ye have made it a den of "
  "thieves. What he adds is the standoff that follows: he taught daily in the temple, the chief "
  "priests and scribes sought to destroy him, and could not find what they might do, for all the "
  "people were very attentive to hear him. The crowd is what keeps him alive for a week."),
],
"luke20": [
 ("The Tribute Question", "The Sadducees and the Resurrection (vv.27-40)",
  "The Sadducees bring the case of seven brothers, and Luke's version of the answer is the fullest "
  "of the three Gospels. The children of this world marry, but they which shall be accounted "
  "worthy to obtain that world neither marry, nor are given in marriage, neither can they die any "
  "more. Then the argument from the burning bush, which the Sadducees accepted as scripture, and "
  "the clause Luke alone adds, for all live unto him. Some of the scribes concede the point out "
  "loud, Master, thou hast well said, and Luke notes the result, after that they durst not ask him "
  "any question at all."),
 ("The Sadducees and the Resurrection", "David's Son, and Beware of the Scribes (vv.41-47)",
  "He asks the question this time, how say they that Christ is David's son? and puts Psalm 110 "
  "against it, David therefore calleth him Lord, how is he then his son? No answer is recorded. "
  "Then, in the hearing of all the people, a warning about the men he has been debating: beware of "
  "the scribes, which desire to walk in long robes, and love greetings in the markets, and the "
  "highest seats in the synagogues. The charge underneath the vanity is which devour widows' "
  "houses, and for a shew make long prayers, and Luke places it immediately before the widow with "
  "two mites."),
],
"luke21": [
 ("The Widow's Mites", "Not One Stone Upon Another (vv.5-19)",
  "Somebody admires the stonework and the reply is that not one stone shall be left upon another. "
  "The question that follows is about timing and signs, and the first instruction is a warning "
  "against being taken in, take heed that ye be not deceived, for many shall come in my name. "
  "Wars, earthquakes, famines and pestilences are described as things that must first come to "
  "pass, but the end is not by and by. Then the section turns personal and practical: they will be "
  "delivered up to synagogues and prisons, and Luke's promise about that is specific, I will give "
  "you a mouth and wisdom, which all your adversaries shall not be able to gainsay. The two "
  "closing sentences are held together without resolution, some of you shall they cause to be put "
  "to death, and there shall not an hair of your head perish."),
 ("The Fall of Jerusalem", "Signs, the Fig Tree, and Watch Ye (vv.25-38)",
  "The signs widen from a city to the sky, and Luke describes the effect on people rather than the "
  "phenomena, men's hearts failing them for fear, and for looking after those things which are "
  "coming on the earth. Then the Son of man coming in a cloud, and an instruction that inverts "
  "the fear, when these things begin to come to pass, then look up, and lift up your heads, for "
  "your redemption draweth nigh. The fig tree parable follows, and then a warning about the "
  "specific way readiness is lost, lest at any time your hearts be overcharged with surfeiting, "
  "and drunkenness, and cares of this life. Luke closes with a note on the week's routine, in the "
  "day time he was teaching in the temple, and at night he went out and abode in the mount of "
  "Olives."),
],
"luke22": [
 ("", "The Passover Prepared (vv.1-13)",
  "The chapter opens on a conspiracy that has a problem, they sought how they might kill him, for "
  "they feared the people, and the problem is solved by an insider. Luke's account of Judas is "
  "brief and stark, then entered Satan into Judas, and he went his way, and communed with the "
  "chief priests how he might betray him unto them. Money is mentioned but not counted here. Then "
  "the arrangements, and they have the same shape as the colt in chapter 19: Peter and John are "
  "sent to follow a man bearing a pitcher of water, and the room is already prepared."),
 ("The Passover Prepared", "The Last Supper (vv.14-23)",
  "With desire I have desired to eat this passover with you before I suffer. Luke's account has two "
  "cups, one before the bread and one after, which is why his version is the one liturgies argue "
  "over. The words over the bread and cup are given with the clause Paul also records, this do in "
  "remembrance of me, and the cup is named the new testament in my blood. Then the announcement of "
  "the betrayal, and Luke's placing of it after the meal rather than before means the traitor was "
  "served. The disciples' response is not horror but investigation, they began to enquire among "
  "themselves, which of them it was that should do this thing."),
 ("Jesus' Prayer for Peter", "I Will Not Deny Thee (vv.33-38)",
  "Peter answers the warning with an offer, Lord, I am ready to go with thee, both into prison, "
  "and to death, and receives the prediction in reply, the cock shall not crow this day, before "
  "that thou shalt thrice deny that thou knowest me. Then a passage found only in Luke and much "
  "argued over: he reminds them that they lacked nothing when sent out without purse or scrip, and "
  "then reverses the instruction, he that hath no sword, let him sell his garment, and buy one. "
  "When they produce two, the answer closes the subject rather than approving it, it is enough."),
 ("I Will Not Deny Thee", "Gethsemane (vv.39-46)",
  "Luke's Gethsemane is the shortest and the most medical. The instruction given twice, once "
  "before and once after, is pray that ye enter not into temptation. The prayer itself is one "
  "sentence, Father, if thou be willing, remove this cup from me, nevertheless not my will, but "
  "thine, be done. Then two verses absent from some manuscripts and impossible to leave out of a "
  "description, an angel strengthening him, and being in an agony he prayed more earnestly, and "
  "his sweat was as it were great drops of blood falling down to the ground. The disciples are "
  "found sleeping, and Luke alone offers a reason for it, sleeping for sorrow."),
 ("Gethsemane", "The Arrest (vv.47-53)",
  "Judas draws near to kiss him and the question stops him mid-gesture, Judas, betrayest thou the "
  "Son of man with a kiss? One of them strikes the high priest's servant, and Luke, alone of the "
  "four, records the repair, he touched his ear, and healed him. The words to the arresting party "
  "are about method rather than injustice, be ye come out, as against a thief, with swords and "
  "staves? I was daily with you in the temple, and ye stretched forth no hands against me. Then "
  "the sentence that gives the night its character, but this is your hour, and the power of "
  "darkness."),
 ("The Arrest", "Peter Denies Him (vv.54-62)",
  "Peter follows afar off and sits down among them at the fire, and the three denials are "
  "prompted by a maid, a man, and another man, over about the space of one hour. Luke's version "
  "keeps two details the others lack. The cock crows while Peter is still speaking. And then the "
  "Lord turned, and looked upon Peter, which is the only place in the Gospels the look is "
  "recorded. He remembered the word of the Lord, and Peter went out, and wept bitterly."),
 ("Peter Denies Him", "Mocked, and Before the Council (vv.63-71)",
  "The mockery is described as a game with a rule, they blindfolded him, and struck him on the "
  "face, and asked, Prophesy, who is it that smote thee? Then the morning hearing, and it turns "
  "on two questions. Art thou the Christ? tell us, answered with a refusal to play, if I tell you, "
  "ye will not believe, and then a claim anyway, hereafter shall the Son of man sit on the right "
  "hand of the power of God. Art thou then the Son of God? answered with ye say that I am. What "
  "need we any further witness? for we ourselves have heard of his own mouth."),
],
"luke23": [
 ("", "Before Pilate (vv.1-5)",
  "The charge presented to Pilate is translated out of theology into politics, and Luke lists "
  "three counts: perverting the nation, forbidding to give tribute to Caesar, and saying that he "
  "himself is Christ a King. The second is simply false, as chapter 20 has already shown. Pilate "
  "asks one question, gets one answer, and delivers a verdict in the first five verses, I find no "
  "fault in this man. The accusers respond not with evidence but with volume and geography, he "
  "stirreth up the people, beginning from Galilee to this place, which is what gives Pilate the "
  "idea of sending him to Herod."),
 ("The Trial Before Herod", "Barabbas, and the Third Verdict (vv.13-25)",
  "Pilate states his finding for the second time and adds Herod's, and then proposes flogging as a "
  "compromise, I will therefore chastise him, and release him. Luke has Pilate declare him "
  "innocent three separate times and hand him over anyway, which is the point the chapter is "
  "making about Roman justice. The crowd asks for Barabbas, and Luke tells us exactly who that "
  "was, who for a certain sedition made in the city, and for murder, was cast into prison, so the "
  "man released is guilty of what Jesus was charged with. The last verse is a sentence about "
  "authority, and he delivered Jesus to their will."),
 ("Barabbas, and the Third Verdict", "The Road, and the Daughters of Jerusalem (vv.26-31)",
  "Simon of Cyrene is compelled to carry the cross, and then Luke records something no other "
  "Gospel does: a great company of people, and of women, which also bewailed and lamented him, "
  "and he turns to speak to them. What he says is not consolation, weep not for me, but weep for "
  "yourselves, and for your children, and it is a warning about the city rather than about "
  "himself. The saying that follows is the bleakest thing he says on the way, blessed are the "
  "barren, and the wombs that never bare, with a question left open at the end, if they do these "
  "things in a green tree, what shall be done in the dry?"),
 ("The Road, and the Daughters of Jerusalem", "The Crucifying, and the Mocking (vv.32-38)",
  "Two malefactors are led with him, and the crucifixion itself is one clause, there they "
  "crucified him. Then the first of the seven sayings, and Luke alone has it, Father, forgive "
  "them, for they know not what they do. The soldiers part his raiment, casting lots. The mocking "
  "comes from three directions and all three use the same word: the rulers say let him save "
  "himself, the soldiers say save thyself, and the superscription over him reads THIS IS THE KING "
  "OF THE JEWS. Luke notes that the people stood beholding, which distinguishes them from the "
  "rulers."),
 ("The Repentant Thief", "Darkness, and the Last Cry (vv.44-49)",
  "Darkness over all the earth from the sixth hour to the ninth, and Luke gives a cause, the sun "
  "was darkened. The veil of the temple is rent in the midst. Then the last words, and Luke's are "
  "different from Mark's, Father, into thy hands I commend my spirit, which is Psalm 31 and is a "
  "line a Jewish child would say at bedtime. The centurion's verdict in Luke is also different, "
  "certainly this was a righteous man. Then two crowds: the people who smote their breasts and "
  "went home, and his acquaintance and the women that followed him from Galilee, standing afar "
  "off, beholding these things."),
 ("Darkness, and the Last Cry", "Joseph, and the Sabbath Drawing On (vv.50-56)",
  "Joseph is described in terms that make his position uncomfortable, a counsellor, and he was a "
  "good man, and a just, with a clause Luke inserts to explain it, the same had not consented to "
  "the counsel and deed of them. The burial is quick and the details are the kind that matter "
  "later: a sepulchre hewn in stone, wherein never man before was laid, and the day is the "
  "preparation, and the sabbath drew on. The women follow and note the place. Then the sentence "
  "that explains why they come back and why the spices are late, and they rested the sabbath day "
  "according to the commandment."),
],
"luke24": [
 ("", "The Empty Sepulchre (vv.1-12)",
  "The women come with the spices they prepared before the sabbath, find the stone rolled away, "
  "and are much perplexed. Two men in shining garments ask a question rather than making an "
  "announcement, why seek ye the living among the dead? and then tell them to remember something "
  "they were already told, remember how he spake unto you when he was yet in Galilee. The women "
  "are named, and the response of the eleven is recorded without charity, their words seemed to "
  "them as idle tales, and they believed them not. Peter goes anyway, sees the linen clothes laid "
  "by themselves, and departs wondering, which is not the same as believing."),
 ("The Physical Resurrection", "Then Opened He Their Understanding (vv.44-45)",
  "Two verses that describe the method rather than an event. These are the words which I spake "
  "unto you, while I was yet with you, that all things must be fulfilled which were written in the "
  "law of Moses, and in the prophets, and in the psalms. All three divisions of the Hebrew Bible "
  "are named. Then the clause that explains the whole chapter, and the Emmaus road before it, "
  "then opened he their understanding, that they might understand the scriptures. The problem was "
  "never the evidence."),
 ("The Great Commission in Luke", "Carried Up Into Heaven (vv.50-53)",
  "The Gospel ends where it began, in the temple. He leads them out as far as Bethany, lifts up "
  "his hands and blesses them, and while he blessed them he was parted from them. The last posture "
  "anyone sees is a blessing. Luke's closing three clauses are all about what the disciples did "
  "next, and none of them is fear: they worshipped him, and returned to Jerusalem with great joy, "
  "and were continually in the temple, praising and blessing God. Volume two of the same work "
  "begins in that room."),
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
        for after, label, prose in ops:
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
