#!/usr/bin/env python3
"""
Bible Study Site Builder
========================
Reads .txt study notes and translation files, generates HTML pages
in the new design format. Run this after any content update.

Usage: python build_site.py
"""

import os
import re
import html

# Base directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "docs")

# Book data
OT_BOOKS = [
    ("01", "Genesis", 50), ("02", "Exodus", 40), ("03", "Leviticus", 27),
    ("04", "Numbers", 36), ("05", "Deuteronomy", 34), ("06", "Joshua", 24),
    ("07", "Judges", 21), ("08", "Ruth", 4), ("09", "1 Samuel", 31),
    ("10", "2 Samuel", 24), ("11", "1 Kings", 22), ("12", "2 Kings", 25),
    ("13", "1 Chronicles", 29), ("14", "2 Chronicles", 36), ("15", "Ezra", 10),
    ("16", "Nehemiah", 13), ("17", "Esther", 10), ("18", "Job", 42),
    ("19", "Psalms", 150), ("20", "Proverbs", 31), ("21", "Ecclesiastes", 12),
    ("22", "Song of Solomon", 8), ("23", "Isaiah", 66), ("24", "Jeremiah", 52),
    ("25", "Lamentations", 5), ("26", "Ezekiel", 48), ("27", "Daniel", 12),
    ("28", "Hosea", 14), ("29", "Joel", 3), ("30", "Amos", 9),
    ("31", "Obadiah", 1), ("32", "Jonah", 4), ("33", "Micah", 7),
    ("34", "Nahum", 3), ("35", "Habakkuk", 3), ("36", "Zephaniah", 3),
    ("37", "Haggai", 2), ("38", "Zechariah", 14), ("39", "Malachi", 4),
]

NT_BOOKS = [
    ("01", "Matthew", 28), ("02", "Mark", 16), ("03", "Luke", 24),
    ("04", "John", 21), ("05", "Acts", 28), ("06", "Romans", 16),
    ("07", "1 Corinthians", 16), ("08", "2 Corinthians", 13),
    ("09", "Galatians", 6), ("10", "Ephesians", 6), ("11", "Philippians", 4),
    ("12", "Colossians", 4), ("13", "1 Thessalonians", 5),
    ("14", "2 Thessalonians", 3), ("15", "1 Timothy", 6),
    ("16", "2 Timothy", 4), ("17", "Titus", 3), ("18", "Philemon", 1),
    ("19", "Hebrews", 13), ("20", "James", 5), ("21", "1 Peter", 5),
    ("22", "2 Peter", 3), ("23", "1 John", 5), ("24", "2 John", 1),
    ("25", "3 John", 1), ("26", "Jude", 1), ("27", "Revelation", 22),
]

def book_slug(name):
    """Convert book name to URL slug: '1 Corinthians' -> '1corinthians'"""
    return name.lower().replace(" ", "")


