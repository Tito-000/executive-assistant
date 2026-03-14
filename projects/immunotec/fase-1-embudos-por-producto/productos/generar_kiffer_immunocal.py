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
    "slide_01_metas":               (0.28, 0.55, 0.45),
    "slide_02_para_que_sirve":      (0.70, 0.55, 0.50),
    "slide_03_como_tomar":          (0.75, 0.60, 0.45),
    "slide_04_quienes":             None,               # sin producto
    "slide_05_compras":             (0.50, 0.60, 0.50),
}

# ── Prompts (SIN producto — lo pega Pillow) ───────────────────────────────────
def get_slides(producto: str, datos: dict) -> list[dict]:
    nombre = datos.get("nombre", producto.upper())
    return [
        {
            "nombre": "slide_01_metas",
            "prompt": f"""
                Professional Meta Ads carousel image, 1080x1080px, clean white background.
                TOP: Huge bold black text "ALCANZA TUS METAS" in italics.
                RIGHT SIDE: 4 circular icons with red outlines forming a grid. 
                Below each icon, bold red text respectively: "ELEVA GLUTATIÓN", "SISTEMA INMUNE", "ENERGÍA NATURAL", "SALUD CELULAR".
                LEFT SIDE: empty space reserved for product — do NOT place any object here.
                Minimalist, high contrast, fitness and health brand aesthetic.
            """
        },
        {
            "nombre": "slide_02_para_que_sirve",
            "prompt": f"""
                Professional Meta Ads carousel image, 1080x1080px, clean white background.
                LEFT SIDE (50% width): Huge bold black text "¿PARA QUE SIRVE IMMUNOCAL?" stacked vertically across 4 lines.
                RIGHT SIDE (50% width): empty space reserved for product container — do NOT place any object here.
                Minimalist layout. High contrast text. Clean health brand aesthetic.
            """
        },
        {
            "nombre": "slide_03_como_tomar",
            "prompt": f"""
                Professional Meta Ads carousel image, 1080x1080px, clean white background.
                TOP LEFT SIDE: Huge bold black text "¿COMO TOMAR?" stacked.
                BELOW TEXT (Left Side 60% width): Two paragraphs in black bold sans-serif font:
                "SI BUSCAS MEJORAR TU SALUD, LOS ESPECIALISTAS RECOMIENDAN TOMAR 1 O 2 SOBRES DE IMMUNOCAL AL DÍA POR LAS MAÑANAS."
                "TE RECOMENDAMOS MEZCLAR EL PRODUCTO ÚNICAMENTE CON UNA ONZA DE AGUA O JUGO FRÍO EN TU VASO MEZCLADOR INSTITUCIONAL. NO LICUAR NI USAR LÍQUIDOS CALIENTES."
                RIGHT SIDE (40% width): empty space reserved for product — do NOT place any object here.
                Minimalist layout. High contrast text.
            """
        },
        {
            "nombre": "slide_04_quienes",
            "prompt": f"""
                Professional Meta Ads carousel image, 1080x1080px, clean white background.
                TOP: Huge bold black text "¿QUIENES PUEDEN TOMAR?".
                BELOW: Centered vertical list in black bold uppercase text with line breaks:
                "PERSONAS QUE BUSQUEN REFORZAR SU SISTEMA INMUNOLÓGICO."
                "PERSONAS QUE SUFREN DE DEBILIDAD O ENFERMEDADES."
                "PERSONAS CON BAJOS NIVELES DE ENERGÍA."
                "DEPORTISTAS EN BUSCA DE UNA MEJOR RECUPERACIÓN."
                "ADULTOS MAYORES PARA MANTENER SU VITALIDAD."
                "CUALQUIER PERSONA QUE QUIERA UN ENVEJECIMIENTO SALUDABLE."
                Minimalist. Solid white background, dense black bold typography. No product image.
            """
        },
        {
            "nombre": "slide_05_compras",
            "prompt": f"""
                Professional Meta Ads carousel image, 1080x1080px, clean white background.
                TOP: Bold black text "REALIZA TUS COMPRAS EN" and massive bold black website link "WWW.IMMUNOTEC.COM" below it.
                CENTER: large empty space reserved for multiple product containers — do NOT place any object here.
                BOTTOM LEFT: Small social media icons (Instagram, Facebook text).
                Minimalist layout. High contrast commercial aesthetic.
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

    # Pegar
    base.paste(producto, (x, y), producto)
    base.convert("RGB").save(str(slide_path))


def remover_fondo_claro(img: Image.Image, threshold: int = 240) -> Image.Image:
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

    datos = json.loads(args.datos)
    slides = get_slides(args.producto, datos)

    print(f"\nGenerando carrusel Kiffer-style para: {args.producto}")
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
