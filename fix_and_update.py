#!/usr/bin/env python3
"""
Script to fix corrupted Translation Notes and properly add ESV comparisons.
Step 1: Fix the corruption from v1 script (restore original KJV entries)
Step 2: Properly insert ESV comparisons after KJV quotes
"""

import os
import re

BASE_PATH = "/Users/jeremymcadoo/Desktop/Kiro Projects/Bible Study/New Testament"

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


def fix_corrupted_line(line):
    """
    Fix a line corrupted by v1 script.
    Corruption pattern: KJV: " / ESV: "something"actual kjv phrase" — rest
    Or: KJV: " / ESV: Both equivalent.actual kjv phrase" — rest
    Should become: KJV: "actual kjv phrase" — rest
    """
    # Pattern 1: KJV: " / ESV: "esv text"kjv text" — rest
    match = re.search(r'(KJV:\s*)" / ESV: "[^"]*"([^"]+)"', line)
    if match:
        # Restore to: KJV: "kjv text"
        prefix = line[:match.start()] + match.group(1) + '"' + match.group(2) + '"'
        suffix = line[match.end():]
        return prefix + suffix
    
    # Pattern 2: KJV: " / ESV: Both equivalent.kjv text" — rest
    match = re.search(r'(KJV:\s*)" / ESV: Both equivalent\.([^"]+)"', line)
    if match:
        prefix = line[:match.start()] + match.group(1) + '"' + match.group(2) + '"'
        suffix = line[match.end():]
        return prefix + suffix
    
    # Pattern 3: KJV: " / ESV: Both identical.kjv text" — rest
    match = re.search(r'(KJV:\s*)" / ESV: Both identical\.([^"]+)"', line)
    if match:
        prefix = line[:match.start()] + match.group(1) + '"' + match.group(2) + '"'
        suffix = line[match.end():]
        return prefix + suffix
    
    return line


def fix_corrupted_content(content):
    """Fix all corrupted lines in the content."""
    lines = content.split('\n')
    fixed_lines = [fix_corrupted_line(line) for line in lines]
    return '\n'.join(fixed_lines)


def find_esv_rendering(kjv_phrase, esv_verse):
    """
    Find the ESV equivalent of a KJV phrase.
    Returns: (esv_phrase_string, status)
    status: 'different', 'equivalent', 'not_found'
    """
    if not esv_verse or not kjv_phrase:
        return None, 'not_found'
    
    kjv_lower = kjv_phrase.lower().strip()
    esv_lower = esv_verse.lower()
    
    # Direct match - phrase exists verbatim in ESV
    if kjv_lower in esv_lower:
        return None, 'equivalent'
    
    # Check if it's just archaic spelling differences (thee/you, etc.)
    # Try common substitutions
    modified = kjv_lower
    for kjv_word, esv_word in KJV_TO_ESV.items():
        if kjv_word in modified:
            modified = modified.replace(kjv_word, esv_word)
    
    # Also handle archaic pronouns
    archaic_subs = [
        (r'\bthy\b', 'your'), (r'\bthee\b', 'you'), (r'\bthou\b', 'you'),
        (r'\bthine\b', 'your'), (r'\bye\b', 'you'), (r'\bunto\b', 'to'),
        (r'\bhimself\b', 'himself'), (r'\bshall\b', 'will'),
    ]
    for pattern, replacement in archaic_subs:
        modified = re.sub(pattern, replacement, modified)
    
    if modified != kjv_lower and modified in esv_lower:
        idx = esv_lower.find(modified)
        return esv_verse[idx:idx + len(modified)], 'different'
    
    # Try to find a matching segment by key content words
    stop_words = {'the', 'a', 'an', 'of', 'in', 'to', 'and', 'for', 'is', 'are',
                  'was', 'were', 'be', 'been', 'being', 'that', 'which', 'who',
                  'whom', 'this', 'these', 'ye', 'thee', 'thou', 'thy', 'thine',
                  'hath', 'doth', 'shall', 'shalt', 'unto', 'upon', 'thereof',
                  'therein', 'whereby', 'wherein', 'wherefore', 'yea', 'nay',
                  'lo', 'not', 'but', 'with', 'from', 'have', 'has', 'had',
                  'his', 'her', 'our', 'my', 'it', 'its', 'him', 'them', 'their',
                  'all', 'no', 'nor', 'or', 'so', 'as', 'at', 'by', 'on', 'up',
                  'if', 'do', 'did', 'will', 'can', 'may'}
    
    kjv_words = kjv_lower.split()
    content_words = []
    for w in kjv_words:
        clean = w.strip('.,;:!?')
        if clean and clean not in stop_words and len(clean) > 2:
            # Also add ESV equivalent if exists
            content_words.append(clean)
    
    if not content_words:
        return None, 'not_found'
    
    # Sliding window search in ESV
    esv_words = esv_verse.split()
    best_match = None
    best_score = 0
    best_len = 999
    
    window_size = max(len(kjv_words) + 4, 8)
    
    for start in range(len(esv_words)):
        for end in range(start + 1, min(start + window_size + 1, len(esv_words) + 1)):
            window = ' '.join(esv_words[start:end])
            window_lower = window.lower()
            
            score = 0
            for word in content_words:
                if word in window_lower:
                    score += 1
                else:
                    # Check if ESV equivalent is in window
                    for kjv_w, esv_w in KJV_TO_ESV.items():
                        if word == kjv_w and esv_w in window_lower:
                            score += 1
                            break
            
            win_len = end - start
            if score > best_score or (score == best_score and score > 0 and win_len < best_len):
                best_score = score
                best_match = window
                best_len = win_len
    
    # Accept if we matched at least 50% of content words
    threshold = max(1, len(content_words) * 0.5)
    if best_match and best_score >= threshold:
        best_match = best_match.strip('.,;:')
        best_lower = best_match.lower().strip()
        # Make sure it's actually different from KJV
        if best_lower != kjv_lower.strip('.,;:'):
            return best_match, 'different'
        else:
            return None, 'equivalent'
    
    return None, 'not_found'


