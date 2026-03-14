"""
Generador de imágenes para carrusel Meta Ads usando Gemini
- Slides con producto: gemini-2.5-flash-image recibe la foto real y diseña el ad alrededor de ella
- Slide sin producto (quiénes): imagen-4.0-ultra-generate-001
Uso: python3 generar_imagenes_gemini.py --producto immunocla --output "/ruta/Creativos nuevos para test"
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


# ── Config ───────────────────────────────────────────────────────────────────
API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    print("ERROR: GEMINI_API_KEY no encontrada. Ejecuta: source ~/.zshenv")
    sys.exit(1)

client = genai.Client(api_key=API_KEY)

# Slides que necesitan la foto del producto como referencia
SLIDES_CON_PRODUCTO = {"slide_01_hook", "slide_02_que_es", "slide_03_para_que_sirve", "slide_05_resultados", "slide_06_oferta"}

# ── Prompts ───────────────────────────────────────────────────────────────────
PRODUCT_INSTRUCTION = "IMPORTANT: The first image provided is the EXACT product photo to use. Include it faithfully in the design — do not create or imagine a different product. Place it prominently as indicated."

def get_slides(producto: str, datos: dict) -> list[dict]:
    nombre = datos.get("nombre", producto.upper())
    beneficios = datos.get("beneficios", [])
    mecanismo = datos.get("mecanismo", "")
    bens = "\n".join([f'- "{b}"' for b in beneficios[:5]]) if beneficios else \
        '- "Apoya el sistema inmune"\n- "Reduce el cansancio crónico"\n- "Protege las células"\n- "Regeneración celular"\n- "Mejora la energía"'

    p = PRODUCT_INSTRUCTION
    return [
        {
            "nombre": "slide_01_hook",
            "prompt": f"""
                {p}
                Create a professional Meta Ads carousel image, 1080x1080px square.
                Background: dark navy blue solid (#0A1628).
                LEFT SIDE (50%): Large bold white text in Spanish, uppercase, heavy sans-serif:
                Line 1: "¿POR QUÉ"
                Line 2: "TE CANSAS"
                Line 3: "TAN RÁPIDO?"
                RIGHT SIDE (50%): Place the product from the provided image here, prominent, with a subtle cyan glow effect around it.
                Minimalist. No watermarks. Professional health brand aesthetic.
            """
        },
        {
            "nombre": "slide_02_que_es",
            "prompt": f"""
                {p}
                Create a professional Meta Ads carousel image, 1080x1080px square.
                Background: clean white.
                TOP CENTER: Bold dark navy title: "¿QUÉ ES {nombre.upper()}?"
                LEFT SIDE (40%): Place the product from the provided image here, full height, prominent.
                RIGHT SIDE (60%): vertical list with blue checkmarks (✓), bold dark text:
                ✓ Suplemento nutricional clínico
                ✓ {mecanismo[:55] if mecanismo else 'Apoya la producción natural de glutatión'}
                ✓ Protege y regenera las células
                ✓ Fabricado en USA
                ✓ Más de 30 años de investigación
                Immunotec blue accent (#0057A8). Clean modern health brand layout.
            """
        },
        {
            "nombre": "slide_03_para_que_sirve",
            "prompt": f"""
                {p}
                Create a professional Meta Ads carousel image, 1080x1080px square.
                Background: clean white.
                TOP: Large bold dark title: "¿PARA QUÉ SIRVE?"
                LEFT/CENTER (65%): vertical list with green checkmarks, bold dark text:
                {bens}
                BOTTOM RIGHT: Place the product from the provided image here, smaller size, as accent.
                BOTTOM LEFT: small "IMMUNOTEC" text in blue.
                Clean minimal health brand aesthetic.
            """
        },
        {
            "nombre": "slide_04_quienes",
            "prompt": f"""
                Create a professional Meta Ads carousel image, 1080x1080px square.
                Background: dark blue gradient (#0A1628 to #1a3a6b).
                TOP: Large bold white title: "¿QUIÉNES PUEDEN TOMARLO?"
                CENTER: clean vertical list, white text, bullet points:
                • Personas con cansancio constante
                • Personas con enfermedades crónicas
                • Quienes quieren fortalecer sus defensas
                • Adultos que quieren mantener su vitalidad
                • Cuidadores que dan todo por su familia
                No product image on this slide. Minimalist. Bold typography. Professional.
            """
        },
        {
            "nombre": "slide_05_resultados",
            "prompt": f"""
                {p}
                Create a professional Meta Ads carousel image, 1080x1080px square.
                Background: white.
                LEFT SIDE (55%):
                Bold dark title: "¿CUÁNDO VER RESULTADOS?"
                Text: "Entre 10 y 30 días de uso constante"
                Three rows with blue arrow icons:
                → Más energía en el día a día
                → Mejor recuperación
                → Mayor estabilidad y bienestar
                Small italic: "*Cada cuerpo es diferente."
                RIGHT SIDE (45%): Place the product from the provided image here, floating, prominent.
                Blue accent (#0057A8). Clean modern layout.
            """
        },
        {
            "nombre": "slide_06_oferta",
            "prompt": f"""
                {p}
                Create a professional Meta Ads carousel image, 1080x1080px square.
                Background: solid blue (#0057A8).
                LEFT SIDE (45%): Place the product from the provided image here, large and prominent.
                RIGHT SIDE (55%), white text:
                Bold title: "{nombre.upper()} AZUL"
                Strikethrough price (gray): "RD$7,300"
                Large yellow highlighted price: "RD$5,840"
                Small: "Ahorras RD$1,460"
                Checkmarks in white:
                ✓ Pago contra entrega
                ✓ Entrega 24-72 horas
                ✓ Asesor por WhatsApp
                Yellow rounded button at bottom: "PIDE EL TUYO HOY"
                High-energy sales aesthetic. Professional.
            """
        }
    ]


# ── Generación ────────────────────────────────────────────────────────────────
def generar_slide(slide: dict, output_dir: Path, foto_producto: Optional[Path]) -> Path:
    print(f"  Generando {slide['nombre']}...")

    img_path = output_dir / f"{slide['nombre']}.png"
    usa_producto = slide["nombre"] in SLIDES_CON_PRODUCTO

    if usa_producto and foto_producto and foto_producto.exists():
        # Usar gemini-2.5-flash-image con la foto real como referencia
        with open(foto_producto, "rb") as f:
            foto_bytes = f.read()

        response = client.models.generate_content(
            model="gemini-2.5-flash-image",
            contents=[
                types.Part.from_bytes(data=foto_bytes, mime_type="image/png"),
                types.Part.from_text(text=slide["prompt"])
            ],
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE", "TEXT"],
            )
        )

        for part in response.candidates[0].content.parts:
            if part.inline_data and "image" in part.inline_data.mime_type:
                with open(img_path, "wb") as f:
                    f.write(part.inline_data.data)
                print(f"  ✓ {img_path.name} (producto real integrado)")
                return img_path

        raise Exception("Gemini no devolvió imagen")

    else:
        # Slide sin producto — usar Imagen 4 Ultra
        response = client.models.generate_images(
            model="imagen-4.0-ultra-generate-001",
            prompt=slide["prompt"],
            config=types.GenerateImagesConfig(
                number_of_images=1,
                aspect_ratio="1:1",
                safety_filter_level="BLOCK_LOW_AND_ABOVE",
            )
        )
        for img in response.generated_images:
            img.image.save(str(img_path))
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
