#!/usr/bin/env python3
"""
Generate ASV/NET/WEB translation comparison notes for OT chapters that
currently only have KJV/ESV comparisons. Uses the actual translation text
files to identify meaningful differences and appends them to the existing
TRANSLATION COMPARISON section.
"""

import os
import re
import sys
import glob
import difflib


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def read_translation_file(chapter_dir, chapter_num, translation):
    """Read a translation file and return dict of {verse_num: text}."""
    filename = f"Chapter {chapter_num} - {translation}.txt"
    filepath = os.path.join(chapter_dir, filename)
    verses = {}
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for line in f:
                m = re.match(r'^(\d+)\.\s+(.+)$', line.strip())
                if m:
                    verses[int(m.group(1))] = m.group(2)
    except FileNotFoundError:
        pass
    return verses


def get_discussed_verses(translation_section):
    """Extract verse numbers that are already discussed in the TRANSLATION COMPARISON."""
    verses = set()
    for m in re.finditer(r'v\.(\d+)', translation_section):
        verses.add(int(m.group(1)))
    return sorted(verses)


def find_key_differences(kjv_text, esv_text, asv_text, net_text, web_text):
    """
    Find notable differences between translations for a verse.
    Returns a list of observation strings about ASV/NET/WEB differences.
    """
    observations = []

    if not any([asv_text, net_text, web_text]):
        return observations

    # Compare word-level differences
    kjv_words = set(kjv_text.lower().split()) if kjv_text else set()
    esv_words = set(esv_text.lower().split()) if esv_text else set()

    # Check for divine name differences (LORD vs Jehovah vs Yahweh)
    name_diffs = []
    if asv_text and ('Jehovah' in asv_text or 'jehovah' in asv_text.lower()):
        name_diffs.append('ASV: "Jehovah"')
    if web_text and ('Yahweh' in web_text or 'yahweh' in web_text.lower()):
        name_diffs.append('WEB: "Yahweh"')
    if name_diffs and kjv_text and ('LORD' in kjv_text or 'Lord' in kjv_text):
        kjv_form = 'LORD' if 'LORD' in kjv_text else 'Lord'
        observations.append(f'KJV: "{kjv_form}" — {" / ".join(name_diffs)} — different renderings of the divine name (Hebrew YHWH).')

    # Check for significant phrase differences in NET (often paraphrases)
    if net_text and kjv_text:
        # NET often restructures significantly
        kjv_len = len(kjv_text.split())
        net_len = len(net_text.split())
        # Check similarity ratio
        ratio = difflib.SequenceMatcher(None, kjv_text.lower(), net_text.lower()).ratio()
        if ratio < 0.5 and net_len > 5:
            # Significant restructuring - show the NET rendering
            net_short = net_text[:120] + ('...' if len(net_text) > 120 else '')
            observations.append(f'NET significantly restructures: "{net_short}"')

    # Check for archaic language modernization
    archaic_pairs = [
        ('saith', 'says'),
        ('unto', 'to'),
        ('hath', 'has'),
        ('doth', 'does'),
        ('thee', 'you'),
        ('thou', 'you'),
        ('thy', 'your'),
        ('ye', 'you'),
        ('wherefore', 'why'),
        ('begat', 'fathered'),
    ]

    for old, modern in archaic_pairs:
        if kjv_text and old in kjv_text.lower():
            # Check if modern translations use the modern form
            modernized = []
            if asv_text and old not in asv_text.lower():
                modernized.append('ASV')
            if net_text and old not in net_text.lower():
                modernized.append('NET')
            if web_text and old not in web_text.lower():
                modernized.append('WEB')
            # Only note if at least one modernizes and it's interesting
            if modernized and len(modernized) >= 2:
                # Skip common ones that aren't interesting
                if old in ('unto', 'saith') and len(modernized) == 3:
                    continue  # Too common to note

    # Check for key theological/vocabulary differences
    if asv_text and kjv_text:
        # ASV specific patterns
        if 'firmament' in kjv_text and 'expanse' in asv_text:
            observations.append('ASV: "expanse" for KJV\'s "firmament" — better conveys Hebrew "raqia."')

    return observations


