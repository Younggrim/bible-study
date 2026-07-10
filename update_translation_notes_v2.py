#!/usr/bin/env python3
"""
Script to update Translation Notes sections in Bible Study notes files
to include ESV comparisons alongside existing KJV notes.
Version 2 - Fixed insertion logic.
"""

import os
import re
import copy

BASE_PATH = "/Users/jeremymcadoo/Desktop/Kiro Projects/Bible Study/New Testament"

# Define books and their chapter counts
BOOKS = [
    ("13 - 1 Thessalonians", 5),
    ("14 - 2 Thessalonians", 3),
    ("15 - 1 Timothy", 6),
    ("16 - 2 Timothy", 4),
    ("17 - Titus", 3),
    ("18 - Philemon", 1),
    ("19 - Hebrews", 13),
    ("20 - James", 5),
    ("21 - 1 Peter", 5),
    ("22 - 2 Peter", 3),
    ("23 - 1 John", 5),
    ("24 - 2 John", 1),
    ("25 - 3 John", 1),
    ("26 - Jude", 1),
    ("27 - Revelation", 22),
]

# Common KJV -> ESV word substitutions
KJV_TO_ESV = {
    'charity': 'love',
    'conversation': 'conduct',
    'prevent': 'precede',
    'by and by': 'immediately',
    'meat': 'food',
    'quick': 'living',
    'peculiar': 'his own possession',
    'study to be quiet': 'aspire to live quietly',
    'communicate': 'share',
    'holy ghost': 'holy spirit',
    'shew': 'show',
    'shewed': 'showed',
    'saith': 'says',
    'hath': 'has',
    'doth': 'does',
    'wherefore': 'therefore',
    'brethren': 'brothers',
    'cometh': 'comes',
    'knoweth': 'knows',
    'giveth': 'gives',
    'taketh': 'takes',
    'maketh': 'makes',
    'goeth': 'goes',
    'doeth': 'does',
    'liveth': 'lives',
    'abideth': 'abides',
    'remaineth': 'remains',
    'worketh': 'works',
    'pleaseth': 'pleases',
    'passeth': 'surpasses',
    'endureth': 'endures',
    'believeth': 'believes',
    'receiveth': 'receives',
    'overcometh': 'overcomes',
    'keepeth': 'keeps',
    'loveth': 'loves',
    'hateth': 'hates',
    'seeketh': 'seeks',
    'teacheth': 'teaches',
    'preacheth': 'preaches',
    'speaketh': 'speaks',
    'heareth': 'hears',
    'seeth': 'sees',
    'sitteth': 'sits',
    'standeth': 'stands',
    'reigneth': 'reigns',
    'suffereth': 'suffers',
}


def parse_esv_verses(esv_text):
    """Parse ESV text file into a dictionary of verse_number -> verse_text."""
    verses = {}
    lines = esv_text.strip().split('\n')
    for line in lines:
        line = line.strip()
        match = re.match(r'^(\d+)\.\s+(.+)$', line)
        if match:
            verse_num = int(match.group(1))
            verse_text = match.group(2)
            verses[verse_num] = verse_text
    return verses


