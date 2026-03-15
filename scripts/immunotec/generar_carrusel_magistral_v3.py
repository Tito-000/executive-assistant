"""
Carrusel Magistral v3 — Replica exacta del estilo Immunocal Azul
5 slides: Hook, ¿Qué es?, ¿Para qué sirve? (iconos), ¿Quiénes?, Oferta
"""
from pathlib import Path
try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
except ImportError:
    raise SystemExit("ERROR: pip3 install Pillow")

BASE     = Path("/Users/martinmercedes/Desktop/Executive assistant 2")
PROD_DIR = BASE / "projects/immunotec/fase-1-embudos-por-producto/productos/magistral"
OUT_DIR  = PROD_DIR / "Creativos nuevos para test/carrusel-kiffer-v3"
PROD_IMG = PROD_DIR / "recursos/imagenes-producto/assets%2Ffdb4d79bfbfd478d89398007f8c29424%2F304711d179b94747a8bebe75d6abe295.webp"
FONT     = "/System/Library/Fonts/HelveticaNeue.ttc"

IDX_REG   = 0
IDX_BOLD  = 1
IDX_BLACK = 9   # Condensed Black

# ── Paleta — igual que Immunocal Azul ─────────────────────────────────────────
BG         = (7,   7,   7)      # negro casi puro
WHITE      = (255, 255, 255)
GRAY_DARK  = (100, 100, 100)    # texto tachado / subtítulos débiles
GRAY_MID   = (150, 155, 165)    # sub-copy slides
DIVIDER    = (55,  55,  55)     # línea divisoria
GLOW_BLUE  = (10,  60, 200)     # glow azul profundo del producto
GLOW_CYAN  = (20, 120, 255)     # corona exterior del glow
BADGE_GOLD = (220, 175,  20)    # badge amarillo oferta
BADGE_TXT  = (20,  15,   5)     # texto sobre badge amarillo
CTA_BLUE   = (25,  80, 210)     # barra CTA footer

W, H = 1080, 1080


# ── Utilidades de fuente/texto ─────────────────────────────────────────────────
def fnt(size, idx=IDX_REG):
    return ImageFont.truetype(FONT, size, index=idx)

def th(draw, text, f):
    bb = draw.textbbox((0, 0), text, font=f)
    return bb[3] - bb[1]

def tw(draw, text, f):
    bb = draw.textbbox((0, 0), text, font=f)
    return bb[2] - bb[0]

def text_cx(draw, text, f, cx):
    w = tw(draw, text, f)
    return cx - w // 2

def strikethrough(draw, x, y, text, f, fill):
    draw.text((x, y), text, font=f, fill=fill)
    bb = draw.textbbox((x, y), text, font=f)
    mid = (bb[1] + bb[3]) // 2
    draw.line([(bb[0], mid), (bb[2], mid)], fill=fill, width=4)


# ── Producto ──────────────────────────────────────────────────────────────────
def remove_bg(img, thr=220):
    img = img.convert("RGBA")
    data = [(r, g, b, 0) if r > thr and g > thr and b > thr else (r, g, b, a)
            for r, g, b, a in img.getdata()]
    img.putdata(data)
    return img

def product_glow(canvas, cx, cy, radius):
    """Glow azul profundo igual al Immunocal Azul."""
    g = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(g)
    # capa exterior más difusa
    for r in range(radius, 0, -20):
        progress = 1 - r / radius
        a = int(130 * (progress ** 1.8))
        col = (
            int(GLOW_BLUE[0] + (GLOW_CYAN[0] - GLOW_BLUE[0]) * progress * 0.4),
            int(GLOW_BLUE[1] + (GLOW_CYAN[1] - GLOW_BLUE[1]) * progress * 0.4),
            int(GLOW_BLUE[2] + (GLOW_CYAN[2] - GLOW_BLUE[2]) * progress * 0.2),
        )
        gd.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(*col, a))
    g = g.filter(ImageFilter.GaussianBlur(55))
    return Image.alpha_composite(canvas, g)

def paste_product(canvas, max_w, max_h, cx, cy, thr=220):
    """Carga, recorta fondo y pega producto centrado en (cx, cy)."""
    if not PROD_IMG.exists():
        return canvas
    prod = Image.open(PROD_IMG).convert("RGBA")
    prod = remove_bg(prod, thr)
    r  = min(max_w / prod.width, max_h / prod.height)
    nw, nh = int(prod.width * r), int(prod.height * r)
    prod = prod.resize((nw, nh), Image.LANCZOS)
    px = cx - nw // 2
    py = cy - nh // 2
    canvas.alpha_composite(prod, (max(0, px), max(0, py)))
    return canvas


