#!/usr/bin/env python3
"""Spelling and wording audit, 25 Sep 2026.

Prompted by luke1.html, where the Authorship & Background pane called
Zechariah's wife "Elisabeth" while the Summary, the map and the Reflection
tab on the same page said "Elizabeth". Elisabeth is the KJV/ASV spelling and
is correct inside those two translation blocks, but the site's own voice
otherwise follows the modern spelling the default (ESV) text uses, so the
page disagreed with itself.

The cause was general: the verse-range sections were drafted from the KJV
text (dump_kjv.py) and carried its name forms into the commentary. This
script puts KJV-only name forms back into the modern (ESV) spelling wherever
they appear in the site's own prose, plus British spellings that
normalize_british_spelling.py and fix_kjv_vocab_spelling.py did not cover
and a handful of plain typos.

What it never touches:
  * the scripture container (all six translation blocks),
  * video captions (they are YouTube's titles),
  * anything inside quotation marks -- a quoted KJV verse keeps its KJV
    spelling ("The Lion of the tribe of Juda", "after the order of
    Melchisedec"), because changing it would misquote the verse.

Names deliberately left alone, because the prose uses them knowingly:
Jehovah, Sabaoth, Olivet, Beelzebub, Lucifer, Nethinim, Mazzaroth,
superscription terms (Maschil, Michtam, Shoshannim, Nehiloth), and places
where the text is explaining the KJV form itself ("Susa (Shushan)",
"Josheb-basshebeth/Adino", "Raguel/Reuel", "Joshua/Jehoshua",
"Noph is Memphis", "Socoh (KJV: Shochoh)").

    python3 fix_spelling_audit.py [--check]
"""
import glob
import html as htmllib
import os
import re
import sys

DOCS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "docs")

# KJV-only form -> ESV form, applied as whole words in unquoted prose.
NAMES = {
    "Elisabeth": "Elizabeth", "Zacharias": "Zechariah", "Abia": "Abijah",
    "Abiah": "Abijah", "Elias": "Elijah", "Jonas": "Jonah", "Noe": "Noah",
    "Thamar": "Tamar", "Rachab": "Rahab", "Urias": "Uriah",
    "Zabulon": "Zebulun", "Nephthalim": "Naphtali", "Judaea": "Judea",
    "Idumaea": "Idumea", "Arimathaea": "Arimathea", "Arphad": "Arpad",
    "Ashchenaz": "Ashkenaz", "Askelon": "Ashkelon", "Azur": "Azzur",
    "Bezaleel": "Bezalel", "Charchemish": "Carchemish",
    "Cherethims": "Cherethites", "Chittim": "Kittim",
    "Cononiah": "Conaniah", "Coos": "Cos", "Dodavah": "Dodavahu",
    "Enos": "Enosh", "Ephrain": "Ephron", "Ephratah": "Ephrathah",
    "Goath": "Goah", "Hadadrimmon": "Hadad-rimmon",
    "Hadarezer": "Hadadezer", "Hagarites": "Hagrites",
    "Hagarenes": "Hagrites", "Hanameel": "Hanamel", "Hananeel": "Hananel",
    "Imla": "Imlah", "Ivah": "Ivvah", "Jaazer": "Jazer",
    "Jahazah": "Jahzah", "Jechonias": "Jechoniah", "Josedech": "Jehozadak",
    "Jotbath": "Jotbathah", "Kirjath": "Kiriath", "Kison": "Kishon",
    "Malcham": "Milcom", "Mesech": "Meshech", "Michmethah": "Michmethath",
    "Nazarite": "Nazirite", "Nazarites": "Nazirites",
    "Nebuzar-adan": "Nebuzaradan", "Padan-aram": "Paddan-aram",
    "Palestina": "Philistia", "Pashur": "Pashhur", "Pergamos": "Pergamum",
    "Pharez": "Perez", "Phenicia": "Phoenicia", "Phut": "Put",
    "Phygellus": "Phygelus", "Pibeseth": "Pi-beseth", "Salcah": "Salecah",
    "Shechaniah": "Shecaniah", "Shenir": "Senir", "Sherah": "Sheerah",
    "Shulamite": "Shulammite", "Sibbechai": "Sibbecai", "Sion": "Zion",
    "Sodoma": "Sodom", "Tilgath-pilneser": "Tiglath-pileser",
    "Timotheus": "Timothy", "Tophet": "Topheth", "Tyrus": "Tyre",
    "Zaanaim": "Zaanannim", "Zarthan": "Zarethan", "Zidon": "Sidon",
    "Zidonians": "Sidonians", "Zaphnath-paaneah": "Zaphenath-paneah",
    "Berodach-baladan": "Merodach-baladan", "Diblath": "Riblah",
    "Urijah": "Uriah", "Rephaims": "Rephaim", "Shoco": "Soco",
    "Alleluia": "Hallelujah", "Aholah": "Oholah", "Aholibah": "Oholibah",
    "Baalim": "the Baals", "Chaldees": "Chaldeans",
}

