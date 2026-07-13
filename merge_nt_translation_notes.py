#!/usr/bin/env python3
"""
Merge split TRANSLATION NOTES and ADDITIONAL TRANSLATION NOTES (ASV, NET, WEB)
sections into a unified TRANSLATION COMPARISON section in all New Testament
study notes files — matching the format used in Genesis 1.

The Genesis 1 format groups all translations (KJV, ESV, ASV, NET, WEB) together
per verse with an "Analysis:" line summarizing the differences.
"""

import os
import re
import sys
import glob


def find_sections(content):
    """
    Find all section boundaries in the file.
    Returns list of (header_text, start_pos, text_start_pos) sorted by position.
    """
    # Match section headers: ALL CAPS line followed by dashes
    pattern = re.compile(r'^([A-Z][A-Z &().,\-/\'0-9]+)\n-{4,}\n', re.MULTILINE)
    sections = []
    for m in pattern.finditer(content):
        sections.append({
            'header': m.group(1),
            'header_start': m.start(),
            'text_start': m.end()
        })
    return sections


def get_section_text(content, sections, header_name):
    """
    Get the text of a section by header name.
    Returns (text, header_start, section_end) or (None, None, None).
    """
    for i, sec in enumerate(sections):
        if sec['header'].startswith(header_name):
            text_start = sec['text_start']
            # End is start of next section (or end of file)
            if i + 1 < len(sections):
                section_end = sections[i + 1]['header_start']
            else:
                section_end = len(content)
            text = content[text_start:section_end].strip()
            return text, sec['header_start'], section_end
    return None, None, None


def parse_verse_entries(section_text):
    """
    Parse a translation notes section into verse entries.
    Returns list of (verse_key, full_text) tuples.
    verse_key is a tuple of ints for sorting (e.g., (1,) or (24,26,28)).
    """
    if not section_text or not section_text.strip():
        return []

    entries = []
    lines = section_text.split('\n')
    current_lines = []
    current_verse = None

    for line in lines:
        # Check if line starts a new verse entry
        verse_match = re.match(r'^(v\.[\d,]+)', line)
        if verse_match:
            # Save previous entry
            if current_verse is not None:
                entries.append((current_verse, '\n'.join(current_lines)))
            # Start new entry
            verse_str = verse_match.group(1)
            nums = re.findall(r'\d+', verse_str)
            current_verse = tuple(int(n) for n in nums)
            current_lines = [line]
        elif current_verse is not None:
            current_lines.append(line)

    # Save last entry
    if current_verse is not None:
        entries.append((current_verse, '\n'.join(current_lines)))

    return entries


def strip_verse_prefix_and_reindent(text):
    """
    Remove the verse prefix (v.N  — ) from text and normalize indentation
    so continuation lines align at 7 spaces (matching primary entry format).
    """
    lines = text.split('\n')
    if not lines:
        return text

    # Remove "v.N  — " from first line
    first_line = re.sub(r'^v\.[\d,]+\s*[-–—]\s*', '', lines[0])

    # For continuation lines, strip existing indentation and re-indent to 7 spaces
    result_lines = [first_line]
    for line in lines[1:]:
        stripped = line.lstrip()
        if stripped:
            result_lines.append('       ' + stripped)
        else:
            result_lines.append('')

    return '\n'.join(result_lines)


def merge_entries(primary_entries, additional_entries):
    """
    Merge primary and additional translation entries by verse.
    For verses that appear in both, combine the content.
    The additional content is appended under the primary with proper indentation.
    """
    # Build lookup from additional entries
    additional_map = {}
    for verse_key, text in additional_entries:
        additional_map[verse_key] = text

    # Track which additional entries have been consumed
    consumed = set()

    merged = []
    for verse_key, primary_text in primary_entries:
        if verse_key in additional_map:
            # Combine: primary text + additional content (with verse prefix stripped)
            add_text = additional_map[verse_key]
            add_content = strip_verse_prefix_and_reindent(add_text)
            # Indent the first line and keep others as-is (already re-indented)
            add_lines = add_content.split('\n')
            first_add_line = '       ' + add_lines[0] if add_lines[0].strip() else ''
            rest_add_lines = add_lines[1:] if len(add_lines) > 1 else []
            indented_add = '\n'.join([first_add_line] + rest_add_lines)
            combined = primary_text.rstrip() + '\n' + indented_add.rstrip()
            merged.append((verse_key, combined))
            consumed.add(verse_key)
        else:
            merged.append((verse_key, primary_text.rstrip()))

    # Add any additional entries that weren't in primary
    for verse_key, text in additional_entries:
        if verse_key not in consumed:
            merged.append((verse_key, text.rstrip()))

    # Sort by verse number
    merged.sort(key=lambda x: x[0])
    return merged