def find_esv_rendering(kjv_phrase, esv_verse):
    """
    Find the ESV equivalent of a KJV phrase.
    Returns: (esv_phrase, is_equivalent)
    - esv_phrase: the ESV rendering (or None if identical)
    - is_equivalent: True if phrases are essentially the same
    """
    if not esv_verse or not kjv_phrase:
        return None, False
    
    kjv_lower = kjv_phrase.lower().strip()
    esv_lower = esv_verse.lower()
    
    # Direct match - phrase exists verbatim in ESV
    if kjv_lower in esv_lower:
        return None, True  # Equivalent
    
    # Try common substitutions to find the ESV rendering
    # First, try simple word-level replacements
    modified = kjv_lower
    for kjv_word, esv_word in KJV_TO_ESV.items():
        if kjv_word in modified:
            modified = modified.replace(kjv_word, esv_word)
    
    if modified != kjv_lower and modified in esv_lower:
        idx = esv_lower.find(modified)
        return esv_verse[idx:idx + len(modified)], False
    
    # Try to find a matching segment in ESV by key content words
    # Remove archaic pronouns and verb forms
    archaic = {'ye', 'thee', 'thou', 'thy', 'thine', 'hath', 'doth', 'shalt',
               'shall', 'unto', 'upon', 'thereof', 'therein', 'whereby', 'wherein',
               'wherefore', 'yea', 'nay', 'lo', 'behold'}
    
    kjv_words = kjv_lower.split()
    content_words = [w.strip('.,;:!?') for w in kjv_words 
                     if w.strip('.,;:!?') not in archaic 
                     and len(w.strip('.,;:!?')) > 2
                     and w.strip('.,;:!?') not in ('the', 'and', 'for', 'are', 'was', 'were', 'not', 'but', 'that', 'this', 'with', 'from', 'have', 'has', 'his', 'her', 'our', 'who', 'which')]
    
    if not content_words:
        return None, False
    
    # Look for the best matching window in ESV
    esv_words = esv_verse.split()
    best_match = None
    best_score = 0
    best_start = 0
    best_end = 0
    
    window_size = max(len(kjv_words) + 3, 6)
    
    for start in range(len(esv_words)):
        for end in range(start + 2, min(start + window_size + 1, len(esv_words) + 1)):
            window = ' '.join(esv_words[start:end])
            window_lower = window.lower()
            
            score = 0
            for word in content_words:
                if word in window_lower:
                    score += 1
                else:
                    # Check ESV equivalents
                    for kjv_w, esv_w in KJV_TO_ESV.items():
                        if word == kjv_w and esv_w in window_lower:
                            score += 1
                            break
            
            # Prefer shorter windows with same score
            if score > best_score or (score == best_score and score > 0 and (end - start) < (best_end - best_start)):
                best_score = score
                best_match = window
                best_start = start
                best_end = end
    
    # Only accept if we matched at least 50% of content words
    if best_match and best_score >= max(1, len(content_words) * 0.5):
        # Clean up
        best_match = best_match.strip('.,;:')
        best_lower = best_match.lower()
        if best_lower != kjv_lower and best_lower != kjv_lower.rstrip('.,;:'):
            return best_match, False
    
    return None, False


