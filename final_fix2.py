#!/usr/bin/env python3
"""
Final fix for smart quote issues in ESV renderings.
The ESV text sometimes contains smart/curly quotes (U+201C, U+201D) from the source,
which creates issues when wrapped in straight quotes.
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
    """Fix smart quote issues in ESV annotations."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Pattern: / ESV: "[\u201c]text[\u201d]" or / ESV: "text[\u201d]"
    # The smart quotes from ESV source text are embedded inside our straight-quote delimiters
    
    # Fix: straight quote followed by smart opening quote: "\u201c -> "
    # i.e., remove the smart quote that's inside our delimiter
    content = content.replace('/ ESV: "\u201c', '/ ESV: "')
    content = content.replace('/ ESV: "\u201d', '/ ESV: "')
    
    # Fix: smart closing quote followed by straight quote at end: \u201d" -> "
    # Find pattern within ESV annotations
    # Replace any smart quotes inside ESV: "..." with nothing or appropriate char
    def fix_esv_annotation(match):
        prefix = match.group(1)  # / ESV: "
        inner = match.group(2)   # content between quotes
        suffix = match.group(3)  # "
        
        # Remove smart quotes from inner content
        inner = inner.replace('\u201c', '')
        inner = inner.replace('\u201d', '')
        # Also remove trailing commas that came from verse punctuation
        inner = inner.rstrip(',')
        
        return prefix + inner + suffix
    
    # Match / ESV: "content" where content may have smart quotes
    content = re.sub(r'(/ ESV: ")([^"]*?)(")', fix_esv_annotation, content)
    
    # Also handle case where smart closing quote acts as the delimiter
    # Pattern: / ESV: "text\u201d — (smart quote used instead of straight closing quote)
    content = re.sub(r'(/ ESV: "[^"]*)\u201d(\s*[—\-])', r'\1"\2', content)
    
    # Handle: / ESV: "text\u201d\s  (at end of annotation before next content)
    content = re.sub(r'(/ ESV: "[^"]*)\u201d', r'\1"', content)
    
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
