#!/usr/bin/env python3
"""
Extract the first page of a PDF as a high-quality PNG thumbnail.

Usage:
    python3 extract_pdf_thumbnail.py <input.pdf> [<output.png>]

If output is omitted, it defaults to <input>-thumb.png in the same directory.

Requires: pymupdf (pip install pymupdf)
"""

import sys
import os

try:
    import fitz
except ImportError:
    print("Error: pymupdf is required. Install with: pip install pymupdf")
    sys.exit(1)


def extract_thumbnail(pdf_path, output_path=None):
    if not os.path.exists(pdf_path):
        print(f"Error: {pdf_path} not found")
        sys.exit(1)

    if output_path is None:
        base, _ = os.path.splitext(pdf_path)
        output_path = base + "-thumb.png"

    doc = fitz.open(pdf_path)
    page = doc[0]  # First page
    pix = page.get_pixmap(dpi=150)
    pix.save(output_path)
    doc.close()

    print(f"Saved thumbnail: {output_path} ({pix.width}x{pix.height})")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    pdf_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else None
    extract_thumbnail(pdf_path, output_path)
