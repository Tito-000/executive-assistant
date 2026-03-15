from PIL import Image, ImageFilter, ImageEnhance
import sys

BASE = "/Users/martinmercedes/Desktop/Executive assistant 2/projects/immunotec/fase-1-embudos-por-producto/productos/platinum/Creativos nuevos para test/platinum-winning-ad-multiflex-base.jpg"
BOX = "/Users/martinmercedes/Desktop/Executive assistant 2/projects/immunotec/fase-1-embudos-por-producto/productos/platinum/recursos/imagenes-producto/vsd.png"
SACHET = "/Users/martinmercedes/Desktop/Executive assistant 2/projects/immunotec/fase-1-embudos-por-producto/productos/platinum/recursos/imagenes-producto/vsf.png"
OUTPUT = "/Users/martinmercedes/Desktop/Executive assistant 2/projects/immunotec/fase-1-embudos-por-producto/productos/platinum/Creativos nuevos para test/platinum-winning-ad-multiflex-final.jpg"

def remove_white_bg(img, threshold=230):
    img = img.convert("RGBA")
    data = img.getdata()
    new_data = []
    for r, g, b, a in data:
        if r > threshold and g > threshold and b > threshold:
            new_data.append((r, g, b, 0))
        else:
            new_data.append((r, g, b, a))
    img.putdata(new_data)
    return img

def add_soft_glow(img, glow_color=(212, 175, 55), radius=25, opacity=90):
    glow = img.copy().convert("RGBA")
    colored = Image.new("RGBA", img.size, (*glow_color, 0))
    for i in range(3):
        blurred = glow.filter(ImageFilter.GaussianBlur(radius + i * 8))
        colored.paste(blurred, mask=blurred.split()[3])
    colored.putalpha(opacity)
    result = Image.new("RGBA", img.size, (0, 0, 0, 0))
    result.paste(colored, (0, 0), colored)
    result.paste(img, (0, 0), img)
    return result

base = Image.open(BASE).convert("RGBA")
W, H = base.size

# Load and prep box
box_img = Image.open(BOX).convert("RGBA")
box_img = remove_white_bg(box_img, threshold=220)

# Load and prep sachet
sachet_img = Image.open(SACHET).convert("RGBA")
sachet_img = remove_white_bg(sachet_img, threshold=220)

# --- Position box (centered, slightly left, product zone ~18%-65% of height) ---
# Box: width ~32% of canvas, centered horizontally slightly left
box_w = int(W * 0.34)
box_ar = box_img.height / box_img.width
box_h = int(box_w * box_ar)
box_img = box_img.resize((box_w, box_h), Image.LANCZOS)
box_img = add_soft_glow(box_img, glow_color=(212, 175, 55), radius=20, opacity=80)

# Box position: center at ~42% from top, shift left slightly
box_x = int(W * 0.5 - box_w * 0.58)
box_y = int(H * 0.19)

# --- Position sachet (overlapping box, front-right, slightly lower) ---
sachet_w = int(W * 0.22)
sachet_ar = sachet_img.height / sachet_img.width
sachet_h = int(sachet_w * sachet_ar)
sachet_img = sachet_img.resize((sachet_w, sachet_h), Image.LANCZOS)
sachet_img = add_soft_glow(sachet_img, glow_color=(212, 175, 55), radius=15, opacity=70)

# Sachet: overlaps box to the right and slightly lower (layered effect)
sachet_x = int(W * 0.5 + box_w * 0.02)
sachet_y = int(H * 0.28)

# Paste in order: box first, then sachet on top
composite = base.copy()
composite.paste(box_img, (box_x, box_y), box_img)
composite.paste(sachet_img, (sachet_x, sachet_y), sachet_img)

# Save as JPEG
final = composite.convert("RGB")
final.save(OUTPUT, "JPEG", quality=95)
print(f"Saved: {OUTPUT}")