# Occurrences of a NAMES key that must stay, as (file, text right after it).
KEEP = [
    ("micah1.html", "..."), ("micah2.html", "..."), ("micah3.html", "..."),
    ("micah4.html", "..."), ("micah5.html", "..."), ("micah6.html", "..."),
    ("micah7.html", "..."),                     # 'But thou, Bethlehem Ephratah...' (KJV quote)
]

# American spellings for British forms still in the site's own prose.
BRITISH = {
    "civilisation": "civilization", "harmonising": "harmonizing",
    "panelling": "paneling", "panelled": "paneled",
    "spiritualising": "spiritualizing", "penalised": "penalized",
    "internalised": "internalized", "judgement": "judgment",
    "judgements": "judgments", "judgementalism": "judgmentalism",
    "dishonours": "dishonors", "dishonoured": "dishonored",
    "summarising": "summarizing", "specialised": "specialized",
    "neutralised": "neutralized", "notarised": "notarized",
    "immobilisation": "immobilization", "moulds": "molds",
    "mobilise": "mobilize", "demobilisation": "demobilization",
    "outmanoeuvred": "outmaneuvered", "recognises": "recognizes",
    "recognising": "recognizing", "recognisable": "recognizable",
    "unrecognisable": "unrecognizable", "unrecognised": "unrecognized",
    "baptise": "baptize", "baptises": "baptizes",
    "baptised": "baptized", "baptising": "baptizing",
    "moralising": "moralizing", "authorising": "authorizing",
    "authorised": "authorized", "authorises": "authorizes",
    "authorisation": "authorization", "unauthorised": "unauthorized",
    "ploughman": "plowman", "ploughmen": "plowmen",
    "apologises": "apologizes", "apologising": "apologizing",
    "formalised": "formalized", "armourer": "armorer",
    "armouries": "armories", "relativised": "relativized",
    "relativises": "relativizes", "signalling": "signaling",
    "enquires": "inquires", "enquiring": "inquiring",
    "neighbouring": "neighboring", "moulting": "molting",
    "idealised": "idealized", "litres": "liters",
    "characterises": "characterizes", "favouritism": "favoritism",
    "favourite": "favorite", "defenceless": "defenseless",
    "centralising": "centralizing", "labelling": "labeling",
    "labelled": "labeled", "theatres": "theaters",
    "amphitheatre": "amphitheater", "paralysed": "paralyzed",
    "instalments": "installments", "minimising": "minimizing",
    "editorialise": "editorialize", "fulfilments": "fulfillments",
    "fulfils": "fulfills", "centred": "centered",
    "cancelling": "canceling", "scepticism": "skepticism",
    "storey": "story", "storeys": "stories", "candour": "candor",
    "organisation": "organization", "reorganisation": "reorganization",
    "organising": "organizing", "generalises": "generalizes",
    "levelling": "leveling", "itemised": "itemized",
    "harbour": "harbor", "harbours": "harbors",
}

