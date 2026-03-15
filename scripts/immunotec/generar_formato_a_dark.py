"""
Formato A — "Atención Directa"
Fondo azul navy profundo, headline grande en blanco, producto con glow.
Inspirado en el estilo CalmAlive Senior (referencia de Martin).
Salida: magistral_formato_a.png en Creativos nuevos para test/
"""

import math
import os
import sys
from pathlib import Path

try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
except ImportError:
    print("ERROR: pip3 install Pillow")
    sys.exit(1)

BASE_DIR  = Path(__file__).parent.parent.parent.parent
PRODS_DIR = BASE_DIR / "projects/immunotec/fase-1-embudos-por-producto/productos"
OUT_DIR   = PRODS_DIR / "magistral/Creativos nuevos para test"
FONT      = "/System/Library/Fonts/HelveticaNeue.ttc"

IDX_BLACK  = 9
IDX_BOLD   = 1
IDX_MEDIUM = 10
IDX_REG    = 0

# ── Paleta ────────────────────────────────────────────────────────────────────
BG_TOP    = (8,  28,  65)     # navy profundo
BG_BOT    = (13, 58, 110)     # navy más claro (gradiente)
CYAN      = (0, 185, 220)     # badge "LANZAMIENTO"
WHITE     = (255, 255, 255)
LIGHT_BLUE= (160, 210, 255)   # subtexto suave
GREEN     = (46, 200, 90)     # checkmark
GOLD      = (255, 210, 80)    # sello / award
DARK_NAVY = (5, 18, 45)       # sombra sello


def font(size, idx=IDX_REG):
    return ImageFont.truetype(FONT, size, index=idx)


def v_gradient(img, top, bot):
    """Rellena img con gradiente vertical de top a bot."""
    w, h = img.size
    draw = ImageDraw.Draw(img)
    for y in range(h):
        t = y / h
        r = int(top[0] + (bot[0] - top[0]) * t)
        g = int(top[1] + (bot[1] - top[1]) * t)
        b = int(top[2] + (bot[2] - top[2]) * t)
        draw.line([(0, y), (w, y)], fill=(r, g, b, 255))


def remove_bg(img, thr=215):
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


