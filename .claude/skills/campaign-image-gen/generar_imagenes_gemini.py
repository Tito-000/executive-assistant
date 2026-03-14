"""
Generador de imágenes para carrusel Meta Ads usando Gemini + Pillow
- Todos los slides: imagen-4.0-ultra-generate-001 genera el diseño base (SIN producto)
- Pillow pega la foto real del producto encima con glow y posicionamiento por slide
Uso: python3 generar_imagenes_gemini.py --producto immunocla --output "/ruta/Creativos nuevos para test"
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Optional
from io import BytesIO

try:
    from google import genai
    from google.genai import types
except ImportError:
    print("ERROR: pip3 install google-genai")
    sys.exit(1)

try:
    from PIL import Image, ImageFilter, ImageDraw, ImageEnhance
except ImportError:
    print("ERROR: pip3 install Pillow")
    sys.exit(1)


# ── Config ───────────────────────────────────────────────────────────────────
API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    print("ERROR: GEMINI_API_KEY no encontrada. Ejecuta: source ~/.zshenv")
    sys.exit(1)

client = genai.Client(api_key=API_KEY)

# Slides que necesitan la foto del producto compuesta encima
SLIDES_CON_PRODUCTO = {"slide_01_hook", "slide_02_que_es", "slide_03_para_que_sirve", "slide_05_resultados", "slide_06_oferta"}

# Configuración de posición/tamaño del producto por slide (x%, y%, w%, h%)
# Coordenadas relativas al canvas 1080x1080
PRODUCTO_CONFIG = {
    "slide_01_hook":          {"x": 0.55, "y": 0.08, "w": 0.40, "h": 0.84, "glow": "cyan"},
    "slide_02_que_es":        {"x": 0.02, "y": 0.15, "w": 0.38, "h": 0.72, "glow": "blue"},
    "slide_03_para_que_sirve":{"x": 0.65, "y": 0.45, "w": 0.32, "h": 0.52, "glow": "blue"},
    "slide_05_resultados":    {"x": 0.55, "y": 0.08, "w": 0.42, "h": 0.84, "glow": "blue"},
    "slide_06_oferta":        {"x": 0.02, "y": 0.08, "w": 0.44, "h": 0.84, "glow": "white"},
}


# ── Prompts ───────────────────────────────────────────────────────────────────
def get_slides(producto: str, datos: dict) -> list:
    nombre = datos.get("nombre", producto.upper())
    beneficios = datos.get("beneficios", [])
    mecanismo = datos.get("mecanismo", "")
    bens = "\n".join([f'- "{b}"' for b in beneficios[:5]]) if beneficios else \
        '- "Apoya el sistema inmune"\n- "Reduce el cansancio crónico"\n- "Protege las células"\n- "Regeneración celular"\n- "Mejora la energía"'

    return [
        {
            "nombre": "slide_01_hook",
            "prompt": f"""
                Create a professional Meta Ads carousel image, 1080x1080px square.
                Background: dark navy blue solid (#0A1628).
                LEFT SIDE (50%): Large bold white text in Spanish, uppercase, heavy sans-serif:
                Line 1: "¿POR QUÉ"
                Line 2: "TE CANSAS"
                Line 3: "TAN RÁPIDO?"
                RIGHT SIDE (50%): Leave this area COMPLETELY EMPTY — solid dark background only, no objects, no decorations. A product image will be placed here in post-production.
                Subtle cyan radial glow on the right side center to indicate where product goes.
                Minimalist. No watermarks. Professional health brand aesthetic.
            """
        },
        {
            "nombre": "slide_02_que_es",
            "prompt": f"""
                Create a professional Meta Ads carousel image, 1080x1080px square.
                Background: clean white.
                TOP CENTER: Bold dark navy title: "¿QUÉ ES {nombre.upper()}?"
                LEFT SIDE (40%): Leave this area COMPLETELY EMPTY — white background only. A product image will be placed here in post-production.
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
                Create a professional Meta Ads carousel image, 1080x1080px square.
                Background: clean white.
                TOP: Large bold dark title: "¿PARA QUÉ SIRVE?"
                LEFT/CENTER (65%): vertical list with green checkmarks, bold dark text:
                {bens}
                BOTTOM LEFT: small "IMMUNOTEC" text in blue.
                BOTTOM RIGHT corner: Leave this area EMPTY — white background. A product image will be composited here in post-production.
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
                No product needed. Minimalist. Bold typography. Professional.
            """
        },
        {
            "nombre": "slide_05_resultados",
            "prompt": f"""
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
                RIGHT SIDE (45%): Leave this area COMPLETELY EMPTY — white background only. A product image will be placed here in post-production.
                Blue accent (#0057A8). Clean modern layout.
            """
        },
        {
            "nombre": "slide_06_oferta",
            "prompt": f"""
                Create a professional Meta Ads carousel image, 1080x1080px square.
                Background: solid blue (#0057A8).
                LEFT SIDE (45%): Leave this area COMPLETELY EMPTY — solid blue background only. A product image will be placed here in post-production.
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


# ── Remoción de fondo blanco con Pillow ──────────────────────────────────────
def remove_white_background(img: Image.Image, threshold: int = 210) -> Image.Image:
    """Convierte pixels blancos/casi-blancos en transparentes."""
    img = img.convert("RGBA")
    data = img.getdata()
    new_data = []
    for r, g, b, a in data:
        if r > threshold and g > threshold and b > threshold:
            new_data.append((r, g, b, 0))
        else:
            new_data.append((r, g, b, a))
    img.putdata(new_data)
    return img


def add_glow(img: Image.Image, color: str, radius: int = 30, opacity: int = 160) -> Image.Image:
    """Añade un glow de color alrededor del producto."""
    glow_colors = {
        "cyan":  (0, 210, 230),
        "blue":  (0, 87, 168),
        "white": (255, 255, 255),
    }
    glow_rgb = glow_colors.get(color, (0, 210, 230))

    # Canvas para el glow (más grande para el blur)
    pad = radius * 3
    w, h = img.size
    glow_canvas = Image.new("RGBA", (w + pad*2, h + pad*2), (0, 0, 0, 0))

    # Usar el canal alpha del producto como máscara del glow
    alpha = img.split()[3]
    glow_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    for x in range(w):
        for y in range(h):
            a_val = alpha.getpixel((x, y))
            if a_val > 30:
                glow_layer.putpixel((x, y), (*glow_rgb, min(opacity, a_val)))

    glow_canvas.paste(glow_layer, (pad, pad), glow_layer)
    glow_canvas = glow_canvas.filter(ImageFilter.GaussianBlur(radius))

    # Componer glow + imagen original
    result = Image.new("RGBA", (w + pad*2, h + pad*2), (0, 0, 0, 0))
    result.paste(glow_canvas, (0, 0), glow_canvas)
    result.paste(img, (pad, pad), img)

    # Recortar de vuelta al tamaño original
    result = result.crop((pad, pad, pad + w, pad + h))
    return result


def composite_product(base_img: Image.Image, product_path: Path, slide_name: str) -> Image.Image:
    """Pega el producto real con glow sobre el slide generado por IA."""
    cfg = PRODUCTO_CONFIG.get(slide_name)
    if not cfg:
        return base_img

    canvas_w, canvas_h = base_img.size  # 1080x1080

    # Cargar producto y remover fondo blanco
    producto = Image.open(product_path).convert("RGBA")
    producto = remove_white_background(producto, threshold=210)

    # Calcular tamaño objetivo
    target_w = int(canvas_w * cfg["w"])
    target_h = int(canvas_h * cfg["h"])

    # Escalar manteniendo aspecto dentro del bounding box
    prod_w, prod_h = producto.size
    scale = min(target_w / prod_w, target_h / prod_h)
    new_w = int(prod_w * scale)
    new_h = int(prod_h * scale)
    producto = producto.resize((new_w, new_h), Image.LANCZOS)

    # Añadir glow
    producto = add_glow(producto, cfg["glow"], radius=25, opacity=140)

    # Posición (centrado dentro del área de destino)
    dest_x = int(canvas_w * cfg["x"]) + (target_w - new_w) // 2
    dest_y = int(canvas_h * cfg["y"]) + (target_h - new_h) // 2

    # Componer
    result = base_img.convert("RGBA")
    result.paste(producto, (dest_x, dest_y), producto)
    return result.convert("RGB")


# ── Generación ────────────────────────────────────────────────────────────────
def generar_slide(slide: dict, output_dir: Path, foto_producto: Optional[Path]) -> Path:
    print(f"  Generando {slide['nombre']}...")

    img_path = output_dir / f"{slide['nombre']}.png"
    usa_producto = slide["nombre"] in SLIDES_CON_PRODUCTO

    # Generar diseño base con Imagen 4 Ultra
    response = client.models.generate_images(
        model="imagen-4.0-ultra-generate-001",
        prompt=slide["prompt"],
        config=types.GenerateImagesConfig(
            number_of_images=1,
            aspect_ratio="1:1",
            safety_filter_level="BLOCK_LOW_AND_ABOVE",
        )
    )

    # Obtener imagen base
    base_img = None
    for img_obj in response.generated_images:
        # Guardar temporalmente y cargar con Pillow
        tmp_path = output_dir / f"_tmp_{slide['nombre']}.png"
        img_obj.image.save(str(tmp_path))
        base_img = Image.open(tmp_path)
        break

    if base_img is None:
        raise Exception("Imagen 4 no devolvió imagen")

    # Composite del producto real si corresponde
    if usa_producto and foto_producto and foto_producto.exists():
        final_img = composite_product(base_img, foto_producto, slide["nombre"])
        final_img.save(str(img_path))
        # Limpiar temporal
        tmp_path.unlink(missing_ok=True)
        print(f"  ✓ {img_path.name} (producto real integrado con Pillow)")
    else:
        # Sin producto — renombrar el temporal
        tmp_path.rename(img_path)
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
        base = Path("/Users/martinmercedes/Desktop/Executive assistant 2/projects/immunotec/fase-1-embudos-por-producto/productos")
        carpeta_img = base / args.producto / "recursos" / "Imagenes de producto "
        if carpeta_img.exists():
            imgs = list(carpeta_img.glob("*.png")) + list(carpeta_img.glob("*.jpg"))
            if imgs:
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
