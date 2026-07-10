#!/usr/bin/env python3
"""
Script to update Translation Notes sections in Bible Study notes files
to include ESV comparisons alongside existing KJV notes.
"""

import os
import re

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


def parse_esv_verses(esv_text):
    """Parse ESV text file into a dictionary of verse_number -> verse_text."""
    verses = {}
    lines = esv_text.strip().split('\n')
    for line in lines:
        line = line.strip()
        # Match lines starting with a number followed by period
        match = re.match(r'^(\d+)\.\s+(.+)$', line)
        if match:
            verse_num = int(match.group(1))
            verse_text = match.group(2)
            verses[verse_num] = verse_text
    return verses


def extract_kjv_phrase(note_text):
    """Extract the KJV quoted phrase from a translation note entry."""
    # Look for KJV: "phrase" pattern
    match = re.search(r'KJV:\s*"([^"]+)"', note_text)
    if match:
        return match.group(1)
    # Look for KJV: "phrase" with smart quotes
    match = re.search(r'KJV:\s*["\u201c]([^"\u201d]+)["\u201d]', note_text)
    if match:
        return match.group(1)
    return None


def find_esv_equivalent(kjv_phrase, esv_verse, verse_num):
    """Find the ESV equivalent of a KJV phrase in the ESV verse text."""
    if not esv_verse or not kjv_phrase:
        return None
    
    kjv_lower = kjv_phrase.lower()
    esv_lower = esv_verse.lower()
    
    # Direct match
    if kjv_lower in esv_lower:
        # Find the actual case version
        idx = esv_lower.find(kjv_lower)
        return esv_verse[idx:idx+len(kjv_phrase)]
    
    # Try to find a close match by looking for key words
    kjv_words = [w for w in kjv_lower.split() if len(w) > 3]
    
    # If most key words appear in ESV, the phrases are likely equivalent
    if kjv_words:
        matches = sum(1 for w in kjv_words if w in esv_lower)
        if matches >= len(kjv_words) * 0.7:
            return None  # Close enough - will need manual comparison
    
    return None


def get_esv_for_verse(esv_verses, verse_num, kjv_phrase):
    """Get the relevant ESV text for a specific verse and KJV phrase."""
    if verse_num not in esv_verses:
        return None
    return esv_verses[verse_num]


def already_has_esv(line):
    """Check if a translation note line already has ESV comparison."""
    return '/ ESV:' in line or 'ESV:' in line.split('—', 2)[-1] if '—' in line else False


def check_note_has_esv(note_block):
    """Check if a multi-line note block already has ESV."""
    return '/ ESV:' in note_block or 'ESV:' in note_block


