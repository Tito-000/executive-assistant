"""
Create favicon and apple-touch-icon from a base logo image.

Usage:
    python3 make_favicon.py <input_image> <output_dir>

Creates:
    - mm-favicon-32.png (32x32)
    - mm-favicon-180.png (180x180, apple-touch-icon)
"""

import sys
import os
from PIL import Image

def make_favicons(input_path, output_dir):
    img = Image.open(input_path)

    # Ensure square crop (center crop if not square)
    w, h = img.size
    if w != h:
        size = min(w, h)
        left = (w - size) // 2
        top = (h - size) // 2
        img = img.crop((left, top, left + size, top + size))

    sizes = {
        "mm-favicon-32.png": 32,
        "mm-favicon-180.png": 180,
    }

    for filename, size in sizes.items():
        resized = img.resize((size, size), Image.LANCZOS)
        path = os.path.join(output_dir, filename)
        resized.save(path, "PNG")
        print(f"Saved {path} ({size}x{size})")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 make_favicon.py <input_image> <output_dir>")
        sys.exit(1)

    make_favicons(sys.argv[1], sys.argv[2])
