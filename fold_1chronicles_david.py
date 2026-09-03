#!/usr/bin/env python3
"""
1 Chronicles 10 to 29: David's reign. Twenty pages, 535 verses, no existing sections.

The Chronicler's David is not the David of Samuel, and the sections have to describe
what is on the page rather than what the reader may remember from the other account.
Bathsheba is absent. Absalom's rebellion is absent. Amnon, Tamar and Adonijah are
absent. Saul's reign is compressed into a single chapter that exists to record his
death. What fills the space instead is the temple: five chapters of Levites, priests,
singers, gatekeepers, treasurers and army rotas that Samuel does not have at all.

Two consequences for the sectioning. Chapters 23 to 27 are administrative registers
and are sectioned by their own divisions, the same way chapters 1 to 9 were, because
that is what they are. And where the Chronicler does keep a failure, it is worth
saying that he kept it: the census in chapter 21 is retained in full, including the
plague and the price paid for the threshing floor, because the site becomes the
temple mount.

Usage:
    python3 fold_1chronicles_david.py [--check]
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
"1chronicles10": [
 ("", "The Death of Saul (vv.1-7)",
  "Saul's entire reign gets one chapter in this book and it is the chapter in which he dies. The "
  "battle at Gilboa is given in seven verses: the archers find him, his three sons are killed, he "
  "asks his armourbearer to run him through, the man refuses, and Saul falls on his own sword. "
  "The Chronicler adds no reign, no anointing, no jealousy and no pursuit of David. A reader who "
  "did not know 1 Samuel would learn here only that there was a king before David and that he "
  "lost a battle."),
 ("The Death of Saul", "The Philistines Strip Him (vv.8-10)",
  "The body is found the next day and treated as a trophy: they stripped him, took his head and "
  "his armour, sent word through the land of the Philistines to their idols and to the people, "
  "put his armour in the house of their gods and fastened his head in the temple of Dagon. The "
  "Chronicler is interested in the religious use made of the corpse, which is why the detail about "
  "which temple survives."),
 ("The Philistines Strip Him", "Jabesh-gilead, and Why Saul Died (vv.11-14)",
  "The men of Jabesh-gilead retrieve the bodies and bury the bones under an oak, and fasted seven "
  "days. Then the Chronicler does something Samuel never does: he explains the death "
  "theologically. So Saul died for his transgression which he committed against the LORD, and for "
  "asking counsel of one that had a familiar spirit, and enquired not of the LORD, therefore he "
  "slew him, and turned the kingdom unto David. The reign is given a verdict rather than a "
  "narrative."),
],
"1chronicles11": [
 ("", "All Israel Anoints David (vv.1-3)",
  "There is no seven-year war with the house of Saul in this account. All Israel gathers at Hebron "
  "at once and the argument they make is about kinship and record, behold, we are thy bone and thy "
  "flesh, and even in time past, when Saul was king, thou wast he that leddest out and broughtest "
  "in Israel. The covenant is made before the LORD and the anointing is credited to prophecy, "
  "according to the word of the LORD by Samuel."),
 ("All Israel Anoints David", "The Taking of Jerusalem (vv.4-9)",
  "The Jebusites tell him he shall not come in, and David offers a promotion to whoever goes up "
  "first. Joab wins it and becomes chief. The Chronicler notes the building work that followed, he "
  "built the city round about, even from Millo, and Joab repaired the rest, and closes with a "
  "sentence he will repeat in different words throughout the book, so David waxed greater and "
  "greater, for the LORD of hosts was with him."),
 ("The Taking of Jerusalem", "The Three, and the Water of Bethlehem (vv.10-19)",
  "The roll of the mighty men opens with three feats: Jashobeam against three hundred, Eleazar "
  "holding a barley field at Pas-dammim when the people fled. Then the incident the Chronicler "
  "clearly relishes. David says, longing rather than commanding, oh that one would give me drink "
  "of the water of the well of Bethlehem. Three men break through the Philistine garrison to get "
  "it, and he will not drink it, and pours it out to the LORD, saying, shall I drink the blood of "
  "these men that have put their lives in jeopardy?"),
 ("The Three, and the Water of Bethlehem", "The Roll of the Mighty Men (vv.20-47)",
  "Twenty-eight verses of names, and the list is longer here than in 2 Samuel, running on past the "
  "thirty into men from Reuben, Moab, Aroer and Mesopotamia. The individual feats recorded are "
  "specific and physical: Abishai against three hundred, Benaiah killing two lionlike men of Moab "
  "and a lion in a pit in time of snow, and taking a spear out of an Egyptian's hand and killing "
  "him with it. What the roll is doing is documenting that the kingdom rested on named men from "
  "many tribes and some from outside Israel altogether."),
],
"1chronicles12": [
 ("", "Those Who Came to Ziklag (vv.1-22)",
  "The chapter reaches back before the anointing to list defectors, men who came to David while he "
  "kept himself close because of Saul. The details are military and admiring: Benjamites of Saul's "
  "own tribe who could use both the right hand and the left in hurling stones, Gadites whose "
  "faces were like the faces of lions and who were as swift as the roes upon the mountains, and "
  "the men of Issachar who had understanding of the times, to know what Israel ought to do. The "
  "section closes on a number that keeps growing, for daily there came to David to help him, until "
  "it was a great host, like the host of God."),
 ("Those Who Came to Ziklag", "The Numbers at Hebron (vv.23-40)",
  "The muster at Hebron is given tribe by tribe with totals, and the totals are enormous, "
  "including one hundred and twenty thousand from the eastern tribes. The Chronicler's point is "
  "unanimity, all the rest also of Israel were of one heart to make David king. The last three "
  "verses are about food rather than force: relatives bringing bread on asses and camels and "
  "mules and oxen, meal, cakes of figs, bunches of raisins, wine, oil, oxen and sheep abundantly, "
  "for there was joy in Israel. A coronation described as a supply operation and a party."),
],
"1chronicles13": [
 ("", "The Ark Fetched from Kirjath-jearim (vv.1-8)",
  "David consults the captains and the whole congregation first, and the reason he gives for "
  "moving the ark is a criticism of the previous reign, for we enquired not at it in the days of "
  "Saul. The ark is carried on a new cart, which is how the Philistines transported it and not how "
  "the law prescribes. The Chronicler records the celebration in full, all Israel played before "
  "God with all their might, with singing, harps, psalteries, timbrels, cymbals and trumpets, "
  "which makes the next paragraph land harder."),
 ("The Ark Fetched from Kirjath-jearim", "Uzza Struck at the Threshingfloor (vv.9-14)",
  "The oxen stumble, Uzza puts out his hand to hold the ark, and he dies there before God. David "
  "is described as displeased and then afraid, and asks a question rather than praying, how shall I "
  "bring the ark of God home to me? The ark is diverted to the house of Obed-edom and stays three "
  "months, and the Chronicler notes what happened there, the LORD blessed the house of Obed-edom, "
  "and all that he had. The same object kills one man and blesses a household, and chapter 15 will "
  "explain the difference."),
],
"1chronicles14": [
 ("", "Hiram's Builders, and David's Household (vv.1-7)",
  "Hiram of Tyre sends cedar, masons and carpenters, and David draws the conclusion the Chronicler "
  "wants drawn, David perceived that the LORD had confirmed him king over Israel, for his kingdom "
  "was lifted up on high, because of his people Israel. The blessing is for the nation rather than "
  "the man. Then the sons born at Jerusalem are listed, thirteen names, and among them Solomon, "
  "recorded without any account of his mother."),
 ("Hiram's Builders, and David's Household", "Two Victories over the Philistines (vv.8-17)",
  "Both battles are fought after enquiring, and the Chronicler makes the enquiry the point of the "
  "chapter. The first time the answer is go up, and the place is renamed Baal-perazim, the place "
  "of breakings. The second time the same question gets a different answer: go not up after them, "
  "turn away from them, and come upon them over against the mulberry trees, and wait for the sound "
  "of a going in the tops of the trees. A commander who had won once is told to do something else "
  "the next time. The chapter closes with his fame going out into all lands."),
],
"1chronicles15": [
 ("", "None Ought to Carry the Ark But the Levites (vv.1-15)",
  "The second attempt begins with research. David states the rule he broke, none ought to carry "
  "the ark of God but the Levites, for them hath the LORD chosen, and then names the failure "
  "directly, the LORD our God made a breach upon us, for that we sought him not after the due "
  "order. Four thousand priests and Levites are gathered by family, and the closing verse "
  "describes the correction being executed, the children of the Levites bare the ark of God upon "
  "their shoulders with the staves thereon. No cart."),
 ("None Ought to Carry the Ark But the Levites",
  "The Singers and the Order of the Procession (vv.16-24)",
  "Nine verses of musical staffing, which is the sort of detail only Chronicles keeps. Heman, "
  "Asaph and Ethan are appointed with psalteries on Alamoth and harps on Sheminith, terms the "
  "Chronicler does not explain and which survive in psalm headings. Chenaniah is put in charge of "
  "the song because he was skilful, and two porters are named for the door of the ark. A "
  "procession is being organised like an orchestra."),
 ("The Singers and the Order of the Procession",
  "The Ark Comes Up, and Michal Despises (vv.25-29)",
  "God helped the Levites, and they offered seven bullocks and seven rams, and David wore a linen "
  "ephod and danced. The Chronicler keeps Michal at the window despising him in her heart, which "
  "is the one piece of the Samuel account's domestic conflict he does not omit, and he cuts the "
  "argument that follows it. She looks, she despises, and the chapter ends."),
],
"1chronicles16": [
 ("", "The Ark Set in Place (vv.1-6)",
  "Offerings, a blessing in the name of the LORD, and a distribution to every one of Israel, both "
  "man and woman, of a loaf of bread, a good piece of flesh and a flagon of wine. Then the "
  "appointments before the ark, and the job description is unusually specific, to record, and to "
  "thank and praise the LORD God of Israel. Asaph is given the cymbals and two priests the "
  "trumpets continually."),
 ("The Ark Set in Place", "O Give Thanks Unto the LORD (vv.7-22)",
  "The psalm David delivers into Asaph's hand, and readers of the Psalter will recognise it, "
  "because this section is Psalm 105 almost word for word. The opening is a run of imperatives, "
  "give thanks, call upon his name, sing unto him, talk ye of all his wondrous works. Then the "
  "argument turns to the covenant with Abraham, the word which he commanded to a thousand "
  "generations, quoted as still in force, saying, Unto thee will I give the land of Canaan. And "
  "the protection clause the exiles would have read closely, touch not mine anointed, and do my "
  "prophets no harm."),
 ("O Give Thanks Unto the LORD", "Sing Unto the LORD, All the Earth (vv.23-36)",
  "The second half of the psalm is Psalm 96 with the end of Psalm 106 attached, and its reach is "
  "wider than the first: declare his glory among the heathen, for all the gods of the people are "
  "idols, but the LORD made the heavens. Creation is called in to respond, let the heavens be "
  "glad, let the sea roar, let the fields rejoice, then shall the trees of the wood sing out. The "
  "closing petition is the one an exile prays, save us, O God of our salvation, and gather us "
  "together, and deliver us from the heathen, and the people answer Amen."),
 ("Sing Unto the LORD, All the Earth", "Ministers at Both Places (vv.37-43)",
  "A practical arrangement that shows the state of worship at this point: the ark is in Jerusalem "
  "with Asaph and his brethren before it continually, and the tabernacle with the altar of burnt "
  "offering is still at Gibeon, with Zadok and his priests there to offer morning and evening. "
  "Two sanctuaries, one with the ark and no altar, one with the altar and no ark, which is exactly "
  "the problem the temple is built to solve. Then everyone goes home, and David returns to bless "
  "his house."),
],
"1chronicles17": [
 ("", "Thou Shalt Not Build Me an House (vv.1-6)",
  "David's proposal is stated as an embarrassment about accommodation, lo, I dwell in an house of "
  "cedars, but the ark of the covenant of the LORD remaineth under curtains. Nathan approves it "
  "and is corrected the same night. The refusal is put as a question with a history attached, "
  "whereas I have not dwelt in an house since the day that I brought up Israel unto this day, and "
  "then the argument that God never asked for one, spake I a word to any of the judges, saying, "
  "Why have ye not built me an house of cedars?"),
 ("Thou Shalt Not Build Me an House", "The Promise of a House and a Throne (vv.7-15)",
  "The refusal turns into the largest promise in the book, and the pivot is a play on the word "
  "house. David wanted to build one and is told one will be built for him, the LORD will build "
  "thee an house. Then a place for the people that shall not be moved, and a son whose throne "
  "shall be established for ever, with a clause the Chronicler keeps and softens from Samuel, I "
  "will not take my mercy away from him, as I took it from him that was before thee. What David "
  "asked to do for God is answered by what God undertakes to do for him."),
 ("The Promise of a House and a Throne", "Who Am I, O LORD God (vv.16-27)",
  "The prayer is the longest speech David makes in Chronicles and it is almost entirely about "
  "smallness and scale. Who am I, O LORD God, and what is mine house, that thou hast brought me "
  "hitherto? Then a comparison, and thou hast regarded me according to the estate of a man of high "
  "degree. The nation is described in the same terms, what one nation in the earth is like thy "
  "people Israel, whom God went to redeem to be his own people. And the prayer ends by asking for "
  "nothing new, only that the promise stand, let it be established for ever, and do as thou hast "
  "said."),
],
"1chronicles18": [
 ("", "Victories on Every Border (vv.1-8)",
  "Eight verses covering campaigns in four directions, Philistines to the west, Moab to the east, "
  "Hadarezer of Zobah to the north, Syrians of Damascus beyond that. The Chronicler's interest is "
  "in what came back rather than how the fighting went: shields of gold, exceeding much brass, "
  "chariots and horsemen, and one detail he adds for a later purpose, wherewith Solomon made the "
  "brasen sea, and the pillars, and the vessels of brass. Temple furniture is being paid for by "
  "these wars."),
 ("Victories on Every Border", "Tou of Hamath, and David's Officers (vv.9-17)",
  "Tou sends his son with vessels of gold and silver and brass, and David dedicates them, which is "
  "the pattern for the whole chapter, and the summary sentence is repeated, the LORD preserved "
  "David whithersoever he went. Then the cabinet list: Joab over the host, Jehoshaphat the "
  "recorder, Zadok and Abimelech the priests, Shavsha the scribe, Benaiah over the Cherethites and "
  "the Pelethites, and the sons of David chief about the king. A conquest chapter ends with a "
  "civil service."),
],
"1chronicles19": [
 ("", "The Ambassadors Humiliated (vv.1-5)",
  "David sends condolences on the death of Nahash, and Hanun's princes talk him out of receiving "
  "them, thinkest thou that David doth honour thy father, that he hath sent comforters unto thee? "
  "are not his servants come unto thee for to search? The messengers are shaved and their garments "
  "cut off by the middle, and David's response is to spare them the humiliation of being seen, "
  "tarry at Jericho until your beards be grown. A war begins over a diplomatic insult."),
 ("The Ambassadors Humiliated", "Joab and Abishai Divide the Army (vv.6-15)",
  "The Ammonites hire thirty-two thousand chariots and the Syrians besides, and Joab finds himself "
  "with a battle in front and behind. The arrangement he makes with his brother is practical and "
  "the speech attached to it is the best thing he says anywhere: be of good courage, and let us "
  "behave ourselves valiantly for our people, and for the cities of our God, and let the LORD do "
  "that which is good in his sight. Both enemies break and flee, and Joab returns to Jerusalem "
  "without pressing the pursuit."),
 ("Joab and Abishai Divide the Army", "The Syrians Beaten Beyond Jordan (vv.16-19)",
  "The Syrians regroup with reinforcements from beyond the river and David comes out himself. The "
  "casualties are given in round numbers, seven thousand chariots and forty thousand footmen, and "
  "the outcome is political rather than territorial: when the servants of Hadarezer saw that they "
  "were put to the worse, they made peace with David, and became his servants, neither would the "
  "Syrians help the children of Ammon any more. Ammon is left without an ally, which sets up the "
  "siege in the next chapter."),
],
"1chronicles20": [
 ("", "The Taking of Rabbah (vv.1-3)",
  "Three verses where Samuel has three chapters, and the omission is the most conspicuous in the "
  "book. Joab besieges Rabbah, and the Chronicler notes only that David tarried at Jerusalem, "
  "without saying what he did there. Bathsheba, Uriah, Nathan's parable and the death of the child "
  "are all absent. What is kept is the crown taken from the king's head, a talent of gold with "
  "precious stones in it, and the forced labour imposed on the people of the city."),
 ("The Taking of Rabbah", "The Sons of the Giant at Gath (vv.4-8)",
  "Three short encounters with unusually large men, and each is credited to a named soldier rather "
  "than to David: Sibbechai kills Sippai, Elhanan kills Lahmi the brother of Goliath, and "
  "Jonathan the son of Shimea kills a man with six fingers on every hand and six toes on every "
  "foot. The Chronicler's summary makes the point about who did it, they fell by the hand of David, "
  "and by the hand of his servants, which is his way of assigning credit to a reign rather than to "
  "a man."),
],
"1chronicles21": [
 ("", "Satan Provoked David to Number Israel (vv.1-8)",
  "The Chronicler keeps this failure in full, and his opening clause differs from Samuel's: Satan "
  "stood up against Israel, and provoked David to number Israel. Joab objects on principle and "
  "asks why my lord requireth this thing, why will he be a cause of trespass to Israel? and is "
  "overruled. He leaves Levi and Benjamin out of the count because the king's word was abominable "
  "to him. The judgment falls, and David's confession is unqualified, I have sinned greatly, "
  "because I have done this thing, but now, I beseech thee, do away the iniquity of thy servant, "
  "for I have done very foolishly."),
 ("Satan Provoked David to Number Israel", "Choose One of Three (vv.9-17)",
  "Gad brings three options, three years of famine, three months of defeat, or three days of "
  "pestilence, and David's answer is a preference about who holds the sword, let me fall now into "
  "the hand of the LORD, for very great are his mercies, but let me not fall into the hand of man. "
  "Seventy thousand die. The angel is seen standing between the earth and the heaven with a drawn "
  "sword stretched out over Jerusalem, and is stopped at the threshingfloor of Ornan. David's plea "
  "is that the punishment be redirected onto him, is it not I that commanded the people to be "
  "numbered? but as for these sheep, what have they done?"),
 ("Choose One of Three", "The Threshingfloor of Ornan (vv.18-30)",
  "Ornan offers the site, the oxen, the wood and the wheat for nothing, and David refuses on a "
  "principle he states plainly, I will not take that which is thine for the LORD, nor offer burnt "
  "offerings without cost. He pays six hundred shekels of gold. The fire falls from heaven upon "
  "the altar, and the last three verses explain why this location matters more than the story that "
  "reached it: the tabernacle was still at Gibeon and David could not go before it, for he was "
  "afraid because of the sword of the angel. The temple site is chosen at the place where a plague "
  "stopped."),
],
"1chronicles22": [
 ("", "This Is the House of the LORD God (vv.1-5)",
  "David identifies the site in one sentence, this is the house of the LORD God, and this is the "
  "altar of the burnt offering for Israel, and then starts buying materials. Masons are set to "
  "hew stones, iron for nails, brass without weight, and cedar from Zidon and Tyre. The reason "
  "given for stockpiling is a judgement about his son, Solomon my son is young and tender, and the "
  "house must be exceeding magnifical, I will therefore now make preparation for it. A man told he "
  "may not build spends his last years buying the materials."),
 ("This Is the House of the LORD God", "Thou Shalt Not Build, Solomon Shall (vv.6-16)",
  "The charge to Solomon includes the reason David was refused, and Chronicles is the only book "
  "that gives it in David's own mouth: thou hast shed blood abundantly, and hast made great wars, "
  "thou shalt not build an house unto my name. The contrast drawn is in the son's name, a man of "
  "rest, and I will give him rest from all his enemies, for his name shall be Solomon. Then the "
  "commission, be strong, and of good courage, dread not, nor be dismayed, with an inventory "
  "attached: a hundred thousand talents of gold, a thousand thousand talents of silver, and brass "
  "and iron without weight."),
 ("Thou Shalt Not Build, Solomon Shall", "The Charge to the Princes (vv.17-19)",
  "The last three verses turn from the son to the officials, and the argument made to them is that "
  "the work is possible because the fighting is over, is not the LORD your God with you? and hath "
  "he not given you rest on every side? The instruction is in two parts and the order matters, "
  "now set your heart and your soul to seek the LORD your God, arise therefore, and build ye the "
  "sanctuary."),
],
"1chronicles23": [
 ("", "The Levites from Thirty Years Old (vv.1-6)",
  "Six verses that set up five chapters of administration. David is old and full of days and makes "
  "Solomon king, and then numbers the Levites: thirty-eight thousand from thirty years old and "
  "upward. The division that follows is functional rather than tribal, twenty-four thousand to set "
  "forward the work of the house, six thousand officers and judges, four thousand porters, and "
  "four thousand praising the LORD with the instruments which I made, said David."),
 ("The Levites from Thirty Years Old", "Gershon, Kohath and Merari (vv.7-23)",
  "The three families are listed with their sons and grandsons, and the register keeps its "
  "irregularities: one man had no sons, so his brethren were reckoned together with him, and "
  "another's sons were few, so they were in one reckoning according to their father's house. A "
  "document that has to allocate duty cannot round its numbers, and the awkward entries are the "
  "evidence that it is a working list rather than a composition."),
 ("Gershon, Kohath and Merari", "The New Charge from Twenty Years Old (vv.24-32)",
  "The age is lowered from thirty to twenty and the Chronicler explains why, and it is because the "
  "job has changed: the Levites shall no more carry the tabernacle, nor any vessels of it. A "
  "portable sanctuary needed strong men. A permanent building needs staff. The new duties are "
  "listed, the courts, the chambers, the purifying, the shewbread, the fine flour, the measures, "
  "and to stand every morning to thank and praise the LORD, and likewise at even. The one thing "
  "carried away in the exile was the pattern of the work."),
],
"1chronicles24": [
 ("", "The Twenty-Four Courses of the Priests (vv.1-19)",
  "Aaron's four sons are named and two of them removed in the first two verses, Nadab and Abihu "
  "died before their father, and had no children. The rota is drawn from the remaining two houses "
  "and the method is stated to forestall any dispute: thus were they divided by lot, one sort with "
  "another, and the lots are cast in the presence of David, Zadok, Ahimelech and the chief "
  "fathers. Twenty-four names in order, and the eighth is Abijah, which is the course Zacharias "
  "belonged to in Luke 1. This rota was still running a thousand years later."),
 ("The Twenty-Four Courses of the Priests", "The Rest of the Sons of Levi (vv.20-31)",
  "The non-priestly Levites are then given the same treatment, family by family, and the closing "
  "verse repeats the fairness clause with one addition, these likewise cast lots over against "
  "their brethren the sons of Aaron, the principal fathers even as their younger brethren. Seniority "
  "is explicitly set aside in the drawing. The register is at pains to record that nobody was "
  "given a better rota because of his standing."),
],
"1chronicles25": [
 ("", "Prophesying with Harps and Cymbals (vv.1-8)",
  "The musicians are described in terms nobody expects: David separated to the service the sons of "
  "Asaph, and of Heman, and of Jeduthun, who should prophesy with harps, with psalteries, and with "
  "cymbals. Three times in eight verses the word for their work is prophesying. Heman is called "
  "the king's seer and credited with fourteen sons and three daughters, all under his direction. "
  "The last verse insists on the same impartiality as the priestly rota, they cast lots, as well "
  "the small as the great, the teacher as the scholar."),
 ("Prophesying with Harps and Cymbals", "The Twenty-Four Courses of the Singers (vv.9-31)",
  "Twenty-three verses of names and lot numbers, twelve men to each course, two hundred and eighty "
  "eight in all. The list has one feature readers have noticed for a long time: a run of the names "
  "in verse 4, taken in order, reads in Hebrew as a short prayer about mercy and visions, which "
  "may be a fragment of a psalm turned into a family. Whether or not that is intended, the "
  "chapter's purpose is administrative. The music at the temple was rostered like the sacrifices."),
],
"1chronicles26": [
 ("", "The Porters and the Gates (vv.1-19)",
  "The gatekeepers are assigned by family and by direction, and the register keeps the reasons for "
  "the appointments. Obed-edom is here, the man the ark stayed with in chapter 13, and his sons are "
  "described as mighty men of valour, with the note that God blessed him. One man is chosen because "
  "he was a wise counsellor. The east gate gets six Levites a day, the north four, the south four, "
  "the storehouse two, and the assignments are settled by lot. It is a duty roster for a building "
  "that does not exist yet."),
 ("The Porters and the Gates", "The Treasuries (vv.20-28)",
  "Two treasuries are distinguished, the treasures of the house of God and the treasures of the "
  "dedicated things, and named families are put over each. The Chronicler then lists where the "
  "dedicated things came from, and the list is a summary of the wars: Samuel the seer, Saul, "
  "Abner, Joab, and all that had dedicated, out of the spoils won in battles. Plunder taken over "
  "generations is being catalogued as temple endowment."),
 ("The Treasuries", "Officers and Judges Outward (vv.29-32)",
  "The last four verses put Levites outside the sanctuary altogether, for the outward business "
  "over Israel, for officers and judges, and the numbers are substantial, seventeen hundred on the "
  "west side of Jordan and two thousand seven hundred over the eastern tribes. The remit named is "
  "both civil and religious, in every matter pertaining to God, and in the affairs of the king. The "
  "tribe with no land is the tribe that administers everybody else's."),
],
"1chronicles27": [
 ("", "The Twelve Monthly Courses (vv.1-15)",
  "The army is organised as a rota rather than a standing force: twelve divisions of twenty-four "
  "thousand, each serving one month of the year, so at any time one twelfth is on duty. The "
  "commanders are drawn from the mighty men of chapter 11, which ties the militia to the men who "
  "took Jerusalem. One entry records a succession within a family, and another names Asahel with "
  "the note that his son succeeded him, which is the Chronicler quietly acknowledging that Asahel "
  "died young."),
 ("The Twelve Monthly Courses", "The Rulers of the Tribes (vv.16-24)",
  "The tribal princes are listed, and two omissions in the list are conspicuous: Gad and Asher are "
  "absent, and the Chronicler offers no explanation. Then the census of chapter 21 is returned to, "
  "and the note about it is unusually candid. David took not the number of them from twenty years "
  "old and under, because the LORD had said he would increase Israel like to the stars. Joab began "
  "to number, and finished not, because there fell wrath for it against Israel, neither was the "
  "number put in the account of the chronicles of king David. An official record admitting that a "
  "record was deliberately left incomplete."),
 ("The Rulers of the Tribes", "The Stewards of the King's Substance (vv.25-34)",
  "Ten verses on estate management, and they are the closest thing in scripture to an inventory of "
  "a royal economy: officers over the treasures, the storehouses in the fields, the cities and "
  "villages, the tillage, the vineyards, the wine cellars, the olive trees, the sycomore trees, "
  "the herds in Sharon, the camels, the asses and the flocks. Each has a named man over it, and "
  "two of them are foreigners. Then the counsellors, Ahithophel and Hushai, and Joab last, general "
  "of the king's army."),
],
"1chronicles28": [
 ("", "David Stands Up and Speaks (vv.1-8)",
  "The whole administration of the previous five chapters is assembled, princes, officers, "
  "captains, stewards and mighty men, and the Chronicler notes that David stood up upon his feet, "
  "which for a man described as old and full of days is a detail with effort in it. The speech "
  "repeats the refusal and the reason, thou shalt not build an house for my name, because thou "
  "hast been a man of war, and hast shed blood, and then recounts the choosings: Judah out of the "
  "tribes, his father's house out of Judah, himself out of his father's sons, and Solomon out of "
  "his own. The charge to the assembly is conditional, keep and seek for all the commandments, "
  "that ye may possess this good land."),
 ("David Stands Up and Speaks", "Know Thou the God of Thy Father (vv.9-10)",
  "Two verses addressed to Solomon in front of everyone, and they are the sharpest thing David "
  "says in Chronicles. Know thou the God of thy father, and serve him with a perfect heart and "
  "with a willing mind, for the LORD searcheth all hearts, and understandeth all the imaginations. "
  "Then both outcomes stated without softening, if thou seek him, he will be found of thee, but if "
  "thou forsake him, he will cast thee off for ever. And the instruction that follows is simply, "
  "be strong, and do it."),
 ("Know Thou the God of Thy Father", "The Pattern Given by the Spirit (vv.11-21)",
  "David hands over the plans, and the Chronicler describes their origin in a way that puts them "
  "beside the tabernacle in Exodus: all this, said David, the LORD made me understand by writing "
  "by his hand upon me, and the pattern of all that he had by the spirit. The specifications run "
  "to weights, the candlesticks and their lamps, the tables of shewbread, the fleshhooks, the "
  "basons, the golden chariot of the cherubims. Then the closing encouragement, which admits the "
  "size of the task before promising help, be strong and of good courage, and do it, fear not, nor "
  "be dismayed, for the LORD God, even my God, will be with thee, he will not fail thee."),
],
"1chronicles29": [
 ("", "The Willing Offering (vv.1-9)",
  "David makes his own contribution first and describes it as personal rather than royal, because "
  "I have set my affection to the house of my God, I have of mine own proper good given to the "
  "house of my God. The figures are enormous, three thousand talents of gold and seven thousand of "
  "silver. Then the question put to the room, who then is willing to consecrate his service this "
  "day unto the LORD? and the response is itemised by group. The Chronicler's note on the mood is "
  "repeated three times in one verse, they offered willingly, with perfect heart they offered "
  "willingly, and the people rejoiced, for that they offered willingly."),
 ("The Willing Offering", "Blessed Be Thou, LORD God of Israel (vv.10-19)",
  "The prayer is the last thing David says in Chronicles and its argument is that nothing given was "
  "ever theirs. All that is in the heaven and in the earth is thine, both riches and honour come of "
  "thee, and in thine hand is power and might. Then the sentence that undercuts the entire "
  "collection just taken, all things come of thee, and of thine own have we given thee. The "
  "self-description is bleak and unembarrassed, for we are strangers before thee, and sojourners, "
  "as were all our fathers, our days on the earth are as a shadow, and there is none abiding. The "
  "closing petition is for his son's inward state rather than for the building, give unto Solomon "
  "my son a perfect heart."),
 ("Blessed Be Thou, LORD God of Israel", "Solomon Made King, and David's Death (vv.20-30)",
  "The assembly blesses the LORD and bows down, and the sacrifices are counted, a thousand "
  "bullocks, a thousand rams, a thousand lambs. Solomon is anointed and the Chronicler describes "
  "the succession as untroubled, all the princes and the mighty men, and all the sons likewise of "
  "king David, submitted themselves unto Solomon the king. Adonijah's attempt on the throne is not "
  "mentioned. David's death is given in the formula used of the good kings, he died in a good old "
  "age, full of days, riches, and honour, and the book closes by naming its sources, the book of "
  "Samuel the seer, the book of Nathan the prophet, and the book of Gad the seer."),
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


def verify(planned):
    """Apply the audit's checks to the planned HTML without writing it.

    The tree is shared with another session, so nothing can be written yet and the
    usual write-then-audit sequence is unavailable. Running the same rules against
    the strings in memory is what makes --check worth anything here.
    """
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import audit_authorship as A
    found = []
    for path, html in planned.items():
        page = os.path.basename(path)[:-5]
        nums = {int(x) for x in re.findall(r'class="verse-num"[^>]*>(\d+)', html)}
        total = max(nums) if nums else 0
        labels = [H.unescape(x).strip() for x in A.LABEL.findall(
            A.PANE.search(html).group(2))]
        secs = [(l, A.TAIL.search(l)) for l in labels]
        secs = [(l, m.group(1)) for l, m in secs if m]
        covered, repeated, starts = set(), set(), []
        for label, spec in secs:
            got = A.halves(spec)
            repeated |= got & covered
            covered |= got
            starts.append(min(v for v, _ in got) if got else 0)
            if total and max(v for v, _ in got) > total:
                found.append(f"{page}: {label!r} runs past verse {total}")
        want = {(v, h) for v in range(1, total + 1) for h in ("a", "b")}
        missing = sorted({v for v, _ in (want - covered)})
        if missing:
            found.append(f"{page}: verses uncovered {missing}")
        if repeated:
            found.append(f"{page}: described twice {sorted({v for v, _ in repeated})}")
        if starts != sorted(starts):
            found.append(f"{page}: sections out of verse order")
        for label in labels:
            fault = A.label_fault(label)
            if fault:
                found.append(f"{page}: label {fault}: {label!r}")
            stray = sorted({w for w in A.CAPS.findall(label) if w not in A.CAPS_OK})
            if stray and A.TAIL.search(label):
                found.append(f"{page}: capitals {stray} in {label!r}")
    return found


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
        d_open = (len(re.findall(r"<div\b", new_body))
                  - len(re.findall(r"<div\b", pane.group(2))))
        d_close = (len(re.findall(r"</div>", new_body))
                   - len(re.findall(r"</div>", pane.group(2))))
        if d_open != d_close:
            problems.append(f"{page}: pane gains {d_open} opens, {d_close} closes")
        planned[path] = html[:pane.start(2)] + new_body + html[pane.end(2):]
    problems += verify(planned)
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
