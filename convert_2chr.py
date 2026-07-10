#!/usr/bin/env python3
"""
Convert KEY VERSES and CROSS-REFERENCES from KJV to ESV in 2 Chronicles Study Notes.
This script handles chapters 9-36 (chapters 1-8 already done manually).
"""

import os
import re

BASE_DIR = "/Users/jeremymcadoo/Desktop/Kiro Projects/Bible Study/Old Testament/14 - 2 Chronicles"

def get_esv_verses(esv_file):
    """Parse ESV file into a dict of verse_number -> text."""
    verses = {}
    with open(esv_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Match lines starting with verse numbers
    for match in re.finditer(r'^(\d+)\.\s+(.+?)(?=\n\d+\.\s+|\n*$)', content, re.MULTILINE | re.DOTALL):
        num = int(match.group(1))
        text = match.group(2).strip()
        # Clean up multi-line verses
        text = re.sub(r'\s+', ' ', text)
        verses[num] = text
    
    return verses

def find_section(content, section_name):
    """Find the start and end positions of a section."""
    pattern = rf'^{re.escape(section_name)}\s*\n-+\n'
    match = re.search(pattern, content, re.MULTILINE)
    if not match:
        return None, None
    
    start = match.end()
    
    # Find the next section header (ALL CAPS followed by dashes)
    next_section = re.search(r'^\n[A-Z][A-Z &]+\n-+\n', content[start:], re.MULTILINE)
    if next_section:
        end = start + next_section.start()
    else:
        end = len(content)
    
    return start, end

def replace_kjv_with_esv_in_key_verses(section_text, esv_verses):
    """Replace KJV quotations in KEY VERSES with ESV text."""
    result = section_text
    
    # Find verse entries like "v.1  — " or "v.10 — "
    # Pattern: verse ref, quoted text (possibly multi-line), (KJV) marker, then commentary
    entries = list(re.finditer(r'(v\.(\d+)\s*—\s*)"([^"]*?)"(\s*\(KJV\))', result, re.DOTALL))
    
    for match in reversed(entries):  # Process in reverse to maintain positions
        verse_num = int(match.group(2))
        if verse_num in esv_verses:
            esv_text = esv_verses[verse_num]
            
            # Format the ESV text with proper indentation (~72 char wrap)
            prefix = match.group(1)  # "v.X  — "
            indent = "        "  # 8 spaces for continuation lines
            
            # Wrap the ESV text
            wrapped = wrap_text(esv_text, 72 - len(indent), indent)
            
            # First line gets the prefix formatting preserved from original
            # Replace the old quoted text + (KJV) with new quoted text + (ESV)
            new_text = f'"{wrapped}" (ESV)'
            old_start = match.start(3) - 1  # Include opening quote
            old_end = match.end(4)  # Include (KJV)
            
            result = result[:old_start] + new_text + result[old_end:]
    
    return result

def replace_kjv_with_esv_in_crossrefs(section_text, esv_verses_by_book=None):
    """Replace KJV language in CROSS-REFERENCES with ESV text."""
    result = section_text
    
    # KJV indicators
    kjv_words = ['thee', 'thou', 'thy', 'thine', 'ye', 'hath', 'saith', 
                 'shalt', 'unto', 'doth', 'doeth', 'giveth', 'maketh',
                 'cometh', 'goeth', 'keepeth', 'loveth', 'endureth',
                 'taketh', 'turneth', 'hearken', 'wherefore', 'thereof',
                 'therein', 'thereat', 'whereunto', 'hearest', 'seeketh',
                 'remaineth', 'abideth', 'dwelleth', 'knoweth', 'seeth',
                 'speaketh', 'worketh', 'believeth', 'receiveth', 'bringeth',
                 'teacheth', 'liveth', 'reigneth', 'judgeth', 'saveth',
                 'sendeth', 'buildeth', 'planteth', 'calleth', 'leadeth',
                 'feedeth', 'holdeth', 'standeth', 'sitteth', 'lieth',
                 'walketh', 'runneth', 'fighteth', 'striketh', 'breaketh',
                 'wilt', 'wouldest', 'canst', 'didst', 'dost', 'hast',
                 'hadst', 'mayest', 'mightest', 'shouldest', 'couldest',
                 'art', 'wast', 'wert',
                 'bethink', 'whoso', 'whosoever', 'whatsoever',
                 'forasmuch', 'inasmuch', 'insomuch', 'howbeit',
                 'peradventure', 'notwithstanding', 'nought',
                 'beseech', 'becometh', 'availeth', 'profiteth',
                 'burneth', 'consumeth', 'destroyeth', 'delivereth']
    
    # Find quoted text in cross-references that uses KJV language
    # Pattern: "quoted text" possibly followed by commentary
    quotes = list(re.finditer(r'"([^"]+)"', result))
    
    for match in quotes:
        quote_text = match.group(1).lower()
        # Check if this quote contains KJV language
        has_kjv = any(re.search(r'\b' + word + r'\b', quote_text) for word in kjv_words)
        if has_kjv:
            # Mark this for manual review - we can't automatically replace
            # cross-references to other books without their ESV text
            pass  # We'll handle this with the chapter's own ESV file for same-chapter refs
    
    return result

def wrap_text(text, width, indent):
    """Wrap text to specified width with indent for continuation lines."""
    words = text.split()
    lines = []
    current_line = ""
    
    for word in words:
        if not current_line:
            current_line = word
        elif len(current_line) + 1 + len(word) <= width:
            current_line += " " + word
        else:
            lines.append(current_line)
            current_line = word
    
    if current_line:
        lines.append(current_line)
    
    if not lines:
        return ""
    
    # First line (no extra indent, will be placed after the opening quote in context)
    result = lines[0]
    for line in lines[1:]:
        result += "\n" + indent + line
    
    return result

def process_chapter(chapter_num):
    """Process a single chapter."""
    chapter_dir = os.path.join(BASE_DIR, f"Chapter {chapter_num}")
    study_file = os.path.join(chapter_dir, f"Chapter {chapter_num} - Study Notes.txt")
    esv_file = os.path.join(chapter_dir, f"Chapter {chapter_num} - ESV.txt")
    
    if not os.path.exists(study_file) or not os.path.exists(esv_file):
        print(f"Chapter {chapter_num}: Missing files, skipping.")
        return False
    
    # Read files
    with open(study_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    esv_verses = get_esv_verses(esv_file)
    
    # Find KEY VERSES section
    kv_start, kv_end = find_section(content, "KEY VERSES")
    if kv_start is None:
        print(f"Chapter {chapter_num}: No KEY VERSES section found.")
        return False
    
    # Process KEY VERSES section
    kv_section = content[kv_start:kv_end]
    new_kv_section = replace_kjv_with_esv_in_key_verses(kv_section, esv_verses)
    
    # Replace in content
    new_content = content[:kv_start] + new_kv_section + content[kv_end:]
    
    # Write back
    with open(study_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Chapter {chapter_num}: KEY VERSES updated successfully.")
    return True

def main():
    """Process chapters 9-36."""
    for chapter_num in range(9, 37):
        try:
            process_chapter(chapter_num)
        except Exception as e:
            print(f"Chapter {chapter_num}: ERROR - {e}")

if __name__ == "__main__":
    main()
