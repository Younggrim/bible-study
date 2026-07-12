#!/usr/bin/env python3
"""
Bible Translation Audit Script
Scans all Bible translation files and identifies missing or incomplete ones.
"""

import os
import re
from collections import defaultdict
from datetime import datetime

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TRANSLATIONS = ["ESV", "KJV", "ASV", "NET", "WEB"]
TESTAMENTS = ["Old Testament", "New Testament"]
REPORT_PATH = os.path.join(BASE_DIR, "translation_audit_report.txt")


def count_verses(filepath):
    """Count the number of verses in a translation file.
    Verses are formatted as 'N. Verse text here' at the start of a line."""
    if not os.path.exists(filepath):
        return -1  # File doesn't exist
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception:
        return -1
    
    # Match lines that start with a number followed by a period and space
    verses = re.findall(r'^\d+\.\s+', content, re.MULTILINE)
    return len(verses)


def get_chapters(book_path):
    """Get all chapter directories within a book directory."""
    chapters = []
    if not os.path.isdir(book_path):
        return chapters
    
    for item in os.listdir(book_path):
        item_path = os.path.join(book_path, item)
        if os.path.isdir(item_path) and item.startswith("Chapter "):
            # Extract chapter number for sorting
            try:
                ch_num = int(item.replace("Chapter ", ""))
                chapters.append((ch_num, item, item_path))
            except ValueError:
                continue
    
    chapters.sort(key=lambda x: x[0])
    return chapters


def get_books(testament_path):
    """Get all book directories within a testament directory."""
    books = []
    if not os.path.isdir(testament_path):
        return books
    
    for item in os.listdir(testament_path):
        item_path = os.path.join(testament_path, item)
        if os.path.isdir(item_path) and re.match(r'^\d+\s*-\s*.+', item):
            # Extract book number for sorting
            try:
                num = int(re.match(r'^(\d+)', item).group(1))
                books.append((num, item, item_path))
            except (ValueError, AttributeError):
                continue
    
    books.sort(key=lambda x: x[0])
    return books


def audit_translations():
    """Main audit function."""
    total_chapters = 0
    total_files_checked = 0
    missing_files = []
    incomplete_files = []
    empty_files = []
    
    for testament in TESTAMENTS:
        testament_path = os.path.join(BASE_DIR, testament)
        if not os.path.isdir(testament_path):
            continue
        
        books = get_books(testament_path)
        
        for book_num, book_name, book_path in books:
            chapters = get_chapters(book_path)
            
            for ch_num, ch_dir_name, ch_path in chapters:
                total_chapters += 1
                verse_counts = {}
                
                # Count verses for each translation
                for translation in TRANSLATIONS:
                    filename = f"{ch_dir_name} - {translation}.txt"
                    filepath = os.path.join(ch_path, filename)
                    total_files_checked += 1
                    verse_counts[translation] = count_verses(filepath)
                
                # Determine expected verse count (max across available translations)
                available_counts = [c for c in verse_counts.values() if c > 0]
                if not available_counts:
                    expected = 0
                else:
                    expected = max(available_counts)
                
                # Flag problems
                location = f"{testament}/{book_name}/{ch_dir_name}"
                
                for translation in TRANSLATIONS:
                    count = verse_counts[translation]
                    filename = f"{ch_dir_name} - {translation}.txt"
                    
                    if count == -1:
                        missing_files.append({
                            "location": location,
                            "translation": translation,
                            "filename": filename,
                            "expected": expected
                        })
                    elif count == 0:
                        empty_files.append({
                            "location": location,
                            "translation": translation,
                            "filename": filename,
                            "expected": expected
                        })
                    elif expected > 0 and count < expected:
                        incomplete_files.append({
                            "location": location,
                            "translation": translation,
                            "filename": filename,
                            "has": count,
                            "expected": expected
                        })
    
    return {
        "total_chapters": total_chapters,
        "total_files_checked": total_files_checked,
        "missing": missing_files,
        "incomplete": incomplete_files,
        "empty": empty_files
    }


