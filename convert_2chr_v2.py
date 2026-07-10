#!/usr/bin/env python3
"""
Convert KEY VERSES and CROSS-REFERENCES from KJV to ESV in 2 Chronicles Study Notes.
This script handles chapters 9-36.
Fixed version with proper line wrapping.
"""

import os
import re

BASE_DIR = "/Users/jeremymcadoo/Desktop/Kiro Projects/Bible Study/Old Testament/14 - 2 Chronicles"

def get_esv_verses(esv_file):
    """Parse ESV file into a dict of verse_number -> text."""
    verses = {}
    with open(esv_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Match lines starting with verse numbers - handle multi-line verses
    lines = content.split('\n')
    current_verse = None
    current_text = ""
    
    for line in lines:
        match = re.match(r'^(\d+)\.\s+(.+)', line)
        if match:
            # Save previous verse
            if current_verse is not None:
                verses[current_verse] = current_text.strip()
            current_verse = int(match.group(1))
            current_text = match.group(2)
        elif current_verse is not None and line.strip():
            # Continuation of current verse (shouldn't happen normally but just in case)
            current_text += " " + line.strip()
    
    # Save last verse
    if current_verse is not None:
        verses[current_verse] = current_text.strip()
    
    return verses

def find_section_bounds(content, section_name):
    """Find the start and end positions of a section."""
    # Look for section header
    pattern = rf'^{re.escape(section_name)}\s*\n-+\n'
    match = re.search(pattern, content, re.MULTILINE)
    if not match:
        return None, None
    
    start = match.end()
    
    # Find the next section (line that starts with uppercase word followed by newline and dashes)
    rest = content[start:]
    next_match = re.search(r'\n\n[A-Z][A-Z &/]+\n-+\n', rest)
    if next_match:
        end = start + next_match.start()
    else:
        end = len(content)
    
    return start, end

def wrap_verse_text(text, first_line_width=64, continuation_indent="        ", max_width=72):
    """
    Wrap verse text for display in study notes.
    first_line_width: available chars on first line (after 'v.X  — "')
    continuation_indent: spaces before continuation lines (8 spaces)
    max_width: total line width
    """
    cont_width = max_width - len(continuation_indent)
    words = text.split()
    lines = []
    current_line = ""
    first_line = True
    
    for word in words:
        width = first_line_width if first_line else cont_width
        if not current_line:
            current_line = word
        elif len(current_line) + 1 + len(word) <= width:
            current_line += " " + word
        else:
            lines.append(current_line)
            current_line = word
            first_line = False
    
    if current_line:
        lines.append(current_line)
    
    if not lines:
        return ""
    
    # Join with continuation indent
    result = lines[0]
    for i, line in enumerate(lines[1:], 1):
        result += "\n" + continuation_indent + line
    
    return result

def process_key_verses(content, esv_verses):
    """Process the KEY VERSES section, replacing KJV with ESV."""
    kv_start, kv_end = find_section_bounds(content, "KEY VERSES")
    if kv_start is None:
        return content, False
    
    section = content[kv_start:kv_end]
    
    # Find all verse entries with (KJV) markers
    # Pattern: v.NUM — "...text..." (KJV) — commentary
    # The verse text can span multiple lines
    
    # We need to find each entry and replace it
    # Entry format: v.XX — "quoted KJV text" (KJV) followed by commentary
    
    new_section = section
    
    # Find patterns: start with v.NUMBER, then quoted text ending with (KJV)
    # Use a more careful approach - find each verse entry
    entries = []
    
    # Split into verse entries (each starts with "v." at line start or after newlines)
    parts = re.split(r'(?=\nv\.\d)', section)
    
    rebuilt_section = ""
    for part in parts:
        # Check if this part has a (KJV) marker
        kjv_match = re.search(r'^(\n?v\.(\d+)\s*(?:[-–—])\s*)"(.*?)"\s*\(KJV\)', part, re.DOTALL)
        if kjv_match:
            verse_num = int(kjv_match.group(2))
            prefix = kjv_match.group(1)  # e.g., "\nv.6  — "
            
            if verse_num in esv_verses:
                esv_text = esv_verses[verse_num]
                
                # Calculate first line available width
                # prefix is like "v.6  — " which gives us ~8 chars used + 1 for quote
                prefix_on_line = prefix.split('\n')[-1]  # Get last line of prefix
                first_line_used = len(prefix_on_line) + 1  # +1 for opening quote
                first_line_width = 72 - first_line_used
                
                # Wrap the ESV text
                wrapped = wrap_verse_text(esv_text, first_line_width, "        ", 72)
                
                # Replace the quoted text
                after_kjv = part[kjv_match.end():]
                new_part = f'{prefix}"{wrapped}" (ESV){after_kjv}'
                rebuilt_section += new_part
            else:
                rebuilt_section += part
        else:
            rebuilt_section += part
    
    # Replace section in content
    new_content = content[:kv_start] + rebuilt_section + content[kv_end:]
    return new_content, True

def process_cross_references(content, chapter_esv_verses):
    """Process the CROSS-REFERENCES section, replacing KJV language with ESV."""
    cr_start, cr_end = find_section_bounds(content, "CROSS-REFERENCES")
    if cr_start is None:
        return content, False
    
    section = content[cr_start:cr_end]
    
    # KJV indicators - words that mark KJV-style language
    kjv_patterns = [
        r'\bthee\b', r'\bthou\b', r'\bthy\b', r'\bthine\b', r'\bye\b',
        r'\bhath\b', r'\bsaith\b', r'\bshalt\b', r'\bunto\b', r'\bdoth\b',
        r'\bgiveth\b', r'\bmaketh\b', r'\bcometh\b', r'\bgoeth\b',
        r'\bkeepeth\b', r'\bloveth\b', r'\bendureth\b', r'\btaketh\b',
        r'\bhearken\b', r'\bwherefore\b', r'\bthereof\b', r'\btherein\b',
        r'\bthereat\b', r'\bwhereunto\b', r'\bhearest\b', r'\bseeketh\b',
        r'\babideth\b', r'\bdwelleth\b', r'\bknoweth\b', r'\bseeth\b',
        r'\bspeaketh\b', r'\bworketh\b', r'\bbelieveth\b', r'\breceiveth\b',
        r'\bbringeth\b', r'\bteacheth\b', r'\bliveth\b', r'\breigneth\b',
        r'\bjudgeth\b', r'\bsendeth\b', r'\bcalleth\b', r'\bleadeth\b',
        r'\bfeedeth\b', r'\bholdeth\b', r'\bstandeth\b', r'\bsitteth\b',
        r'\bwalketh\b', r'\brunneth\b', r'\bburneth\b', r'\bconsumeth\b',
        r'\bdestroyeth\b', r'\bdelivereth\b', r'\bwilt\b', r'\bcanst\b',
        r'\bdidst\b', r'\bdost\b', r'\bhast\b', r'\bmayest\b',
        r'\bart\b(?!\s+of)', r'\bwast\b', r'\bwert\b', r'\bbethink\b',
        r'\bwhoso\b', r'\bwhosoever\b', r'\bforasmuch\b',
        r'\bhowbeit\b', r'\bperadventure\b', r'\bbeseech\b',
        r'\bavaileth\b', r'\bprofiteth\b', r'\bturneth\b',
        r'\bsaveth\b', r'\bplucketh\b', r'\btrusteth\b',
        r'\bfeareth\b', r'\bfindeth\b', r'\bblesseth\b',
        r'\bhateth\b', r'\bsmiteth\b', r'\bforsake\b.*\bthee\b',
        r'\blieth\b', r'\btwain\b', r'\brent\b(?=.*temple)',
        r'\bhath\b', r'\bshewn\b', r'\bshew\b',
    ]
    
    # Find all quoted text in cross-references
    # We'll check each quote for KJV language
    quotes = list(re.finditer(r'"([^"]+)"', section))
    
    modified = False
    offset = 0
    new_section = section
    
    for match in quotes:
        quote_text = match.group(1)
        quote_lower = quote_text.lower()
        
        # Check if quote uses KJV language
        is_kjv = any(re.search(pat, quote_lower) for pat in kjv_patterns)
        
        if is_kjv:
            # Check if there's already an (ESV) marker after this quote
            after_pos = match.end() + offset
            after_text = new_section[after_pos:after_pos+10]
            if '(ESV)' in after_text:
                continue  # Already converted
            
            # We can't automatically replace cross-reference text from other books
            # since we don't have those ESV files in context.
            # But we can mark them for replacement. For this chapter's own verses,
            # we can use the ESV text.
            modified = True
    
    if not modified:
        return content, False
    
    return content, False  # Return unchanged - we'll handle cross-refs manually

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
    
    # Process KEY VERSES section
    new_content, kv_changed = process_key_verses(content, esv_verses)
    
    if kv_changed:
        with open(study_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Chapter {chapter_num}: KEY VERSES updated.")
    else:
        print(f"Chapter {chapter_num}: No KEY VERSES changes needed.")
    
    return True

def main():
    """Process chapters 9-36."""
    for chapter_num in range(9, 37):
        try:
            process_chapter(chapter_num)
        except Exception as e:
            print(f"Chapter {chapter_num}: ERROR - {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()
