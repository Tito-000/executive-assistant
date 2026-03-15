"""
Compone la foto real del Magistral sobre los 5 slides base generados por Nano Banana / Kie.ai.
"""
from pathlib import Path
from PIL import Image, ImageFilter


def remove_white_bg(img: Image.Image, threshold: int = 220) -> Image.Image:
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


def add_glow(img: Image.Image, color_rgb: tuple, radius: int = 35, opacity: int = 160) -> Image.Image:
    pad = radius * 3
    w, h = img.size
    glow_canvas = Image.new("RGBA", (w + pad*2, h + pad*2), (0, 0, 0, 0))
    alpha = img.split()[3]
    glow_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    alpha_pixels = list(alpha.getdata())
    new_pixels = []
    for a_val in alpha_pixels:
        if a_val > 30:
            new_pixels.append((*color_rgb, min(opacity, int(a_val * 0.85))))
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
    base_dir = Path("/Users/martinmercedes/Desktop/Executive assistant 2/projects/immunotec/fase-1-embudos-por-producto/productos/magistral/Creativos nuevos para test/carrusel-nano-banana-v1")
    product_path = Path("/Users/martinmercedes/Desktop/Executive assistant 2/projects/immunotec/fase-1-embudos-por-producto/productos/magistral/recursos/imagenes-producto/Imagend el magistral .png")

    print("Cargando foto del Magistral...")
    product = Image.open(product_path)
    product = remove_white_bg(product, threshold=220)
    print(f"  Producto cargado: {product.size}, mode: {product.mode}")

    # Glow azul magistral (sky blue)
    GLOW = (100, 180, 240)

    slides = [
        {
            # Slide 01 — Hook: columna izquierda texto, columna derecha vacía (46% right)
            "base": "slide-01-base.jpg",
            "output": "slide-01-final.jpg",
            "x": 0.54, "y": 0.08, "w": 0.42, "h": 0.80,
            "glow": GLOW,
        },
        {
            # Slide 02 — ¿Qué es?: zona derecha vacía (42% right, bottom 68%)
            "base": "slide-02-base.jpg",
            "output": "slide-02-final.jpg",
            "x": 0.56, "y": 0.30, "w": 0.40, "h": 0.60,
            "glow": GLOW,
        },
        {
            # Slide 03 — ¿Para qué sirve?: layout full-width, sin zona de producto
            # Ponemos producto flotando arriba a la derecha pequeño
            "base": "slide-03-base.jpg",
            "output": "slide-03-final.jpg",
            "x": 0.68, "y": 0.00, "w": 0.30, "h": 0.22,
            "glow": GLOW,
        },
        {
            # Slide 04 — ¿Quiénes?: zona derecha top-right vacía (42% right, top 48%)
            "base": "slide-04-base.jpg",
            "output": "slide-04-final.jpg",
            "x": 0.57, "y": 0.02, "w": 0.40, "h": 0.44,
            "glow": GLOW,
        },
        {
            # Slide 05 — Oferta: zona derecha completamente vacía (48% right)
            "base": "slide-05-base.jpg",
            "output": "slide-05-final.jpg",
            "x": 0.52, "y": 0.05, "w": 0.46, "h": 0.82,
            "glow": GLOW,
        },
    ]

    for slide in slides:
        base_path = base_dir / slide["base"]
        out_path = base_dir / slide["output"]

        if not base_path.exists():
            print(f"  ⚠ Falta: {slide['base']} — saltando")
            continue

        print(f"Componiendo {slide['output']}...")
        base = Image.open(base_path)
        final = place_product(base, product.copy(),
                              slide["x"], slide["y"], slide["w"], slide["h"], slide["glow"])
        final.save(str(out_path), "JPEG", quality=95)
        print(f"  ✓ {out_path.name}")

    print("\n✓ Compositing completado.")


if __name__ == "__main__":
    main()
