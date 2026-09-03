#!/usr/bin/env python3
"""
The gazetteer behind the Map & Geography maps.

Every place the Map & Geography panes mention and that can be located with
reasonable confidence lives here: where it is, what it is now, and a couple of
sentences of context. `build_mapgeo.py` compiles this into
`docs/site/mapgeo.js`, which draws the pins and shows the notes.

This replaced a bare Wikipedia link. A reader who did not already know where
Nineveh was got a link that took them off the page; now the map shows it on the
Tigris opposite modern Mosul, 500 miles from Israel, which is the fact the
verse is actually leaning on.

Fields
------
name     what the pin is labelled, using the biblical name where the pages do
lat/lon  decimal degrees, north and east positive
kind     city | region | water | river | mountain | island, drives the marker
modern   present-day location, or "" for regions with no single modern place
note     the write-up, one to three sentences, geography first
wiki     Wikipedia article title, kept as a secondary "read more" link
aka      extra strings to match in the pane text, beyond `name`

On coordinates
--------------
Cities are placed on their excavated tell or traditional site. Regions and
bodies of water have no single point, so they are anchored somewhere
representative and the renderer draws them without a pin dot. Where a site is
genuinely disputed the note says so rather than the map implying precision it
does not have; Sodom, Emmaus, Ai, Gilgal, Derbe and Tarshish are the main ones.
"""