def generate_additional_notes(chapter_dir, chapter_num, existing_section):
    """
    Generate ASV/NET/WEB notes for verses already discussed in the section.
    Returns the additional text to append, or empty string if nothing useful.
    """
    # Read all translations
    kjv = read_translation_file(chapter_dir, chapter_num, 'KJV')
    esv = read_translation_file(chapter_dir, chapter_num, 'ESV')
    asv = read_translation_file(chapter_dir, chapter_num, 'ASV')
    net = read_translation_file(chapter_dir, chapter_num, 'NET')
    web = read_translation_file(chapter_dir, chapter_num, 'WEB')

    if not asv and not net and not web:
        return ""

    # Get verses already discussed
    discussed_verses = get_discussed_verses(existing_section)

    # If section is empty, pick interesting verses to compare
    if not discussed_verses:
        # Pick up to 5 verses with notable differences
        discussed_verses = find_interesting_verses(kjv, esv, asv, net, web)

    if not discussed_verses:
        return ""

    # For each discussed verse, find ASV/NET/WEB differences
    notes = []
    for v_num in discussed_verses:
        kjv_text = kjv.get(v_num, "")
        esv_text = esv.get(v_num, "")
        asv_text = asv.get(v_num, "")
        net_text = net.get(v_num, "")
        web_text = web.get(v_num, "")

        if not kjv_text:
            continue

        # Build concise comparison showing key differences
        parts = []

        # Find the most interesting word/phrase differences
        if asv_text:
            asv_diff = find_notable_phrase(kjv_text, asv_text, 'ASV')
            if asv_diff:
                parts.append(asv_diff)

        if net_text:
            net_diff = find_notable_phrase(kjv_text, net_text, 'NET')
            if net_diff:
                parts.append(net_diff)

        if web_text:
            web_diff = find_notable_phrase(kjv_text, web_text, 'WEB')
            if web_diff:
                parts.append(web_diff)

        if parts:
            entry_lines = [f"v.{v_num} — " + parts[0]]
            for p in parts[1:]:
                entry_lines.append(f"       {p}")
            notes.append("\n".join(entry_lines))

    return "\n".join(notes)


def find_interesting_verses(kjv, esv, asv, net, web, max_verses=5):
    """
    Find verses with the most notable differences across translations.
    Returns a list of verse numbers.
    """
    scores = {}
    for v_num in kjv:
        kjv_text = kjv.get(v_num, "")
        net_text = net.get(v_num, "")
        asv_text = asv.get(v_num, "")
        web_text = web.get(v_num, "")

        if not kjv_text:
            continue

        score = 0
        # Divine name differences are always interesting
        if 'LORD' in kjv_text:
            if asv_text and 'Jehovah' in asv_text:
                score += 2
            if web_text and 'Yahweh' in web_text:
                score += 2

        # NET restructuring
        if net_text:
            ratio = difflib.SequenceMatcher(None, kjv_text.lower(), net_text.lower()).ratio()
            if ratio < 0.5:
                score += 3
            elif ratio < 0.7:
                score += 1

        # Only count verses with actual differences
        if score > 0:
            scores[v_num] = score

    # Return top N verses by score
    sorted_verses = sorted(scores.keys(), key=lambda v: scores[v], reverse=True)
    return sorted_verses[:max_verses]


def find_notable_phrase(kjv_text, other_text, trans_name):
    """
    Find the most notable difference between KJV and another translation.
    Returns a concise note string or empty string.
    """
    if not kjv_text or not other_text:
        return ""

    # Check divine name differences first (most common notable difference)
    if 'LORD' in kjv_text or 'Lord' in kjv_text:
        if trans_name == 'ASV' and 'Jehovah' in other_text:
            return f'{trans_name}: uses "Jehovah" for KJV\'s "LORD" (Hebrew YHWH).'
        if trans_name == 'WEB' and 'Yahweh' in other_text:
            return f'{trans_name}: uses "Yahweh" for KJV\'s "LORD" (Hebrew YHWH).'

    # Look for significantly different key phrases
    kjv_words = kjv_text.split()
    other_words = other_text.split()

    # Find the first substantially different segment
    # Use difflib to find changed blocks
    matcher = difflib.SequenceMatcher(None, kjv_words, other_words)
    changes = []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag == 'replace' and (i2 - i1) >= 2:
            kjv_phrase = " ".join(kjv_words[i1:i2])
            other_phrase = " ".join(other_words[j1:j2])
            # Skip very long phrases (truncate)
            if len(kjv_phrase) > 60:
                kjv_phrase = kjv_phrase[:57] + "..."
            if len(other_phrase) > 60:
                other_phrase = other_phrase[:57] + "..."
            changes.append((kjv_phrase, other_phrase))
        elif tag == 'insert' and (j2 - j1) >= 2:
            inserted = " ".join(other_words[j1:j2])
            if len(inserted) > 60:
                inserted = inserted[:57] + "..."
            changes.append(("", inserted))

    if changes:
        # Pick the most interesting change (longest replacement)
        best = max(changes, key=lambda c: len(c[1]))
        kjv_part, other_part = best
        if kjv_part:
            return f'{trans_name}: "{other_part}" for KJV\'s "{kjv_part}"'
        else:
            return f'{trans_name}: adds "{other_part}"'

    # Check overall similarity — if very different, show a snippet
    ratio = difflib.SequenceMatcher(None, kjv_text.lower(), other_text.lower()).ratio()
    if ratio < 0.5:
        snippet = other_text[:80] + ('...' if len(other_text) > 80 else '')
        return f'{trans_name}: "{snippet}"'

    return ""


