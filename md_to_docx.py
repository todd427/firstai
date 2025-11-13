#!/usr/bin/env python3
"""
md_to_docx.py — Convert Markdown files in a directory to DOCX
Usage:
    python md_to_docx.py input_dir [output_dir]
Dependencies:
    pip install pypandoc
"""

import os
import sys
import pypandoc

def convert_md_to_docx(src_dir, out_dir=None):
    src_dir = os.path.abspath(src_dir)
    out_dir = os.path.abspath(out_dir or src_dir)

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    for fname in os.listdir(src_dir):
        if fname.lower().endswith(".md"):
            md_path = os.path.join(src_dir, fname)
            docx_name = os.path.splitext(fname)[0] + ".docx"
            out_path = os.path.join(out_dir, docx_name)

            print(f"Converting {fname} → {docx_name}")
            pypandoc.convert_file(md_path, "docx", outputfile=out_path)

    print(f"✅ Conversion complete. Files saved in: {out_dir}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python md_to_docx.py input_dir [output_dir]")
        sys.exit(1)
    convert_md_to_docx(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)

