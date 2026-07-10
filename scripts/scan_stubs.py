#!/usr/bin/env python3
"""Scan OT and NT study notes for stub/skeleton files that are incomplete.
Criteria for a stub:
- File is very short (under 80 lines)
- Missing KEY VERSES section
- Missing CROSS-REFERENCES section
- Missing PERSONAL REFLECTION section
- Has placeholder text like "[content needed]" or very thin sections
"""
import os

def scan_file(filepath):
    with open(filepath, 'r') as f:
        content = f.read()
        lines = content.split('\n')
    
    issues = []
    line_count = len(lines)
    
    # Very short file (likely a stub)
    if line_count < 80:
        issues.append("VERY SHORT (" + str(line_count) + " lines)")
    
    # Check for missing critical sections
    if 'KEY VERSES' not in content:
        issues.append("missing KEY VERSES")
    if 'CROSS-REFERENCES' not in content:
        issues.append("missing CROSS-REFERENCES")
    if 'AUTHORSHIP & HISTORICAL BACKGROUND' not in content:
        issues.append("missing AUTHORSHIP")
    if 'TRANSLATION NOTES' not in content:
        issues.append("missing TRANSLATION NOTES")
    if 'PERSONAL REFLECTION' not in content:
        issues.append("missing PERSONAL REFLECTION")
    if 'COMMENTARY REFERENCES' not in content:
        issues.append("missing COMMENTARY REFERENCES")
    
    # Check for placeholder text
    if '[content needed]' in content.lower() or '[to be added]' in content.lower():
        issues.append("has placeholder text")
    
    return issues

# Scan both OT and NT
results = []
for testament in ["Old Testament", "New Testament"]:
    tbase = "/Users/jeremymcadoo/Desktop/Kiro Projects/Bible Study/" + testament
    for bookdir in sorted(os.listdir(tbase)):
        bookpath = os.path.join(tbase, bookdir)
        if not os.path.isdir(bookpath) or bookdir.startswith('.'):
            continue
        for chapdir in sorted(os.listdir(bookpath)):
            if not chapdir.startswith("Chapter"):
                continue
            filepath = os.path.join(bookpath, chapdir, chapdir + " - Study Notes.txt")
            if not os.path.isfile(filepath):
                continue
            issues = scan_file(filepath)
            if issues:
                results.append((testament, bookdir, chapdir, issues))

# Report
print("=== STUB/SKELETON FILE SCAN RESULTS ===\n")

# Group by severity
very_short = [r for r in results if any("VERY SHORT" in i for i in r[3])]
missing_multiple = [r for r in results if len(r[3]) >= 3 and r not in very_short]
missing_one_two = [r for r in results if len(r[3]) <= 2 and r not in very_short]

print("--- VERY SHORT FILES (likely stubs) ---")
print("Count: " + str(len(very_short)))
for t, book, ch, issues in very_short[:50]:
    print("  " + t[:2] + " " + book + "/" + ch + ": " + ", ".join(issues))
if len(very_short) > 50:
    print("  ... and " + str(len(very_short) - 50) + " more")

print("\n--- MISSING 3+ SECTIONS (incomplete) ---")
print("Count: " + str(len(missing_multiple)))
for t, book, ch, issues in missing_multiple[:30]:
    print("  " + t[:2] + " " + book + "/" + ch + ": " + ", ".join(issues))
if len(missing_multiple) > 30:
    print("  ... and " + str(len(missing_multiple) - 30) + " more")

print("\n--- MISSING 1-2 SECTIONS (mostly complete) ---")
print("Count: " + str(len(missing_one_two)))
# Just summarize by section
from collections import Counter
missing_counts = Counter()
for t, book, ch, issues in missing_one_two:
    for i in issues:
        missing_counts[i] += 1
for section, cnt in missing_counts.most_common():
    print("  " + section + ": " + str(cnt) + " files")

print("\n--- TOTAL ---")
print("Files with issues: " + str(len(results)) + " out of 1189")
print("Files fully complete: " + str(1189 - len(results)))