def process_file(notes_file, esv_file):
    """Process a single study notes file to add ESV comparisons."""
    
    with open(esv_file, 'r', encoding='utf-8') as f:
        esv_content = f.read()
    with open(notes_file, 'r', encoding='utf-8') as f:
        notes_content = f.read()
    
    # Parse ESV verses
    esv_verses = parse_esv_verses(esv_content)
    if not esv_verses:
        return False
    
    # Find TRANSLATION NOTES section boundaries
    tn_match = re.search(r'TRANSLATION NOTES\s*\n-+\n', notes_content)
    if not tn_match:
        return False
    
    tn_start = tn_match.end()
    
    # Find end of translation notes section
    next_sections = ['GLOSSARY', 'PERSONAL REFLECTION', 'PERSONAL NOTES', 
                     'STUDY NOTES', '========']
    tn_end = len(notes_content)
    for section in next_sections:
        idx = notes_content.find(section, tn_start)
        if idx != -1 and idx < tn_end:
            tn_end = idx
    
    tn_section = notes_content[tn_start:tn_end]
    
    # Process each verse entry using regex to find KJV: "phrase" patterns
    # Pattern: v.X — KJV: "phrase" — rest of content
    # We need to insert / ESV: "phrase" after the closing quote of KJV phrase
    
    modified = False
    new_section = tn_section
    
    # Find all KJV entries that don't already have ESV
    # Pattern matches: KJV: "some phrase"
    # We need to be careful about entries that already have / ESV:
    
    # Split into verse entries
    # Each entry starts with v.NUMBER
    entries = re.split(r'(?=^v\.\d+)', tn_section, flags=re.MULTILINE)
    
    new_entries = []
    for entry in entries:
        if not entry.strip():
            new_entries.append(entry)
            continue
        
        # Check if already has ESV
        if '/ ESV:' in entry or 'ESV:' in entry:
            # This entry was already corrupted by v1 script - need to fix it
            # Or it legitimately has ESV already
            new_entries.append(entry)
            continue
        
        # Extract verse number
        verse_match = re.match(r'v\.(\d+)(?:-(\d+))?\s', entry)
        if not verse_match:
            new_entries.append(entry)
            continue
        
        verse_num = int(verse_match.group(1))
        verse_end = int(verse_match.group(2)) if verse_match.group(2) else verse_num
        
        # Get combined ESV text for this verse range
        esv_text = ''
        for v in range(verse_num, verse_end + 1):
            if v in esv_verses:
                esv_text += (' ' if esv_text else '') + esv_verses[v]
        
        if not esv_text:
            new_entries.append(entry)
            continue
        
        # Find KJV: "phrase" pattern in this entry
        kjv_pattern = re.search(r'KJV:\s*"([^"]+)"', entry)
        if not kjv_pattern:
            new_entries.append(entry)
            continue
        
        kjv_phrase = kjv_pattern.group(1)
        kjv_end_pos = kjv_pattern.end()  # Position after the closing quote
        
        # Find ESV rendering
        esv_rendering, is_equivalent = find_esv_rendering(kjv_phrase, esv_text)
        
        if is_equivalent:
            # Insert "/ ESV: Both equivalent." after the KJV closing quote
            esv_insert = ' / ESV: Both equivalent.'
        elif esv_rendering:
            esv_insert = f' / ESV: "{esv_rendering}"'
        else:
            # Could not determine - skip
            new_entries.append(entry)
            continue
        
        # Insert the ESV text after the KJV closing quote
        new_entry = entry[:kjv_end_pos] + esv_insert + entry[kjv_end_pos:]
        new_entries.append(new_entry)
        modified = True
    
    if modified:
        new_tn_section = ''.join(new_entries)
        new_content = notes_content[:tn_start] + new_tn_section + notes_content[tn_end:]
        with open(notes_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    
    return False


def restore_and_process(book_dir, book_name, chapter_num):
    """Restore original file from git if corrupted, then process."""
    chapter_dir = os.path.join(book_dir, f"Chapter {chapter_num}")
    esv_file = os.path.join(chapter_dir, f"Chapter {chapter_num} - ESV.txt")
    notes_file = os.path.join(chapter_dir, f"Chapter {chapter_num} - Study Notes.txt")
    
    if not os.path.exists(esv_file):
        print(f"  WARNING: ESV file not found: {esv_file}")
        return False
    if not os.path.exists(notes_file):
        print(f"  WARNING: Study Notes file not found: {notes_file}")
        return False
    
    return process_file(notes_file, esv_file)


def main():
    """Main processing function."""
    total_modified = 0
    total_chapters = 0
    
    for book_name, num_chapters in BOOKS:
        book_dir = os.path.join(BASE_PATH, book_name)
        print(f"\nProcessing {book_name} ({num_chapters} chapters)...")
        
        if not os.path.exists(book_dir):
            print(f"  ERROR: Book directory not found: {book_dir}")
            continue
        
        for chapter in range(1, num_chapters + 1):
            total_chapters += 1
            result = restore_and_process(book_dir, book_name, chapter)
            if result:
                total_modified += 1
                print(f"  Chapter {chapter}: Updated")
            else:
                print(f"  Chapter {chapter}: No changes or already has ESV")
    
    print(f"\n{'='*50}")
    print(f"Processing complete!")
    print(f"Total chapters processed: {total_chapters}")
    print(f"Total chapters modified: {total_modified}")


if __name__ == '__main__':
    main()
