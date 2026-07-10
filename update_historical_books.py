#!/usr/bin/env python3
"""
Update study notes for all Historical Books (Joshua through Esther).
Makes 4 changes to each chapter's study notes file.
"""

import os
import re

BASE = "/Users/jeremymcadoo/Desktop/Kiro Projects/Bible Study/Old Testament"

# Book definitions: (folder_name, num_chapters, url_book_name, bible_project_slug, display_name)
BOOKS = [
    ("06 - Joshua", 24, "joshua", "joshua", "Joshua"),
    ("07 - Judges", 21, "judges", "judges", "Judges"),
    ("08 - Ruth", 4, "ruth", "ruth", "Ruth"),
    ("09 - 1 Samuel", 31, "1-samuel", "1-samuel", "1 Samuel"),
    ("10 - 2 Samuel", 24, "2-samuel", "2-samuel", "2 Samuel"),
    ("11 - 1 Kings", 22, "1-kings", "1-2-kings", "1 Kings"),
    ("12 - 2 Kings", 25, "2-kings", "1-2-kings", "2 Kings"),
    ("13 - 1 Chronicles", 29, "1-chronicles", "1-2-chronicles", "1 Chronicles"),
    ("14 - 2 Chronicles", 36, "2-chronicles", "1-2-chronicles", "2 Chronicles"),
    ("15 - Ezra", 10, "ezra", "ezra-nehemiah", "Ezra"),
    ("16 - Nehemiah", 13, "nehemiah", "ezra-nehemiah", "Nehemiah"),
    ("17 - Esther", 10, "esther", "esther", "Esther"),
]

