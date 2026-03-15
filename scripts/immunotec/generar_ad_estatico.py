"""
Generador de ad estático estilo "ingredientes" para Meta Ads.
Layout: columna izquierda (texto) / columna derecha (producto) — sin solapamiento.
Psicología de color: crema cálido + navy = confianza + salud masculina.
"""

import os
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
except ImportError:
    print("ERROR: pip3 install Pillow")
    sys.exit(1)

BASE_DIR   = Path(__file__).parent.parent.parent.parent
PRODS_DIR  = BASE_DIR / "projects/immunotec/fase-1-embudos-por-producto/productos"
OUTPUT_DIR = PRODS_DIR / "magistral/Creativos nuevos para test"
FONT       = "/System/Library/Fonts/HelveticaNeue.ttc"

IDX_BLACK  = 9   # Condensed Black
IDX_BOLD   = 1
IDX_MEDIUM = 10
IDX_REG    = 0

# ── Paleta ─────────────────────────────────────────────────────────────────────
# Crema cálido (confianza, salud) + Navy (autoridad, masculinidad)
BG          = (243, 238, 228)   # crema cálido
NAVY        = (10,  35,  75)    # navy profundo — texto principal
BLUE_MID    = (22,  90,  170)   # azul medio — badges, acentos
PANEL_BG    = (10,  35,  75)    # navy — panel ingredientes
PANEL_TEXT  = (255, 255, 255)   # blanco
BADGE_BG    = (10,  35,  75)    # navy
BADGE_TEXT  = (255, 255, 255)
CIRCLE_BG   = (255, 255, 255)
CIRCLE_BOR  = (22,  90,  170)
CIRCLE_TEXT = (10,  35,  75)
FOOTER_BG   = (10,  35,  75)
FOOTER_TEXT = (255, 255, 255)
DIVIDER     = (200, 195, 185)   # línea divisora sutil


def font(size, idx=IDX_REG):
    return ImageFont.truetype(FONT, size, index=idx)


def pill(draw, xy, r, fill, border=None, bw=0):
    draw.rounded_rectangle(xy, radius=r, fill=fill,
                            outline=border, width=bw)


def remove_bg(img, thr=225):
    img = img.convert("RGBA")
    px = list(img.getdata())
    new = []
    for r, g, b, a in px:
        if r > thr and g > thr and b > thr:
            new.append((r, g, b, 0))
        else:
            new.append((r, g, b, a))
    img.putdata(new)
    return img


