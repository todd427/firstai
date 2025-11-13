#!/usr/bin/env python3
"""
remove_bookmarks.py
Removes all Word bookmarks from one or more DOCX files.

Usage:
    python remove_bookmarks.py *.docx
    python remove_bookmarks.py input.docx other.docx
    python remove_bookmarks.py --in-place *.docx
    python remove_bookmarks.py --output cleaned_docs *.docx
"""

import argparse
import os
import sys
import glob
from docx import Document

def strip_bookmarks(element):
    """Recursively remove all bookmarkStart and bookmarkEnd tags from an element."""
    # Use local-name() instead of explicit namespace to avoid namespace issues
    for node in element.xpath(".//*[local-name()='bookmarkStart' or local-name()='bookmarkEnd']"):
        parent = node.getparent()
        if parent is not None:
            parent.remove(node)

def clean_docx(input_path, output_path):
    """Open a DOCX, remove bookmarks everywhere, and save."""
    doc = Document(input_path)

    # Body
    strip_bookmarks(doc.element.body)

    # Headers & footers
    for section in doc.sections:
        if section.header:
            strip_bookmarks(section.header._element)
        if section.footer:
            strip_bookmarks(section.footer._element)

    doc.save(output_path)
    print(f"✅ Cleaned: {os.path.basename(input_path)} → {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Remove all bookmarks from DOCX files.")
    parser.add_argument("files", nargs="+", help="DOCX files or patterns (e.g. *.docx)")
    parser.add_argument("--in-place", action="store_true", help="Overwrite original files")
    parser.add_argument("--output", type=str, help="Output directory for cleaned files")

    args = parser.parse_args()

    file_list = []
    for pattern in args.files:
        file_list.extend(glob.glob(pattern))
    file_list = [f for f in file_list if f.lower().endswith(".docx")]

    if not file_list:
        print("No DOCX files found.")
        sys.exit(1)

    if args.output:
        os.makedirs(args.output, exist_ok=True)

    for path in file_list:
        if args.in_place:
            output_path = path
        elif args.output:
            output_path = os.path.join(args.output, os.path.basename(path))
        else:
            base, ext = os.path.splitext(path)
            output_path = f"{base}_cleaned{ext}"

        clean_docx(path, output_path)

if __name__ == "__main__":
    main()

