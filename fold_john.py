#!/usr/bin/env python3
"""
Completes John: chapters 1, 2, 3, 4, 5, 6, 7, 10, 14, 17, 19 and 21.

Same shape as Luke 5, 6 and 10 -- topical fields rather than sublists, with no verse
ranges and no coverage of the whole chapter. "Wedding at Cana:", "Pool of Bethesda:",
"The Greek Words for Love:" and the rest are substantive and easy to mistake for
sections. Each is folded into the section covering the same material, and the missing
sections are written.

AM stays on the allow-list. john10's own field is labelled 'The chapter contains two
"I AM" statements:', and the I AM sayings are the backbone of this Gospel.

Usage:
    python3 fold_john.py [--check]
"""
import os
import re
import sys

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")

ITEM = ('                    <div class="auth-item">'
        '<span class="auth-label">{label}</span> {body}</div>')

VERSES = {"john1": 51, "john2": 25, "john3": 36, "john4": 54, "john5": 47,
          "john6": 71, "john7": 53, "john10": 42, "john14": 31, "john17": 26,
          "john19": 42, "john21": 25}

CAPS_OK = {"LORD", "GOD", "YHWH", "OT", "NT", "BC", "AD", "KJV", "ESV", "ASV",
           "AM", "II"}

KEEP = {
    "john1": ["Author:", "Date Written:", "Audience:", "Historical Context:"],
    "john2": ["Author:", "Historical Context:"],
    "john3": ["Author:", "Historical Context:"],
    "john4": ["Author:", "Historical Context:"],
    "john5": ["Author:", "Historical Context:"],
    "john6": ["Author:", "Historical Context:"],
    "john7": ["Author:", "Historical Context:"],
    "john10": ["Author:", "Historical Context:"],
    "john14": ["Author:", "Historical Context:"],
    "john17": ["Author:", "Historical Context:"],
    "john19": ["Author:", "Historical Context:"],
    "john21": ["Author:", "Historical Context:"],
}

DROP = {
    "john1": ["Purpose of Chapter 1:"],
    "john2": ["Wedding at Cana:", "Temple Cleansing:"],
    "john3": ["Theological Significance:"],
    "john4": ["Jews and Samaritans:", "Jacob&#x27;s Well:", "The Nobleman&#x27;s Son:"],
    "john5": ["Pool of Bethesda:", "The Sabbath Controversy:"],
    "john6": ["Feeding the 5,000:", "The Bread of Life Discourse:"],
    "john7": ["The Feast of Tabernacles Context:"],
    "john10": ["Shepherd Imagery:", "Sheepfold:",
               "The chapter contains two &quot;I AM&quot; statements:"],
    "john14": ["The Holy Spirit (Paraclete):"],
    "john17": ["Structure:", "Theological Significance:"],
    "john19": ["Roman Crucifixion:", "Fulfilled Prophecy:"],
    "john21": ["Peter&#x27;s Restoration:", "The Greek Words for Love:"],
}

GENRE = "Gospel \u2014 Narrative and Discourse"

THEMES = {
"john1": "A prologue that starts before Genesis does, the Word made flesh and "
  "dwelling among us, a forerunner who defines himself by what he is not, a lamb "
  "identified before anything is explained, and disciples gathered by invitation",
"john2": "Water turned to wine at a wedding on the third day, a mother's confidence "
  "and a son's stated hour, a whip made deliberately, and a temple whose destruction "
  "and raising is offered as the only sign",
"john3": "A ruler who comes at night, birth described as something that happens to a "
  "person, a bronze serpent read as a foreshadowing, the most quoted verse in "
  "Scripture, and a forerunner content to decrease",
"john4": "A route taken through Samaria by necessity, a request for water from a woman "
  "at the wrong hour, worship relocated from a mountain to spirit and truth, a harvest "
  "already white, and a healing at a distance",
"john5": "A man waiting thirty-eight years by a pool, a healing that starts the "
  "hostility, work claimed on the Sabbath because the Father works, resurrection and "
  "judgment given to the Son, and four witnesses called",
"john6": "Five thousand fed from a boy's lunch, a crowd wanting a king who provides, "
  "walking on water, bread from heaven contrasted with manna, teaching hard enough to "
  "empty the room, and a question left with the twelve",
"john7": "Brothers who do not believe issuing a challenge, timing repeatedly called "
  "not yet come, a cry on the last day of the feast about thirst, officers who return "
  "without an arrest, and one Pharisee asking about due process",
"john10": "A common sheepfold and a shepherd known by voice, two I AM sayings, a life "
  "laid down rather than taken, other sheep not of this fold, and a charge of blasphemy "
  "answered from the Psalms",
"john14": "Troubled hearts addressed directly, a house with many rooms, an exclusive "
  "claim about the way, another Comforter of the same kind, and a peace distinguished "
  "from the world's",
"john17": "The longest recorded prayer of Jesus, glory asked for and glory shared "
  "before the world was, disciples described as given rather than recruited, "
  "sanctification through truth, and future believers prayed for by name of category",
"john19": "A scourging and a crown of thorns, authority described as given from above, "
  "a title in three languages that the priests could not get changed, a garment not "
  "torn, one word meaning paid in full, and a burial by two secret disciples",
"john21": "A return to fishing and an unrecognised figure on the shore, a net that "
  "does not break, a charcoal fire matching an earlier one, three questions for three "
  "denials, and a Gospel that ends by admitting it left things out",
}