# --------------------------------------------------------------------------
# The 72 places the panes already linked to Wikipedia. Every one of these must
# stay present: build_mapgeo.py fails the build if a link target loses its
# entry, because that would silently drop a pin the prose still refers to.
# --------------------------------------------------------------------------
PLACES = {

"jerusalem": dict(
    name="Jerusalem", lat=31.7683, lon=35.2137, kind="city",
    modern="Jerusalem", wiki="Jerusalem",
    aka=["Zion", "Mount Zion", "City of David", "Salem"],
    note="A hill town about 2,500 feet up in the central spine of Judah, "
         "roughly 35 miles inland from the Mediterranean and 15 miles west of "
         "the Jordan. It sits on no trade route and has no river, which is why "
         "it mattered as a fortress and a sanctuary rather than as a market."),

"babylon": dict(
    name="Babylon", lat=32.5355, lon=44.4275, kind="city",
    modern="near Hillah, Iraq", wiki="Babylon",
    aka=["Babylonia", "Babylonian", "Babylonians", "Chaldea", "Shinar"],
    note="On the Euphrates about 55 miles south of modern Baghdad. Judah's "
         "exiles were marched roughly 900 miles to get here, the long way round "
         "the Arabian desert, which is why the journey took months and the "
         "return was a genuine undertaking rather than a short trip home."),

"egypt": dict(
    name="Egypt", lat=29.60, lon=31.20, kind="region",
    modern="Egypt", wiki="Ancient_Egypt",
    aka=["Ancient Egypt", "Mizraim", "Egyptian", "Egyptians"],
    note="A ribbon of irrigated land along the Nile, ending in the Delta where "
         "Israel settled in Goshen. Rain-fed Canaan depended on weather; Egypt "
         "depended on a river that flooded on schedule, which made it the place "
         "everyone went when the harvest failed."),

"jordan_river": dict(
    name="Jordan River", lat=32.10, lon=35.57, kind="river",
    modern="Israel / Jordan border", wiki="Jordan_River",
    aka=["Jordan", "the Jordan", "Jordan Valley"],
    note="Runs about 65 miles as the crow flies from the Sea of Galilee to the "
         "Dead Sea, dropping from 700 to 1,400 feet below sea level. Narrow "
         "enough to wade at most fords, it was still the boundary that divided "
         "wilderness from inheritance."),

"sinai": dict(
    name="Mount Sinai", lat=28.5392, lon=33.9750, kind="mountain",
    modern="Jebel Musa, Sinai Peninsula, Egypt", wiki="Mount_Sinai",
    aka=["Sinai", "Horeb", "Mount Horeb"],
    note="Traditionally Jebel Musa in the granite mountains of the southern "
         "Sinai peninsula, about 7,500 feet high. The identification dates from "
         "Christian monastic tradition rather than from the text, and other "
         "candidates have been proposed, but this has been the pilgrimage site "
         "since the fourth century."),

"samaria": dict(
    name="Samaria", lat=32.2804, lon=35.1969, kind="city",
    modern="Sebastia, West Bank", wiki="Samaria",
    aka=["Samaritan", "Samaritans"],
    note="Omri bought a bare hill and built a capital on it, which gave the "
         "northern kingdom a fortress with no prior claim on it, the same "
         "calculation David made with Jerusalem. It commands the pass west "
         "toward the coastal plain. The name later spread to the whole region "
         "between Galilee and Judea."),

"moab": dict(
    name="Moab", lat=31.45, lon=35.75, kind="region",
    modern="west-central Jordan", wiki="Moab",
    aka=["Moabite", "Moabites", "plains of Moab"],
    note="The plateau east of the Dead Sea, cut off from Israel by the "
         "rift valley and from Ammon by the Arnon gorge. High enough to farm "
         "grain, which is why Naomi's family went there in a famine."),

"assyria": dict(
    name="Assyria", lat=35.90, lon=43.20, kind="region",
    modern="northern Iraq", wiki="Assyria",
    aka=["Assyrian", "Assyrians", "Asshur"],
    note="The upper Tigris heartland around Nineveh, Calah and Asshur. Its "
         "armies reached Israel by following the Fertile Crescent north-west "
         "and then south down the coast, so the threat always arrived from the "
         "north even though Assyria lay to the east."),

"galilee": dict(
    name="Galilee", lat=32.85, lon=35.35, kind="region",
    modern="northern Israel", wiki="Galilee",
    aka=["Galilean", "Galileans"],
    note="The northern hill country above the Jezreel Valley, wetter and "
         "greener than Judah and crossed by the trade road to Damascus. That "
         "traffic is why Judeans considered it mixed and provincial, and why "
         "Jesus grew up hearing more than one language."),

"dead_sea": dict(
    name="Dead Sea", lat=31.50, lon=35.47, kind="water",
    modern="Israel / Jordan", wiki="Dead_Sea",
    aka=["Salt Sea", "Sea of the Arabah"],
    note="The lowest exposed ground on earth, about 1,400 feet below sea "
         "level, and roughly ten times saltier than the ocean because water "
         "leaves only by evaporation. Nothing lives in it, which is the image "
         "Ezekiel 47 overturns when he has it filled with fish."),

"sea_of_galilee": dict(
    name="Sea of Galilee", lat=32.8222, lon=35.5900, kind="water",
    modern="Lake Kinneret, Israel", wiki="Sea_of_Galilee",
    aka=["Lake of Gennesaret", "Sea of Tiberias", "Chinnereth", "Kinneret"],
    note="A freshwater lake 13 miles by 8, sunk 700 feet below sea level in a "
         "bowl of hills. Cold air spilling over the rim onto warm water is what "
         "produces the sudden violent squalls the Gospels keep describing."),

"hebron": dict(
    name="Hebron", lat=31.5326, lon=35.0954, kind="city",
    modern="Hebron, West Bank", wiki="Hebron",
    aka=["Kirjath-arba", "Kiriath-arba", "Mamre"],
    note="The highest town in the Judean hills at about 3,000 feet, 19 miles "
         "south of Jerusalem. Abraham bought a burial cave here, and David "
         "reigned from it for seven years before moving north, so it carries "
         "both the patriarchal and the royal claim to the land."),

"gilead": dict(
    name="Gilead", lat=32.30, lon=35.75, kind="region",
    modern="northern Jordan", wiki="Gilead",
    aka=["Gileadite", "Gileadites"],
    note="The wooded highlands east of the Jordan between the Yarmuk and the "
         "Arnon, good grazing country and a source of the resin traded as balm. "
         "Being across the river left its tribes perpetually worried about "
         "being written out of Israel."),

"damascus": dict(
    name="Damascus", lat=33.5131, lon=36.2919, kind="city",
    modern="Damascus, Syria", wiki="Damascus",
    aka=["Aram-Damascus"],
    note="An oasis city where the Barada river runs out of the Anti-Lebanon "
         "into the desert, about 135 miles north-east of Jerusalem. It sat "
         "astride the caravan roads to Mesopotamia and Arabia, which made Aram "
         "rich and made it Israel's most persistent northern rival."),

"canaan": dict(
    name="Canaan", lat=31.90, lon=35.05, kind="region",
    modern="Israel, West Bank, Lebanon", wiki="Canaan",
    aka=["Canaanite", "Canaanites", "Promised Land", "land of promise"],
    note="The land bridge between Egypt and Mesopotamia, which is why armies "
         "crossed it for three thousand years. Within about 60 miles it goes "
         "from coastal plain to hill country to rift valley to desert plateau, "
         "so control of it was always local and piecemeal."),

"nineveh": dict(
    name="Nineveh", lat=36.3594, lon=43.1528, kind="city",
    modern="Mosul, Iraq", wiki="Nineveh",
    aka=[],
    note="Assyria's last capital, on the east bank of the Tigris across from "
         "modern Mosul, about 500 miles north-east of Israel. Sennacherib "
         "walled in an enormous city here, which is the scale behind Jonah's "
         "three days' journey and its 120,000 who cannot tell right from left."),

"jericho": dict(
    name="Jericho", lat=31.8711, lon=35.4443, kind="city",
    modern="Jericho, West Bank", wiki="Jericho",
    aka=[],
    note="An oasis at a perennial spring in the Jordan valley, 850 feet below "
         "sea level and among the oldest continuously settled sites anywhere. "
         "It guarded the ford and the climb up to the central hills, so anyone "
         "entering Canaan from the east had to deal with it first."),

"edom": dict(
    name="Edom", lat=30.60, lon=35.50, kind="region",
    modern="southern Jordan", wiki="Edom",
    aka=["Edomite", "Edomites", "Seir", "Mount Seir"],
    note="The red sandstone highlands south-east of the Dead Sea, holding the "
         "King's Highway and later Petra. Settlements sat behind cliffs and "
         "narrow gorges, which is the pride Obadiah addresses when he speaks to "
         "those who dwell in the clefts of the rock."),

"tyre": dict(
    name="Tyre", lat=33.2705, lon=35.1960, kind="city",
    modern="Sour, Lebanon", wiki="Tyre,_Lebanon",
    aka=["Tyrian", "Tyrians"],
    note="Originally an island fortress a half mile off the Phoenician coast, "
         "which is why it held out against Assyria and Babylon and only fell "
         "when Alexander built a causeway to it. That causeway silted up, and "
         "Tyre has been a peninsula ever since."),

"lebanon": dict(
    name="Lebanon", lat=34.20, lon=36.00, kind="region",
    modern="Mount Lebanon range, Lebanon", wiki="Lebanon",
    aka=["cedars of Lebanon"],
    note="In the Bible this is the mountain range, not the modern country: a "
         "snow-capped wall rising over 10,000 feet behind the Phoenician coast. "
         "Its cedar was the prestige timber of the ancient Near East and both "
         "the tabernacle's successors and Solomon's temple were built from it."),

"capernaum": dict(
    name="Capernaum", lat=32.8808, lon=35.5750, kind="city",
    modern="Kfar Nahum, Israel", wiki="Capernaum",
    aka=[],
    note="A fishing village on the north-west shore of the Sea of Galilee, "
         "on the road running from the coast to Damascus. A customs post and a "
         "garrison explain the tax collector and the centurion; the harbour and "
         "the synagogue explain why Jesus made it his base."),

"mediterranean": dict(
    name="Mediterranean Sea", lat=33.50, lon=32.50, kind="water",
    modern="", wiki="Mediterranean_Sea",
    aka=["Great Sea", "the Great Sea"],
    note="Called simply the Great Sea, and treated as the western edge of the "
         "world. Israel's coast has almost no natural harbours, so for most of "
         "its history the sea was a boundary rather than a road, and seafaring "
         "was left to the Phoenicians."),

"bethlehem": dict(
    name="Bethlehem", lat=31.7054, lon=35.2024, kind="city",
    modern="Bethlehem, West Bank", wiki="Bethlehem",
    aka=["Ephrath", "Ephrathah", "Bethlehem Ephratah"],
    note="A small town on the ridge road five miles south of Jerusalem, at the "
         "edge of the cultivated land before the Judean wilderness. Its name "
         "means house of bread, and its terraced barley fields are where Ruth "
         "gleaned and where David kept sheep."),

"phoenicia": dict(
    name="Phoenicia", lat=33.60, lon=35.40, kind="region",
    modern="coastal Lebanon", wiki="Phoenicia",
    aka=["Phoenician", "Phoenicians", "Sidonian", "Sidonians"],
    note="A narrow strip of coast backed hard against the Lebanon range, with "
         "too little farmland to feed itself and excellent harbours. That "
         "combination made its cities trade by sea, plant colonies as far as "
         "Spain, and supply Israel with timber, craftsmen and Jezebel."),

"mount_of_olives": dict(
    name="Mount of Olives", lat=31.7784, lon=35.2456, kind="mountain",
    modern="Jerusalem", wiki="Mount_of_Olives",
    aka=["Olivet"],
    note="A limestone ridge just east of Jerusalem, separated from the city by "
         "the Kidron Valley and about 250 feet higher, so it looks straight "
         "down into the temple courts. The road to Jericho and Bethany crosses "
         "it, which is why Jesus is so often on it."),

"euphrates": dict(
    name="Euphrates", lat=35.00, lon=40.20, kind="river",
    modern="Turkey, Syria, Iraq", wiki="Euphrates",
    aka=["the great river"],
    note="The longest river in western Asia, running about 1,700 miles from "
         "eastern Turkey to the Persian Gulf. It is the northern limit named in "
         "the promise to Abraham and the boundary Assyria and Babylon crossed "
         "to reach the Levant."),

"mount_carmel": dict(
    name="Mount Carmel", lat=32.7300, lon=35.0500, kind="mountain",
    modern="Haifa, Israel", wiki="Mount_Carmel",
    aka=["Carmel"],
    note="A wooded limestone ridge that runs 15 miles from the coast inland, "
         "reaching about 1,700 feet and forcing the main north-south road "
         "through the passes at Megiddo. Rain clouds break on it first, which "
         "is why Elijah's contest over rain was staged here."),

"bashan": dict(
    name="Bashan", lat=32.85, lon=36.10, kind="region",
    modern="Golan and Hauran, Syria", wiki="Bashan",
    aka=[],
    note="The volcanic tableland north-east of the Sea of Galilee, deep in "
         "basalt soil and famous for cattle and oak. The bulls of Bashan in the "
         "Psalms are a compliment to the pasture before they are an insult to "
         "anyone."),

"shechem": dict(
    name="Shechem", lat=32.2131, lon=35.2831, kind="city",
    modern="Tell Balata, Nablus, West Bank", wiki="Shechem",
    aka=[],
    note="In the pass between Mount Ebal and Mount Gerizim, the natural "
         "east-west crossing of the central hills. Abraham's first altar, "
         "Joseph's burial and Joshua's covenant renewal all happen here, which "
         "made it the north's answer to Jerusalem."),

"ammon": dict(
    name="Ammon", lat=31.9515, lon=35.9340, kind="region",
    modern="Amman, Jordan", wiki="Ammon",
    aka=["Ammonite", "Ammonites", "Rabbah", "Rabbath"],
    note="The plateau at the desert's edge east of Gilead, with its capital "
         "Rabbah at the head of a wadi where modern Amman still preserves the "
         "name. Squeezed between the desert and Israel, it spent its history "
         "pushing west whenever Israel was weak."),

"bethel": dict(
    name="Bethel", lat=31.9303, lon=35.2217, kind="city",
    modern="Beitin, West Bank", wiki="Bethel",
    aka=[],
    note="A ridge-road town about 11 miles north of Jerusalem, where Jacob "
         "dreamed of the stairway and named the place house of God. Jeroboam "
         "later put one of his two golden calves here precisely because "
         "pilgrims already came."),

"shiloh": dict(
    name="Shiloh", lat=32.0556, lon=35.2894, kind="city",
    modern="Khirbet Seilun, West Bank", wiki="Shiloh_(biblical_city)",
    aka=[],
    note="A hill site in Ephraim, off the main road and defensible, which is "
         "why the tabernacle and the ark stood here for generations before "
         "Jerusalem. Its destruction after the ark was captured became "
         "Jeremiah's warning about assuming a sanctuary is safe."),

"ephesus": dict(
    name="Ephesus", lat=37.9411, lon=27.3419, kind="city",
    modern="near Selcuk, Turkey", wiki="Ephesus",
    aka=["Ephesian", "Ephesians"],
    note="The largest port of Roman Asia, at the mouth of the Cayster on the "
         "west coast of Asia Minor, and home to the temple of Artemis. Its "
         "harbour silted up and the ruins now sit several miles inland, which is "
         "why a great seaport has no sea."),

"bethany": dict(
    name="Bethany", lat=31.7714, lon=35.2633, kind="city",
    modern="al-Eizariya, West Bank", wiki="Bethany_(biblical_village)",
    aka=[],
    note="A village on the east slope of the Mount of Olives, under two miles "
         "from Jerusalem but out of sight of it. Close enough for Jesus to "
         "lodge here through the last week and walk in each morning."),

"tarshish": dict(
    name="Tarshish", lat=36.90, lon=-6.35, kind="region",
    modern="probably southern Spain", wiki="Tarshish",
    aka=[],
    note="Usually identified with Tartessos near the mouth of the Guadalquivir "
         "in southern Spain, at the far western end of the Phoenician trade "
         "routes, though the identification is not certain. Either way it meant "
         "the end of the known world, and it lies almost exactly opposite "
         "Nineveh from Joppa."),

"nazareth": dict(
    name="Nazareth", lat=32.6996, lon=35.3035, kind="city",
    modern="Nazareth, Israel", wiki="Nazareth",
    aka=["Nazarene"],
    note="A small village in a hollow of the Galilean hills, unmentioned in "
         "the Old Testament or by Josephus. The Roman city of Sepphoris was "
         "four miles away and the Via Maris ran below, so it was obscure "
         "without being isolated."),

"caesarea": dict(
    name="Caesarea", lat=32.5000, lon=34.8917, kind="city",
    modern="Caesarea, Israel", wiki="Caesarea_Maritima",
    aka=["Caesarea Maritima"],
    note="Herod built an artificial deep-water harbour on an open coast that "
         "had none, and it became the Roman administrative capital of Judea. "
         "Paul was held here two years and sailed for Rome from it; it is also "
         "where the gospel first went to a Gentile household."),

"nile": dict(
    name="Nile", lat=27.20, lon=31.20, kind="river",
    modern="Egypt", wiki="Nile",
    aka=["the river"],
    note="Egypt's only real water source, flooding every summer and leaving "
         "the silt that made the valley farmable. Because the whole country "
         "depended on it, turning it to blood was an attack on Egypt's economy "
         "and its gods at once."),

"red_sea": dict(
    name="Red Sea", lat=27.50, lon=34.20, kind="water",
    modern="Egypt, Sudan, Saudi Arabia", wiki="Red_Sea",
    aka=["Sea of Reeds", "yam suph"],
    note="The Hebrew yam suph, sea of reeds, covers the Red Sea proper and its "
         "two northern arms, the Gulf of Suez and the Gulf of Aqaba, along with "
         "the marshy lakes between. Which of them Israel crossed is debated; "
         "the northern route is the usual reconstruction."),

"harran": dict(
    name="Harran", lat=36.8642, lon=39.0311, kind="city",
    modern="Harran, Turkey", wiki="Harran",
    aka=["Haran", "Padan-aram", "Paddan-aram"],
    note="A caravan town on the Balikh, a tributary of the Euphrates in "
         "northern Mesopotamia. Abraham's family stopped here on the way from "
         "Ur, and it stayed the family's home ground: Isaac's and Jacob's wives "
         "were both fetched from it."),

"antioch": dict(
    name="Antioch", lat=36.2021, lon=36.1613, kind="city",
    modern="Antakya, Turkey", wiki="Antioch",
    aka=["Antioch on the Orontes", "Syrian Antioch"],
    note="On the Orontes about 300 miles north of Jerusalem, with a port at "
         "the river mouth, the third city of the Roman empire. Disciples were "
         "first called Christians here, and it was the base every one of Paul's "
         "journeys started from."),

"gaza": dict(
    name="Gaza", lat=31.5040, lon=34.4667, kind="city",
    modern="Gaza City", wiki="Gaza_City",
    aka=[],
    note="The southernmost of the five Philistine cities and the last stop on "
         "the coastal road before the desert crossing to Egypt. Controlling it "
         "meant controlling the caravan trade, which is why it changes hands "
         "constantly through the Old Testament."),

"gethsemane": dict(
    name="Gethsemane", lat=31.7794, lon=35.2397, kind="city",
    modern="Jerusalem", wiki="Gethsemane",
    aka=[],
    note="An olive grove at the foot of the Mount of Olives, just across the "
         "Kidron from the temple. The name means oil press. It was outside the "
         "walls but minutes from them, which is why an arrest there could be "
         "made quietly at night."),

"philistia": dict(
    name="Philistia", lat=31.60, lon=34.65, kind="region",
    modern="southern coastal Israel and Gaza", wiki="Philistia",
    aka=["Philistine", "Philistines"],
    note="The coastal plain south of Joppa, held by a league of five cities: "
         "Gaza, Ashkelon, Ashdod, Gath and Ekron. Flat, fertile and on the "
         "trade road, it gave the Philistines chariots and iron while Israel "
         "held the hills above them."),

"midian": dict(
    name="Midian", lat=28.50, lon=35.50, kind="region",
    modern="north-western Saudi Arabia", wiki="Midian",
    aka=["Midianite", "Midianites"],
    note="Desert and oasis country east of the Gulf of Aqaba, home to camel "
         "caravanning herdsmen rather than to cities. Moses spent forty years "
         "here as a shepherd, which is how a man raised in an Egyptian palace "
         "learned to cross a wilderness."),

"kidron": dict(
    name="Kidron Valley", lat=31.7750, lon=35.2383, kind="region",
    modern="Jerusalem", wiki="Kidron_Valley",
    aka=["brook Kidron", "Kidron"],
    note="The dry ravine between Jerusalem and the Mount of Olives, dropping "
         "steeply below the temple's eastern wall. It ran with the runoff of "
         "sacrifice and became the city's dumping ground for idols, and it is "
         "the valley David crossed fleeing Absalom and Jesus crossed to "
         "Gethsemane."),

"corinth": dict(
    name="Corinth", lat=37.9060, lon=22.8790, kind="city",
    modern="Ancient Corinth, Greece", wiki="Ancient_Corinth",
    aka=["Corinthian", "Corinthians"],
    note="On the four-mile isthmus joining the Peloponnese to mainland Greece, "
         "with a harbour on each side. Cargo was hauled overland between them "
         "to avoid the dangerous voyage round the cape, so the city was rich, "
         "transient and famously loose."),

"rome": dict(
    name="Rome", lat=41.8911, lon=12.4864, kind="city",
    modern="Rome, Italy", wiki="Ancient_Rome",
    aka=[],
    note="Fifteen miles up the Tiber from its port at Ostia, about 1,400 miles "
         "from Jerusalem by sea and road. Reaching it is the destination Acts "
         "is aimed at from chapter one, because from Rome the roads ran "
         "everywhere else."),

"philippi": dict(
    name="Philippi", lat=41.0131, lon=24.2867, kind="city",
    modern="near Krinides, Greece", wiki="Philippi",
    aka=["Philippian", "Philippians"],
    note="A Roman colony in Macedonia on the Via Egnatia, the trunk road from "
         "the Aegean to the Adriatic, settled with army veterans. That is why "
         "its citizens were so conscious of Roman citizenship, and why Paul's "
         "own came in useful there."),

"galatia": dict(
    name="Galatia", lat=39.93, lon=32.86, kind="region",
    modern="central Turkey", wiki="Galatia",
    aka=["Galatian", "Galatians"],
    note="The high inland plateau of Asia Minor, named for Gallic settlers and "
         "organised by Rome as a province stretching south to Antioch, Iconium, "
         "Lystra and Derbe. Whether Paul wrote to the northern tribes or the "
         "southern cities he planted is a long-running question."),

"decapolis": dict(
    name="Decapolis", lat=32.2811, lon=35.8911, kind="region",
    modern="northern Jordan and southern Syria", wiki="Decapolis",
    aka=[],
    note="A cluster of Greek-speaking cities east and south-east of the Sea of "
         "Galilee, Gerasa and Gadara among them, self-governing under Rome. "
         "Gentile territory a day's walk from Jewish Galilee, which is why "
         "there were pigs there to drown."),

"caesarea_philippi": dict(
    name="Caesarea Philippi", lat=33.2481, lon=35.6944, kind="city",
    modern="Banias, Golan Heights", wiki="Caesarea_Philippi",
    aka=["Banias", "Paneas"],
    note="At the foot of Mount Hermon, where a spring bursts out of a cliff "
         "beside a grotto of Pan, about 25 miles north of the Sea of Galilee. "
         "Peter's confession is made here, in the most conspicuously pagan "
         "place in the region."),

"heshbon": dict(
    name="Heshbon", lat=31.8000, lon=35.8083, kind="city",
    modern="Tell Hesban, Jordan", wiki="Heshbon",
    aka=[],
    note="On the Transjordan plateau about 15 miles east of the Jordan, near "
         "the King's Highway. Taken from Sihon before Israel crossed the river, "
         "it became the marker for where the eastern tribes' inheritance began."),

"persia": dict(
    name="Persia", lat=29.9350, lon=52.8910, kind="region",
    modern="Fars, Iran", wiki="Achaemenid_Empire",
    aka=["Achaemenid Empire", "Persian", "Persians"],
    note="The empire's ceremonial centre was Persepolis in the Iranian "
         "highlands, but it governed from Susa and Babylon and ran roads from "
         "the Indus to the Aegean. Its scale is the point of Esther's opening: "
         "127 provinces from India to Ethiopia."),

"thessalonica": dict(
    name="Thessalonica", lat=40.6403, lon=22.9444, kind="city",
    modern="Thessaloniki, Greece", wiki="Thessaloniki",
    aka=["Thessalonian", "Thessalonians"],
    note="The capital of Macedonia, with a natural harbour on the Aegean and "
         "the Via Egnatia running through it. A letter left here travelled well, "
         "which is part of why Paul could say the word had sounded out from "
         "them in every place."),

"judean_desert": dict(
    name="Judean Wilderness", lat=31.60, lon=35.35, kind="region",
    modern="West Bank and Israel", wiki="Judean_Desert",
    aka=["Judean Desert", "wilderness of Judea", "wilderness of Judah"],
    note="The rain shadow on the eastern side of the Judean ridge: chalk hills "
         "falling 3,500 feet to the Dead Sea in about 15 miles, with almost no "
         "water. Close enough to Jerusalem to walk to in a morning, empty "
         "enough to disappear into, which is why fugitives, prophets and "
         "monastics all used it."),

"mount_hermon": dict(
    name="Mount Hermon", lat=33.4162, lon=35.8573, kind="mountain",
    modern="Syria / Lebanon / Golan border", wiki="Mount_Hermon",
    aka=["Hermon", "Sion"],
    note="The 9,200-foot southern end of the Anti-Lebanon range, snow-covered "
         "most of the year and visible from much of Galilee. Its snowmelt feeds "
         "the springs that become the Jordan, and it marked the northern limit "
         "of Israel's conquests."),

"perea": dict(
    name="Perea", lat=31.85, lon=35.70, kind="region",
    modern="western Jordan", wiki="Perea",
    aka=[],
    note="The strip east of the Jordan between Pella and the Arnon, Jewish in "
         "population and ruled with Galilee under Herod Antipas. Pilgrims used "
         "it to bypass Samaria, which is the route behind the phrase beyond "
         "Jordan in the Gospels."),

"sidon": dict(
    name="Sidon", lat=33.5630, lon=35.3689, kind="city",
    modern="Sidon, Lebanon", wiki="Sidon",
    aka=[],
    note="A Phoenician harbour city 25 miles north of Tyre and about 60 miles "
         "from Nazareth. Older than Tyre and often paired with it; Jezebel came "
         "from its royal house, and Elijah was fed by a widow in its territory "
         "at Zarephath."),

"calvary": dict(
    name="Calvary", lat=31.7784, lon=35.2297, kind="city",
    modern="Church of the Holy Sepulchre, Jerusalem", wiki="Calvary",
    aka=["Golgotha", "place of a skull"],
    note="Golgotha, place of a skull, was an outcrop of rock beside a road "
         "just outside the city wall of the time, next to a disused quarry used "
         "for tombs. The wall was later extended, which is why the traditional "
         "site now sits inside the Old City."),

"mount_nebo": dict(
    name="Mount Nebo", lat=31.7683, lon=35.7253, kind="mountain",
    modern="Mount Nebo, Jordan", wiki="Mount_Nebo",
    aka=["Pisgah"],
    note="A 2,300-foot spur on the western edge of the Moabite plateau, "
         "looking across the Jordan valley to the Judean hills. On a clear day "
         "the view runs from the Dead Sea to Jericho and beyond, which is the "
         "land Moses was shown and not given."),

"megiddo": dict(
    name="Megiddo", lat=32.5850, lon=35.1842, kind="city",
    modern="Tel Megiddo, Israel", wiki="Megiddo",
    aka=["Tel Megiddo", "Armageddon", "Har Megiddo"],
    note="A fortress mound guarding the pass where the main coastal road cuts "
         "through the Carmel ridge into the Jezreel Valley. More battles have "
         "been fought on this plain than almost anywhere, which is why "
         "Revelation borrows its name for the last one."),

"crete": dict(
    name="Crete", lat=35.24, lon=24.81, kind="island",
    modern="Crete, Greece", wiki="Crete",
    aka=["Cretan", "Cretans"],
    note="A long mountainous island across the southern Aegean, about 160 "
         "miles end to end, with the shipping lane running along its southern "
         "coast. Paul's grain ship sheltered there before the storm, and Titus "
         "was left to organise its churches."),

"malta": dict(
    name="Malta", lat=35.90, lon=14.45, kind="island",
    modern="Malta", wiki="Malta",
    aka=["Melita"],
    note="A small limestone island 60 miles south of Sicily, in the middle of "
         "the Mediterranean narrows. Fourteen days adrift from Crete puts a "
         "drifting ship almost exactly here, which is one reason the Acts "
         "account reads as a sailor's record."),

"athens": dict(
    name="Athens", lat=37.9715, lon=23.7257, kind="city",
    modern="Athens, Greece", wiki="Athens",
    aka=["Athenian", "Athenians"],
    note="Five miles inland from its port at Piraeus, past its political peak "
         "by Paul's day but still the prestige address in philosophy. The "
         "Areopagus is a bare rock below the Acropolis, in full view of the "
         "temples Paul was commenting on."),

"tigris": dict(
    name="Tigris", lat=34.50, lon=44.40, kind="river",
    modern="Turkey, Syria, Iraq", wiki="Tigris",
    aka=["Hiddekel"],
    note="The faster and shorter of Mesopotamia's two rivers, running about "
         "1,150 miles from eastern Turkey to join the Euphrates near the Gulf. "
         "Nineveh, Calah and Asshur all sat on it, and Daniel received his last "
         "vision on its bank."),

"mount_tabor": dict(
    name="Mount Tabor", lat=32.6869, lon=35.3903, kind="mountain",
    modern="Mount Tabor, Israel", wiki="Mount_Tabor",
    aka=["Tabor"],
    note="A steep isolated dome rising 1,300 feet straight out of the Jezreel "
         "Valley, unmistakable from every direction. Barak mustered on it "
         "because chariots could not follow him up, and later tradition made it "
         "the mount of transfiguration."),

"patmos": dict(
    name="Patmos", lat=37.3089, lon=26.5483, kind="island",
    modern="Patmos, Greece", wiki="Patmos",
    aka=[],
    note="A rocky island of about 13 square miles in the Aegean, some 40 miles "
         "off the coast of Asia Minor and 60 from Ephesus. Close enough for a "
         "letter to reach the seven churches, remote enough to serve Rome as a "
         "place of banishment."),

"temple_mount": dict(
    name="Temple Mount", lat=31.7780, lon=35.2354, kind="city",
    modern="Jerusalem", wiki="Temple_Mount",
    aka=["Mount Moriah", "Moriah"],
    note="The flattened summit at the north end of Jerusalem's eastern ridge, "
         "identified with the threshing floor David bought from Araunah. Herod "
         "extended it into the largest artificial platform in the ancient "
         "world, and its retaining walls still stand."),

"memphis": dict(
    name="Memphis", lat=29.8450, lon=31.2500, kind="city",
    modern="Mit Rahina, Egypt", wiki="Memphis,_Egypt",
    aka=["Noph"],
    note="At the apex of the Nile Delta just south of modern Cairo, the point "
         "where Upper and Lower Egypt meet and so Egypt's administrative centre "
         "for most of its history. Jeremiah and Ezekiel name it when they mean "
         "Egyptian power itself."),

"idumea": dict(
    name="Idumea", lat=31.35, lon=34.95, kind="region",
    modern="southern Israel", wiki="Idumea",
    aka=["Idumean", "Idumeans"],
    note="The Greek name for the country south of Judea settled by Edomites "
         "after they were pushed out of their own highlands. Herod the Great's "
         "family came from here, which is why his claim to a Jewish throne was "
         "always contested."),

}

