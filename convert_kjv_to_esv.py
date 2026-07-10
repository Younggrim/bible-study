#!/usr/bin/env python3
"""
Script to convert KJV quotes to ESV in KEY VERSES and CROSS-REFERENCES sections
of Bible study notes files.
"""
import os
import re
import glob

def get_esv_replacements():
    """Common KJV to ESV word/phrase replacements."""
    return [
        # Pronouns - must come before verb forms to avoid issues
        (r'\bthee\b', 'you'),
        (r'\bThee\b', 'You'),
        (r'\bthou\b', 'you'),
        (r'\bThou\b', 'You'),
        (r'\bthy\b', 'your'),
        (r'\bThy\b', 'Your'),
        (r'\bthine\b', 'your'),
        (r'\bThine\b', 'Your'),
        (r'\bye\b', 'you'),
        (r'\bYe\b', 'You'),
        # Verb forms
        (r'\bhath\b', 'has'),
        (r'\bHath\b', 'Has'),
        (r'\bdoth\b', 'does'),
        (r'\bDoth\b', 'Does'),
        (r'\bdost\b', 'do'),
        (r'\bshalt\b', 'shall'),
        (r'\bShalt\b', 'Shall'),
        (r'\bwilt\b', 'will'),
        (r'\bWilt\b', 'Will'),
        (r'\bart\b', 'are'),
        (r'\bArt\b', 'Are'),
        (r'\bhast\b', 'have'),
        (r'\bHast\b', 'Have'),
        (r'\bcanst\b', 'can'),
        # Common -eth/-th endings
        (r'\bcometh\b', 'comes'),
        (r'\bgiveth\b', 'gives'),
        (r'\bliveth\b', 'lives'),
        (r'\bsaith\b', 'says'),
        (r'\bknoweth\b', 'knows'),
        (r'\bmaketh\b', 'makes'),
        (r'\btaketh\b', 'takes'),
        (r'\bgoeth\b', 'goes'),
        (r'\bdoeth\b', 'does'),
        (r'\bseeth\b', 'sees'),
        (r'\bheareth\b', 'hears'),
        (r'\banswereth\b', 'answers'),
        (r'\bkilleth\b', 'kills'),
        (r'\bsetteth\b', 'sets'),
        (r'\bstandeth\b', 'stands'),
        (r'\bsitteth\b', 'sits'),
        (r'\breigneth\b', 'reigns'),
        (r'\bspeaketh\b', 'speaks'),
        (r'\bteacheth\b', 'teaches'),
        (r'\bleadeth\b', 'leads'),
        (r'\bfalleth\b', 'falls'),
        (r'\brunneth\b', 'runs'),
        (r'\bpasseth\b', 'passes'),
        (r'\bturneth\b', 'turns'),
        (r'\bkeepeth\b', 'keeps'),
        (r'\bhelpeth\b', 'helps'),
        (r'\bfindeth\b', 'finds'),
        (r'\blooketh\b', 'looks'),
        (r'\bworketh\b', 'works'),
        (r'\bwalketh\b', 'walks'),
        (r'\bcalleth\b', 'calls'),
        (r'\bdwelleth\b', 'dwells'),
        (r'\bremaineth\b', 'remains'),
        (r'\bperformeth\b', 'performs'),
        (r'\bexalteth\b', 'exalts'),
        # Common archaic words
        (r'\bunto\b', 'to'),
        (r'\bUnto\b', 'To'),
        (r'\bwherefore\b', 'why'),
        (r'\bWherefore\b', 'Why'),
        (r'\bhitherto\b', 'thus far'),
        (r'\bthereof\b', 'of it'),
        (r'\bwhereof\b', 'of which'),
        (r'\btherein\b', 'in it'),
        (r'\bwhither\b', 'where'),
        (r'\bWhither\b', 'Where'),
        (r'\bhither\b', 'here'),
        (r'\bthence\b', 'from there'),
        # Common phrases
        (r'\bit came to pass\b', 'it happened'),
        (r'\bIt came to pass\b', 'It happened'),
    ]


