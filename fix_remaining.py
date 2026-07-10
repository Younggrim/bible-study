#!/usr/bin/env python3
"""Fix remaining footer issues in 2 Samuel chapters 17-24."""

import os

BASE = "/Users/jeremymcadoo/Desktop/Kiro Projects/Bible Study/Old Testament/10 - 2 Samuel"

for ch in range(17, 25):
    filepath = os.path.join(BASE, f"Chapter {ch}", f"Chapter {ch} - Study Notes.txt")
    if not os.path.exists(filepath):
        print(f"MISSING: {filepath}")
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Handle the multi-line wrapped footer variant
    # Pattern: "Commentary sources: Enduring Word (enduringword.com), Charles\nSpurgeon (Public Domain), Moody Bible Commentary, The MacArthur\nBible Commentary"
    old_patterns = [
        "Commentary sources: Enduring Word (enduringword.com), Charles\nSpurgeon (Public Domain), Moody Bible Commentary, The MacArthur\nBible Commentary",
        "Commentary sources: Enduring Word (enduringword.com), Charles Spurgeon (Public Domain), Moody Bible Commentary, The MacArthur\nBible Commentary",
        "Commentary sources: Enduring Word (enduringword.com), Charles\nSpurgeon (Public Domain), Moody Bible Commentary, The MacArthur Bible Commentary",
    ]
    
    new_footer = "Commentary sources: Enduring Word (enduringword.com), Charles Spurgeon (Public Domain),\nMatthew Henry (Public Domain)"
    
    replaced = False
    for old in old_patterns:
        if old in content:
            content = content.replace(old, new_footer)
            replaced = True
            break
    
    if not replaced:
        # Try a more flexible approach - find lines containing Moody and MacArthur near the footer
        lines = content.split('\n')
        new_lines = []
        i = 0
        while i < len(lines):
            line = lines[i]
            # Look for the commentary sources line that wraps
            if 'Commentary sources:' in line and 'Enduring Word' in line:
                # Collect the full footer attribution (may span multiple lines)
                footer_block = line
                j = i + 1
                while j < len(lines) and ('Moody' in lines[j] or 'MacArthur' in lines[j] or 'Spurgeon' in lines[j] or 'Bible Commentary' in lines[j]):
                    footer_block += '\n' + lines[j]
                    j += 1
                
                if 'Moody' in footer_block or 'MacArthur' in footer_block:
                    new_lines.append("Commentary sources: Enduring Word (enduringword.com), Charles Spurgeon (Public Domain),")
                    new_lines.append("Matthew Henry (Public Domain)")
                    replaced = True
                    i = j
                    continue
                else:
                    new_lines.append(line)
            else:
                new_lines.append(line)
            i += 1
        
        if replaced:
            content = '\n'.join(new_lines)
    
    if replaced:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"  Fixed: Chapter {ch}")
    else:
        print(f"  Could not fix: Chapter {ch}")
        # Print the last few lines for debugging
        lines = content.split('\n')
        for l in lines[-10:]:
            print(f"    |{l}")