def process_translation_notes(study_notes_content, esv_verses):
    """Process the translation notes section to add ESV comparisons."""
    
    # Find the TRANSLATION NOTES section
    tn_start = study_notes_content.find('TRANSLATION NOTES')
    if tn_start == -1:
        return study_notes_content, False
    
    # Find the section after TRANSLATION NOTES
    tn_header_end = study_notes_content.find('\n', tn_start)
    separator_end = study_notes_content.find('\n', tn_header_end + 1)
    
    # Find the next section (GLOSSARY, PERSONAL REFLECTION, etc.)
    next_sections = ['GLOSSARY', 'PERSONAL REFLECTION', 'PERSONAL NOTES', 'STUDY NOTES']
    tn_end = len(study_notes_content)
    for section in next_sections:
        idx = study_notes_content.find(section, separator_end)
        if idx != -1 and idx < tn_end:
            tn_end = idx
    
    # Extract the translation notes section
    tn_section = study_notes_content[separator_end:tn_end]
    
    # Process each verse entry
    # Entries start with "v.X" or "v.X-Y"
    lines = tn_section.split('\n')
    new_lines = []
    i = 0
    modified = False
    
    while i < len(lines):
        line = lines[i]
        
        # Check if this is a verse entry line
        verse_match = re.match(r'^(v\.(\d+)(?:-(\d+))?)\s*—\s*(.*)$', line.strip())
        
        if verse_match:
            verse_ref = verse_match.group(1)
            verse_num = int(verse_match.group(2))
            verse_end = verse_match.group(3)
            content = verse_match.group(4)
            
            # Collect the full entry (may span multiple lines)
            full_entry_lines = [line]
            j = i + 1
            while j < len(lines):
                next_line = lines[j]
                # Next entry starts with v.X or is empty line before next entry
                if re.match(r'^v\.\d+', next_line.strip()):
                    break
                if next_line.strip() == '' and j + 1 < len(lines) and re.match(r'^v\.\d+', lines[j+1].strip()):
                    break
                full_entry_lines.append(next_line)
                j += 1
            
            full_entry = '\n'.join(full_entry_lines)
            
            # Check if already has ESV
            if check_note_has_esv(full_entry):
                new_lines.extend(full_entry_lines)
                i = j
                continue
            
            # Get ESV verse text
            esv_text = esv_verses.get(verse_num, '')
            if verse_end:
                # Multi-verse reference - combine
                for v in range(verse_num, int(verse_end) + 1):
                    if v in esv_verses and v != verse_num:
                        esv_text += ' ' + esv_verses[v]
            
            # Extract KJV phrase
            kjv_match = re.search(r'KJV:\s*"([^"]*)"', full_entry)
            if not kjv_match:
                kjv_match = re.search(r'KJV:\s*["\u201c]([^"\u201d]*)["\u201d]', full_entry)
            
            if kjv_match and esv_text:
                kjv_phrase = kjv_match.group(1).lower().strip()
                esv_lower = esv_text.lower()
                
                # Find the corresponding ESV phrase
                esv_phrase = find_corresponding_esv_phrase(kjv_phrase, esv_text)
                
                if esv_phrase:
                    # Insert ESV after KJV quote
                    # Find the position after the KJV quote in the first line
                    first_line = full_entry_lines[0]
                    kjv_end_pos = first_line.find('"', first_line.find('KJV:') + 5)
                    if kjv_end_pos == -1:
                        kjv_end_pos = first_line.find('\u201d', first_line.find('KJV:') + 5)
                    
                    if kjv_end_pos != -1:
                        # Check what comes after the KJV quote
                        after_quote = first_line[kjv_end_pos + 1:].strip()
                        
                        if after_quote.startswith('—') or after_quote.startswith('\u2014'):
                            # Insert ESV before the dash
                            insert_text = f' / ESV: "{esv_phrase}"'
                            new_first_line = first_line[:kjv_end_pos + 1] + insert_text + ' ' + first_line[kjv_end_pos + 1:].lstrip()
                            # Adjust spacing
                            new_first_line = re.sub(r'\s+—', ' —', new_first_line)
                        else:
                            insert_text = f' / ESV: "{esv_phrase}"'
                            new_first_line = first_line[:kjv_end_pos + 1] + insert_text + first_line[kjv_end_pos + 1:]
                        
                        full_entry_lines[0] = new_first_line
                        modified = True
                    else:
                        # Try alternate approach - add ESV on same line after KJV content
                        pass
                elif esv_text:
                    # Phrases are identical or very similar
                    if kjv_phrase in esv_lower or esv_lower.find(kjv_phrase) != -1:
                        # Identical phrase exists in ESV
                        first_line = full_entry_lines[0]
                        kjv_end_pos = first_line.find('"', first_line.find('KJV:') + 5)
                        if kjv_end_pos == -1:
                            kjv_end_pos = first_line.find('\u201d', first_line.find('KJV:') + 5)
                        if kjv_end_pos != -1:
                            after_quote = first_line[kjv_end_pos + 1:].strip()
                            insert_text = ' / ESV: Both equivalent.'
                            if after_quote.startswith('—') or after_quote.startswith('\u2014'):
                                new_first_line = first_line[:kjv_end_pos + 1] + insert_text + ' ' + first_line[kjv_end_pos + 1:].lstrip()
                                new_first_line = re.sub(r'\s+—', ' —', new_first_line)
                            else:
                                new_first_line = first_line[:kjv_end_pos + 1] + insert_text + first_line[kjv_end_pos + 1:]
                            full_entry_lines[0] = new_first_line
                            modified = True
            elif esv_text and 'KJV:' in full_entry:
                # Has KJV reference but no quoted phrase - try to add ESV comparison
                # Look for the pattern: KJV: "text" where text might use different quote style
                pass
            
            new_lines.extend(full_entry_lines)
            i = j
        else:
            new_lines.append(line)
            i += 1
    
    if modified:
        new_tn_section = '\n'.join(new_lines)
        result = study_notes_content[:separator_end] + new_tn_section + study_notes_content[tn_end:]
        return result, True
    
    return study_notes_content, False