# ── Elementos de diseño ────────────────────────────────────────────────────────
def draw_arrow(draw, x, y, lh, color=WHITE):
    cy  = y + lh // 2 + 1
    tip = x + 34
    draw.line([(x, cy), (tip - 10, cy)], fill=color, width=3)
    draw.polygon([(tip - 12, cy - 8), (tip, cy), (tip - 12, cy + 8)], fill=color)

def draw_check(draw, x, y, size, color=WHITE):
    """Checkmark dibujado a mano."""
    pts = [
        (x, y + size * 0.5),
        (x + size * 0.35, y + size * 0.85),
        (x + size, y),
    ]
    draw.line(pts, fill=color, width=3)

def pill_badge(draw, x, y, text, f, bg, fg, pad_x=22, pad_h=14):
    bw = tw(draw, text, f) + pad_x * 2
    bh = th(draw, text, f) + pad_h * 2
    draw.rounded_rectangle([x, y, x + bw, y + bh], radius=bh // 2, fill=bg)
    draw.text((x + pad_x, y + pad_h - 2), text, font=f, fill=fg)
    return bw, bh

def divider(draw, x1, x2, y, color=DIVIDER):
    draw.rectangle([x1, y, x2, y + 2], fill=color)

def footer_simple(draw):
    """Footer gris simple (slides informativos)."""
    draw.rectangle([0, H - 60, W, H], fill=(12, 12, 12))
    draw.rectangle([0, H - 61, W, H - 60], fill=DIVIDER)
    f = fnt(21, IDX_BOLD)
    draw.text((52, H - 40), "MAGISTRAL", font=f, fill=GRAY_MID)
    rw = tw(draw, "IMMUNOTEC", f)
    draw.text((W - 52 - rw, H - 40), "IMMUNOTEC", font=f, fill=WHITE)

def footer_cta(draw):
    """Footer azul grande con CTA (slide oferta)."""
    # Mini texto centrado justo encima
    f_mini = fnt(19, IDX_BOLD)
    label = "MAGISTRAL — IMMUNOTEC"
    draw.text((text_cx(draw, label, f_mini, W // 2), H - 105), label,
              font=f_mini, fill=GRAY_DARK)
    # Barra azul
    draw.rectangle([0, H - 80, W, H], fill=CTA_BLUE)
    f_cta = fnt(48, IDX_BLACK)
    cta = "ESCRÍBENOS AHORA"
    draw.text((text_cx(draw, cta, f_cta, W // 2), H - 72), cta,
              font=f_cta, fill=WHITE)


# ── Íconos outline (estilo Immunocal) ─────────────────────────────────────────
LW = 4   # line width global de íconos

def icon_drop(draw, cx, cy, r, c=WHITE):
    """Gota de agua — urgencia urinaria"""
    draw.ellipse([cx - r, cy, cx + r, cy + r * 2], outline=c, width=LW)
    draw.line([(cx - r + 6, cy + r // 2), (cx, cy - r)], fill=c, width=LW)
    draw.line([(cx + r - 6, cy + r // 2), (cx, cy - r)], fill=c, width=LW)

def icon_moon(draw, cx, cy, r, c=WHITE):
    """Luna — sueño nocturno"""
    draw.arc([cx - r, cy - r, cx + r, cy + r], 30, 330, fill=c, width=LW)
    offset = r // 3
    draw.arc([cx - r + offset, cy - r + offset // 2,
              cx + r + offset, cy + r - offset // 2],
             210, 150, fill=c, width=LW)

def icon_bolt(draw, cx, cy, r, c=WHITE):
    """Rayo — energía"""
    pts = [
        (cx + r * 2 // 3, cy - r),
        (cx - r // 5,     cy + r // 8),
        (cx + r // 3,     cy + r // 8),
        (cx - r * 2 // 3, cy + r),
    ]
    draw.line(pts, fill=c, width=LW + 1)

def icon_shield(draw, cx, cy, r, c=WHITE):
    """Escudo — salud prostática"""
    pts = [
        (cx - r,     cy - r + r // 3),
        (cx - r,     cy + r // 3),
        (cx,         cy + r),
        (cx + r,     cy + r // 3),
        (cx + r,     cy - r + r // 3),
        (cx - r,     cy - r + r // 3),
    ]
    draw.line(pts, fill=c, width=LW)

def icon_leaf(draw, cx, cy, r, c=WHITE):
    """Hoja — natural"""
    draw.arc([cx - r, cy - r, cx + r, cy + r], 135, 315, fill=c, width=LW)
    draw.arc([cx - r, cy - r, cx + r, cy + r], 315, 135, fill=c, width=LW)
    draw.line([(cx - r // 2 - 2, cy + r // 2 + 2),
               (cx + r // 2 + 2, cy - r // 2 - 2)], fill=c, width=LW - 1)

ICONS = [icon_drop, icon_moon, icon_bolt, icon_shield, icon_leaf]


# ════════════════════════════════════════════════════════════════════════════
# SLIDES
# ════════════════════════════════════════════════════════════════════════════

def slide_01():
    """Hook: pregunta + producto con glow grande"""
    canvas = Image.new("RGBA", (W, H), (*BG, 255))

    # Glow a la derecha — igual que referencia
    PROD_CX, PROD_CY = 800, 480
    canvas = product_glow(canvas, PROD_CX, PROD_CY, 370)
    canvas = paste_product(canvas, max_w=460, max_h=860, cx=PROD_CX, cy=PROD_CY)
    draw = ImageDraw.Draw(canvas)

    # Headline izquierda
    PAD = 58
    f_h = fnt(108, IDX_BLACK)
    lines = ["¿POR QUÉ", "TE LEVANTAS", "3 VECES", "AL BAÑO?"]
    y = 90
    for line in lines:
        draw.text((PAD, y), line, font=f_h, fill=WHITE)
        y += th(draw, line, f_h) + 6

    # Divisor
    y += 18
    divider(draw, PAD, 555, y)
    y += 22

    # Sub-copy
    f_sub = fnt(33, IDX_REG)
    draw.text((PAD, y), "Esto no es la edad.", font=f_sub, fill=GRAY_MID)
    draw.text((PAD, y + 42), "Tu próstata necesita apoyo.", font=f_sub, fill=GRAY_MID)

    footer_simple(draw)
    return canvas.convert("RGB")


def slide_02():
    """¿Qué es Magistral? — bullets + producto flotante"""
    canvas = Image.new("RGBA", (W, H), (*BG, 255))

    # Glow pequeño en zona derecha
    canvas = product_glow(canvas, 830, 600, 240)
    canvas = paste_product(canvas, max_w=300, max_h=500, cx=830, cy=580)
    draw = ImageDraw.Draw(canvas)

    PAD = 70
    # Título grande 2 líneas
    f_t = fnt(108, IDX_BLACK)
    draw.text((PAD, 78),  "¿QUÉ ES",    font=f_t, fill=WHITE)
    draw.text((PAD, 78 + th(draw, "X", f_t) + 4), "MAGISTRAL?", font=f_t, fill=WHITE)

    y = 78 + (th(draw, "X", f_t) + 4) * 2 + 24
    divider(draw, PAD, W - PAD, y)
    y += 28

    # Lista de bullets — columna izquierda (hasta x=640)
    bullets = [
        "Suplemento nutricional clínico",
        "Fórmula líquida de alta absorción",
        "Con Saw Palmetto (Serenoa repens)",
        "Fabricado en USA",
        "Más de 30 años de respaldo clínico",
    ]
    f_b = fnt(36, IDX_BOLD)
    LH  = th(draw, "X", f_b) + 10
    for item in bullets:
        draw_arrow(draw, PAD, y, LH)
        draw.text((PAD + 52, y + 2), item, font=f_b, fill=WHITE)
        y += LH + 18

    footer_simple(draw)
    return canvas.convert("RGB")


def slide_03():
    """¿Para qué sirve? — layout iconos igual que referencia"""
    canvas = Image.new("RGBA", (W, H), (*BG, 255))
    draw   = ImageDraw.Draw(canvas)
    PAD    = 70

    # Título full-width
    f_t = fnt(96, IDX_BLACK)
    draw.text((PAD, 72), "¿PARA QUÉ SIRVE?", font=f_t, fill=WHITE)

    y = 72 + th(draw, "X", f_t) + 18
    divider(draw, PAD, W - PAD, y)
    y += 32

    rows = [
        (icon_drop,   "REDUCE LA URGENCIA URINARIA",    "Fluye sin interrupciones"),
        (icon_moon,   "DEVUELVE EL SUEÑO COMPLETO",     "Duerme de corrido"),
        (icon_bolt,   "AUMENTA TU ENERGÍA",             "Activo desde la mañana"),
        (icon_shield, "APOYA LA SALUD PROSTÁTICA",      "Saw Palmetto clínicamente probado"),
        (icon_leaf,   "NATURAL SIN EFECTOS",            "Sin receta · Sin pastillas"),
    ]

    f_main = fnt(40, IDX_BLACK)
    f_sub  = fnt(26, IDX_REG)
    ICON_R = 28
    GAP    = 145

    for icon_fn, title, sub in rows:
        icon_cx = PAD + ICON_R
        icon_cy = y + GAP // 2 - ICON_R // 2 - 10
        icon_fn(draw, icon_cx, icon_cy, ICON_R)

        tx = PAD + ICON_R * 2 + 22
        draw.text((tx, y + 8),  title, font=f_main, fill=WHITE)
        draw.text((tx, y + 8 + th(draw, "X", f_main) + 4), sub,   font=f_sub,  fill=GRAY_MID)
        y += GAP

    footer_simple(draw)
    return canvas.convert("RGB")


def slide_04():
    """¿Quiénes pueden tomarlo? — título + producto arriba, lista abajo"""
    canvas = Image.new("RGBA", (W, H), (*BG, 255))

    # Glow arriba derecha
    canvas = product_glow(canvas, 830, 280, 260)
    canvas = paste_product(canvas, max_w=320, max_h=500, cx=830, cy=260)
    draw   = ImageDraw.Draw(canvas)

    PAD = 60
    # Título grande izquierda (3 líneas)
    f_t = fnt(104, IDX_BLACK)
    draw.text((PAD, 72),  "¿QUIÉNES",  font=f_t, fill=WHITE)
    lh = th(draw, "X", f_t) + 5
    draw.text((PAD, 72 + lh),    "PUEDEN",    font=f_t, fill=WHITE)
    draw.text((PAD, 72 + lh * 2), "TOMARLO?", font=f_t, fill=WHITE)

    y = 72 + lh * 3 + 20
    divider(draw, PAD, W - PAD, y)
    y += 28

    items = [
        "Hombres mayores de 40 años",
        "Con urgencia urinaria frecuente",
        "Que se levantan al baño de noche",
        "Con baja energía y cansancio",
        "Que buscan una solución natural",
    ]
    f_b = fnt(36, IDX_BOLD)
    LH  = th(draw, "X", f_b) + 12
    for item in items:
        draw_arrow(draw, PAD, y, LH)
        draw.text((PAD + 52, y + 2), item, font=f_b, fill=WHITE)
        y += LH + 20

    footer_simple(draw)
    return canvas.convert("RGB")


def slide_05():
    """Oferta — precio + badge amarillo + CTA azul"""
    canvas = Image.new("RGBA", (W, H), (*BG, 255))

    # Glow derecha (grande, igual que referencia)
    PROD_CX = 760
    canvas = product_glow(canvas, PROD_CX, 460, 330)
    canvas = paste_product(canvas, max_w=400, max_h=720, cx=PROD_CX, cy=460)
    draw   = ImageDraw.Draw(canvas)

    PAD = 60

    # Nombre producto grande
    f_prod = fnt(96, IDX_BLACK)
    draw.text((PAD, 72), "MAGISTRAL",  font=f_prod, fill=WHITE)

    y = 72 + th(draw, "MAGISTRAL", f_prod) + 16

    # Badge amarillo
    f_badge = fnt(26, IDX_BLACK)
    _, bh = pill_badge(draw, PAD, y, "SAW PALMETTO + ZINC", f_badge,
                       BADGE_GOLD, BADGE_TXT)
    y += bh + 26

    # Precio tachado
    f_old = fnt(36, IDX_BOLD)
    strikethrough(draw, PAD, y, "RD$7,300", f_old, GRAY_DARK)
    y += th(draw, "X", f_old) + 10

    # Precio nuevo grande
    f_new = fnt(74, IDX_BLACK)
    draw.text((PAD, y), "RD$5,840", font=f_new, fill=WHITE)
    y += th(draw, "X", f_new) + 28

    # Checkmarks
    checks = [
        "Pago contra entrega",
        "Entrega 24-72 horas",
        "Asesor real por WhatsApp",
    ]
    f_ck = fnt(34, IDX_BOLD)
    ck_h = th(draw, "X", f_ck)
    for item in checks:
        draw_check(draw, PAD, y + 4, ck_h - 4)
        draw.text((PAD + ck_h + 10, y), item, font=f_ck, fill=WHITE)
        y += ck_h + 20

    footer_cta(draw)
    return canvas.convert("RGB")


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    slides = [
        ("slide_01_hook.png",           slide_01),
        ("slide_02_que_es.png",         slide_02),
        ("slide_03_para_que_sirve.png", slide_03),
        ("slide_04_quienes.png",        slide_04),
        ("slide_05_oferta.png",         slide_05),
    ]

    for name, gen in slides:
        print(f"  Generando {name}...")
        gen().save(str(OUT_DIR / name), "PNG", quality=95)
        print(f"  ✓ {name}")

    print(f"\nCarrusel v3 listo en:\n{OUT_DIR}")


if __name__ == "__main__":
    main()
