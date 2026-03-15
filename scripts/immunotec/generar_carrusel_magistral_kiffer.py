"""
Carrusel Magistral — estilo Kiffer / fondo negro
4 slides: Hook+Producto, ¿Qué es?, ¿Para qué sirve?, ¿Cuándo sentir la diferencia?
Pure Pillow — sin IA, $0 costo, control total.
"""

from pathlib import Path
try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
except ImportError:
    raise SystemExit("ERROR: pip3 install Pillow")

# ── Rutas ─────────────────────────────────────────────────────────────────────
BASE     = Path("/Users/martinmercedes/Desktop/Executive assistant 2")
PROD_DIR = BASE / "projects/immunotec/fase-1-embudos-por-producto/productos/magistral"
OUT_DIR  = PROD_DIR / "Creativos nuevos para test/carrusel-kiffer-v1"
PROD_IMG = PROD_DIR / "recursos/imagenes-producto/assets%2Ffdb4d79bfbfd478d89398007f8c29424%2F304711d179b94747a8bebe75d6abe295.webp"
FONT     = "/System/Library/Fonts/HelveticaNeue.ttc"

# Índices TTC
IDX_REG   = 0
IDX_BOLD  = 1
IDX_BLACK = 9   # Condensed Black

# ── Paleta ────────────────────────────────────────────────────────────────────
BG         = (8,   8,   8)
WHITE      = (255, 255, 255)
GRAY       = (175, 175, 175)
DARK_LINE  = (45,  45,  45)
FOOTER_BG  = (18,  18,  18)

W, H = 1080, 1080


# ── Helpers ───────────────────────────────────────────────────────────────────
def fnt(size, idx=IDX_REG):
    return ImageFont.truetype(FONT, size, index=idx)


def text_h(draw, text, f):
    bb = draw.textbbox((0, 0), text, font=f)
    return bb[3] - bb[1]


def draw_footer(draw, left="MAGISTRAL", right="IMMUNOTEC"):
    draw.rectangle([0, H - 64, W, H], fill=FOOTER_BG)
    draw.rectangle([0, H - 65, W, H - 64], fill=DARK_LINE)
    f = fnt(22, IDX_BOLD)
    draw.text((50, H - 43), left,  font=f, fill=GRAY)
    bb = draw.textbbox((0, 0), right, font=f)
    draw.text((W - 50 - (bb[2] - bb[0]), H - 43), right, font=f, fill=WHITE)


def wrap(draw, text, max_w, f):
    """Word-wrap text, returns list of lines."""
    words  = text.split()
    lines  = []
    cur    = ""
    for w in words:
        test = (cur + " " + w).strip()
        bb = draw.textbbox((0, 0), test, font=f)
        if bb[2] - bb[0] <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def remove_bg(img, thr=228):
    img = img.convert("RGBA")
    data = [(r, g, b, 0) if r > thr and g > thr and b > thr else (r, g, b, a)
            for r, g, b, a in img.getdata()]
    img.putdata(data)
    return img


