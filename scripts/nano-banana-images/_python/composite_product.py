"""
Compone la foto real del producto sobre los 3 formatos base generados por Nano Banana.
"""
import sys
from pathlib import Path
from PIL import Image, ImageFilter

def remove_white_bg(img: Image.Image, threshold: int = 215) -> Image.Image:
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

def add_glow(img: Image.Image, color_rgb: tuple, radius: int = 28, opacity: int = 150) -> Image.Image:
    pad = radius * 3
    w, h = img.size
    glow_canvas = Image.new("RGBA", (w + pad*2, h + pad*2), (0, 0, 0, 0))
    alpha = img.split()[3]
    glow_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    pixels = list(glow_layer.getdata())
    alpha_pixels = list(alpha.getdata())
    new_pixels = []
    for i, a_val in enumerate(alpha_pixels):
        if a_val > 30:
            new_pixels.append((*color_rgb, min(opacity, int(a_val * 0.8))))
        else:
            new_pixels.append((0, 0, 0, 0))
    glow_layer.putdata(new_pixels)
    glow_canvas.paste(glow_layer, (pad, pad), glow_layer)
    glow_canvas = glow_canvas.filter(ImageFilter.GaussianBlur(radius))
    result = Image.new("RGBA", (w + pad*2, h + pad*2), (0, 0, 0, 0))
    result.paste(glow_canvas, (0, 0), glow_canvas)
    result.paste(img, (pad, pad), img)
    result = result.crop((pad, pad, pad + w, pad + h))
    return result

def place_product(base: Image.Image, product: Image.Image,
                  x_pct: float, y_pct: float, w_pct: float, h_pct: float,
                  glow_color: tuple) -> Image.Image:
    cw, ch = base.size
    target_w = int(cw * w_pct)
    target_h = int(ch * h_pct)
    pw, ph = product.size
    scale = min(target_w / pw, target_h / ph)
    new_w, new_h = int(pw * scale), int(ph * scale)
    prod_scaled = product.resize((new_w, new_h), Image.LANCZOS)
    prod_glow = add_glow(prod_scaled, glow_color)
    dest_x = int(cw * x_pct) + (target_w - new_w) // 2
    dest_y = int(ch * y_pct) + (target_h - new_h) // 2
    result = base.convert("RGBA")
    result.paste(prod_glow, (dest_x, dest_y), prod_glow)
    return result.convert("RGB")

def main():
    base_dir = Path("/Users/martinmercedes/Desktop/Executive assistant 2/projects/immunotec/fase-1-embudos-por-producto/productos/immunocla/Creativos nuevos para test")
    product_path = Path("/Users/martinmercedes/Desktop/Executive assistant 2/projects/immunotec/fase-1-embudos-por-producto/productos/immunocla/recursos/Imagenes de producto /hgj.png")

    print("Cargando foto del producto...")
    product = Image.open(product_path)
    product = remove_white_bg(product, threshold=215)

    formats = [
        {
            "base": "formato-a-base.png",
            "output": "formato-a-final.png",
            # Derecha completa
            "x": 0.54, "y": 0.06, "w": 0.43, "h": 0.82,
            "glow": (0, 180, 220),  # cyan
        },
        {
            "base": "formato-b-base.png",
            "output": "formato-b-final.png",
            # Centro
            "x": 0.27, "y": 0.12, "w": 0.46, "h": 0.70,
            "glow": (255, 255, 255),  # white
        },
        {
            "base": "formato-c-base.png",
            "output": "formato-c-final.png",
            # Izquierda completa
            "x": 0.01, "y": 0.10, "w": 0.44, "h": 0.78,
            "glow": (0, 128, 128),  # teal
        },
    ]

    for fmt in formats:
        base_path = base_dir / fmt["base"]
        out_path = base_dir / fmt["output"]
        print(f"Componiendo {fmt['output']}...")
        base = Image.open(base_path)
        final = place_product(base, product.copy(),
                              fmt["x"], fmt["y"], fmt["w"], fmt["h"], fmt["glow"])
        final.save(str(out_path), "PNG")
        print(f"  ✓ Guardado: {out_path.name}")

    print("\n✓ Los 3 formatos finales listos.")

if __name__ == "__main__":
    main()