SECTIONS = {
"john1": [
  ("In the Beginning Was the Word (vv.1-5)",
   "John opens where Genesis opens and then goes further back. The Word was in the "
   "beginning, was with God, and was God -- three clauses that distinguish and identify "
   "in the same breath. Logos carried weight in both Greek philosophy and Jewish wisdom "
   "literature, so the term reached two audiences at once. Writing against early "
   "Gnostic denials of Christ's full humanity and deity, John settles both before "
   "narrating anything."),
  ("A Man Sent to Bear Witness (vv.6-13)",
   "The prologue interrupts itself for John the Baptist, and the interruption is "
   "careful: he was not that Light, but was sent to bear witness of that Light. Then the "
   "tragedy in v.11 -- he came unto his own, and his own received him not -- set against "
   "v.12's provision for as many as received him. Verse 13 rules out three sources of "
   "that birth: not of blood, nor of the will of the flesh, nor of the will of man."),
  ("The Word Made Flesh (vv.14-18)",
   "The Word was made flesh and dwelt among us, and the verb behind \u201cdwelt\u201d is "
   "tabernacled -- pitched a tent, the language of Exodus 40. Glory is described as seen "
   "rather than inferred. Verse 17 sets Moses beside Christ without dismissing Moses, and "
   "v.18 states the problem the Gospel exists to solve: no man hath seen God at any time, "
   "and the only begotten Son hath declared him."),
  ("John's Testimony to the Priests (vv.19-28)",
   "Questioned by the delegation, John answers almost entirely in negatives -- not the "
   "Christ, not Elijah, not that prophet. He identifies himself only by quoting Isaiah, "
   "a voice in the wilderness. Asked why he baptises, he points past himself to one "
   "standing among them whose shoe latchet he is not worthy to unloose. A man defined by "
   "what he is not, which the next chapter's disciples will act on."),
  ("Behold the Lamb of God (vv.29-34)",
   "The identification comes without argument: behold the Lamb of God, which taketh away "
   "the sin of the world. For a first-century Jewish audience the phrase would summon "
   "Passover and the daily offerings at once. John adds that he did not know him, but "
   "that the one who sent him to baptise gave him the sign of the descending Spirit. His "
   "certainty rests on something shown to him rather than deduced."),
  ("The First Disciples Follow (vv.35-42)",
   "Two of John's own disciples hear him repeat the phrase and follow Jesus, and the "
   "first words Jesus speaks in this Gospel are a question: what seek ye? The exchange is "
   "domestic -- come and see, and they abode with him that day, and the tenth hour is "
   "recorded as though the writer remembers it. Andrew finds his brother, and Simon is "
   "renamed on sight."),
  ("Nathanael and the Ladder (vv.43-51)",
   "Philip is called directly, and his answer to Nathanael's scepticism about Nazareth "
   "is the same phrase used earlier: come and see. Nathanael's conversion turns on being "
   "seen under the fig tree before he was met. The chapter closes with an allusion to "
   "Jacob's ladder -- angels ascending and descending upon the Son of man -- so the "
   "connecting point between heaven and earth is named as a person."),
],
"john2": [
  ("The Wedding at Cana (vv.1-11)",
   "A first-century Jewish wedding ran about seven days, and running out of wine was a "
   "social disgrace for the host family rather than a minor inconvenience. Mary states "
   "the problem without a request, which is its own kind of confidence, and her "
   "instruction to the servants assumes he will act. Jesus's reply about his hour "
   "introduces a timing theme the Gospel returns to repeatedly. Six stone jars for "
   "purification, holding perhaps 120 gallons, are filled with water and the water is "
   "wine when it reaches the governor of the feast. John calls it the beginning of "
   "miracles and says the disciples believed."),
  ("Down to Capernaum (v.12)",
   "One transitional verse, and it is worth noticing who travels: his mother, his "
   "brethren and his disciples. The brothers are with him here and will be unbelieving "
   "at 7:5, so the Gospel records the family relationship changing over time rather than "
   "presenting it as settled."),
  ("Cleansing the Temple (vv.13-17)",
   "The trade occupied the Court of the Gentiles, and money changing and animal selling "
   "were necessary for pilgrims but had become exploitative. The response is not a "
   "spontaneous outburst -- he made a scourge of small cords, which takes time and "
   "intention. The disciples remember Psalm 69, the zeal of thine house hath eaten me "
   "up. John places this early where the other Gospels place a cleansing at the end, and "
   "whether these are one event or two has been argued for centuries."),
  ("Destroy This Temple (vv.18-25)",
   "Asked for a sign, he offers the one thing that cannot be produced on demand: "
   "destroy this temple, and in three days I will raise it up. His hearers take it "
   "literally and reckon the forty-six years of construction; John notes that he spoke "
   "of his body and that the disciples understood only after the resurrection. The "
   "chapter ends on a cool note -- he did not commit himself to those who believed "
   "because of miracles, since he knew what was in man."),
],
"john3": [
  ("Nicodemus Comes by Night (vv.1-8)",
   "A Pharisee and a member of the Sanhedrin, the council of seventy, comes at night, "
   "which the Gospel mentions without explaining and most readers take as caution. He "
   "opens with a compliment and gets an answer to a question he did not ask: except a "
   "man be born again he cannot see the kingdom of God. The Greek can mean again or from "
   "above and probably means both. Nicodemus's literal objection about entering the womb "
   "is answered with wind -- you hear it and cannot tell where it comes from."),
  ("The Serpent Lifted Up (vv.9-15)",
   "How can these things be, asks a man whose profession was knowing such things, and "
   "the reply is pointed: art thou a master of Israel and knowest not these things? Then "
   "the image from Numbers 21 -- as Moses lifted up the serpent in the wilderness, so "
   "must the Son of man be lifted up. Israel looked at a bronze snake on a pole and "
   "lived. Lifted up becomes this Gospel's word for the crucifixion."),
  ("For God So Loved the World (vv.16-21)",
   "The best-known verse in Scripture sits in a paragraph most people do not read past. "
   "God's motive is stated as love and the scope as the world, in a Gospel written to a "
   "community inclined to draw boundaries. Verse 17 rules out condemnation as the "
   "purpose; v.18 states that judgment is already settled by response. Then the reason "
   "given for unbelief is moral rather than intellectual: men loved darkness because "
   "their deeds were evil, and hate the light lest their deeds be reproved."),
  ("John's Final Testimony (vv.22-30)",
   "John's disciples come to him with a complaint that amounts to losing market share, "
   "and his answer refuses the premise. He calls himself the friend of the bridegroom "
   "who rejoices to hear his voice, which is a role with no ambition attached to it. "
   "Verse 30 is his last recorded word in this Gospel and the most quoted line about "
   "humility in it: he must increase, but I must decrease."),
  ("He That Cometh from Above (vv.31-36)",
   "Whether these verses are John the Baptist still speaking or the writer's own "
   "commentary is genuinely unclear, and translations differ on where the quotation "
   "ends. Either way the content escalates -- he that cometh from above is above all, "
   "and God giveth not the Spirit by measure. The chapter closes with the two outcomes "
   "stated plainly, everlasting life for the believer and the wrath of God abiding on "
   "the one who does not."),
],
"john4": [
  ("Through Samaria by Necessity (vv.1-6)",
   "He must needs go through Samaria, which was geographically the direct route and "
   "socially the avoided one. The hostility went back to 722 BC, when Assyria resettled "
   "the northern kingdom with foreign peoples who intermarried with those remaining, "
   "producing a mixed people with a mixed religion that Jews treated as unclean. Jacob's "
   "well still exists near Nablus and is around a hundred feet deep. He sits there at "
   "the sixth hour, being wearied with his journey."),
  ("Give Me to Drink (vv.7-15)",
   "Noon was not when respectable women drew water, and her being there alone at that "
   "hour hints at isolation before anything is said about her life. The request crosses "
   "three boundaries at once -- a Jew asking a Samaritan, a man asking a woman, a "
   "teacher asking a person of no standing -- and she says so. The conversation turns on "
   "living water, which she hears as a labour-saving offer and he means as something "
   "else."),
  ("Thou Hast Had Five Husbands (vv.16-19)",
   "The pivot is a request that seems to change the subject: go, call thy husband. Her "
   "answer is technically true and incomplete, and what follows is stated without "
   "commentary or rebuke. Five husbands and a present arrangement that is not marriage. "
   "Her response is not shame but recognition -- sir, I perceive that thou art a "
   "prophet."),
  ("In Spirit and in Truth (vv.20-26)",
   "She raises the standing dispute about the right mountain, which may be deflection or "
   "may be the real question of her life. The answer relocates worship rather than "
   "settling the geography: the hour cometh when neither in Jerusalem nor in this "
   "mountain, but in spirit and in truth. Then the plainest self-disclosure in the "
   "Gospels so far, made to a Samaritan woman rather than to the Sanhedrin: I that speak "
   "unto thee am he."),
  ("The Fields Are White (vv.27-38)",
   "The disciples return with lunch and are startled that he is talking to her, and John "
   "notes that none of them asked why. Meanwhile she leaves her waterpot -- a small "
   "detail that says she is not coming straight back. His answer about meat they know "
   "not of leads into the harvest image, and the point of v.35 is timing: not four months "
   "off, but white already."),
  ("Many Believed in Sychar (vv.39-42)",
   "Her testimony brings the town out, and the Gospel is careful about the sequence. "
   "Many believed because of her word, and then more believed because they heard him "
   "themselves, and they say so -- now we believe, not because of thy saying. Her witness "
   "was sufficient to start and not meant to be the end. He stays two days, which for a "
   "Jewish teacher in Samaria is the most remarkable line in the passage."),
  ("The Nobleman's Son (vv.43-54)",
   "Back in Galilee, a royal official asks him to come down before his child dies, and "
   "the healing happens without the visit -- go thy way, thy son liveth. The man believed "
   "the word and set off, and the servants' report matched the hour exactly. John calls "
   "it the second miracle in Galilee and the point of pairing it with Cana is faith "
   "acting on a word alone."),
],
"john5": [
  ("The Pool of Bethesda (vv.1-9)",
   "Excavations near the Sheep Gate have confirmed a pool with five colonnades, matching "
   "John's description precisely. The sick gathered there believing the stirred water "
   "healed. One man had been there thirty-eight years, and the question put to him is "
   "strange enough to be worth asking -- wilt thou be made whole? His answer is not yes "
   "but an explanation of why he cannot. He is told to rise, take up his bed and walk, "
   "and does, and the last clause of v.9 sets up everything after it: on the same day "
   "was the sabbath."),
  ("It Is the Sabbath Day (vv.10-16)",
   "Carrying an object was prohibited, so the objection is to the mat rather than the "
   "miracle. The man cannot name who healed him, and when Jesus finds him later the word "
   "given is sin no more, lest a worse thing come. Then he reports the name, and v.16 "
   "records the consequence: therefore did the Jews persecute Jesus. This chapter is "
   "where the hostility becomes settled."),
  ("My Father Worketh Hitherto (vv.17-24)",
   "The defence is the escalation. My Father worketh hitherto, and I work -- which the "
   "hearers understood correctly as a claim to equality, since v.18 says they sought to "
   "kill him for making himself equal with God. What follows is the most sustained "
   "statement of the Son's relation to the Father in the Synoptics or here: the Son can "
   "do nothing of himself, and also does whatever the Father does, and honour is owed to "
   "both alike."),
  ("The Dead Shall Hear His Voice (vv.25-30)",
   "Two resurrections are described, one present and one future -- the hour that is "
   "coming and now is, and the hour when all in the graves shall hear his voice. "
   "Authority to execute judgment is given to him because he is the Son of man. Verse "
   "30's \u201cI can of mine own self do nothing\u201d sits deliberately beside the "
   "largest claims in the chapter."),
  ("Four Witnesses (vv.31-40)",
   "He concedes that his own testimony alone would not stand and calls four others: "
   "John the Baptist, the works themselves, the Father, and the Scriptures. Verse 39 is "
   "the sharpest -- ye search the scriptures, for in them ye think ye have eternal life, "
   "and they testify of me, and ye will not come to me. Diligent study is granted and "
   "then shown to have missed its object."),
  ("Moses Wrote of Me (vv.41-47)",
   "The closing charge is that they receive honour from one another and not from God, "
   "and would receive someone coming in his own name. The last argument is the most "
   "pointed: Moses, in whom ye trust, is your accuser, for he wrote of me. Their "
   "authority is turned into a witness against them, which ends the chapter without any "
   "response recorded."),
],
"john6": [
  ("Feeding the Five Thousand (vv.1-14)",
   "The only miracle besides the resurrection in all four Gospels, set near the Sea of "
   "Galilee before Passover. John alone names Philip and Andrew and the boy with five "
   "loaves and two small fishes, and alone records the arithmetic -- two hundred "
   "pennyworth would not be enough. The gathering of twelve baskets afterwards is "
   "recorded as instruction rather than tidiness. The crowd's conclusion in v.14 is "
   "correct and their intention in v.15 is not."),
  ("Walking on the Sea (vv.15-21)",
   "He withdraws because they meant to make him king by force, and the miracle that "
   "follows has no audience but the disciples. Twenty-five or thirty furlongs out, in a "
   "rising wind, they see him walking on the water and are afraid. \u201cIt is I; be not "
   "afraid\u201d is in Greek closer to I am, which in this Gospel is never accidental."),
  ("Seeking Him for Bread (vv.22-27)",
   "The crowd tracks him to Capernaum and asks when he arrived. He does not answer the "
   "question. Ye seek me not because ye saw the miracles, but because ye did eat of the "
   "loaves -- the diagnosis is delivered before any teaching, and the instruction "
   "follows from it: labour not for the meat which perisheth."),
  ("The Bread from Heaven (vv.28-40)",
   "Asked what works God requires, he reduces it to one: believe on him whom he hath "
   "sent. They ask for a sign and cite the manna, which is a considerable request from "
   "people who ate bread the previous day. The answer distinguishes the true bread from "
   "the wilderness供 -- Moses did not give it, the Father gives it -- and then identifies "
   "it: I am the bread of life. Verse 37 states that none who come will be cast out."),
  ("Murmuring at Capernaum (vv.41-51)",
   "The objection is local and social: is not this Jesus, the son of Joseph, whose "
   "father and mother we know? Familiarity is the obstacle rather than argument. He does "
   "not soften the claim but sharpens it -- your fathers ate manna and died, and this is "
   "the bread which a man may eat and not die -- and adds that the bread is his flesh."),
  ("Eat My Flesh, Drink My Blood (vv.52-59)",
   "The language becomes deliberately harder rather than clearer, and the verb shifts to "
   "one used of chewing. To a Jewish audience for whom blood was forbidden, this was as "
   "offensive as it could be made. John notes the setting in v.59 -- the synagogue at "
   "Capernaum -- so this was said in the most public religious space available."),
  ("Many Went Back (vv.60-66)",
   "Even disciples call it a hard saying, and he does not retract it. The question in "
   "v.61, doth this offend you, is asked without a concession following. Verse 66 records "
   "the outcome plainly: from that time many of his disciples went back and walked no "
   "more with him. Nothing in the passage treats the loss as a failure of "
   "communication."),
  ("Will Ye Also Go Away? (vv.67-71)",
   "The question is put to the twelve and Peter answers with another: to whom shall we "
   "go? Thou hast the words of eternal life. It is agreement without claiming to have "
   "understood, which is the honest position after the discourse. The chapter closes on "
   "the note that one of the twelve was a devil, so the sifting is not finished."),
],
"john7": [
  ("His Brethren Did Not Believe (vv.1-13)",
   "The Feast of Tabernacles was one of three pilgrimage feasts, a week of living in "
   "booths commemorating the wilderness years. His brothers -- probably sons of Joseph "
   "and Mary born later -- tell him to show himself to the world, and John states baldly "
   "that they did not believe in him. The challenge echoes the wilderness temptation. He "
   "goes up later and privately, and the crowd is already arguing about him in "
   "whispers."),
  ("Teaching in the Midst of the Feast (vv.14-24)",
   "He teaches openly halfway through the feast and the reaction is to his lack of "
   "training: how knoweth this man letters, having never learned? His reply grounds the "
   "teaching outside himself, and offers a test anyone can apply -- if any man will do "
   "his will, he shall know of the doctrine. Then he raises their own inconsistency: they "
   "circumcise on the sabbath, and are angry that he made a man whole on it."),
  ("Is Not This the Christ? (vv.25-36)",
   "The Jerusalem crowd knows something the pilgrims do not, that the authorities want "
   "him dead and yet he speaks openly. Their objection is about origin -- we know whence "
   "this man is -- which the Gospel treats as ironic given the prologue. Officers are "
   "sent and nothing happens, because his hour was not yet come. His remark about going "
   "where they cannot come baffles them into speculating about the Greeks."),
  ("If Any Man Thirst (vv.37-39)",
   "On the last and greatest day of the feast the high priest poured water from the Pool "
   "of Siloam over the altar, a ceremony praying for rain and recalling water from the "
   "rock. Against that backdrop Jesus stands and cries out: if any man thirst, let him "
   "come unto me and drink. John adds the explanation that he spoke of the Spirit, not "
   "yet given."),
  ("Division Among the People (vv.40-44)",
   "The crowd splits three ways -- the Prophet, the Christ, or disqualified by coming "
   "from Galilee rather than Bethlehem. The objection is factually wrong and nobody "
   "checks, which is the quiet joke of the passage for a reader who knows where he was "
   "born. No arrest is made."),
  ("Nicodemus Speaks (vv.45-53)",
   "The officers return empty-handed with the best excuse in the Gospel: never man spake "
   "like this man. The Pharisees' contempt for the crowd is on display, and then "
   "Nicodemus -- last seen at night in chapter 3 -- asks a procedural question about "
   "condemning a man unheard. It is not a defence of Jesus so much as of due process, "
   "and it is enough to get him insulted."),
],
"john10": [
  ("The Door of the Sheep (vv.1-10)",
   "Sheep from several flocks shared a stone enclosure overnight with one entrance, and "
   "each shepherd called his own out by name in the morning. That is the picture behind "
   "the discourse, and it explains why recognition is by voice rather than by sight. The "
   "first I AM saying of the chapter follows: I am the door. Verse 10 sets the contrast "
   "-- the thief comes to steal and kill and destroy, and he came that they might have "
   "life more abundantly."),
  ("The Good Shepherd Giveth His Life (vv.11-18)",
   "The second I AM saying, and the definition attached to it is a death rather than a "
   "quality: the good shepherd giveth his life for the sheep. The hireling flees because "
   "the sheep are not his. Shepherd language is loaded in the Old Testament -- God is "
   "Israel's shepherd in Psalm 23, and Ezekiel 34 condemns the shepherds who failed the "
   "flock and promises God will come himself. Verse 16's other sheep not of this fold "
   "widens it past Israel, and v.18 insists the life is laid down, not taken."),
  ("Division Among the Jews (vv.19-21)",
   "Three verses of reaction, and the split is between madness and evidence. Some say he "
   "has a devil; others answer that a devil does not open the eyes of the blind. The "
   "healing of chapter 9 is still doing work, which is why John placed these chapters "
   "together."),
  ("At the Feast of Dedication (vv.22-30)",
   "The setting is Hanukkah, commemorating the temple's rededication after Antiochus "
   "Epiphanes desecrated it in the 160s BC -- a feast about cleansing God's house, which "
   "gives the question its edge. Asked plainly whether he is the Christ, he points to "
   "works and to the security of the sheep, and then states v.30: I and my Father are "
   "one."),
  ("The Charge of Blasphemy (vv.31-42)",
   "They take up stones and name the offence -- that thou being a man makest thyself "
   "God -- which is an accurate reading of v.30 rather than a misunderstanding. His "
   "answer quotes Psalm 82 and argues from the lesser to the greater, and then returns to "
   "the works: though ye believe not me, believe the works. He withdraws beyond Jordan, "
   "where many believed, and the chapter ends where the Gospel began, at John's baptising "
   "place."),
],
"john14": [
  ("In My Father's House (vv.1-6)",
   "This is the Upper Room Discourse, spoken the night of the arrest after Jesus has "
   "announced his departure, predicted Peter's denial and identified a betrayer. The "
   "disciples are troubled, and the chapter is the direct answer to that. Let not your "
   "heart be troubled, and the reason offered is a place prepared. Thomas's admission "
   "that they do not know the way produces v.6, the most exclusive sentence in the "
   "Gospel: I am the way, the truth, and the life."),
  ("He That Hath Seen Me (vv.7-11)",
   "Philip asks to be shown the Father, which after thirteen chapters is a poignant "
   "request. The reply is gentle and complete: he that hath seen me hath seen the Father, "
   "how sayest thou then, shew us the Father? The mutual indwelling of Father and Son is "
   "offered as the thing to believe, with the works given as the fallback for anyone who "
   "cannot."),
  ("Whatsoever Ye Shall Ask (vv.12-14)",
   "Greater works than these shall the believer do, because he goes to the Father -- a "
   "statement about scope rather than power, since the mission widens after Pentecost. "
   "The promise about asking is twice qualified by \u201cin my name\u201d, which the "
   "chapter treats as a limit as much as a licence."),
  ("Another Comforter (vv.15-24)",
   "The Spirit is introduced as the Paraclete, one called alongside to help, and the word "
   "\u201canother\u201d in v.16 means another of the same kind -- so the Spirit is "
   "personal in the way Jesus is, not a force. He will abide for ever, teach, and bring "
   "things to remembrance. Love and obedience are tied together three times in this "
   "section, and Judas not Iscariot asks the only other question in the chapter."),
  ("My Peace I Give unto You (vv.25-31)",
   "Peace is given and immediately distinguished: not as the world giveth. The "
   "instruction to rejoice at his going is the hardest thing in the chapter for people "
   "who do not want him to go. Verse 30 notes that the prince of this world comes and "
   "has nothing in him, and the chapter ends with arise, let us go hence -- so the "
   "remaining discourse is spoken on the way out."),
],
"john17": [
  ("Glorify Thy Son (vv.1-5)",
   "The longest recorded prayer of Jesus, and it opens with him lifting his eyes and "
   "naming the hour as come. The request is glory, and its stated purpose is that the "
   "Son may glorify the Father -- so the asking is not self-regarding. Verse 3 defines "
   "eternal life as knowing God and the one he sent, which is relational rather than "
   "temporal. Verse 5 asks for the glory he had with the Father before the world was."),
  ("I Have Manifested Thy Name (vv.6-12)",
   "The prayer turns to the disciples, described throughout as given to him -- the men "
   "which thou gavest me out of the world. They are characterised by having kept the "
   "word and by knowing it came from the Father. Verse 12's exception is stated without "
   "elaboration, that the son of perdition was lost, that the scripture might be "
   "fulfilled."),
  ("Sanctify Them Through Thy Truth (vv.13-19)",
   "The request is not removal but preservation: I pray not that thou shouldest take "
   "them out of the world, but that thou shouldest keep them from the evil. In the world "
   "and not of it is the position described, and the means of sanctifying is named as "
   "truth -- thy word is truth. Verse 18 sends them as he was sent, which sets the "
   "pattern for everything after."),
  ("That They All May Be One (vv.20-26)",
   "The prayer widens to those who will believe through their word, which includes every "
   "later reader. The petition is unity, and its model is the unity of Father and Son and "
   "its purpose is that the world may believe. Verse 24 asks that they be with him to "
   "behold his glory, and v.26 closes on the love the Father had for the Son being in "
   "them. It is the most intimate glimpse of the Trinity in Scripture, and it is given "
   "as overheard prayer rather than as doctrine."),
],
"john19": [
  ("Behold the Man (vv.1-7)",
   "Roman scourging used a flagellum weighted with bone and metal and could kill on its "
   "own. The crown of thorns and the purple robe were mockery of a claim to kingship. "
   "Pilate's \u201cbehold the man\u201d appears to be an attempt to satisfy the crowd "
   "with a broken figure, and it fails. The charge then changes from sedition to "
   "blasphemy -- he made himself the Son of God -- which is the real objection surfacing "
   "at last."),
  ("Thou Couldest Have No Power (vv.8-16)",
   "Pilate is afraid and asks where he is from, and gets silence. His assertion of "
   "authority is answered by relocating its source: thou couldest have no power at all "
   "against me, except it were given thee from above. The pressure that decides it is "
   "political -- if thou let this man go, thou art not Caesar's friend -- and the chief "
   "priests' final answer, we have no king but Caesar, is a considerable thing for them "
   "to have said."),
  ("The Title on the Cross (vv.17-22)",
   "The title is written in Hebrew, Greek and Latin so that everyone present could read "
   "it, and it states the charge as fact: Jesus of Nazareth the King of the Jews. The "
   "priests ask for it to be reworded as a claim rather than a statement, and Pilate "
   "refuses in the one line where he holds firm -- what I have written, I have written."),
  ("They Parted My Raiment (vv.23-27)",
   "The soldiers divide the clothes four ways and cast lots for the seamless coat rather "
   "than tear it, and John notes Psalm 22:18 fulfilled in the detail. Then the scene at "
   "the foot of the cross: his mother, and the disciple whom he loved, and a household "
   "arranged in two sentences. From that hour that disciple took her unto his own home."),
  ("It Is Finished (vv.28-30)",
   "The thirst is recorded with the scripture it fulfils, and the vinegar given on "
   "hyssop recalls Passover. Then one word in Greek, tetelestai -- paid in full, "
   "accomplished, completed -- which was stamped on settled accounts. John presents the "
   "last word from the cross as a declaration rather than a collapse, and adds that he "
   "bowed his head and gave up the ghost, in that order."),
  ("No Bone Broken; the Burial (vv.31-42)",
   "The legs are broken to hasten death before the sabbath, and his are not, and John "
   "cites both the Passover requirement that no bone be broken and Zechariah's they "
   "shall look on him whom they pierced. The blood and water are reported as eyewitness "
   "detail. Then two men who had kept quiet act publicly -- Joseph of Arimathaea, a "
   "secret disciple, and Nicodemus, who came by night in chapter 3 and now brings a "
   "hundred pound weight of spices."),
],
"john21": [
  ("Cast the Net on the Right Side (vv.1-8)",
   "Seven disciples go fishing, which reads as men returning to what they know while "
   "waiting for instructions. They catch nothing all night. The figure on the shore is "
   "not recognised, asks whether they have any meat, and tells them to try the other "
   "side. The recognition belongs to the disciple whom Jesus loved, and Peter's response "
   "is to put his coat on and jump in -- entirely characteristic."),
  ("Coals of Fire and Breakfast (vv.9-14)",
   "There is already a fire of coals with fish on it and bread, so breakfast was made "
   "before the catch was landed. The number of fish is given as a hundred and fifty "
   "three, and the reason has been debated for centuries -- the count of known species, a "
   "symbol, or simply what an eyewitness remembers. The detail John does draw out is that "
   "the net was not broken."),
  ("Lovest Thou Me? (vv.15-19)",
   "Peter denied him three times beside a charcoal fire, and this is the second charcoal "
   "fire in the Gospel. Three questions answer three denials. Jesus uses agapao twice and "
   "Peter answers with phileo, and on the third question Jesus switches to phileo -- "
   "meeting him where he is rather than holding the higher word over him. Each answer is "
   "followed by a commission, so restoration and reinstatement happen together, in front "
   "of witnesses. Then the prediction of how Peter will die, and the same two words that "
   "began it all: follow me."),
  ("What Is That to Thee? (vv.20-25)",
   "Peter's immediate question about John gets the bluntest answer in the chapter: what "
   "is that to thee? follow thou me. The Gospel then corrects a rumour that had grown out "
   "of the reply, which is a small window into the community that first read it. The last "
   "verse is the most disarming ending in Scripture -- there are many other things Jesus "
   "did, and if they were all written the world itself could not contain the books. A "
   "Gospel that ends by admitting how much it left out."),
],
}

