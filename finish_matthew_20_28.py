#!/usr/bin/env python3
"""
Matthew, third pass: chapters 20 to 28. This completes the book and clears the last
page in the project that had no verse-range section at all outside the five untouched
blocks.

matthew26 is the longest chapter in the Gospel at seventy-five verses and it had
nothing: the anointing at Bethany, the bargain with Judas, the Last Supper, Gethsemane,
the arrest, the trial before Caiaphas and Peter's denial, none of it described.
matthew27 had one section, 'The Veil Torn (v.51)', for sixty-six verses, so a single
verse in the middle of the crucifixion stood for the whole of Pilate, Barabbas, the
mocking, the death and the burial. matthew24 and matthew25 had nothing at all, which
means the Olivet discourse and the three parables of readiness were both undescribed.

matthew23's seven woes and matthew21's entry, temple cleansing and fig tree were in
the same state.

Usage:
    python3 finish_matthew_20_28.py [--check]
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
"matthew20": [
 ("", "The Labourers in the Vineyard (vv.1-16)",
  "A parable found only in Matthew, and it exists to unsettle the promise Peter has just been given "
  "at the end of chapter 19. Men are hired at dawn, at the third, sixth, ninth and eleventh hours, "
  "and all are paid a penny. The complaint of the first group is not that they were underpaid but "
  "that the others were not, thou hast made them equal unto us, which have borne the burden and heat "
  "of the day. The answer concedes the contract and denies the grievance, didst not thou agree with "
  "me for a penny? is thine eye evil, because I am good? The parable closes with the sentence that "
  "framed it, so the last shall be first, and the first last."),
 ("The Labourers in the Vineyard", "The Third Prediction, and the Cup (vv.17-24)",
  "The third passion prediction is the most detailed, and in Matthew the request that follows it is "
  "made by the mother of James and John rather than by the brothers. The reply is addressed to them "
  "anyway, ye know not what ye ask, and the question put is about the cup. The other ten are "
  "indignant, and the correction is aimed at all twelve: the princes of the Gentiles exercise "
  "dominion, but it shall not be so among you. Then the sentence that explains the death and is "
  "Matthew's only statement of its purpose, even as the Son of man came not to be ministered unto, "
  "but to minister, and to give his life a ransom for many."),
 ("Servant Leadership", "Two Blind Men at Jericho (vv.29-34)",
  "Matthew has two blind men where Mark has one, and the scene is built on persistence against "
  "discouragement: the multitude rebuked them, because they should hold their peace, but they cried "
  "the more. The title they use is the one that matters this close to Jerusalem, thou son of David. "
  "The question asked of them is the same one asked of the mother a few verses earlier, what will ye "
  "that I shall do unto you? and the answers are instructive against each other. She asked for "
  "thrones. They ask that our eyes may be opened. Matthew's closing clause is that they followed "
  "him."),
],
"matthew21": [
 ("", "The Entry into Jerusalem (vv.1-11)",
  "The arrangements are given in detail, including what to say if challenged, and Matthew attaches "
  "Zechariah 9:9 to them. He is the only evangelist to mention both an ass and a colt, following the "
  "two halves of the Hebrew line. The crowd spreads garments and branches and shouts Hosanna to the "
  "son of David, which is a royal acclamation rather than a religious one. Matthew's note on the "
  "effect is about the city rather than the procession, all the city was moved, saying, Who is this? "
  "and the answer the crowd gives is smaller than the shout, this is Jesus the prophet of Nazareth "
  "of Galilee."),
 ("The Entry into Jerusalem", "The Temple, and the Fig Tree (vv.12-22)",
  "The cleansing is immediate and Matthew pairs two quotations, my house shall be called the house of "
  "prayer, but ye have made it a den of thieves. What he alone adds is what happened next in the same "
  "space: the blind and the lame came to him in the temple, and he healed them, and children were "
  "shouting there, which the chief priests object to. The fig tree follows, and Matthew compresses "
  "the two days into one scene so that the withering is immediate, and the lesson drawn is about "
  "prayer rather than judgment, if ye have faith, and doubt not, ye shall say unto this mountain, Be "
  "thou removed."),
 ("The Temple, and the Fig Tree", "By What Authority, and Two Sons (vv.23-32)",
  "The question is jurisdictional and the counter-question about John's baptism traps them between "
  "the crowd and their own record. They answer we cannot tell and get no answer in return. Then a "
  "parable only Matthew has: two sons, one who refuses and goes, one who agrees and does not. The "
  "question put to them is which of the twain did the will of his father, and they answer correctly, "
  "which is what makes the application unanswerable, the publicans and the harlots go into the "
  "kingdom of God before you. The reason given is a matter of record, John came unto you, and ye "
  "believed him not, but the publicans and the harlots believed him."),
 ("By What Authority, and Two Sons", "The Wicked Husbandmen (vv.33-46)",
  "The vineyard of Isaiah 5, servants sent and beaten and stoned and killed, and then the son. The "
  "reasoning of the tenants is quoted, this is the heir, come, let us kill him, and let us seize on "
  "his inheritance. Then Matthew has him ask them to pass sentence on the story, and they do it, "
  "which is the trap: he will miserably destroy those wicked men. The stone which the builders "
  "rejected is quoted, with a sentence that only Matthew adds, the kingdom of God shall be taken from "
  "you, and given to a nation bringing forth the fruits thereof. They understood that he spake of "
  "them, and could not arrest him because the multitude took him for a prophet."),
],
"matthew22": [
 ("", "The Wedding Feast (vv.1-14)",
  "A king's son's marriage, invitations refused, servants mistreated and killed, and a city "
  "destroyed, which in Matthew's telling reads unmistakably against Jerusalem. Then the doors thrown "
  "open, go ye therefore into the highways, and as many as ye shall find, bid to the marriage, and "
  "the hall filled with both bad and good. The ending belongs only to Matthew and is the part readers "
  "trip over: a man without a wedding garment, questioned, speechless, and cast out. The moral given "
  "is not about generosity but about selection, for many are called, but few are chosen."),
 ("The Wedding Feast", "Render Unto Caesar (vv.15-22)",
  "The trap is set with flattery Matthew labels as such, they took counsel how they might entangle "
  "him in his talk, and the alliance behind it is unnatural, the Pharisees with the Herodians. The "
  "question about tribute has no safe answer, which is the point. He asks for the coin and asks whose "
  "image and superscription it carries, so the answer is drawn out of them, render therefore unto "
  "Caesar the things which are Caesar's, and unto God the things that are God's. They marvelled, and "
  "left him, and went their way."),
 ("Render Unto Caesar", "The Sadducees, and the Great Commandment (vv.23-40)",
  "The Sadducees bring seven brothers and one widow, and the reply names two errors, ye do err, not "
  "knowing the scriptures, nor the power of God. The first is corrected by describing the "
  "resurrection state, they are as the angels of God in heaven, and the second from Exodus, with the "
  "tense doing the work, God is not the God of the dead, but of the living. Then a lawyer asks which "
  "is the great commandment, and the answer gives two rather than one, love God and love thy "
  "neighbour as thyself, with a claim about the whole law hanging on them."),
 ("The Sadducees, and the Great Commandment", "David's Son and David's Lord (vv.41-46)",
  "This time he asks. What think ye of Christ? whose son is he? They answer the son of David, and "
  "Psalm 110 is put against it, the LORD said unto my Lord, Sit thou on my right hand. If David then "
  "call him Lord, how is he his son? No answer is given. Matthew's closing sentence ends the week's "
  "arguments, and no man was able to answer him a word, neither durst any man from that day forth ask "
  "him any more questions, which is why chapter 23 is a monologue."),
],
"matthew23": [
 ("", "They Say, and Do Not (vv.1-12)",
  "The address is to the multitude and the disciples about the scribes and Pharisees, and it opens "
  "with an instruction to obey them, whatsoever they bid you observe, that observe and do, but do not "
  "ye after their works. The charge is inconsistency rather than error. Then the specifics, and all "
  "are about visibility: heavy burdens laid on others, phylacteries made broad, the uppermost rooms "
  "at feasts, greetings in the markets, and the title Rabbi. Three titles are then forbidden to the "
  "disciples, Rabbi, father and master, and the section closes on the reversal that governs the "
  "chapter, he that is greatest among you shall be your servant."),
 ("They Say, and Do Not", "The Seven Woes (vv.13-33)",
  "Woe is a lament as much as a curse, and the seven are specific charges rather than general abuse. "
  "Shutting the kingdom and not entering it. Compassing sea and land for one convert and making him "
  "worse. An elaborate scheme of oath-technicalities, answered by pointing out that the temple "
  "sanctifies the gold and the altar the gift. Tithing mint, anise and cummin while omitting "
  "judgment, mercy and faith, with the image of straining a gnat and swallowing a camel. Cleaning "
  "the outside of the cup. Whited sepulchres, beautiful outward and full of dead men's bones. And "
  "building the tombs of the prophets their fathers killed, which is the one that turns into the "
  "sentence, fill ye up then the measure of your fathers."),
 ("The Seven Woes", "O Jerusalem, Jerusalem (vv.34-39)",
  "The tone changes in the last six verses from prosecution to grief. Prophets and wise men and "
  "scribes sent and killed, from the blood of righteous Abel to Zacharias, which spans the whole "
  "Hebrew canon as it was then ordered. Then the lament, and the image is domestic and maternal, how "
  "often would I have gathered thy children together, even as a hen gathereth her chickens under her "
  "wings, and ye would not. Behold, your house is left unto you desolate. The last sentence leaves "
  "the door ajar, ye shall not see me henceforth, till ye shall say, Blessed is he that cometh in the "
  "name of the Lord."),
],
"matthew24": [
 ("", "Not One Stone Upon Another (vv.1-14)",
  "A disciple points out the buildings and the reply is that not one stone shall be left upon "
  "another. The question that follows has three parts and Matthew keeps them joined, when shall "
  "these things be? and what shall be the sign of thy coming, and of the end of the world? The first "
  "answer is a warning against being deceived, for many shall come in my name, saying, I am Christ. "
  "Wars, famines, pestilences and earthquakes are called the beginning of sorrows, not the end. Then "
  "persecution, betrayal, cooling love, and the one condition given for the end, this gospel of the "
  "kingdom shall be preached in all the world, and then shall the end come."),
 ("Not One Stone Upon Another", "The Abomination, and the Flight (vv.15-28)",
  "The sign given is a specific one, the abomination of desolation, spoken of by Daniel the prophet, "
  "with an aside to the reader rather than the hearers, whoso readeth, let him understand. What "
  "follows is practical instruction for a day: flee to the mountains, do not go back into the house "
  "for anything, and two clauses of sympathy, woe unto them that are with child, and pray that your "
  "flight be not in the winter, neither on the sabbath day. Then false Christs with signs and "
  "wonders, and a warning against chasing reports, believe it not, for as the lightning cometh out "
  "of the east, and shineth even unto the west, so shall also the coming of the Son of man be."),
 ("The Abomination, and the Flight", "The Fig Tree, and No Man Knoweth (vv.29-44)",
  "The sun darkened, the moon not giving light, the stars falling, and then the Son of man coming in "
  "the clouds with power and great glory. The fig tree parable says the season can be read, and the "
  "next sentence says the date cannot, of that day and hour knoweth no man, no, not the angels of "
  "heaven, but my Father only. Then Noah is used as the pattern, and what is stressed is normality "
  "rather than wickedness, they were eating and drinking, marrying and giving in marriage, until the "
  "day that Noe entered into the ark. Two in a field, two at a mill, one taken and one left. The "
  "instruction drawn from all of it is one word, watch."),
 ("The Fig Tree, and No Man Knoweth", "The Faithful and Evil Servant (vv.45-51)",
  "The discourse ends with a servant left in charge of a household, and the difference between the "
  "two versions of him is what he does with a delay. The faithful one is found giving them meat in "
  "due season. The evil one says in his heart, My lord delayeth his coming, and begins to smite his "
  "fellowservants, and to eat and drink with the drunken. The point is not that the second disbelieves "
  "the return but that he has priced it as distant. The chapter closes on the sentence that leads "
  "straight into the three parables of chapter 25."),
],
"matthew25": [
 ("", "The Ten Virgins (vv.1-13)",
  "Five wise and five foolish, and the only difference between them is oil in reserve. All ten sleep, "
  "which is worth noticing: the failure is not staying awake but being unprepared for a delay. The "
  "refusal to share is practical rather than unkind, lest there be not enough for us and you, and by "
  "the time the others return the door is shut. The exchange at the door is the coldest sentence in "
  "the chapter, verily I say unto you, I know you not. The moral given is the same word chapter 24 "
  "ended on, watch therefore, for ye know neither the day nor the hour."),
 ("The Ten Virgins", "The Talents (vv.14-30)",
  "Three servants and unequal sums, to every man according to his several ability, and the "
  "distribution is not the point of the parable. The first two double what they were given and are "
  "commended in identical words. The third buries his and explains himself with an accusation, I knew "
  "thee that thou art an hard man, and the answer uses his own premise against him, thou knewest that "
  "I reap where I sowed not, wherefore then hast thou not put my money to the exchangers? The sin is "
  "inactivity justified by a theory about the master. The talent is taken and given to the man who "
  "already had ten."),
 ("The Talents", "The Sheep and the Goats (vv.31-46)",
  "The last teaching in Matthew before the passion, and the criterion is unexpected. Both groups are "
  "surprised, and both ask the same question, when did we see thee? Neither recognised him at the "
  "time, which means the deeds were not done for credit. Six actions are listed twice, and they are "
  "all mundane: food, drink, shelter, clothing, visiting the sick and the prisoner. The identification "
  "is the sentence the passage turns on, inasmuch as ye have done it unto one of the least of these "
  "my brethren, ye have done it unto me. The judgment separates on the basis of what was done to "
  "people nobody was watching."),
],
"matthew26": [
 ("", "The Plot, and the Anointing at Bethany (vv.1-16)",
  "Matthew closes the last discourse with his usual formula and then dates the plot, ye know that "
  "after two days is the feast of the passover. The chief priests want it done without a riot, not on "
  "the feast day, lest there be an uproar among the people. Then the anointing at Bethany, and the "
  "objection is costed, this ointment might have been sold for much, and given to the poor. The "
  "defence given is a burial, she did it for my burial, with a promise attached that this shall be "
  "told for a memorial of her. Judas goes to the priests immediately afterwards, and Matthew alone "
  "gives the figure, thirty pieces of silver."),
 ("The Plot, and the Anointing at Bethany", "The Last Supper (vv.17-30)",
  "The room is arranged through an unnamed man in the city. At the table the betrayal is announced "
  "and each disciple asks the same question, Lord, is it I? Matthew alone records Judas asking it too, "
  "and the answer, thou hast said. Then the bread and the cup, and Matthew's version of the words over "
  "the cup includes a clause the others do not, for the remission of sins. The promise that follows "
  "looks past the night, I will not drink henceforth of this fruit of the vine, until that day when I "
  "drink it new with you in my Father's kingdom. And they sang a hymn before going out."),
 ("The Last Supper", "Gethsemane (vv.31-46)",
  "Zechariah is quoted on the shepherd smitten and the sheep scattered, and Peter's denial is "
  "predicted and denied by everyone present, likewise also said all the disciples. In the garden he "
  "takes three and tells them something he tells nobody else, my soul is exceeding sorrowful, even "
  "unto death. Three prayers and the wording shifts between them, from if it be possible to thy will "
  "be done. The disciples sleep three times, and the two sentences said to them are held together "
  "without resolution, the spirit indeed is willing, but the flesh is weak, and then, rise, let us be "
  "going."),
 ("Gethsemane", "The Arrest (vv.47-56)",
  "The sign agreed with the party is a kiss, and Matthew gives the greeting that goes with it, hail, "
  "master. The answer is two words in the Greek, friend, wherefore art thou come? One of them draws a "
  "sword and cuts off an ear, and the rebuke has three parts: all they that take the sword shall "
  "perish with the sword, twelve legions of angels are available and not requested, and the scriptures "
  "must be fulfilled. Then the question about method, are ye come out as against a thief, with swords "
  "and staves? And the flattest sentence in the chapter, then all the disciples forsook him, and fled."),
 ("The Arrest", "Before Caiaphas, and Peter's Denial (vv.57-75)",
  "The hearing has a problem Matthew states plainly: they sought false witness and the two they found "
  "could not agree. He answers nothing until put under oath, and then answers directly, thou hast "
  "said, with Daniel 7 added, hereafter shall ye see the Son of man sitting on the right hand of "
  "power. The high priest tears his clothes. Then the spitting and the buffeting and the game, "
  "prophesy unto us, thou Christ, who is he that smote thee? Peter's three denials escalate from I "
  "know not what thou sayest to an oath and then to a curse, and the chapter ends in four words, and "
  "he went out, and wept bitterly."),
],
"matthew27": [
 ("", "Judas, and the Potter's Field (vv.1-10)",
  "Only Matthew tells what became of Judas. He brings the money back with a confession, I have sinned "
  "in that I have betrayed the innocent blood, and the priests refuse responsibility in a phrase that "
  "matches their own conduct, see thou to that. The silver is thrown down in the temple, and the "
  "priests will not put it in the treasury because it is the price of blood, so they buy a field with "
  "it. Matthew's fulfilment note cites Jeremiah for a text closest to Zechariah, which readers have "
  "puzzled over for centuries, and the field is named the field of blood."),
 ("Judas, and the Potter's Field", "Before Pilate, and Barabbas (vv.11-26)",
  "One question, one answer, and then silence, insomuch that the governor marvelled greatly. Matthew "
  "alone records two things here. Pilate's wife sends word during the hearing, have thou nothing to "
  "do with that just man, for I have suffered many things this day in a dream because of him. And "
  "Pilate washes his hands in front of the crowd and says I am innocent of the blood of this just "
  "person. Matthew states his motive for giving in without softening it, he knew that for envy they "
  "had delivered him, and yet he was willing to content the people."),
 ("Before Pilate, and Barabbas", "The Mocking, and the Road (vv.27-34)",
  "The whole band is gathered in the common hall for something outside the sentence: a scarlet robe, a "
  "crown of thorns, a reed for a sceptre, and a mock salute, hail, King of the Jews. They spit on him "
  "and take the reed and strike him on the head with it. Then the robe comes off and his own clothes "
  "go back on, and Simon of Cyrene is compelled to carry the cross. At Golgotha they offer vinegar "
  "mingled with gall, and he would not drink."),
 ("The Mocking, and the Road", "The Crucifying (vv.35-44)",
  "The crucifixion itself is one clause, and they crucified him, and what Matthew records around it "
  "is the dividing of the garments, the superscription, THIS IS JESUS THE KING OF THE JEWS, and two "
  "thieves. Then three sets of mockers using the same argument. Passers-by throw his own words about "
  "the temple back at him. The chief priests and scribes and elders make it a taunt about "
  "consistency, he saved others, himself he cannot save, and add a condition, let him now come down "
  "from the cross, and we will believe him. The thieves cast the same in his teeth."),
 ("The Veil Torn", "The Earthquake, and the Centurion (vv.45-50,52-56)",
  "Darkness from the sixth hour to the ninth, and then the cry Matthew keeps in Aramaic before "
  "translating, Eli, Eli, lama sabachthani, which is the first line of Psalm 22. Some hear Elias. "
  "Then the death, and after the veil, three things only Matthew reports: an earthquake, rocks rent, "
  "and graves opened with many bodies of the saints appearing in the city. The centurion's verdict "
  "here is a confession, truly this was the Son of God, and the section ends by naming the women "
  "watching from afar, Mary Magdalene, Mary the mother of James and Joses, and the mother of "
  "Zebedee's children."),
 ("The Earthquake, and the Centurion", "The Burial, and the Guard (vv.57-66)",
  "Joseph of Arimathaea is described as a rich man and a disciple, and the burial uses his own new "
  "tomb hewn out in the rock. The two Marys sit over against the sepulchre, which Matthew notes so "
  "that the next chapter has witnesses to the place. Then the episode only Matthew has: the priests "
  "go to Pilate the following day, quote the prediction back at him, we remember that that deceiver "
  "said, After three days I will rise again, and ask for a guard. Their stated fear is a stolen body "
  "and a worse rumour, so the last error shall be worse than the first. The stone is sealed and the "
  "watch set, which is what makes the accusation in chapter 28 necessary."),
],
"matthew28": [
 ("", "The Angel, and the Empty Tomb (vv.1-10)",
  "Matthew alone has the earthquake and the angel descending and rolling back the stone and sitting "
  "on it, and alone reports the effect on the guard, they did shake, and became as dead men. The "
  "message to the women is four clauses, fear not, he is not here, he is risen, come see the place, "
  "and then an errand, go quickly, and tell his disciples. They leave with fear and great joy "
  "together, and are met on the road. The instruction he gives repeats the angel's and adds one word "
  "the angel did not use, go tell my brethren."),
 ("The Guard's Report", "Some Doubted (vv.16-17)",
  "Two verses that Matthew declines to tidy. The eleven go into Galilee, to a mountain where Jesus "
  "had appointed them, and when they saw him they worshipped him. And then the clause that follows "
  "it in the same sentence, but some doubted. Matthew puts the doubt inside the worship rather than "
  "before it, and offers no explanation and no resolution. The commission in the next verse is given "
  "to that group."),
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