# --------------------------------------------------------------------------
# Places the panes name in plain text without ever linking them. Revelation 1
# is the clearest case: it lists seven churches and only two were links, so a
# map built from links alone would have shown two pins for a chapter that is
# about all seven. These are matched against the pane text by name and alias.
# --------------------------------------------------------------------------
PLACES.update({

# --- Jerusalem and Judah -------------------------------------------------
"judea": dict(
    name="Judea", lat=31.65, lon=35.15, kind="region",
    modern="southern Israel and the West Bank", wiki="Judea",
    aka=["Judean", "Judah"],
    note="The southern hill country around Jerusalem, high, stony and dry, "
         "with the wilderness on one side and the Philistine plain on the "
         "other. Poor farming and hard access are what let it stay independent "
         "longest."),
"gibeon": dict(
    name="Gibeon", lat=31.8511, lon=35.1839, kind="city",
    modern="el-Jib, West Bank", wiki="Gibeon_(ancient_city)", aka=[],
    note="Six miles north-west of Jerusalem on the plateau, with an enormous "
         "rock-cut water system. Its people tricked Joshua into a treaty, and "
         "the tabernacle stood here in Solomon's early reign."),
"gibeah": dict(
    name="Gibeah", lat=31.8239, lon=35.2300, kind="city",
    modern="Tell el-Ful, West Bank", wiki="Gibeah", aka=[],
    note="A Benjamite hilltop three miles north of Jerusalem, Saul's home and "
         "first capital. It is also the scene of the atrocity in Judges 19 that "
         "nearly destroyed the tribe."),
"mizpah": dict(
    name="Mizpah", lat=31.8839, lon=35.2161, kind="city",
    modern="Tell en-Nasbeh, West Bank", wiki="Mizpah_in_Benjamin", aka=[],
    note="A fortified town on the northern approach to Jerusalem, used as a "
         "gathering point by Samuel and as Judah's administrative centre after "
         "Jerusalem fell."),
"ramah": dict(
    name="Ramah", lat=31.8450, lon=35.2339, kind="city",
    modern="er-Ram, West Bank", wiki="Ramah_(Israel)", aka=[],
    note="A Benjamite town on the ridge road north of Jerusalem, Samuel's home "
         "and the staging point from which Judah's captives were marched to "
         "Babylon, which is the weeping in Ramah Jeremiah hears."),
"michmash": dict(
    name="Michmash", lat=31.8692, lon=35.2811, kind="city",
    modern="Mukhmas, West Bank", wiki="Michmash", aka=[],
    note="On the north side of a steep gorge seven miles north-east of "
         "Jerusalem. Jonathan and his armour-bearer climbed that gorge to "
         "surprise the Philistine garrison."),
"geba": dict(
    name="Geba", lat=31.8583, lon=35.2667, kind="city",
    modern="Jaba, West Bank", wiki="Geba,_Benjamin", aka=[],
    note="Facing Michmash across the same gorge, and the southern marker of "
         "the reduced kingdom in the phrase from Geba to Beersheba."),
"anathoth": dict(
    name="Anathoth", lat=31.8131, lon=35.2639, kind="city",
    modern="Anata, West Bank", wiki="Anathoth", aka=[],
    note="A priestly village three miles north-east of Jerusalem, close enough "
         "to see the city. Jeremiah was from here, and bought a field here as "
         "the Babylonians closed in."),
"bethphage": dict(
    name="Bethphage", lat=31.7772, lon=35.2531, kind="city",
    modern="Jerusalem", wiki="Bethphage", aka=[],
    note="A village on the Mount of Olives beside Bethany, the last stop on "
         "the pilgrim road before Jerusalem comes into view. The donkey was "
         "fetched here."),
"tekoa": dict(
    name="Tekoa", lat=31.6383, lon=35.2189, kind="city",
    modern="Khirbet Tequ, West Bank", wiki="Tekoa", aka=[],
    note="On the edge of the wilderness six miles south of Bethlehem, high "
         "enough to see the Dead Sea. Amos herded sheep here before he was sent "
         "north to Bethel."),
"herodium": dict(
    name="Herodium", lat=31.6656, lon=35.2411, kind="city",
    modern="Herodion, West Bank", wiki="Herodium", aka=[],
    note="Herod's artificial cone of a fortress-palace three miles south-east "
         "of Bethlehem, visible from the whole area and built as his tomb."),
"en_gedi": dict(
    name="En-gedi", lat=31.4617, lon=35.3922, kind="city",
    modern="Ein Gedi, Israel", wiki="Ein_Gedi", aka=["Engedi"],
    note="A freshwater spring and waterfall in the cliffs on the western shore "
         "of the Dead Sea, an oasis in absolute desert. David hid in its caves, "
         "and spared Saul in one of them."),
"masada": dict(
    name="Masada", lat=31.3156, lon=35.3539, kind="city",
    modern="Masada, Israel", wiki="Masada", aka=[],
    note="An isolated plateau above the western shore of the Dead Sea with "
         "1,300-foot cliffs on every side, fortified by Herod and the last "
         "position to fall in the revolt of AD 70."),
"qumran": dict(
    name="Qumran", lat=31.7411, lon=35.4589, kind="city",
    modern="Qumran, West Bank", wiki="Qumran", aka=[],
    note="A settlement on the marl terrace above the north-west shore of the "
         "Dead Sea. The scrolls were found in caves in the cliffs behind it, "
         "the oldest Hebrew biblical manuscripts known."),
"arad": dict(
    name="Arad", lat=31.2811, lon=35.1261, kind="city",
    modern="Tel Arad, Israel", wiki="Tel_Arad", aka=[],
    note="A fortified mound on the northern edge of the Negev controlling the "
         "desert approach to Judah from the south."),
"valley_of_elah": dict(
    name="Valley of Elah", lat=31.6861, lon=34.9781, kind="region",
    modern="Israel", wiki="Valley_of_Elah", aka=["Elah"],
    note="A broad wadi running from the Judean foothills down to the Philistine "
         "plain, one of the natural invasion routes into Judah. David met "
         "Goliath where the two armies faced each other across it."),
"adullam": dict(
    name="Adullam", lat=31.6522, lon=34.9761, kind="city",
    modern="Khirbet esh-Sheikh Madhkur, Israel", wiki="Adullam", aka=[],
    note="In the honeycombed limestone of the Judean foothills above the Elah "
         "valley. David's cave stronghold here was close enough to Philistine "
         "country to be outside Saul's easy reach."),
"keilah": dict(
    name="Keilah", lat=31.6167, lon=34.9650, kind="city",
    modern="Khirbet Qila, West Bank", wiki="Keilah", aka=["Keliah"],
    note="A walled town in the same foothills, which David rescued from the "
         "Philistines and then had to abandon when he learned its people would "
         "hand him to Saul."),
"beersheba": dict(
    name="Beersheba", lat=31.2450, lon=34.8422, kind="city",
    modern="Beersheba, Israel", wiki="Beersheba", aka=["Beer-sheba"],
    note="A well at the top of the Negev, the last settled place before the "
         "desert, which is why from Dan to Beersheba means the whole land. "
         "Abraham, Isaac and Jacob all camped here."),
"negev": dict(
    name="Negev", lat=30.80, lon=34.80, kind="region",
    modern="southern Israel", wiki="Negev", aka=["the Negeb", "Negeb", "the South"],
    note="The arid triangle south of the Judean hills, grazing land in a good "
         "year and desert in a bad one. Hebrew uses the same word for it as for "
         "the direction south."),
"mamre": dict(
    name="Mamre", lat=31.5497, lon=35.1006, kind="city",
    modern="Ramat el-Khalil, West Bank", wiki="Mamre", aka=[],
    note="The oak grove just north of Hebron where Abraham camped and where he "
         "was visited by the three strangers."),

# --- Coast and Shephelah -------------------------------------------------
"joppa": dict(
    name="Joppa", lat=32.0542, lon=34.7522, kind="city",
    modern="Jaffa, Tel Aviv, Israel", wiki="Jaffa", aka=["Jaffa"],
    note="The one usable harbour on Israel's straight coast, a rock shelf with "
         "a gap in it, dangerous but workable. Cedar for both temples was "
         "landed here, Jonah sailed from here, and Peter saw his vision on a "
         "roof here."),
"ashkelon": dict(
    name="Ashkelon", lat=31.6667, lon=34.5500, kind="city",
    modern="Ashkelon, Israel", wiki="Ashkelon", aka=["Askelon"],
    note="A Philistine harbour city on the coastal road, and the only one of "
         "the five that sat directly on the sea."),
"ashdod": dict(
    name="Ashdod", lat=31.7522, lon=34.6500, kind="city",
    modern="Tel Ashdod, Israel", wiki="Ashdod", aka=["Azotus"],
    note="A Philistine city three miles inland from the coast, where the "
         "captured ark was set beside Dagon and Dagon fell over."),
"gath": dict(
    name="Gath", lat=31.7000, lon=34.8472, kind="city",
    modern="Tell es-Safi, Israel", wiki="Gath_(city)", aka=[],
    note="The Philistine city closest to the Judean foothills, guarding the "
         "Elah valley. Goliath came from here, and David later took refuge with "
         "its king."),
"ekron": dict(
    name="Ekron", lat=31.7772, lon=34.8517, kind="city",
    modern="Tel Miqne, Israel", wiki="Ekron", aka=[],
    note="The northernmost of the five Philistine cities, on the boundary with "
         "Judah, and the last place the ark was sent before being returned."),
"lachish": dict(
    name="Lachish", lat=31.5650, lon=34.8489, kind="city",
    modern="Tel Lachish, Israel", wiki="Lachish", aka=[],
    note="Judah's second city and the fortress covering the southern approach "
         "to Jerusalem. Sennacherib's siege of it is carved in relief on his "
         "palace walls, the most detailed picture of an Assyrian assault that "
         "survives."),
"beth_shemesh": dict(
    name="Beth-shemesh", lat=31.7517, lon=34.9758, kind="city",
    modern="Tel Beth Shemesh, Israel", wiki="Beit_Shemesh", aka=["Bethshemesh"],
    note="Where the Elah valley opens onto the plain, on the Judah-Philistia "
         "border. The cart carrying the ark home came to a stop here."),
"timnah": dict(
    name="Timnah", lat=31.7519, lon=34.9181, kind="city",
    modern="Tel Batash, Israel", wiki="Timnah", aka=[],
    note="A border town in the same valley, where Samson found a wife among "
         "the Philistines."),
"gezer": dict(
    name="Gezer", lat=31.8619, lon=34.9211, kind="city",
    modern="Tel Gezer, Israel", wiki="Tel_Gezer", aka=[],
    note="A mound commanding the junction where the road from Joppa turns up "
         "toward Jerusalem. Pharaoh took it and gave it to Solomon as a dowry."),
"aphek": dict(
    name="Aphek", lat=32.1039, lon=34.9331, kind="city",
    modern="Tel Afek, Israel", wiki="Aphek_(biblical)", aka=[],
    note="At the springs of the Yarkon, where the coastal road is squeezed "
         "between the river and the hills. The Philistines mustered here before "
         "the battle in which the ark was captured."),
"sharon": dict(
    name="Sharon", lat=32.30, lon=34.90, kind="region",
    modern="central coastal Israel", wiki="Sharon_plain",
    aka=["plain of Sharon"],
    note="The coastal plain between Joppa and Carmel, marshy and oak-covered in "
         "antiquity rather than farmed, which is why it is a byword for wild "
         "flowering growth."),

# --- Central hills and the north -----------------------------------------
"mount_ebal": dict(
    name="Mount Ebal", lat=32.2353, lon=35.2733, kind="mountain",
    modern="Nablus, West Bank", wiki="Mount_Ebal", aka=["Ebal"],
    note="The bare northern side of the Shechem pass, 3,080 feet. The curses "
         "of the covenant were read from this side, facing Gerizim across the "
         "valley, in a natural amphitheatre with remarkable acoustics."),
"mount_gerizim": dict(
    name="Mount Gerizim", lat=32.1992, lon=35.2733, kind="mountain",
    modern="Nablus, West Bank", wiki="Mount_Gerizim", aka=["Gerizim"],
    note="The southern side of the same pass and the mountain of blessing. "
         "Samaritans built their temple on it and still worship there, which is "
         "the this mountain of the woman at the well."),
"ai": dict(
    name="Ai", lat=31.9167, lon=35.2600, kind="city",
    modern="et-Tell, West Bank", wiki="Ai_(Canaan)", aka=[],
    note="A small site east of Bethel, taken on the second attempt after the "
         "defeat over Achan's theft. Which ruin is Ai remains disputed, since "
         "et-Tell appears to have been unoccupied at the likely date."),
"gilgal": dict(
    name="Gilgal", lat=31.8700, lon=35.5100, kind="city",
    modern="Jordan valley, West Bank", wiki="Gilgal", aka=[],
    note="Israel's first camp west of the Jordan, between the river and "
         "Jericho, where the twelve stones were set up. The exact site has never "
         "been fixed."),
"ephraim": dict(
    name="Ephraim", lat=32.05, lon=35.20, kind="region",
    modern="central West Bank", wiki="Ephraim",
    aka=["Ephraimite", "Ephraimites"],
    note="The central hill country north of Benjamin, the largest and best "
         "watered of the northern territories. It dominated the north so "
         "thoroughly that the prophets use Ephraim to mean the whole northern "
         "kingdom."),
"tirzah": dict(
    name="Tirzah", lat=32.2808, lon=35.3389, kind="city",
    modern="Tell el-Farah North, West Bank", wiki="Tirzah_(ancient_city)", aka=[],
    note="A spring-fed site north-east of Shechem that served as the northern "
         "kingdom's capital before Omri moved to Samaria."),
"dothan": dict(
    name="Dothan", lat=32.4117, lon=35.1961, kind="city",
    modern="Tell Dothan, West Bank", wiki="Dothan", aka=[],
    note="In a fertile basin on the caravan route north of Shechem, which is "
         "why a passing Midianite trade caravan was available to buy Joseph. "
         "Elisha was later besieged here."),
"jezreel_valley": dict(
    name="Jezreel Valley", lat=32.60, lon=35.30, kind="region",
    modern="northern Israel", wiki="Jezreel_Valley",
    aka=["valley of Jezreel", "plain of Esdraelon", "Esdraelon"],
    note="The one flat corridor cutting across the country from the coast to "
         "the Jordan, dividing Galilee from the central hills. Good chariot "
         "ground, which is why every invading army and most of Israel's "
         "decisive battles ended up here."),
"jezreel": dict(
    name="Jezreel", lat=32.5558, lon=35.3306, kind="city",
    modern="Tel Yizre'el, Israel", wiki="Jezreel_(city)", aka=[],
    note="Ahab's second residence, at the eastern end of the valley that "
         "carries its name. Naboth's vineyard was here, and Jezebel died here."),
"beth_shan": dict(
    name="Beth-shan", lat=32.5000, lon=35.5000, kind="city",
    modern="Beit She'an, Israel", wiki="Beit_She'an",
    aka=["Beth-shean", "Bethshan", "Scythopolis"],
    note="Where the Jezreel Valley meets the Jordan, controlling both routes. "
         "Saul's body was hung on its wall after Gilboa."),
"shunem": dict(
    name="Shunem", lat=32.6050, lon=35.3361, kind="city",
    modern="Sulam, Israel", wiki="Shunem", aka=[],
    note="A village on the southern slope of the hill of Moreh in the Jezreel "
         "Valley, where a well-off woman built Elisha a room on the roof."),
"nain": dict(
    name="Nain", lat=32.6317, lon=35.3450, kind="city",
    modern="Nein, Israel", wiki="Nain,_Israel", aka=[],
    note="A small village on the same hillside, about six miles from Nazareth, "
         "where Jesus stopped a funeral procession at the gate."),
"sepphoris": dict(
    name="Sepphoris", lat=32.7519, lon=35.2794, kind="city",
    modern="Tzippori, Israel", wiki="Sepphoris", aka=["Zippori"],
    note="Herod Antipas's Galilean capital, being rebuilt through Jesus' "
         "childhood four miles from Nazareth, which is the likeliest work a "
         "Nazarene builder would have walked to."),
"cana": dict(
    name="Cana", lat=32.8131, lon=35.3122, kind="city",
    modern="Khirbet Qana, Israel", wiki="Cana", aka=[],
    note="A Galilean village a few miles north of Nazareth, site of the first "
         "sign. Two candidate locations compete and neither is settled."),
"tiberias": dict(
    name="Tiberias", lat=32.7922, lon=35.5311, kind="city",
    modern="Tiberias, Israel", wiki="Tiberias", aka=[],
    note="Built by Herod Antipas on the western shore of the lake and named "
         "for the emperor. Founded over a graveyard, so observant Jews avoided "
         "it at first, and the Gospels never have Jesus enter it."),
"magdala": dict(
    name="Magdala", lat=32.8269, lon=35.5158, kind="city",
    modern="Migdal, Israel", wiki="Magdala", aka=[],
    note="A fishing and fish-salting town on the western shore between "
         "Tiberias and Capernaum, and where Mary Magdalene's name comes from."),
"bethsaida": dict(
    name="Bethsaida", lat=32.9100, lon=35.6300, kind="city",
    modern="et-Tell, Golan Heights", wiki="Bethsaida", aka=[],
    note="Just east of where the Jordan enters the lake, the home town of "
         "Peter, Andrew and Philip. The name means house of the fisherman."),
"chorazin": dict(
    name="Chorazin", lat=32.9111, lon=35.5644, kind="city",
    modern="Korazim, Israel", wiki="Korazim", aka=["Chorazim"],
    note="A basalt-built town in the hills two miles above Capernaum, named "
         "with Bethsaida in the woe over towns that saw the most and changed "
         "the least."),
"gadara": dict(
    name="Gadara", lat=32.6550, lon=35.6850, kind="city",
    modern="Umm Qais, Jordan", wiki="Gadara", aka=["Gadarene", "Gadarenes"],
    note="A Decapolis city on a ridge above the Yarmuk, south-east of the Sea "
         "of Galilee, whose territory ran down to the lake shore."),
"gerasa": dict(
    name="Gerasa", lat=32.2811, lon=35.8911, kind="city",
    modern="Jerash, Jordan", wiki="Jerash", aka=["Gergesa", "Gerasene", "Gerasenes"],
    note="The best preserved of the Decapolis cities, in the Gilead highlands. "
         "Its colonnaded streets and theatres show what Greek-speaking urban "
         "life looked like a day's walk from Galilee."),
"hazor": dict(
    name="Hazor", lat=33.0172, lon=35.5681, kind="city",
    modern="Tel Hazor, Israel", wiki="Tel_Hazor", aka=[],
    note="The largest Canaanite city in the country, on the trade road north of "
         "the Sea of Galilee, called the head of all those kingdoms. Joshua "
         "burned it and Solomon refortified it."),
"dan": dict(
    name="Dan", lat=33.2489, lon=35.6519, kind="city",
    modern="Tel Dan, Israel", wiki="Tel_Dan", aka=["Laish"],
    note="At the largest of the Jordan's headwater springs under Mount Hermon, "
         "the northern limit of Israel. Jeroboam set his second golden calf "
         "here, as far from Jerusalem as he could get."),
"zarephath": dict(
    name="Zarephath", lat=33.4544, lon=35.2950, kind="city",
    modern="Sarafand, Lebanon", wiki="Sarepta", aka=["Sarepta"],
    note="A Phoenician coastal village between Tyre and Sidon, outside Israel "
         "and inside Jezebel's home territory, where Elijah was fed through the "
         "drought by a widow."),
"kishon": dict(
    name="River Kishon", lat=32.7900, lon=35.0600, kind="river",
    modern="northern Israel", wiki="Kishon_River", aka=["Kishon"],
    note="Drains the Jezreel Valley north-west past Carmel to the sea. Usually "
         "a trickle, it floods fast, which is how it swept away Sisera's "
         "chariots."),
"mount_gilboa": dict(
    name="Mount Gilboa", lat=32.5083, lon=35.4139, kind="mountain",
    modern="Mount Gilboa, Israel", wiki="Mount_Gilboa", aka=["Gilboa"],
    note="The ridge on the south side of the Jezreel Valley, where Saul and "
         "Jonathan died and where David's lament asks for no dew to fall."),

# --- East of the Jordan --------------------------------------------------
"succoth": dict(
    name="Succoth", lat=32.1939, lon=35.6222, kind="city",
    modern="Deir Alla, Jordan", wiki="Succoth_(Israel)", aka=[],
    note="In the Jordan valley near the mouth of the Jabbok, where Jacob "
         "stopped after Peniel and where Solomon's bronze was cast."),
"jabbok": dict(
    name="Jabbok", lat=32.1900, lon=35.6000, kind="river",
    modern="Zarqa River, Jordan", wiki="Jabbok", aka=[],
    note="A tributary running west out of Gilead into the Jordan through a deep "
         "gorge. Jacob wrestled at its ford, and it divided Ammon from Gilead."),
"arnon": dict(
    name="Arnon", lat=31.4700, lon=35.5800, kind="river",
    modern="Wadi Mujib, Jordan", wiki="Arnon", aka=[],
    note="A canyon up to 1,700 feet deep cutting west into the Dead Sea, and "
         "the border between Moab and the territory north of it. Crossing it "
         "meant descending and climbing a mile of switchbacks."),
"dibon": dict(
    name="Dibon", lat=31.5069, lon=35.7831, kind="city",
    modern="Dhiban, Jordan", wiki="Dhiban,_Jordan", aka=[],
    note="A Moabite town just north of the Arnon on the King's Highway. The "
         "Mesha Stele, found here, is Moab's own account of rebelling against "
         "Israel."),
"kir_hareseth": dict(
    name="Kir-hareseth", lat=31.1808, lon=35.7017, kind="city",
    modern="Kerak, Jordan", wiki="Al-Karak", aka=["Kir", "Kir-haraseth"],
    note="Moab's hilltop fortress capital south of the Arnon, where the king "
         "sacrificed his own son on the wall when the siege closed in."),
"ramoth_gilead": dict(
    name="Ramoth-gilead", lat=32.5500, lon=36.0000, kind="city",
    modern="northern Jordan", wiki="Ramoth-Gilead", aka=["Ramoth"],
    note="A fortified city of refuge on the Gilead plateau near the Aramean "
         "frontier, fought over repeatedly. Ahab died attacking it. The site is "
         "not certainly identified."),
"jabesh_gilead": dict(
    name="Jabesh-gilead", lat=32.4500, lon=35.6500, kind="city",
    modern="northern Jordan", wiki="Jabesh-Gilead", aka=["Jabesh"],
    note="A Gileadite town east of the Jordan whose rescue from the Ammonites "
         "made Saul king. Its men later recovered his body from Beth-shan. The "
         "exact site is uncertain."),
"machaerus": dict(
    name="Machaerus", lat=31.5667, lon=35.6250, kind="city",
    modern="Mukawir, Jordan", wiki="Machaerus", aka=[],
    note="A Herodian hilltop fortress east of the Dead Sea, where Josephus "
         "says John the Baptist was imprisoned and executed."),
"petra": dict(
    name="Sela", lat=30.3290, lon=35.4440, kind="city",
    modern="Petra, Jordan", wiki="Petra", aka=["Petra"],
    note="A basin in the Edomite sandstone reached through a slot canyon, "
         "later the Nabatean capital. It is the sort of place the prophets have "
         "in view when they mock Edom's confidence in its rock."),
"transjordan": dict(
    name="Transjordan", lat=31.90, lon=35.80, kind="region",
    modern="western Jordan", wiki="Transjordan_(region)",
    aka=["beyond Jordan", "beyond the Jordan"],
    note="Everything east of the Jordan and the Dead Sea: the plateau taken "
         "before the river was crossed and settled by Reuben, Gad and half of "
         "Manasseh, who then spent centuries anxious about being counted out."),

# --- Egypt, Sinai and the south -----------------------------------------
"goshen": dict(
    name="Goshen", lat=30.8000, lon=31.8500, kind="region",
    modern="eastern Nile Delta, Egypt", wiki="Land_of_Goshen", aka=[],
    note="The eastern Delta, well watered grazing country on the edge of Egypt "
         "rather than in its heart, which is exactly why shepherds were "
         "settled there and could stay distinct."),
"rameses": dict(
    name="Rameses", lat=30.7981, lon=31.8331, kind="city",
    modern="Qantir, Egypt", wiki="Pi-Ramesses", aka=["Raamses", "Pi-Ramesses"],
    note="A Delta royal city usually identified with Qantir, one of the two "
         "store cities Israel built and the starting point of the exodus."),
"tanis": dict(
    name="Zoan", lat=30.9758, lon=31.8806, kind="city",
    modern="San el-Hagar, Egypt", wiki="Tanis", aka=["Tanis"],
    note="A Delta capital in later periods, named by the prophets when they "
         "mean Egypt's court, and the field of Zoan in Psalm 78."),
"kadesh_barnea": dict(
    name="Kadesh-barnea", lat=30.6667, lon=34.4333, kind="city",
    modern="Ain el-Qudeirat, Egypt/Israel border", wiki="Kadesh-barnea",
    aka=["Kadesh"],
    note="The largest spring in the northern Sinai, about 50 miles south of "
         "Beersheba. Israel camped here, sent the spies north from here, and "
         "was turned back here to spend a generation in the wilderness."),
"ezion_geber": dict(
    name="Ezion-geber", lat=29.5500, lon=34.9800, kind="city",
    modern="near Aqaba / Eilat", wiki="Ezion-Geber", aka=["Elath", "Eloth"],
    note="At the head of the Gulf of Aqaba, Israel's only access to the Red "
         "Sea. Solomon based a merchant fleet here, and Jehoshaphat's was "
         "wrecked here."),
"cush": dict(
    name="Cush", lat=19.00, lon=32.50, kind="region",
    modern="Sudan / northern Nubia", wiki="Kingdom_of_Kush",
    aka=["Ethiopia", "Ethiopian", "Nubia"],
    note="The Nile kingdom upstream of Egypt beyond the first cataract, taken "
         "as the far southern edge of the known world in the same way Tarshish "
         "marks the west."),
"sheba": dict(
    name="Sheba", lat=15.4200, lon=45.3300, kind="region",
    modern="Yemen", wiki="Sheba", aka=[],
    note="South-west Arabia, roughly modern Yemen, controlling the incense "
         "trade. Its queen's visit to Solomon meant a caravan journey of some "
         "1,400 miles each way, which is the point of the gifts she brought."),

# --- Mesopotamia and the east -------------------------------------------
"mesopotamia": dict(
    name="Mesopotamia", lat=34.50, lon=43.00, kind="region",
    modern="Iraq and eastern Syria", wiki="Mesopotamia",
    aka=["Aram-naharaim"],
    note="The land between the Tigris and Euphrates, flat, hot and farmable "
         "only by irrigation, which forced early cities into large-scale "
         "cooperation. Abraham came from its southern end and Israel's exiles "
         "were taken to its middle."),
"ur": dict(
    name="Ur", lat=30.9617, lon=46.1031, kind="city",
    modern="Tell el-Muqayyar, Iraq", wiki="Ur", aka=["Ur of the Chaldees"],
    note="A Sumerian city near the lower Euphrates, once close to the head of "
         "the Persian Gulf before the coastline moved. Leaving it for Canaan "
         "meant leaving one of the most developed places on earth for hill "
         "country."),
"susa": dict(
    name="Susa", lat=32.1892, lon=48.2575, kind="city",
    modern="Shush, Iran", wiki="Susa", aka=["Shushan"],
    note="An ancient Elamite capital on the plain east of the Tigris, used by "
         "the Persian kings as a winter residence. Esther's court and "
         "Nehemiah's cupbearing both happen here, about 1,000 miles from "
         "Jerusalem."),
"elam": dict(
    name="Elam", lat=32.00, lon=48.50, kind="region",
    modern="Khuzestan, Iran", wiki="Elam", aka=["Elamite", "Elamites"],
    note="The lowland and mountain country east of the Tigris around Susa, "
         "Mesopotamia's oldest rival and later absorbed into Persia."),
"media": dict(
    name="Media", lat=34.8000, lon=48.5100, kind="region",
    modern="north-western Iran", wiki="Medes", aka=["Mede", "Medes", "Ecbatana"],
    note="The Zagros highlands north-east of Mesopotamia. The Medes helped "
         "destroy Nineveh and then joined Persia, which is why Daniel keeps "
         "saying Medes and Persians as one phrase."),
"ararat": dict(
    name="Ararat", lat=39.7019, lon=44.2983, kind="mountain",
    modern="Agri Dagi, Turkey", wiki="Mount_Ararat", aka=[],
    note="Genesis says the mountains of Ararat, a region of eastern Anatolia "
         "rather than one peak; the 16,850-foot volcano now carrying the name is "
         "a later identification."),
"aram": dict(
    name="Aram", lat=34.0000, lon=37.0000, kind="region",
    modern="Syria", wiki="Aram_(region)", aka=["Syria", "Syrian", "Syrians", "Aramean"],
    note="The Syrian interior north-east of Israel, a set of city-states rather "
         "than one kingdom, with Damascus the strongest. Aramaic, its language, "
         "became the everyday speech of the whole region including Judea."),

# --- Asia Minor and the Aegean ------------------------------------------
"asia_minor": dict(
    name="Asia Minor", lat=39.00, lon=32.50, kind="region",
    modern="Turkey", wiki="Anatolia", aka=["Anatolia", "Asia"],
    note="The peninsula between the Black Sea and the Mediterranean, a high dry "
         "plateau ringed by mountains with the Greek cities on its western "
         "coast. Roman Asia, the province Paul worked from Ephesus, was only "
         "its western end."),
"tarsus": dict(
    name="Tarsus", lat=36.9167, lon=34.8950, kind="city",
    modern="Tarsus, Turkey", wiki="Tarsus,_Mersin", aka=[],
    note="On the Cilician plain a few miles up a navigable river from the sea, "
         "below the pass through the Taurus called the Cilician Gates. A "
         "university town and a Roman citizen colony, which explains a good "
         "deal about Paul."),
"cilicia": dict(
    name="Cilicia", lat=37.00, lon=35.00, kind="region",
    modern="southern Turkey", wiki="Cilicia", aka=[],
    note="The coastal plain of south-eastern Asia Minor, shut in by the Taurus "
         "mountains and reached overland only through narrow passes."),
"cyprus": dict(
    name="Cyprus", lat=35.00, lon=33.20, kind="island",
    modern="Cyprus", wiki="Cyprus", aka=["Cypriot"],
    note="The large island 60 miles off the Syrian coast, a copper source since "
         "the Bronze Age. Barnabas came from here, and it was the first stop of "
         "the first missionary journey."),
"salamis_cyprus": dict(
    name="Salamis", lat=35.1833, lon=33.9050, kind="city",
    modern="near Famagusta, Cyprus", wiki="Salamis,_Cyprus", aka=[],
    note="Cyprus's main eastern harbour and the landing point on the way from "
         "Antioch."),
"paphos": dict(
    name="Paphos", lat=34.7750, lon=32.4239, kind="city",
    modern="Paphos, Cyprus", wiki="Paphos", aka=[],
    note="The Roman administrative seat at the western end of Cyprus, where "
         "the governor Sergius Paulus was persuaded."),
"pisidian_antioch": dict(
    name="Antioch in Pisidia", lat=38.3050, lon=31.1900, kind="city",
    modern="Yalvac, Turkey", wiki="Antioch_of_Pisidia",
    aka=["Pisidian Antioch"],
    note="A Roman colony 3,600 feet up on the Anatolian plateau, on the road "
         "east from Ephesus. Distinct from Syrian Antioch, and the first "
         "synagogue sermon Acts records in full was preached here."),
"iconium": dict(
    name="Iconium", lat=37.8742, lon=32.4922, kind="city",
    modern="Konya, Turkey", wiki="Konya", aka=[],
    note="An oasis city on the central plateau at the junction of several "
         "trade roads, about 80 miles south-east of Pisidian Antioch."),
"lystra": dict(
    name="Lystra", lat=37.5772, lon=32.4531, kind="city",
    modern="Hatunsaray, Turkey", wiki="Lystra", aka=[],
    note="A small Roman colony on the plateau where Paul was taken for Hermes "
         "and then stoned, and where Timothy was from."),
"derbe": dict(
    name="Derbe", lat=37.3500, lon=33.2800, kind="city",
    modern="Karaman province, Turkey", wiki="Derbe", aka=[],
    note="The furthest point east on the first journey, near the frontier of "
         "the province. The site is identified only approximately."),
"perga": dict(
    name="Perga", lat=36.9611, lon=30.8542, kind="city",
    modern="near Antalya, Turkey", wiki="Perga", aka=["Perge"],
    note="A city on the Pamphylian coastal plain, reached up a navigable river, "
         "where the road inland to Pisidia begins."),
"attalia": dict(
    name="Attalia", lat=36.8850, lon=30.7042, kind="city",
    modern="Antalya, Turkey", wiki="Antalya", aka=[],
    note="The harbour of Pamphylia, from which the first journey sailed home to "
         "Antioch."),
"troas": dict(
    name="Troas", lat=39.8158, lon=26.1589, kind="city",
    modern="Dalyan, Turkey", wiki="Alexandria_Troas", aka=[],
    note="The port at the north-west corner of Asia Minor facing Europe across "
         "the Aegean, and the natural crossing point. The call to Macedonia came "
         "here."),
"miletus": dict(
    name="Miletus", lat=37.5306, lon=27.2778, kind="city",
    modern="Balat, Turkey", wiki="Miletus", aka=[],
    note="A harbour city 30 miles south of Ephesus, where Paul summoned the "
         "Ephesian elders rather than go into the city himself."),
"colossae": dict(
    name="Colossae", lat=37.7881, lon=29.2631, kind="city",
    modern="near Honaz, Turkey", wiki="Colossae", aka=["Colossian", "Colossians"],
    note="In the Lycus valley about 100 miles inland from Ephesus, already "
         "declining by Paul's day and overshadowed by Laodicea and Hierapolis "
         "a few miles away."),
"laodicea": dict(
    name="Laodicea", lat=37.8358, lon=29.1078, kind="city",
    modern="near Denizli, Turkey", wiki="Laodicea_on_the_Lycus", aka=[],
    note="A wealthy banking and textile city in the same valley, with one "
         "weakness: its water had to be piped in from miles away and arrived "
         "lukewarm, which is the image the letter to it uses."),
"hierapolis": dict(
    name="Hierapolis", lat=37.9250, lon=29.1283, kind="city",
    modern="Pamukkale, Turkey", wiki="Hierapolis", aka=[],
    note="Across the valley from Laodicea, famous for hot mineral springs that "
         "terrace down a white cliff face, visible for miles."),
"smyrna": dict(
    name="Smyrna", lat=38.4192, lon=27.1394, kind="city",
    modern="Izmir, Turkey", wiki="Smyrna", aka=[],
    note="A well-planned harbour city 40 miles north of Ephesus, loyal to Rome "
         "and prosperous, whose letter nonetheless speaks only of poverty and "
         "pressure."),
"pergamum": dict(
    name="Pergamum", lat=39.1208, lon=27.1836, kind="city",
    modern="Bergama, Turkey", wiki="Pergamon", aka=["Pergamos"],
    note="Built up a steep 1,000-foot hill, the province's original capital and "
         "the seat of the imperial cult in Asia, with the great altar of Zeus on "
         "the acropolis."),
"thyatira": dict(
    name="Thyatira", lat=38.9181, lon=27.8422, kind="city",
    modern="Akhisar, Turkey", wiki="Thyatira", aka=[],
    note="An inland manufacturing town known for dyeing, which is Lydia the "
         "seller of purple's home trade, and heavily organised into craft "
         "guilds."),
"sardis": dict(
    name="Sardis", lat=38.4875, lon=28.0406, kind="city",
    modern="Sart, Turkey", wiki="Sardis", aka=[],
    note="The old Lydian capital on a spur of Mount Tmolus, thought "
         "unassailable and twice taken by night because nobody watched the "
         "cliff. Its letter tells it to wake up."),
"philadelphia_asia": dict(
    name="Philadelphia", lat=38.3500, lon=28.5181, kind="city",
    modern="Alasehir, Turkey", wiki="Philadelphia_(Lydia)", aka=[],
    note="A frontier town on the road east from Sardis, in earthquake country, "
         "founded to spread Greek culture inland, which suits a letter about an "
         "open door."),
"rhodes": dict(
    name="Rhodes", lat=36.2000, lon=28.0000, kind="island",
    modern="Rhodes, Greece", wiki="Rhodes", aka=[],
    note="An island off the south-west corner of Asia Minor and a standard "
         "waypoint on the coastal shipping route."),
"cnidus": dict(
    name="Cnidus", lat=36.6861, lon=27.3742, kind="city",
    modern="Datca peninsula, Turkey", wiki="Knidos", aka=[],
    note="A harbour at the tip of a long peninsula where ships heading west "
         "must commit to open water, which is where Paul's ship lost the wind."),

# --- Greece and Italy ----------------------------------------------------
"macedonia": dict(
    name="Macedonia", lat=40.9000, lon=22.5000, kind="region",
    modern="northern Greece", wiki="Macedonia_(Roman_province)",
    aka=["Macedonian", "Macedonians"],
    note="The Roman province north of Greece proper, crossed by the Via "
         "Egnatia. Crossing into it from Troas took the gospel from Asia into "
         "Europe."),
"greece": dict(
    name="Achaia", lat=38.5000, lon=22.5000, kind="region",
    modern="southern Greece", wiki="Achaia_(Roman_province)",
    aka=["Greece", "Hellas"],
    note="The Roman province covering southern Greece, governed from Corinth. "
         "Long past political power and still the cultural reference point of "
         "the eastern empire."),
"berea": dict(
    name="Berea", lat=40.5236, lon=22.2028, kind="city",
    modern="Veria, Greece", wiki="Veria", aka=["Beroea"],
    note="A town off the main road at the foot of Mount Bermion, 50 miles "
         "west of Thessalonica, whose synagogue checked what it was told against "
         "the Scriptures."),
"cenchreae": dict(
    name="Cenchreae", lat=37.8881, lon=22.9872, kind="city",
    modern="Kechries, Greece", wiki="Cenchreae", aka=["Cenchrea"],
    note="Corinth's eastern harbour on the Saronic Gulf, six miles from the "
         "city, with a church of its own and Phoebe as its deacon."),
"puteoli": dict(
    name="Puteoli", lat=40.8231, lon=14.1214, kind="city",
    modern="Pozzuoli, Italy", wiki="Pozzuoli", aka=[],
    note="The main grain port for Rome, on the bay of Naples, where Paul landed "
         "for the last 130 miles up the Appian Way."),
"syracuse": dict(
    name="Syracuse", lat=37.0750, lon=15.2867, kind="city",
    modern="Syracuse, Sicily", wiki="Syracuse,_Sicily", aka=[],
    note="The chief city of Sicily and a three-day stop on the voyage from "
         "Malta to Italy."),

})


