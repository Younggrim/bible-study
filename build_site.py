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
    items = []
    current = []
    for line in text.split("\n"):
        if line.strip() == "":
            if current:
                items.append(" ".join(current))
                current = []
        else:
            current.append(line.strip())
    if current:
        items.append(" ".join(current))

    html_items = []
    for item in items:
        if item:
            # Convert URLs to links
            item = re.sub(r'(https?://\S+)', r'<a href="\1" target="_blank">\1</a>', item)
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


def render_key_verses(text):
    """Render key verses with highlight styling."""
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
            items.append(f'''                <div class="key-verse">
                    <div class="ref">{escape(ref)}</div>
                    <div class="text">{escape(full_text)}</div>
                </div>''')
    return "\n".join(items)

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

    return build_html_page(book_name, chapter_num, verses_html, tab_bar, tab_panels, left_sidebar)

def build_html_page(book_name, chapter_num, verses_html, tab_bar, tab_panels, left_sidebar):
    """Assemble the full HTML page."""
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{book_name} {chapter_num} — Bible Study</title>
    <link href="https://fonts.googleapis.com/css2?family=Merriweather:ital,wght@0,300;0,400;0,700;1,400&family=Inter:wght@400;500;600;700&family=Cinzel:wght@400;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
    <link rel="stylesheet" href="site/style.css">
</head>
<body>
    <nav class="top-nav">
        <button class="hamburger" onclick="toggleSidebar()"><i class="fas fa-bars"></i></button>
        <a href="index.html" class="nav-brand">Bible Study</a>
        <div class="nav-center">
            <span style="font-size:0.9rem;color:var(--text-secondary);">{book_name} &bull; Chapter {chapter_num}</span>
            <select class="nav-translation" onchange="switchTranslation(this.value)">
                <option value="ESV">ESV</option>
                <option value="KJV">KJV</option>
                <option value="ASV">ASV</option>
                <option value="NET">NET</option>
                <option value="WEB">WEB</option>
            </select>
        </div>
    </nav>

    <div class="sidebar-overlay" onclick="toggleSidebar()"></div>

{left_sidebar}

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
                <a class="book-link topic-link" href="#">Fruits of the Spirit</a>
                <a class="book-link topic-link" href="#">The 12 Apostles</a>
                <a class="book-link topic-link" href="#">Names of God</a>
                <a class="book-link topic-link" href="#">Armor of God</a>
                <a class="book-link topic-link" href="#">Parables of Jesus</a>
                <a class="book-link topic-link" href="#">Prophecy &amp; Fulfillment</a>
                <a class="book-link topic-link" href="#">Prayers in the Bible</a>
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
