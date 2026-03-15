"""
Carrusel Magistral — v2
Diseño con branding: fondo azul-negro profundo, azul Immunotec, glow ciánico, producto prominente.
"""
from pathlib import Path
try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
except ImportError:
    raise SystemExit("ERROR: pip3 install Pillow")

BASE     = Path("/Users/martinmercedes/Desktop/Executive assistant 2")
PROD_DIR = BASE / "projects/immunotec/fase-1-embudos-por-producto/productos/magistral"
OUT_DIR  = PROD_DIR / "Creativos nuevos para test/carrusel-kiffer-v2"
PROD_IMG = PROD_DIR / "recursos/imagenes-producto/assets%2Ffdb4d79bfbfd478d89398007f8c29424%2F304711d179b94747a8bebe75d6abe295.webp"
FONT     = "/System/Library/Fonts/HelveticaNeue.ttc"

IDX_REG   = 0
IDX_BOLD  = 1
IDX_BLACK = 9   # Condensed Black

# ── Paleta Immunotec/Magistral ────────────────────────────────────────────────
BG          = (5,   7,  15)    # azul-negro muy profundo
ACCENT      = (20, 110, 230)   # azul Immunotec
ACCENT_L    = (60, 160, 255)   # azul claro para highlights
CYAN        = (0,  200, 240)   # cian para glow del producto
WHITE       = (255, 255, 255)
GRAY        = (160, 170, 190)  # gris con tinte azul
DARK_CARD   = (10,  14,  28)   # tarjeta oscura
SEP         = (25,  40,  70)   # separador
FOOTER_BG   = (8,   10,  22)

W, H = 1080, 1080


# ── Utilidades ────────────────────────────────────────────────────────────────
def fnt(size, idx=IDX_REG):
    return ImageFont.truetype(FONT, size, index=idx)

def th(draw, text, f):
    bb = draw.textbbox((0, 0), text, font=f)
    return bb[3] - bb[1]

def tw(draw, text, f):
    bb = draw.textbbox((0, 0), text, font=f)
    return bb[2] - bb[0]

def wrap(draw, text, max_w, f):
    words, lines, cur = text.split(), [], ""
    for w in words:
        test = (cur + " " + w).strip()
        bb = draw.textbbox((0, 0), test, font=f)
        if bb[2] - bb[0] <= max_w:
            cur = test
        else:
            if cur: lines.append(cur)
            cur = w
    if cur: lines.append(cur)
    return lines

def remove_bg(img, thr=222):
    img = img.convert("RGBA")
    data = [(r, g, b, 0) if r > thr and g > thr and b > thr else (r, g, b, a)
            for r, g, b, a in img.getdata()]
    img.putdata(data)
    return img

def canvas_glow(canvas, cx, cy, radius, color, opacity=110):
    """Pinta un glow radial suave en el canvas."""
    g = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(g)
    for r in range(radius, 0, -30):
        a = int(opacity * (1 - r / radius) ** 1.4)
        gd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(*color, a))
    g = g.filter(ImageFilter.GaussianBlur(50))
    return Image.alpha_composite(canvas, g)

def pill(draw, xy, r, fill, border=None, bw=2):
    draw.rounded_rectangle(xy, radius=r, fill=fill, outline=border, width=bw)

def draw_arrow(draw, x, y, lh, color=WHITE):
    cy  = y + lh // 2 + 2
    tip = x + 36
    draw.line([(x, cy), (tip - 10, cy)], fill=color, width=3)
    draw.polygon([(tip - 12, cy - 8), (tip, cy), (tip - 12, cy + 8)], fill=color)

def draw_footer(draw, left="MAGISTRAL", right="IMMUNOTEC"):
    # Línea acento azul
    draw.rectangle([0, H - 66, W, H - 63], fill=ACCENT)
    draw.rectangle([0, H - 63, W, H], fill=FOOTER_BG)
    f = fnt(22, IDX_BOLD)
    draw.text((50, H - 44), left,  font=f, fill=(*GRAY, 255))
    rw = tw(draw, right, f)
    draw.text((W - 50 - rw, H - 44), right, font=f, fill=WHITE)

def load_product(max_w, max_h, thr=222):
    if not PROD_IMG.exists():
        return None
    prod = Image.open(PROD_IMG).convert("RGBA")
    prod = remove_bg(prod, thr)
    r  = min(max_w / prod.width, max_h / prod.height)
    nw = int(prod.width  * r)
    nh = int(prod.height * r)
    return prod.resize((nw, nh), Image.LANCZOS)