# Link targets the panes use that are a second Wikipedia article for a place
# already in the gazetteer. Without these the build would report the target as
# unknown and drop the pin.
WIKI_ALIASES = {
    "Tel_Megiddo": "megiddo",
    "Megiddo": "megiddo",
    "Gaza_City": "gaza",
    "Ancient_Egypt": "egypt",
    "Ancient_Rome": "rome",
    "Ancient_Corinth": "corinth",
    "Achaemenid_Empire": "persia",
    "Thessaloniki": "thessalonica",
    "Caesarea_Maritima": "caesarea",
    "Mount_Sinai": "sinai",
    "Tyre,_Lebanon": "tyre",
    "Memphis,_Egypt": "memphis",
    "Judean_Desert": "judean_desert",
    "Kidron_Valley": "kidron",
    "Mediterranean_Sea": "mediterranean",
    "Jordan_River": "jordan_river",
    "Shiloh_(biblical_city)": "shiloh",
    "Bethany_(biblical_village)": "bethany",
}

# Names that must never be matched in running prose, because in these panes they
# almost always mean something other than the place. Overlaps between names are
# not the problem here; matching is longest-first, so "Sea of Galilee" already
# beats "Galilee" and "Pergamum" is never read as "Perga". These are the terms
# where no pin is the right answer.
NEVER_MATCH = {
    "Judah",        # overwhelmingly the kingdom or the tribe, not a location
    "Israel",       # likewise
    "the South",    # a compass direction more often than the Negev
    "Kir",          # a bare three letters, matches inside other words
    "Elah",         # the valley is matched by its full name
    "Ramoth",       # ambiguous between Ramoth-gilead and other Ramoths
    "Jabesh",       # matched by its full name
}


