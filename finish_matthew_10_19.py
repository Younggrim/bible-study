#!/usr/bin/env python3
"""
Matthew, second pass: chapters 10 to 19.

The inherited sections on these pages are single verses or interpretive notes rather
than passages, and the effect is odd once you list them. matthew16 had 'The Rock
(v.18)' and nothing else, so a chapter containing the demand for a sign, the leaven of
the Pharisees, Peter's confession, the first passion prediction and 'get thee behind
me, Satan' was represented by one verse of an argument about ecclesiology. matthew12
had 'The Unforgivable Sin (vv.31-32)' for fifty verses. matthew13 had 'Why Parables?
(vv.10-17)' for fifty-eight.

matthew15's 'Corban (vv.5-6)' is the same shape: a technical note on a word, kept
while the Syrophoenician woman, the feeding of the four thousand and the argument
about what defiles a man had nothing.

Where the odd sections exist they are worked around rather than displaced, so
matthew15's opening runs vv.1-4 and vv.7-9, matthew16's confession runs vv.13-17 and
vv.19-20, and matthew11's John section keeps vv.2-6 with the surrounding material
split either side.

Usage:
    python3 finish_matthew_10_19.py [--check]
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
"matthew10": [
 ("", "The Twelve Named and Sent (vv.1-15)",
  "The twelve are listed by name, in pairs, with two identified by what marks them out: Matthew "
  "the publican, which is the author labelling himself by the job, and Judas Iscariot, who also "
  "betrayed him. The commission is deliberately narrow at this stage, go not into the way of the "
  "Gentiles, but rather to the lost sheep of the house of Israel, which Matthew will reverse in his "
  "last chapter. The instructions are about dependence: freely ye have received, freely give, and no "
  "gold, no scrip, no second coat, no shoes, no staves, for the workman is worthy of his meat. "
  "Rejection is handled with a gesture rather than an argument, shake off the dust of your feet."),
 ("The Twelve Named and Sent", "As Sheep Among Wolves (vv.16-25)",
  "The tone changes from logistics to warning without transition, behold, I send you forth as sheep "
  "in the midst of wolves, with the instruction that follows sounding almost contradictory, be ye "
  "therefore wise as serpents, and harmless as doves. What is predicted is specific: councils, "
  "synagogues, scourging, governors and kings, and betrayal within families. The promise attached is "
  "not rescue but speech, it is not ye that speak, but the Spirit of your Father which speaketh in "
  "you. Then the argument from the master's own treatment, if they have called the master of the "
  "house Beelzebub, how much more them of his household."),
 ("As Sheep Among Wolves", "Fear Not Them Which Kill the Body (vv.26-33)",
  "Fear them not is said three times in this passage with three different reasons. The first is "
  "exposure, there is nothing covered, that shall not be revealed, so secrecy is temporary either "
  "way. The second draws the line where the danger actually lies, fear not them which kill the body, "
  "but are not able to kill the soul. The third is providence at its smallest scale, two sparrows "
  "sold for a farthing and not one of them falling to the ground without your Father, and the hairs "
  "of your head all numbered. Then the reciprocal confession, whosoever shall confess me before men, "
  "him will I confess also before my Father."),
 ("Fear Not Them Which Kill the Body", "Not Peace, But a Sword (vv.34-42)",
  "Think not that I am come to send peace on earth, and the divisions listed are all inside one "
  "house, a man at variance against his father, the daughter against her mother. The demand that "
  "follows is the most absolute in the Gospel, he that loveth father or mother more than me is not "
  "worthy of me, and he that taketh not his cross and followeth after me. Then the paradox, he that "
  "findeth his life shall lose it. The chapter ends unexpectedly gently, on hospitality: whoever "
  "receives a prophet, a righteous man, or gives a cup of cold water to a little one, shall not lose "
  "his reward. After the sword, a drink of water."),
],
"matthew11": [
 ("", "John Sends from Prison (v.1)",
  "One verse of transition that Matthew uses to close every discourse in the Gospel, and when Jesus "
  "had made an end of commanding his twelve disciples, he departed thence to teach and to preach in "
  "their cities. The formula appears five times and marks the five blocks of teaching the book is "
  "built from."),
 ("John's Doubt", "Among Those Born of Women (vv.7-19)",
  "Once the messengers leave, Jesus praises John to the crowd, and the praise is built on three "
  "questions about what they went out to see, a reed shaken with the wind, a man in soft clothing, "
  "a prophet. The verdict is unqualified, among them that are born of women there hath not risen a "
  "greater than John the Baptist, and then relativised in the next clause, notwithstanding he that "
  "is least in the kingdom of heaven is greater than he. Then the image of children in the "
  "marketplace who will play neither game, and the observation that John was rejected for fasting "
  "and the Son of man for eating, which shows the objection was never about the behaviour."),
 ("The Unrepentant Cities", "Come Unto Me, All Ye That Labour (vv.25-30)",
  "The chapter turns from judgment to invitation in one verse, and it opens with thanksgiving for "
  "something that sounds like a loss, thou hast hid these things from the wise and prudent, and hast "
  "revealed them unto babes. Then the claim that everything runs through him, all things are "
  "delivered unto me of my Father, and no man knoweth the Son, but the Father. And the invitation, "
  "which is the passage Matthew is most quoted for: come unto me, all ye that labour and are heavy "
  "laden, and I will give you rest. What is offered is not the removal of the yoke but a different "
  "one, take my yoke upon you, for my yoke is easy, and my burden is light."),
],
"matthew12": [
 ("", "Lord of the Sabbath (vv.1-14)",
  "Two sabbath disputes, and both are answered from precedent rather than principle. The disciples "
  "pluck corn and are accused, and the reply cites David eating the shewbread and the priests "
  "working in the temple, then makes two claims larger than the argument requires: in this place is "
  "one greater than the temple, and the Son of man is Lord even of the sabbath day. Hosea is quoted "
  "in between, I will have mercy, and not sacrifice. Then the man with the withered hand, and this "
  "time the question is put to them first, is it lawful to heal on the sabbath days? with the "
  "sheep-in-a-pit argument attached. Matthew notes the result, the Pharisees held a council against "
  "him, how they might destroy him."),
 ("Lord of the Sabbath", "He Shall Not Strive Nor Cry (vv.15-30)",
  "Matthew interrupts the conflict with the longest Old Testament quotation in his Gospel, from "
  "Isaiah 42, and it describes a manner rather than a mission: he shall not strive, nor cry, neither "
  "shall any man hear his voice in the streets. A bruised reed shall he not break, and smoking flax "
  "shall he not quench. It is placed immediately after a plot to kill him and immediately before the "
  "Beelzebub accusation, which is the point. The answer to that accusation is the divided kingdom "
  "argument, and then the alternative it forces, if I cast out devils by the Spirit of God, then the "
  "kingdom of God is come unto you."),
 ("The Unforgivable Sin", "By Thy Words Thou Shalt Be Judged (vv.33-42)",
  "The tree and its fruit again, and this time applied to speech, for out of the abundance of the "
  "heart the mouth speaketh. Then a warning that has no parallel elsewhere, every idle word that men "
  "shall speak, they shall give account thereof in the day of judgment, with the summary, by thy "
  "words thou shalt be justified, and by thy words thou shalt be condemned. The demand for a sign "
  "follows and is refused except for one, the sign of the prophet Jonas, with Matthew's own gloss "
  "attached, as Jonas was three days and three nights in the whale's belly. The Ninevites and the "
  "queen of the south are then produced as Gentiles who responded to less."),
 ("By Thy Words Thou Shalt Be Judged", "The Empty House, and Who Is My Mother (vv.43-50)",
  "A parable about a house swept and garnished and left empty, and the returning spirit bringing "
  "seven others, so that the last state of that man is worse than the first. Reform without "
  "occupancy is described as an invitation. Then the family arriving and asking for him, and the "
  "answer given while stretching out his hand toward the disciples, behold my mother and my "
  "brethren, with the criterion stated in the last verse, whosoever shall do the will of my Father "
  "which is in heaven, the same is my brother, and sister, and mother."),
],
"matthew13": [
 ("", "The Parable of the Sower (vv.1-9)",
  "He sits in a ship and the crowd stands on the shore, which Matthew records as staging rather "
  "than convenience. The parable is told without interpretation, four soils and four outcomes, and "
  "the yields on the good ground are graded, some an hundredfold, some sixtyfold, some thirtyfold. "
  "The closing line is the one that governs the whole chapter, who hath ears to hear, let him hear."),
 ("Why Parables?", "The Sower Explained, and the Tares (vv.18-30)",
  "The interpretation is given privately and identifies each soil with a way of hearing rather than "
  "a class of person: the wayside is the word not understood, the stony places receive it with joy "
  "and have no root, the thorns are the care of this world and the deceitfulness of riches. Then the "
  "wheat and the tares, which is Matthew's own parable and answers a practical question about mixed "
  "congregations. The servants offer to weed and are refused, lest while ye gather up the tares, ye "
  "root up also the wheat with them. Let both grow together until the harvest."),
 ("The Sower Explained, and the Tares", "Mustard Seed, Leaven, and the Parables Explained (vv.31-43)",
  "Two parables of small beginnings, the mustard seed becoming a tree and the leaven hidden in three "
  "measures of meal. Then Matthew's note that this was the method throughout, without a parable "
  "spake he not unto them, with a quotation from Psalm 78, I will utter things which have been kept "
  "secret from the foundation of the world. The explanation of the tares follows and is the most "
  "detailed allegory in the Gospels, with every element named: the field is the world, the good seed "
  "the children of the kingdom, the enemy the devil, the harvest the end of the world, the reapers "
  "the angels."),
 ("Mustard Seed, Leaven, and the Parables Explained", "Treasure, Pearl, Net, and Nazareth (vv.44-58)",
  "Three more parables and all three are about response. A man finds treasure in a field and sells "
  "all he has to buy it, a merchant does the same for one pearl, and both are described as acting "
  "with joy rather than sacrifice. The net gathers of every kind and is sorted on the shore, which "
  "repeats the tares. Then the question, have ye understood all these things? and a saying about the "
  "scribe who brings forth out of his treasure things new and old. The chapter ends at Nazareth, "
  "where the objection is his ordinariness, is not this the carpenter's son? and Matthew's closing "
  "sentence is the bleakest in the chapter, he did not many mighty works there because of their "
  "unbelief."),
],
"matthew14": [
 ("", "The Death of John the Baptist (vv.1-12)",
  "Matthew tells it as a flashback prompted by Herod's guilty conscience, this is John the Baptist, "
  "he is risen from the dead. The reason John was arrested is given plainly, for Herodias' sake, and "
  "the reason he was not killed sooner is political, he feared the multitude, because they counted "
  "him as a prophet. The execution turns on a rash oath made at a birthday party and a daughter "
  "prompted by her mother. Matthew's last note is about the disciples, they came and took up the "
  "body, and buried it, and went and told Jesus, which is the sentence that sets up the withdrawal "
  "in the next verse."),
 ("The Death of John the Baptist", "The Feeding of the Five Thousand (vv.13-21)",
  "He withdraws by ship into a desert place apart, having just heard of John's death, and the crowd "
  "follows on foot. Matthew gives the reason he does not send them away, and was moved with "
  "compassion toward them, and he healed their sick. The disciples' proposal is practical, this is a "
  "desert place, and the time is now past, send the multitude away. The answer puts it back on them, "
  "give ye them to eat. Five loaves, two fishes, and Matthew's count at the end is precise about who "
  "was included and who was not, about five thousand men, beside women and children."),
 ("The Feeding of the Five Thousand", "Walking on the Water (vv.22-27)",
  "He sends them ahead and goes up into a mountain apart to pray, and Matthew notes that he was "
  "there alone. The boat is in trouble, tossed with waves, for the wind was contrary, and the hour "
  "is the fourth watch, which is between three and six in the morning. The disciples' reaction is "
  "recorded as terror and a misidentification, they were troubled, saying, It is a spirit, and they "
  "cried out for fear. The answer is three short clauses, be of good cheer, it is I, be not afraid."),
 ("Peter Walking on Water", "They Worshipped Him, and Gennesaret (vv.32-36)",
  "When they were come into the ship, the wind ceased. Then the confession, and it is the first time "
  "in Matthew the disciples say it together, of a truth thou art the Son of God. The chapter closes "
  "at Gennesaret with a scene of pressure rather than teaching: the men of that place send word into "
  "all the country round about, bring their diseased, and besought him that they might only touch the "
  "hem of his garment, and as many as touched were made perfectly whole."),
],
"matthew15": [
 ("", "The Tradition of the Elders (vv.1-4,7-9)",
  "The charge is procedural, why do thy disciples transgress the tradition of the elders? for they "
  "wash not their hands when they eat bread, and the counter-charge is that their tradition breaks a "
  "commandment. Matthew has him quote the fifth commandment and its penalty clause before showing "
  "how the vow rule voids it. Then Isaiah, and it is the harshest quotation in the chapter: this "
  "people draweth nigh unto me with their mouth, but their heart is far from me. In vain do they "
  "worship me, teaching for doctrines the commandments of men."),
 ("Corban", "Not That Which Goeth Into the Mouth (vv.10-20)",
  "The principle is announced to the crowd, not that which goeth into the mouth defileth a man, but "
  "that which cometh out. The disciples report that the Pharisees were offended, and the reply is "
  "unconciliatory, every plant which my heavenly Father hath not planted shall be rooted up, and "
  "then the image of the blind leading the blind and both falling into the ditch. Peter asks for the "
  "explanation and gets a mild rebuke with it, are ye also yet without understanding? The "
  "explanation is anatomical and then moral: what enters goes into the belly, but out of the heart "
  "proceed evil thoughts, murders, adulteries, thefts, false witness, blasphemies."),
 ("Not That Which Goeth Into the Mouth", "The Woman of Canaan (vv.21-28)",
  "The hardest exchange in Matthew. She asks, and he answered her not a word. The disciples ask him "
  "to send her away. He states the limit of his commission, I am not sent but unto the lost sheep of "
  "the house of Israel. She worships and asks again. He answers with a proverb about children and "
  "dogs. And she takes the proverb and turns it, truth, Lord, yet the dogs eat of the crumbs which "
  "fall from their masters' table. The verdict is one of only two occasions in this Gospel where "
  "faith is called great, O woman, great is thy faith, and both times it is a Gentile."),
 ("The Woman of Canaan", "The Four Thousand Fed (vv.29-39)",
  "A second feeding, and Matthew records it without apology for the repetition. He goes up into a "
  "mountain and great multitudes come with the lame, blind, dumb and maimed, and the summary of the "
  "result is unusually vivid, insomuch that the multitude wondered, when they saw the dumb to speak, "
  "the maimed to be whole. The reason given for feeding them is duration, they continue with me now "
  "three days, and have nothing to eat, with a practical concern attached, lest they faint in the "
  "way. Seven loaves, a few little fishes, seven baskets left over, four thousand men beside women "
  "and children."),
],
"matthew16": [
 ("", "A Sign, and the Leaven of the Pharisees (vv.1-12)",
  "Pharisees and Sadducees together ask for a sign from heaven, and the answer mocks the request "
  "using their own competence, ye can discern the face of the sky, but can ye not discern the signs "
  "of the times? No sign is given but the sign of the prophet Jonas. Then in the boat a warning "
  "about the leaven of the Pharisees and of the Sadducees, which the disciples take as a comment on "
  "bread, having forgotten to bring any. The rebuke works through the arithmetic of both feedings "
  "before Matthew supplies the answer they missed, then understood they that he spake not of bread, "
  "but of the doctrine."),
 ("The Rock", "Whom Say Ye That I Am (vv.13-17,19-20)",
  "The question is asked at Caesarea Philippi and in two stages, first what men say, which produces "
  "a list, and then whom say ye that I am. Peter's answer goes further than any of the reported "
  "rumours, thou art the Christ, the Son of the living God. The reply credits the source rather than "
  "the insight, flesh and blood hath not revealed it unto thee, but my Father which is in heaven. "
  "Then the keys and the binding and loosing, and finally the charge that closes the scene and sits "
  "oddly against everything just granted, he charged his disciples that they should tell no man that "
  "he was Jesus the Christ."),
 ("Whom Say Ye That I Am", "Get Thee Behind Me, Satan (vv.21-28)",
  "From that time forth began Jesus to shew unto his disciples how he must go unto Jerusalem, and "
  "suffer many things. Matthew marks it as a beginning, so the confession is what makes the "
  "disclosure possible. Peter's objection is a rebuke, be it far from thee, Lord, this shall not be "
  "unto thee, and the answer to it is the harshest thing said to any disciple, get thee behind me, "
  "Satan, thou art an offence unto me. The reason given is a matter of perspective rather than "
  "loyalty, thou savourest not the things that be of God, but those that be of men. Then the terms "
  "for followers, and the question that measures them, what shall a man give in exchange for his "
  "soul?"),
],
"matthew17": [
 ("", "The Transfiguration (vv.1-13)",
  "Six days after, and the three taken up are the same three who will be taken into Gethsemane. "
  "Matthew describes the change in two comparisons, his face did shine as the sun, and his raiment "
  "was white as the light. Moses and Elias appear, Peter offers to build three tabernacles, and the "
  "voice from the cloud repeats the words from the baptism with three added, hear ye him. The "
  "disciples fall on their faces and are touched and told to rise, and Matthew's closing note is "
  "quiet, they lifted up their eyes, they saw no man, save Jesus only. Coming down, the question "
  "about Elijah is answered by identifying him with a man already dead."),
 ("The Transfiguration", "The Boy the Disciples Could Not Heal (vv.14-21)",
  "The father's complaint is about the disciples rather than the illness, I brought him to thy "
  "disciples, and they could not cure him, and the first response is exasperated, O faithless and "
  "perverse generation, how long shall I be with you? The healing is one clause. Then the private "
  "question, why could not we cast him out? and the answer is about size, because of your unbelief, "
  "for verily I say unto you, if ye have faith as a grain of mustard seed, ye shall say unto this "
  "mountain, Remove hence to yonder place, and it shall remove."),
 ("The Boy the Disciples Could Not Heal", "The Tribute Money (vv.22-27)",
  "The second passion prediction is given in two verses and Matthew records the reaction in four "
  "words, and they were exceeding sorry. Then an episode found only in this Gospel, and it is about "
  "a temple tax. Peter answers for his master before asking him, and the argument put to him "
  "afterwards is about family, do the kings of the earth take custom of their own children, or of "
  "strangers? The conclusion is that they are exempt, and the tax is paid anyway, notwithstanding, "
  "lest we should offend them. The coin comes out of a fish's mouth, and it is enough for two."),
],
"matthew18": [
 ("", "Who Is the Greatest (vv.1-14)",
  "The question is asked directly, who is the greatest in the kingdom of heaven? and the answer is a "
  "child called into the middle of the room, with a demand attached, except ye be converted, and "
  "become as little children, ye shall not enter. Then the warnings, and they are the most violent "
  "language in Matthew, aimed at whoever causes one of these little ones to offend: a millstone, and "
  "then hand, foot and eye. The section ends on the lost sheep, and Matthew's version is about a "
  "shepherd's arithmetic, doth he not leave the ninety and nine, and go into the mountains, and seek "
  "that which is gone astray? with the conclusion, it is not the will of your Father that one of "
  "these little ones should perish."),
 ("Church Discipline", "Where Two or Three Are Gathered (vv.18-22)",
  "The binding and loosing granted to Peter in chapter 16 is granted here to the community, and the "
  "context is the discipline procedure immediately before it rather than prayer in general. The "
  "promise about two or three gathered together in my name is part of the same paragraph. Then "
  "Peter's question, and he offers a generous number expecting approval, till seven times? The answer "
  "is seventy times seven, which is not a larger limit but the abolition of counting, and the parable "
  "that follows exists to explain why."),
],
"matthew19": [
 ("", "What Therefore God Hath Joined (vv.1-12)",
  "The question is put as a test and in the terms of a live rabbinic dispute, is it lawful for a man "
  "to put away his wife for every cause? The answer goes behind Moses to Genesis, quoting both "
  "creation accounts, and draws the conclusion, what therefore God hath joined together, let not man "
  "put asunder. Moses' provision is described as a concession to hardness of heart rather than a "
  "permission. The exception Matthew records is fornication. The disciples' reaction is telling, if "
  "it be so, it is not good to marry, and the reply neither denies nor generalises it, all men "
  "cannot receive this saying, he that is able to receive it, let him receive it."),
 ("What Therefore God Hath Joined", "Suffer the Little Children (vv.13-15)",
  "Three verses, and the disciples are wrong twice in three chapters about the same group. They "
  "rebuke the people bringing children, and the correction is short, suffer little children, and "
  "forbid them not, to come unto me, with the reason given as a statement about the kingdom rather "
  "than about children, for of such is the kingdom of heaven. He laid his hands on them, and "
  "departed thence."),
 ("Suffer the Little Children", "The Rich Young Man (vv.16-30)",
  "Matthew alone tells us he was young, and alone records the exchange about which commandments, "
  "and alone has the questioner ask what lack I yet? The instruction is total, go and sell that thou "
  "hast, and give to the poor, and Matthew's note on the outcome is one of the saddest sentences in "
  "the Gospel, he went away sorrowful, for he had great possessions. Then the camel and the needle's "
  "eye, the disciples' astonishment, and the answer that removes the matter from human capacity, "
  "with God all things are possible. Peter asks what they will get, and the reply promises thrones "
  "and then immediately unsettles it, but many that are first shall be last, and the last shall be "
  "first."),
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
