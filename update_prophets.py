#!/usr/bin/env python3
"""
Update study notes for the five Major Prophets books.
Processes all 183 chapters across Isaiah (66), Jeremiah (52), 
Lamentations (5), Ezekiel (48), and Daniel (12).
"""

import os
import re

BASE_PATH = "/Users/jeremymcadoo/Desktop/Kiro Projects/Bible Study/Old Testament"

BOOKS = [
    {"name": "Isaiah", "folder": "23 - Isaiah", "chapters": 66,
     "video_url": "https://bibleproject.com/explore/video/isaiah/"},
    {"name": "Jeremiah", "folder": "24 - Jeremiah", "chapters": 52,
     "video_url": "https://bibleproject.com/explore/video/jeremiah/"},
    {"name": "Lamentations", "folder": "25 - Lamentations", "chapters": 5,
     "video_url": "https://bibleproject.com/explore/video/lamentations/"},
    {"name": "Ezekiel", "folder": "26 - Ezekiel", "chapters": 48,
     "video_url": "https://bibleproject.com/explore/video/ezekiel/"},
    {"name": "Daniel", "folder": "27 - Daniel", "chapters": 12,
     "video_url": "https://bibleproject.com/explore/video/daniel/"},
]

CALVIN_URL = "https://www.ccel.org/ccel/calvin/"

PODCAST_SECTION = """PODCAST RESOURCES
------------------------------------
David Guzik — Enduring Word Podcast:
  Apple Podcasts: https://podcasts.apple.com/nz/podcast/enduring-word/id1717516011

BibleProject Podcast:
  https://bibleproject.com/podcast/"""

NEW_FOOTER = """========================================
Study Notes generated for personal Bible study use.
Translations referenced: KJV, ESV
Commentary sources: Enduring Word (enduringword.com), Charles
Spurgeon (Public Domain), Matthew Henry (Public Domain), John Calvin (Public Domain)"""


def get_video_section(book_name, video_url):
    return f"""VIDEO RESOURCES
------------------------------------
The Bible Project — {book_name} Overview (Video):
  {video_url}
  Animated overview of the book of {book_name} showing the literary
  structure, key themes, and how this book fits into the larger
  biblical narrative. Excellent visual introduction."""


def get_calvin_entry(book_name, chapter_num):
    return f"""John Calvin (Commentary on {book_name}):
  {CALVIN_URL}
  Calvin's verse-by-verse exposition of {book_name} {chapter_num},
  emphasizing God's sovereignty, the doctrines of grace, and
  practical application for the believer."""