def add_glow(img, color=(60, 120, 200), blur=28):
    glow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    alpha = img.split()[3]
    col_img = Image.new("RGBA", img.size, (*color, 180))
    col_img.putalpha(alpha)
    for _ in range(4):
        col_img = col_img.filter(ImageFilter.GaussianBlur(blur // 4))
    return Image.alpha_composite(col_img, img)


def text_center(draw, text, cx, y, fnt, fill):
    bb = draw.textbbox((0, 0), text, font=fnt)
    w  = bb[2] - bb[0]
    draw.text((cx - w // 2, y), text, font=fnt, fill=fill)


def main():
    W, H = 1080, 1080
    SPLIT = 490          # x donde termina columna texto / empieza producto

    canvas = Image.new("RGBA", (W, H), (*BG, 255))
    draw   = ImageDraw.Draw(canvas)

    # ── Fondo sólido crema (sin gradiente — limpio como el reference) ──────────
    draw.rectangle([0, 0, W, H], fill=(*BG, 255))

    # Línea divisora sutil entre columnas
    draw.rectangle([SPLIT, 60, SPLIT + 2, H - 70], fill=(*DIVIDER, 180))

    # ═══════════════════════════════════════════════════════════════════
    # COLUMNA IZQUIERDA  (x: 0 → SPLIT)
    # ═══════════════════════════════════════════════════════════════════

    PAD = 52   # padding izquierdo

    # ── Marca ──────────────────────────────────────────────────────────────────
    f_marca = font(26, IDX_BOLD)
    draw.text((PAD, 46), "IMMUNOTEC®", font=f_marca, fill=BLUE_MID)

    # ── Badge "INGREDIENTES" — arriba derecha de la columna izquierda ──────────
    badge_txt = "INGREDIENTES"
    f_badge   = font(22, IDX_BOLD)
    bb        = draw.textbbox((0, 0), badge_txt, font=f_badge)
    bw, bh    = bb[2] - bb[0] + 36, bb[3] - bb[1] + 16
    bx        = SPLIT - bw - 16
    by        = 38
    pill(draw, [bx, by, bx + bw, by + bh], 20, BADGE_BG)
    draw.text((bx + 18, by + 8), badge_txt, font=f_badge, fill=BADGE_TEXT)

    # ── Nombre del producto ────────────────────────────────────────────────────
    f_title = font(148, IDX_BLACK)
    draw.text((PAD, 92), "MAGISTRAL", font=f_title, fill=NAVY)

    # Línea decorativa bajo el título
    draw.rectangle([PAD, 250, SPLIT - 30, 256], fill=(*BLUE_MID, 220))

    # ── Subtítulo ──────────────────────────────────────────────────────────────
    f_sub = font(38, IDX_BOLD)
    draw.text((PAD, 268), "PARA LA", font=f_sub, fill=NAVY)
    draw.text((PAD, 312), "PRÓSTATA", font=f_sub, fill=BLUE_MID)

    # ── Badges circulares ──────────────────────────────────────────────────────
    badges = [("SIN\nPARABENOS", 140), ("474\nML", 270), ("100%\nNATURAL", 400)]
    BY, BR = 425, 55
    f_cb = font(19, IDX_BOLD)
    for label, cx in badges:
        draw.ellipse([cx - BR, BY - BR, cx + BR, BY + BR],
                     fill=CIRCLE_BG, outline=CIRCLE_BOR, width=4)
        lines  = label.split("\n")
        tot_h  = len(lines) * 24
        start  = BY - tot_h // 2 + 2
        for i, line in enumerate(lines):
            lb = draw.textbbox((0, 0), line, font=f_cb)
            lw = lb[2] - lb[0]
            draw.text((cx - lw // 2, start + i * 24), line, font=f_cb, fill=CIRCLE_TEXT)

    # ── Panel ingredientes ─────────────────────────────────────────────────────
    PX1, PY1 = PAD, 508
    PX2, PY2 = SPLIT - 22, 1000
    pill(draw, [PX1, PY1, PX2, PY2], 24, PANEL_BG)

    ingredientes = [
        "SAW PALMETTO",
        "SERENOA REPENS",
        "LICOPENO",
        "ZINC",
        "VITAMINA E",
        "SELENIO",
    ]
    f_ingr = font(30, IDX_BOLD)
    iy     = PY1 + 30
    gap    = (PY2 - PY1 - 60) // len(ingredientes)
    for ing in ingredientes:
        # bullet
        draw.ellipse([PX1 + 22, iy + 11, PX1 + 34, iy + 23],
                     fill=(255, 255, 255, 200))
        draw.text((PX1 + 48, iy), ing, font=f_ingr, fill=PANEL_TEXT)
        iy += gap

    # ═══════════════════════════════════════════════════════════════════
    # COLUMNA DERECHA  (x: SPLIT → W)  — solo el producto
    # ═══════════════════════════════════════════════════════════════════

    prod_path = str(PRODS_DIR / "magistral/recursos/imagenes-producto/assets%2Ffdb4d79bfbfd478d89398007f8c29424%2F304711d179b94747a8bebe75d6abe295.webp")

    if os.path.exists(prod_path):
        prod   = Image.open(prod_path).convert("RGBA")
        prod   = remove_bg(prod, thr=228)
        prod   = add_glow(prod, color=(22, 90, 170), blur=36)

        # Escalar: que quepa en la columna derecha con margen
        col_w = W - SPLIT
        col_h = H - 140
        ratio = min((col_w - 40) / prod.width, col_h / prod.height)
        nw    = int(prod.width  * ratio)
        nh    = int(prod.height * ratio)
        prod  = prod.resize((nw, nh), Image.LANCZOS)

        # Centrar en columna derecha
        px = SPLIT + (col_w - nw) // 2
        py = (H - 70 - nh) // 2 + 20
        canvas.alpha_composite(prod, (px, py))
    else:
        draw.text((SPLIT + 30, 400), "⚠️ Imagen\nno encontrada",
                  font=font(30, IDX_BOLD), fill=NAVY)

    # ═══════════════════════════════════════════════════════════════════
    # FOOTER
    # ═══════════════════════════════════════════════════════════════════
    draw.rectangle([0, H - 68, W, H], fill=(*FOOTER_BG, 255))
    f_ft = font(19, IDX_REG)
    ft   = "immunotec.com  •  SAW PALMETTO (SERENOA)  •  SUPLEMENTO DIETÉTICO  •  CLEAN LABEL CERTIFIED"
    bb   = draw.textbbox((0, 0), ft, font=f_ft)
    fw   = bb[2] - bb[0]
    draw.text(((W - fw) // 2, H - 68 + 24), ft, font=f_ft, fill=FOOTER_TEXT)

    # ── Guardar ───────────────────────────────────────────────────────────────
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUTPUT_DIR / "magistral_ad_ingredientes.png"
    canvas.convert("RGB").save(str(out), "PNG", quality=95)
    print(f"✓ {out}")


if __name__ == "__main__":
    main()
