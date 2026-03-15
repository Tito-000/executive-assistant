"""
Winning Ad — Magistral v2
Réplica exacta del formato Prostatricum:
  - Fondo teal oscuro + rayos diagonales
  - Estatua de bronce izquierda (generada con Gemini)
  - Headline bold italic blanco arriba (2 líneas)
  - Badge naranja starburst centro ("Solo / 50% / HOY")
  - Producto derecha grande
  - SIN footer, SIN copy adicional
"""

import os
import sys
import math
from pathlib import Path
from io import BytesIO

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("ERROR: pip3 install google-genai")
    sys.exit(1)

try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
except ImportError:
    print("ERROR: pip3 install Pillow")
    sys.exit(1)

# ── Rutas ─────────────────────────────────────────────────────────────────────
BASE_DIR   = Path(__file__).parent.parent.parent.parent
PRODS_DIR  = BASE_DIR / "projects/immunotec/fase-1-embudos-por-producto/productos"
OUT_DIR    = PRODS_DIR / "magistral/Creativos nuevos para test"
PROD_IMG   = PRODS_DIR / "magistral/recursos/imagenes-producto/assets%2Ffdb4d79bfbfd478d89398007f8c29424%2F304711d179b94747a8bebe75d6abe295.webp"
FONT       = "/System/Library/Fonts/HelveticaNeue.ttc"

# ── Índices fuente ────────────────────────────────────────────────────────────
IDX_REG    = 0
IDX_BOLD   = 1
IDX_BLACK  = 9   # Condensed Black — el más pesado

# ── Paleta ────────────────────────────────────────────────────────────────────
WHITE      = (255, 255, 255)
ORANGE     = (220,  95,  18)   # naranja badge (como el reference)
ORANGE_LT  = (255, 210, 100)   # texto dentro del badge


def font(size, idx=IDX_REG):
    return ImageFont.truetype(FONT, size, index=idx)


