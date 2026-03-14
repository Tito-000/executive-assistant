"""
Generador de imágenes para carrusel Meta Ads usando Gemini Imagen + Pillow
- Gemini genera el fondo/layout
- Pillow compone el producto real encima
Uso: python3 generar_imagenes_gemini.py --producto immunocla --output "/ruta/Creativos nuevos para test" --foto_producto "/ruta/producto.png"
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Optional

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("ERROR: pip3 install google-genai")
    sys.exit(1)

try:
    from PIL import Image, ImageEnhance
    import io
except ImportError:
    print("ERROR: pip3 install Pillow")
    sys.exit(1)

# ── Config ───────────────────────────────────────────────────────────────────
API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    print("ERROR: GEMINI_API_KEY no encontrada. Ejecuta: source ~/.zshenv")
    sys.exit(1)

client = genai.Client(api_key=API_KEY)
CANVAS = 1080  # px cuadrado

# ── Posiciones del producto por slide ────────────────────────────────────────
# (x_center_pct, y_center_pct, scale_pct_of_canvas)
PRODUCT_POSITIONS = {
    "slide_01_hook":         (0.73, 0.55, 0.45),
    "slide_02_que_es":       (0.22, 0.60, 0.40),
    "slide_03_para_que_sirve":(0.78, 0.70, 0.28),
    "slide_04_quienes":      None,               # sin producto
    "slide_05_resultados":   (0.75, 0.55, 0.38),
    "slide_06_oferta":       (0.28, 0.52, 0.52),
}

# ── Prompts (SIN producto — lo pega Pillow) ───────────────────────────────────
def get_slides(producto: str, datos: dict) -> list[dict]:
    nombre = datos.get("nombre", producto.upper())
    beneficios = datos.get("beneficios", [])
    mecanismo = datos.get("mecanismo", "")
    bens = "\n".join([f'- "{b}"' for b in beneficios[:5]]) if beneficios else \
        '- "Apoya el sistema inmune"\n- "Reduce el cansancio crónico"\n- "Protege las células"\n- "Regeneración celular"\n- "Mejora la energía"'

    return [
        {
            "nombre": "slide_01_hook",
            "prompt": f"""
                Professional Meta Ads carousel image, 1080x1080px, dark navy blue solid background (#0A1628).
                LEFT SIDE: Large bold white text in Spanish, two lines:
                "¿POR QUÉ" first line, "TE CANSAS" second line, "TAN RÁPIDO?" third line.
                Font: heavy black sans-serif, uppercase. Text takes up left 55% of image.
                RIGHT SIDE: empty space reserved for product photo (do not place any product here).
                Subtle blue glow/light effect on the right side where product will be placed.
                Minimalist. No extra decorations. No watermark. Professional health brand.
            """
        },
        {
            "nombre": "slide_02_que_es",
            "prompt": f"""
                Professional Meta Ads carousel image, 1080x1080px, clean white background.
                TOP CENTER: Bold dark navy title: "¿QUÉ ES {nombre.upper()}?"
                RIGHT SIDE (60% width): vertical list with blue checkmarks (✓), bold dark text:
                - "Suplemento nutricional clínico"
                - "{mecanismo[:55] if mecanismo else 'Apoya la producción natural de glutatión'}"
                - "Protege y regenera las células"
                - "Fabricado en USA"
                - "Más de 30 años de investigación"
                LEFT SIDE (40% width): empty space reserved for product — do NOT place any object here.
                Immunotec blue accent (#0057A8). Clean modern health brand layout.
            """
        },
        {
            "nombre": "slide_03_para_que_sirve",
            "prompt": f"""
                Professional Meta Ads carousel image, 1080x1080px, clean white background.
                TOP: Large bold dark title: "¿PARA QUÉ SIRVE?"
                CENTER-LEFT (65% width): vertical list with green checkmarks, bold dark text:
                {bens}
                BOTTOM LEFT: small "IMMUNOTEC" logo text in blue.
                BOTTOM RIGHT CORNER: empty space reserved for product — do NOT place any object there.
                Clean, minimal, health brand aesthetic.
            """
        },
        {
            "nombre": "slide_04_quienes",
            "prompt": f"""
                Professional Meta Ads carousel image, 1080x1080px, dark blue gradient background (#0A1628 to #1a3a6b).
                TOP: Large bold white title: "¿QUIÉNES PUEDEN TOMARLO?"
                CENTER: clean vertical list, white text, each item separated clearly:
                • Personas con cansancio constante
                • Personas con enfermedades crónicas
                • Quienes quieren fortalecer sus defensas
                • Adultos que quieren mantener su vitalidad
                • Cuidadores que dan todo por su familia
                Minimalist. Bold typography. No product image. Professional.
            """
        },
        {
            "nombre": "slide_05_resultados",
            "prompt": f"""
                Professional Meta Ads carousel image, 1080x1080px, white background.
                LEFT SIDE (60% width):
                TOP: Bold dark title: "¿CUÁNDO VER RESULTADOS?"
                Below: text "Entre 10 y 30 días de uso constante"
                Three rows with blue arrow icons:
                "→ Más energía en el día a día"
                "→ Mejor recuperación"
                "→ Mayor estabilidad y bienestar"
                Small italic note: "*Cada cuerpo es diferente."
                RIGHT SIDE (40% width): empty space for product — do NOT place any object here.
                Blue accent (#0057A8). Clean modern layout.
            """
        },
        {
            "nombre": "slide_06_oferta",
            "prompt": f"""
                Professional Meta Ads carousel image, 1080x1080px, solid blue background (#0057A8).
                RIGHT SIDE (55% width), white text:
                Title bold: "{nombre.upper()}"
                Strikethrough price in light gray: "RD$7,300"
                Large price highlighted in yellow: "RD$5,840"
                Small text: "Ahorras RD$1,460"
                Three lines with white checkmarks:
                "✓ Pago contra entrega"
                "✓ Entrega 24-72 horas"
                "✓ Asesor por WhatsApp"
                Yellow rounded CTA button at bottom right: "PIDE EL TUYO HOY"
                LEFT SIDE (45% width): empty space reserved for product — do NOT place any object here.
                High-energy sales aesthetic. Professional.
            """
        }
    ]


# ── Composición del producto ──────────────────────────────────────────────────
def componer_producto(slide_path: Path, foto_producto: Path, posicion: tuple) -> None:
    """Pega el producto real sobre el slide generado."""
    x_pct, y_pct, scale_pct = posicion

    base = Image.open(slide_path).convert("RGBA")
    producto = Image.open(foto_producto).convert("RGBA")

    # Remover fondo blanco/gris del producto si lo tiene
    producto = remover_fondo_claro(producto)

    # Escalar el producto
    target_size = int(CANVAS * scale_pct)
    ratio = target_size / max(producto.size)
    new_w = int(producto.width * ratio)
    new_h = int(producto.height * ratio)
    producto = producto.resize((new_w, new_h), Image.LANCZOS)

    # Posición centrada en el punto indicado
    x = int(CANVAS * x_pct - new_w / 2)
    y = int(CANVAS * y_pct - new_h / 2)

    # Agregar sombra/glow sutil
    base.paste(producto, (x, y), producto)
    base.convert("RGB").save(str(slide_path))


def remover_fondo_claro(img: Image.Image, threshold: int = 230) -> Image.Image:
    """Hace transparente el fondo blanco/gris claro del producto."""
    img = img.convert("RGBA")
    data = img.getdata()
    nueva = []
    for r, g, b, a in data:
        if r > threshold and g > threshold and b > threshold:
            nueva.append((r, g, b, 0))
        else:
            nueva.append((r, g, b, a))
    img.putdata(nueva)
    return img


# ── Generación ────────────────────────────────────────────────────────────────
def generar_slide(slide: dict, output_dir: Path, foto_producto: Optional[Path]) -> Path:
    print(f"  Generando {slide['nombre']}...")

    response = client.models.generate_images(
        model="imagen-4.0-ultra-generate-001",
        prompt=slide["prompt"],
        config=types.GenerateImagesConfig(
            number_of_images=1,
            aspect_ratio="1:1",
            safety_filter_level="BLOCK_LOW_AND_ABOVE",
        )
    )

    img_path = output_dir / f"{slide['nombre']}.png"
    for img in response.generated_images:
        img.image.save(str(img_path))

    # Componer producto real encima
    posicion = PRODUCT_POSITIONS.get(slide["nombre"])
    if posicion and foto_producto and foto_producto.exists():
        componer_producto(img_path, foto_producto, posicion)
        print(f"  ✓ {img_path.name} + producto real")
    else:
        print(f"  ✓ {img_path.name}")

    return img_path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--producto", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--datos", default="{}")
    parser.add_argument("--foto_producto", default=None, help="Ruta a la foto del producto")
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Auto-detectar foto si no se especifica
    foto_producto = None
    if args.foto_producto:
        foto_producto = Path(args.foto_producto)
    else:
        # Buscar en recursos/Imagenes de producto/ del producto
        base = Path("/Users/martinmercedes/Desktop/Executive assistant 2/projects/immunotec/fase-1-embudos-por-producto/productos")
        carpeta_img = base / args.producto / "recursos" / "Imagenes de producto "
        if carpeta_img.exists():
            imgs = list(carpeta_img.glob("*.png")) + list(carpeta_img.glob("*.jpg"))
            if imgs:
                # Preferir la de mayor tamaño
                foto_producto = max(imgs, key=lambda p: p.stat().st_size)
                print(f"  Foto detectada: {foto_producto.name}")

    datos = json.loads(args.datos)
    slides = get_slides(args.producto, datos)

    print(f"\nGenerando carrusel para: {args.producto}")
    print(f"Destino: {output_dir}\n")

    generadas, errores = [], []
    for slide in slides:
        try:
            generar_slide(slide, output_dir, foto_producto)
            generadas.append(slide["nombre"])
        except Exception as e:
            print(f"  ✗ Error en {slide['nombre']}: {e}")
            errores.append(slide["nombre"])

    print(f"\n✓ {len(generadas)} imágenes generadas")
    if errores:
        print(f"✗ Errores: {', '.join(errores)}")
    print(f"Carrusel listo en: {output_dir}")


if __name__ == "__main__":
    main()
