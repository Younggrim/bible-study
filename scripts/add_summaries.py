#!/usr/bin/env python3
"""Add CHAPTER SUMMARY to NT study notes files."""
import os
import sys

def add_summary(filepath, summary_text):
    with open(filepath, 'r') as f:
        lines = f.readlines()
    sep_idx = None
    for i, line in enumerate(lines):
        if line.strip().startswith('========') and i < 5:
            sep_idx = i
            break
    if sep_idx is None:
        return False
    for line in lines:
        if 'CHAPTER SUMMARY' in line:
            return False
    new_lines = lines[:sep_idx + 1]
    new_lines.append('\n')
    new_lines.append('CHAPTER SUMMARY\n')
    new_lines.append('------------------------------------\n')
    new_lines.append(summary_text + '\n')
    rest_start = sep_idx + 1
    if rest_start < len(lines) and lines[rest_start].strip() == '':
        new_lines.append('\n')
        rest_start += 1
    else:
        new_lines.append('\n')
    new_lines.extend(lines[rest_start:])
    with open(filepath, 'w') as f:
        f.writelines(new_lines)
    return True

data_file = sys.argv[1]
with open(data_file, 'r') as f:
    for line in f:
        line = line.strip()
        if '|||' in line:
            filepath, summary = line.split('|||', 1)
            if os.path.isfile(filepath):
                if add_summary(filepath, summary):
                    ch = os.path.basename(os.path.dirname(filepath))
                    print(f"  done {ch}")
                else:
                    print(f"  skip {os.path.basename(os.path.dirname(filepath))}")
            else:
                print(f"  missing: {filepath}")
