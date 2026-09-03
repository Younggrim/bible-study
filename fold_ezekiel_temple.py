#!/usr/bin/env python3
"""
Ezekiel 40 to 48: the temple vision. Nine pages, 260 verses.

ezekiel40 has no sublist and its sections are written from scratch. The other eight have
gapless outlines and are folded, including ezekiel41's, which splits at a half verse,
13-15a and 15b-21, and the halves are kept because the text divides there.

Two one-off inherited fields are dropped and their substance folded into the sections
that cover the verses they describe. ezekiel41's Notable field observes that the guide
measures the most holy place and Ezekiel is not said to enter it, which belongs in the
section on verses 3 and 4. ezekiel48's item labelled The positioning matters explains why
Judah sits immediately north of the sanctuary and Benjamin immediately south, which
belongs in the section on verses 1 to 7. Neither field appears anywhere else in the
corpus, and a field that occurs on one page out of 1189 is an inconsistency rather than a
feature.

The purpose of the survey is stated inside it, at 43:10-12: shew the house to the house of
Israel, that they may be ashamed of their iniquities, and let them measure the pattern.
Whether the measurements were ever meant to be built from has been argued for two
thousand years, and the sections say so where it matters rather than choosing a side.

Usage:
    python3 fold_ezekiel_temple.py [--check]
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
KEEP = ("Author:", "Date:", "Classification:", "Key Themes:", "Historical Context:")
REPAIRS = {}

SECTIONS = {
"ezekiel40": [
 ("The Date, the Mountain and the Man with the Line (vv.1-4)",
  "The date is given three ways, the five and twentieth year of our captivity, the tenth day of the "
  "month, and the fourteenth year after that the city was smitten, which places it in 573 BC, twelve "
  "and a half years after the fall and twenty years after the vision by the Chebar. He is brought in "
  "the visions of God into the land of Israel and set upon a very high mountain, with what looked "
  "like the frame of a city on it. The guide is described before the tour begins, a man whose "
  "appearance was like the appearance of brass, with a line of flax in his hand and a measuring reed. "
  "And the prophet's role for the next nine chapters is set out in advance, behold with thine eyes, "
  "and hear with thine ears, and declare all that thou seest to the house of Israel. He watches "
  "someone else measure, and reports numbers."),
 ("The Wall, and the East Gate (vv.5-16)",
  "The survey starts at the perimeter and establishes its unit before anything else, the measuring "
  "reed of six cubits long by the cubit and an hand breadth, that is, the long cubit of roughly "
  "twenty-one inches rather than the ordinary one. Then the east gate, and it gets more detail than "
  "any other feature in the complex: the steps, the threshold, the little chambers on either side, "
  "the posts, the porch, the narrow windows and the palm trees carved on the posts. The "
  "disproportion is not accidental. The east gate is the one the glory left by in chapter 10, and it "
  "is the one it comes back through in chapter 43."),
 ("The Outer Court, and the North and South Gates (vv.17-27)",
  "The outer court has a pavement running round it with thirty chambers upon it. Then the north gate "
  "is measured and reported to be the same as the east, and the south gate is measured and reported "
  "to be the same again, with their arches, chambers, posts and palm trees, and seven steps up to "
  "each. Reading three near-identical paragraphs is what a survey feels like, and the point being "
  "made by the repetition is that the numbers agree: this is a structure with no irregularities in "
  "it."),
 ("The Inner Court Gates (vv.28-37)",
  "The same three gates are then measured on the inner side, south, east and north, and each one is "
  "recorded as being according to these measures. One number changes, and it is the one worth "
  "noticing: eight steps instead of seven. The complex rises as it moves inward, so approaching the "
  "sanctuary is physically an ascent, and the gradient is built into the architecture rather than "
  "described in a sermon."),
 ("The Tables for Slaughtering (vv.38-43)",
  "The vision includes the working equipment. Chambers and entries by the posts of the gates, where "
  "they washed the burnt offering. Eight tables whereupon they slew their sacrifices, four on one "
  "side and four on the other. And the fittings, hooks, an hand broad, fastened round about within. "
  "A description of holiness that specifies where the carcases were rinsed and what the meat was "
  "hung on is making a claim about what holiness involves."),
 ("The Chambers for the Singers, and the Porch (vv.44-49)",
  "Chambers in the inner court for the singers, and two more for the priests, one set over the "
  "charge of the house and one over the charge of the altar, and the second is identified by family, "
  "the sons of Zadok, which anticipates the reorganisation of chapter 44. The inner court is a "
  "hundred cubits square with the altar standing in front of the house. Then the porch of the house "
  "itself, with pillars by the posts and eight steps to go up. The tour has reached the door and "
  "chapter 41 goes inside."),
],
"ezekiel41": [
 ("The Vestibule of the Temple Proper (vv.1-2)",
  "The guide brings him to the temple and measures the posts and the breadth of the door and the "
  "sides of the door, and then the length and breadth of the holy place, forty cubits by twenty. The "
  "figures match the dimensions of Solomon's temple in 1 Kings 6 closely enough that the reader is "
  "meant to recognise the building even though nothing else in this vision corresponds to it."),
 ("The Most Holy Place Measured, and Not Entered (vv.3-4)",
  "Then went he inward, and measured, twenty cubits by twenty, and said unto me, This is the most "
  "holy place. Two words in that sentence do the work. He measured. The guide goes in and the prophet "
  "does not; nothing in the text says Ezekiel crossed that threshold, and the narration stays outside "
  "with him. Even in a vision, where no priestly rule could physically be broken, the boundary is "
  "kept. The measurements are reported at second hand, which is exactly how a priest would want them "
  "reported."),
 ("The Side Chambers, in Three Stories (vv.5-11)",
  "The wall of the house is measured, then the side chambers built against it, thirty of them in "
  "three storeys, and the construction detail given is that the wall narrows as it rises so each "
  "storey is wider than the one below, and the beams rest on the ledges rather than being let into "
  "the wall itself. Nothing is fastened into the sanctuary wall. That is a structural fact and it "
  "reads as a deliberate one in a book this concerned with separation."),
 ("The Building on the West (v.12)",
  "One verse for a structure the vision names but does not explain, the building that was before the "
  "separate place at the end toward the west, seventy cubits broad with a wall five cubits thick. Its "
  "function is never given. An honest note says so rather than inventing a use for it."),
 ("The Overall Measurements (vv.13-15a)",
  "The totals are then taken, a hundred cubits for the house, and a hundred for the separate place "
  "with the building and its walls. The section breaks in the middle of verse 15, which is why the "
  "range is written as 13 to 15a: the first half of the verse finishes the arithmetic and the second "
  "half starts on the decoration."),
 ("Cherubim and Palm Trees on Every Wall (vv.15b-21)",
  "The interior is panelled with wood and carved throughout, and the pattern is given exactly, a "
  "cherub and a palm tree, so that a palm tree was between a cherub and a cherub, alternating all "
  "the way round. Then a detail worth comparing with chapter 1: and every cherub had two faces, the "
  "face of a man toward the palm tree on the one side, and the face of a young lion toward the palm "
  "tree on the other side. The creatures by the Chebar had four faces each. These carvings have two, "
  "which is what a flat relief can show."),
 ("The Wooden Altar Called the Table Before the LORD (v.22)",
  "The altar was of wood, three cubits high and two broad, and the corners and the length and the "
  "walls of it were of wood, and he said unto me, This is the table that is before the LORD. It is "
  "the only piece of furniture named inside the house in the whole vision, and it is called both an "
  "altar and a table. What is absent is more striking: no lampstand, no shewbread, no veil described "
  "as torn or intact, and in all nine chapters no ark of the covenant anywhere."),
 ("The Double Doors (vv.23-26)",
  "The temple and the sanctuary each have two doors, and the doors have two leaves apiece, two "
  "turning leaves for the one door and two for the other. The carving of the walls is carried onto "
  "them, cherubims and palm trees, like as were made upon the walls, so the decoration does not stop "
  "at the doorway. And thick planks upon the face of the porch without. The chapter ends with the "
  "carpentry, which is where a measured survey of a house should end."),
],
"ezekiel42": [
 ("The Chambers on the North (vv.1-9)",
  "The tour moves out into the utter court and measures a block of chambers on the north side, in "
  "three storeys with a walk before them, and the upper chambers shorter than the lower because the "
  "galleries take space from them. The description is dense and hard to follow on a first reading, "
  "and it is worth knowing why the detail is being recorded at all: verses 13 and 14 will explain "
  "the function, and the function is the point of the whole block."),
 ("The Chambers on the South (vv.10-12)",
  "The matching block on the south side, with a door at the head of the way and an entrance "
  "corresponding to the northern one. Three verses where the north took nine, because the survey has "
  "already established the pattern and only needs to record that it repeats."),
 ("What the Chambers Are For (vv.13-14)",
  "Two verses that explain the architecture of the last three chapters. There the priests that "
  "approach unto the LORD shall eat the most holy things, and there they shall lay the most holy "
  "things. Then the rule about movement, and it is the reason the rooms exist: when the priests enter "
  "therein, they shall not go out of the holy place into the utter court, but there they shall lay "
  "their garments wherein they minister, for they are holy, and shall put on other garments, and "
  "shall approach to that which appertaineth to the people. It is a changing room, and its purpose is "
  "to stop holiness being carried out into ordinary space by accident."),
 ("The Outer Dimensions, and the Wall Between (vv.15-20)",
  "The guide takes the whole complex from the outside, five hundred by five hundred, squared, with a "
  "wall round about. The last clause of the chapter is the vision's own summary of what it has been "
  "measuring for, to make a separation between the sanctuary and the profane place. Every dimension "
  "in these chapters is in service of that sentence."),
],
"ezekiel43": [
 ("The Glory Returns from the East (vv.1-5)",
  "Behold, the glory of the God of Israel came from the way of the east, and his voice was like a "
  "noise of many waters, and the earth shined with his glory. The prophet identifies it himself, and "
  "his cross-reference is exact, it was according to the vision that I saw when I came to destroy the "
  "city, and according to the vision that I saw by the river Chebar. Then the direction of travel, "
  "and the glory of the LORD came into the house by the way of the gate whose prospect is toward the "
  "east. Chapters 9 to 11 tracked the departure in three stages, threshold, east gate, mountain. It "
  "returns by the same route in reverse."),
 ("This Is My Throne, and My Holy Name (vv.6-9)",
  "Son of man, the place of my throne, and the place of the soles of my feet, where I will dwell in "
  "the midst of the children of Israel for ever. The offence that had to be cleared away is described "
  "as a matter of distance rather than of doctrine, they have set their threshold by my threshold, and "
  "their post by my post, and there was but a wall between me and them. The palace and the temple had "
  "shared a wall, and the royal graves were on the other side of it. Now let them put away their "
  "whoredom, and the carcases of their kings, far from me, and I will dwell in the midst of them for "
  "ever."),
 ("Show the House to Israel, That They May Be Ashamed (vv.10-12)",
  "This is the purpose statement for the entire survey and it is easy to miss in the middle of the "
  "measurements. Shew the house to the house of Israel, that they may be ashamed of their iniquities, "
  "and let them measure the pattern. The order is worth following: seeing the dimensions is expected "
  "to produce shame, and only then, if they be ashamed of all that they have done, shew them the form "
  "of the house. A measurable description of holiness is being offered to people who need to see the "
  "difference between it and what they had. And the summary, this is the law of the house, most holy."),
 ("The Altar Measured (vv.13-17)",
  "The altar is given its own paragraph and its own units, the bottom, the settle, the greater settle, "
  "the border round about and the four horns, rising in stages like a stepped tower. The stairs face "
  "east, which puts the officiating priest with his back to the rising sun and his face to the house, "
  "the exact reverse of the twenty-five men at 8:16."),
 ("Seven Days to Consecrate the Altar (vv.18-27)",
  "The consecration is set out as a procedure: a young bullock for a sin offering, blood put on the "
  "four horns and on the four corners of the settle and upon the border, the carcase burnt outside "
  "the sanctuary, then a kid of the goats daily for seven days, with a bullock and a ram. And on the "
  "eighth day and so forward the regular offerings begin, and I will accept you, saith the Lord GOD. "
  "It is worth being plain about what these chapters are doing here: a full sacrificial system is "
  "being restored in operational detail. Readers have taken that three ways, as a literal blueprint "
  "for a temple still to be built, as an idealised pattern never intended for construction, and as a "
  "symbolic description of later worship. The text supplies measurements and a procedure and does not "
  "supply an interpretation, and a note that pretends otherwise is adding something."),
],
"ezekiel44": [
 ("The East Gate Shut for Good (vv.1-3)",
  "This gate shall be shut, it shall not be opened, and no man shall enter in by it, and the reason "
  "given is the event of the previous chapter, because the LORD, the God of Israel, hath entered in by "
  "it. A door is used once and then sealed. The one exception is the prince, who may sit in it to eat "
  "bread, entering by the porch and going out the same way, so even he does not pass through."),
 ("No Stranger in the Sanctuary (vv.4-9)",
  "O ye house of Israel, let it suffice you of all your abominations, in that ye have brought into my "
  "sanctuary strangers, uncircumcised in heart and uncircumcised in flesh. The charge is about staffing "
  "the sanctuary with people who had no business in it, and the summary is administrative, ye have not "
  "kept the charge of mine holy things, but ye have set keepers of my charge in my sanctuary for "
  "yourselves. Read beside 47:22, which grants resident foreigners a share in the land, this verse is "
  "about the sanctuary specifically and not about belonging generally."),
 ("The Levites Demoted (vv.10-14)",
  "The Levites that are gone away far from me, when Israel went astray, they shall bear their "
  "iniquity. The sentence keeps them in employment and reduces the employment: they shall be ministers "
  "in it, keepers of the charge of the house, they shall slay the burnt offering and the sacrifice for "
  "the people, but they shall not come near unto me, to do the office of a priest. The carefully "
  "organised courses of 1 Chronicles 23 to 26 become gatekeeping and butchery, and the stated cause is "
  "service at the high places."),
 ("The Sons of Zadok (vv.15-16)",
  "But the priests the Levites, the sons of Zadok, that kept the charge of my sanctuary when the "
  "children of Israel went astray from me, they shall come near to me to minister unto me. Zadok was "
  "the priest who backed Solomon at the succession and whose line held the high priesthood through "
  "the monarchy. The reorganisation described here is not only theological: the second temple "
  "priesthood did operate with a distinction of this kind, and Ezekiel is the text it is argued from."),
 ("Linen, Marriage and Conduct (vv.17-27)",
  "The regulations are practical and specific. Linen garments in the inner court and no wool, and the "
  "reason given is sweat. The ministering clothes left in the holy chambers before going out to the "
  "people. Hair neither shaved nor left long but polled. No wine before entering the inner court. "
  "Marriage restricted to a virgin of Israel or a priest's widow. Rules about contact with the dead "
  "and seven days of cleansing after. And in the middle of the list, the duty whose neglect was the "
  "charge against the priests at 22:26, they shall teach my people the difference between the holy and "
  "profane, and cause them to discern between the unclean and the clean."),
 ("The Priests' Inheritance (vv.28-31)",
  "And it shall be unto them for an inheritance, I am their inheritance, and ye shall give them no "
  "possession in Israel, I am their possession. The arrangement is the one Numbers 18 sets out and it "
  "is restated here as part of the new order: the priests hold no land, and they live on the "
  "offerings, the meat offering, the sin offering, the trespass offering, every dedicated thing and "
  "the first of all the firstfruits. The last verse adds a prohibition that applies to them as it does "
  "to everyone, on eating anything torn or that died of itself."),
],
"ezekiel45": [
 ("The Holy Portion of the Land (vv.1-6)",
  "The allocation begins with an oblation set aside before anyone else is given anything, five and "
  "twenty thousand reeds long by ten thousand broad, holy in all the borders thereof. Inside it, a "
  "portion for the priests with the sanctuary in the middle, a portion for the Levites, and a strip "
  "five thousand by twenty-five thousand for the city, which the text says shall be for the whole "
  "house of Israel. The land is being laid out from the sanctuary outward rather than from the "
  "borders in."),
 ("The Prince's Portion (vv.7-8)",
  "And a portion shall be for the prince on the one side and on the other side of the oblation. The "
  "reason given is not honour but restraint, and my princes shall no more oppress my people, and the "
  "rest of the land shall they give to the house of Israel by their tribes. A fixed land grant is "
  "being used as a structural cure for royal expropriation, which is the abuse Samuel warned about "
  "when Israel asked for a king and the one Ahab demonstrated on Naboth's vineyard."),
 ("Just Weights (vv.9-12)",
  "Let it suffice you, O princes of Israel, remove violence and spoil, and execute judgment and "
  "justice, take away your exactions from my people. Then the requirement, ye shall have just "
  "balances, and a just ephah, and a just bath, followed by an actual conversion table, the ephah and "
  "the bath of one measure, the shekel of twenty gerahs. It is the one place in these nine chapters "
  "where the measuring reed is put down and commercial measures are picked up, and the transition is "
  "not a change of subject: the same word covers both."),
 ("The Offerings Brought to the Prince (vv.13-17)",
  "The people's contribution is specified as fractions, a sixth part of an ephah from a homer of "
  "wheat and of barley, a tenth part of a bath of oil, one lamb out of two hundred. And what the "
  "prince does with it is specified too, it shall be the prince's part to give the burnt offerings "
  "and the meat offerings and the drink offerings in the feasts, and he shall prepare the sin "
  "offering to make reconciliation for the house of Israel. The tax is collected upward and spent "
  "outward, which is the reverse of the arrangement the chapter opened by prohibiting."),
 ("Passover and Tabernacles (vv.18-25)",
  "The calendar given here is short and does not match the one in Leviticus 23. The first day of the "
  "first month for cleansing the sanctuary, the seventh day for everyone who erred through ignorance, "
  "the fourteenth day for the passover and seven days of unleavened bread, and in the seventh month, "
  "on the fifteenth day, seven days more according to the same rite. What is missing is conspicuous: "
  "no day of atonement, no feast of weeks, and offerings that differ in quantity from the ones Numbers "
  "28 and 29 prescribe. These divergences are among the reasons rabbinic tradition found the book "
  "difficult enough to discuss whether it belonged in the canon, and they remain one of the standing "
  "puzzles of these chapters."),
],
"ezekiel46": [
 ("The Inner East Gate Opened on Sabbaths (vv.1-3)",
  "The gate of the inner court that looketh toward the east shall be shut the six working days, but "
  "on the sabbath it shall be opened, and in the day of the new moon it shall be opened. The prince "
  "worships at the threshold of it and the people worship at the door of that gate before the LORD. "
  "The arrangement gives the ordinary worshipper a sight line into the inner court without an entry, "
  "which is how this vision usually solves the problem of access."),
 ("The Prince's Offerings (vv.4-8)",
  "The sabbath offering is six lambs without blemish and a ram, with an ephah of flour to the ram and "
  "as much as he is able to give with the lambs, and a hin of oil to an ephah. The new moon is a "
  "young bullock, six lambs and a ram. The prince's route is specified as carefully as his offering, "
  "he shall enter by the way of the porch of that gate, and he shall go forth by the way thereof, so "
  "he goes out the way he came in, unlike the people in the next section."),
 ("In at One Gate, Out at the Other (vv.9-10)",
  "He that entereth in by the way of the north gate to worship shall go out by the way of the south "
  "gate, and he that entereth by the way of the south gate shall go forth by the way of the north "
  "gate, he shall not return by the way of the gate whereby he came in, but shall go forth over "
  "against it. It is a one-way circulation plan for a crowd, and it is the most practical detail in "
  "the whole vision. The prince is placed inside the flow rather than above it, and the prince in the "
  "midst of them, when they go in, shall go in, and when they go forth, shall go forth."),
 ("Feast and Freewill Offerings (vv.11-12)",
  "In the feasts the meat offering is an ephah to a bullock and an ephah to a ram, and with the lambs "
  "as he is able. Then a provision for offerings outside the calendar, when the prince shall prepare a "
  "voluntary burnt offering, one shall open him the gate that looketh toward the east, and after he "
  "has gone out the gate shall be shut again. The east gate opens for a freewill offering and closes "
  "behind it."),
 ("The Daily Morning Lamb (vv.13-15)",
  "Thou shalt daily prepare a burnt offering unto the LORD of a lamb of the first year without "
  "blemish, thou shalt prepare it every morning, with a meat offering of the sixth part of an ephah "
  "and the third part of a hin of oil. And the closing clause makes it the baseline of the whole "
  "system, they shall prepare the lamb, and the meat offering, and the oil, every morning for a "
  "continual burnt offering. Every other offering in these chapters is occasional. This one is what "
  "the days are made of."),
 ("The Prince May Not Take an Inheritance (vv.16-18)",
  "The inheritance rules are stated as two cases. A gift from the prince to one of his sons stays with "
  "the son. A gift to a servant returns to the prince at the year of liberty. And then the "
  "prohibition the pair of cases exists to frame, moreover the prince shall not take of the people's "
  "inheritance by oppression, to thrust them out of their possession. Naboth's vineyard, legislated "
  "against directly, in a chapter otherwise concerned with lambs and flour."),
 ("The Boiling Places (vv.19-24)",
  "The survey ends in the kitchens. There is a place at the back of the priests' chambers where they "
  "shall boil the trespass offering and the sin offering and bake the meat offering, and the reason is "
  "given, that they bear them not out into the utter court, to sanctify the people. Then four courts "
  "in the four corners of the outer court, each with its own boiling places, for the ministers of the "
  "house to boil the sacrifice of the people. Two sets of kitchens, kept apart. After forty chapters "
  "of glory and judgment, the vision's last architectural concern is where the meat is cooked, and it "
  "is the same concern as everywhere else: keeping the holy and the ordinary from mixing by accident."),
],
"ezekiel47": [
 ("The Water from Under the Threshold (vv.1-2)",
  "Behold, waters issued out from under the threshold of the house eastward, and ran down from under "
  "the right side of the house, at the south side of the altar. The source is the building that has "
  "just been measured for eight chapters, and the water comes out from under the door of it. Then he "
  "is taken round to the outside of the east gate, which is shut, and the water is running past it on "
  "the right side."),
 ("Ankles, Knees, Loins, and Then Swimming (vv.3-5)",
  "The guide measures a thousand cubits and leads him through, and the water is to the ankles. A "
  "thousand more, to the knees. A thousand more, to the loins. A thousand more, and it was a river "
  "that I could not pass over, for the waters were risen, waters to swim in. The detail that matters "
  "is what is not mentioned: no tributary joins it anywhere. A stream that quadruples in depth over "
  "four thousand cubits with nothing feeding it is not a river being described, it is a river being "
  "used to say something."),
 ("Everything Lives Where the River Goes (vv.6-10)",
  "The river runs east into the desert and into the sea, and the effect is stated as a rule, every "
  "thing that liveth, which moveth, whithersoever the rivers shall come, shall live, and the waters "
  "shall be healed. The specificity is what makes it concrete: fishermen will stand from En-gedi to "
  "En-eglaim, and their fish shall be according to their kinds, as the fish of the great sea, "
  "exceeding many. The Dead Sea is about a third salt by weight and holds no fish at all, so the "
  "healing named here is a particular and identifiable reversal rather than a general improvement."),
 ("The Marshes Left Salt (v.11)",
  "One verse declines to make the picture total, but the miry places thereof and the marishes thereof "
  "shall not be healed, they shall be given to salt. The usual practical reading is that salt "
  "production had to continue somewhere, since salt was a necessity and the region's supply came from "
  "exactly those flats. Whatever the reason, the vision is precise enough to carve out an exception, "
  "and noticing the exception is part of reading it honestly."),
 ("Trees Whose Leaf Is Medicine (v.12)",
  "By the river upon the bank thereof shall grow all trees for meat, whose leaf shall not fade, "
  "neither shall the fruit thereof be consumed, it shall bring forth new fruit according to his "
  "months, and the fruit thereof shall be for meat, and the leaf thereof for medicine. Revelation 22 "
  "takes this verse, sets it beside the tree of life from Genesis 2, and puts both on the banks of a "
  "river coming out of a throne, and the leaves for the healing of the nations come from here."),
 ("The Borders of the Land (vv.13-20)",
  "The allocation begins, and the boundaries are traced point by point on all four sides, north from "
  "the great sea by Hethlon to Hamath and Hazar-hatticon, east between Damascus and Gilead down the "
  "Jordan to the east sea, south from Tamar to the waters of strife and the river to the great sea, "
  "and the west border the great sea itself. One clause governs the division, and ye shall divide it "
  "by lot, and Joseph shall have two portions, which keeps the count at twelve without Levi."),
 ("The Stranger Shall Have an Inheritance (vv.21-23)",
  "The last three verses of the chapter are the most surprising in these nine, and they should be "
  "read beside 44:9. The strangers that sojourn among you, which shall beget children among you, they "
  "shall be unto you as born in the country, and they shall have inheritance with you among the "
  "tribes of Israel, in what tribe the stranger sojourneth, there shall ye give him his inheritance. "
  "The sanctuary is closed to the foreigner and the land is opened to him. The book holds both, and "
  "it holds them three chapters apart without any sense of a difficulty."),
],
"ezekiel48": [
 ("Seven Tribes North of the Holy Portion (vv.1-7)",
  "The tribal allocation ignores the historical geography completely. Instead of the irregular "
  "territories of Joshua, every tribe gets a band running the full width of the land from the east "
  "side unto the west side, and the seven laid out north of the holy portion are Dan, Asher, "
  "Naphtali, Manasseh, Ephraim, Reuben and Judah, in that order. The positioning is the interesting "
  "part. Judah, the royal tribe, is put immediately north of the holy portion, and Benjamin, the "
  "tribe that stayed with the house of David, immediately south of it, so the two tribes that held "
  "together after the division flank the sanctuary. Joseph appears as Ephraim and Manasseh, which "
  "keeps the number at twelve while Levi is provided for separately inside the holy portion."),
 ("The Holy Portion, the City, and the Prince's Land (vv.8-22)",
  "The middle band is the oblation of chapter 45 set out again with its internal divisions: the "
  "priests' portion with the sanctuary in the midst of it, the Levites' portion beside it, and the "
  "profane place, five thousand by twenty-five thousand, for the city and its suburbs and its "
  "farmland. The city is described in terms of who works it, and they that serve the city shall serve "
  "it out of all the tribes of Israel, and its produce feeds them. The prince's land lies on both "
  "sides of the whole block. The city is deliberately not the sanctuary and is deliberately not "
  "assigned to a tribe, which is the arrangement the last verse of the book will comment on."),
 ("Five Tribes South of the Holy Portion (vv.23-29)",
  "Benjamin, Simeon, Issachar, Zebulun and Gad, each in a band from the east side unto the west side, "
  "and then the summary, this is the land which ye shall divide by lot unto the tribes of Israel for "
  "inheritance. Twelve equal strips and one holy portion, with no allowance made for terrain, "
  "fertility, coastline or where anybody actually used to live. The plan is symmetrical because it is "
  "making a point about order rather than proposing a survey."),
 ("Twelve Gates, Named for the Tribes (vv.30-34)",
  "The city has three gates on each of its four sides, twelve in all, and each is named for a tribe. "
  "The list here is not identical to the list of land portions: Levi and Joseph both appear as gates, "
  "where in the land division Levi held the holy portion and Joseph was split into Ephraim and "
  "Manasseh. Everyone gets a door whether or not they got a field. Revelation 21 gives the new "
  "Jerusalem exactly this arrangement, twelve gates with the names of the twelve tribes, three on "
  "each side."),
 ("The Name of the City, The LORD Is There (v.35)",
  "The perimeter is given, eighteen thousand measures round about, and then the last line of the "
  "book, and the name of the city from that day shall be, The LORD is there. In Hebrew it is two "
  "words, and it is a name rather than a description. Set against the beginning of the book it is the "
  "whole argument in one phrase: the elders in the dark room at 8:12 said the LORD hath forsaken the "
  "earth, the glory left by the east gate in chapter 11, and the last thing the book does is put the "
  "presence into the city's name. Note also what the name is not. It is not the temple that is called "
  "this, and the sanctuary sits outside the city in this plan. It is the city."),
],
}


def verify(planned):
    """Run the audit's own checks against the planned HTML, without writing it."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import audit_authorship as A
    found = []
    for path, html in planned.items():
        page = os.path.basename(path)[:-5]
        nums = {int(x) for x in re.findall(r'class="verse-num"[^>]*>(\d+)', html)}
        total = max(nums) if nums else 0
        pane = A.PANE.search(html).group(2)
        labels = [H.unescape(x).strip() for x in A.LABEL.findall(pane)]
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
            found.append(f"{page}: verses described twice "
                         f"{sorted({v for v, _ in repeated})}")
        if starts != sorted(starts):
            found.append(f"{page}: sections out of verse order")
        if "<li>" in pane or "auth-sublist" in pane:
            found.append(f"{page}: sublist survived the fold")
        for label in labels:
            fault = A.label_fault(label)
            if fault:
                found.append(f"{page}: label {fault}: {label!r}")
            stray = sorted({w for w in A.CAPS.findall(label)
                            if w not in A.CAPS_OK})
            if stray and A.TAIL.search(label):
                found.append(f"{page}: capitals {stray} in {label!r}")
    return found


