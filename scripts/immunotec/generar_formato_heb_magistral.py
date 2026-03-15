"""
Ad Formato H-E-B 1:1 — Magistral (Próstata)
Base: generada por Nano Banana via Kie.ai (magistral_heb_base_1x1.jpg)
Layout: hombre izquierda | columna derecha: headline + desc + beneficios + producto
"""

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

IDX_BLACK = 9
IDX_BOLD  = 1
IDX_REG   = 0

WHITE     = (255, 255, 255)
ORANGE    = (218, 88, 28)
GRAY      = (175, 195, 220)
SEP       = (60, 90, 145)
FOOTER_BG = (10, 20, 42)
BRAND_CLR = (130, 160, 205)

S = 1080   # canvas final cuadrado


def fnt(size, idx=IDX_REG):
    return ImageFont.truetype(FONT, size, index=idx)


def remove_bg(img, thr=220):
    img = img.convert("RGBA")
    px  = list(img.getdata())
    img.putdata([(r, g, b, 0) if (r > thr and g > thr and b > thr) else (r, g, b, a)
                 for r, g, b, a in px])
    return img


def add_glow(img, color=(100, 160, 240), blur=28):
    pad = blur * 2
    w, h = img.size
    bg  = Image.new("RGBA", (w + pad*2, h + pad*2), (0, 0, 0, 0))
    col = Image.new("RGBA", (w, h), (*color, 155))
    col.putalpha(img.split()[3])
    bg.paste(col, (pad, pad), col)
    bg  = bg.filter(ImageFilter.GaussianBlur(blur))
    out = Image.new("RGBA", (w + pad*2, h + pad*2), (0, 0, 0, 0))
    out.alpha_composite(bg)
    out.paste(img, (pad, pad), img)
    return out.crop((pad, pad, pad + w, pad + h))


def wrap(draw, text, max_w, f):
    words = text.split()
    lines, cur = [], ""
    for word in words:
        test = (cur + " " + word).strip()
        if draw.textbbox((0, 0), test, font=f)[2] <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def mixed_line(draw, x, y, parts):
    cx = x
    for text, fill, f in parts:
        draw.text((cx, y), text, font=f, fill=fill)
        bb = draw.textbbox((0, 0), text, font=f)
        cx += bb[2] - bb[0]


def lw(draw, parts):
    return sum(draw.textbbox((0,0), t, font=f)[2] - draw.textbbox((0,0), t, font=f)[0]
               for t, _, f in parts)