# ── SLIDE 01 — Hook + Producto ────────────────────────────────────────────────
def slide_01():
    img  = Image.new("RGBA", (W, H), (*BG, 255))

    # Glow ciánico donde irá el producto (columna derecha)
    img = canvas_glow(img, cx=790, cy=480, radius=380, color=CYAN, opacity=90)
    # Segundo glow azul más suave
    img = canvas_glow(img, cx=800, cy=500, radius=260, color=ACCENT_L, opacity=70)

    draw = ImageDraw.Draw(img)

    # Línea vertical divisoria sutil
    draw.rectangle([520, 50, 522, H - 80], fill=(*SEP, 200))

    # ── Producto — columna derecha ──
    prod = load_product(max_w=480, max_h=860)
    if prod:
        nw, nh = prod.size
        px = 525 + (555 - nw) // 2
        py = (H - 66 - nh) // 2
        img.alpha_composite(prod, (max(px, 525), max(py, 20)))
        draw = ImageDraw.Draw(img)

    # ── Badge "SUPLEMENTO LÍQUIDO" ──
    PAD = 55
    f_badge = fnt(20, IDX_BOLD)
    badge_txt = "SUPLEMENTO LÍQUIDO"
    bw = tw(draw, badge_txt, f_badge) + 32
    pill(draw, [PAD, 48, PAD + bw, 48 + 36], 18, ACCENT, border=ACCENT_L, bw=1)
    draw.text((PAD + 16, 54), badge_txt, font=f_badge, fill=WHITE)

    # ── Headline ──
    f_h = fnt(92, IDX_BLACK)
    lines = [
        ("¿POR QUÉ",    WHITE),
        ("TE LEVANTAS", WHITE),
        ("AL BAÑO",     WHITE),
        ("3 VECES",     ACCENT_L),   # número destacado en azul
        ("POR NOCHE?",  WHITE),
    ]
    y = 105
    for text, color in lines:
        draw.text((PAD, y), text, font=f_h, fill=color)
        y += th(draw, text, f_h) + 8

    # ── Sub-copy ──
    f_sub = fnt(31, IDX_REG)
    draw.text((PAD, y + 16), "Esto no es solo la edad.", font=f_sub, fill=GRAY)
    draw.text((PAD, y + 52), "Tu próstata necesita apoyo.", font=f_sub, fill=GRAY)

    draw_footer(draw)
    return img.convert("RGB")


# ── SLIDE 02 — ¿Qué es? ───────────────────────────────────────────────────────
def slide_02():
    img  = Image.new("RGBA", (W, H), (*BG, 255))
    # Glow sutil esquina superior derecha
    img = canvas_glow(img, cx=1000, cy=80, radius=200, color=ACCENT, opacity=50)
    draw = ImageDraw.Draw(img)
    PAD  = 80

    # ── Título con barra de acento ──
    f_title = fnt(116, IDX_BLACK)
    draw.text((PAD, 82), "¿QUÉ ES?", font=f_title, fill=WHITE)
    title_w = tw(draw, "¿QUÉ ES?", f_title)
    # Barra azul bajo el título
    draw.rectangle([PAD, 82 + 115, PAD + title_w, 82 + 120], fill=ACCENT)

    # ── Cuerpo ──
    f_b   = fnt(37, IDX_REG)
    f_bb  = fnt(37, IDX_BOLD)
    MAX_W = W - PAD * 2

    paras = [
        ("Magistral es un suplemento líquido formulado con "
         "Saw Palmetto (Serenoa repens), la planta más "
         "estudiada para la salud de la próstata.", False),

        ("A diferencia de las cápsulas, su fórmula líquida "
         "permite una absorción más rápida — con resultados "
         "notables desde los primeros días.", True),   # bold = highlight

        ("Fabricado por Immunotec con más de 30 años de "
         "respaldo clínico. Natural. Sin pastillas. "
         "Sin procedimientos invasivos.", False),
    ]
    y = 275
    for para, bold in paras:
        f = f_bb if bold else f_b
        color = WHITE if bold else (215, 218, 228)
        for line in wrap(draw, para, MAX_W, f):
            draw.text((PAD, y), line, font=f, fill=color)
            y += th(draw, line, f) + 7
        y += 28

    # ── Pequeño producto esquina inferior derecha ──
    prod = load_product(max_w=200, max_h=300)
    if prod:
        nw, nh = prod.size
        img.alpha_composite(prod, (W - nw - 40, H - 66 - nh - 20))
        draw = ImageDraw.Draw(img)

    draw_footer(draw)
    return img.convert("RGB")