# One-off rewrites: (file, old, new). Exact text, every occurrence.
PHRASES = [
    ("ezekiel23.html",
     "Samaria is Aholah, and Jerusalem Aholibah, spelled Oholah and Oholibah in most modern translations.",
     "Samaria is Oholah, and Jerusalem Oholibah, spelled Aholah and Aholibah in the KJV."),
    ("ezra6.html", "turns up at Achmetha, Ecbatana,", "turns up at Ecbatana,"),
    ("ezekiel27.html", "and Gammadims in the towers", "and men of Gamad in the towers"),
    ("zephaniah1.html", "and Maktesh,", "and the Mortar,"),
    ("psalms42.html", "and of the Hermonites, from the hill Mizar", "and of Hermon, from Mount Mizar"),
    ("jeremiah26.html", "Micah the Morasthite", "Micah of Moresheth"),
    ("1chronicles4.html", "the valley of Charashim being the valley of craftsmen",
     "Ge-harashim being the valley of craftsmen"),
    ("joshua18.html", "Ramah and Jebusi, which is Jerusalem", "Ramah and Jebus, which is Jerusalem"),
    ("luke6.html", "Simon called Zelotes", "Simon called the Zealot"),
    ("jeremiah2.html", "to drink the waters of Sihor", "to drink the waters of the Nile"),
    ("2chronicles16.html", "the Ethiopians and the Lubims", "the Ethiopians and the Libyans"),
    ("2chronicles16.html", "the Ethiopians and Lubims", "the Ethiopians and Libyans"),
    ("nahum3.html", "Put and Lubim for helpers", "Put and the Libyans for helpers"),
    ("jeremiah44.html", "Tahpanhes, Noph and Pathros", "Tahpanhes, Memphis and Pathros"),
    ("jeremiah46.html", "publish in Noph and", "publish in Memphis and"),
    ("zechariah12.html", "in the valley of Megiddon", "in the plain of Megiddo"),
    ("acts28.html", "as far as Appii forum", "as far as the Forum of Appius"),
    ("acts28.html", "The Appii Forum and the Three Taverns", "The Forum of Appius and the Three Taverns"),
    ("2samuel6.html", "at Nachon's threshing floor", "at Nacon's threshing floor"),
    ("romans16.html", "Timotheus, Tertius and Gaius", "Timothy, Tertius and Gaius"),
    # factual corrections: counts checked against the verse counts
    # (Psalm 117 has 2 verses, Psalm 87 has 7; Matthew 3 has 17, Matthew 28
    # has 20; Judges 20:17 musters 400,000, and 22,000 + 18,000 fall), and
    # claims softened where they are disputed or unsupported (no Egyptian
    # locust deity named Serapia is attested; Luke's Gentile identity is the
    # majority view, not a certainty; Judges 6:39 and Isaiah 7:11 also have
    # God inviting or permitting a test)
    ("psalms87.html", "This is the shortest psalm in the psalter and the strangest",
     "This is one of the shortest psalms in the psalter and one of the strangest"),
    ("matthew28.html", "It is the shortest chapter in Matthew but contains",
     "It is one of the shorter chapters in Matthew but contains"),
    ("exodus10.html", "Targets: Serapia (locust deity), Isis/Osiris (agriculture gods).",
     "Targets: Isis/Osiris (agriculture gods), whose crops the locusts strip."),
    ("luke1.html", "He is the only non-Jewish author in the New Testament.",
     "He is traditionally regarded as the only Gentile author in the New Testament."),
    ("judges20.html", "Total losses: 40,000 men — nearly 10% of their army.",
     "Total losses: 40,000 men — a tenth of their army."),
    ("malachi3.html", "This is the only place in Scripture where God invites testing.",
     "This is one of the very few places in Scripture where God invites testing."),
    # typos
    ("isaiah7.html", "telling him: don&#x27;T fear", "telling him: don&#x27;t fear"),
    ("1chronicles20.html", "giant- killing", "giant-killing"),
    ("2chronicles10.html", "servant- leadership", "servant-leadership"),
    ("esther5.html", "self- destructive", "self-destructive"),
    ("job3.html", "anti- creation", "anti-creation"),
    ("proverbs30.html", "anti- intellectualism", "anti-intellectualism"),
]

