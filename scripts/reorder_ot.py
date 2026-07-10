#!/usr/bin/env python3
"""
Reorder all OT study notes to match the Matthew 1 gold standard order:
1. CHAPTER SUMMARY
2. AUTHORSHIP & HISTORICAL BACKGROUND
3. MAP & GEOGRAPHY NOTES (if present)
4. KEY VERSES
5. CROSS-REFERENCES
6. COMMENTARY REFERENCES
7. TRANSLATION NOTES
8. ADDITIONAL TRANSLATION NOTES (if present)
9. GLOSSARY (if present)
10. PERSONAL REFLECTION & APPLICATION (if present)
11. REFLECTION QUESTIONS (if present)
12. VIDEO RESOURCES
13. PODCAST RESOURCES
14. PERSONAL NOTES
Also: Remove Matthew Henry and John Calvin from COMMENTARY REFERENCES.
Also: Fix footer attribution.
"""
import os
import re

SECTION_ORDER = [
    'CHAPTER SUMMARY',
    'AUTHORSHIP & HISTORICAL BACKGROUND',
    'MAP & GEOGRAPHY NOTES',
    'KEY VERSES',
    'CROSS-REFERENCES',
    'COMMENTARY REFERENCES',
    'TRANSLATION NOTES',
    'ADDITIONAL TRANSLATION NOTES',
    'GLOSSARY',
    'PERSONAL REFLECTION & APPLICATION',
    'REFLECTION QUESTIONS',
    'VIDEO RESOURCES',
    'PODCAST RESOURCES',
    'PERSONAL NOTES',
]

def get_section_key(section_title):
    title_upper = section_title.strip().upper()
    for i, s in enumerate(SECTION_ORDER):
        if title_upper.startswith(s):
            return i
    # Handle NOTE: lines that appear in some files
    if title_upper.startswith('NOTE:') or title_upper.startswith('NOTE '):
        return 998
    return 999

def parse_sections(content):
    lines = content.split('\n')
    
    # Find header
    header_end = 0
    for i, line in enumerate(lines):
        if line.strip().startswith('========') and i < 5:
            header_end = i
            break
    header = lines[:header_end + 1]
    
    # Find footer
    footer_start = len(lines)
    for i in range(len(lines) - 1, header_end, -1):
        if lines[i].strip().startswith('========') and i > header_end + 5:
            footer_start = i
            break
    footer = lines[footer_start:]
    
    # Parse sections
    body = lines[header_end + 1:footer_start]
    sections = []
    current_section = None
    current_lines = []
    
    for line in body:
        stripped = line.strip()
        if (stripped and
            len(stripped) > 3 and
            stripped == stripped.upper() and
            not stripped.startswith('----') and
            not stripped.startswith('====') and
            not stripped.startswith('HTTP') and
            not stripped.startswith('V.') and
            not stripped.startswith('(') and
            not stripped.startswith('"') and
            not stripped.startswith("'") and
            any(stripped.startswith(s) for s in SECTION_ORDER)):
            
            if current_section is not None:
                sections.append((current_section, current_lines))
            current_section = stripped
            current_lines = [line]
        else:
            current_lines.append(line)
    
    if current_section is not None:
        sections.append((current_section, current_lines))
    elif current_lines:
        sections.append(('_PREAMBLE', current_lines))
    
    return header, sections, footer

def remove_henry_calvin(sections):
    new_sections = []
    for title, lines in sections:
        if title.startswith('COMMENTARY REFERENCES'):
            filtered_lines = []
            skip_until_next = False
            for line in lines:
                if 'Matthew Henry' in line and ('Commentary' in line or 'Whole Bible' in line):
                    skip_until_next = True
                    continue
                elif 'John Calvin' in line and ('Commentar' in line or 'ccel.org' in line):
                    skip_until_next = True
                    continue
                elif skip_until_next:
                    if (line.strip() and
                        not line.startswith(' ') and
                        not line.startswith('\t') and
                        not line.strip().startswith('http') and
                        line.strip() != '------------------------------------'):
                        skip_until_next = False
                        filtered_lines.append(line)
                    elif line.strip() == '' and filtered_lines and filtered_lines[-1].strip() == '':
                        continue
                    else:
                        continue
                else:
                    filtered_lines.append(line)
            
            while filtered_lines and filtered_lines[-1].strip() == '':
                filtered_lines.pop()
            filtered_lines.append('')
            new_sections.append((title, filtered_lines))
        else:
            new_sections.append((title, lines))
    return new_sections

def reorder_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
    
    header, sections, footer = parse_sections(content)
    
    if not sections:
        return False
    
    # Remove Henry/Calvin
    sections = remove_henry_calvin(sections)
    
    # Sort sections
    sections.sort(key=lambda x: get_section_key(x[0]))
    
    # Rebuild file
    new_lines = header[:]
    for i, (title, section_lines) in enumerate(sections):
        if new_lines and new_lines[-1].strip() != '':
            new_lines.append('')
        for line in section_lines:
            new_lines.append(line)
    
    if new_lines and new_lines[-1].strip() != '':
        new_lines.append('')
    new_lines.append('')
    new_lines.extend(footer)
    
    new_content = '\n'.join(new_lines)
    new_content = re.sub(r'\n{4,}', '\n\n\n', new_content)
    
    # Fix footer
    new_content = new_content.replace(
        'Commentary sources: Enduring Word (enduringword.com), Charles\nSpurgeon (Public Domain), Matthew Henry (Public Domain), John Calvin (Public Domain)',
        'Commentary sources: Enduring Word (enduringword.com), Charles\nSpurgeon (Public Domain)')
    new_content = new_content.replace(
        'Commentary sources: Enduring Word (enduringword.com), Charles Spurgeon (Public Domain),\nMatthew Henry (Public Domain), John Calvin (Public Domain)',
        'Commentary sources: Enduring Word (enduringword.com), Charles Spurgeon (Public Domain)')
    new_content = new_content.replace(
        'Commentary sources: Enduring Word (enduringword.com), Charles Spurgeon (Public Domain), Matthew Henry (Public Domain), John Calvin (Public Domain)',
        'Commentary sources: Enduring Word (enduringword.com), Charles Spurgeon (Public Domain)')
    
    # Fix translations line
    new_content = re.sub(
        r'Translations referenced:.*',
        'Translations referenced: KJV, ESV, ASV, NET, WEB',
        new_content)
    
    if new_content != content:
        with open(filepath, 'w') as f:
            f.write(new_content)
        return True
    return False

# Process all OT files
base = "/Users/jeremymcadoo/Desktop/Kiro Projects/Bible Study/Old Testament"
total = 0
fixed = 0

for bookdir in sorted(os.listdir(base)):
    bookpath = os.path.join(base, bookdir)
    if not os.path.isdir(bookpath) or bookdir.startswith('.'):
        continue
    
    book_fixed = 0
    for chapdir in sorted(os.listdir(bookpath)):
        if not chapdir.startswith("Chapter"):
            continue
        filepath = os.path.join(bookpath, chapdir, chapdir + " - Study Notes.txt")
        if not os.path.isfile(filepath):
            continue
        total += 1
        if reorder_file(filepath):
            fixed += 1
            book_fixed += 1
    
    if book_fixed > 0:
        print("  " + bookdir + ": " + str(book_fixed) + " chapters reordered")

print("\nTotal: " + str(total) + " files checked, " + str(fixed) + " reordered")
