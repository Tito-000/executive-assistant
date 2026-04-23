from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

BASE = Path("/Users/martinmercedes/Desktop/Executive assistant 2")
LOGO_PATH = BASE / "projects/agencia-marketing/branding/logo/transparent/mm-v8-circle-stacked-transparent.png"
OUTPUT = BASE / "outputs/paypal-products/crm-ghl-mensualidad-600.png"

SIZE = 600
BG = (10, 10, 10)
YELLOW = (250, 220, 0)
WHITE = (255, 255, 255)
GRAY = (170, 170, 170)

canvas = Image.new("RGB", (SIZE, SIZE), BG)

logo = Image.open(LOGO_PATH).convert("RGBA")
logo_size = 280
logo.thumbnail((logo_size, logo_size), Image.LANCZOS)
lx = (SIZE - logo.width) // 2
ly = 90
canvas.paste(logo, (lx, ly), logo)

draw = ImageDraw.Draw(canvas)

def load_font(size, bold=False):
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/HelveticaNeue.ttc",
        "/Library/Fonts/Arial.ttf",
    ]
    for c in candidates:
        try:
            return ImageFont.truetype(c, size)
        except Exception:
            continue
    return ImageFont.load_default()

title_font = load_font(44, bold=True)
subtitle_font = load_font(26)
small_font = load_font(20)

def center_text(text, y, font, color):
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    draw.text(((SIZE - w) // 2, y), text, font=font, fill=color)

center_text("CRM GoHighLevel", 400, title_font, WHITE)
center_text("Mensualidad", 460, subtitle_font, YELLOW)
center_text("MM AGENCY", 520, small_font, GRAY)

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
canvas.save(OUTPUT, "PNG", optimize=True)
print(f"Saved: {OUTPUT}")
print(f"Size: {canvas.size}")