# Classic-KJV-vocabulary British spellings (honour, neighbour, labour, favour,
# defence, offence, rumour, behaviour, sceptre, ...) in the site's own voice.
# Same method as fix_kjv_vocab_spelling.py: every candidate outside quotation
# marks and not matching a >=20-character run of the page's KJV text was read
# in its sentence, and only those in the site's own analytical voice are
# listed. Echoes of a verse were left alone -- "labour of love" (1 Thess 1:3),
# "thou shalt find favour" (Prov 3:4), "fair colours" (Isa 54:11), "crowned
# with glory and honour" (Ps 8:5), "the sceptre shall not depart" (Gen 49:10),
# and every spot fix_kjv_vocab_spelling.py already ruled an echo (Luke 1:58,
# Luke 10:29/36, Habakkuk 2, Ecclesiastes 2:18-21, Proverbs 3:4 and 3:28-29).
# Entries are (file, exact raw-HTML text unique in that file, replacement).
VOCAB = [
    ('1chronicles20.html', ' forced labour', ' forced labor'),
    ('1chronicles26.html', 'y because he was a wise counsellor', 'y because he was a wise counselor'),
    ('1chronicles27.html', 'hen the counsellors', 'hen the counselors'),
    ('1corinthians15.html', 'es from behaviour', 'es from behavior'),
    ('1corinthians5.html', 'not the offence', 'not the offense'),
    ('1timothy6.html', 'cted to honour', 'cted to honor'),
    ('2chronicles2.html', 'ws. The labour', 'ws. The labor'),
    ('2chronicles20.html', 'mary is favourable', 'mary is favorable'),
    ('2chronicles26.html', 'on. The offence', 'on. The offense'),
    ('2chronicles33.html', 'r as unqualified as the offence', 'r as unqualified as the offense'),
    ('2chronicles33.html', 's as unqualified as the offence', 's as unqualified as the offense'),
    ('2corinthians1.html', 'ot. His defence', 'ot. His defense'),
    ('2corinthians7.html', ' Then a defence', ' Then a defense'),
    ('acts13.html', 'its the offence', 'its the offense'),
    ('acts16.html', 'serious offence', 'serious offense'),
    ('acts22.html', 'The Defence', 'The Defense'),
    ('acts24.html', 'er than rumour', 'er than rumor'),
    ('acts25.html', 'er as a favour', 'er as a favor'),
    ('acts26.html', 's whole defence', 's whole defense'),
    ('acts4.html', 'pecific offence', 'pecific offense'),
    ('esther5.html', 'door, a sceptre', 'door, a scepter'),
    ('esther5.html', ' Golden Sceptre', ' Golden Scepter'),
    ('esther5.html', 'niquely honoured', 'niquely honored'),
    ('ezekiel11.html', 'roof of favour', 'roof of favor'),
    ('ezekiel16.html', ' of the offence', ' of the offense'),
    ('ezekiel17.html', 'and the offence', 'and the offense'),
    ('ezekiel25.html', " Moab's offence", " Moab's offense"),
    ('ezekiel32.html', 'concern honourable', 'concern honorable'),
    ('ezekiel36.html', 'ing the neighbours', 'ing the neighbors'),
    ('ezekiel43.html', 'er. The offence', 'er. The offense'),
    ('ezekiel45.html', ' is not honour', ' is not honor'),
    ('ezekiel5.html', 'pecific offence', 'pecific offense'),
    ('ezra1.html', '. Their neighbours', '. Their neighbors'),
    ('ezra1.html', 'f their neighbours', 'f their neighbors'),
    ('ezra4.html', ' say to neighbours', ' say to neighbors'),
    ('hosea9.html', ' on the neighbours', ' on the neighbors'),
    ('isaiah47.html', 'was the labour', 'was the labor'),
    ('isaiah49.html', ' so the honour', ' so the honor'),
    ('isaiah61.html', 'hen the labour', 'hen the labor'),
    ('jeremiah12.html', 'ven the Neighbours', 'ven the Neighbors'),
    ('jeremiah17.html', 'et. His defence', 'et. His defense'),
    ('jeremiah22.html', 'on. The offence', 'on. The offense'),
    ('jeremiah22.html', 'it is a labour', 'it is a labor'),
    ('jeremiah22.html', ' labor offence', ' labor offense'),
    ('jeremiah32.html', 'mes the offence', 'mes the offense'),
    ('jeremiah51.html', " year's rumour", " year's rumor"),
    ('jeremiah6.html', ' is not defence', ' is not defense'),
    ('jeremiah8.html', ' to the offence', ' to the offense'),
    ('john12.html', 'ag. The defence', 'ag. The defense'),
    ('john12.html', "ather's honour", "ather's honor"),
    ('john5.html', ' The defence', ' The defense'),
    ('john5.html', 'es, and honour', 'es, and honor'),
    ('john8.html', 's about honour', 's about honor'),
    ('john9.html', 'hen the neighbours', 'hen the neighbors'),
    ('lamentations5.html', '; their labour', '; their labor'),
    ('luke17.html', 'Offences', 'Offenses'),
    ('luke3.html', 'ncestry defence', 'ncestry defense'),
    ('luke6.html', 'and the defence', 'and the defense'),
    ('luke7.html', 'out the behaviour', 'out the behavior'),
    ('luke9.html', 'sts the rumours', 'sts the rumors'),
    ('luke9.html', 'rst the rumours', 'rst the rumors'),
    ('malachi1.html', ': a son honours', ': a son honors'),
    ('malachi1.html', "s God's honour", "s God's honor"),
    ('malachi1.html', 'ne. The offence', 'ne. The offense'),
    ('mark12.html', ' public behaviour', ' public behavior'),
    ('mark14.html', 'and the defence', 'and the defense'),
    ('mark4.html', 'n about behaviour', 'n about behavior'),
    ('matthew16.html', 'eported rumours', 'eported rumors'),
    ('matthew26.html', 'or. The defence', 'or. The defense'),
    ('matthew27.html', 'd for a sceptre', 'd for a scepter'),
    ('matthew27.html', 'a worse rumour', 'a worse rumor'),
    ('matthew3.html', 'and the defence', 'and the defense'),
    ('matthew5.html', 'ther in favour', 'ther in favor'),
    ('nahum1.html', 'mes the offence', 'mes the offense'),
    ('nehemiah11.html', 'ublicly honoured', 'ublicly honored'),
    ('numbers24.html', 'n. The Star and Sceptre', 'n. The Star and Scepter'),
    ('numbers24.html', 'e: The Star and Sceptre', 'e: The Star and Scepter'),
    ('numbers24.html', 'de. The Sceptre', 'de. The Scepter'),
    ('numbers24.html', 'at the Star and Sceptre', 'at the Star and Scepter'),
    ('philippians1.html', 's legal defence', 's legal defense'),
    ('proverbs10.html', 'Speech, Labour', 'Speech, Labor'),
    ('proverbs24.html', 'between neighbours', 'between neighbors'),
    ('proverbs25.html', 'Honey, Neighbours', 'Honey, Neighbors'),
    ('proverbs6.html', "y for a neighbour's", "y for a neighbor's"),
    ('proverbs6.html', 's to be honoured', 's to be honored'),
    ('psalms103.html', 'cue and honour', 'cue and honor'),
    ('psalms105.html', 'lose to humour', 'lose to humor'),
    ('psalms11.html', 'And the counsellors', 'And the counselors'),
    ('psalms126.html', 'ven the neighbours', 'ven the neighbors'),
    ('psalms127.html', 'say the labour', 'say the labor'),
    ('psalms23.html', " host's honour", " host's honor"),
    ('psalms28.html', 'ts. The offence', 'ts. The offense'),
    ('psalms33.html', 'er than labour', 'er than labor'),
    ('psalms38.html', 'pposite behaviour', 'pposite behavior'),
    ('psalms41.html', ' double behaviour', ' double behavior'),
    ('psalms5.html', ' so the offence', ' so the offense'),
    ('psalms51.html', 'nes the offence', 'nes the offense'),
    ('psalms52.html', 'and the offence', 'and the offense'),
    ('romans10.html', 'ds in a defence', 'ds in a defense'),
    ('zechariah5.html', 'th. Two offences', 'th. Two offenses'),
]