def add_glow(img, color=(200, 215, 255), radius=30):
    alpha = img.split()[3]
    ci = Image.new("RGBA", img.size, (*color, 150))
    ci.putalpha(alpha)
    for _ in range(5):
        ci = ci.filter(ImageFilter.GaussianBlur(radius // 5))
    return Image.alpha_composite(ci, img)


def dot(draw, cx, cy, r, c=DARK_LINE):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c)


def draw_arrow(draw, x, y, line_h, color=WHITE):
    """Flecha → dibujada con Pillow (no depende del font)."""
    cy  = y + line_h // 2
    tip = x + 38
    # Línea horizontal
    draw.line([(x, cy), (tip - 10, cy)], fill=color, width=3)
    # Cabeza de flecha
    pts = [(tip - 12, cy - 9), (tip, cy), (tip - 12, cy + 9)]
    draw.polygon(pts, fill=color)


# ── Slide 01 — Hook + Producto ────────────────────────────────────────────────
def slide_01():
    img    = Image.new("RGBA", (W, H), (*BG, 255))
    draw   = ImageDraw.Draw(img)
    PAD    = 60
    SPLIT  = 540   # columna izquierda max x

    # Producto — columna derecha
    if PROD_IMG.exists():
        prod = Image.open(PROD_IMG).convert("RGBA")
        prod = remove_bg(prod)
        prod = add_glow(prod)
        max_w, max_h = W - SPLIT - 20, H - 80
        r  = min(max_w / prod.width, max_h / prod.height)
        nw = int(prod.width * r)
        nh = int(prod.height * r)
        prod = prod.resize((nw, nh), Image.LANCZOS)
        px  = SPLIT + (W - SPLIT - nw) // 2
        py  = (H - 64 - nh) // 2
        img.alpha_composite(prod, (px, py))
        draw = ImageDraw.Draw(img)

    # Headline izquierda
    f_h   = fnt(94, IDX_BLACK)
    lines = ["¿POR QUÉ", "TE LEVANTAS", "AL BAÑO", "3 VECES", "POR NOCHE?"]
    y = 100
    for line in lines:
        draw.text((PAD, y), line, font=f_h, fill=WHITE)
        y += text_h(draw, line, f_h) + 8

    # Sub-copy
    f_sub = fnt(33, IDX_REG)
    draw.text((PAD, y + 18), "Esto no es solo la edad.", font=f_sub, fill=GRAY)
    draw.text((PAD, y + 58), "Tu próstata necesita apoyo.", font=f_sub, fill=GRAY)

    # Decoración
    dot(draw, 970, 90,  4)
    dot(draw, 1010, 140, 6)
    dot(draw, 1040, 85,  2)

    draw_footer(draw)
    return img.convert("RGB")


# ── Slide 02 — ¿Qué es? ───────────────────────────────────────────────────────
def slide_02():
    img  = Image.new("RGBA", (W, H), (*BG, 255))
    draw = ImageDraw.Draw(img)
    PAD  = 80

    # Decoración puntual
    dot(draw,  90,  85, 10)
    dot(draw, 950,  90,  9)
    dot(draw, 200, 155,  5)
    dot(draw, 1010, 200,  4)
    dot(draw,  80, 480,  4)
    dot(draw, 975, 860,  7)

    # Título
    f_title = fnt(118, IDX_BLACK)
    draw.text((PAD, 90), "¿QUÉ ES?", font=f_title, fill=WHITE)

    # Cuerpo — 3 párrafos
    f_b   = fnt(37, IDX_REG)
    MAX_W = W - PAD * 2
    paras = [
        "Magistral es un suplemento líquido formulado con Saw Palmetto (Serenoa repens), "
        "la planta más estudiada para la salud de la próstata.",

        "A diferencia de las cápsulas, su fórmula líquida permite una absorción más rápida "
        "— con resultados notables desde los primeros días.",

        "Fabricado por Immunotec con más de 30 años de respaldo clínico. "
        "Natural. Sin pastillas. Sin procedimientos invasivos.",
    ]
    y = 275
    for para in paras:
        for line in wrap(draw, para, MAX_W, f_b):
            draw.text((PAD, y), line, font=f_b, fill=(215, 215, 215))
            y += text_h(draw, line, f_b) + 7
        y += 30   # espacio entre párrafos

    draw_footer(draw)
    return img.convert("RGB")


# ── Slide 03 — ¿Para qué sirve? ───────────────────────────────────────────────
def slide_03():
    img  = Image.new("RGBA", (W, H), (*BG, 255))
    draw = ImageDraw.Draw(img)
    PAD  = 80

    # Título 2 líneas
    f_title = fnt(105, IDX_BLACK)
    draw.text((PAD, 75),  "¿PARA QUÉ", font=f_title, fill=WHITE)
    draw.text((PAD, 185), "SIRVE?",    font=f_title, fill=WHITE)

    # Beneficios
    benefits = [
        ("Reduce la urgencia y frecuencia urinaria",    "Fluye sin interrupciones"),
        ("Mejora el flujo y vacía la vejiga por completo", "Sin quedar a medias"),
        ("Devuelve el sueño sin levantarte de noche",   "Duerme de corrido"),
        ("Aumenta tu energía y vitalidad durante el día", "Activo desde la mañana"),
        ("Natural, sin efectos secundarios ni receta",  "Sin pastillas de por vida"),
    ]

    f_main  = fnt(34, IDX_BOLD)
    f_sub   = fnt(27, IDX_REG)

    y   = 340
    GAP = 132
    LH  = text_h(draw, "X", f_main) + 8   # line height for arrow centering

    for i, (main, sub) in enumerate(benefits):
        draw_arrow(draw, PAD, y, LH)
        draw.text((PAD + 58, y + 2),  main, font=f_main, fill=WHITE)
        mh = text_h(draw, main, f_main)
        draw.text((PAD + 58, y + mh + 6), sub, font=f_sub, fill=GRAY)

        if i < len(benefits) - 1:
            draw.rectangle([PAD, y + GAP - 12, W - PAD, y + GAP - 11], fill=DARK_LINE)
        y += GAP

    dot(draw, 990, 105, 6)
    draw_footer(draw)
    return img.convert("RGB")


# ── Slide 04 — ¿Cuándo empiezo a sentir la diferencia? ───────────────────────
def slide_04():
    img  = Image.new("RGBA", (W, H), (*BG, 255))
    draw = ImageDraw.Draw(img)
    PAD  = 72

    # Headline masivo
    f_h   = fnt(110, IDX_BLACK)
    lines = ["¿CUÁNDO", "EMPIEZO A", "SENTIR LA", "DIFERENCIA?"]
    y = 68
    for line in lines:
        draw.text((PAD, y), line, font=f_h, fill=WHITE)
        y += text_h(draw, line, f_h) + 5

    # Divisor
    y += 22
    draw.rectangle([PAD, y, W - PAD, y + 2], fill=(72, 72, 72))
    y += 28

    # Intro
    f_intro = fnt(36, IDX_REG)
    intro1 = "Entre 10 y 30 días de uso constante,"
    intro2 = "muchas personas reportan:"
    draw.text((PAD, y), intro1, font=f_intro, fill=(200, 200, 200))
    y += text_h(draw, intro1, f_intro) + 6
    draw.text((PAD, y), intro2, font=f_intro, fill=(200, 200, 200))
    y += text_h(draw, intro2, f_intro) + 30

    # Bullets con flecha
    results = [
        "Más energía en el día a día",
        "Mejor recuperación nocturna",
        "Mayor bienestar y estabilidad",
    ]
    f_res   = fnt(41, IDX_BOLD)
    LH4     = text_h(draw, "X", f_res) + 8
    for res in results:
        draw_arrow(draw, PAD, y, LH4)
        draw.text((PAD + 60, y), res, font=f_res, fill=WHITE)
        y += text_h(draw, res, f_res) + 15

    y += 26
    # Cierre itálico
    f_it = fnt(30, IDX_REG)
    draw.text((PAD, y), "Cada cuerpo es diferente.", font=f_it, fill=(118, 118, 118))
    y += text_h(draw, "x", f_it) + 7
    draw.text((PAD, y), "El proceso empieza desde adentro.", font=f_it, fill=(118, 118, 118))

    draw_footer(draw)
    return img.convert("RGB")


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    slides = [
        ("slide_01_hook.png",          slide_01),
        ("slide_02_que_es.png",        slide_02),
        ("slide_03_para_que_sirve.png", slide_03),
        ("slide_04_cuando.png",        slide_04),
    ]

    for name, gen in slides:
        print(f"  Generando {name}...")
        out = OUT_DIR / name
        gen().save(str(out), "PNG", quality=95)
        print(f"  ✓ {out}")

    print(f"\nCarrusel listo en:\n{OUT_DIR}")


if __name__ == "__main__":
    main()
