#!/usr/bin/env python3
"""
Luke, first pass: the ten flagged pages in chapters 2 to 14.

Luke's pages are the sparsest set left in the project, and the reason is visible in
what survived. luke9 carried one section, 'The Cost of Discipleship (vv.57-62)', for
sixty-two verses, so the sending of the twelve, the feeding of the five thousand,
Peter's confession, the Transfiguration and the second passion prediction were all
undescribed while six verses at the very end of the chapter had a heading. luke8 had
'The Women Who Followed (vv.1-3)' and nothing else, so the sower, the storm, Legion
and Jairus' daughter were missing from a fifty-six verse chapter.

luke7 lost vv.1-35, which is the centurion's servant, the widow of Nain, and John's
question from prison. luke2 lost vv.1-24, so the census, the manger and the shepherds
had no section on the page that describes the nativity.

The inherited topical notes without verse ranges are kept: 'Caesar Augustus:',
'The Shepherds:', 'The Temptation:', 'The Centurion's Faith:', 'The Widow of Nain:',
'The Parable of the Sower:', 'The Gadarene Demoniac:', 'The Rejection at Nazareth:'.
They carry background the sections do not repeat.

Usage:
    python3 finish_luke_first.py [--check]
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
"luke2": [
 ("", "The Decree of Caesar Augustus (vv.1-7)",
  "Luke dates the birth by an administrative act, a decree from Caesar Augustus that all the "
  "world should be taxed, and names the official responsible for the province. The whole point "
  "of the paragraph is ordinariness: a couple travelling because a government required it, "
  "arriving in a full town, and a first child born where the animals were kept. She brought "
  "forth her firstborn son, and wrapped him in swaddling clothes, and laid him in a manger, "
  "because there was no room for them in the inn. Luke gives no angels and no star here. He "
  "gives a census and a feeding trough."),
 ("The Decree of Caesar Augustus", "The Shepherds and the Angels (vv.8-20)",
  "The announcement goes to men working a night shift, and the first thing said to them is fear "
  "not, because they were sore afraid. The message names the town and gives them a sign they can "
  "check, ye shall find the babe wrapped in swaddling clothes, lying in a manger. Then the "
  "multitude of the heavenly host, and the song, glory to God in the highest, and on earth peace, "
  "good will toward men. What the shepherds do with it is practical, let us now go even unto "
  "Bethlehem, and see this thing which is come to pass, and afterwards they told everyone. Luke "
  "keeps Mary's reaction separate and quieter, she kept all these things, and pondered them in "
  "her heart."),
 ("The Shepherds and the Angels", "Circumcision and Presentation (vv.21-24)",
  "Four verses of law being kept. He is circumcised on the eighth day and named as the angel "
  "instructed. Then the family goes up to Jerusalem for the purification, and Luke cites the "
  "statute twice, and the offering they bring is the one Leviticus allows for people who cannot "
  "afford a lamb, a pair of turtledoves, or two young pigeons. Luke does not comment on it. The "
  "detail tells the reader what kind of household this is."),
 ("Simeon and Anna", "Return to Nazareth (vv.39-40)",
  "Two verses closing the infancy narrative, and they are deliberately uneventful. When they had "
  "performed all things according to the law of the Lord, they returned into Galilee, to their "
  "own city Nazareth. Then a summary of about a decade in one sentence, the child grew, and waxed "
  "strong in spirit, filled with wisdom, and the grace of God was upon him. Luke is the only "
  "Gospel that says anything at all about the years between, and this is most of it."),
],
"luke3": [
 ("", "The Word Came to John (vv.1-9)",
  "Luke dates the ministry with the precision of a historian and names seven office-holders to do "
  "it, from Tiberius Caesar down to Annas and Caiaphas, and then says the word of God came to "
  "none of them. It came unto John the son of Zacharias in the wilderness. Isaiah is quoted at "
  "greater length here than in the other Gospels, and Luke keeps the clause the others drop, all "
  "flesh shall see the salvation of God. The preaching itself is unsparing: O generation of "
  "vipers, and the demand is for evidence rather than sentiment, bring forth therefore fruits "
  "worthy of repentance, with the ancestry defence refused in advance, begin not to say within "
  "yourselves, We have Abraham to our father."),
 ("John's Practical Ethics", "The Baptism, and Herod's Prison (vv.15-22)",
  "The people are in expectation and wondering whether John is the Christ, which he denies in "
  "terms of relative standing, one mightier than I cometh, the latchet of whose shoes I am not "
  "worthy to unloose. Then Luke does something the other Gospels do not: he finishes John's story "
  "before the baptism, noting the rebuke of Herod over Herodias and that Herod shut up John in "
  "prison. Only after that does he record the baptism, and he puts it in a subordinate clause, "
  "when all the people were baptized, it came to pass, that Jesus also being baptized, and "
  "praying, the heaven was opened. The praying is Luke's addition. The voice says, Thou art my "
  "beloved Son, in thee I am well pleased."),
],
"luke4": [
 ("", "Forty Days in the Wilderness (vv.1-13)",
  "He is led by the Spirit into the wilderness, so the testing is not an interruption of the "
  "calling but part of it. Three temptations, and Luke's order puts the temple last. Bread from a "
  "stone, answered from Deuteronomy, man shall not live by bread alone. Then all the kingdoms of "
  "the world offered on one condition, and the devil's claim to own them is not disputed. Then "
  "the pinnacle of the temple, where scripture is quoted at him for the first time, and answered "
  "with scripture, thou shalt not tempt the Lord thy God. Luke's closing line leaves the matter "
  "open rather than settled, he departed from him for a season."),
 ("Forty Days in the Wilderness", "In the Power of the Spirit (vv.14-15)",
  "Two verses of summary that set up the sermon at Nazareth: Jesus returned in the power of the "
  "Spirit into Galilee, and there went out a fame of him through all the region round about. He "
  "taught in their synagogues, being glorified of all. The reputation arrives before he does, "
  "which is why the hometown congregation has expectations to disappoint."),
 ("The Rejection at Nazareth", "Capernaum, and the Unclean Spirit (vv.31-37)",
  "After being run out of Nazareth he goes down to Capernaum, and the reaction there is the "
  "opposite, they were astonished at his doctrine, for his word was with power. Then the unclean "
  "spirit, which shouts a correct answer, I know thee who thou art, the Holy One of God, and is "
  "silenced. Luke, who is interested in medical detail, notes that the demon threw him down in "
  "the midst and hurt him not. The crowd's question is about method rather than identity, what a "
  "word is this! for with authority and power he commandeth the unclean spirits, and they come "
  "out."),
 ("Capernaum, and the Unclean Spirit", "Simon's Wife's Mother, and the Many (vv.38-44)",
  "The healings move indoors and then outdoors. Simon's wife's mother is taken with a great "
  "fever, which Luke describes as rebuked rather than treated, and she rose and ministered unto "
  "them. Then at sunset the whole town brings its sick, and he laid his hands on every one of "
  "them, which is a detail about pace rather than power. The devils are silenced again because "
  "they knew that he was Christ. In the morning he leaves, and when the crowds try to keep him he "
  "gives the reason he cannot stay, I must preach the kingdom of God to other cities also, for "
  "therefore am I sent."),
],
"luke7": [
 ("", "The Centurion's Servant (vv.1-10)",
  "The centurion never appears in person. He sends Jewish elders, who commend him on grounds that "
  "are unusual in the Gospels, he loveth our nation, and he hath built us a synagogue, and then "
  "sends friends with a second message stopping Jesus before he arrives. The reasoning in it is "
  "military and is the only place anyone in the Gospels argues from chain of command: I also am a "
  "man set under authority, having under me soldiers, and I say to one, Go, and he goeth. Say in "
  "a word, and my servant shall be healed. The response is the strongest compliment Jesus pays "
  "anyone, I have not found so great faith, no, not in Israel."),
 ("The Centurion's Servant", "The Widow of Nain (vv.11-17)",
  "The only raising in Luke that nobody asks for. He meets the funeral coming out of the town gate "
  "and Luke gives the two facts that make it unbearable, the only son of his mother, and she was a "
  "widow. With no son she has no support at all. The response is recorded before the miracle, and "
  "when the Lord saw her, he had compassion on her, and said unto her, Weep not. Then he touches "
  "the bier, which makes him unclean, and says, Young man, I say unto thee, Arise. The last clause "
  "is the point of the story rather than the resurrection, and he delivered him to his mother. The "
  "crowd's verdict is that a great prophet is risen up among us, and it is this report that "
  "reaches John in prison in the next paragraph."),
 ("The Widow of Nain", "Art Thou He That Should Come (vv.18-28)",
  "John sends two disciples from prison with a question that concedes doubt, art thou he that "
  "should come? or look we for another? The answer is not reassurance but a list of things to "
  "report, the blind see, the lame walk, the lepers are cleansed, the poor have the gospel "
  "preached to them, which is Isaiah with one item conspicuously left out, the opening of the "
  "prison. Then a beatitude aimed at the man who asked, blessed is he, whosoever shall not be "
  "offended in me. Once the messengers leave, Jesus praises John without qualification, among "
  "those that are born of women there is not a greater prophet, and then relativises it in the "
  "next clause, he that is least in the kingdom of God is greater than he."),
 ("Art Thou He That Should Come", "Children in the Marketplace (vv.29-35)",
  "Luke notes who accepted John and who did not, and the division is by class: the people and the "
  "publicans justified God, being baptized, but the Pharisees and lawyers rejected the counsel of "
  "God against themselves. Then the image, and it is of children who will not join either game, "
  "we have piped unto you, and ye have not danced, we have mourned to you, and ye have not wept. "
  "The application is that both messengers were refused on opposite grounds, John for fasting and "
  "the Son of man for eating and drinking, which shows the objection was never about the "
  "behaviour. But wisdom is justified of all her children."),
],
"luke8": [
 ("The Women Who Followed", "The Parable of the Sower (vv.4-15)",
  "The parable is told to a great crowd and explained only to the disciples, and Luke keeps the "
  "hard saying about why, unto others in parables, that seeing they might not see. The four soils "
  "are interpreted one by one, and Luke's version of each is about what happens to the word "
  "rather than to the ground: taken away by the devil, received with joy and no root, choked with "
  "cares and riches and pleasures of this life. The good ground is described with two words the "
  "others do not use, an honest and good heart, and one that is Luke's own emphasis, bring forth "
  "fruit with patience."),
 ("The Parable of the Sower", "Nothing Hid That Shall Not Be Known (vv.16-21)",
  "A candle covered with a vessel or put under a bed is a picture of concealment that cannot last, "
  "for nothing is secret, that shall not be made manifest. Then a warning about hearing, take "
  "heed therefore how ye hear, and the measure that follows it. The paragraph ends with the "
  "family arriving and being unable to reach him for the crowd, and the answer given, my mother "
  "and my brethren are these which hear the word of God, and do it. Luke places it here so that "
  "hearing and doing is the thread joining all three parts."),
 ("Nothing Hid That Shall Not Be Known", "Peace, Be Still (vv.22-25)",
  "He is asleep in the boat when the storm comes, and Luke says the boat was filling, they were "
  "in jeopardy. The disciples' cry is Master, master, we perish, and he rebukes the wind and the "
  "raging of the water. Then the question that is harder than the storm, where is your faith? and "
  "the reaction, which Luke records as fear rather than relief, they being afraid wondered, "
  "saying one to another, What manner of man is this! for he commandeth even the winds and water, "
  "and they obey him."),
 ("Peace, Be Still", "Legion, and the Swine (vv.26-39)",
  "The man is described before the exorcism in detail Luke does not spare: no clothes, no house, "
  "living in the tombs, kept bound with chains and fetters and breaking them. The name given is "
  "Legion, because many devils were entered into him. What they ask for is not to be sent into "
  "the deep, and what they get is the herd. Then the scene afterwards, and it is the reason the "
  "story is told: the townspeople find the man sitting at the feet of Jesus, clothed, and in his "
  "right mind, and they were afraid, and asked him to leave. The healed man asks to come with him "
  "and is refused, and given an errand instead, return to thine own house, and shew how great "
  "things God hath done unto thee."),
 ("Legion, and the Swine", "The Woman and the Ruler's Daughter (vv.40-56)",
  "Two stories interleaved, and Luke the physician keeps the medical details. The woman had spent "
  "all her living upon physicians, neither could be healed of any, and the touch is of the border "
  "of his garment. The exchange that follows is about disclosure rather than power, somebody hath "
  "touched me, for I perceive that virtue is gone out of me, and she comes trembling and tells "
  "all the people why. The delay is what kills the girl, and the message arrives mid-conversation, "
  "thy daughter is dead, trouble not the Master. The reply is fear not, believe only. Then the "
  "room cleared, two words, Maid, arise, and the flattest possible follow-up instruction, he "
  "commanded to give her meat."),
],
"luke9": [
 ("", "The Twelve Sent Out (vv.1-9)",
  "The twelve are given power and authority and sent to preach and heal, with a packing list of "
  "prohibitions, neither staves, nor scrip, neither bread, neither money, neither have two coats "
  "apiece. Luke then cuts to Herod, who hears of it and is perplexed, and lists the rumours going "
  "round: that John was risen from the dead, that Elias had appeared, that one of the old prophets "
  "was risen again. Herod's own line is left hanging, John have I beheaded, but who is this of "
  "whom I hear such things? and he desired to see him. It is the question the chapter will answer "
  "twice over, and Herod never gets an answer to it."),
 ("The Twelve Sent Out", "Five Thousand Fed (vv.10-17)",
  "The apostles return and report, and he takes them away privately, and the crowd follows. Luke "
  "notes that he received them, which is a small phrase carrying the loss of the rest. The "
  "disciples' suggestion is practical, send them away, that they may go into the towns and lodge, "
  "and the answer puts the problem back on them, give ye them to eat. Five loaves and two fishes, "
  "and the organisation is specified, make them sit down by fifties in a company. Twelve baskets "
  "of fragments remain, which is one for each of the men who said it could not be done."),
 ("Five Thousand Fed", "Whom Say Ye That I Am (vv.18-27)",
  "The question comes while he is praying alone, which is Luke's habit of noting. First the "
  "rumours again, whom say the people that I am? and the same list Herod heard. Then the question "
  "to them, and Peter's answer, the Christ of God. Immediately he charges them to tell no man and "
  "gives the reason, the Son of man must suffer many things, and be rejected of the elders and "
  "chief priests and scribes, and be slain, and be raised the third day. Then the terms for "
  "anyone following, and Luke adds one word to them that the other Gospels do not, let him take "
  "up his cross daily."),
 ("Whom Say Ye That I Am", "The Transfiguration (vv.28-36)",
  "About an eight days after, and again he goes up to pray. Luke alone reports what Moses and "
  "Elias were talking about, they spake of his decease which he should accomplish at Jerusalem, "
  "and alone notes that the disciples were heavy with sleep. Peter's suggestion about three "
  "tabernacles is dismissed in the text itself, not knowing what he said. The cloud comes and "
  "they are afraid as they enter it, and the voice says, This is my beloved Son, hear him. Then "
  "the anticlimax Luke keeps: they found Jesus alone, and they told no man in those days any of "
  "those things which they had seen."),
 ("The Transfiguration", "The Only Child, and the Second Prediction (vv.37-45)",
  "The next day a man in the crowd cries out about his only child, which is a phrase Luke uses "
  "three times in this Gospel and never carelessly. The disciples could not cast it out, and the "
  "response is exasperated, O faithless and perverse generation, how long shall I be with you? "
  "The healing is one sentence. Then, while everyone is still marvelling, the second prediction "
  "is delivered privately, and Luke's note on the reception is the frankest in any Gospel: they "
  "understood not this saying, and it was hid from them that they perceived it not, and they "
  "feared to ask him of that saying."),
 ("The Only Child, and the Second Prediction",
  "Who Is Greatest, and the Samaritan Village (vv.46-56)",
  "There arose a reasoning among them, which of them should be greatest, and the answer is a "
  "child set beside him and a sentence about receiving. Then John's complaint about a man casting "
  "out devils outside the group, answered with forbid him not, for he that is not against us is "
  "for us. Then the Samaritan village that will not receive him, and James and John asking "
  "whether they should call down fire. The rebuke is aimed at them rather than at the village, "
  "and Luke's closing line is that they went to another village. Three consecutive attempts by "
  "the disciples to make the movement smaller, and all three refused."),
],
"luke11": [
 ("The Persistent Friend", "Ask, and It Shall Be Given (vv.9-13)",
  "Three imperatives with three promises, ask and it shall be given you, seek and ye shall find, "
  "knock and it shall be opened. Then the argument from ordinary fatherhood, and Luke's version "
  "of the examples is bread and a stone, a fish and a serpent, an egg and a scorpion. The "
  "conclusion concedes the premise about human character in passing, if ye then, being evil, know "
  "how to give good gifts unto your children, how much more shall your heavenly Father give. And "
  "Luke's ending differs from Matthew's in what is promised: not good things, but the Holy Spirit."),
 ("The Beelzebub Controversy", "The Sign of Jonas (vv.27-36)",
  "A woman in the crowd calls out a blessing on his mother, blessed is the womb that bare thee, "
  "and the reply redirects it rather than refusing it, yea rather, blessed are they that hear the "
  "word of God, and keep it. Then the demand for a sign is answered with two: Jonas to the "
  "Ninevites, and the queen of the south who came from the uttermost parts of the earth to hear "
  "Solomon. Both examples are Gentiles who responded to less evidence. The section ends on the "
  "single eye and the candle, take heed therefore that the light which is in thee be not "
  "darkness, which is about the capacity to see rather than the availability of light."),
 ("The Sign of Jonas", "Woe Unto You, Pharisees (vv.37-54)",
  "A dinner invitation turns into the harshest passage in the Gospel. The complaint is that he "
  "did not wash first, and the answer moves from cups to people, ye make clean the outside, but "
  "your inward part is full of ravening. Then three woes on the Pharisees and three on the "
  "lawyers. Tithing mint and rue while passing over judgment and the love of God. Loving the "
  "uppermost seats. Being as graves which appear not, so that men walk over them unaware. Laying "
  "burdens on others and not touching them. Building the tombs of the prophets their fathers "
  "killed. And the last, which is the one that closes the passage, ye have taken away the key of "
  "knowledge, ye entered not in yourselves, and them that were entering in ye hindered. Luke "
  "records what it produced, they began to urge him vehemently, laying wait for him."),
],
"luke12": [
 ("", "Beware the Leaven of the Pharisees (vv.1-3)",
  "The crowd is so thick they trod upon one another, and the first thing he says is addressed to "
  "the disciples over their heads: beware ye of the leaven of the Pharisees, which is hypocrisy. "
  "Luke defines the word for the reader, which none of the Gospels usually does. Then the reason "
  "it cannot last, there is nothing covered, that shall not be revealed, and a warning about "
  "private speech, that which ye have spoken in the ear in closets shall be proclaimed upon the "
  "housetops."),
 ("Fear Not", "Confess Me Before Men (vv.8-12)",
  "Whosoever shall confess me before men, him shall the Son of man also confess before the angels "
  "of God. The symmetry is exact and so is its reverse. Then the saying about blasphemy against "
  "the Holy Ghost, placed here without explanation, and immediately after it a practical "
  "reassurance for people facing tribunals: take ye no thought how or what ye shall answer, for "
  "the Holy Ghost shall teach you in the same hour what ye ought to say. The same Spirit named in "
  "the warning is named in the promise."),
 ("Confess Me Before Men", "Who Made Me a Judge (vv.13-15)",
  "A man interrupts with an inheritance dispute, Master, speak to my brother, that he divide the "
  "inheritance with me, and the refusal is flat, who made me a judge or a divider over you? Then "
  "the warning that turns a family quarrel into the chapter's theme, take heed, and beware of "
  "covetousness, for a man's life consisteth not in the abundance of the things which he "
  "possesseth. The parable of the rich fool follows from this refusal rather than from a general "
  "topic."),
 ("The Rich Fool", "Consider the Ravens and the Lilies (vv.22-31)",
  "Two examples chosen for what they do not do: the ravens neither sow nor reap nor have "
  "storehouse nor barn, the lilies toil not, they spin not. The argument each time is from lesser "
  "to greater, how much more are ye better than the fowls? The clause about worry is unanswerable "
  "and is meant to be, which of you with taking thought can add to his stature one cubit? Then "
  "the reframing, the nations of the world seek after these things, and your Father knoweth that "
  "ye have need of these things, and the instruction, rather seek ye the kingdom of God, and all "
  "these things shall be added unto you."),
 ("Consider the Ravens and the Lilies", "Let Your Loins Be Girded (vv.33-40)",
  "Sell that ye have, and give alms, which is Luke's version and is more concrete than Matthew's. "
  "Then the sentence the argument turns on, for where your treasure is, there will your heart be "
  "also, and the order of it matters: the treasure decides the heart, not the other way round. "
  "The rest is a picture of servants waiting up for a master returning from a wedding, with one "
  "detail nobody expects, he shall gird himself, and make them to sit down to meat, and will come "
  "forth and serve them. Then the thief in the night, and the instruction, be ye therefore ready "
  "also."),
 ("Let Your Loins Be Girded", "The Faithful and Unfaithful Steward (vv.41-48)",
  "Peter asks whether the parable is for them or for everybody, and gets an answer aimed squarely "
  "at people with responsibility. The faithful steward is found giving the household its portion "
  "of meat in due season. The unfaithful one says in his heart, My lord delayeth his coming, and "
  "begins to beat the servants. Then the calibration that makes the passage uncomfortable, and it "
  "is graded: he that knew his lord's will and did it not shall be beaten with many stripes, and "
  "he that knew not with few. Unto whomsoever much is given, of him shall be much required."),
 ("The Faithful and Unfaithful Steward", "Not Peace, But Division (vv.49-59)",
  "I am come to send fire on the earth, and what will I, if it be already kindled? Then a "
  "sentence about his own dread, I have a baptism to be baptized with, and how am I straitened "
  "till it be accomplished. The denial that follows is the hardest in Luke, suppose ye that I am "
  "come to give peace on earth? I tell you, Nay, but rather division, and the divisions listed are "
  "all within one house. The chapter ends on two images of ordinary competence: men who can read "
  "the weather but not the time they are living in, and a debtor who should settle out of court "
  "while he still can."),
],
"luke13": [
 ("The Barren Fig Tree", "The Woman Bowed Eighteen Years (vv.10-17)",
  "Luke describes the condition precisely, a spirit of infirmity eighteen years, and was bowed "
  "together, and could in no wise lift up herself. The healing is unasked for, he called her to "
  "him, which is unusual. Then the objection from the ruler of the synagogue, who does not address "
  "Jesus at all but tells the congregation there are six other days. The answer uses their own "
  "practice, doth not each one of you on the sabbath loose his ox or his ass from the stall, and "
  "lead him away to watering? and then the comparison that closes it, ought not this woman, being "
  "a daughter of Abraham, be loosed from this bond on the sabbath day? Luke records both "
  "reactions, his adversaries were ashamed, and all the people rejoiced."),
 ("The Woman Bowed Eighteen Years", "The Mustard Seed and the Leaven (vv.18-22)",
  "Two short parables about small beginnings, and both are domestic. A grain of mustard seed cast "
  "into a garden becomes a great tree with birds lodging in it. Leaven is hid in three measures of "
  "meal till the whole is leavened, and the verb is hid rather than mixed. Luke closes the section "
  "with a travel note that keeps the destination in view, and he went through the cities and "
  "villages, teaching, and journeying toward Jerusalem."),
 ("The Narrow Door", "Herod, and O Jerusalem (vv.31-35)",
  "Pharisees warn him that Herod means to kill him, and the reply is contemptuous and precise, go "
  "ye, and tell that fox, Behold, I cast out devils, and I do cures today and tomorrow, and the "
  "third day I shall be perfected. He adds a reason for continuing anyway that is grimly "
  "geographical, it cannot be that a prophet perish out of Jerusalem. Then the lament, and it is "
  "the only place in Luke he addresses the city directly, O Jerusalem, Jerusalem, which killest "
  "the prophets, how often would I have gathered thy children together, as a hen doth gather her "
  "brood under her wings, and ye would not."),
],
"luke14": [
 ("", "The Man with the Dropsy (vv.1-6)",
  "He is a guest at a Pharisee's house on the sabbath and they watched him, and a man with dropsy "
  "is present. Luke has him ask the question first this time, is it lawful to heal on the sabbath "
  "day? and they hold their peace. He heals the man, then puts the argument, which of you shall "
  "have an ass or an ox fallen into a pit, and will not straightway pull him out on the sabbath "
  "day? They could not answer him again to these things, which Luke notes with some satisfaction."),
 ("The Man with the Dropsy", "Sit Not Down in the Highest Room (vv.7-14)",
  "Two pieces of advice about seating, and both are about status. The first is given as prudence, "
  "sit not down in the highest room, lest a more honourable man be bidden, and then be told to "
  "give place, and the principle drawn from it is general, whosoever exalteth himself shall be "
  "abased. The second is addressed to the host and is harder: call not thy friends, nor thy "
  "brethren, nor thy rich neighbours, lest they also bid thee again, but call the poor, the "
  "maimed, the lame, the blind. The reason given is the absence of reciprocity, and thou shalt be "
  "blessed, for they cannot recompense thee."),
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