def find_corresponding_esv_phrase(kjv_phrase_lower, esv_text):
    """Find the ESV equivalent of a KJV phrase."""
    esv_lower = esv_text.lower()
    
    # Direct match - phrases are identical
    if kjv_phrase_lower in esv_lower:
        return None  # Same phrase, will mark as equivalent
    
    # Common KJV -> ESV word substitutions
    kjv_to_esv_mappings = {
        'charity': 'love',
        'conversation': 'conduct',
        'prevent': 'precede',
        'let': 'restrain',
        'suffer': 'allow',
        'by and by': 'immediately',
        'meat': 'food',
        'quick': 'living',
        'peculiar': 'his own possession',
        'study': 'aspire',
        'communicate': 'share',
        'ghost': 'spirit',
        'holy ghost': 'holy spirit',
        'shew': 'show',
        'saith': 'says',
        'hath': 'has',
        'doth': 'does',
        'wherefore': 'therefore',
        'unto': 'to',
        'thee': 'you',
        'thou': 'you',
        'thy': 'your',
        'thine': 'your',
        'ye': 'you',
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
        'which': 'who',
        'that which': 'what',
    }
    
    # Try substituting KJV words with ESV equivalents
    modified_phrase = kjv_phrase_lower
    for kjv_word, esv_word in kjv_to_esv_mappings.items():
        if kjv_word in modified_phrase:
            modified_phrase = modified_phrase.replace(kjv_word, esv_word)
    
    if modified_phrase != kjv_phrase_lower and modified_phrase in esv_lower:
        idx = esv_lower.find(modified_phrase)
        return esv_text[idx:idx + len(modified_phrase)]
    
    # Try to find the ESV rendering by looking for key content words
    # Remove common KJV function words
    kjv_content_words = [w for w in kjv_phrase_lower.split() 
                         if w not in ('the', 'a', 'an', 'of', 'in', 'to', 'and', 'for', 
                                     'is', 'are', 'was', 'were', 'be', 'been', 'being',
                                     'that', 'which', 'who', 'whom', 'this', 'these',
                                     'ye', 'thee', 'thou', 'thy', 'thine', 'hath',
                                     'doth', 'shall', 'shalt', 'unto', 'upon')]
    
    if not kjv_content_words:
        return None
    
    # Find a window in ESV that contains most of these content words
    esv_words = esv_text.split()
    best_match = None
    best_score = 0
    
    window_size = len(kjv_phrase_lower.split()) + 4  # Allow some extra words
    
    for start in range(len(esv_words)):
        end = min(start + window_size, len(esv_words))
        window = ' '.join(esv_words[start:end]).lower()
        
        score = 0
        for word in kjv_content_words:
            # Check for the word or its common ESV equivalent
            if word in window:
                score += 1
            else:
                for kjv_w, esv_w in kjv_to_esv_mappings.items():
                    if word == kjv_w and esv_w in window:
                        score += 1
                        break
        
        if score > best_score and score >= len(kjv_content_words) * 0.5:
            best_score = score
            best_match = ' '.join(esv_words[start:end])
    
    if best_match and best_match.lower() != kjv_phrase_lower:
        # Clean up the match - remove trailing punctuation if needed
        best_match = best_match.strip('.,;:')
        return best_match
    
    return None


def process_chapter(book_dir, book_name, chapter_num):
    """Process a single chapter."""
    chapter_dir = os.path.join(book_dir, f"Chapter {chapter_num}")
    esv_file = os.path.join(chapter_dir, f"Chapter {chapter_num} - ESV.txt")
    notes_file = os.path.join(chapter_dir, f"Chapter {chapter_num} - Study Notes.txt")
    
    if not os.path.exists(esv_file):
        print(f"  WARNING: ESV file not found: {esv_file}")
        return False
    if not os.path.exists(notes_file):
        print(f"  WARNING: Study Notes file not found: {notes_file}")
        return False
    
    # Read files
    with open(esv_file, 'r', encoding='utf-8') as f:
        esv_content = f.read()
    with open(notes_file, 'r', encoding='utf-8') as f:
        notes_content = f.read()
    
    # Parse ESV verses
    esv_verses = parse_esv_verses(esv_content)
    
    if not esv_verses:
        print(f"  WARNING: No verses parsed from ESV file for {book_name} Ch.{chapter_num}")
        return False
    
    # Process translation notes
    updated_content, was_modified = process_translation_notes(notes_content, esv_verses)
    
    if was_modified:
        with open(notes_file, 'w', encoding='utf-8') as f:
            f.write(updated_content)
        return True
    
    return False


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
            result = process_chapter(book_dir, book_name, chapter)
            if result:
                total_modified += 1
                print(f"  Chapter {chapter}: Updated")
            else:
                print(f"  Chapter {chapter}: No changes needed or file not found")
    
    print(f"\n{'='*50}")
    print(f"Processing complete!")
    print(f"Total chapters processed: {total_chapters}")
    print(f"Total chapters modified: {total_modified}")


if __name__ == '__main__':
    main()
