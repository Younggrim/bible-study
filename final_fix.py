#!/usr/bin/env python3
"""
Final fix for embedded quotes in ESV renderings.
Handles cases where ESV text contains quotation marks (dialogue in verses).
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


def fix_file(filepath):
    """Fix embedded quote issues in ESV annotations."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Fix pattern: / ESV: ""text" -> / ESV: "text"
    # The "" at start means the ESV verse had a quote at the beginning
    content = content.replace('/ ESV: ""', '/ ESV: "')
    
    # Fix pattern: text,"" -> text"
    # The ,"" at end means the ESV verse had a comma+quote at the end of the phrase
    # We need to handle: / ESV: "some text,"" -> / ESV: "some text"
    content = re.sub(r'(/ ESV: "[^"]*[^"]),""', r'\1"', content)
    
    # Also handle: / ESV: "text"" (double quote at end without comma)
    content = re.sub(r'(/ ESV: "[^"]+)""', r'\1"', content)
    
    # Handle case where the captured ESV text ends with punctuation before the closing quote
    # e.g., / ESV: "text," -> / ESV: "text"
    # Only fix if there's clearly a trailing comma that shouldn't be there
    content = re.sub(r'(/ ESV: "[^"]+),"(\s*—)', r'\1"\2', content)
    
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
            
            if fix_file(notes_file):
                total_fixed += 1
                print(f"  Fixed: {book_name} Chapter {chapter}")
    
    if total_fixed == 0:
        print("No files needed fixing.")
    else:
        print(f"\nTotal files fixed: {total_fixed}")


if __name__ == '__main__':
    main()