def text_cx(draw, text, cx, y, fnt, fill, shadow_offset=0):
    bb = draw.textbbox((0, 0), text, font=fnt)
    w  = bb[2] - bb[0]
    if shadow_offset:
        draw.text((cx - w // 2 + shadow_offset, y + shadow_offset),
                  text, font=fnt, fill=(0, 0, 0, 110))
    draw.text((cx - w // 2, y), text, font=fnt, fill=fill)


def remove_bg(img, thr=220):
    img = img.convert("RGBA")
    data = list(img.getdata())
    new  = [(r, g, b, 0) if (r > thr and g > thr and b > thr)
            else (r, g, b, a) for r, g, b, a in data]
    img.putdata(new)
    return img


def add_glow(img, color=(0, 200, 230), blur=30):
    alpha   = img.split()[3]
    col_img = Image.new("RGBA", img.size, (*color, 185))
    col_img.putalpha(alpha)
    for _ in range(5):
        col_img = col_img.filter(ImageFilter.GaussianBlur(blur // 5))
    return Image.alpha_composite(col_img, img)


def starburst_badge(draw, cx, cy, r_out, r_in, n_points, fill):
    """Polígono de estrella (starburst) para el badge."""
    pts = []
    for i in range(n_points * 2):
        angle = math.pi / n_points * i - math.pi / 2
        r = r_out if i % 2 == 0 else r_in
        pts.append((cx + r * math.cos(angle), cy + r * math.sin(angle)))
    draw.polygon(pts, fill=fill)


# ── Step 1: Generar fondo + estatua con Gemini ────────────────────────────────
def generar_fondo_con_estatua() -> Image.Image:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise EnvironmentError("GEMINI_API_KEY no encontrada. Ejecuta: source ~/.zshenv")

    client = genai.Client(api_key=api_key)
    print("  Generando fondo + estatua con Gemini Imagen 4...")

    prompt = """
Create a 1080x1080 square advertisement background image.

BACKGROUND: Deep dark teal-to-cyan gradient. Top: very dark teal (#041E28).
Center: richer dark teal-cyan (#0A5060). Edges slightly darker.
Add 2-3 subtle diagonal light rays (very faint white, like light beams) going from bottom-left toward upper-right.

LEFT SIDE (40% of image width, full height): Place a realistic dark bronze-colored statue of a
small chubby cherub child boy (classic European fountain statue style), standing or crouching,
3D realistic, dark metallic bronze texture, positioned from roughly y=35% down to y=95% of the image.
The statue should blend naturally with the dark teal background.

RIGHT SIDE (60% of image width): Leave COMPLETELY EMPTY — only the dark teal gradient background.
No objects, no decorations, no light effects. This area will receive a product bottle in post-production.

No text anywhere. No watermarks. Photorealistic. Premium health supplement advertisement.
"""

    response = client.models.generate_images(
        model="imagen-4.0-ultra-generate-001",
        prompt=prompt,
        config=types.GenerateImagesConfig(
            number_of_images=1,
            aspect_ratio="1:1",
            safety_filter_level="BLOCK_LOW_AND_ABOVE",
        )
    )

    for img_obj in response.generated_images:
        tmp = OUT_DIR / "_tmp_bg.png"
        img_obj.image.save(str(tmp))
        bg = Image.open(tmp).convert("RGBA")
        tmp.unlink(missing_ok=True)
        print("  ✓ Fondo generado")
        return bg

    raise Exception("Gemini no devolvió imagen")


# ── Step 2: Componer todo con Pillow ──────────────────────────────────────────
def componer(bg: Image.Image) -> Image.Image:
    W, H = 1080, 1080
    canvas = bg.resize((W, H), Image.LANCZOS).convert("RGBA")
    draw   = ImageDraw.Draw(canvas)

    # ─────────────────────────────────────────────────────────────────────────
    # HEADLINE — bold italic blanco, 2 líneas, alineado izquierda
    # Réplica de: "Come ha potuto farlo senza / battere ciglio per 400 anni?"
    # Para Magistral: "¿Cómo pudo aguantarlo / sin parpadear 400 años?"
    # ─────────────────────────────────────────────────────────────────────────
    f_h  = font(88, IDX_BLACK)
    PAD  = 48

    line1 = "¿Cómo pudo aguantarlo"
    line2 = "sin parpadear 400 años?"

    # Sombra sutil
    draw.text((PAD + 4, 44 + 4), line1, font=f_h, fill=(0, 0, 0, 100))
    draw.text((PAD + 4, 140 + 4), line2, font=f_h, fill=(0, 0, 0, 100))
    # Texto blanco
    draw.text((PAD, 44),  line1, font=f_h, fill=WHITE)
    draw.text((PAD, 140), line2, font=f_h, fill=WHITE)

    # ─────────────────────────────────────────────────────────────────────────
    # BADGE NARANJA STARBURST — centro, overlapping estatua y producto
    # Contenido exacto del reference: "Solo" / "50%" / "HOY"
    # ─────────────────────────────────────────────────────────────────────────
    BCX, BCY = 390, 580   # posición centro del badge
    R_OUT, R_IN = 118, 88  # radio exterior e interior del starburst
    N_PTS = 14             # puntas del starburst

    starburst_badge(draw, BCX, BCY, R_OUT, R_IN, N_PTS, ORANGE)
    # Círculo relleno interior
    draw.ellipse([BCX - 86, BCY - 86, BCX + 86, BCY + 86], fill=ORANGE)

    f_solo  = font(34, IDX_BLACK)
    f_pct   = font(88, IDX_BLACK)
    f_hoy   = font(36, IDX_BLACK)

    text_cx(draw, "Solo", BCX, BCY - 78, f_solo, WHITE)
    text_cx(draw, "50%",  BCX, BCY - 40, f_pct,  ORANGE_LT)
    text_cx(draw, "HOY",  BCX, BCY + 52, f_hoy,  WHITE)

    # ─────────────────────────────────────────────────────────────────────────
    # PRODUCTO — derecha, grande, glow cyan
    # ─────────────────────────────────────────────────────────────────────────
    if PROD_IMG.exists():
        prod  = Image.open(str(PROD_IMG)).convert("RGBA")
        prod  = remove_bg(prod, thr=222)
        prod  = add_glow(prod, color=(0, 200, 230), blur=34)

        # Escalar: columna derecha, casi full height
        target_h = int(H * 0.82)
        target_w = int(W * 0.50)
        ratio    = min(target_w / prod.width, target_h / prod.height)
        nw       = int(prod.width  * ratio)
        nh       = int(prod.height * ratio)
        prod     = prod.resize((nw, nh), Image.LANCZOS)

        # Posicionar: lado derecho, centrado verticalmente
        px = W - nw - 10
        py = (H - nh) // 2 + 30
        canvas.alpha_composite(prod, (px, py))
    else:
        draw.text((620, 460), "⚠️ Sin imagen", font=font(32, IDX_BOLD), fill=WHITE)

    return canvas


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # Step 1: Fondo + estatua via Gemini
    bg = generar_fondo_con_estatua()

    # Step 2: Componer texto + badge + producto
    final = componer(bg)

    # Guardar
    out = OUT_DIR / "magistral_winning_ad_v2.png"
    final.convert("RGB").save(str(out), "PNG", quality=95)
    print(f"\n✓ Guardado: {out}")


if __name__ == "__main__":
    main()