def main():
    check = "--check" in sys.argv
    planned, problems, notes = {}, [], []
    for page, sections in SECTIONS.items():
        path = os.path.join(DOCS, page + ".html")
        html = open(path, encoding="utf-8").read()
        pane = PANE.search(html)
        if not pane:
            problems.append(f"{page}: no authorship pane")
            continue
        body_html = pane.group(2)
        found = [H.unescape(l).strip() for l, _ in ITEM_RE.findall(body_html)]
        keep = [[l, b.strip()] for l, b in ITEM_RE.findall(body_html)
                if H.unescape(l).strip() in KEEP]
        if not keep:
            problems.append(f"{page}: no book fields found to preserve")
            continue
        for label in found:
            if label not in KEEP:
                notes.append(f"{page}: dropped one-off item {label!r}, "
                             f"its content is folded into the sections")
        for i, (label, body) in enumerate(keep):
            for old, new in REPAIRS.get(page, []):
                if old in body:
                    keep[i][1] = body = body.replace(old, new)
                    notes.append(f"{page}: repaired {old!r} in {label}")
        parts = ["\n                <h3>Authorship &amp; Background</h3>\n"]
        for label, body in keep:
            parts.append(ITEM.format(label=label, body=body) + "\n")
        notes.append(f"{page}: kept {len(keep)} book field(s)")
        for label, prose in sections:
            parts.append(ITEM.format(label=label + ":", body=prose) + "\n")
            notes.append(f"{page}: {label}")
        new_body = "".join(parts) + "            </div>\n\n            "
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
    print(f"{'would fold' if check else 'folded'} {len(planned)} pages, "
          f"{sum(len(v) for v in SECTIONS.values())} section(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