def wiki_to_key():
    """Wikipedia article title -> gazetteer key."""
    out = dict(WIKI_ALIASES)
    for key, p in PLACES.items():
        out.setdefault(p["wiki"], key)
    return out


def match_terms():
    """(term, key) pairs for finding places in pane prose, longest term first so
    'Sea of Galilee' wins over 'Galilee' and 'Mount Carmel' over 'Carmel'."""
    terms = []
    for key, p in PLACES.items():
        for term in [p["name"]] + list(p.get("aka") or []):
            if term in NEVER_MATCH:
                continue
            terms.append((term, key))
    terms.sort(key=lambda t: (-len(t[0]), t[0]))
    return terms


def validate():
    """Catch the mistakes that would otherwise show up as a pin in the sea."""
    problems = []
    seen_names = {}
    for key, p in PLACES.items():
        for field in ("name", "lat", "lon", "kind", "modern", "note", "wiki"):
            if field not in p:
                problems.append(f"{key}: missing {field}")
        if p.get("kind") not in ("city", "region", "water", "river", "mountain",
                                 "island"):
            problems.append(f"{key}: bad kind {p.get('kind')!r}")
        lat, lon = p.get("lat"), p.get("lon")
        # The renderer's frame, from mapgeo_basemap.py. A pin outside it would
        # be drawn off the edge of every map it appears on.
        if not (11.0 <= lat <= 48.0 and -11.0 <= lon <= 56.0):
            problems.append(f"{key}: {lat},{lon} is outside the map frame")
        if len(p.get("note", "")) < 40:
            problems.append(f"{key}: note is too short to be a write-up")
        seen_names.setdefault(p["name"], []).append(key)
    for name, keys in seen_names.items():
        if len(keys) > 1:
            problems.append(f"duplicate name {name!r}: {', '.join(keys)}")
    return problems