def read_file_safe(path):
    """Read a file, return empty string if not found."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return ""


def parse_verses(text):
    """Parse translation text file into list of (number, text) tuples."""
    verses = []
    for line in text.strip().split("\n"):
        m = re.match(r"^(\d+)\.\s+(.+)$", line)
        if m:
            verses.append((m.group(1), m.group(2)))
    return verses


def parse_study_notes(text):
    """Parse study notes into sections dict."""
    sections = {}
    current_section = None
    current_lines = []

    for line in text.split("\n"):
        # Section headers are ALL CAPS followed by dashes
        if re.match(r"^[A-Z][A-Z &\-]+$", line.strip()) and len(line.strip()) > 3:
            if current_section:
                sections[current_section] = "\n".join(current_lines).strip()
            current_section = line.strip()
            current_lines = []
        elif line.strip().startswith("----"):
            continue
        elif current_section:
            current_lines.append(line)

    if current_section:
        sections[current_section] = "\n".join(current_lines).strip()

    return sections


def escape(text):
    """HTML escape."""
    return html.escape(text)

def render_verses_html(verses):
    """Render verses as HTML paragraphs."""
    lines = []
    for num, text in verses:
        lines.append(f'            <p class="verse"><span class="verse-num">{num}</span>{escape(text)}</p>')
    return "\n".join(lines)


def render_section_as_list(text):
    """Render a text section as HTML list items."""
    # First try splitting on lines that start with v.X pattern (cross-references)
    # This handles cases where entries aren't separated by blank lines
    lines = text.strip().split("\n")
    items = []
    current = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            if current:
                items.append(" ".join(current))
                current = []
        elif re.match(r'^v\.?\d', stripped) and current:
            # New verse reference starts - save previous and start new
            items.append(" ".join(current))
            current = [stripped]
        else:
            current.append(stripped)
    if current:
        items.append(" ".join(current))

    html_items = []
    for item in items:
        if item:
            # Convert URLs to links first (show clean domain name)
            item = re.sub(r'(https?://)([^/\s]+)(/\S*)', r'<a href="\1\2\3" target="_blank">\2</a>', item)
            # Bold commentary source names (like "Enduring Word (David Guzik):")
            item = re.sub(r'^([A-Z][^:]+:)\s*', r'<strong>\1</strong> ', item)
            # Format cross-reference pattern: v.X — Reference — "quote"
            item = re.sub(r'^(v\.?\d+\S*)\s*[—–-]\s*', r'<strong>\1</strong> → ', item)
            # Bold standalone scripture references at start
            item = re.sub(r'^(\d?\s?[A-Z][a-z]+ \d+[:\d\-,]*)\s*[—–-]\s*', r'<strong>\1</strong> — ', item)
            # Bold translation abbreviations (KJV, ESV, ASV, NET, WEB)
            item = re.sub(r'\b(KJV|ESV|ASV|NET|WEB):', r'<strong>\1:</strong>', item)
            # Convert / between translations to arrow
            item = re.sub(r'\s*/\s*(?=(KJV|ESV|ASV|NET|WEB|<strong>))', r' → ', item)
            html_items.append(f"                    <li>{item}</li>")
    return "\n".join(html_items)


def render_video_cards(text):
    """Render video resources as styled cards."""
    cards = []
    entries = re.split(r'\n(?=\S)', text.strip())
    for entry in entries:
        if not entry.strip():
            continue
        lines = entry.strip().split("\n")
        title = lines[0].rstrip(":")
        url = ""
        desc_lines = []
        for line in lines[1:]:
            line = line.strip()
            url_match = re.match(r'(https?://\S+)', line)
            if url_match and not url:
                url = url_match.group(1)
            elif line and not line.startswith("http"):
                desc_lines.append(line)
        desc = " ".join(desc_lines)
        if title:
            link = f'<a href="{url}" target="_blank">{escape(title)}</a>' if url else escape(title)
            cards.append(f'''                <div class="video-card">
                    <div class="video-card-icon"><i class="fab fa-youtube"></i></div>
                    <div class="video-card-info">
                        <h4>{link}</h4>
                        <p>{escape(desc)}</p>
                    </div>
                </div>''')
    return "\n".join(cards)


# Wikipedia links for common biblical locations
LOCATION_WIKI_LINKS = {
    "jerusalem": "https://en.wikipedia.org/wiki/Jerusalem",
    "bethlehem": "https://en.wikipedia.org/wiki/Bethlehem",
    "nazareth": "https://en.wikipedia.org/wiki/Nazareth",
    "capernaum": "https://en.wikipedia.org/wiki/Capernaum",
    "sea of galilee": "https://en.wikipedia.org/wiki/Sea_of_Galilee",
    "galilee": "https://en.wikipedia.org/wiki/Galilee",
    "jordan river": "https://en.wikipedia.org/wiki/Jordan_River",
    "jordan": "https://en.wikipedia.org/wiki/Jordan_River",
    "egypt": "https://en.wikipedia.org/wiki/Ancient_Egypt",
    "nile": "https://en.wikipedia.org/wiki/Nile",
    "nile river": "https://en.wikipedia.org/wiki/Nile",
    "sinai": "https://en.wikipedia.org/wiki/Mount_Sinai",
    "mount sinai": "https://en.wikipedia.org/wiki/Mount_Sinai",
    "horeb": "https://en.wikipedia.org/wiki/Mount_Sinai",
    "mount horeb": "https://en.wikipedia.org/wiki/Mount_Sinai",
    "babylon": "https://en.wikipedia.org/wiki/Babylon",
    "assyria": "https://en.wikipedia.org/wiki/Assyria",
    "persia": "https://en.wikipedia.org/wiki/Achaemenid_Empire",
    "rome": "https://en.wikipedia.org/wiki/Ancient_Rome",
    "ephesus": "https://en.wikipedia.org/wiki/Ephesus",
    "corinth": "https://en.wikipedia.org/wiki/Ancient_Corinth",
    "antioch": "https://en.wikipedia.org/wiki/Antioch",
    "damascus": "https://en.wikipedia.org/wiki/Damascus",
    "samaria": "https://en.wikipedia.org/wiki/Samaria",
    "jericho": "https://en.wikipedia.org/wiki/Jericho",
    "bethany": "https://en.wikipedia.org/wiki/Bethany_(biblical_village)",
    "mount of olives": "https://en.wikipedia.org/wiki/Mount_of_Olives",
    "mount olives": "https://en.wikipedia.org/wiki/Mount_of_Olives",
    "gethsemane": "https://en.wikipedia.org/wiki/Gethsemane",
    "golgotha": "https://en.wikipedia.org/wiki/Calvary",
    "calvary": "https://en.wikipedia.org/wiki/Calvary",
    "dead sea": "https://en.wikipedia.org/wiki/Dead_Sea",
    "red sea": "https://en.wikipedia.org/wiki/Red_Sea",
    "mount hermon": "https://en.wikipedia.org/wiki/Mount_Hermon",
    "tyre": "https://en.wikipedia.org/wiki/Tyre,_Lebanon",
    "sidon": "https://en.wikipedia.org/wiki/Sidon",
    "caesarea philippi": "https://en.wikipedia.org/wiki/Caesarea_Philippi",
    "caesarea": "https://en.wikipedia.org/wiki/Caesarea_Maritima",
    "decapolis": "https://en.wikipedia.org/wiki/Decapolis",
    "phoenicia": "https://en.wikipedia.org/wiki/Phoenicia",
    "kidron valley": "https://en.wikipedia.org/wiki/Kidron_Valley",
    "temple mount": "https://en.wikipedia.org/wiki/Temple_Mount",
    "hebron": "https://en.wikipedia.org/wiki/Hebron",
    "beersheba": "https://en.wikipedia.org/wiki/Beersheba",
    "shechem": "https://en.wikipedia.org/wiki/Shechem",
    "bethel": "https://en.wikipedia.org/wiki/Bethel",
    "shiloh": "https://en.wikipedia.org/wiki/Shiloh_(biblical_city)",
    "ur": "https://en.wikipedia.org/wiki/Ur",
    "haran": "https://en.wikipedia.org/wiki/Harran",
    "canaan": "https://en.wikipedia.org/wiki/Canaan",
    "philistia": "https://en.wikipedia.org/wiki/Philistia",
    "moab": "https://en.wikipedia.org/wiki/Moab",
    "edom": "https://en.wikipedia.org/wiki/Edom",
    "ammon": "https://en.wikipedia.org/wiki/Ammon",
    "nineveh": "https://en.wikipedia.org/wiki/Nineveh",
    "tarshish": "https://en.wikipedia.org/wiki/Tarshish",
    "patmos": "https://en.wikipedia.org/wiki/Patmos",
    "thessalonica": "https://en.wikipedia.org/wiki/Thessaloniki",
    "philippi": "https://en.wikipedia.org/wiki/Philippi",
    "galatia": "https://en.wikipedia.org/wiki/Galatia",
    "colossae": "https://en.wikipedia.org/wiki/Colossae",
    "crete": "https://en.wikipedia.org/wiki/Crete",
    "malta": "https://en.wikipedia.org/wiki/Malta",
    "athens": "https://en.wikipedia.org/wiki/Athens",
    "mount carmel": "https://en.wikipedia.org/wiki/Mount_Carmel",
    "mount zion": "https://en.wikipedia.org/wiki/Mount_Zion",
    "petra": "https://en.wikipedia.org/wiki/Petra",
    "tigris": "https://en.wikipedia.org/wiki/Tigris",
    "euphrates": "https://en.wikipedia.org/wiki/Euphrates",
    "mediterranean": "https://en.wikipedia.org/wiki/Mediterranean_Sea",
    "perea": "https://en.wikipedia.org/wiki/Perea",
    "idumea": "https://en.wikipedia.org/wiki/Idumea",
    "wilderness of judea": "https://en.wikipedia.org/wiki/Judean_Desert",
    "judean wilderness": "https://en.wikipedia.org/wiki/Judean_Desert",
    "mount tabor": "https://en.wikipedia.org/wiki/Mount_Tabor",
    "dan": "https://en.wikipedia.org/wiki/Tel_Dan",
    "megiddo": "https://en.wikipedia.org/wiki/Megiddo",
    "armageddon": "https://en.wikipedia.org/wiki/Tel_Megiddo",
    "carchemish": "https://en.wikipedia.org/wiki/Carchemish",
    "thebes": "https://en.wikipedia.org/wiki/Thebes,_Egypt",
    "memphis": "https://en.wikipedia.org/wiki/Memphis,_Egypt",
    "heshbon": "https://en.wikipedia.org/wiki/Heshbon",
    "gilead": "https://en.wikipedia.org/wiki/Gilead",
    "bashan": "https://en.wikipedia.org/wiki/Bashan",
    "lebanon": "https://en.wikipedia.org/wiki/Lebanon",
    "mount nebo": "https://en.wikipedia.org/wiki/Mount_Nebo",
    "midian": "https://en.wikipedia.org/wiki/Midian",
    "gaza": "https://en.wikipedia.org/wiki/Gaza_City",
    "tekoa": "https://en.wikipedia.org/wiki/Tekoa,_Gush_Etzion",
}


def render_authorship(text):
    """Render authorship & historical background as clean bullet points by paragraph."""
    paragraphs = re.split(r'\n\s*\n', text.strip())
    items = []

    for para in paragraphs:
        if not para.strip():
            continue
        # Join multi-line paragraphs into single lines
        joined = " ".join(line.strip() for line in para.strip().split("\n") if line.strip())
        if not joined:
            continue

        # Check if paragraph has a label like "Author:", "Historical Context:", etc.
        label_match = re.match(r'^([A-Za-z][^:]{2,40}):\s*(.+)', joined)
        if label_match:
            label = label_match.group(1).strip()
            content = label_match.group(2).strip()
            items.append(f'                    <li><strong>{escape(label)}:</strong> {escape(content)}</li>')
        else:
            items.append(f'                    <li>{escape(joined)}</li>')

    if items:
        return "<ul>\n" + "\n".join(items) + "\n                </ul>"
    return "<p>No authorship information available for this chapter.</p>"


def render_map_geography(text):
    """Render map & geography notes as a list with Wikipedia links for locations."""
    lines = text.strip().split("\n")
    items = []
    current = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            if current:
                items.append(" ".join(current))
                current = []
        elif stripped.startswith("-") or stripped.startswith("•"):
            if current:
                items.append(" ".join(current))
            current = [stripped.lstrip("-•").strip()]
        else:
            current.append(stripped)
    if current:
        items.append(" ".join(current))

    html_items = []
    for item in items:
        if not item:
            continue
        escaped_item = escape(item)
        # Try to link known locations - case insensitive matching
        for location, wiki_url in sorted(LOCATION_WIKI_LINKS.items(), key=lambda x: -len(x[0])):
            # Use word boundary matching on the escaped text
            pattern = re.compile(re.escape(escape(location)), re.IGNORECASE)
            match = pattern.search(escaped_item)
            if match:
                matched_text = match.group(0)
                escaped_item = escaped_item.replace(
                    matched_text,
                    f'<a href="{wiki_url}" target="_blank" style="color:#8b3a2a;text-decoration:none;border-bottom:1px dotted #8b3a2a;">{matched_text}</a>',
                    1  # Only replace first occurrence
                )
        html_items.append(f"                    <li>{escaped_item}</li>")

    if html_items:
        return "<ul>\n" + "\n".join(html_items) + "\n                </ul>"
    return "<p>No geography notes available for this chapter.</p>"


def render_glossary(text):
    """Legacy glossary renderer - kept for fallback."""
    return ""


# Dictionary of uncommon/archaic English words found in Bible translations with definitions
UNCOMMON_WORDS = {
    "hath": "has",
    "doth": "does",
    "thee": "you (singular, object form)",
    "thou": "you (singular, subject form)",
    "thy": "your (singular possessive)",
    "thine": "yours / your (before a vowel)",
    "ye": "you (plural)",
    "wherefore": "why; for what reason",
    "thereof": "of that; of it",
    "therein": "in that place; in that matter",
    "thereto": "to that; in addition",
    "wherein": "in which; in what",
    "whereby": "by which; by what means",
    "wherewith": "with which; with what",
    "hitherto": "until now; up to this point",
    "thither": "to that place; there",
    "hither": "to this place; here",
    "whither": "to where; to what place",
    "hence": "from this place; from now",
    "thence": "from that place; from that time",
    "forthwith": "immediately; without delay",
    "straightway": "immediately; at once",
    "peradventure": "perhaps; possibly",
    "notwithstanding": "nevertheless; in spite of",
    "inasmuch": "to the extent that; since",
    "forasmuch": "since; because",
    "howbeit": "nevertheless; however",
    "albeit": "although; even though",
    "lest": "for fear that; in order to prevent",
    "nay": "no; not so",
    "yea": "yes; indeed",
    "verily": "truly; certainly",
    "behold": "look; see; pay attention",
    "lo": "look; see (exclamation)",
    "woe": "grief; sorrow; a curse",
    "wist": "knew; was aware",
    "wot": "know; knows",
    "wroth": "angry; furious",
    "sore": "greatly; severely; very much",
    "selah": "a musical or liturgical pause (meaning uncertain)",
    "begat": "fathered; was the parent of",
    "begotten": "fathered; brought into being",
    "brethren": "brothers; fellow believers",
    "damsel": "a young unmarried woman",
    "raiment": "clothing; garments",
    "vesture": "clothing; a garment",
    "girdle": "a belt or sash worn around the waist",
    "loins": "the area of the hips and lower abdomen",
    "victuals": "food; provisions",
    "kine": "cows; cattle",
    "oxen": "plural of ox; domesticated cattle",
    "hart": "a male deer; stag",
    "hind": "a female deer",
    "cockatrice": "a venomous serpent",
    "leviathan": "a great sea creature",
    "behemoth": "a massive beast",
    "firmament": "the sky; the expanse of heaven",
    "tabernacle": "a tent or temporary dwelling; the portable sanctuary",
    "ephod": "a priestly garment worn over the chest",
    "cubit": "a unit of measurement, about 18 inches / 45 cm",
    "shekel": "a unit of weight/currency, about 11 grams",
    "ephah": "a dry measure, about 22 liters or 3/5 bushel",
    "hin": "a liquid measure, about 6 liters or 1.5 gallons",
    "sojourn": "to live temporarily in a place; to dwell as a foreigner",
    "sojourner": "a temporary resident; a foreigner",
    "bondage": "slavery; forced servitude",
    "handmaid": "a female servant",
    "concubine": "a secondary wife with lower legal status",
    "harlot": "a prostitute",
    "smite": "to strike; to hit forcefully",
    "smote": "struck; hit (past tense of smite)",
    "smitten": "struck; afflicted",
    "slay": "to kill",
    "slew": "killed (past tense of slay)",
    "slain": "killed (past participle of slay)",
    "prevail": "to overcome; to be stronger than",
    "entreat": "to plead with; to ask earnestly",
    "beseech": "to beg; to implore earnestly",
    "supplication": "a humble, earnest prayer or request",
    "propitiation": "a sacrifice that turns away God's wrath",
    "atonement": "reconciliation with God through sacrifice",
    "expiation": "making amends for guilt or wrongdoing",
    "remission": "forgiveness; cancellation of a penalty",
    "transgression": "a violation of God's law; sin",
    "trespass": "a sin; an offense against God or another",
    "iniquity": "wickedness; moral perversity; gross injustice",
    "abomination": "something intensely detestable to God",
    "blasphemy": "speaking irreverently about God",
    "covet": "to desire intensely what belongs to another",
    "concupiscence": "strong sinful desire; lust",
    "lasciviousness": "unrestrained sensuality; shameless immorality",
    "wantonness": "reckless disregard for morality",
    "fornication": "sexual immorality; sex outside marriage",
    "profane": "to treat something sacred with disrespect",
    "defile": "to make unclean; to pollute; to corrupt",
    "sanctify": "to set apart as holy; to make pure",
    "consecrate": "to dedicate formally to God's service",
    "hallowed": "made holy; set apart as sacred",
    "justification": "being declared righteous by God",
    "impute": "to credit or attribute to someone's account",
    "quicken": "to make alive; to give life to",
    "quickened": "made alive; given spiritual life",
    "edify": "to build up spiritually; to instruct",
    "exhort": "to strongly urge or encourage",
    "admonish": "to warn or reprimand gently but firmly",
    "rebuke": "to express sharp disapproval; to reprimand",
    "reprove": "to correct; to express disapproval",
    "chasten": "to discipline; to correct through suffering",
    "chastise": "to punish in order to correct",
    "longsuffering": "patient endurance; slow to anger",
    "forbearance": "patient self-control; restraint",
    "temperance": "self-control; moderation",
    "meekness": "gentle strength; humility under control",
    "lovingkindness": "God's steadfast, loyal love; mercy",
    "propitiation": "an atoning sacrifice satisfying God's justice",
    "reconciliation": "restoration of relationship with God",
    "redemption": "deliverance by payment of a ransom",
    "sanctification": "the process of being made holy",
    "predestination": "God's sovereign determination beforehand",
    "omnipotent": "all-powerful; having unlimited power",
    "omniscient": "all-knowing; having unlimited knowledge",
    "immutable": "unchangeable; cannot be altered",
    "efficacious": "producing the intended effect; effective",
    "circumcise": "to cut away the foreskin as a covenant sign",
    "tithe": "a tenth of income given to God",
    "firstfruits": "the first portion of harvest, offered to God",
    "oblation": "an offering or sacrifice presented to God",
    "libation": "a liquid offering poured out before God",
    "frankincense": "a fragrant resin burned as incense",
    "myrrh": "a costly aromatic resin for anointing/embalming",
    "hyssop": "a plant used for sprinkling in purification",
    "sackcloth": "coarse fabric worn as a sign of mourning",
    "phylactery": "a small box containing Scripture, worn on the body",
    "proselyte": "a convert to Judaism from another religion",
    "publican": "a tax collector (often despised)",
    "centurion": "a Roman officer commanding 100 soldiers",
    "sepulchre": "a tomb; a burial place carved in rock",
    "palsy": "paralysis; inability to move",
    "infirmity": "physical weakness or illness",
    "dropsy": "edema; swelling from fluid retention",
    "pestilence": "a deadly epidemic disease; plague",
    "dearth": "a scarcity; famine",
    "wrath": "intense anger; God's fury against sin",
    "indignation": "anger provoked by injustice",
    "vengeance": "divine retribution; punishment in return",
    "recompense": "reward or punishment for actions",
    "requite": "to repay; to make return for",
    "remnant": "a small surviving group; those who remain faithful",
    "posterity": "all future generations; descendants",
    "kindred": "relatives; family; people of same ancestry",
    "birthright": "the rights and inheritance of the firstborn",
    "usury": "interest charged on a loan",
    "surety": "a guarantee; one who pledges for another",
    "mammon": "wealth or riches, especially as an idol",
    "alms": "charitable gifts to the poor",
    "dissimulation": "hypocrisy; hiding true feelings",
    "guile": "deceitful cunning; craftiness",
    "subtil": "crafty; cunning; slyly deceptive",
    "froward": "stubbornly contrary; perverse",
    "gainsay": "to speak against; to contradict",
    "nought": "nothing; zero; worthlessness",
    "asunder": "apart; into pieces; separated",
    "twain": "two",
    "manifold": "many and various; numerous",
    "divers": "various; several different kinds",
    "ere": "before (in time)",
    "anon": "soon; shortly; immediately",
    "betimes": "early; in good time; promptly",
    "withal": "in addition; moreover; as well",
    "haply": "perhaps; by chance",
    "privily": "secretly; privately",
    "succour": "help; assistance in time of need",
    "travail": "painful labor; hard work; childbirth pain",
    "vex": "to annoy; to distress; to torment",
    "upbraid": "to scold harshly; to criticize severely",
    "gainsayers": "those who speak against; opposers",
    "reprobate": "morally unprincipled; rejected by God",
    "perdition": "eternal damnation; utter destruction",
    "tribulation": "great suffering; severe affliction",
    "desolation": "complete emptiness; devastation; ruin",
    "affliction": "suffering; distress; trouble",
    "vouchsafe": "to grant in a gracious manner",
    "sufferance": "patient endurance; tolerance",
    "shew": "show; display; make known",
    "shewed": "showed (past tense)",
    "spake": "spoke (past tense of speak)",
    "saith": "says",
    "cometh": "comes",
    "goeth": "goes",
    "doeth": "does",
    "giveth": "gives",
    "maketh": "makes",
    "taketh": "takes",
    "abideth": "remains; stays",
    "bringeth": "brings",
    "keepeth": "keeps",
    "knoweth": "knows",
    "liveth": "lives",
    "loveth": "loves",
    "passeth": "passes; surpasses",
    "seeketh": "seeks",
    "sendeth": "sends",
    "speaketh": "speaks",
    "worketh": "works",
    "pertaineth": "belongs to; relates to",
    "remaineth": "remains",
    "pleaseth": "pleases",
    "perisheth": "perishes",
    "endureth": "endures",
    "dwelleth": "dwells; lives in",
    "reigneth": "reigns; rules",
    "teacheth": "teaches",
    "leadeth": "leads",
    "heareth": "hears",
    "seeth": "sees",
    "doest": "do (second person singular)",
    "knowest": "know (second person singular)",
    "canst": "can (second person singular)",
    "shalt": "shall (second person singular)",
    "wilt": "will (second person singular)",
    "mayest": "may (second person singular)",
    "wouldest": "would (second person singular)",
    "shouldest": "should (second person singular)",
    "hadst": "had (second person singular)",
    "didst": "did (second person singular)",
    "gavest": "gave (second person singular)",
    "sawest": "saw (second person singular)",
    "hearest": "hear (second person singular)",
    "speakest": "speak (second person singular)",
}


def build_auto_glossary(all_verses):
    """Scan all translation texts and find uncommon words, noting which translation they appear in."""
    found_words = {}  # word -> set of translations

    for trans, verses in all_verses.items():
        if not verses:
            continue
        for _, verse_text in verses:
            words = re.findall(r"[a-zA-Z']+", verse_text.lower())
            for word in words:
                clean = word.strip("'")
                if clean in UNCOMMON_WORDS:
                    if clean not in found_words:
                        found_words[clean] = set()
                    found_words[clean].add(trans)

    return found_words


def render_auto_glossary(all_verses):
    """Render auto-generated glossary from uncommon words found in all translation texts."""
    found_words = build_auto_glossary(all_verses)

    if not found_words:
        return "<p>No uncommon vocabulary found in this chapter.</p>"

    sorted_words = sorted(found_words.items(), key=lambda x: x[0])

    html_items = []
    for word, translations in sorted_words:
        definition = UNCOMMON_WORDS[word]
        trans_list = ", ".join(sorted(translations))
        html_items.append(
            f'                    <li><strong>{escape(word)}</strong> <span style="color:#8b3a2a;font-size:0.8em;">({trans_list})</span> — {escape(definition)}</li>'
        )

    return "<ul>\n" + "\n".join(html_items) + "\n                </ul>"


def render_key_verses(text):
    """Render key verses as a clean bulleted list."""
    items = []
    entries = re.split(r'\n(?=v\.?\d)', text.strip())
    for entry in entries:
        if not entry.strip():
            continue
        lines = entry.strip().split("\n")
        first = lines[0]
        ref_match = re.match(r'v\.?(\d+\S*)\s*[—–-]\s*(.+)', first)
        if ref_match:
            ref = f"v.{ref_match.group(1)}"
            verse_text = ref_match.group(2)
            extra = " ".join(l.strip() for l in lines[1:] if l.strip())
            full_text = verse_text + (" " + extra if extra else "")
            items.append(f'                    <li><strong>{escape(ref)}</strong> — {escape(full_text)}</li>')
    return "<ul>\n" + "\n".join(items) + "\n                </ul>" if items else ""

def build_left_sidebar(testament, book_name, chapter_num, total_chapters):
    """Build the left sidebar HTML with book list and chapter grid."""
    ot_items = []
    nt_items = []

    for num, name, chapters in OT_BOOKS:
        active = " active" if testament == "Old Testament" and name == book_name else ""
        ot_items.append(f'            <a class="sidebar-item{active}" href="{book_slug(name)}1.html"><i class="fas fa-book"></i> {name}</a>')
        if active:
            # Show chapter grid for active book
            grid = '            <div class="chapter-grid">\n'
            for c in range(1, total_chapters + 1):
                c_active = " active" if c == chapter_num else ""
                grid += f'                <a class="chapter-btn{c_active}" href="{book_slug(name)}{c}.html">{c}</a>\n'
            grid += '            </div>'
            ot_items.append(grid)

    for num, name, chapters in NT_BOOKS:
        active = " active" if testament == "New Testament" and name == book_name else ""
        nt_items.append(f'            <a class="sidebar-item{active}" href="{book_slug(name)}1.html"><i class="fas fa-book"></i> {name}</a>')
        if active:
            grid = '            <div class="chapter-grid">\n'
            for c in range(1, total_chapters + 1):
                c_active = " active" if c == chapter_num else ""
                grid += f'                <a class="chapter-btn{c_active}" href="{book_slug(name)}{c}.html">{c}</a>\n'
            grid += '            </div>'
            nt_items.append(grid)

    return f'''    <aside class="left-sidebar">
        <div class="sidebar-section">
            <div class="sidebar-section-title">Old Testament</div>
{chr(10).join(ot_items)}
        </div>
        <div class="sidebar-section">
            <div class="sidebar-section-title">New Testament</div>
{chr(10).join(nt_items)}
        </div>
    </aside>'''

RIGHT_PANEL = ''

def build_page(testament, book_num, book_name, chapter_num, total_chapters):
    """Build a complete HTML page for one chapter."""
    folder = f"{book_num} - {book_name}"
    chapter_dir = os.path.join(BASE_DIR, testament, folder, f"Chapter {chapter_num}")

    # Read all translations
    translations = ["ESV", "KJV", "ASV", "NET", "WEB"]
    all_verses = {}
    for trans in translations:
        text = read_file_safe(os.path.join(chapter_dir, f"Chapter {chapter_num} - {trans}.txt"))
        all_verses[trans] = parse_verses(text)

    # Build verse HTML for each translation
    verses_html_blocks = {}
    for trans in translations:
        if all_verses[trans]:
            verses_html_blocks[trans] = render_verses_html(all_verses[trans])
        else:
            verses_html_blocks[trans] = '<p class="verse" style="color:var(--text-muted);font-style:italic;">This translation is not yet available for this chapter.</p>'

    # Read study notes
    notes_text = read_file_safe(os.path.join(chapter_dir, f"Chapter {chapter_num} - Study Notes.txt"))
    sections = parse_study_notes(notes_text)

    # Build verse HTML
    verses_html = ""
    for trans in translations:
        active = " active" if trans == "ESV" else ""
        verses_html += f'        <div class="translation-block{active}" data-translation="{trans}">\n{verses_html_blocks[trans]}\n        </div>\n'

    # Build study note tabs
    summary = sections.get("CHAPTER SUMMARY", "")
    key_verses = sections.get("KEY VERSES", "")
    authorship = sections.get("AUTHORSHIP & HISTORICAL BACKGROUND", "")
    map_geo = sections.get("MAP & GEOGRAPHY NOTES", "")
    glossary = sections.get("GLOSSARY", "")
    cross_refs = sections.get("CROSS-REFERENCES", "")
    commentary = sections.get("COMMENTARY REFERENCES", "")
    translation = sections.get("TRANSLATION NOTES", "")
    videos = sections.get("VIDEO RESOURCES", "")
    reflection = sections.get("REFLECTION QUESTIONS", "")
    personal = sections.get("PERSONAL REFLECTION & APPLICATION", "")

    # Combine reflection sections
    all_reflection = reflection
    if personal:
        all_reflection = (all_reflection + "\n\n" + personal) if all_reflection else personal

    # Build tabs (only show tabs that have content)
    tabs_html = ""
    tab_headers = []

    if summary:
        tab_headers.append(('summary', 'Summary'))
    if key_verses:
        tab_headers.append(('keyverses', 'Key Verses'))
    if authorship:
        tab_headers.append(('authorship', 'Authorship & Background'))
    if map_geo:
        tab_headers.append(('mapgeo', 'Map & Geography'))
    # Glossary is auto-generated from translation text, always show
    tab_headers.append(('glossary', 'Glossary'))
    if cross_refs:
        tab_headers.append(('crossref', 'Cross-References'))
    if commentary:
        tab_headers.append(('commentary', 'Commentary'))
    if translation:
        tab_headers.append(('translations', 'Translations'))
    if videos:
        tab_headers.append(('videos', 'Videos'))
    if all_reflection:
        tab_headers.append(('reflection', 'Reflection'))

    # Tab header bar
    tab_bar = ""
    for i, (tid, label) in enumerate(tab_headers):
        active = " active" if i == 0 else ""
        tab_bar += f'                <div class="study-tab{active}" data-tab="{tid}">{label}</div>\n'

    # Tab content panels
    tab_panels = ""
    for i, (tid, label) in enumerate(tab_headers):
        active = " active" if i == 0 else ""
        if tid == "summary":
            content = f"<p>{escape(summary)}</p>"
        elif tid == "keyverses":
            content = render_key_verses(key_verses)
        elif tid == "authorship":
            content = render_authorship(authorship)
        elif tid == "mapgeo":
            content = render_map_geography(map_geo)
        elif tid == "glossary":
            content = render_auto_glossary(all_verses)
        elif tid == "crossref":
            content = f"<ul>\n{render_section_as_list(cross_refs)}\n                </ul>"
        elif tid == "commentary":
            content = f"<ul>\n{render_section_as_list(commentary)}\n                </ul>"
        elif tid == "translations":
            content = f"<ul>\n{render_section_as_list(translation)}\n                </ul>"
        elif tid == "videos":
            content = render_video_cards(videos)
        elif tid == "reflection":
            content = f"<ul>\n{render_section_as_list(all_reflection)}\n                </ul>"
        else:
            content = ""

        tab_panels += f'''            <div class="tab-content{active}" id="tab-{tid}">
                <h3>{label}</h3>
                {content}
            </div>\n'''

    left_sidebar = build_left_sidebar(testament, book_name, chapter_num, total_chapters)

    return build_html_page(book_name, chapter_num, total_chapters, verses_html, tab_bar, tab_panels, left_sidebar)

def build_html_page(book_name, chapter_num, total_chapters, verses_html, tab_bar, tab_panels, left_sidebar):
    """Assemble the full HTML page."""
    nav_html = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>''' + f'{book_name} {chapter_num}' + ''' — Bible Study</title>
    <link href="https://fonts.googleapis.com/css2?family=Merriweather:ital,wght@0,300;0,400;0,700;1,400&family=Inter:wght@400;500;600;700&family=Cinzel:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
    <link rel="stylesheet" href="site/style.css">
</head>
<body>
    <nav class="top-nav">
        <button class="hamburger" onclick="toggleSidebar()"><i class="fas fa-bars"></i></button>
        <a href="index.html" class="nav-brand">Bible Study</a>
        <div class="nav-center">
            <select class="nav-book-select" id="bookSelect" onchange="updateChapters()">
                <optgroup label="Old Testament">'''

    for _, name, chapters in OT_BOOKS:
        selected = ' selected' if name == book_name else ''
        nav_html += f'\n                    <option value="{book_slug(name)}" data-chapters="{chapters}"{selected}>{name}</option>'

    nav_html += '''
                </optgroup>
                <optgroup label="New Testament">'''

    for _, name, chapters in NT_BOOKS:
        selected = ' selected' if name == book_name else ''
        nav_html += f'\n                    <option value="{book_slug(name)}" data-chapters="{chapters}"{selected}>{name}</option>'

    nav_html += f'''
                </optgroup>
            </select>
            <select class="nav-chapter-select" id="chapterSelect">'''

    for c in range(1, total_chapters + 1):
        selected = ' selected' if c == chapter_num else ''
        nav_html += f'\n                <option value="{c}"{selected}>Ch {c}</option>'

    nav_html += '''
            </select>
            <button onclick="goToChapter()" style="padding:6px 12px;background:#8b3a2a;color:#fff;border:none;border-radius:6px;cursor:pointer;font-size:0.85rem;font-weight:600;">Go</button>
            <select class="nav-translation" onchange="switchTranslation(this.value)">
                <option value="ESV">ESV</option>
                <option value="KJV">KJV</option>
                <option value="ASV">ASV</option>
                <option value="NET">NET</option>
                <option value="WEB">WEB</option>
            </select>
            <button class="trans-info-btn" onclick="toggleTransInfo()" title="Translation Guide">ℹ</button>
        </div>
    </nav>

    <div class="trans-popup" id="transPopup">
        <button class="close-btn" onclick="toggleTransInfo()">&times;</button>
        <h4>Translation Guide</h4>
        <div class="trans-item"><span class="trans-name">ESV</span> — English Standard Version<br><span class="trans-desc">Essentially literal. Modern English, highly accurate. Best for deep study.</span></div>
        <div class="trans-item"><span class="trans-name">KJV</span> — King James Version<br><span class="trans-desc">Traditional (1611). Beautiful, poetic language. The classic English Bible.</span></div>
        <div class="trans-item"><span class="trans-name">ASV</span> — American Standard Version<br><span class="trans-desc">Formal equivalent (1901). Very literal, precise. Good for word studies.</span></div>
        <div class="trans-item"><span class="trans-name">NET</span> — New English Translation<br><span class="trans-desc">Study Bible with extensive translator notes. Balances accuracy and readability.</span></div>
        <div class="trans-item"><span class="trans-name">WEB</span> — World English Bible<br><span class="trans-desc">Modern, public domain. Based on the Majority Text. Free to use and share.</span></div>
    </div>

    <div class="sidebar-overlay" onclick="toggleSidebar()"></div>

''' + left_sidebar + f'''

    <main class="main-content">
        <div class="book-header">
            <h1>{book_name} — Chapter {chapter_num}</h1>
        </div>

        <div class="scripture-container">
{verses_html}
        </div>

        <div class="study-section">
            <div class="study-tabs">
{tab_bar}            </div>
{tab_panels}        </div>
    </main>

    <script src="site/script.js"></script>
</body>
</html>'''

    return nav_html

def build_index():
    """Build the homepage."""
    # Color palette for book cards - cycles through warm, scholarly colors
    ot_colors = [
        "#8b3a2a", "#2c6b4f", "#4a5a8a", "#7a5c2e", "#5c3d6e",
        "#2a6b6b", "#8b6914", "#6b4c3b", "#3d6b3d", "#6b2a4a",
        "#4a7a6b", "#7a3d5c", "#2c5a7a", "#6b6b2a", "#5c2a2a",
        "#3d5c6b", "#6b5c3d", "#4a3d7a", "#7a6b4a", "#2a4a6b",
        "#6b3d2a", "#3d7a5c", "#5c4a7a", "#7a4a3d", "#2a6b5c",
        "#4a6b3d", "#7a2a5c", "#3d6b7a", "#6b4a2a", "#5c7a3d",
        "#2a5c6b", "#7a5c2a", "#4a2a6b", "#6b7a4a", "#3d2a7a",
        "#5c6b4a", "#7a3d2a", "#2a7a5c", "#6b2a3d",
    ]
    nt_colors = [
        "#8b3a2a", "#2c6b4f", "#4a5a8a", "#7a5c2e", "#5c3d6e",
        "#2a6b6b", "#8b6914", "#6b4c3b", "#3d6b3d", "#6b2a4a",
        "#4a7a6b", "#7a3d5c", "#2c5a7a", "#6b6b2a", "#5c2a2a",
        "#3d5c6b", "#6b5c3d", "#4a3d7a", "#7a6b4a", "#2a4a6b",
        "#6b3d2a", "#3d7a5c", "#5c4a7a", "#7a4a3d", "#2a6b5c",
        "#4a6b3d", "#7a2a5c",
    ]

    ot_cards = ""
    for i, (_, name, _) in enumerate(OT_BOOKS):
        ot_cards += f'                <a class="book-link" href="{book_slug(name)}1.html">{name}</a>\n'

    nt_cards = ""
    for i, (_, name, _) in enumerate(NT_BOOKS):
        nt_cards += f'                <a class="book-link" href="{book_slug(name)}1.html">{name}</a>\n'

    return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bible Study</title>
    <link href="https://fonts.googleapis.com/css2?family=Merriweather:ital,wght@0,300;0,400;0,700;1,400&family=Inter:wght@400;500;600;700&family=Cinzel:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
    <link rel="stylesheet" href="site/style.css">
    <style>
        .home-content { margin-top: 56px; padding: 0; max-width: 900px; margin-left: auto; margin-right: auto; }
        .scroll-banner { display: flex; align-items: center; margin: 32px 32px 0; }
        .scroll-end { width: 40px; height: 140px; border-radius: 20px; background: linear-gradient(to right, #c9a96e, #a67c52, #c9a96e); box-shadow: inset 0 0 8px rgba(0,0,0,0.3), 2px 2px 6px rgba(0,0,0,0.15); }
        .scroll-end.left { border-right: 2px solid #8b6914; }
        .scroll-end.right { border-left: 2px solid #8b6914; }
        .scroll-body { flex: 1; background: linear-gradient(180deg, #faf3e0 0%, #f5ebe0 30%, #f0e4d4 70%, #ebe0cc 100%); border-top: 3px solid #c9a96e; border-bottom: 3px solid #c9a96e; padding: 28px 32px; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.08); }
        .scroll-title { font-family: "Cinzel", serif; font-size: 2.6rem; color: #8b3a2a; margin-bottom: 6px; letter-spacing: 2px; text-shadow: 1px 1px 2px rgba(139,58,42,0.1); }
        .scroll-subtitle { font-family: "Merriweather", serif; font-size: 1.1rem; color: #5a4e44; font-style: italic; }
        .parchment-body { margin: 0 72px; background: linear-gradient(180deg, #f5ebe0 0%, #faf5ed 5%, #fdf9f4 50%, #faf5ed 95%, #f0e4d4 100%); border-left: 3px solid #d4c4a8; border-right: 3px solid #d4c4a8; border-bottom: 3px solid #c9a96e; border-radius: 0 0 8px 8px; padding: 36px 40px 48px; box-shadow: 4px 4px 16px rgba(0,0,0,0.08), -4px 0 16px rgba(0,0,0,0.05); }
        .testament-section { margin-bottom: 36px; }
        .testament-title { font-family: "Cinzel", serif; font-size: 1.3rem; margin-bottom: 16px; padding-bottom: 8px; font-weight: 700; }
        .testament-title.ot { color: #6b4c3b; border-bottom: 2px solid #6b4c3b; }
        .testament-title.nt { color: #2c5a6b; border-bottom: 2px solid #2c5a6b; }
        .testament-title.topical { color: #5c3d6e; border-bottom: 2px solid #5c3d6e; }
        .book-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 10px; }
        .book-link { display: block; padding: 12px 16px; background: #fdf9f4; border: 1px solid #e0d6c8; border-left: 4px solid #6b4c3b; border-radius: var(--radius-md); text-decoration: none; font-size: 0.9rem; font-weight: 600; color: #3d2b1f; transition: box-shadow 0.2s, transform 0.15s, background 0.2s, color 0.2s; }
        .book-link:hover { box-shadow: 0 6px 16px rgba(0,0,0,0.12); transform: translateY(-3px); background: #8b3a2a; color: #fff; border-left-color: #8b3a2a; }
        .topic-link { border-left-color: #5c3d6e !important; }
        .topic-link:hover { background: #5c3d6e !important; border-left-color: #5c3d6e !important; }
        @media (max-width: 768px) { .scroll-title { font-size: 1.6rem; } .scroll-subtitle { font-size: 0.9rem; } .scroll-end { width: 24px; height: 100px; } .scroll-body { padding: 18px 16px; } .parchment-body { margin: 0 16px; padding: 24px 16px; } .scroll-banner { margin: 16px 16px 0; } }
        @media (max-width: 768px) { .home-content { padding: 32px 16px; } .home-title { font-size: 2rem; } .book-grid { grid-template-columns: repeat(auto-fill, minmax(130px, 1fr)); } }
    </style>
</head>
<body>
    <nav class="top-nav">
        <a href="index.html" class="nav-brand">Bible Study</a>
        <div class="nav-center"></div>
    </nav>
    <main class="home-content">
        <div class="scroll-banner">
            <div class="scroll-end left"></div>
            <div class="scroll-body">
                <h1 class="scroll-title">Bible Study</h1>
                <p class="scroll-subtitle">Select a book to begin studying</p>
            </div>
            <div class="scroll-end right"></div>
        </div>
        <div class="parchment-body">
        <div class="testament-section">
            <h2 class="testament-title ot">Old Testament</h2>
            <div class="book-grid">
''' + ot_cards + '''            </div>
        </div>
        <div class="testament-section">
            <h2 class="testament-title nt">New Testament</h2>
            <div class="book-grid">
''' + nt_cards + '''            </div>
        </div>
        <div class="testament-section">
            <h2 class="testament-title topical">Topical Studies</h2>
            <div class="book-grid">
                <a class="book-link topic-link" href="fruits-of-the-spirit.html">Fruits of the Spirit</a>
                <a class="book-link topic-link" href="the-12-apostles.html">The 12 Apostles</a>
                <a class="book-link topic-link" href="names-of-god.html">Names of God</a>
                <a class="book-link topic-link" href="armor-of-god.html">Armor of God</a>
                <a class="book-link topic-link" href="parables-of-jesus.html">Parables of Jesus</a>
                <a class="book-link topic-link" href="prophecy-and-fulfillment.html">Prophecy &amp; Fulfillment</a>
                <a class="book-link topic-link" href="prayers-in-the-bible.html">Prayers in the Bible</a>
                <a class="book-link topic-link" href="i-am-statements.html">I AM Statements of Jesus</a>
                <a class="book-link topic-link" href="ten-commandments.html">The Ten Commandments</a>
                <a class="book-link topic-link" href="beatitudes.html">The Beatitudes</a>
                <a class="book-link topic-link" href="covenants.html">Covenants of the Bible</a>
                <a class="book-link topic-link" href="men-of-the-bible.html">Men of the Bible</a>
                <a class="book-link topic-link" href="women-of-the-bible.html">Women of the Bible</a>
                <a class="book-link topic-link" href="kings-of-israel.html">Kings of Israel &amp; Judah</a>
                <a class="book-link topic-link" href="promises-of-god.html">Promises of God</a>
                <a class="book-link topic-link" href="spiritual-disciplines.html">Spiritual Disciplines</a>
                <a class="book-link topic-link" href="marriage-and-family.html">Marriage &amp; Family</a>
                <a class="book-link topic-link" href="the-trinity.html">The Trinity</a>
                <a class="book-link topic-link" href="the-gospel.html">The Gospel: Salvation</a>
                <a class="book-link topic-link" href="miracles-of-jesus.html">Miracles of Jesus</a>
            </div>
        </div>
        <div class="testament-section">
            <h2 class="testament-title" style="color:#6b4c3b; border-bottom-color:#6b4c3b;">Translation Guide</h2>
            <div style="background:var(--bg-card);border:1px solid #e8e0d6;border-radius:14px;padding:28px 32px;box-shadow:0 1px 3px rgba(44,36,32,0.06);font-size:0.9rem;line-height:1.8;color:#5a4e44;">
                <p style="margin-bottom:16px;"><strong style="color:#8b3a2a;font-size:1rem;">ESV — English Standard Version (2001)</strong><br>An essentially literal translation that balances word-for-word accuracy with modern readability. Translated from the Masoretic Hebrew text and Nestle-Aland Greek text. Widely used for preaching, study, and memorization. Considered one of the best all-around study Bibles available today.</p>
                <p style="margin-bottom:16px;"><strong style="color:#4a5a8a;font-size:1rem;">KJV — King James Version (1611)</strong><br>The most influential English Bible in history. Commissioned by King James I and translated by 47 scholars from the Textus Receptus. Known for its majestic, poetic language that has shaped English literature for over 400 years. Uses older English ("thee," "thou," "hath") but remains beloved for worship and memorization.</p>
                <p style="margin-bottom:16px;"><strong style="color:#7a5c2e;font-size:1rem;">ASV — American Standard Version (1901)</strong><br>A revision of the KJV using more accurate manuscript evidence available in the late 1800s. Extremely literal — almost a word-for-word rendering from the original languages. Excellent for detailed word studies but can read stiffly in English. Uses "Jehovah" instead of "LORD" for God's name.</p>
                <p style="margin-bottom:16px;"><strong style="color:#5c3d6e;font-size:1rem;">NET — New English Translation (2005)</strong><br>A unique translation created by over 25 biblical scholars with 60,000+ translator notes explaining why specific translation choices were made. Balances accuracy with natural English. The notes make it an exceptional study resource — like having a seminary professor explain the text alongside you.</p>
                <p style="margin-bottom:0;"><strong style="color:#2c6b4f;font-size:1rem;">WEB — World English Bible (2000)</strong><br>A modern-language update of the ASV. Completely public domain — free to copy, share, and use without restriction. Based on the Majority Text (Byzantine) tradition rather than the Critical Text. Uses modern English while remaining faithful to the original languages. Ideal for projects requiring unrestricted Scripture usage.</p>
            </div>
        </div>
        </div>
    </main>
</body>
</html>'''

def main():
    """Build the entire site."""
    # Create output directory
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    os.makedirs(os.path.join(OUTPUT_DIR, "site"), exist_ok=True)

    # Copy shared assets
    import shutil
    shutil.copy2(os.path.join(BASE_DIR, "site", "style.css"), os.path.join(OUTPUT_DIR, "site", "style.css"))
    shutil.copy2(os.path.join(BASE_DIR, "site", "script.js"), os.path.join(OUTPUT_DIR, "site", "script.js"))

    # Build index page
    index_html = build_index()
    with open(os.path.join(OUTPUT_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(index_html)
    print("Built: index.html")

    # Build all OT chapters
    count = 0
    for num, name, chapters in OT_BOOKS:
        for ch in range(1, chapters + 1):
            page_html = build_page("Old Testament", num, name, ch, chapters)
            filename = f"{book_slug(name)}{ch}.html"
            with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
                f.write(page_html)
            count += 1

    # Build all NT chapters
    for num, name, chapters in NT_BOOKS:
        for ch in range(1, chapters + 1):
            page_html = build_page("New Testament", num, name, ch, chapters)
            filename = f"{book_slug(name)}{ch}.html"
            with open(os.path.join(OUTPUT_DIR, filename), "w", encoding="utf-8") as f:
                f.write(page_html)
            count += 1

    print(f"\nDone! Built {count} chapter pages + index.html")
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"\nTo preview: open {OUTPUT_DIR}/index.html")
    print("To deploy: copy contents of docs/ to your GitHub Pages root, or configure GitHub Pages to serve from docs/")


if __name__ == "__main__":
    main()
