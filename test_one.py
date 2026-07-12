#!/usr/bin/env python3
"""Test on just Chapter 1."""
import sys
sys.path.insert(0, '/Users/jeremymcadoo/Desktop/Kiro Projects/Bible Study')
from transform_translations import process_file

filepath = "/Users/jeremymcadoo/Desktop/Kiro Projects/Bible Study/Old Testament/05 - Deuteronomy/Chapter 1/Chapter 1 - Study Notes.txt"
process_file(filepath)
