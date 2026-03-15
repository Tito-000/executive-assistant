"""
Winning Ad — Magistral (Próstata)
Estilo: pregunta intrigante + badge de oferta + producto con glow + fondo teal oscuro
Inspirado en: formato winning ad Prostatricum (Italia)
Layout: headline arriba, producto derecha, figura izquierda, badge centro
"""

import os
import sys
import math
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

# Indices de la fuente
IDX_REG    = 0
IDX_BOLD   = 1
IDX_BLACK  = 9   # Condensed Black — el más pesado disponible

# ── Paleta (inspirada en el reference teal oscuro) ──────────────────────────
BG_TOP     = (5,  38,  52)    # teal muy oscuro
BG_BOT     = (8,  72,  88)    # teal medio
ACCENT     = (0,  195, 220)   # cyan brillante (glow, líneas)
WHITE      = (255, 255, 255)
CREAM      = (245, 240, 225)
ORANGE     = (230, 105,  20)  # naranja badge (como el reference)
ORANGE_LT  = (255, 180,  50)  # naranja claro para texto del badge
DARK_TEXT  = (10,  25,  35)


def font(size, idx=IDX_REG):
    return ImageFont.truetype(FONT, size, index=idx)


def remove_bg(img, thr=220):
    img = img.convert("RGBA")
    px = list(img.getdata())
    new = [(r, g, b, 0) if (r > thr and g > thr and b > thr) else (r, g, b, a)
           for r, g, b, a in px]
    img.putdata(new)
    return img


def add_glow(img, color=(0, 195, 220), blur=32):
    pad = blur * 2
    w, h = img.size
    canvas = Image.new("RGBA", (w + pad*2, h + pad*2), (0, 0, 0, 0))
    alpha = img.split()[3]
    col   = Image.new("RGBA", (w, h), (*color, 200))
    col.putalpha(alpha)
    canvas.paste(col, (pad, pad), col)
    canvas = canvas.filter(ImageFilter.GaussianBlur(blur))
    result = Image.new("RGBA", (w + pad*2, h + pad*2), (0, 0, 0, 0))
    result.alpha_composite(canvas)
    result.paste(img, (pad, pad), img)
    return result.crop((pad, pad, pad + w, pad + h))


def draw_gradient_bg(canvas, w, h):
    """Degradado vertical teal oscuro → teal medio."""
    draw = ImageDraw.Draw(canvas)
    for y in range(h):
        t  = y / h
        r  = int(BG_TOP[0] + (BG_BOT[0] - BG_TOP[0]) * t)
        g  = int(BG_TOP[1] + (BG_BOT[1] - BG_TOP[1]) * t)
        b  = int(BG_TOP[2] + (BG_BOT[2] - BG_TOP[2]) * t)
        draw.line([(0, y), (w, y)], fill=(r, g, b))


