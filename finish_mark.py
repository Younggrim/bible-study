#!/usr/bin/env python3
"""
Finishes Mark. Thirteen pages, 252 verses.

mark15 is the worst page found in the project. Forty-seven verses, and it carried two
sections, both single verses: 'Simon of Cyrene (v.21)' and 'The Centurion's Confession
(v.39)'. The trial before Pilate, Barabbas, the crown of thorns, the crucifying
itself, the superscription, the mocking, the darkness, the cry from the cross, the
veil torn, the women watching, and the burial were all undescribed. The crucifixion
chapter had been reduced to two verses somebody liked.

mark12 lost vv.1-27 and vv.35-40, which is the vineyard parable, render to Caesar, and
the Sadducees on resurrection. mark8 lost vv.1-21 and vv.31-33, so the feeding of the
four thousand, the refusal to give a sign, the leaven of the Pharisees, and Peter
being rebuked immediately after confessing the Christ were all missing. mark9 lost
vv.30-50 entirely.

mark10 also carried the last of the cut labels, 'Mark 10:', restored to Historical
Context.

One structural repair: mark7 ran 'Tradition vs. Scripture (vv.1-23)' with a nested
'The Heart as the Source of Sin (vv.20-23)' inside it, describing four verses twice.
The first becomes vv.1-19.

Usage:
    python3 finish_mark.py [--check]
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
"mark2": [
 ("insert", "Levi/Matthew's Calling", "The Question About Fasting (vv.18-22)",
  "Why do the disciples of John and of the Pharisees fast, but thy disciples fast not? The "
  "answer is a wedding, can the children of the bridechamber fast, while the bridegroom is with "
  "them? with a clause that darkens it, the days will come, when the bridegroom shall be taken "
  "away from them. Then two images about the wrong kind of repair: no man seweth a piece of new "
  "cloth on an old garment, and new wine is not put into old bottles. Both are about damage "
  "done by forcing a new thing into an old container, which is what the question assumed he "
  "should do."),
 ("insert", "The Question About Fasting", "Lord of the Sabbath (vv.23-28)",
  "The disciples pluck ears of corn walking through a field and are accused of harvesting. Jesus "
  "answers from a precedent nobody expects, David eating the shewbread when he had need, which "
  "was unlawful and is recorded without censure. Then the two sentences the passage is "
  "remembered for, and the order matters: the sabbath was made for man, and not man for the "
  "sabbath, which is a general principle, and then therefore the Son of man is Lord also of the "
  "sabbath, which is a claim about himself."),
],
"mark3": [
 ("insert", "", "The Withered Hand (vv.1-5)",
  "They watched him, whether he would heal on the sabbath day, that they might accuse him. The "
  "healing is a trap before it is a miracle. He calls the man out into the middle and puts a "
  "question nobody answers, is it lawful to do good on the sabbath days, or to do evil? to save "
  "life, or to kill? and their silence is recorded. Then the one place in the Gospels where "
  "Jesus is described as angry, and Mark gives both feelings at once: he looked round about on "
  "them with anger, being grieved for the hardness of their hearts."),
 ("insert", "The Pharisees and Herodians", "The Multitude by the Sea (vv.7-12)",
  "The pressure of the crowds is described in practical terms, a great multitude from Galilee, "
  "Judaea, Jerusalem, Idumaea, beyond Jordan, Tyre and Sidon, and he asked for a small ship "
  "because they were pressing on him. Mark says why, as many as had plagues pressed upon him "
  "for to touch him. Then the detail Mark keeps returning to: the unclean spirits know who he "
  "is and say so, thou art the Son of God, and he straitly charged them that they should not "
  "make him known."),
 ("insert", "The Twelve Appointed", "He Is Beside Himself (vv.20-27)",
  "Two verdicts arrive in the same paragraph and they are the two the whole book is arguing "
  "against. His friends said, he is beside himself, and came out to lay hold on him. The scribes "
  "said, he hath Beelzebub, and by the prince of the devils casteth he out devils. The answer to "
  "the second is logic, how can Satan cast out Satan? if a house be divided against itself, that "
  "house cannot stand. Then an image that explains the exorcisms as burglary, no man can enter "
  "into a strong man's house, and spoil his goods, except he will first bind the strong man."),
 ("insert", "The Unforgivable Sin", "Who Is My Mother (vv.31-35)",
  "His mother and his brethren come and stand outside and send for him, which closes the frame "
  "opened at verse 21 where the family set out to fetch him home. He answers with a question, "
  "who is my mother, or my brethren? and then looks round on the people sitting in the house and "
  "answers it himself: whosoever shall do the will of God, the same is my brother, and my "
  "sister, and mother. The people inside are named as family while the family stands outside."),
],
"mark4": [
 ("insert", "The Parable of the Sower",
  "Nothing Hid That Shall Not Be Manifested (vv.21-25)",
  "A candle is not lit to be put under a bed, and the principle drawn from it is about eventual "
  "exposure rather than about behaviour, for there is nothing hid, which shall not be "
  "manifested. Then a warning about attention, take heed what ye hear, and a measure that cuts "
  "both ways, with what measure ye mete, it shall be measured to you, and unto you that hear "
  "shall more be given. The chapter's parables are about hearing, and this is the passage that "
  "says so."),
 ("insert", "The Growing Seed", "The Grain of Mustard Seed (vv.30-34)",
  "The kingdom is likened to the smallest seed a farmer sows, and the point is the disproportion "
  "between the start and the finish, it groweth up, and becometh greater than all herbs, so that "
  "the fowls of the air may lodge under the shadow of it. Then Mark's own note on method: with "
  "many such parables spake he the word unto them, and without a parable spake he not unto them, "
  "and when they were alone, he expounded all things to his disciples."),
],
"mark5": [
 ("insert", "The Gadarene Demoniac", "Jairus Falls at His Feet (vv.21-24)",
  "One of the rulers of the synagogue, Jairus by name, falls at his feet and begs, my little "
  "daughter lieth at the point of death, I pray thee, come and lay thy hands on her, that she "
  "may live. A synagogue official kneeling in public is the measure of how bad it is. Jesus goes "
  "with him, and Mark records the obstacle in the same breath, much people followed him, and "
  "thronged him, which is what makes the interruption in the next verse possible."),
],
"mark6": [
 ("insert", "Rejection at Nazareth", "The Twelve Sent Out Two by Two (vv.7-13)",
  "He sends them in pairs with authority over unclean spirits and a packing list that is mostly "
  "prohibitions: no scrip, no bread, no money in their purse, a staff and sandals only, and not "
  "two coats. The instruction about rejection is a gesture rather than an argument, shake off "
  "the dust under your feet for a testimony against them. What they did is summarised in one "
  "verse, and it includes something the Gospels rarely mention, they anointed with oil many that "
  "were sick, and healed them."),
 ("insert", "Walking on Water", "Gennesaret and the Border of His Garment (vv.53-56)",
  "The boat lands at Gennesaret and Mark describes something closer to a crush than a ministry. "
  "They knew him, ran through that whole region round about, and began to carry about in beds "
  "those that were sick, where they heard he was. In the streets and villages and cities they "
  "laid the sick and besought him that they might touch but the border of his garment, and as "
  "many as touched him were made whole. The same detail as the woman in chapter 5, now happening "
  "at scale."),
],
"mark7": [
 ("retitle", "Tradition vs. Scripture", "(vv.1-19)"),
 ("insert", "The Syrophoenician Woman", "Ephphatha (vv.31-37)",
  "A deaf man with an impediment in his speech, and the healing is unusually physical and "
  "private. He took him aside from the multitude, put his fingers into his ears, spit, touched "
  "his tongue, looked up, sighed, and said one word which Mark preserves in Aramaic and then "
  "translates, Ephphatha, that is, Be opened. The sigh is left unexplained. Then the same charge "
  "as everywhere in this Gospel and the same result, he charged them that they should tell no "
  "man, but the more he charged them, so much the more a great deal they published it. The "
  "crowd's verdict closes the chapter, he hath done all things well."),
],
"mark8": [
 ("insert", "", "The Feeding of the Four Thousand (vv.1-10)",
  "A second feeding, and Mark records it without embarrassment at the repetition. The crowd has "
  "been with him three days and has nothing to eat, and the concern given is practical, if I "
  "send them away fasting to their own houses, they will faint by the way. The disciples' "
  "question is the same one they asked before, whence should we have so much bread here in the "
  "wilderness? Seven loaves, a few small fishes, four thousand fed, seven baskets left. The "
  "numbers differ from the first feeding, which is what makes the argument in verses 19 to 21 "
  "possible."),
 ("insert", "The Feeding of the Four Thousand", "No Sign Shall Be Given (vv.11-13)",
  "The Pharisees come seeking a sign from heaven, tempting him, and Mark records the response as "
  "an emotion before it is an answer, he sighed deeply in his spirit. Then the refusal, and it "
  "is absolute, why doth this generation seek after a sign? verily I say unto you, There shall "
  "no sign be given unto this generation. He leaves, gets back in the ship, and departs to the "
  "other side."),
 ("insert", "No Sign Shall Be Given", "The Leaven of the Pharisees (vv.14-21)",
  "The disciples have forgotten to bring bread, and when he warns them about the leaven of the "
  "Pharisees and of Herod they take it as a comment on the shortage. What follows is the "
  "sharpest exchange he has with them in the book, a run of questions with no answer recorded: "
  "perceive ye not yet, neither understand? have ye your heart yet hardened? having eyes, see ye "
  "not? Then the arithmetic, five loaves among five thousand, how many baskets? and seven among "
  "four thousand, how many? They give the right numbers. How is it that ye do not understand?"),
 ("insert", "Peter's Confession", "He Rebuked Peter (vv.31-33)",
  "The first prediction of the passion is stated plainly and Mark says so, he spake that saying "
  "openly, which is a change from everything before it. Peter takes him aside and rebukes him, "
  "using the same verb the Gospel uses for Jesus rebuking demons. The reply is delivered facing "
  "the wrong way on purpose, when he had turned about and looked on his disciples, he rebuked "
  "Peter, so the correction is public though the objection was private. Get thee behind me, "
  "Satan, for thou savourest not the things that be of God, but the things that be of men. Eight "
  "verses after being told who Jesus is, Peter is told whose side he is arguing for."),
],
"mark9": [
 ("extend", "The Transfiguration", "(vv.1-8)",
  "The chapter opens with the saying the Transfiguration answers, there be some of them that "
  "stand here, which shall not taste of death, till they have seen the kingdom of God come with "
  "power, and the next verse begins after six days, which is why the two are read together."),
 ("insert", "The Transfiguration", "Elias Must First Come (vv.9-13)",
  "Coming down the mountain he charges them to tell no man until the Son of man were risen, and "
  "Mark records what they did with that, they questioned one with another what the rising from "
  "the dead should mean. They had no category for it. Their question is about Elijah, and the "
  "answer identifies him with someone already dead: Elias is indeed come, and they have done "
  "unto him whatsoever they listed, as it is written of him."),
 ("insert", "The Demon-Possessed Boy", "The Greatest Is Servant of All (vv.30-37)",
  "The second passion prediction is given privately, and the disciples' response is recorded "
  "twice over: they understood not that saying, and were afraid to ask him. Then, on the road, "
  "an argument about which of them should be the greatest, which they will not admit to when he "
  "asks. The answer is a sentence and then an object lesson. If any man desire to be first, the "
  "same shall be last of all, and servant of all. He sets a child in the midst of them and takes "
  "it in his arms, and the child is the argument."),
 ("insert", "The Greatest Is Servant of All", "He That Is Not Against Us (vv.38-41)",
  "John reports that they forbade a man casting out devils in Jesus' name because he followeth "
  "not us, and expects approval. Forbid him not, for there is no man which shall do a miracle in "
  "my name, that can lightly speak evil of me. Then the principle stated as generously as it "
  "can be put, for he that is not against us is on our part, and a promise attached to the "
  "smallest possible kindness, whosoever shall give you a cup of water to drink in my name shall "
  "not lose his reward."),
 ("insert", "He That Is Not Against Us", "Offend Not One of These Little Ones (vv.42-50)",
  "The warning about causing a little one to stumble is the most violent language in the Gospel, "
  "and it is aimed at the offender rather than the child: it is better for him that a millstone "
  "were hanged about his neck, and he were cast into the sea. Then hand, foot and eye in turn, "
  "with the same conclusion each time, it is better to enter maimed than whole into hell. The "
  "chapter ends on salt, and the two clauses are not obviously connected, if the salt have lost "
  "his saltness, wherewith will ye season it? and then the instruction, have salt in yourselves, "
  "and have peace one with another, which answers the argument on the road."),
],
"mark10": [
 ("merge_into", "Mark 10:", "Historical Context"),
 ("insert", "", "What Did Moses Command You (vv.1-12)",
  "The Pharisees ask whether it is lawful for a man to put away his wife, tempting him. He "
  "answers with a question about their own authority, what did Moses command you? and when they "
  "cite the writing of divorcement he treats it as concession rather than permission, for the "
  "hardness of your heart he wrote you this precept. Then the argument goes behind Moses to "
  "Genesis, from the beginning of the creation God made them male and female, and they twain "
  "shall be one flesh. What therefore God hath joined together, let not man put asunder. The "
  "stricter application is given privately in the house, and Mark's version is the one that "
  "addresses a woman divorcing her husband as well."),
 ("insert", "What Did Moses Command You", "Suffer the Little Children (vv.13-16)",
  "The disciples rebuke the people bringing children to him, and Mark records the reaction, when "
  "Jesus saw it, he was much displeased. The instruction is short, suffer the little children to "
  "come unto me, and forbid them not, and the reason turns the children into the lesson, of such "
  "is the kingdom of God. Then the demand made of everyone else, whosoever shall not receive the "
  "kingdom of God as a little child, he shall not enter therein, and the gesture Mark adds, he "
  "took them up in his arms, put his hands upon them, and blessed them."),
 ("insert", "The Rich Young Ruler", "A Camel Through a Needle's Eye (vv.23-31)",
  "The saying is repeated because of the reaction to it. How hardly shall they that have riches "
  "enter into the kingdom of God, and when the disciples are astonished he says it again with "
  "the camel and the needle. Their question is the right one, who then can be saved? and the "
  "answer removes the question from the realm of effort altogether, with men it is impossible, "
  "but not with God. Peter's claim that they have left all is not disputed, and the promise made "
  "in reply includes something nobody quotes, houses and brethren and lands, with persecutions."),
 ("insert", "A Camel Through a Needle's Eye", "The Third Prediction (vv.32-34)",
  "They were in the way going up to Jerusalem, and Jesus went before them, and they were amazed, "
  "and as they followed, they were afraid. Mark puts the fear on the record before the prediction "
  "rather than after it. The third telling is the most detailed of the three: delivered to the "
  "chief priests, condemned to death, delivered to the Gentiles, mocked, scourged, spat upon, "
  "killed, and the third day he shall rise again."),
 ("insert", "The Third Prediction", "James and John Ask for Glory (vv.35-45)",
  "Immediately after that, two of them ask to sit on his right and left hand in his glory. The "
  "reply asks whether they can drink the cup he drinks, they say they can, and he grants it in "
  "terms they have not understood. The other ten are displeased, and the correction is aimed at "
  "all of them: ye know that they which are accounted to rule over the Gentiles exercise "
  "lordship, but so shall it not be among you. Whosoever will be chiefest, shall be servant of "
  "all. Then the verse the whole Gospel has been building toward, and it is the only place Mark "
  "explains the death: the Son of man came not to be ministered unto, but to minister, and to "
  "give his life a ransom for many."),
],
"mark11": [
 ("insert", "The Fig Tree and Temple", "Dried Up from the Roots (vv.20-21)",
  "In the morning they pass the tree again and Peter notices, Master, behold, the fig tree which "
  "thou cursedst is withered away. Mark alone splits the cursing and the withering across two "
  "days with the temple cleansing between them, which is how the tree becomes a comment on the "
  "temple rather than an outburst about breakfast."),
 ("insert", "Faith and Prayer", "By What Authority (vv.27-33)",
  "The question is jurisdictional, by what authority doest thou these things? and who gave thee "
  "this authority? The counter-question is about John: was his baptism from heaven, or of men? "
  "Mark then records their reasoning out loud, which is the most revealing thing in the passage. "
  "If they say from heaven, he will ask why they did not believe him. If they say of men, they "
  "fear the people. So they answer we cannot tell, and he declines to answer them either. Both "
  "sides know the exchange was not about information."),
],
"mark12": [
 ("insert", "", "The Vineyard and the Husbandmen (vv.1-12)",
  "A parable told against the men standing in front of him, and they know it, for they perceived "
  "that he had spoken the parable against them. The vineyard is Isaiah 5, so the audience knows "
  "who the owner is before the story starts. Servants are sent and beaten and killed in "
  "sequence, and then having yet therefore one son, his wellbeloved, he sent him also last unto "
  "them. Their reasoning is quoted, this is the heir, come, let us kill him, and the inheritance "
  "shall be ours. The stone the builders rejected is quoted at the end, and the only reason they "
  "do not arrest him is the crowd."),
 ("insert", "The Vineyard and the Husbandmen", "Render to Caesar (vv.13-17)",
  "The Pharisees and Herodians come with flattery first, we know that thou art true, and carest "
  "for no man, which Mark identifies as the trap it is. The question about tribute has no safe "
  "answer, which is the point. He asks for a coin and asks whose image is on it, so the answer "
  "is drawn from them rather than given to them. Render to Caesar the things that are Caesar's, "
  "and to God the things that are God's. Mark's note on the effect is one word, they marvelled "
  "at him."),
 ("insert", "Render to Caesar", "The Sadducees and the Resurrection (vv.18-27)",
  "The Sadducees, which say there is no resurrection, bring a hypothetical with seven brothers "
  "in it, and the answer names two errors rather than one. Do ye not therefore err, because ye "
  "know not the scriptures, neither the power of God? The first is corrected by describing what "
  "resurrection is not, they neither marry, nor are given in marriage, but are as the angels. "
  "The second is corrected from a verse the Sadducees accepted, the God of Abraham, and of "
  "Isaac, and of Jacob, with the tense doing the work: he is not the God of the dead, but the "
  "God of the living."),
 ("insert", "The Greatest Commandment", "David's Son and David's Lord (vv.35-37)",
  "Jesus asks the question this time, and it is about a psalm. How say the scribes that Christ "
  "is the son of David? For David himself said, The LORD said to my Lord, Sit thou on my right "
  "hand. David therefore calleth him Lord, and whence is he then his son? No answer is given "
  "and none is expected. Mark adds that the common people heard him gladly, which is the "
  "opposite of the reaction from the men who had been questioning him."),
 ("insert", "David's Son and David's Lord", "Beware of the Scribes (vv.38-40)",
  "Three verses of description and every detail is public behaviour: they love to go in long "
  "clothing, and love salutations in the marketplaces, and the chief seats in the synagogues, "
  "and the uppermost rooms at feasts. Then the charge that is not about vanity at all, which "
  "devour widows' houses, and for a pretence make long prayers. The sentence is placed "
  "immediately before the widow putting her last two coins into the treasury, and the placing "
  "is the argument."),
],
"mark15": [
 ("insert", "", "Before Pilate (vv.1-5)",
  "The council delivers him to Pilate in the morning, and the charge has changed on the way. "
  "Before the priests it was blasphemy, before Pilate it is kingship, art thou the King of the "
  "Jews? The answer is two words, thou sayest it, and after that nothing. Mark makes the silence "
  "the story: they accused him of many things, but he answered nothing, so that Pilate "
  "marvelled. A governor surprised by a defendant who will not defend himself."),
 ("insert", "Before Pilate", "Barabbas Released (vv.6-15)",
  "The custom of releasing a prisoner at the feast gives Pilate a way out and he tries to use "
  "it, for he knew that the chief priests had delivered him for envy. Mark says so plainly, "
  "which makes what follows a failure of nerve rather than of judgement. The priests move the "
  "crowd, the crowd asks for Barabbas, and Pilate's two questions are both answered with "
  "shouting: what will ye then that I shall do unto him whom ye call the King of the Jews? and "
  "why, what evil hath he done? The verdict is given as a motive, and so Pilate, willing to "
  "content the people, released Barabbas."),
 ("insert", "Barabbas Released", "The Crown of Thorns (vv.16-20)",
  "The whole band is called together in the common hall for something that is not part of the "
  "sentence. Purple, a crown of platted thorns, a mock salute, Hail, King of the Jews, and then "
  "they smote him on the head with a reed, and did spit upon him, and bowing their knees "
  "worshipped him. Mark records the kneeling as worship, which is the irony the scene turns on. "
  "Then the purple comes off, his own clothes go back on, and they lead him out."),
 ("insert", "Simon of Cyrene", "The Crucifying and the Superscription (vv.22-28)",
  "Golgotha, which is, being interpreted, The place of a skull. The wine mingled with myrrh is "
  "offered and refused. Then the crucifixion itself, and Mark gives it four words, and they "
  "crucified him, before turning to the soldiers dividing his garments and casting lots. The "
  "hour is given, the third hour, and the charge nailed above him is quoted, THE KING OF THE "
  "JEWS. Two thieves are crucified with him, one on his right and the other on his left, which "
  "is the answer to the request James and John made in chapter 10."),
 ("insert", "The Crucifying and the Superscription", "They That Passed By Railed (vv.29-32)",
  "Three groups mock him and all three use the same argument. The passers-by throw his own words "
  "back, thou that destroyest the temple, and buildest it in three days, save thyself. The chief "
  "priests make it a taunt about consistency, he saved others, himself he cannot save. The men "
  "crucified with him revile him too. The demand common to all of them is a demonstration, let "
  "Christ the King of Israel descend now from the cross, that we may see and believe, and it is "
  "the one thing he does not do."),
 ("insert", "They That Passed By Railed", "Darkness and the Cry from the Cross (vv.33-38)",
  "Darkness over the whole land from the sixth hour to the ninth. Then the only words from the "
  "cross Mark records, and he keeps them in Aramaic before translating, Eloi, Eloi, lama "
  "sabachthani, that is to say, My God, my God, why hast thou forsaken me? It is the first line "
  "of Psalm 22. Some hear Elias, somebody offers vinegar, and he cries with a loud voice and "
  "gives up the ghost. And the veil of the temple was rent in twain from the top to the bottom, "
  "which is Mark's way of saying who tore it."),
 ("insert", "The Centurion's Confession", "The Women Beholding Afar Off (vv.40-41)",
  "There were also women looking on afar off, and they are named: Mary Magdalene, Mary the "
  "mother of James the less and of Joses, and Salome. Mark adds what they had been doing, who "
  "also, when he was in Galilee, followed him, and ministered unto him, and notes there were "
  "many other women. The disciples fled in chapter 14. The people still present at the end are "
  "listed by name, and they are the ones who will find the tomb open."),
 ("insert", "The Women Beholding Afar Off", "Joseph of Arimathaea (vv.42-47)",
  "An honourable counsellor, which also waited for the kingdom of God, came and went in boldly "
  "unto Pilate, and craved the body of Jesus. Mark says boldly, because a member of the council "
  "that condemned him asking for the body is a public act. Pilate is surprised he is dead "
  "already and checks with the centurion, which is the detail that closes off any suggestion "
  "otherwise. The burial is done quickly because the sabbath is coming: linen, a sepulchre hewn "
  "out of a rock, a stone rolled to the door. And the last verse names the witnesses to the "
  "location, Mary Magdalene and Mary the mother of Joses beheld where he was laid."),
],
"mark16": [
 ("insert", "", "The Stone Rolled Away (vv.1-8)",
  "The women buy spices when the sabbath is past and set out at sunrise, and the problem they "
  "discuss on the way is practical, who shall roll us away the stone from the door of the "
  "sepulchre? It is already done. Inside, a young man in a long white garment tells them he is "
  "not there, behold the place where they laid him, and gives them an errand that names one "
  "disciple specifically, go your way, tell his disciples and Peter. Then the sentence on which "
  "the earliest manuscripts of this Gospel end: they went out quickly, and fled from the "
  "sepulchre, for they trembled and were amazed, neither said they any thing to any man, for "
  "they were afraid."),
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