def process_file(notes_file, esv_file):
    """Process a single study notes file."""
    
    with open(esv_file, 'r', encoding='utf-8') as f:
        esv_content = f.read()
    with open(notes_file, 'r', encoding='utf-8') as f:
        notes_content = f.read()
    
    # Step 1: Fix any corruption from v1
    notes_content = fix_corrupted_content(notes_content)
    
    # Parse ESV verses
    esv_verses = parse_esv_verses(esv_content)
    if not esv_verses:
        return False
    
    # Find TRANSLATION NOTES section
    tn_match = re.search(r'TRANSLATION NOTES\s*\n-+\n', notes_content)
    if not tn_match:
        # Write back fixed content even if no TN section
        with open(notes_file, 'w', encoding='utf-8') as f:
            f.write(notes_content)
        return False
    
    tn_start = tn_match.end()
    
    # Find end of translation notes section
    next_sections = ['GLOSSARY', 'PERSONAL REFLECTION', 'PERSONAL NOTES', 
                     '========']
    tn_end = len(notes_content)
    for section in next_sections:
        idx = notes_content.find(section, tn_start)
        if idx != -1 and idx < tn_end:
            tn_end = idx
    
    tn_section = notes_content[tn_start:tn_end]
    
    # Process the translation notes section
    # We'll work with the full text and use regex to find and modify KJV entries
    
    # Pattern: KJV: "phrase" (not already followed by / ESV:)
    # We need to find each KJV: "phrase" that isn't already followed by / ESV:
    
    result = tn_section
    modified = False
    
    # Find all KJV: "phrase" occurrences
    # Use finditer to get positions
    kjv_pattern = re.compile(r'KJV:\s*"([^"]+)"(?!\s*/ ESV:)')
    
    # We need to also extract the verse number for context
    # Process line by line to maintain verse context
    lines = tn_section.split('\n')
    new_lines = []
    current_verse = None
    
    for line in lines:
        # Check for verse number
        verse_match = re.match(r'^v\.(\d+)(?:-(\d+))?\s', line)
        if verse_match:
            current_verse = int(verse_match.group(1))
            verse_end = int(verse_match.group(2)) if verse_match.group(2) else current_verse
        
        # Check if this line has a KJV: "phrase" without ESV
        kjv_match = kjv_pattern.search(line)
        if kjv_match and current_verse:
            kjv_phrase = kjv_match.group(1)
            
            # Get ESV text for this verse
            esv_text = ''
            v_end = verse_end if verse_match else (current_verse)
            for v in range(current_verse, v_end + 1):
                if v in esv_verses:
                    esv_text += (' ' if esv_text else '') + esv_verses[v]
            
            if esv_text:
                esv_rendering, status = find_esv_rendering(kjv_phrase, esv_text)
                
                if status == 'equivalent':
                    insert = ' / ESV: Both equivalent.'
                elif status == 'different' and esv_rendering:
                    insert = f' / ESV: "{esv_rendering}"'
                else:
                    new_lines.append(line)
                    continue
                
                # Insert after the closing quote of KJV phrase
                insert_pos = kjv_match.end()
                new_line = line[:insert_pos] + insert + line[insert_pos:]
                new_lines.append(new_line)
                modified = True
                continue
        
        new_lines.append(line)
    
    if modified:
        new_tn_section = '\n'.join(new_lines)
        new_content = notes_content[:tn_start] + new_tn_section + notes_content[tn_end:]
        with open(notes_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    else:
        # Still write back the fixed content (in case v1 corruption was fixed)
        with open(notes_file, 'w', encoding='utf-8') as f:
            f.write(notes_content)
        return False


def main():
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
            chapter_dir = os.path.join(book_dir, f"Chapter {chapter}")
            esv_file = os.path.join(chapter_dir, f"Chapter {chapter} - ESV.txt")
            notes_file = os.path.join(chapter_dir, f"Chapter {chapter} - Study Notes.txt")
            
            if not os.path.exists(esv_file):
                print(f"  Chapter {chapter}: ESV file not found")
                continue
            if not os.path.exists(notes_file):
                print(f"  Chapter {chapter}: Study Notes file not found")
                continue
            
            result = process_file(notes_file, esv_file)
            if result:
                total_modified += 1
                print(f"  Chapter {chapter}: Updated")
            else:
                print(f"  Chapter {chapter}: No changes needed")
    
    print(f"\n{'='*50}")
    print(f"Processing complete!")
    print(f"Total chapters processed: {total_chapters}")
    print(f"Total chapters modified: {total_modified}")


if __name__ == '__main__':
    main()
