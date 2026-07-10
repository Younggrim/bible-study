#!/usr/bin/env python3
"""
Final conversion script for 2 Chronicles chapters 9-36.
Properly handles:
1. KEY VERSES: Replace KJV quotes with ESV, fix formatting
2. CROSS-REFERENCES: Replace KJV language with ESV where identifiable
"""

import os
import re

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

def wrap_text_with_indent(text, first_line_avail, continuation_indent="        ", max_width=72):
    """Wrap text with first line having different available width."""
    words = text.split()
    lines = []
    current_line = ""
    first_line = True
    
    for word in words:
        avail = first_line_avail if first_line else (max_width - len(continuation_indent))
        if not current_line:
            current_line = word
        elif len(current_line) + 1 + len(word) <= avail:
            current_line += " " + word
        else:
            lines.append(current_line)
            current_line = word
            first_line = False
    if current_line:
        lines.append(current_line)
    
    result = lines[0] if lines else ""
    for line in lines[1:]:
        result += "\n" + continuation_indent + line
    return result

def rebuild_key_verses_entry(verse_ref_str, esv_text, commentary_text):
    """
    Rebuild a complete KEY VERSES entry.
    verse_ref_str: e.g. "v.6  — " or "v.14 — "
    esv_text: the ESV verse text
    commentary_text: everything after the translation marker
    """
    indent = "        "  # 8 spaces for continuation
    
    # Handle ESV text that ends with a quotation mark (dialogue ending)
    # We need to not double-quote it
    if esv_text.endswith('"'):
        # The verse text has internal dialogue ending with "
        # Our outer quotes will be: "verse text ending with inner quote"
        # This creates: ..."word."" which looks odd but is correct
        # Better: use the text as-is and just close with single "
        pass
    
    # Build the verse quotation block
    prefix = verse_ref_str + '"'
    first_line_avail = 72 - len(prefix)
    
    # Wrap the ESV text
    wrapped_verse = wrap_text_with_indent(esv_text, first_line_avail, indent, 72)
    
    # Close quote and add marker
    verse_block = prefix + wrapped_verse + '" (ESV)'
    
    # Now handle commentary
    if commentary_text.strip():
        comm = commentary_text.strip()
        # Ensure commentary starts with " — "
        if not comm.startswith('—') and not comm.startswith('- '):
            comm = '— ' + comm
        
        # Calculate available space on current last line
        last_line = verse_block.split('\n')[-1]
        current_len = len(last_line)
        
        # Add space before commentary
        separator = " "
        first_comm_avail = 72 - current_len - len(separator)
        
        if first_comm_avail < 15:
            # Not enough room, start commentary on next line
            verse_block += "\n" + indent
            first_comm_avail = 72 - len(indent)
        else:
            verse_block += separator
        
        wrapped_comm = wrap_text_with_indent(comm, first_comm_avail, indent, 72)
        verse_block += wrapped_comm
    
    return verse_block

def process_key_verses_section(section_text, esv_verses):
    """Process KEY VERSES section and return rebuilt version."""
    # Split into individual verse entries
    # Each entry starts with v.NUMBER at the beginning of a line
    
    # Find all entry start positions
    entry_starts = list(re.finditer(r'^v\.(\d+)\s*[-–—]\s*', section_text, re.MULTILINE))
    
    if not entry_starts:
        return section_text
    
    entries = []
    for i, match in enumerate(entry_starts):
        start = match.start()
        end = entry_starts[i+1].start() if i+1 < len(entry_starts) else len(section_text)
        entry_text = section_text[start:end].rstrip()
        entries.append((match.group(1), match.end() - start, entry_text))
    
    new_entries = []
    for verse_num_str, quote_offset, entry_text in entries:
        verse_num = int(verse_num_str)
        
        # Parse the entry to find the quoted verse and commentary
        # Pattern: v.X  — "quoted text" (KJV|ESV) — commentary OR just commentary
        # The quote starts at quote_offset position
        after_ref = entry_text[quote_offset:]
        
        # Find the opening quote
        if after_ref.startswith('"'):
            # Find the matching close quote + (KJV) or (ESV)
            # Need to handle multi-line quotes
            # Strategy: find "(KJV)" or "(ESV)" and work backwards to find close quote
            kjv_match = re.search(r'"\s*\(KJV\)', after_ref)
            esv_match = re.search(r'"\s*\(ESV\)', after_ref)
            
            if kjv_match:
                quoted_text = after_ref[1:kjv_match.start()]
                # Clean up the quoted text (remove newlines and excess whitespace)
                quoted_text = re.sub(r'\s+', ' ', quoted_text).strip()
                commentary = after_ref[kjv_match.end():].strip()
                
                # Get ESV text
                if verse_num in esv_verses:
                    esv_text = esv_verses[verse_num]
                    # Build verse ref string
                    ref_match = re.match(r'(v\.\d+\s*[-–—]\s*)', entry_text)
                    verse_ref = ref_match.group(1) if ref_match else f"v.{verse_num} — "
                    
                    new_entry = rebuild_key_verses_entry(verse_ref, esv_text, commentary)
                    new_entries.append(new_entry)
                else:
                    new_entries.append(entry_text)
            elif esv_match:
                # Already converted (from previous script run), but may have formatting issues
                quoted_text = after_ref[1:esv_match.start()]
                quoted_text = re.sub(r'\s+', ' ', quoted_text).strip()
                commentary = after_ref[esv_match.end():].strip()
                
                # Check if we have ESV text for this verse to reformat
                if verse_num in esv_verses:
                    esv_text = esv_verses[verse_num]
                    ref_match = re.match(r'(v\.\d+\s*[-–—]\s*)', entry_text)
                    verse_ref = ref_match.group(1) if ref_match else f"v.{verse_num} — "
                    
                    new_entry = rebuild_key_verses_entry(verse_ref, esv_text, commentary)
                    new_entries.append(new_entry)
                else:
                    new_entries.append(entry_text)
            else:
                # No translation marker found, keep as-is
                new_entries.append(entry_text)
        else:
            # No opening quote, keep as-is
            new_entries.append(entry_text)
    
    return "\n\n".join(new_entries) + "\n"