# ── SLIDE 03 — ¿Para qué sirve? ───────────────────────────────────────────────
def slide_03():
    img  = Image.new("RGBA", (W, H), (*BG, 255))
    img  = canvas_glow(img, cx=950, cy=200, radius=220, color=ACCENT, opacity=45)
    draw = ImageDraw.Draw(img)
    PAD  = 78

    # ── Título: "¿PARA QUÉ" blanco / "SIRVE?" en azul ──
    f_title = fnt(102, IDX_BLACK)
    draw.text((PAD, 72), "¿PARA QUÉ", font=f_title, fill=WHITE)
    draw.text((PAD, 72 + 110), "SIRVE?",    font=f_title, fill=ACCENT_L)

    benefits = [
        ("Reduce la urgencia y frecuencia urinaria",     "Fluye sin interrupciones"),
        ("Mejora el flujo y vacía la vejiga completo",   "Sin quedar a medias"),
        ("Devuelve el sueño sin levantarte de noche",    "Duerme de corrido"),
        ("Aumenta tu energía y vitalidad en el día",     "Activo desde la mañana"),
        ("Natural, sin efectos secundarios ni receta",   "Sin pastillas de por vida"),
    ]

    f_main = fnt(33, IDX_BOLD)
    f_sub  = fnt(26, IDX_REG)
    LH     = th(draw, "X", f_main) + 10

    y   = 348
    GAP = 130

    for i, (main, sub) in enumerate(benefits):
        # Flecha en azul
        draw_arrow(draw, PAD, y, LH, color=ACCENT_L)
        draw.text((PAD + 56, y + 2),  main, font=f_main, fill=WHITE)
        mh = th(draw, main, f_main)
        draw.text((PAD + 56, y + mh + 5), sub, font=f_sub, fill=GRAY)
        if i < len(benefits) - 1:
            draw.rectangle([PAD, y + GAP - 10, W - PAD, y + GAP - 9], fill=SEP)
        y += GAP

    draw_footer(draw)
    return img.convert("RGB")


# ── SLIDE 04 — ¿Cuándo sentir la diferencia? ─────────────────────────────────
def slide_04():
    img  = Image.new("RGBA", (W, H), (*BG, 255))
    img  = canvas_glow(img, cx=950, cy=900, radius=280, color=ACCENT, opacity=50)
    draw = ImageDraw.Draw(img)
    PAD  = 72

    # ── Headline masivo ──
    f_h   = fnt(108, IDX_BLACK)
    lines = ["¿CUÁNDO", "EMPIEZO A", "SENTIR LA", "DIFERENCIA?"]
    y = 65
    for line in lines:
        draw.text((PAD, y), line, font=f_h, fill=WHITE)
        y += th(draw, line, f_h) + 5

    # Divisor azul
    y += 20
    draw.rectangle([PAD, y, W - PAD, y + 3], fill=ACCENT)
    y += 28

    # Intro — "10 y 30 días" resaltado
    f_intro = fnt(35, IDX_REG)
    f_bold  = fnt(35, IDX_BOLD)

    # Línea 1: "Entre" + "10 y 30 días" (bold azul) + "de uso constante,"
    x_cur = PAD
    parts1 = [("Entre ", f_intro, GRAY), ("10 y 30 días ", f_bold, ACCENT_L),
              ("de uso constante,", f_intro, GRAY)]
    for t, f, c in parts1:
        draw.text((x_cur, y), t, font=f, fill=c)
        x_cur += tw(draw, t, f)
    y += th(draw, "X", f_intro) + 7

    draw.text((PAD, y), "muchas personas reportan:", font=f_intro, fill=GRAY)
    y += th(draw, "X", f_intro) + 30

    # Bullets con flechas azules
    results = [
        "Más energía en el día a día",
        "Mejor recuperación nocturna",
        "Mayor bienestar y estabilidad",
    ]
    f_res = fnt(40, IDX_BOLD)
    LH4   = th(draw, "X", f_res) + 10
    for res in results:
        draw_arrow(draw, PAD, y, LH4, color=ACCENT_L)
        draw.text((PAD + 58, y), res, font=f_res, fill=WHITE)
        y += th(draw, res, f_res) + 15

    y += 24
    f_it = fnt(29, IDX_REG)
    draw.text((PAD, y), "Cada cuerpo es diferente.", font=f_it, fill=(105, 115, 140))
    y += th(draw, "x", f_it) + 6
    draw.text((PAD, y), "El proceso empieza desde adentro.", font=f_it, fill=(105, 115, 140))

    draw_footer(draw)
    return img.convert("RGB")


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    slides = [
        ("slide_01_hook.png",           slide_01),
        ("slide_02_que_es.png",         slide_02),
        ("slide_03_para_que_sirve.png", slide_03),
        ("slide_04_cuando.png",         slide_04),
    ]

    for name, gen in slides:
        print(f"  Generando {name}...")
        out = OUT_DIR / name
        gen().save(str(out), "PNG", quality=95)
        print(f"  ✓ {out}")

    print(f"\nCarrusel v2 listo en:\n{OUT_DIR}")


if __name__ == "__main__":
    main()