if __name__ == "__main__":
    import sys
    bad = validate()
    print(f"{len(PLACES)} places, {len(match_terms())} match terms")
    for line in bad:
        print(f"  PROBLEM {line}")
    sys.exit(1 if bad else 0)


# --------------------------------------------------------------------------
# Finding the places a pane is talking about
# --------------------------------------------------------------------------
_TAG = None
_PATS = None


def _compile():
    global _TAG, _PATS
    import re
    if _TAG is None:
        _TAG = re.compile(r"<[^>]+>")
        # (?<![\w-]) rather than \b so that Beth-shemesh is not found inside
        # Beth-shemesh-something, and Perga is not found inside Pergamum.
        _PATS = [(re.compile(r"(?<![\w-])" + re.escape(t) + r"(?![\w-])"), k)
                 for t, k in match_terms()]
    return _TAG, _PATS


_MAP_DIV = None
_NOTES_BLOCK = None


def pane_source(pane_html):
    """A pane with the map and the write-ups taken back out again.

    Everything downstream reads a pane through this. The write-ups are full of
    place names -- "Nineveh, Calah and Asshur all sat on it" -- and each one
    carries a Wikipedia link, so reading a pane that already has them would
    find places the chapter never mentions and grow the list a little on every
    run. Stripping here rather than in each caller means no caller can forget.
    """
    global _MAP_DIV, _NOTES_BLOCK
    import re
    if _MAP_DIV is None:
        _MAP_DIV = re.compile(r'[ \t]*<div class="geo-map"[^>]*></div>\n?')
        _NOTES_BLOCK = re.compile(
            r"\n?[ \t]*<!-- geo-notes -->.*?<!-- /geo-notes -->", re.S)
    return _NOTES_BLOCK.sub("", _MAP_DIV.sub("", pane_html))


