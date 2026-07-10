#!/usr/bin/env python3
"""
Cleanup script for remaining KJV archaic words in KEY VERSES and CROSS-REFERENCES.
"""
import os
import re

def get_additional_replacements():
    """Additional archaic word replacements missed by first pass."""
    return [
        # Archaic verbs
        (r'\bshew\b', 'show'),
        (r'\bShew\b', 'Show'),
        (r'\bshewed\b', 'showed'),
        (r'\bsheweth\b', 'shows'),
        (r'\benquire\b', 'inquire'),
        (r'\benquired\b', 'inquired'),
        (r'\brequite\b', 'repay'),
        (r'\bknoweth\b', 'knows'),
        (r'\bknowst\b', 'know'),
        (r'\bknowest\b', 'know'),
        # "knowest you" -> "Do you know" (can't easily regex this context)
        (r'\bsaith\b', 'says'),
        (r'\bcometh\b', 'comes'),
        (r'\bwouldest\b', 'would'),
        (r'\bshouldest\b', 'should'),
        (r'\bcouldest\b', 'could'),
        (r'\bmightest\b', 'might'),
        # More -eth forms
        (r'\babideth\b', 'abides'),
        (r'\bariseth\b', 'arises'),
        (r'\bbelongeth\b', 'belongs'),
        (r'\bblesseth\b', 'blesses'),
        (r'\bbringeth\b', 'brings'),
        (r'\bburneth\b', 'burns'),
        (r'\bcleaveth\b', 'cleaves'),
        (r'\bcomforteth\b', 'comforts'),
        (r'\bcrieth\b', 'cries'),
        (r'\bdelivereth\b', 'delivers'),
        (r'\bdeparteth\b', 'departs'),
        (r'\bdesireth\b', 'desires'),
        (r'\bdestroyeth\b', 'destroys'),
        (r'\bdevoureth\b', 'devours'),
        (r'\bendureth\b', 'endures'),
        (r'\bexecuteth\b', 'executes'),
        (r'\bfeareth\b', 'fears'),
        (r'\bfeedeth\b', 'feeds'),
        (r'\bfighteth\b', 'fights'),
        (r'\bforgetteth\b', 'forgets'),
        (r'\bforgiveth\b', 'forgives'),
        (r'\bhateth\b', 'hates'),
        (r'\bhealeth\b', 'heals'),
        (r'\bjudgeth\b', 'judges'),
        (r'\bknocketh\b', 'knocks'),
        (r'\bloveth\b', 'loves'),
        (r'\bopenth\b', 'opens'),
        (r'\bopeneth\b', 'opens'),
        (r'\bpleaseth\b', 'pleases'),
        (r'\bpursueth\b', 'pursues'),
        (r'\brejoiceth\b', 'rejoices'),
        (r'\brevealeth\b', 'reveals'),
        (r'\bsaveth\b', 'saves'),
        (r'\bscattereth\b', 'scatters'),
        (r'\bseeketh\b', 'seeks'),
        (r'\bserveth\b', 'serves'),
        (r'\bslayeth\b', 'slays'),
        (r'\bsmiteth\b', 'strikes'),
        (r'\bstriketh\b', 'strikes'),
        (r'\btestifieth\b', 'testifies'),
        (r'\btrusteth\b', 'trusts'),
        (r'\bwatcheth\b', 'watches'),
        # Additional archaic
        (r'\bwhence\b', 'from where'),
        (r'\bbeholdeth\b', 'beholds'),
        (r'\bnought\b', 'nothing'),
        (r'\bsore\b(?= (?:afraid|distressed|displeased|grieved|troubled))', 'very'),
        # Verb forms with "you" (from first pass pronoun conversion)
        (r'\bknowest you\b', 'do you know'),
        (r'"You knowest\b', '"Do you know'),
        (r'\bYou knowest\b', 'Do you know'),
    ]