def analyze_differences(kjv, esv, asv, net, web):
    """Produce a brief analysis of the key differences between translations."""
    points = []

    # Divine name handling
    has_lord_kjv = 'LORD' in kjv if kjv else False
    has_jehovah_asv = 'Jehovah' in asv if asv else False
    has_yahweh_web = 'Yahweh' in web if web else False

    if has_lord_kjv and (has_jehovah_asv or has_yahweh_web):
        names = []
        if has_jehovah_asv:
            names.append('ASV uses "Jehovah"')
        if has_yahweh_web:
            names.append('WEB uses "Yahweh"')
        points.append(f'KJV/ESV: "LORD"; {"; ".join(names)} for the divine name.')

    # Significant NET restructuring
    if net and kjv:
        ratio = difflib.SequenceMatcher(None, kjv.lower(), net.lower()).ratio()
        if ratio < 0.4:
            points.append('NET significantly paraphrases for clarity.')

    # Archaic vs modern
    if kjv and ('saith' in kjv or 'unto' in kjv or 'thee' in kjv or 'thou' in kjv):
        if web and 'saith' not in web and 'unto' not in web and 'thee' not in web:
            pass  # Too common to note every time

    if points:
        return " ".join(points)
    return ""


def extract_translation_section(content):
    """Extract the TRANSLATION COMPARISON section text and its position."""
    match = re.search(r'^TRANSLATION COMPARISON\n-{4,}\n', content, re.MULTILINE)
    if not match:
        return None, None, None

    text_start = match.end()

    # Find next section
    next_match = re.search(r'^[A-Z][A-Z &()\-]+\n-{4,}\n', content[text_start:], re.MULTILINE)
    if next_match:
        section_end = text_start + next_match.start()
    else:
        section_end = len(content)

    section_text = content[text_start:section_end].strip()
    return section_text, text_start, section_end


def has_asv_net_web(section_text):
    """Check if the section already has ASV/NET/WEB content."""
    return bool(re.search(r'\b(ASV|NET|WEB)\b', section_text))


def process_file(filepath, dry_run=False):
    """Process a single study notes file to add ASV/NET/WEB notes."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    section_text, text_start, section_end = extract_translation_section(content)
    if section_text is None:
        return False, "No TRANSLATION COMPARISON section"

    # Skip if already has ASV/NET/WEB (unless section is effectively empty)
    if has_asv_net_web(section_text) and len(section_text.strip()) > 20:
        return False, "Already has ASV/NET/WEB"

    # Determine chapter directory and number
    chapter_dir = os.path.dirname(filepath)
    chapter_match = re.search(r'Chapter (\d+)', chapter_dir)
    if not chapter_match:
        return False, "Cannot determine chapter number"
    chapter_num = int(chapter_match.group(1))

    # Generate additional notes
    additional = generate_additional_notes(chapter_dir, chapter_num, section_text)
    if not additional:
        return False, "No additional content generated"

    # Insert the additional notes into the section
    # Add after existing content with a blank line separator
    new_section_text = section_text + "\n\n" + additional + "\n"

    # Replace in content
    new_content = content[:text_start] + new_section_text + "\n" + content[section_end:]

    if dry_run:
        return True, new_content

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return True, "Added ASV/NET/WEB notes"


def main():
    ot_path = os.path.join(BASE_DIR, 'Old Testament')
    study_files = glob.glob(os.path.join(ot_path, '*', '*', '*Study Notes.txt'))
    study_files.sort()

    print(f"Found {len(study_files)} study notes files in Old Testament")
    print("=" * 60)

    dry_run = '--dry-run' in sys.argv

    success = 0
    skipped = 0
    errors = 0

    for filepath in study_files:
        rel = os.path.relpath(filepath, ot_path)
        try:
            result, msg = process_file(filepath, dry_run=dry_run)
            if result:
                success += 1
                print(f"  [OK] {rel}")
            else:
                skipped += 1
        except Exception as e:
            errors += 1
            print(f"  [ERROR] {rel} - {e}")

    print()
    print("=" * 60)
    print(f"Results: {success} updated, {skipped} skipped, {errors} errors")


if __name__ == '__main__':
    main()