# Shouted capitals in the site's own voice ("the exact OPPOSITE direction",
# "Job HAS been seeking God"), lowercased per WORKFLOW.md's prose-style rule,
# each read in context. Kept: capitals the KJV itself prints (THIS IS THE KING
# OF THE JEWS, HOLINESS TO THE LORD, TO THE UNKNOWN GOD, JESUS at Matthew
# 1:25), I AM WHO I AM, DNA. Two Revelation titles that mixed cases now read
# in full capitals, as the KJV prints them. Applied in order: where two
# shouted words stand together the second needle already has the first fixed.
CAPS = [
    ('1corinthians10.html', ' but escape THROUGH', ' but escape through'),
    ('acts1.html', ' what Jesus BEGAN', ' what Jesus began'),
    ('acts1.html', 'rds what He CONTINUES', 'rds what He continues'),
    ('acts7.html', 'ways worked OUTSIDE', 'ways worked outside'),
    ('acts7.html', ' has always REJECTED', ' has always rejected'),
    ('deuteronomy27.html', 'o one keeps ALL', 'o one keeps all'),
    ('deuteronomy30.html', 'passionate: CHOOSE', 'passionate: choose'),
    ('exodus14.html', 'praying and ACT', 'praying and act'),
    ('exodus7.html', '&#x27;s rod SWALLOWS', '&#x27;s rod swallows'),
    ('exodus8.html', 'plicate but CANNOT', 'plicate but cannot'),
    ('ezekiel1.html', 'ppearing in EXILE', 'ppearing in exile'),
    ('ezekiel10.html', 'sitioned to DEPART', 'sitioned to depart'),
    ('ezekiel14.html', ' INTERNAL', ' Internal'),
    ('ezekiel8.html', ' Idolatry INSIDE', ' Idolatry inside'),
    ('genesis2.html', ' everything EXCEPT', ' everything except'),
    ('genesis49.html', 'n 5:5). The SHILOH', 'n 5:5). The Shiloh'),
    ('genesis49.html', 'on 5:5). The Shiloh PROPHECY', 'on 5:5). The Shiloh prophecy'),
    ('jeremiah42.html', 'romising to REPLANT', 'romising to replant'),
    ('job11.html', 'You deserve WORSE', 'You deserve worse'),
    ('job19.html', 'who has the RIGHT', 'who has the right'),
    ('job19.html', 'o has the right and OBLIGATION', 'o has the right and obligation'),
    ('job21.html', 'et actually LISTENING', 'et actually listening'),
    ('job21.html', 'sponds: let HIM', 'sponds: let him'),
    ('job21.html', ' — that is, SPARED', ' — that is, spared'),
    ('job21.html', ' comfort is EMPTY', ' comfort is empty'),
    ('job23.html', 'ing purpose WHILE', 'ing purpose while'),
    ('job35.html', 'matters for HUMAN', 'matters for human'),
    ('job35.html', 'unfair: Job HAS', 'unfair: Job has'),
    ('job36.html', '(v.10), and COMMAND', '(v.10), and command'),
    ('job36.html', 'uffering as DISCIPLINE', 'uffering as discipline'),
    ('job36.html', 'rather than PUNISHMENT', 'rather than punishment'),
    ('job36.html', '. But it is CLOSER', '. But it is closer'),
    ('job37.html', 'oes what we CANNOT', 'oes what we cannot'),
    ('job37.html', 'does what we cannot COMPREHEND', 'does what we cannot comprehend'),
    ('job42.html', ' moved from HEARING', ' moved from hearing'),
    ('job42.html', 'heology) to SEEING', 'heology) to seeing'),
    ('job42.html', 'ess — spoke RIGHTLY', 'ess — spoke rightly'),
    ('job42.html', 'ogy — spoke WRONGLY', 'ogy — spoke wrongly'),
    ('job42.html', '8) and have JOB', '8) and have Job'),
    ('job42.html', 'essions) is NOT', 'essions) is not'),
    ('job7.html', 'y sin do to YOU', 'y sin do to you'),
    ('john17.html', 'ey are sent INTO', 'ey are sent into'),
    ('john17.html', 'it but kept FROM', 'it but kept from'),
    ('jonah1.html', '; the exact OPPOSITE', '; the exact opposite'),
    ('jonah2.html', '; the exact OPPOSITE', '; the exact opposite'),
    ('jonah3.html', '; the exact OPPOSITE', '; the exact opposite'),
    ('jonah4.html', '; the exact OPPOSITE', '; the exact opposite'),
    ('joshua24.html', 'thing — but WHOM', 'thing — but whom'),
    ('joshua3.html', 'had to step INTO', 'had to step into'),
    ('leviticus10.html', 'hat God had NOT', 'hat God had not'),
    ('leviticus11.html', 'ts 10), the PRINCIPLE', 'ts 10), the principle'),
    ('leviticus13.html', ' covers the ENTIRE', ' covers the entire'),
    ('leviticus13.html', 'onounce him CLEAN', 'onounce him clean'),
    ('leviticus13.html', ' one who is COMPLETELY', ' one who is completely'),
    ('leviticus13.html', 'st does not HEAL', 'st does not heal'),
    ('leviticus13.html', ' not heal — he only DIAGNOSES', ' not heal — he only diagnoses'),
    ('leviticus14.html', 'pology: Two BIRDS', 'pology: Two birds'),
    ('leviticus14.html', 'he heavens. CEDAR', 'he heavens. Cedar'),
    ('leviticus14.html', ' The cross. SCARLET', ' The cross. Scarlet'),
    ('leviticus14.html', 'aiah 1:18). HYSSOP', 'aiah 1:18). Hyssop'),
    ('leviticus14.html', 'ohn 19:29). EARTHEN', 'ohn 19:29). Earthen'),
    ('leviticus14.html', 'ohn 19:29). Earthen VESSEL', 'ohn 19:29). Earthen vessel'),
    ('leviticus14.html', 'hians 4:7). RUNNING', 'hians 4:7). Running'),
    ('leviticus14.html', 'hians 4:7). Running WATER', 'hians 4:7). Running water'),
    ('leviticus14.html', 'n 7:38-39). SEVEN', 'n 7:38-39). Seven'),
    ('leviticus14.html', 'ohn 7:38-39). Seven TIMES', 'ohn 7:38-39). Seven times'),
    ('leviticus14.html', '(v.11). The GUILT', '(v.11). The guilt'),
    ('leviticus14.html', 'e (v.11). The guilt/TRESPASS', 'e (v.11). The guilt/trespass'),
    ('leviticus14.html', 'oly (v.13). BLOOD', 'oly (v.13). Blood'),
    ('leviticus14.html', ' holy (v.13). Blood APPLICATION', ' holy (v.13). Blood application'),
    ('leviticus14.html', '4). This is IDENTICAL', '4). This is identical'),
    ('leviticus14.html', 'to God. Oil APPLICATION', 'to God. Oil application'),
    ('leviticus14.html', '(v.18). Sin OFFERING', '(v.18). Sin offering'),
    ('leviticus14.html', 'ess (v.19). BURNT', 'ess (v.19). Burnt'),
    ('leviticus14.html', 'nness (v.19). Burnt OFFERING', 'nness (v.19). Burnt offering'),
    ('leviticus14.html', ' Burnt offering and GRAIN', ' Burnt offering and grain'),
    ('leviticus14.html', ' offering and grain OFFERING', ' offering and grain offering'),
    ('leviticus14.html', 'led (v.48). CLEANSING', 'led (v.48). Cleansing'),
    ('leviticus14.html', 'd (v.48). Cleansing CEREMONY', 'd (v.48). Cleansing ceremony'),
    ('leviticus20.html', ' purpose of BELONGING', ' purpose of belonging'),
    ('leviticus23.html', 'rist&#x27;s RESURRECTION', 'rist&#x27;s resurrection'),
    ('leviticus23.html', ' baked with LEAVEN', ' baked with leaven'),
    ('leviticus23.html', 'They are in ADDITION', 'They are in addition'),
    ('leviticus24.html', 'rinciple of PROPORTIONAL', 'rinciple of proportional'),
    ('leviticus24.html', 'ple of proportional JUSTICE', 'ple of proportional justice'),
    ('leviticus25.html', 'is requires FAITH', 'is requires faith'),
    ('leviticus27.html', 'dedicates a PURCHASED', 'dedicates a purchased'),
    ('leviticus6.html', 'e fire must NEVER', 'e fire must never'),
    ('names-of-god.html', 'chose to be WITH', 'chose to be with'),
    ('numbers20.html', ' rod... and SPEAK', ' rod... and speak'),
    ('numbers23.html', 'iar and who DOES', 'iar and who does'),
    ('proverbs12.html', "ool doesn't KNOW", "ool doesn't know"),
    ('proverbs13.html', 'ing claim: "ONLY', 'ing claim: "Only'),
    ('proverbs14.html', 'elings: "it SEEMS', 'elings: "it seems'),
    ('proverbs16.html', ' pride is a WARNING', ' pride is a warning'),
    ('proverbs16.html', ' pride is a warning SIGN', ' pride is a warning sign'),
    ('proverbs24.html', ' learned by OBSERVATION', ' learned by observation'),
    ('proverbs26.html', 'mes he must NOT', 'mes he must not'),
    ('proverbs27.html', "'s wound is FAITHFUL", "'s wound is faithful"),
    ('proverbs27.html', "y's kiss is DECEITFUL", "y's kiss is deceitful"),
    ('proverbs29.html', 'line but to SUDDEN', 'line but to sudden'),
    ('proverbs31.html', 'a woman who FEARS', 'a woman who fears'),
    ('proverbs4.html', 'must be the TOP', 'must be the top'),
    ('proverbs8.html', 'eath — they LOVE', 'eath — they love'),
    ('romans6.html', 'appened) to FAITH', 'appened) to faith'),
    ('songofsolomon6.html', "om's praise AFTER", "om's praise after"),
    ('job3.html', 'directed TO God, not AWAY', 'directed to God, not away'),
    ("revelation17.html", "mystery, BABYLON the great, the MOTHER of HARLOTS",
     "MYSTERY, BABYLON THE GREAT, THE MOTHER OF HARLOTS"),
    ("revelation19.html", "KING of KINGS, and LORD of LORDS",
     "KING OF KINGS, AND LORD OF LORDS"),
]

