#!/usr/bin/env python3
"""
Merge TRANSLATION NOTES and ADDITIONAL TRANSLATION NOTES sections in John study notes.
Combines entries that reference the same verse into a single entry.
"""

import os
import re

BASE_DIR = "/Users/jeremymcadoo/Desktop/Kiro Projects/Bible Study/New Testament/04 - John"
NUM_CHAPTERS = 21


def parse_verse_entries(section_text):
    """Parse a translation notes section into a dict keyed by verse reference."""
    entries = {}
    # Split into entries by verse references (v.1, vv.15-17, etc.)
    parts = re.split(r'\n(?=v{1,2}\.?\s*[\d])', section_text)
    
    for part in parts:
        part = part.strip()
        if not part:
            continue
        # Extract verse reference
        match = re.match(r'(v{1,2}\.?\s*[\d\-,\s]+)', part)
        if match:
            ref = match.group(1).strip()
            # Normalize: "v.1" -> "v.1", "v.1  " -> "v.1"
            ref_normalized = re.sub(r'\s+', ' ', ref).strip()
            # Get the verse number(s) for grouping
            nums = re.findall(r'\d+', ref_normalized)
            key = nums[0] if nums else ref_normalized
            
            if key in entries:
                # Append the additional content to existing entry
                # Remove the verse reference prefix from the additional content
                additional = re.sub(r'^v{1,2}\.?\s*[\d\-,\s]+\s*—?\s*', '', part).strip()
                if additional:
                    entries[key]['text'] += '\n  ' + additional
            else:
                entries[key] = {'ref': ref_normalized, 'text': part}
        else:
            # Non-verse content (intro text, etc.) — keep as-is
            if '_intro' in entries:
                entries['_intro']['text'] += '\n' + part
            else:
                entries['_intro'] = {'ref': '', 'text': part}
    
    return entries


def merge_sections(main_section, additional_section):
    """Merge two translation notes sections, combining same-verse entries."""
    main_entries = parse_verse_entries(main_section)
    additional_entries = parse_verse_entries(additional_section)
    
    # Merge additional entries into main
    for key, entry in additional_entries.items():
        if key == '_intro':
            continue  # Skip intro text from additional section
        if key in main_entries:
            # Append additional notes to existing verse entry
            additional_text = entry['text']
            # Remove the "- v.X —" prefix if present at start
            additional_text = re.sub(r'^-\s*', '', additional_text)
            main_entries[key]['text'] += '\n  [ASV/NET/WEB]: ' + re.sub(r'^v{1,2}\.?\s*[\d\-,\s]+\s*—?\s*', '', additional_text).strip()
        else:
            # New verse not in main — add it
            main_entries[key] = entry
    
    # Sort by verse number and reconstruct
    result_parts = []
    
    # Add intro if present
    if '_intro' in main_entries:
        result_parts.append(main_entries['_intro']['text'])
        del main_entries['_intro']
    
    # Sort remaining by verse number
    sorted_keys = sorted(main_entries.keys(), key=lambda x: int(x) if x.isdigit() else 999)
    
    for key in sorted_keys:
        result_parts.append(main_entries[key]['text'])
    
    return '\n\n'.join(result_parts)


def process_chapter(filepath):
    """Process a single study notes file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if both sections exist
    main_match = re.search(
        r'(TRANSLATION NOTES\n-{4,}\n)(.*?)(?=\nADDITIONAL TRANSLATION NOTES|\nGLOSSARY|\nPERSONAL|\nREFLECTION|\nVIDEO|\n={3,})',
        content, re.DOTALL
    )
    additional_match = re.search(
        r'ADDITIONAL TRANSLATION NOTES[^\n]*\n-{4,}\n(.*?)(?=\nGLOSSARY|\nPERSONAL|\nREFLECTION|\nVIDEO|\n={3,})',
        content, re.DOTALL
    )
    
    if not main_match or not additional_match:
        return False  # Nothing to merge
    
    main_text = main_match.group(2).strip()
    additional_text = additional_match.group(1).strip()
    
    # Merge the sections
    merged = merge_sections(main_text, additional_text)
    
    # Replace in the original content:
    # 1. Replace main TRANSLATION NOTES content with merged content
    # 2. Remove the ADDITIONAL TRANSLATION NOTES section entirely
    
    # Find the start of TRANSLATION NOTES section content
    trans_header = 'TRANSLATION NOTES\n------------------------------------\n'
    trans_start = content.find(trans_header)
    if trans_start == -1:
        return False
    
    content_start = trans_start + len(trans_header)
    
    # Find where ADDITIONAL TRANSLATION NOTES begins
    add_match = re.search(r'\nADDITIONAL TRANSLATION NOTES[^\n]*\n-{4,}\n', content)
    if not add_match:
        return False
    
    add_section_start = add_match.start()
    
    # Find where ADDITIONAL section ends (next major section)
    remaining = content[add_match.end():]
    next_section = re.search(r'\n([A-Z][A-Z &()]+)\n-{4,}', remaining)
    if next_section:
        add_section_end = add_match.end() + next_section.start()
    else:
        # Look for ==== or end of file
        footer = re.search(r'\n={5,}', remaining)
        if footer:
            add_section_end = add_match.end() + footer.start()
        else:
            add_section_end = len(content)
    
    # Build new content
    new_content = (
        content[:content_start] +
        merged + '\n\n' +
        content[add_section_end:]
    )
    
    # Clean up any triple+ newlines
    new_content = re.sub(r'\n{4,}', '\n\n\n', new_content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    return True


def main():
    merged_count = 0
    for ch in range(1, NUM_CHAPTERS + 1):
        filepath = os.path.join(BASE_DIR, f"Chapter {ch}", f"Chapter {ch} - Study Notes.txt")
        if not os.path.exists(filepath):
            print(f"  Chapter {ch}: file not found")
            continue
        
        if process_chapter(filepath):
            merged_count += 1
            print(f"  Chapter {ch}: merged translation notes")
        else:
            print(f"  Chapter {ch}: no additional section to merge (or already merged)")
    
    print(f"\nDone. Merged {merged_count} chapters.")


if __name__ == '__main__':
    main()
