#!/usr/bin/env python3
"""
Convert KEY VERSES from KJV to ESV in 2 Chronicles Study Notes.
Handles chapters 9-36. Fixed version with proper formatting.
"""

import os
import re
import textwrap

BASE_DIR = "/Users/jeremymcadoo/Desktop/Kiro Projects/Bible Study/Old Testament/14 - 2 Chronicles"

def get_esv_verses(esv_file):
    """Parse ESV file into a dict of verse_number -> text."""
    verses = {}
    with open(esv_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    current_verse = None
    current_text = ""
    
    for line in lines:
        match = re.match(r'^(\d+)\.\s+(.+)', line)
        if match:
            if current_verse is not None:
                verses[current_verse] = current_text.strip()
            current_verse = int(match.group(1))
            current_text = match.group(2)
        elif current_verse is not None and line.strip():
            current_text += " " + line.strip()
    
    if current_verse is not None:
        verses[current_verse] = current_text.strip()
    
    return verses

def format_verse_entry(verse_ref, esv_text, commentary):
    """
    Format a complete KEY VERSES entry with proper wrapping.
    verse_ref: like "v.6  — " or "v.14 — "
    esv_text: the ESV verse text
    commentary: the commentary text after (ESV)
    """
    indent = "        "  # 8 spaces
    
    # Handle verses that end with a quote mark inside the verse text
    # Remove trailing quote if it's a speech ending (the verse text itself contains quotes)
    # ESV uses proper quotation marks
    
    # Build the quoted verse line
    # First line: verse_ref + "esv_text..." (ESV) — commentary...
    first_line_prefix = verse_ref + '"'
    first_line_width = 72 - len(first_line_prefix)
    
    # Wrap ESV text
    words = esv_text.split()
    lines = []
    current_line = ""
    first_line = True
    
    for word in words:
        width = first_line_width if first_line else (72 - len(indent))
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
    
    # Build verse text block
    if len(lines) == 1:
        verse_block = first_line_prefix + lines[0] + '"'
    else:
        verse_block = first_line_prefix + lines[0] + "\n"
        for i, line in enumerate(lines[1:]):
            if i == len(lines) - 2:  # Last line
                verse_block += indent + line + '"'
            else:
                verse_block += indent + line + "\n"
    
    # Add (ESV) marker and dash before commentary
    full_text = verse_block + " (ESV)"
    
    # Now add the commentary with proper wrapping
    if commentary.strip():
        # Commentary starts with " — " separator
        commentary = commentary.strip()
        if not commentary.startswith("—") and not commentary.startswith("-"):
            commentary = "— " + commentary
        
        # Wrap commentary
        comm_lines = []
        # First commentary line goes on same line as (ESV) if it fits
        # Actually, let's check the pattern - commentary follows on same line after (ESV)
        # with " — " as separator
        
        remaining = " " + commentary
        # Check if (ESV) + remaining fits on current line
        last_verse_line = verse_block.split('\n')[-1]
        current_pos = len(last_verse_line) + len(" (ESV)")
        
        # Wrap the full remaining text starting from current position
        comm_words = remaining.split()
        comm_current = ""
        comm_first = True
        
        for word in comm_words:
            if comm_first:
                avail = 72 - current_pos
            else:
                avail = 72 - len(indent)
            
            if not comm_current:
                comm_current = word
            elif len(comm_current) + 1 + len(word) <= avail:
                comm_current += " " + word
            else:
                comm_lines.append(comm_current)
                comm_current = word
                comm_first = False
        if comm_current:
            comm_lines.append(comm_current)
        
        if comm_lines:
            full_text += comm_lines[0]
            for line in comm_lines[1:]:
                full_text += "\n" + indent + line
    
    return full_text

def process_chapter(chapter_num):
    """Process a single chapter's KEY VERSES section."""
    chapter_dir = os.path.join(BASE_DIR, f"Chapter {chapter_num}")
    study_file = os.path.join(chapter_dir, f"Chapter {chapter_num} - Study Notes.txt")
    esv_file = os.path.join(chapter_dir, f"Chapter {chapter_num} - ESV.txt")
    
    if not os.path.exists(study_file) or not os.path.exists(esv_file):
        print(f"Chapter {chapter_num}: Missing files, skipping.")
        return False
    
    with open(study_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    esv_verses = get_esv_verses(esv_file)
    
    # Find KEY VERSES section
    kv_header = re.search(r'^KEY VERSES\n-+\n', content, re.MULTILINE)
    if not kv_header:
        print(f"Chapter {chapter_num}: No KEY VERSES section.")
        return False
    
    kv_start = kv_header.end()
    
    # Find end of KEY VERSES (next section header)
    next_section = re.search(r'\n\n[A-Z][A-Z &/]+\n-+\n', content[kv_start:])
    if next_section:
        kv_end = kv_start + next_section.start()
    else:
        kv_end = len(content)
    
    section = content[kv_start:kv_end]
    
    # Parse individual verse entries
    # Each entry starts with "v.NUMBER" at the beginning of a line (or after \n)
    # Split on verse boundaries
    entry_pattern = r'(?:^|\n)(v\.(\d+)\s*(?:[-–—])\s*)'
    entries = list(re.finditer(entry_pattern, section))
    
    if not entries:
        print(f"Chapter {chapter_num}: No verse entries found in KEY VERSES.")
        return False
    
    new_entries = []
    changed = False
    
    for i, entry_match in enumerate(entries):
        # Get the full text of this entry (up to next entry or end)
        entry_start = entry_match.start()
        if entry_match.group(0).startswith('\n'):
            entry_start += 1  # Skip the leading newline
        
        if i + 1 < len(entries):
            next_start = entries[i+1].start()
            if section[entries[i+1].start()] == '\n':
                next_start += 0  # Include trailing newline with current entry
            entry_text = section[entry_start:entries[i+1].start()]
        else:
            entry_text = section[entry_start:]
        
        verse_num = int(entry_match.group(2))
        
        # Check if this entry has (KJV) or (ESV) already from first script run
        # Pattern: starts with verse ref, then quoted text, then marker
        # Handle both (KJV) that needs replacing and (ESV) that was already 
        # replaced but may have bad formatting
        
        # Try to find the quoted verse text and marker
        # The quote starts after "v.X  — " and is enclosed in double quotes
        # Can span multiple lines
        quote_match = re.match(
            r'(v\.\d+\s*[-–—]\s*)"(.*?)"\s*\((KJV|ESV)\)\s*(.*)',
            entry_text, re.DOTALL
        )
        
        if quote_match:
            verse_ref = quote_match.group(1)
            old_text = quote_match.group(2)
            marker = quote_match.group(3)
            commentary = quote_match.group(4)
            
            if verse_num in esv_verses:
                esv_text = esv_verses[verse_num]
                new_entry = format_verse_entry(verse_ref, esv_text, commentary)
                new_entries.append(new_entry)
                changed = True
            else:
                new_entries.append(entry_text.rstrip())
        else:
            new_entries.append(entry_text.rstrip())
    
    if changed:
        # Rebuild section
        new_section = "\n".join(new_entries) + "\n"
        new_content = content[:kv_start] + new_section + content[kv_end:]
        
        with open(study_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Chapter {chapter_num}: KEY VERSES reformatted.")
    else:
        print(f"Chapter {chapter_num}: No changes needed.")
    
    return True

def main():
    for chapter_num in range(9, 37):
        try:
            process_chapter(chapter_num)
        except Exception as e:
            print(f"Chapter {chapter_num}: ERROR - {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    main()