def crop_to_square(img):
    """Crop centrado al cuadrado más grande posible, luego resize a SxS."""
    w, h  = img.size
    side  = min(w, h)
    left  = (w - side) // 2
    top   = max(0, (h - side) // 4)   # ligero bias hacia arriba para no cortar la cabeza
    top   = min(top, h - side)
    img   = img.crop((left, top, left + side, top + side))
    return img.resize((S, S), Image.LANCZOS)


def main():
    base_path = OUTPUT_DIR / "magistral_heb_base_1x1.jpg"
    if not base_path.exists():
        print("ERROR: base no encontrada. Genera con Nano Banana primero.")
        sys.exit(1)

    base   = Image.open(str(base_path)).convert("RGBA")
    base   = crop_to_square(base)         # -> 1080x1080
    canvas = base.copy()
    W = H  = S

    # Columna derecha: empieza en ~47% del ancho
    RX  = int(W * 0.47)    # 507px
    PAD = RX + 14          # 521px — inicio de textos
    RW  = W - PAD - 22     # ~537px ancho disponible

    draw = ImageDraw.Draw(canvas)

    # Overlay semitransparente solo en columna derecha (mejora contraste)
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    od.rectangle([RX, 0, W, H], fill=(8, 18, 40, 130))
    ov = ov.filter(ImageFilter.GaussianBlur(20))
    canvas.alpha_composite(ov)
    draw = ImageDraw.Draw(canvas)

    # ── Marca top-right ───────────────────────────────────────────────────────
    f_br = fnt(19, IDX_BOLD)
    brand = "IMMUNOTEC®  MAGISTRAL"
    bb    = draw.textbbox((0, 0), brand, font=f_br)
    draw.text((W - (bb[2]-bb[0]) - 22, 20), brand, font=f_br, fill=BRAND_CLR)

    # ── Headline (2 líneas, font 40px — cabe en RW=537) ───────────────────────
    f_r  = fnt(40, IDX_BOLD)
    f_b  = fnt(40, IDX_BLACK)
    hl1  = [("Porque los ", WHITE, f_r), ("hombres fuertes", ORANGE, f_b)]
    hl2  = [("necesitan ", WHITE, f_r), ("apoyo real", ORANGE, f_b)]

    hl_y = 50
    mixed_line(draw, PAD, hl_y,      hl1)
    mixed_line(draw, PAD, hl_y + 50, hl2)

    # ── Separador ─────────────────────────────────────────────────────────────
    sep1_y = hl_y + 50 + 48
    draw.rectangle([PAD, sep1_y, W - 22, sep1_y + 2], fill=(*SEP, 160))

    # ── Descripción ───────────────────────────────────────────────────────────
    f_d  = fnt(22, IDX_REG)
    desc = ("Con Saw Palmetto, licopeno, selenio y zinc — "
            "formula liquida de alta absorcion para la salud masculina.")
    dy   = sep1_y + 12
    for line in wrap(draw, desc, RW, f_d):
        draw.text((PAD, dy), line, font=f_d, fill=GRAY)
        dy += 28

    # ── Separador ─────────────────────────────────────────────────────────────
    sep2_y = dy + 8
    draw.rectangle([PAD, sep2_y, W - 22, sep2_y + 2], fill=(*SEP, 160))

    # ── Beneficios bold ───────────────────────────────────────────────────────
    f_bn  = fnt(42, IDX_BLACK)
    ben_y = sep2_y + 14
    for ben in ["Salud prostatica", "Flujo urinario", "Vitalidad masculina"]:
        draw.text((PAD, ben_y), ben, font=f_bn, fill=WHITE)
        ben_y += 50

    # ── Producto ──────────────────────────────────────────────────────────────
    prod_path = PRODS_DIR / "magistral/recursos/imagenes-producto/Imagend el magistral .png"
    if prod_path.exists():
        prod    = Image.open(str(prod_path)).convert("RGBA")
        prod    = remove_bg(prod, thr=225)
        prod    = add_glow(prod, color=(100, 180, 240), blur=28)
        avail_h = H - ben_y - 95
        avail_w = RW
        ratio   = min(avail_w / prod.width, avail_h / prod.height, 0.56)
        nw, nh  = int(prod.width * ratio), int(prod.height * ratio)
        prod    = prod.resize((nw, nh), Image.LANCZOS)
        canvas.alpha_composite(prod, (PAD + (RW - nw) // 2, ben_y + 10))
    else:
        draw.text((PAD, ben_y + 10), "imagen no encontrada", font=fnt(20), fill=WHITE)

    draw = ImageDraw.Draw(canvas)

    # ── Footer ────────────────────────────────────────────────────────────────
    ft_y = H - 72
    draw.rectangle([0, ft_y, W, H], fill=(*FOOTER_BG, 248))
    f_ft = fnt(22, IDX_BOLD)
    cta  = "Disponible  ·  Pago al recibir  ·  Entrega a todo RD"
    bb   = draw.textbbox((0, 0), cta, font=f_ft)
    draw.text(((W - (bb[2]-bb[0])) // 2, ft_y + 22), cta, font=f_ft, fill=WHITE)

    # ── Guardar ───────────────────────────────────────────────────────────────
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUTPUT_DIR / "magistral_formato_heb_1x1.png"
    canvas.convert("RGB").save(str(out), "PNG", quality=95)
    print(f"Guardado: {out}  ({W}x{H})")


if __name__ == "__main__":
    main()