def find_section(content, section_name, all_headers):
    """Find a section's content boundaries."""
    pattern = f'^{re.escape(section_name)}\\n-+\\n'
    match = re.search(pattern, content, re.MULTILINE)
    if not match:
        return None, None
    
    start = match.end()
    end = len(content)
    
    for header in all_headers:
        if header == section_name:
            continue
        next_match = content.find(header + '\n', start)
        if next_match != -1 and next_match < end:
            # Go back to find the separator line
            line_start = content.rfind('\n', 0, next_match)
            end = line_start if line_start != -1 else next_match
    
    return start, end


def replace_in_quotes(text, pattern, replacement):
    """Replace pattern only within double-quoted strings."""
    result = []
    i = 0
    in_quote = False
    current = ""
    
    while i < len(text):
        char = text[i]
        if char == '\u201c' or (char == '"' and not in_quote):  # Opening quote
            result.append(current)
            current = char
            in_quote = True
        elif (char == '\u201d' or (char == '"' and in_quote)):  # Closing quote
            current += char
            current = re.sub(pattern, replacement, current)
            result.append(current)
            current = ""
            in_quote = False
        else:
            current += char
        i += 1
    
    result.append(current)
    return ''.join(result)


def process_file(filepath):
    """Process a single file for remaining KJV forms."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    section_headers = [
        'CHAPTER SUMMARY', 'AUTHORSHIP & HISTORICAL BACKGROUND',
        'MAP & GEOGRAPHY NOTES', 'KEY VERSES',
        'CROSS-REFERENCES', 'COMMENTARY REFERENCES',
        'TRANSLATION NOTES', 'GLOSSARY',
        'PERSONAL REFLECTION & APPLICATION', 'VIDEO RESOURCES',
        'PODCAST RESOURCES', 'PERSONAL NOTES'
    ]
    
    # Find KEY VERSES section
    kv_start, kv_end = find_section(content, 'KEY VERSES', section_headers)
    cr_start, cr_end = find_section(content, 'CROSS-REFERENCES', section_headers)
    
    if kv_start is None:
        return False
    
    replacements = get_additional_replacements()
    modified = False
    new_content = content
    
    # Process KEY VERSES
    if kv_start is not None and kv_end is not None:
        kv_text = new_content[kv_start:kv_end]
        new_kv = kv_text
        for pattern, replacement in replacements:
            new_kv = replace_in_quotes(new_kv, pattern, replacement)
        if new_kv != kv_text:
            new_content = new_content[:kv_start] + new_kv + new_content[kv_end:]
            offset = len(new_kv) - len(kv_text)
            if cr_start is not None and cr_start > kv_start:
                cr_start += offset
                cr_end += offset
            modified = True
    
    # Process CROSS-REFERENCES
    if cr_start is not None and cr_end is not None:
        cr_text = new_content[cr_start:cr_end]
        new_cr = cr_text
        for pattern, replacement in replacements:
            new_cr = replace_in_quotes(new_cr, pattern, replacement)
        if new_cr != cr_text:
            new_content = new_content[:cr_start] + new_cr + new_content[cr_end:]
            modified = True
    
    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
    
    return modified


def main():
    base_path = "/Users/jeremymcadoo/Desktop/Kiro Projects/Bible Study/Old Testament"
    
    books = [
        ("10 - 2 Samuel", 24),
        ("11 - 1 Kings", 22),
        ("12 - 2 Kings", 25),
    ]
    
    total_modified = 0
    
    for book_dir, num_chapters in books:
        book_path = os.path.join(base_path, book_dir)
        print(f"\nProcessing {book_dir}...")
        
        for ch in range(1, num_chapters + 1):
            chapter_dir = f"Chapter {ch}"
            filename = f"Chapter {ch} - Study Notes.txt"
            filepath = os.path.join(book_path, chapter_dir, filename)
            
            if os.path.exists(filepath):
                try:
                    result = process_file(filepath)
                    if result:
                        print(f"  Cleaned: Chapter {ch}")
                        total_modified += 1
                except Exception as e:
                    print(f"  ERROR Chapter {ch}: {e}")
            else:
                print(f"  Not found: {filepath}")
    
    print(f"\nTotal files cleaned: {total_modified}")


if __name__ == "__main__":
    main()