TAG = re.compile(r"<[^>]*>")


def excluded_ranges(h):
    ex = []
    for m in re.finditer(r"<(script|style)\b.*?</\1>", h, re.S):
        ex.append((m.start(), m.end()))
    for m in re.finditer(r"<head>.*?</head>", h, re.S):
        ex.append((m.start(), m.end()))
    s = h.find('<div class="scripture-container">')
    if s >= 0:
        e = h.find('<div class="study-section">', s)
        ex.append((s, e if e > 0 else len(h)))
    s = h.find('id="tab-videos"')
    if s >= 0:
        e = h.find('<div class="tab-content"', s)
        ex.append((s, e if e > 0 else len(h)))
    for m in re.finditer(r"^.*(yt-facade|yt-src|video-card).*$", h, re.M):
        ex.append((m.start(), m.end()))
    return ex


def text_spans(h):
    ex = excluded_ranges(h)
    pos = 0
    for m in TAG.finditer(h + "<x>"):
        if m.start() > pos and not any(a <= pos < b for a, b in ex):
            yield pos, m.start()
        pos = m.end()


def in_quote(h, i):
    s = max(h.rfind('<div class="auth-item">', 0, i), h.rfind("<li", 0, i),
            h.rfind("<p", 0, i), h.rfind("<h", 0, i))
    pre = htmllib.unescape(TAG.sub("", h[s:i]))
    return pre.count("“") > pre.count("”") or pre.count('"') % 2 == 1