CAPS = re.compile(r"\b[A-Z]{2,}\b")


def main():
    check = "--check" in sys.argv
    problems, notes, planned = [], [], {}

    for page in sorted(VERSES, key=lambda s: int(s[4:])):
        path = os.path.join(DOCS, f"{page}.html")
        html = open(path, encoding="utf-8").read()
        pane = re.search(r'(id="tab-authorship">)(.*?)(?=<div class="tab-content")',
                         html, re.S)
        if not pane:
            problems.append(f"{page}: no authorship pane")
            continue

        keep_order = KEEP[page]
        want_drop = DROP.get(page, [])
        fields, dropped, extra = {}, [], []
        for m in re.finditer(r'<div class="auth-item">(.*?)</div>', pane.group(2), re.S):
            inner = m.group(1)
            lab = re.match(r'<span class="auth-label">([^<]*)</span>\s*', inner)
            name = lab.group(1).strip() if lab else None
            rest = inner[lab.end():].strip() if lab else inner.strip()
            if name in keep_order:
                fields[name] = rest
            elif name is not None and name in want_drop:
                dropped.append(name)
            elif name is None:
                extra.append(rest)
            else:
                problems.append(f"{page}: unexpected field {name!r}")

        for want in keep_order:
            if want not in fields:
                problems.append(f"{page}: missing {want}")
        for want in want_drop:
            if want not in dropped:
                problems.append(f"{page}: expected to drop {want!r}, not found")
        if extra:
            fields["Historical Context:"] = " ".join(
                [fields["Historical Context:"]] + extra).strip()
            notes.append(f"{page}: {len(extra)} headless paragraph(s) merged")
        if dropped:
            notes.append(f"{page}: {len(dropped)} topical field(s) carried into sections")

        sections = SECTIONS[page]
        covered = set()
        for label, text in [("Key Themes", THEMES[page])] + \
                           [(f"section {h!r}", p) for h, p in sections] + \
                           [(w, fields[w]) for w in keep_order]:
            stray = sorted({w for w in CAPS.findall(text) if w not in CAPS_OK})
            if stray:
                problems.append(f"{page}: capitals {stray} in {label}")
            if "*" in text:
                problems.append(f"{page}: markdown asterisk in {label}")
        for head, _ in sections:
            if "\u2013" in head:
                problems.append(f"{page}: en-dash in {head!r}")
            if not re.search(r"\(vv?\.[\d]+[a-z]?(?:[-,:\s]+[\d]+[a-z]?)*\)$", head):
                problems.append(f"{page}: {head!r} does not end with its verse range")
            for m in re.finditer(r"\(vv?\.\s*(\d+)[a-z]?(?:\s*-\s*(\d+)[a-z]?)?\)", head):
                a, z = int(m.group(1)), int(m.group(2) or m.group(1))
                if z > VERSES[page]:
                    problems.append(f"{page}: {head!r} exceeds {VERSES[page]}")
                rng = set(range(a, z + 1))
                if rng & covered:
                    problems.append(f"{page}: {head!r} overlaps at {sorted(rng & covered)}")
                covered |= rng
        gaps = sorted(set(range(1, VERSES[page] + 1)) - covered)
        if gaps:
            problems.append(f"{page}: verses uncovered: {gaps}")

        parts = ["\n                <h3>Authorship &amp; Background</h3>\n"]
        for want in keep_order:
            if want == "Historical Context:":
                parts.append(ITEM.format(label="Classification:", body=GENRE) + "\n")
                parts.append(ITEM.format(label="Key Themes:",
                                         body=THEMES[page]) + "\n")
            parts.append(ITEM.format(label=want, body=fields[want]) + "\n")
        for head, prose in sections:
            parts.append(ITEM.format(label=head + ":", body=prose) + "\n")
        new_body = "".join(parts) + "            </div>\n\n            "

        new = html[:pane.start(2)] + new_body + html[pane.end(2):]
        o, c = len(re.findall(r"<div\b", new)), len(re.findall(r"</div>", new))
        if o != c:
            problems.append(f"{page}: div imbalance {o} vs {c}")
            continue
        planned[path] = new

    for n in notes:
        print(f"    note: {n}")
    if problems:
        print(f"refusing to write, {len(problems)} problem(s)")
        for p in problems:
            print(f"    {p}")
        return 1
    if not check:
        for path, new in planned.items():
            open(path, "w", encoding="utf-8").write(new)
    print(f"{'would fold' if check else 'folded'} {len(planned)} chapters")
    return 0


if __name__ == "__main__":
    sys.exit(main())
