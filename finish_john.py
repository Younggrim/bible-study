#!/usr/bin/env python3
"""
Finishes John. Nine pages, and the sparsest input in the project: several of these
carried a single verse-range section for a whole chapter.

What survived on these pages is instructive. john11 had 'Caiaphas' Prophecy
(vv.49-52)' and nothing for the raising of Lazarus. john13 had 'The New Commandment
(v.34)' and nothing for the foot washing or the betrayal. john18 had 'Pilate's
Question (v.38)' and nothing for the arrest, the denials or the trial. john20 had
'Purpose Statement (vv.30-31)' and nothing for the resurrection. In each case the
verse that had been given a section is a famous single line, and the narrative it
sits inside was left undescribed.

The inherited topical notes without verse ranges are kept as they are: 'Bethany:',
'Four Days Dead:', 'Foot Washing:', 'Judas:', 'The Vine and Branches:',
'The Garden of Gethsemane:', 'The Trials:', 'The Empty Tomb:', 'Thomas:',
'Blindness from Birth:', 'The Triumphal Entry:'. They carry real background and
dropping them to make room would be a downgrade. The verse-range sections are added
alongside.

Two sections are widened rather than added, because a one-verse neighbour would have
split a sentence: john9's excommunication note takes in v.23, where the parents
deflect to their son, and john13's new commandment takes in v.35, which is its
consequence.

Usage:
    python3 finish_john.py [--check]
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
"john8": [
 ("insert", "The Woman Caught in Adultery", "I Am the Light of the World (vv.12-20)",
  "The second of the seven I am sayings, and the setting sharpens it: this is spoken during "
  "the feast of tabernacles, in the treasury, near where the great lamps were lit. I am the "
  "light of the world, he that followeth me shall not walk in darkness. The Pharisees object "
  "on a point of law, thou bearest record of thyself, thy record is not true, and the answer "
  "accepts the rule and satisfies it, I am not alone, but I and the Father that sent me. The "
  "chapter notes that no man laid hands on him, for his hour was not yet come."),
 ("insert", "I Am the Light of the World", "Ye Shall Die in Your Sins (vv.21-30)",
  "Whither I go, ye cannot come. They take it as a threat of suicide, will he kill himself? "
  "and the reply moves the argument onto origin, ye are from beneath, I am from above. Then "
  "the sentence that has been read as a divine title since the earliest commentators, if ye "
  "believe not that I am he, ye shall die in your sins, where the Greek is simply I am. He "
  "adds the terms on which the claim can be tested, when ye have lifted up the Son of man, "
  "then shall ye know that I am he."),
 ("insert", "Ye Shall Die in Your Sins", "The Truth Shall Make You Free (vv.31-38)",
  "Addressed to those which believed on him, which makes what follows harder rather than "
  "easier. If ye continue in my word, then are ye my disciples indeed, and ye shall know the "
  "truth, and the truth shall make you free. The reply is a denial that there is anything to "
  "be freed from, we be Abraham's seed, and were never in bondage to any man, said by people "
  "under Roman occupation. The answer redefines the bondage, whosoever committeth sin is the "
  "servant of sin, and contrasts a servant who does not abide in the house with a son who "
  "does."),
 ("insert", "The Truth Shall Make You Free", "Your Father the Devil (vv.39-47)",
  "The exchange turns on paternity and gets steadily worse. They claim Abraham; he answers "
  "that Abraham's children would do Abraham's works, and ye seek to kill me. They claim God; "
  "he answers that if God were their Father they would love him. Then the hardest thing "
  "Jesus says to anyone in the Gospels, ye are of your father the devil, with two charges "
  "attached, he was a murderer from the beginning and he is a liar. The closing question is "
  "put as a diagnosis rather than an insult, which of you convinceth me of sin? and why do ye "
  "not believe me?"),
 ("insert", "Your Father the Devil", "Before Abraham Was, I Am (vv.48-59)",
  "They call him a Samaritan and demon-possessed. He answers about honour rather than "
  "reputation, I honour my Father, and ye do dishonour me. The claim escalates: if a man keep "
  "my saying, he shall never see death. Art thou greater than our father Abraham? Then the "
  "answer that ends the argument and the chapter, your father Abraham rejoiced to see my day, "
  "and, when they object that he is not fifty years old, before Abraham was, I am. The tense "
  "is the point, and so is their response: then took they up stones to cast at him. They "
  "understood exactly what had been said."),
],
"john9": [
 ("insert", "", "Neither This Man Nor His Parents (vv.1-5)",
  "The disciples see a blind man and ask a question about blame, who did sin, this man, or his "
  "parents? Both options assume the affliction is payment for something. The answer refuses "
  "the frame, neither hath this man sinned, nor his parents, but that the works of God should "
  "be made manifest in him. Then the working note attached to it, I must work the works of "
  "him that sent me, while it is day, the night cometh, when no man can work, and the saying "
  "that governs the chapter, as long as I am in the world, I am the light of the world."),
 ("insert", "Neither This Man Nor His Parents", "Clay, Spittle, and Siloam (vv.6-12)",
  "He spat on the ground, made clay of the spittle, anointed the man's eyes, and sent him to "
  "wash. Nothing about the method is necessary and all of it is deliberate: making clay is "
  "work, which is the charge that follows, and the pool of Siloam is a walk across the city "
  "for a blind man carrying mud on his face. John stops to translate the name, which is by "
  "interpretation, Sent. The man obeys, washes, and came seeing. When the neighbours ask how, "
  "his answer is a plain report with a gap in it, a man that is called Jesus, and the last "
  "thing he says is I know not where he is. He has not yet seen the man who healed him."),
 ("insert", "Clay, Spittle, and Siloam", "The First Interrogation (vv.13-17)",
  "The Pharisees begin with the day rather than the man, and the division is recorded "
  "honestly: some say this man is not of God, because he keepeth not the sabbath day, and "
  "others say how can a man that is a sinner do such miracles? There was a division among "
  "them. Then they turn back to the one person present who has evidence, what sayest thou of "
  "him, that he hath opened thine eyes? and he gives the first of his three escalating "
  "answers: he is a prophet."),
 ("insert", "The First Interrogation", "The Parents Questioned (vv.18-21)",
  "They do not believe the man was born blind, so they send for his parents, which is an "
  "attempt to unmake the fact rather than to explain it. The parents confirm the two things "
  "they can, this is our son, and he was born blind, and refuse the third, by what means he "
  "now seeth, we know not. He is of age, ask him. It is a careful answer from frightened "
  "people, and the next verse says why."),
 ("extend", "Excommunication", "(vv.22-23)",
  "The deflection in the following verse repeats the same phrase word for word, he is of age, "
  "ask him, which John records twice to make plain that it was rehearsed."),
 ("insert", "Excommunication", "One Thing I Know (vv.24-34)",
  "The second interrogation opens with an instruction rather than a question, give God the "
  "praise, we know that this man is a sinner. The answer is the most quoted line in the "
  "chapter and it concedes nothing, whether he be a sinner or no, I know not, one thing I "
  "know, that, whereas I was blind, now I see. When they make him repeat the account he asks "
  "why, will ye also be his disciples? and the argument that follows is his own, unanswered: "
  "since the world began was it not heard that any man opened the eyes of one that was born "
  "blind. If this man were not of God, he could do nothing. They cast him out."),
 ("insert", "One Thing I Know", "Dost Thou Believe on the Son of God (vv.35-38)",
  "Jesus finds him, which is the detail the chapter has been withholding since verse 12 when "
  "the man did not know where he was. The question is put directly, dost thou believe on the "
  "Son of God? and the answer is a request rather than an assent, who is he, Lord, that I "
  "might believe on him? Then the disclosure, thou hast both seen him, and it is he that "
  "talketh with thee. The man who could not see at the start of the chapter is told to look "
  "at who is speaking, and he worshipped him."),
 ("insert", "Dost Thou Believe on the Son of God", "For Judgment I Am Come (vv.39-41)",
  "For judgment I am come into this world, that they which see not might see, and that they "
  "which see might be made blind. The chapter closes by turning its own subject into a "
  "measure. The Pharisees ask, are we blind also? and the answer holds the paradox steady: if "
  "ye were blind, ye should have no sin, but now ye say, We see, therefore your sin "
  "remaineth. Admitted blindness is curable. Claimed sight is not."),
],
"john11": [
 ("insert", "", "He Whom Thou Lovest Is Sick (vv.1-16)",
  "The message sent is deliberately short of a request, he whom thou lovest is sick, and what "
  "follows is the hardest sentence in the chapter: when he had heard therefore that he was "
  "sick, he abode two days still in the same place where he was. The therefore is the "
  "difficulty. John states the love first and the delay second and offers no apology for the "
  "order. The disciples argue against going back to Judaea at all, and Jesus speaks of Lazarus "
  "sleeping until they misunderstand it, then says plainly, Lazarus is dead, and adds, I am "
  "glad for your sakes that I was not there, to the intent ye may believe. Thomas gets the "
  "last word and it is loyal and bleak, let us also go, that we may die with him."),
 ("insert", "He Whom Thou Lovest Is Sick", "I Am the Resurrection and the Life (vv.17-27)",
  "Martha meets him on the road with a sentence that is grief and faith in the same breath, "
  "Lord, if thou hadst been here, my brother had not died, but I know that even now, "
  "whatsoever thou wilt ask of God, God will give it thee. He answers with a promise she can "
  "put at a distance, thy brother shall rise again, and she does, at the last day. So the "
  "claim is moved from the calendar to a person: I am the resurrection, and the life. Her "
  "confession in reply is as full as Peter's, I believe that thou art the Christ, the Son of "
  "God, and it is made before anything has happened."),
 ("insert", "I Am the Resurrection and the Life", "Jesus Wept (vv.28-37)",
  "Mary says the same sentence her sister said, word for word, and she says it at his feet, "
  "weeping. He groaned in the spirit, and was troubled, and asked where the grave was. Then "
  "the shortest verse in the Bible, Jesus wept, over a death he has already said he intends to "
  "undo. The crowd reads it two ways in consecutive verses, behold how he loved him, and "
  "could not this man have caused that even this man should not have died? Both readings are "
  "left standing."),
 ("insert", "Jesus Wept", "Lazarus, Come Forth (vv.38-44)",
  "Take ye away the stone. Martha objects on practical grounds, by this time he stinketh, for "
  "he hath been dead four days, and John has already told us four days for a reason, since it "
  "put the death past any argument about swooning. The prayer offered is not a petition but a "
  "thanksgiving, Father, I thank thee that thou hast heard me, and it is said out loud for "
  "the crowd's sake. Then three words, Lazarus, come forth, and a man walks out still tied. "
  "The last instruction is domestic and is given to the bystanders, loose him, and let him go."),
 ("insert", "Lazarus, Come Forth", "The Council Convenes (vv.45-48)",
  "The miracle produces belief in many and a meeting in the rest. The council's reasoning is "
  "recorded without comment and it is entirely political: what do we? for this man doeth many "
  "miracles. If we let him thus alone, all men will believe on him, and the Romans shall come "
  "and take away both our place and our nation. Nobody in the room disputes that the miracles "
  "happened. The problem is the consequences of their being believed."),
 ("insert", "Caiaphas' Prophecy", "Withdrawal to Ephraim and the Passover Watch (vv.53-57)",
  "From that day forth they took counsel together for to put him to death, so Jesus walked no "
  "more openly among the Jews but went to a city called Ephraim. Then the setting shifts to "
  "the feast, and John gives an unusually vivid picture of a crowd waiting: many went up "
  "before the passover to purify themselves, and they sought for Jesus, and spake among "
  "themselves, what think ye, that he will not come to the feast? The chapter ends with a "
  "standing order that any man who knows where he is must report it."),
],
"john12": [
 ("insert", "", "Mary Anoints His Feet (vv.1-11)",
  "Six days before the passover, at supper in Bethany with the raised man at the table. Mary "
  "takes a pound of ointment of spikenard, very costly, anoints his feet and wipes them with "
  "her hair, and John notes that the house was filled with the odour. Judas objects on behalf "
  "of the poor and John supplies the motive, not that he cared for the poor, but because he "
  "was a thief, and had the bag. The defence given is a burial, against the day of my burying "
  "hath she kept this. Then a detail easy to miss: the chief priests consulted that they might "
  "put Lazarus also to death, because the evidence was walking about."),
 ("insert", "Mary Anoints His Feet", "The Entry into Jerusalem (vv.12-19)",
  "The crowd takes palm branches and shouts Hosanna, blessed is the King of Israel, and Jesus "
  "arrives on a young ass. John admits the disciples did not follow it at the time, these "
  "things understood not his disciples at the first, but when Jesus was glorified, then "
  "remembered they. The reason the crowd is there is given as Lazarus, and the Pharisees "
  "concede defeat in a sentence they do not mean as prophecy, perceive ye how ye prevail "
  "nothing? behold, the world is gone after him."),
 ("insert", "The Greeks Seeking Jesus", "The Hour Is Come (v.23)",
  "The request from the Greeks is never answered on its own terms. Instead: the hour is come, "
  "that the Son of man should be glorified. Throughout this Gospel the hour has been the thing "
  "not yet come, and Gentiles asking to see him is what marks its arrival."),
 ("insert", "The Grain of Wheat", "He That Hateth His Life Shall Keep It (vv.25-26)",
  "The image of the dying seed is turned immediately into a demand. He that loveth his life "
  "shall lose it, and he that hateth his life in this world shall keep it unto life eternal. "
  "Then the terms of following are made simple and hard, where I am, there shall also my "
  "servant be, and the reward named is the Father's honour rather than anything the servant "
  "arranges."),
 ("insert", "He That Hateth His Life Shall Keep It", "Now Is My Soul Troubled (vv.27-36)",
  "This is John's Gethsemane, and it is three verses long. Now is my soul troubled, and what "
  "shall I say? Father, save me from this hour, and then the correction in the same breath, "
  "but for this cause came I unto this hour. The voice from heaven answers and the crowd "
  "splits over what it heard, some said that it thundered, others that an angel spake. Then "
  "the sentences the chapter is remembered for, now is the judgment of this world, and I, if I "
  "be lifted up from the earth, will draw all men unto me, with John's own note that this he "
  "said, signifying what death he should die."),
 ("insert", "Now Is My Soul Troubled", "Isaiah Saw His Glory (vv.37-43)",
  "John stops the narrative to account for the unbelief, and he does it with two quotations "
  "from Isaiah rather than an argument. Lord, who hath believed our report? and the hardening "
  "text, he hath blinded their eyes, that they should not see. Then the claim that Isaiah "
  "spoke these things when he saw his glory, which reads the throne vision of Isaiah 6 as a "
  "vision of Christ. The section closes on a quieter failure, among the chief rulers also many "
  "believed on him, but because of the Pharisees they did not confess him, for they loved the "
  "praise of men more than the praise of God."),
 ("insert", "Isaiah Saw His Glory", "He That Rejecteth Me (vv.44-50)",
  "The last public words in the Gospel, and they are a summary rather than a new argument. He "
  "that believeth on me, believeth not on me, but on him that sent me, and he that seeth me "
  "seeth him that sent me. Then a distinction the chapter needs, I came not to judge the world "
  "but to save the world, followed by what happens anyway, the word that I have spoken, the "
  "same shall judge him in the last day. The authority is located outside himself twice over, "
  "I have not spoken of myself, but the Father which sent me, he gave me a commandment, what I "
  "should say."),
],
"john13": [
 ("insert", "", "Having Loved His Own (vv.1-5)",
  "John frames the whole evening in one sentence before anything happens: having loved his own "
  "which were in the world, he loved them unto the end. Then the actions, and the order is "
  "deliberate. Jesus knowing that the Father had given all things into his hands, and that he "
  "was come from God, and went to God, he riseth from supper, and laid aside his garments, and "
  "took a towel. The washing is introduced by a statement of maximum authority, not of "
  "humility, which is the point being made."),
 ("insert", "Having Loved His Own", "Peter Objects to the Washing (vv.6-11)",
  "Lord, dost thou wash my feet? The refusal is absolute, thou shalt never wash my feet, and "
  "the answer is equally absolute, if I wash thee not, thou hast no part with me. Peter "
  "reverses to the opposite extreme, not my feet only, but also my hands and my head, and is "
  "corrected again, he that is washed needeth not save to wash his feet. Then the sentence "
  "that darkens the room, ye are clean, but not all, with John's note, for he knew who should "
  "betray him."),
 ("insert", "Peter Objects to the Washing", "Know Ye What I Have Done (vv.12-17)",
  "He puts his garments back on, sits down, and asks whether they understood it. The teaching "
  "is drawn out explicitly, ye call me Master and Lord, and ye say well, for so I am. If I "
  "then, your Lord and Master, have washed your feet, ye also ought to wash one another's "
  "feet. The instruction is followed by a warning about the gap between knowing and doing, if "
  "ye know these things, happy are ye if ye do them."),
 ("insert", "Know Ye What I Have Done", "One of You Shall Betray Me (vv.18-30)",
  "He was troubled in spirit, and testified, one of you shall betray me. What follows is the "
  "most closely observed scene in the Gospel: the disciples looking at one another, Peter "
  "signalling to the one leaning on Jesus' breast, the quiet question, Lord, who is it? and "
  "the answer given by an action rather than a name, he it is, to whom I shall give a sop. "
  "The sop is handed to Judas, which is a gesture of honour to the guest at a meal. Then that "
  "thou doest, do quickly, and nobody at the table understands what has just been arranged. "
  "John ends the paragraph with four words of setting that do the work of a paragraph: and it "
  "was night."),
 ("insert", "One of You Shall Betray Me", "Now Is the Son of Man Glorified (vv.31-33)",
  "The moment Judas is gone the language changes to glory, and it is in the present tense, now "
  "is the Son of man glorified, and God is glorified in him. The betrayal is treated as the "
  "beginning of the glorification rather than an interruption of it. Then the address that "
  "makes the farewell what it is, little children, yet a little while I am with you, and "
  "whither I go, ye cannot come."),
 ("extend", "The New Commandment", "(vv.34-35)",
  "The commandment is given a public test in the following verse, by this shall all men know "
  "that ye are my disciples, if ye have love one to another. Not by doctrine and not by "
  "conduct in general, by that."),
 ("insert", "The New Commandment", "Thou Shalt Deny Me Thrice (vv.36-38)",
  "Peter goes straight past the commandment to the departure, Lord, whither goest thou? and "
  "then makes the offer, I will lay down my life for thy sake. The reply is a question with "
  "the answer already in it, wilt thou lay down thy life for my sake? and then the "
  "prediction, the cock shall not crow, till thou hast denied me thrice. The chapter that "
  "began with love unto the end closes on a promise of loyalty that will not hold for one "
  "night."),
],
"john15": [
 ("insert", "", "I Am the True Vine (vv.1-8)",
  "The last of the I am sayings, and the only one that assigns the hearers a place inside the "
  "image: I am the vine, ye are the branches. Two kinds of pruning are described with the "
  "same hand doing both, every branch that beareth not fruit he taketh away, and every branch "
  "that beareth fruit, he purgeth it, that it may bring forth more fruit. The verb that "
  "carries the passage is abide, used eight times, and the argument is stated as a plain "
  "impossibility in both directions, the branch cannot bear fruit of itself, and without me ye "
  "can do nothing."),
 ("insert", "I Am the True Vine", "Continue Ye in My Love (vv.9-11)",
  "The chain is set out in order, as the Father hath loved me, so have I loved you, continue "
  "ye in my love. Then the mechanism, if ye keep my commandments, ye shall abide in my love, "
  "with his own obedience offered as the pattern rather than as a contrast. And the stated "
  "purpose, which is easy to read past in a passage about pruning, that my joy might remain in "
  "you, and that your joy might be full."),
 ("insert", "Continue Ye in My Love", "Ye Are My Friends (vv.12-17)",
  "Greater love hath no man than this, that a man lay down his life for his friends. Then the "
  "reclassification, henceforth I call you not servants, for the servant knoweth not what his "
  "lord doeth, but I have called you friends, and the reason given is disclosure, for all "
  "things that I have heard of my Father I have made known unto you. The initiative is put "
  "beyond doubt, ye have not chosen me, but I have chosen you, and the section closes by "
  "repeating the one command the chapter has, that ye love one another."),
],
"john16": [
 ("insert", "", "That Ye Should Not Be Offended (vv.1-7)",
  "These things have I spoken unto you, that ye should not be offended. The warning is "
  "specific and it names the worst part, they shall put you out of the synagogues, yea, the "
  "time cometh, that whosoever killeth you will think that he doeth God service. He admits "
  "these things were not said at the beginning because I was with you, so the teaching is "
  "arriving now because he is leaving. Then the sentence that would sound like consolation "
  "from anyone else and does not here, it is expedient for you that I go away, for if I go not "
  "away, the Comforter will not come unto you."),
 ("insert", "The Spirit's Threefold Work", "He Will Guide You Into All Truth (vv.12-15)",
  "I have yet many things to say unto you, but ye cannot bear them now. An admission that the "
  "teaching is incomplete and that the limit is theirs. What fills the gap is the Spirit of "
  "truth, and the way he works is described the same way Jesus described his own: he shall not "
  "speak of himself, but whatsoever he shall hear, that shall he speak. He shall glorify me, "
  "for he shall receive of mine, and shall shew it unto you."),
 ("insert", "He Will Guide You Into All Truth", "Sorrow Turned Into Joy (vv.16-24)",
  "A little while, and ye shall not see me, and again, a little while, and ye shall see me. "
  "The disciples cannot make sense of it and say so among themselves, we cannot tell what he "
  "saith. The explanation is an image rather than a timetable: a woman in travail hath "
  "sorrow, because her hour is come, but as soon as she is delivered she remembereth no more "
  "the anguish. The sorrow is not cancelled, it is forgotten in what it produced. Then a new "
  "arrangement for prayer, whatsoever ye shall ask the Father in my name, he will give it you, "
  "and the reason, that your joy may be full."),
 ("insert", "Sorrow Turned Into Joy", "I Have Overcome the World (vv.25-33)",
  "The hour cometh when I shall no more speak unto you in proverbs, but I shall shew you "
  "plainly of the Father. The disciples declare themselves satisfied, now are we sure that "
  "thou knowest all things, by this we believe that thou camest forth from God, and the reply "
  "is not a rebuke but a forecast, behold, the hour cometh, that ye shall be scattered, and "
  "shall leave me alone. Then the last sentence of the discourse, and it holds both halves "
  "without softening either: in the world ye shall have tribulation, but be of good cheer, I "
  "have overcome the world."),
],
"john18": [
 ("insert", "", "The Garden and the Arrest (vv.1-11)",
  "John's account of the arrest has no kiss and no agony, and it gives Jesus the initiative "
  "throughout. He asks whom seek ye, answers I am he, and the party falls backward to the "
  "ground. He asks a second time and then negotiates for the others, if therefore ye seek me, "
  "let these go their way, which John reads as fulfilling his own earlier words about losing "
  "none. Peter draws a sword and takes off the right ear of a servant, and John is the only "
  "one to name him, Malchus. The rebuke is put as a question about the cup, the cup which my "
  "Father hath given me, shall I not drink it?"),
 ("insert", "The Garden and the Arrest", "Annas, and the First Denial (vv.12-18)",
  "They take him first to Annas, who is not the serving high priest but is Caiaphas' "
  "father-in-law, which tells you where the power sat. John interleaves the two examinations "
  "deliberately: the door of the palace is opened to Peter by another disciple known to the "
  "high priest, so the access that lets him in is what puts him where the question is asked. "
  "Art not thou also one of this man's disciples? He saith, I am not. The chapter notes the "
  "fire of coals, because it was cold, and that Peter stood with them and warmed himself."),
 ("insert", "Annas, and the First Denial", "Struck Before the High Priest (vv.19-24)",
  "The examination has no witnesses and no charge, only a question about doctrine, and the "
  "answer refuses the format: I spake openly to the world, ask them which heard me. For that "
  "one of the officers struck him with the palm of his hand, and the reply is a point of law "
  "rather than a protest, if I have spoken evil, bear witness of the evil, but if well, why "
  "smitest thou me? Then he is sent bound to Caiaphas, which means the first hearing produced "
  "nothing."),
 ("insert", "Struck Before the High Priest", "The Second and Third Denials (vv.25-27)",
  "The narrative returns to the fire and finishes what it started. Two more questions, and the "
  "second comes from a kinsman of the man whose ear Peter cut off, did not I see thee in the "
  "garden with him? Peter denies it again, and immediately the cock crew. John gives no "
  "weeping and no look from Jesus, only the sound and a full stop."),
 ("insert", "The Second and Third Denials", "Before Pilate (vv.28-32)",
  "They brought him into the hall of judgment and it was early, and then the detail John "
  "keeps: they went not in themselves, lest they should be defiled, but that they might eat "
  "the passover. Men arranging an execution taking care over ritual purity, and the whole "
  "trial conducted with Pilate walking in and out between two parties. Pilate tries to hand "
  "it back, judge him according to your law, and the answer states the real object, it is not "
  "lawful for us to put any man to death. John adds that this fulfilled what Jesus had said "
  "about the manner of his death, which is to say crucifixion rather than stoning."),
 ("insert", "Before Pilate", "My Kingdom Is Not of This World (vv.33-37)",
  "Art thou the King of the Jews? The reply asks where the question came from, sayest thou "
  "this thing of thyself, or did others tell it thee of me? Then the definition that keeps "
  "Pilate from being able to convict, my kingdom is not of this world, with the evidence "
  "offered being the absence of a fight, if my kingdom were of this world, then would my "
  "servants fight. The claim is finally accepted on its own terms, thou sayest that I am a "
  "king, and redefined as testimony, to this end was I born, that I should bear witness unto "
  "the truth."),
 ("insert", "Pilate's Question", "Not This Man, But Barabbas (vv.39-40)",
  "Pilate reaches for a custom instead of a verdict, ye have a custom, that I should release "
  "unto you one at the passover, will ye therefore that I release unto you the King of the "
  "Jews? The answer is shouted, not this man, but Barabbas, and John adds five words that "
  "close the chapter, now Barabbas was a robber."),
],
"john20": [
 ("insert", "", "The Stone Taken Away (vv.1-10)",
  "Mary Magdalene comes early, when it was yet dark, sees the stone taken away and runs with "
  "the wrong conclusion, they have taken away the Lord, and we know not where they have laid "
  "him. Then the footrace, and John records that he outran Peter and stopped at the entrance, "
  "and that Peter went in first. What convinces them is not an absence but an arrangement: the "
  "linen clothes lying, and the napkin that was about his head not lying with them, but "
  "wrapped together in a place by itself. Grave robbers do not fold. Then he saw, and "
  "believed, with the honest admission attached, for as yet they knew not the scripture."),
 ("insert", "The Stone Taken Away", "Mary at the Tomb (vv.11-18)",
  "Mary stays after the men have gone home, and the recognition scene is built on one word. "
  "She talks to angels without registering them, gives the gardener the same explanation she "
  "gave the disciples, and asks to be told where the body is so that she can carry it away "
  "herself. Jesus saith unto her, Mary. She turned herself and saith, Rabboni. The first "
  "instruction after the resurrection is a restriction, touch me not, for I am not yet "
  "ascended, and the second is an errand, go to my brethren, with a message that puts them in "
  "the same relation he has, my Father, and your Father, and my God, and your God."),
 ("insert", "Mary at the Tomb", "Peace Be Unto You (vv.19-23)",
  "The same day at evening, when the doors were shut for fear of the Jews. The greeting is "
  "given twice, peace be unto you, and between them he shews them his hands and his side, so "
  "the peace is attached to the wounds rather than offered instead of them. Then the "
  "commission, as my Father hath sent me, even so send I you, and an action John alone "
  "records, he breathed on them, and saith unto them, Receive ye the Holy Ghost. The verb is "
  "the one used of God breathing into Adam."),
 ("insert", "Peace Be Unto You", "Except I Shall See (vv.24-29)",
  "Thomas was not there and says exactly what he requires, except I shall see in his hands the "
  "print of the nails, and thrust my hand into his side, I will not believe. Eight days later "
  "the offer is made in his own words, reach hither thy finger, and behold my hands, which "
  "means the demand was heard when it was made. There is no record of him touching anything. "
  "His answer is the highest confession in the Gospel and the last thing anyone says to Jesus "
  "in it, my Lord and my God. Then the beatitude that reaches past the room, blessed are they "
  "that have not seen, and yet have believed."),
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
