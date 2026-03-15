# Skill: campaign-image-gen

Genera anuncios para Meta Ads de productos Immunotec. El formato, número de piezas y estructura los define Martin en el momento. La generación de imágenes usa **exclusivamente Nano Banana Pro via Kie.ai** — nunca Gemini, Imagen 4, ni Pillow puro.

## Cuándo usar este skill

Cuando Martin diga:
- "Genera anuncios para [producto]"
- "Crea los ads de [producto]"
- "Hazme las imágenes para [producto]"
- "Usa el skill de imágenes"
- "campaign-image-gen"

---

## Paso 1 — Entender qué se va a generar

Martin especificará qué quiere: un carrusel de N slides, una imagen estática, un formato específico. Si no lo especifica, preguntar:

> "¿Qué quieres generar?"
> Ejemplos: carrusel de 5 slides, imagen estática de oferta, slide de hook, etc.

La carpeta raíz del producto es:
`projects/immunotec/fase-1-embudos-por-producto/productos/[nombre-producto]/`

---

## Paso 2 — Investigar los documentos del producto

Antes de generar nada, leer TODOS los archivos disponibles en estas carpetas del producto:

1. `WWP/` — Winning Writing Process: estructura del mensaje, gancho, historia, oferta, CTA
2. `Market Reaserch/` — investigación de mercado: dolores, deseos, objeciones, lenguaje del avatar
3. `Top player analisis/` — análisis de top players: formatos ganadores, ángulos de ataque

**Si alguna carpeta está vacía, continuar con las que tengan contenido.**

### Síntesis obligatoria antes de generar

Extraer de los documentos:

- **Gancho principal** — idea más poderosa para captar atención en 1-2 segundos
- **Ángulo de mensaje** — eje emocional o racional que más resuena con el avatar
- **Beneficios top 3-5** — los que aparecen con más fuerza en los documentos
- **Headline principal** — derivado del WWP y del lenguaje del mercado
- **CTA** — el llamado a la acción más alineado con la etapa del funnel
- **Oferta / promesa** — si hay una oferta activa o promesa de transformación clara

Todo el copy de la imagen debe salir de esta síntesis.

---

## Paso 3 — Obtener la imagen del producto

Buscar la foto del producto en:
`projects/immunotec/fase-1-embudos-por-producto/productos/[nombre-producto]/recursos/Imagenes de producto/`

Usar la imagen de mayor resolución disponible. Si hay varias, preguntar a Martin cuál prefiere.

---

## Paso 4 — Construir los prompts Nano Banana

Para cada pieza a generar, crear un archivo JSON en:
`scripts/nano-banana-images/prompt-[producto]-[nombre-slide].json`

Usar el **Dense Narrative Format** del skill nano-banana-images:

```json
{
  "prompt": "descripción ultra-detallada zona a zona con hex colors, posiciones, tipografía, layout exacto",
  "negative_prompt": "elementos a evitar separados por coma",
  "api_parameters": {
    "aspect_ratio": "1:1",
    "resolution": "1K",
    "output_format": "jpg"
  }
}
```

### Reglas de construcción de prompts

- Describir cada zona del canvas con posición y porcentaje exacto (ej: `LEFT COLUMN (left 54%)`)
- Especificar hex colors para cada elemento
- Para slides con producto: dejar zona vacía con glow — `"COMPLETELY EMPTY — deep navy background with soft blue radial glow"`
- Agregar al negative_prompt: `"product images, bottles, any object in product zone"`
- El producto NUNCA lo genera la IA — siempre se composita después con PIL

---

## Paso 5 — Ejecutar generación via Kie.ai

Para cada prompt JSON:

```bash
source ~/.zshenv && python3 scripts/nano-banana-images/generate_kie.py \
  scripts/nano-banana-images/prompt-[producto]-[slide].json \
  "[ruta-output]/[slide]-base.jpg" \
  "1:1"
```

Si son múltiples slides, lanzar en paralelo con `&` y esperar con `wait`.

Guardar bases en:
`projects/immunotec/fase-1-embudos-por-producto/productos/[nombre-producto]/Creativos nuevos para test/[nombre-carpeta]/`

---

## Paso 6 — Compositar el producto real

Usar PIL para colocar la foto real del producto sobre cada base generada:

```python
from PIL import Image, ImageFilter

def remove_white_bg(img, threshold=220): ...
def add_glow(img, color_rgb, radius=35, opacity=160): ...
def place_product(base, product, x_pct, y_pct, w_pct, h_pct, glow_color): ...
```

**Posicionamiento por tipo de slide:**
- Slide con zona derecha vacía: `x=0.52, y=0.08, w=0.44, h=0.80`
- Slide con zona top-right vacía: `x=0.57, y=0.02, w=0.40, h=0.44`
- Slide full-width (beneficios/iconos): producto pequeño top-right `x=0.68, y=0.00, w=0.30, h=0.22`

**Colores de glow por producto:**
- Magistral: `(100, 180, 240)` — sky blue
- Immunocal: `(0, 180, 220)` — cyan
- Platinum: `(212, 175, 55)` — gold
- Multi-Resveratrol: `(180, 50, 50)` — rojo

Guardar finales como `-final.jpg` junto a los `-base.jpg`.

---

## Paso 7 — Generar el copy completo para Meta Ads

Para cada pieza generada, crear el copy del anuncio:

**Primaria (texto principal):**
- Hook de apertura — primera línea que detiene el scroll
- Desarrollo — agitar el problema o amplificar el deseo
- Credibilidad — ingrediente, mecanismo único, o resultado específico
- CTA — claro y directo

**Titular:** versión corta del gancho (máx. 40 caracteres)

**Descripción:** 1 línea que refuerza el beneficio o la oferta

Guardar en `copy-ads-[producto]-[fecha].md` dentro de `Creativos nuevos para test/`.

---

## Paso 8 — Mostrar resultados y validar

1. Mostrar cada imagen final a Martin una por una
2. Preguntar: "¿Cuáles te quedas y cuáles descartamos?"
3. Eliminar las descartadas
4. Subir las aprobadas a Canva via MCP si Martin lo pide

---

## Costo estimado

- Nano Banana via Kie.ai: ~$0.04–0.06 USD por imagen
- Carrusel de 5 slides: ~$0.20–0.30 USD

---

## Reglas inamovibles

- **Solo Nano Banana Pro via Kie.ai** — nunca Gemini, Imagen 4, ni Pillow puro para fondos
- Siempre usar la foto real del producto — nunca dejar que la IA la genere
- Todo el copy sale de los documentos de investigación — no inventar nada
- Textos siempre en español dominicano (tú, no usted)
- Si los documentos están vacíos o incompletos, notificar a Martin antes de continuar