def find_places(pane_html):
    """The gazetteer keys a Map & Geography pane refers to, in the order a
    reader meets them.

    Two passes. Wikipedia link targets are authoritative, because a person chose
    them. Then the prose is scanned for names, which is what picks up the five
    churches of Revelation 1 that were never linked, and Aram, Judea, Gibeon and
    the rest. Longest match first, and each stretch of text is consumed once, so
    "Sea of Galilee" does not also register Galilee."""
    import html
    import re
    tag, pats = _compile()
    pane_html = pane_source(pane_html)
    keys = []
    w2k = wiki_to_key()
    # Both spellings of an authoritative reference, in document order. The
    # Wikipedia form is what the panes started with; the #geo-note- form is what
    # add_mapgeo_maps.py rewrites them into, and reading both is what makes that
    # rewrite safe to run twice.
    for wiki, note in re.findall(
            r'href="https://en\.wikipedia\.org/wiki/([^"]+)"'
            r'|href="#geo-note-([a-z0-9_]+)"', pane_html):
        key = w2k.get(wiki) if wiki else (note if note in PLACES else None)
        if key and key not in keys:
            keys.append(key)
    # Stripping tags leaves double spaces wherever a name was half inside a
    # link, as in "<a>Antioch</a> in Pisidia". Collapsing runs of whitespace is
    # what lets multi-word names survive that.
    text = re.sub(r"\s+", " ", html.unescape(tag.sub(" ", pane_html)))
    hits = []
    taken = [False] * len(text)
    for pat, key in pats:
        for m in pat.finditer(text):
            if any(taken[m.start():m.end()]):
                continue
            taken[m.start():m.end()] = [True] * (m.end() - m.start())
            hits.append((m.start(), key))
    for _, key in sorted(hits):
        if key not in keys:
            keys.append(key)
    return keys