def process_file(filepath, dry_run=False):
    """
    Process a single study notes file.
    Returns (success: bool, message_or_content: str)
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check prerequisites
    if 'TRANSLATION COMPARISON\n----' in content:
        return False, "Already has TRANSLATION COMPARISON"

    if 'TRANSLATION NOTES\n----' not in content:
        return False, "No TRANSLATION NOTES section found"

    # Find all sections
    sections = find_sections(content)

    # Get primary TRANSLATION NOTES
    primary_text, primary_start, primary_end = get_section_text(
        content, sections, 'TRANSLATION NOTES'
    )

    if primary_text is None:
        return False, "Could not extract TRANSLATION NOTES"

    # Get ADDITIONAL TRANSLATION NOTES (if present)
    additional_text, additional_start, additional_end = get_section_text(
        content, sections, 'ADDITIONAL TRANSLATION NOTES'
    )

    # Parse entries
    primary_entries = parse_verse_entries(primary_text)
    additional_entries = parse_verse_entries(additional_text) if additional_text else []

    # Merge
    merged_entries = merge_entries(primary_entries, additional_entries)

    # Build new section content
    merged_lines = []
    for i, (verse_key, text) in enumerate(merged_entries):
        merged_lines.append(text)
        # Add blank line between entries (but not after last)
        if i < len(merged_entries) - 1:
            # Only add blank line if not already ending with one
            if not text.endswith('\n'):
                merged_lines.append('')

    merged_content = '\n'.join(merged_lines)

    new_section = 'TRANSLATION COMPARISON\n'
    new_section += '------------------------------------\n'
    new_section += merged_content + '\n\n'

    # Build new file content by removing both old sections and inserting new one
    if additional_start is not None:
        # Both sections exist - determine order and remove both
        if primary_start < additional_start:
            # Primary comes first (normal case)
            # Replace from primary_start to additional_end with new section
            new_content = content[:primary_start] + new_section + content[additional_end:]
        else:
            # Additional comes first (unusual)
            new_content = content[:additional_start] + new_section + content[primary_end:]
    else:
        # Only primary section exists
        new_content = content[:primary_start] + new_section + content[primary_end:]

    if dry_run:
        return True, new_content

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

    return True, "Merged successfully"


def main():
    nt_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'New Testament')

    if not os.path.isdir(nt_path):
        print(f"Error: New Testament directory not found at {nt_path}")
        sys.exit(1)

    # Find all study notes files
    study_files = glob.glob(os.path.join(nt_path, '*', '*', '*Study Notes.txt'))
    study_files.sort()

    print(f"Found {len(study_files)} study notes files in New Testament")
    print("=" * 60)

    dry_run = '--dry-run' in sys.argv

    if dry_run:
        print("DRY RUN MODE - no files will be modified\n")

    success_count = 0
    skip_count = 0
    error_count = 0
    errors = []

    for filepath in study_files:
        rel_path = os.path.relpath(filepath, nt_path)
        try:
            result, message = process_file(filepath, dry_run=dry_run)
            if result:
                success_count += 1
                if not dry_run:
                    print(f"  [OK] {rel_path}")
            else:
                skip_count += 1
                print(f"  [SKIP] {rel_path} - {message}")
        except Exception as e:
            error_count += 1
            errors.append((rel_path, str(e)))
            print(f"  [ERROR] {rel_path} - {e}")

    print("\n" + "=" * 60)
    print(f"Results: {success_count} merged, {skip_count} skipped, {error_count} errors")
    print(f"Total files processed: {len(study_files)}")

    if errors:
        print("\nErrors:")
        for path, err in errors:
            print(f"  {path}: {err}")


if __name__ == '__main__':
    main()
