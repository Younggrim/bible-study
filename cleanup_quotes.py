#!/usr/bin/env python3
"""
Cleanup script to fix minor formatting issues in ESV comparisons:
1. Double quotes: ""phrase" -> "phrase"
2. Trailing quotes inside: phrase,"" -> phrase"
3. Very short ESV matches (1-2 words) that are likely wrong
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


def cleanup_file(filepath):
    """Fix formatting issues in a file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Fix 1: Double opening quotes: ESV: ""phrase" -> ESV: "phrase"
    content = re.sub(r'ESV: ""([^"]+)"', r'ESV: "\1"', content)
    
    # Fix 2: Trailing double quotes: phrase,"" -> phrase"  
    content = re.sub(r'ESV: "([^"]+)""', r'ESV: "\1"', content)
    
    # Fix 3: ESV matches that are just 1 word and likely wrong
    # Pattern: / ESV: "X" where X is a single common word
    def check_short_match(match):
        phrase = match.group(1)
        words = phrase.split()
        # If it's just 1 word and it's a common word, remove the ESV note
        if len(words) == 1 and phrase.lower() in ('come', 'the', 'a', 'and', 'of', 'to', 'in', 'for', 'is', 'it', 'he', 'we', 'be'):
            return ''  # Remove this ESV note
        return match.group(0)
    
    content = re.sub(r' / ESV: "(\w+)"', check_short_match, content)
    
    # Fix 4: Clean up any resulting double spaces
    content = re.sub(r'  +', ' ', content)
    
    # Fix 5: Ensure proper spacing around em-dashes after ESV notes
    # Pattern: equivalent. — should stay as is
    # Pattern: "phrase" — should stay as is
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def main():
    total_fixed = 0
    
    for book_name, num_chapters in BOOKS:
        book_dir = os.path.join(BASE_PATH, book_name)
        
        if not os.path.exists(book_dir):
            continue
        
        for chapter in range(1, num_chapters + 1):
            chapter_dir = os.path.join(book_dir, f"Chapter {chapter}")
            notes_file = os.path.join(chapter_dir, f"Chapter {chapter} - Study Notes.txt")
            
            if not os.path.exists(notes_file):
                continue
            
            if cleanup_file(notes_file):
                total_fixed += 1
                print(f"  Fixed: {book_name} Chapter {chapter}")
    
    print(f"\nTotal files cleaned up: {total_fixed}")


if __name__ == '__main__':
    main()