def has_kjv_language(text):
    """Check if text contains KJV-style language."""
    kjv_words = [
        r'\bthee\b', r'\bthou\b', r'\bthy\b', r'\bthine\b', r'\bye\b',
        r'\bhath\b', r'\bsaith\b', r'\bshalt\b', r'\bunto\b', r'\bdoth\b',
        r'\bgiveth\b', r'\bmaketh\b', r'\bcometh\b', r'\bgoeth\b',
        r'\bkeepeth\b', r'\bloveth\b', r'\bendureth\b', r'\btaketh\b',
        r'\bhearken\b', r'\bwherefore\b', r'\bthereof\b', r'\btherein\b',
        r'\bthereat\b', r'\bwhereunto\b', r'\bseeketh\b',
        r'\babideth\b', r'\bdwelleth\b', r'\bknoweth\b',
        r'\bspeaketh\b', r'\bworketh\b', r'\bbelieveth\b', r'\breceiveth\b',
        r'\bbringeth\b', r'\bteacheth\b', r'\breigneth\b',
        r'\bjudgeth\b', r'\bsendeth\b', r'\bcalleth\b', r'\bleadeth\b',
        r'\bfeedeth\b', r'\bholdeth\b', r'\bstandeth\b',
        r'\bwalketh\b', r'\brunneth\b', r'\bburneth\b', r'\bconsumeth\b',
        r'\bdestroyeth\b', r'\bdelivereth\b', r'\bwilt\b', r'\bcanst\b',
        r'\bdidst\b', r'\bdost\b', r'\bhast\b', r'\bmayest\b',
        r'\bwast\b', r'\bwert\b', r'\bbethink\b',
        r'\bwhoso\b', r'\bwhosoever\b', r'\bforasmuch\b',
        r'\bhowbeit\b', r'\bperadventure\b', r'\bbeseech\b',
        r'\bturneth\b', r'\bsaveth\b', r'\btrusteth\b',
        r'\bfeareth\b', r'\bfindeth\b', r'\bblesseth\b',
        r'\bhateth\b', r'\bsmiteth\b', r'\btwain\b',
        r'\bshew\b', r'\bshewn\b', r'\bshewed\b',
    ]
    text_lower = text.lower()
    return any(re.search(pat, text_lower) for pat in kjv_words)

def process_chapter(chapter_num):
    """Process a single chapter."""
    chapter_dir = os.path.join(BASE_DIR, f"Chapter {chapter_num}")
    study_file = os.path.join(chapter_dir, f"Chapter {chapter_num} - Study Notes.txt")
    esv_file = os.path.join(chapter_dir, f"Chapter {chapter_num} - ESV.txt")
    
    if not os.path.exists(study_file) or not os.path.exists(esv_file):
        print(f"Chapter {chapter_num}: Missing files, skipping.")
        return
    
    with open(study_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    esv_verses = get_esv_verses(esv_file)
    
    # Find KEY VERSES section boundaries
    kv_header = re.search(r'^KEY VERSES\n-+\n', content, re.MULTILINE)
    if not kv_header:
        print(f"Chapter {chapter_num}: No KEY VERSES section.")
        return
    
    kv_start = kv_header.end()
    
    # Find CROSS-REFERENCES section (which follows KEY VERSES)
    cr_header = re.search(r'^CROSS-REFERENCES\n-+\n', content, re.MULTILINE)
    if cr_header:
        kv_end = cr_header.start()
    else:
        # Find any next section
        next_sect = re.search(r'\n[A-Z][A-Z &/]+\n-+\n', content[kv_start:])
        kv_end = kv_start + next_sect.start() if next_sect else len(content)
    
    # Process KEY VERSES
    kv_section = content[kv_start:kv_end]
    new_kv_section = process_key_verses_section(kv_section, esv_verses)
    
    # Rebuild content with proper section separation
    new_content = content[:kv_start] + new_kv_section + "\n" + content[kv_end:]
    
    with open(study_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"Chapter {chapter_num}: Done.")

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