def process_file(filepath, book_name, chapter_num, video_url):
    """Process a single study notes file."""
    if not os.path.exists(filepath):
        print(f"  SKIP (not found): {filepath}")
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # --- Step 1: Remove Moody and MacArthur entries ---
    # Remove from COMMENTARY REFERENCES section
    # Remove lines mentioning Moody Bible Commentary
    content = re.sub(
        r'(?m)^.*Moody Bible Commentary.*\n?', '', content
    )
    # Remove lines mentioning MacArthur Bible Commentary
    content = re.sub(
        r'(?m)^.*MacArthur Bible Commentary.*\n?', '', content
    )
    # Also remove "The MacArthur Bible Commentary" variant
    content = re.sub(
        r'(?m)^.*The MacArthur Bible Commentary.*\n?', '', content
    )

    # --- Step 2: Add John Calvin reference if not present ---
    if "John Calvin" not in content and "john calvin" not in content.lower():
        calvin_entry = get_calvin_entry(book_name, chapter_num)
        # Try to add after Matthew Henry section
        if "Matthew Henry" in content:
            # Find end of Matthew Henry section (before next section or double newline)
            henry_pattern = r'(Matthew Henry.*?(?=\n\n[A-Z]|\n\n\n|\nJohn Calvin|\n========))'
            match = re.search(henry_pattern, content, re.DOTALL)
            if match:
                insert_pos = match.end()
                content = content[:insert_pos] + "\n\n" + calvin_entry + "\n" + content[insert_pos:]
            else:
                # Just add before TRANSLATION NOTES or PERSONAL REFLECTION
                for marker in ["TRANSLATION NOTES", "PERSONAL REFLECTION"]:
                    if marker in content:
                        idx = content.index(marker)
                        content = content[:idx] + calvin_entry + "\n\n\n" + content[idx:]
                        break
        elif "COMMENTARY REFERENCES" in content:
            # Add at end of commentary section
            idx = content.index("COMMENTARY REFERENCES")
            # Find the next section after COMMENTARY REFERENCES
            next_section = re.search(r'\n\n[A-Z][A-Z ]+\n----', content[idx+25:])
            if next_section:
                insert_pos = idx + 25 + next_section.start()
                content = content[:insert_pos] + "\n" + calvin_entry + "\n" + content[insert_pos:]
        else:
            # Add before PERSONAL REFLECTION or TRANSLATION NOTES
            for marker in ["PERSONAL REFLECTION", "TRANSLATION NOTES"]:
                if marker in content:
                    idx = content.index(marker)
                    content = content[:idx] + "COMMENTARY REFERENCES\n------------------------------------\n" + calvin_entry + "\n\n\n" + content[idx:]
                    break

    # --- Step 3: Add VIDEO and PODCAST RESOURCES if not present ---
    video_section = get_video_section(book_name, video_url)

    # --- Step 4: Ensure section order ---
    # Target order: Personal Reflection & Application → Video Resources → Podcast Resources → Personal Notes → Footer
    
    # Extract sections
    has_video = "VIDEO RESOURCES" in content
    has_podcast = "PODCAST RESOURCES" in content
    
    # Find PERSONAL REFLECTION section
    refl_match = re.search(r'(PERSONAL REFLECTION & APPLICATION\n------------------------------------\n.*?)(?=\nVIDEO RESOURCES|\nPODCAST RESOURCES|\nPERSONAL NOTES|\n=====)', content, re.DOTALL)
    
    # Find PERSONAL NOTES section
    notes_match = re.search(r'(PERSONAL NOTES\n------------------------------------\n.*?)(?=\nVIDEO RESOURCES|\nPODCAST RESOURCES|\n=====)', content, re.DOTALL)
    
    # Find footer
    footer_match = re.search(r'(={5,}.*$)', content, re.DOTALL)
    
    # Strategy: Remove Video, Podcast, Personal Notes, and Footer sections, 
    # then re-add them in correct order at the end
    
    # Remove existing VIDEO RESOURCES section if present
    content = re.sub(
        r'\n*VIDEO RESOURCES\n------------------------------------\n.*?(?=\nPODCAST RESOURCES|\nPERSONAL NOTES|\n=====|\Z)',
        '', content, flags=re.DOTALL
    )
    
    # Remove existing PODCAST RESOURCES section if present
    content = re.sub(
        r'\n*PODCAST RESOURCES\n------------------------------------\n.*?(?=\nPERSONAL NOTES|\nVIDEO RESOURCES|\n=====|\Z)',
        '', content, flags=re.DOTALL
    )
    
    # Remove existing PERSONAL NOTES section
    personal_notes_content = "[Your notes here]"
    pn_match = re.search(
        r'\n*PERSONAL NOTES\n------------------------------------\n(.*?)(?=\n=====|\Z)',
        content, flags=re.DOTALL
    )
    if pn_match:
        personal_notes_content = pn_match.group(1).strip()
        content = re.sub(
            r'\n*PERSONAL NOTES\n------------------------------------\n.*?(?=\n=====|\Z)',
            '', content, flags=re.DOTALL
        )
    
    # Remove existing footer
    content = re.sub(r'\n*={5,}\n.*$', '', content, flags=re.DOTALL)
    
    # Clean trailing whitespace
    content = content.rstrip()
    
    # Now rebuild the end of the file in correct order:
    # Personal Reflection should already be in content
    # Add: Video Resources → Podcast Resources → Personal Notes → Footer
    
    content += "\n\n"
    content += video_section + "\n\n"
    content += PODCAST_SECTION + "\n\n"
    content += f"PERSONAL NOTES\n------------------------------------\n{personal_notes_content}\n\n\n"
    content += NEW_FOOTER + "\n"

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return True


def main():
    total_processed = 0
    total_skipped = 0
    
    for book in BOOKS:
        book_name = book["name"]
        book_folder = book["folder"]
        num_chapters = book["chapters"]
        video_url = book["video_url"]
        
        print(f"\nProcessing {book_name} ({num_chapters} chapters)...")
        
        for ch in range(1, num_chapters + 1):
            chapter_folder = f"Chapter {ch}"
            filename = f"Chapter {ch} - Study Notes.txt"
            filepath = os.path.join(BASE_PATH, book_folder, chapter_folder, filename)
            
            success = process_file(filepath, book_name, ch, video_url)
            if success:
                total_processed += 1
            else:
                total_skipped += 1
    
    print(f"\n{'='*50}")
    print(f"COMPLETE: {total_processed} files processed, {total_skipped} skipped")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
