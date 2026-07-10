#!/usr/bin/env python3
"""
Final cleanup pass to fix remaining double-quote issues.
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
    """Fix remaining double-quote issues."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Fix double opening quotes after ESV: - pattern: ESV: ""text"
    # This happens when the ESV text itself starts with a quote mark
    content = re.sub(r'(/ ESV: )""([^"]+)"', r'\1"\2"', content)
    
    # Fix double closing quotes - pattern: text,""
    content = re.sub(r'(/ ESV: "[^"]+),""', r'\1"', content)
    
    # More general: any "" within ESV notes
    # Pattern: / ESV: "...""  (double quote at end)
    content = re.sub(r'(/ ESV: "[^"]*[^"])"" ', r'\1" ', content)
    content = re.sub(r'(/ ESV: "[^"]*[^"])""(\s*—)', r'\1"\2', content)
    
    # Pattern: / ESV: ""...(double quote at start)
    content = re.sub(r'(/ ESV: )""', r'\1"', content)
    
    # Fix any remaining double quotes that shouldn't be there
    # But be careful not to break intentional quotes in the text
    # Only fix within the ESV annotation context
    def fix_esv_quotes(match):
        text = match.group(0)
        # Remove any double quotes
        text = text.replace('""', '"')
        return text
    
    content = re.sub(r'/ ESV: "[^"]*"', fix_esv_quotes, content)
    
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
    
    if total_fixed == 0:
        print("No files needed fixing.")
    else:
        print(f"\nTotal files cleaned up: {total_fixed}")


if __name__ == '__main__':
    main()