def generate_report(results):
    """Generate the audit report."""
    lines = []
    lines.append("=" * 70)
    lines.append("BIBLE TRANSLATION AUDIT REPORT")
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append("=" * 70)
    lines.append("")
    lines.append("SUMMARY")
    lines.append("-" * 40)
    lines.append(f"Total chapters scanned:    {results['total_chapters']}")
    lines.append(f"Total files checked:       {results['total_files_checked']}")
    lines.append(f"Translations checked:      {', '.join(TRANSLATIONS)}")
    lines.append("")
    
    total_problems = len(results['missing']) + len(results['incomplete']) + len(results['empty'])
    lines.append(f"Total problems found:      {total_problems}")
    lines.append(f"  - Missing files:         {len(results['missing'])}")
    lines.append(f"  - Incomplete files:      {len(results['incomplete'])}")
    lines.append(f"  - Empty files:           {len(results['empty'])}")
    lines.append("")
    
    # Missing files
    lines.append("=" * 70)
    lines.append(f"MISSING FILES ({len(results['missing'])})")
    lines.append("=" * 70)
    if results['missing']:
        for item in results['missing']:
            lines.append(f"  [{item['translation']}] {item['location']}")
            lines.append(f"         File: {item['filename']}")
            if item['expected'] > 0:
                lines.append(f"         Expected verses: {item['expected']}")
            lines.append("")
    else:
        lines.append("  None - all translation files are present!")
        lines.append("")
    
    # Empty files
    lines.append("=" * 70)
    lines.append(f"EMPTY FILES ({len(results['empty'])})")
    lines.append("=" * 70)
    if results['empty']:
        for item in results['empty']:
            lines.append(f"  [{item['translation']}] {item['location']}")
            lines.append(f"         File: {item['filename']}")
            lines.append(f"         Has 0 verses (expected {item['expected']})")
            lines.append("")
    else:
        lines.append("  None - no empty translation files found!")
        lines.append("")
    
    # Incomplete files
    lines.append("=" * 70)
    lines.append(f"INCOMPLETE FILES ({len(results['incomplete'])})")
    lines.append("=" * 70)
    if results['incomplete']:
        for item in results['incomplete']:
            lines.append(f"  [{item['translation']}] {item['location']}")
            lines.append(f"         File: {item['filename']}")
            lines.append(f"         Has {item['has']} verses (expected {item['expected']})")
            lines.append("")
    else:
        lines.append("  None - all translation files have complete verse counts!")
        lines.append("")
    
    # Per-translation summary
    lines.append("=" * 70)
    lines.append("PER-TRANSLATION BREAKDOWN")
    lines.append("=" * 70)
    for trans in TRANSLATIONS:
        missing_count = sum(1 for x in results['missing'] if x['translation'] == trans)
        empty_count = sum(1 for x in results['empty'] if x['translation'] == trans)
        incomplete_count = sum(1 for x in results['incomplete'] if x['translation'] == trans)
        total = missing_count + empty_count + incomplete_count
        lines.append(f"  {trans:5s}: {total:4d} issues  "
                     f"(Missing: {missing_count}, Empty: {empty_count}, Incomplete: {incomplete_count})")
    lines.append("")
    lines.append("=" * 70)
    lines.append("END OF REPORT")
    lines.append("=" * 70)
    
    return "\n".join(lines)


if __name__ == "__main__":
    print("Bible Translation Audit")
    print("Scanning translation files...")
    print()
    
    results = audit_translations()
    report = generate_report(results)
    
    # Write report to file
    with open(REPORT_PATH, 'w', encoding='utf-8') as f:
        f.write(report)
    
    # Print report to console
    print(report)
    print()
    print(f"Report saved to: {REPORT_PATH}")