def process_file(filepath, chapter_num, url_book, bp_slug, display_name):
    """Process a single study notes file with all 4 changes."""
    if not os.path.exists(filepath):
        print(f"  MISSING: {filepath}")
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # ===== CHANGE 1: Remove Moody and MacArthur lines =====
    # Remove "Moody Bible Commentary:" and its description line
    content = re.sub(r'\nMoody Bible Commentary:\n  See Moody Bible Commentary — [^\n]+\n', '\n', content)
    # Remove "MacArthur Bible Commentary:" and its description line
    content = re.sub(r'\nMacArthur Bible Commentary:\n  See The MacArthur Bible Commentary — [^\n]+\n', '\n', content)
    
    # Also handle any variant patterns
    content = re.sub(r'\nMoody Bible Commentary:[^\n]*\n(?:  [^\n]*\n)*', '\n', content)
    content = re.sub(r'\nMacArthur Bible Commentary:[^\n]*\n(?:  [^\n]*\n)*', '\n', content)

    # ===== CHANGE 2: Add Matthew Henry after Spurgeon entry =====
    # Find the end of the Spurgeon entry (look for the paragraph ending before next section)
    matthew_henry_entry = f'''Matthew Henry (Commentary on the Whole Bible):
  https://www.biblestudytools.com/commentaries/matthew-henry-complete/{url_book}/{chapter_num}.html'''

    # Check if Matthew Henry is already there
    if "Matthew Henry" not in content:
        # Find Spurgeon section - it ends with a blank line before the next section
        # Pattern: find the last line of Spurgeon's quote block, then insert after it
        # Spurgeon entries end with a quote followed by a blank line
        spurgeon_pattern = r'(Charles Spurgeon:\n(?:  [^\n]*\n|  [^\n]*\n\n)*(?:[^\n]+\n)*?)(\n(?:TRANSLATION NOTES|CROSS-REFERENCES|COMMENTARY REFERENCES|\n))'
        
        # Simpler approach: find "Charles Spurgeon:" block and insert after it
        # The Spurgeon block is a quote that ends before the next section
        # Let's find the pattern more reliably
        lines = content.split('\n')
        new_lines = []
        in_spurgeon = False
        spurgeon_done = False
        inserted = False
        
        for i, line in enumerate(lines):
            new_lines.append(line)
            
            if 'Charles Spurgeon:' in line:
                in_spurgeon = True
                continue
            
            if in_spurgeon and not inserted:
                # Look for end of Spurgeon block - it's followed by an empty line
                # then another section header or TRANSLATION NOTES
                if line.strip() == '' and i + 1 < len(lines):
                    next_line = lines[i + 1] if i + 1 < len(lines) else ''
                    # Check if next non-empty line starts a new section or is another commentary
                    if (next_line.startswith('TRANSLATION') or 
                        next_line.startswith('CROSS-REFERENCE') or
                        next_line.startswith('GLOSSARY') or
                        next_line.startswith('PERSONAL') or
                        next_line.strip() == ''):
                        # Insert Matthew Henry before this empty line? No, after.
                        new_lines.append(matthew_henry_entry)
                        new_lines.append('')
                        in_spurgeon = False
                        inserted = True
        
        if inserted:
            content = '\n'.join(new_lines)
        else:
            # Fallback: insert after any line containing just a closing quote from Spurgeon
            # Try a regex approach
            # Find end of Spurgeon section (text ending in quote mark followed by blank line before next section)
            pattern = r'(Charles Spurgeon:\n(?:.*\n)*?)(  .*["\u201d].*\n)(\n)'
            match = re.search(pattern, content)
            if match:
                insert_point = match.end(2)
                content = content[:insert_point] + '\n' + matthew_henry_entry + '\n' + content[insert_point:]

    # ===== CHANGE 3: Add VIDEO RESOURCES and PODCAST RESOURCES before footer =====
    video_podcast_section = f'''VIDEO RESOURCES
------------------------------------
The Bible Project \u2014 {display_name} Overview:
  https://bibleproject.com/explore/video/{bp_slug}/

PODCAST RESOURCES
------------------------------------
David Guzik \u2014 Enduring Word Podcast:
  Apple Podcasts: https://podcasts.apple.com/nz/podcast/enduring-word/id1717516011

BibleProject Podcast:
  https://bibleproject.com/podcast/'''

    if "VIDEO RESOURCES" not in content:
        # Insert after PERSONAL NOTES section, before the footer
        # Footer starts with "========"
        # Find the footer line
        footer_pattern = r'(\n\n========================================\nStudy Notes generated)'
        if re.search(footer_pattern, content):
            content = re.sub(footer_pattern, f'\n\n{video_podcast_section}\n\n\\1', content, count=1)
        else:
            # Try alternate footer pattern
            footer_pattern2 = r'(\n========================================\nStudy Notes generated)'
            if re.search(footer_pattern2, content):
                content = re.sub(footer_pattern2, f'\n\n{video_podcast_section}\n\\1', content, count=1)

    # ===== CHANGE 4: Update footer =====
    # Replace Moody/MacArthur with Matthew Henry
    old_footer = 'Commentary sources: Enduring Word (enduringword.com), Charles Spurgeon (Public Domain),\nMoody Bible Commentary, The MacArthur Bible Commentary'
    new_footer = 'Commentary sources: Enduring Word (enduringword.com), Charles Spurgeon (Public Domain),\nMatthew Henry (Public Domain)'
    content = content.replace(old_footer, new_footer)
    
    # Also try single-line variant
    old_footer2 = 'Moody Bible Commentary, The MacArthur Bible Commentary'
    if old_footer2 in content:
        content = content.replace(old_footer2, 'Matthew Henry (Public Domain)')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return True


def main():
    total = 0
    success = 0
    missing = 0

    for folder_name, num_chapters, url_book, bp_slug, display_name in BOOKS:
        print(f"\nProcessing {display_name} ({num_chapters} chapters)...")
        for ch in range(1, num_chapters + 1):
            filepath = os.path.join(BASE, folder_name, f"Chapter {ch}", f"Chapter {ch} - Study Notes.txt")
            total += 1
            result = process_file(filepath, ch, url_book, bp_slug, display_name)
            if result:
                success += 1
            else:
                missing += 1

    print(f"\n{'='*50}")
    print(f"COMPLETE: {success}/{total} files processed successfully")
    if missing > 0:
        print(f"MISSING: {missing} files not found")


if __name__ == "__main__":
    main()