def add_glow(img, color=(0, 140, 200), blur=32):
    alpha   = img.split()[3]
    col_img = Image.new("RGBA", img.size, (*color, 200))
    col_img.putalpha(alpha)
    for _ in range(5):
        col_img = col_img.filter(ImageFilter.GaussianBlur(blur // 5))
    return Image.alpha_composite(col_img, img)


def pill(draw, xy, r, fill=None, border=None, bw=0):
    draw.rounded_rectangle(xy, radius=r, fill=fill, outline=border, width=bw)


def text_cx(draw, text, cx, y, fnt, fill):
    bb = draw.textbbox((0, 0), text, font=fnt)
    w  = bb[2] - bb[0]
    draw.text((cx - w // 2, y), text, font=fnt, fill=fill)


def draw_award_seal(canvas, cx, cy, r=88):
    """Sello holográfico tipo medalla — estilo del reference."""
    draw = ImageDraw.Draw(canvas)

    # Anillos exteriores
    for i, (radius, alpha) in enumerate([(r, 60), (r - 14, 90), (r - 26, 120)]):
        col = (*CYAN, alpha)
        draw.ellipse(
            [cx - radius, cy - radius, cx + radius, cy + radius],
            outline=col, width=3
        )

    # Puntas de la estrella
    n_points = 16
    for i in range(n_points):
        angle = math.radians(360 / n_points * i - 90)
        x1 = cx + int((r - 8) * math.cos(angle))
        y1 = cy + int((r - 8) * math.sin(angle))
        x2 = cx + int((r + 6) * math.cos(angle))
        y2 = cy + int((r + 6) * math.sin(angle))
        draw.line([(x1, y1), (x2, y2)], fill=(*CYAN, 180), width=2)

    # Relleno del sello
    draw.ellipse(
        [cx - r + 28, cy - r + 28, cx + r - 28, cy + r - 28],
        fill=(*DARK_NAVY, 240)
    )

    # Checkmark en el sello
    f_check = font(54, IDX_BOLD)
    text_cx(draw, "OK", cx, cy - 34, f_check, CYAN)

    # Texto dentro
    f_seal = font(14, IDX_BOLD)
    text_cx(draw, "CERTIFICADO", cx, cy + 24, f_seal, (*CYAN, 230))
    text_cx(draw, "IMMUNOTEC", cx, cy + 42, f_seal, (*WHITE, 200))


def draw_pedestal(canvas, cx, y_base, width=260, height=40):
    """Pequeño pedestal debajo del producto."""
    draw = ImageDraw.Draw(canvas)
    x1 = cx - width // 2
    x2 = cx + width // 2
    # Gradiente del pedestal (simulado con capas)
    for i in range(height):
        t = i / height
        r = int(0 + (40 - 0) * t)
        g = int(120 + (180 - 120) * t)
        b = int(200 + (240 - 200) * t)
        alpha = int(200 * (1 - t * 0.5))
        draw.line([(x1, y_base + i), (x2, y_base + i)], fill=(r, g, b, alpha))
    # Reflejo superior del pedestal
    draw.line([(x1, y_base), (x2, y_base)], fill=(*WHITE, 120), width=2)


def main():
    W, H = 1080, 1080

    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    v_gradient(canvas, (*BG_TOP, 255), (*BG_BOT, 255))
    draw = ImageDraw.Draw(canvas)

    # ── Brillo radial sutil al centro (atmósfera) ──────────────────────────────
    glow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gd = ImageDraw.Draw(glow_layer)
    for radius in range(420, 0, -4):
        alpha = int(30 * (1 - radius / 420))
        gd.ellipse(
            [W // 2 - radius, H // 2 - radius,
             W // 2 + radius, H // 2 + radius],
            fill=(20, 80, 160, alpha)
        )
    canvas = Image.alpha_composite(canvas, glow_layer)
    draw = ImageDraw.Draw(canvas)

    # ══════════════════════════════════════════════════════════════════════════
    # BADGE "LANZAMIENTO" — arriba izquierda
    # ══════════════════════════════════════════════════════════════════════════
    f_badge = font(28, IDX_BOLD)
    badge_txt = "  ◆ Lanzamiento  "
    bb = draw.textbbox((0, 0), badge_txt, font=f_badge)
    bw = bb[2] - bb[0] + 24
    bh = bb[3] - bb[1] + 16
    pill(draw, [38, 36, 38 + bw, 36 + bh], 22, CYAN)
    draw.text((38 + 12, 36 + 8), badge_txt, font=f_badge, fill=DARK_NAVY)

    # ══════════════════════════════════════════════════════════════════════════
    # NOMBRE DE MARCA — centrado arriba
    # ══════════════════════════════════════════════════════════════════════════
    f_brand = font(30, IDX_BOLD)
    text_cx(draw, "Magistral® de Immunotec", W // 2, 110, f_brand, (*LIGHT_BLUE, 230))

    # ══════════════════════════════════════════════════════════════════════════
    # HEADLINE PRINCIPAL — 3 líneas, centrado, blanco, condensed black
    # ══════════════════════════════════════════════════════════════════════════
    headline_lines = [
        "LA FÓRMULA",
        "PARA LA PRÓSTATA",
        "DESPUÉS DE LOS 40",
    ]
    f_h1 = font(120, IDX_BLACK)
    f_h2 = font(100, IDX_BLACK)
    f_h3 = font(90,  IDX_BLACK)
    fonts_h = [f_h1, f_h2, f_h3]
    ys_h    = [155, 278, 388]

    for line, fnt, y in zip(headline_lines, fonts_h, ys_h):
        # Sombra
        text_cx(draw, line, W // 2 + 3, y + 3, fnt, (0, 0, 0, 100))
        # Texto
        text_cx(draw, line, W // 2, y, fnt, WHITE)

    # ══════════════════════════════════════════════════════════════════════════
    # SELLO AWARD — izquierda medio
    # ══════════════════════════════════════════════════════════════════════════
    draw_award_seal(canvas, cx=135, cy=680, r=90)
    draw = ImageDraw.Draw(canvas)

    # ══════════════════════════════════════════════════════════════════════════
    # PRODUCTO — centro
    # ══════════════════════════════════════════════════════════════════════════
    prod_path = str(
        PRODS_DIR / "magistral/recursos/imagenes-producto/"
        "assets%2Ffdb4d79bfbfd478d89398007f8c29424%2F304711d179b94747a8bebe75d6abe295.webp"
    )

    PROD_CX = W // 2 + 20
    PROD_Y_BASE = H - 120

    if os.path.exists(prod_path):
        prod  = Image.open(prod_path).convert("RGBA")
        prod  = remove_bg(prod, thr=215)
        prod  = add_glow(prod, color=(0, 140, 200), blur=40)

        max_h = int(H * 0.56)
        max_w = 380
        ratio = min(max_w / prod.width, max_h / prod.height)
        nw    = int(prod.width  * ratio)
        nh    = int(prod.height * ratio)
        prod  = prod.resize((nw, nh), Image.LANCZOS)

        px = PROD_CX - nw // 2
        py = PROD_Y_BASE - nh
        canvas.alpha_composite(prod, (px, py))
        draw = ImageDraw.Draw(canvas)

        # Pedestal bajo el producto
        draw_pedestal(canvas, PROD_CX, py + nh - 6, width=nw + 40, height=38)
        draw = ImageDraw.Draw(canvas)

        # Sombra suave bajo pedestal
        shadow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        sd = ImageDraw.Draw(shadow)
        sd.ellipse(
            [PROD_CX - 160, py + nh + 24,
             PROD_CX + 160, py + nh + 58],
            fill=(0, 0, 0, 80)
        )
        shadow = shadow.filter(ImageFilter.GaussianBlur(14))
        canvas = Image.alpha_composite(canvas, shadow)
        draw = ImageDraw.Draw(canvas)
    else:
        draw.text((PROD_CX - 80, 500), "⚠️ Sin imagen", font=font(30, IDX_BOLD), fill=WHITE)

    # ══════════════════════════════════════════════════════════════════════════
    # TEXTO DERECHO — "Fórmula líquida…" + checkmark verde
    # ══════════════════════════════════════════════════════════════════════════
    RX = 870
    RY = 600
    f_rt = font(32, IDX_BOLD)
    f_rs = font(28, IDX_MEDIUM)

    # Líneas de texto derecho
    right_lines = ["Fórmula líquida", "optimizada para", "hombres 40+"]
    for i, line in enumerate(right_lines):
        text_cx(draw, line, RX, RY + i * 38, f_rs, (*LIGHT_BLUE, 240))

    # Checkmark verde con pill
    check_y = RY + len(right_lines) * 38 + 16
    pill(draw, [RX - 32, check_y, RX + 32, check_y + 44], 22, GREEN)
    f_chk = font(30, IDX_BOLD)
    text_cx(draw, "✓", RX, check_y + 6, f_chk, WHITE)

    # ══════════════════════════════════════════════════════════════════════════
    # FOOTER — franja azul oscura
    # ══════════════════════════════════════════════════════════════════════════
    draw.rectangle([0, H - 72, W, H], fill=(*DARK_NAVY, 240))
    f_ft = font(22, IDX_REG)
    ft   = "immunotec.com  •  SAW PALMETTO  •  FÓRMULA LÍQUIDA  •  SUPLEMENTO DIETÉTICO"
    bb   = draw.textbbox((0, 0), ft, font=f_ft)
    fw   = bb[2] - bb[0]
    draw.text(((W - fw) // 2, H - 72 + 22), ft, font=f_ft, fill=(*LIGHT_BLUE, 200))

    # ── Guardar ───────────────────────────────────────────────────────────────
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / "magistral_formato_a.png"
    canvas.convert("RGB").save(str(out), "PNG", quality=95)
    print(f"✓ Guardado: {out}")


if __name__ == "__main__":
    main()
