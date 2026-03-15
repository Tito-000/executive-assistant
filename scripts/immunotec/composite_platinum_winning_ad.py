"""
Composita el sachet de Immunocal Platinum sobre el winning ad base.
"""
from PIL import Image, ImageFilter, ImageEnhance
import sys

BASE_PATH = "projects/immunotec/fase-1-embudos-por-producto/productos/platinum/Creativos nuevos para test/platinum-winning-ad-base.jpg"
PRODUCT_PATH = "projects/immunotec/fase-1-embudos-por-producto/productos/platinum/recursos/imagenes-producto/vsf.png"
OUTPUT_PATH = "projects/immunotec/fase-1-embudos-por-producto/productos/platinum/Creativos nuevos para test/platinum-winning-ad-final.jpg"

GLOW_COLOR = (212, 175, 55)  # Gold para Platinum


def remove_white_bg(img, threshold=230):
    """Remove white/near-white background, return RGBA."""
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


def add_glow(img, color_rgb, radius=30, opacity=140):
    """Add a soft outer glow to the product."""
    glow_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    r, g, b = color_rgb
    for pixel in range(img.size[0] * img.size[1]):
        pass

    alpha = img.split()[3]
    glow = Image.new("RGBA", img.size, (r, g, b, 0))
    glow.putalpha(alpha)
    glow = glow.filter(ImageFilter.GaussianBlur(radius))

    data = list(glow.getdata())
    new_data = []
    for pr, pg, pb, pa in data:
        new_data.append((pr, pg, pb, min(pa, opacity)))
    glow.putdata(new_data)

    result = Image.alpha_composite(glow_layer, glow)
    result = Image.alpha_composite(result, img)
    return result


def place_product(base, product_path, x_pct, y_pct, w_pct, h_pct):
    """Load product, remove bg, add glow, place on base."""
    product = Image.open(product_path).convert("RGBA")
    product = remove_white_bg(product, threshold=230)
    product = add_glow(product, GLOW_COLOR, radius=35, opacity=150)

    W, H = base.size
    target_w = int(W * w_pct)
    target_h = int(H * h_pct)

    # Maintain aspect ratio
    orig_w, orig_h = product.size
    ratio = min(target_w / orig_w, target_h / orig_h)
    new_w = int(orig_w * ratio)
    new_h = int(orig_h * ratio)
    product = product.resize((new_w, new_h), Image.LANCZOS)

    x = int(W * x_pct) - new_w // 2
    y = int(H * y_pct) - new_h // 2

    base_rgba = base.convert("RGBA")
    base_rgba.paste(product, (x, y), product)
    return base_rgba


def main():
    base = Image.open(BASE_PATH)
    W, H = base.size
    print(f"Base size: {W}x{H}")

    # Place product centered in left column (x=25%, y=58%)
    result = place_product(base, PRODUCT_PATH,
                           x_pct=0.25,
                           y_pct=0.58,
                           w_pct=0.40,
                           h_pct=0.62)

    # Restore the bubble + silhouette region from original base so bubbles
    # appear IN FRONT of the product (z-order trick on flat image).
    # Bubble zone: x=30% to 100%, y=27% to 88%
    bx1 = int(W * 0.30)
    by1 = int(H * 0.27)
    bx2 = W
    by2 = int(H * 0.88)
    bubble_region = base.crop((bx1, by1, bx2, by2))
    result_rgb = result.convert("RGB")
    result_rgb.paste(bubble_region, (bx1, by1))

    result_rgb.save(OUTPUT_PATH, "JPEG", quality=95)
    print(f"Saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
