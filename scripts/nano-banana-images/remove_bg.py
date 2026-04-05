"""
Remove solid background from logo images and create transparent PNGs.
Works by converting near-black pixels to transparent.

Usage:
    python3 remove_bg.py <input_image> <output_png> [threshold]

    threshold: how far from black (#0A0A0A) a pixel can be and still be removed (default: 30)

Examples:
    python3 remove_bg.py originals/mm-v7-circle-ring.jpg transparent/mm-v7-circle-ring-transparent.png
    python3 remove_bg.py originals/mm-v7-circle-ring.jpg transparent/mm-v7-circle-ring-transparent.png 40
"""

import sys
from PIL import Image

def remove_bg(input_path, output_path, threshold=30):
    img = Image.open(input_path).convert("RGBA")
    pixels = img.load()
    w, h = img.size

    for y in range(h):
        for x in range(w):
            r, g, b, a = pixels[x, y]
            # If pixel is near-black (close to #0A0A0A or #000000), make transparent
            if r <= threshold and g <= threshold and b <= threshold:
                pixels[x, y] = (0, 0, 0, 0)

    img.save(output_path, "PNG")
    print(f"Saved transparent PNG: {output_path} ({w}x{h})")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python3 remove_bg.py <input_image> <output_png> [threshold]")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    threshold = int(sys.argv[3]) if len(sys.argv) > 3 else 30

    remove_bg(input_path, output_path, threshold)
