#!/usr/bin/env python3
"""Fix 2 Samuel chapters 21-24 that are missing VIDEO RESOURCES."""

import os
import re

BASE = "/Users/jeremymcadoo/Desktop/Kiro Projects/Bible Study/Old Testament/10 - 2 Samuel"
bp_slug = "2-samuel"
display_name = "2 Samuel"

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

for ch in [21, 22, 23, 24]:
    filepath = os.path.join(BASE, f"Chapter {ch}", f"Chapter {ch} - Study Notes.txt")
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if "VIDEO RESOURCES" in content:
        print(f"  Chapter {ch}: Already has VIDEO RESOURCES, skipping")
        continue
    
    # Find the footer separator line (=== line before "Study Notes generated")
    # Use a flexible pattern for the === line
    pattern = r'(\n\n={38,42}\nStudy Notes generated)'
    match = re.search(pattern, content)
    if match:
        content = content[:match.start()] + '\n\n' + video_podcast_section + '\n' + match.group() + content[match.end():]
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  Fixed: Chapter {ch}")
    else:
        # Try single newline pattern
        pattern2 = r'(\n={38,42}\nStudy Notes generated)'
        match = re.search(pattern2, content)
        if match:
            content = content[:match.start()] + '\n\n' + video_podcast_section + '\n' + match.group() + content[match.end():]
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"  Fixed: Chapter {ch}")
        else:
            print(f"  Could not fix: Chapter {ch}")
            # Print last 5 lines for debugging
            lines = content.split('\n')
            for l in lines[-8:]:
                print(f"    |{l}|")