def process_file(filepath):
    """Process a single study notes file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find KEY VERSES section
    key_verses_match = re.search(r'^KEY VERSES\n-+\n', content, re.MULTILINE)
    cross_ref_match = re.search(r'^CROSS-REFERENCES\n-+\n', content, re.MULTILINE)
    
    if not key_verses_match:
        return False
    
    # Find section boundaries
    sections = []
    section_headers = [
        'CHAPTER SUMMARY', 'AUTHORSHIP', 'MAP & GEOGRAPHY', 'KEY VERSES',
        'CROSS-REFERENCES', 'COMMENTARY', 'TRANSLATION NOTES', 'GLOSSARY',
        'PERSONAL REFLECTION', 'VIDEO RESOURCES', 'PODCAST RESOURCES',
        'PERSONAL NOTES'
    ]
    
    # Get the KEY VERSES section text  
    kv_start = key_verses_match.end()
    # Find next section after KEY VERSES
    kv_end = len(content)
    for header in section_headers:
        if header == 'KEY VERSES':
            continue
        next_match = content.find(header + '\n', kv_start)
        if next_match != -1 and next_match < kv_end:
            # Go back to find the start of the dashes line above
            line_start = content.rfind('\n', 0, next_match)
            kv_end = line_start if line_start != -1 else next_match
    
    key_verses_text = content[kv_start:kv_end]
    
    # Get CROSS-REFERENCES section text
    cr_text = ""
    cr_start = 0
    cr_end = 0
    if cross_ref_match:
        cr_start = cross_ref_match.end()
        cr_end = len(content)
        for header in section_headers:
            if header == 'CROSS-REFERENCES':
                continue
            next_match = content.find(header + '\n', cr_start)
            if next_match != -1 and next_match < cr_end:
                line_start = content.rfind('\n', 0, next_match)
                cr_end = line_start if line_start != -1 else next_match
        cr_text = content[cr_start:cr_end]
    
    # Apply replacements to KEY VERSES section
    new_kv = key_verses_text
    replacements = get_esv_replacements()
    
    # Replace (KJV) with (ESV) in KEY VERSES
    new_kv = new_kv.replace('(KJV)', '(ESV)')
    
    # Apply word-level replacements within quoted text
    # Find all quoted text and replace within quotes
    def replace_in_quotes(text, pattern, replacement):
        """Replace pattern only within quoted strings."""
        result = []
        in_quote = False
        quote_char = None
        i = 0
        current_segment = ""
        
        while i < len(text):
            char = text[i]
            if char == '"' and not in_quote:
                # Process non-quoted segment as-is
                result.append(current_segment)
                current_segment = char
                in_quote = True
                quote_char = char
            elif char == '"' and in_quote:
                current_segment += char
                # Apply replacement to the quoted segment
                current_segment = re.sub(pattern, replacement, current_segment)
                result.append(current_segment)
                current_segment = ""
                in_quote = False
            else:
                current_segment += char
            i += 1
        
        result.append(current_segment)
        return ''.join(result)
    
    for pattern, replacement in replacements:
        new_kv = replace_in_quotes(new_kv, pattern, replacement)
    
    # Apply replacements to CROSS-REFERENCES section (only within quotes)
    new_cr = cr_text
    if cr_text:
        for pattern, replacement in replacements:
            new_cr = replace_in_quotes(new_cr, pattern, replacement)
    
    # Reconstruct the file
    modified = False
    new_content = content
    
    if new_kv != key_verses_text:
        new_content = new_content[:kv_start] + new_kv + new_content[kv_end:]
        modified = True
        # Recalculate cr positions if needed
        offset = len(new_kv) - len(key_verses_text)
        if cr_text and cr_start > kv_start:
            cr_start += offset
            cr_end += offset
    
    if new_cr != cr_text and cr_text:
        new_content = new_content[:cr_start] + new_cr + new_content[cr_end:]
        modified = True
    
    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False


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
                        print(f"  Modified: Chapter {ch}")
                        total_modified += 1
                    else:
                        print(f"  No changes: Chapter {ch}")
                except Exception as e:
                    print(f"  ERROR Chapter {ch}: {e}")
            else:
                print(f"  Not found: {filepath}")
    
    print(f"\nTotal files modified: {total_modified}")


if __name__ == "__main__":
    main()