def draw_light_rays(canvas, w, h):
    """Rayos de luz diagonales sutiles (como el reference)."""
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw    = ImageDraw.Draw(overlay)
    # 3 rayos diagonales desde esquina inferior izquierda
    origin = (0, h)
    targets = [(w * 0.35, 0), (w * 0.65, 0), (w * 0.90, 0)]
    widths  = [160, 120, 80]
    alphas  = [18, 12, 8]
    for (tx, ty), rw, alpha in zip(targets, widths, alphas):
        draw.polygon([
            (origin[0] - rw//2, origin[1]),
            (origin[0] + rw//2, origin[1]),
            (tx + rw//2, ty),
            (tx - rw//2, ty),
        ], fill=(255, 255, 255, alpha))
    # Blur para suavizar
    overlay = overlay.filter(ImageFilter.GaussianBlur(40))
    canvas.alpha_composite(overlay)


def draw_starburst_badge(draw, cx, cy, r_outer, r_inner, n_points, fill):
    """Dibuja el badge de estrella (como el reference) usando polígono de picos."""
    points = []
    for i in range(n_points * 2):
        angle  = math.pi / n_points * i - math.pi / 2
        r = r_outer if i % 2 == 0 else r_inner
        points.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    draw.polygon(points, fill=fill)


def text_center(draw, text, cx, y, fnt, fill, shadow=False):
    bb = draw.textbbox((0, 0), text, font=fnt)
    w  = bb[2] - bb[0]
    if shadow:
        draw.text((cx - w//2 + 3, y + 3), text, font=fnt, fill=(0, 0, 0, 100))
    draw.text((cx - w//2, y), text, font=fnt, fill=fill)


def wrap_text(text, max_w, draw, fnt):
    """Divide texto en líneas que quepan en max_w px."""
    words = text.split()
    lines, current = [], ""
    for word in words:
        test = (current + " " + word).strip()
        bb   = draw.textbbox((0, 0), test, font=fnt)
        if bb[2] - bb[0] <= max_w:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_headline(canvas, draw, w):
    """Dibuja el headline principal — pregunta que para el scroll."""
    # Línea decorativa cyan arriba
    draw.rectangle([50, 52, w - 50, 58], fill=(*ACCENT, 200))

    # Headline: 2 líneas en itálica negra
    # Línea 1 — pequeña
    f_tag = font(32, IDX_BOLD)
    draw.text((58, 68), "¿POR QUÉ ÉL LO AGUANTÓ", font=f_tag, fill=(*ACCENT, 255))

    # Línea grande — impacto total
    f_h1 = font(102, IDX_BLACK)
    line1 = "400 AÑOS"
    bb1   = draw.textbbox((0, 0), line1, font=f_h1)
    # Sombra
    draw.text((58 + 4, 102 + 4), line1, font=f_h1, fill=(0, 0, 0, 120))
    draw.text((58, 102), line1, font=f_h1, fill=WHITE)

    # Línea complementaria
    f_h2  = font(56, IDX_BLACK)
    line2 = "SIN PARAR?"
    draw.text((58 + 3, 205 + 3), line2, font=f_h2, fill=(0, 0, 0, 100))
    draw.text((58, 205), line2, font=f_h2, fill=(*ACCENT, 255))

    # Subtítulo
    f_sub = font(30, IDX_BOLD)
    sub   = "Tu próstata lleva años gritando — hoy puedes escucharla."
    lines = wrap_text(sub, w - 120, draw, f_sub)
    sy = 278
    for ln in lines:
        draw.text((58, sy), ln, font=f_sub, fill=(*CREAM, 230))
        sy += 40


def draw_badge(canvas, draw, cx, cy):
    """Badge naranja estilo starburst (como el reference)."""
    # Starburst exterior
    draw_starburst_badge(draw, cx, cy, 105, 80, 14, fill=ORANGE)
    # Círculo interior
    draw.ellipse([cx - 75, cy - 75, cx + 75, cy + 75], fill=ORANGE)
    # Texto
    f_big  = font(36, IDX_BLACK)
    f_sm   = font(22, IDX_BOLD)
    f_tiny = font(18, IDX_BOLD)
    text_center(draw, "PRECIO",  cx, cy - 52, f_tiny, ORANGE_LT)
    text_center(draw, "ESPECIAL", cx, cy - 30, f_sm,  WHITE)
    # Precio tachado
    f_cross = font(22, IDX_REG)
    text_center(draw, "RD$7,300", cx, cy + 2,  f_cross, (255, 220, 180))
    bb = draw.textbbox((0, 0), "RD$7,300", font=f_cross)
    bw = bb[2] - bb[0]
    draw.line([(cx - bw//2, cy + 14), (cx + bw//2, cy + 14)], fill=WHITE, width=2)
    # Precio final
    f_price = font(38, IDX_BLACK)
    text_center(draw, "RD$5,840", cx, cy + 28, f_price, ORANGE_LT)
    text_center(draw, "HOY",     cx, cy + 70, f_sm, WHITE)


def draw_bottom_strip(draw, w, h):
    """Franja inferior con propuesta de valor."""
    strip_h = 72
    draw.rectangle([0, h - strip_h, w, h], fill=(0, 0, 0, 200))
    f_ft = font(22, IDX_BOLD)
    items = ["✓ PAGO AL RECIBIR", "✓ ENTREGA 24-72H", "✓ SAW PALMETTO", "✓ FÓRMULA LÍQUIDA"]
    total_w = sum(draw.textbbox((0, 0), it, font=f_ft)[2] for it in items) + (len(items) - 1) * 40
    x = (w - total_w) // 2
    y = h - strip_h + (strip_h - 26) // 2
    for i, item in enumerate(items):
        bb = draw.textbbox((0, 0), item, font=f_ft)
        iw = bb[2] - bb[0]
        # Alternar color
        clr = ACCENT if i % 2 == 0 else WHITE
        draw.text((x, y), item, font=f_ft, fill=clr)
        x += iw + 40


def main():
    W, H = 1080, 1080

    # Crear canvas base
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 255))

    # 1. Fondo degradado
    draw_gradient_bg(canvas, W, H)

    # 2. Rayos de luz
    draw_light_rays(canvas, W, H)

    draw = ImageDraw.Draw(canvas)

    # 3. Headline (arriba izquierda)
    draw_headline(canvas, draw, W)

    # 4. Producto (derecha, grande)
    prod_path = PRODS_DIR / "magistral/recursos/imagenes-producto/assets%2Ffdb4d79bfbfd478d89398007f8c29424%2F304711d179b94747a8bebe75d6abe295.webp"
    if prod_path.exists():
        prod  = Image.open(str(prod_path)).convert("RGBA")
        prod  = remove_bg(prod, thr=225)
        prod  = add_glow(prod, color=(0, 195, 220), blur=36)
        # Escalar para lado derecho
        target_h = int(H * 0.72)
        target_w = int(W * 0.46)
        ratio    = min(target_w / prod.width, target_h / prod.height)
        nw       = int(prod.width  * ratio)
        nh       = int(prod.height * ratio)
        prod     = prod.resize((nw, nh), Image.LANCZOS)
        # Posición: derecha, centrado verticalmente en zona media-baja
        px = W - nw - 20
        py = (H - nh) // 2 + 60
        canvas.alpha_composite(prod, (px, py))
    else:
        draw.text((600, 400), "⚠️ imagen no encontrada", font=font(30, IDX_BOLD), fill=WHITE)

    # 5. Badge de oferta (centro-izquierda, sobre la zona media)
    draw_badge(canvas, draw, 230, 680)

    # 6. Línea divisora sutil entre headline y zona media
    draw.rectangle([50, 335, W // 2 + 80, 339], fill=(*ACCENT, 80))

    # 7. Copy apoyo (debajo del badge)
    f_copy = font(27, IDX_BOLD)
    copy_lines = [
        "Magistral apoya la salud prostática",
        "con Saw Palmetto — más rápido",
        "que cualquier cápsula del mercado.",
    ]
    cy = 790
    for line in copy_lines:
        draw.text((58, cy), line, font=f_copy, fill=(*CREAM, 210))
        cy += 38

    # 8. Franja inferior
    draw_bottom_strip(draw, W, H)

    # ── Guardar ───────────────────────────────────────────────────────────────
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUTPUT_DIR / "magistral_winning_ad.png"
    canvas.convert("RGB").save(str(out), "PNG", quality=95)
    print(f"✓ Guardado: {out}")


if __name__ == "__main__":
    main()
