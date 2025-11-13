#!/usr/bin/env python3
"""
md_to_docx_recursive.py — Convert all Markdown files in a directory tree to DOCX
Usage:
    python md_to_docx_recursive.py input_dir [output_dir]

Dependencies:
    pip install pypandoc
    # Pandoc must be installed system-wide:
    #   Windows: choco install pandoc
    #   Ubuntu: sudo apt install pandoc
"""

import os
import sys
import pypandoc

def convert_md_to_docx(src_dir, out_dir=None):
    src_dir = os.path.abspath(src_dir)
    out_dir = os.path.abspath(out_dir or src_dir)

    for root, _, files in os.walk(src_dir):
        # Determine output path mirroring structure
        rel_path = os.path.relpath(root, src_dir)
        dest_path = os.path.join(out_dir, rel_path)
        os.makedirs(dest_path, exist_ok=True)

        for fname in files:
            if fname.lower().endswith(".md"):
                md_path = os.path.join(root, fname)
                docx_name = os.path.splitext(fname)[0] + ".docx"
                out_path = os.path.join(dest_path, docx_name)

                print(f"Converting {md_path} → {out_path}")
                try:
                    pypandoc.convert_file(md_path, "docx", outputfile=out_path)
                except Exception as e:
                    print(f"⚠️ Failed to convert {fname}: {e}")

    print(f"\n✅ Conversion complete.\nDOCX files saved in: {out_dir}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python md_to_docx_recursive.py input_dir [output_dir]")
        sys.exit(1)
    convert_md_to_docx(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)

