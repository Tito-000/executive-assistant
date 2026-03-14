import os
import sys
from pathlib import Path
from PIL import Image
try:
    from google import genai
    from google.genai import types
except ImportError:
    print("ERROR: pip3 install google-genai")
    sys.exit(1)

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    print("ERROR: GEMINI_API_KEY no encontrada.")
    sys.exit(1)

client = genai.Client(api_key=API_KEY)
CANVAS = 1080

def componer_producto(slide_path: Path, foto_producto: Path, posicion: tuple) -> None:
    x_pct, y_pct, scale_pct = posicion
    base = Image.open(slide_path).convert("RGBA")
    producto = Image.open(foto_producto).convert("RGBA")
    
    # Remover fondo blanco
    data = producto.getdata()
    nueva = []
    for r, g, b, a in data:
        if r > 240 and g > 240 and b > 240:
            nueva.append((r, g, b, 0))
        else:
            nueva.append((r, g, b, a))
    producto.putdata(nueva)
    
    target_size = int(CANVAS * scale_pct)
    ratio = target_size / max(producto.size)
    new_w = int(producto.width * ratio)
    new_h = int(producto.height * ratio)
    producto = producto.resize((new_w, new_h), Image.LANCZOS)
    
    x = int(CANVAS * x_pct - new_w / 2)
    y = int(CANVAS * y_pct - new_h / 2)
    base.paste(producto, (x, y), producto)
    base.convert("RGB").save(str(slide_path))

prompt = """
Professional Meta Ads graphic image, 1080x1080px, clean white background.
EXTREME LEFT SIDE (Occupying left 50%): Massive, very condensed, ultra-bold black typography text stacked in 3 lines:
"¿PARA QUÉ" (first line)
"SIRVE" (second line)
"IMMUNOCAL?" (third line).
The text must be styled exactly like an aggressive modern fitness supplement ad. It is perfectly left-aligned, extremely tight line spacing, and takes up the entire left half of the image.
RIGHT SIDE (Occupying right 50%): empty white space reserved for product container — do NOT place any object or text here.
Minimalist layout. Ultra high contrast solid black text on pure white background. No other visual elements, no logos.
"""

print("Generando imagen con Gemini/Imagen...")
response = client.models.generate_images(
    model="imagen-4.0-ultra-generate-001",
    prompt=prompt,
    config=types.GenerateImagesConfig(
        number_of_images=1,
        aspect_ratio="1:1",
        safety_filter_level="BLOCK_LOW_AND_ABOVE",
    )
)

out_dir = Path("/Users/martinmercedes/Desktop/Executive assistant 2/projects/immunotec/fase-1-embudos-por-producto/productos/immunocla/recursos/KifferStyle")
out_dir.mkdir(parents=True, exist_ok=True)
img_path = out_dir / "para_que_sirve_v2.png"

for img in response.generated_images:
    img.image.save(str(img_path))

foto_path = Path("/Users/martinmercedes/Desktop/Executive assistant 2/projects/immunotec/fase-1-embudos-por-producto/productos/immunocla/recursos/Imagenes de producto /Gemini_Generated_Image_y2lwsy2lwsy2lwsy (1).png")
componer_producto(img_path, foto_path, (0.75, 0.55, 0.65)) # Producto grande en la derecha
print("✓ Generado en:", img_path)