def case_like(src, rep):
    if src[:1].isupper():
        return rep[:1].upper() + rep[1:]
    return rep


def build(words, flags=0):
    return re.compile(r"(?<![\w-])(" + "|".join(
        re.escape(w) for w in sorted(words, key=len, reverse=True)) + r")(?!\w)", flags)


NAME_RE = build(NAMES)
BRIT_RE = build(BRITISH, re.I)


def fix_file(path):
    name = os.path.basename(path)
    h = open(path, encoding="utf-8").read()
    changes = []
    for fname, old, new in PHRASES + VOCAB + CAPS:
        if fname == name and old in h:
            h = h.replace(old, new)
            changes.append((old, new))
    edits = []
    for a, b in text_spans(h):
        for m in NAME_RE.finditer(h, a, b):
            if in_quote(h, m.start()):
                continue
            if any(f == name and h.startswith(after, m.end()) for f, after in KEEP):
                continue
            rep, end = NAMES[m.group(1)], m.end()
            # Zacharias' -> Zechariah's: a possessive needs its s back
            pm = re.match(r"('|&#x27;|’)(?!s\b)", h[end:end + 7])
            if m.group(1).endswith("s") and not rep.endswith("s") and pm:
                rep, end = rep + pm.group(1) + "s", end + len(pm.group(1))
            edits.append((m.start(), end, rep))
        for m in BRIT_RE.finditer(h, a, b):
            w = m.group(1)
            if in_quote(h, m.start()):
                continue
            rep = BRITISH[w.lower()]
            edits.append((m.start(), m.end(), case_like(w, rep)))
    for s, e, rep in sorted(edits, reverse=True):
        # "the Baals" after a word that already supplies an article
        if rep == "the Baals" and h[max(0, s - 4):s].lower() == "the ":
            rep = "Baals"
        changes.append((h[s:e], rep))
        h = h[:s] + rep + h[e:]
    return h, changes


def main():
    check = "--check" in sys.argv
    total = 0
    for path in sorted(glob.glob(os.path.join(DOCS, "*.html"))):
        new, changes = fix_file(path)
        if not changes:
            continue
        total += len(changes)
        print(f"{os.path.basename(path)}: " + ", ".join(f"{o} -> {n}" for o, n in changes))
        if not check:
            open(path, "w", encoding="utf-8").write(new)
    print(f"{total} change(s){' (check only)' if check else ''}")


if __name__ == "__main__":
    main()
