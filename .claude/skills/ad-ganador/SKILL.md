---
name: ad-ganador
description: Use when someone asks to generate winning ads, create Meta Ads images, or make ad creatives for a product. Reads WWP, Market Research, and Top Player Analysis, then generates HD images using Nano Banana 2.
disable-model-invocation: true
argument-hint: "[producto]"
---

# Skill: /ad-ganador

Genera anuncios ganadores para Meta Ads. Lee toda la investigación del producto, sintetiza el mejor ángulo de mensaje, genera copy de clase mundial, y produce imágenes HD con Nano Banana 2 (kie.ai).

---

## Paso 1 — Preguntar el producto

Si no se proporcionó en `$ARGUMENTS`, preguntar:

> "¿Para cuál producto genero los anuncios?"
> - Immunocal
> - Magistral
> - Platinum
> - Multy-Resveratrol

La carpeta raíz del producto es:
`projects/immunotec/fase-1-embudos-por-producto/productos/[nombre-producto]/`

---

## Paso 2 — Investigar los documentos del producto

Leer TODOS los archivos disponibles en estas carpetas:

1. `WWP/` — Winning Writing Process: gancho, historia, oferta, CTA, avatar, niveles de conciencia y sofisticación
2. `Market Reaserch/` — dolores, deseos, objeciones, lenguaje exacto del avatar
3. `Top player analisis/` — formatos ganadores, ángulos de los mejores, qué está funcionando

**Si alguna carpeta está vacía o no existe, continuar con las que tengan contenido.**

### Síntesis obligatoria

Después de leer, extraer:

- **Gancho principal** — la idea más poderosa para detener el scroll en 1-2 segundos
- **Ángulo de mensaje** — el eje emocional o racional que más resuena con el avatar
- **Beneficios top 3-5** — los que aparecen con más fuerza en los documentos
- **Headline 1 y Headline 2** — del WWP y del lenguaje del mercado
- **CTA** — alineado con la etapa del funnel
- **Oferta / promesa** — si hay una oferta activa o promesa de transformación

Todo el copy debe salir de esta síntesis. No inventar nada que no esté en los documentos.

---

## Paso 3 — Obtener imagen del producto

Buscar la foto del producto en:
`projects/immunotec/fase-1-embudos-por-producto/productos/[nombre-producto]/recursos/Imagenes de producto/`

Si hay varias imágenes, usar la de mayor resolución. Si hay duda, preguntar.

---

## Paso 4 — Generar copy completo para los 3 formatos

Para cada formato, crear copy de Meta Ads aplicando técnicas de los mejores copywriters (Ogilvy, Halbert, Schwartz, Hormozi).

### Estructura por anuncio

**Texto principal:**
- Hook — primera línea que detiene el scroll (basado en el dolor o deseo más fuerte)
- Desarrollo — agitar el problema o amplificar el deseo, usar lenguaje exacto del Market Research
- Credibilidad — ingrediente, mecanismo único, o resultado específico
- CTA — claro y directo

**Titular:** Versión corta y poderosa del gancho (máx. 40 caracteres)

**Descripción:** 1 línea que refuerza el beneficio principal o la oferta

### Técnicas a aplicar
- Interrupción de patrón, especificidad, lenguaje del avatar, future pacing, mecanismo único

Guardar el copy en:
`projects/immunotec/fase-1-embudos-por-producto/productos/[nombre-producto]/Creativos nuevos para test/copy-ads-[producto]-[fecha].md`

Formato:
```
# Copy Meta Ads — [Producto] — [Fecha]

## Formato A — Atención Directa
**Titular:** ...
**Texto principal:** ...
**Descripción:** ...

## Formato B — Resultado Transformación
**Titular:** ...
**Texto principal:** ...
**Descripción:** ...

## Formato C — Limpio Beneficios
**Titular:** ...
**Texto principal:** ...
**Descripción:** ...
```

---

## Paso 5 — Generar imágenes HD con Nano Banana 2

Para cada formato, construir un prompt JSON y ejecutar el script. Las imágenes se guardan en:
`projects/immunotec/fase-1-embudos-por-producto/productos/[nombre-producto]/Creativos nuevos para test/`

### Comando de ejecución
```bash
python3 scripts/nano-banana-images/generate_kie.py \
  scripts/nano-banana-images/prompt-[producto]-[formato].json \
  "projects/immunotec/fase-1-embudos-por-producto/productos/[nombre-producto]/Creativos nuevos para test/[producto]-formato-[A|B|C]-[fecha].jpg" \
  "4:5"
```

---

### Formato A — "Atención Directa"

**Concepto visual:** Fondo negro sólido. Titular grande izquierda en mayúsculas. Producto real derecha con glow azul. Botón CTA azul. Banner inferior azul claro.

**Prompt JSON a guardar en** `scripts/nano-banana-images/prompt-[producto]-formato-a.json`:

```json
{
  "prompt": "Professional Meta Ads static image. Graphic design style, high resolution, clean and bold layout. EXACT LAYOUT: Solid black background (#000000), completely flat, no gradients. LEFT SIDE: Large bold uppercase white headline text in 2 lines — '[HEADLINE_DERIVADO_DEL_GANCHO]'. Below headline: smaller subtitle in white or light gray — '[SUBTITULO_DEL_BENEFICIO]'. Below subtitle: a bold blue CTA button (#1877F2) with white text — '[CTA]'. RIGHT SIDE: The product [nombre-producto] — a [descripción del producto: sobre/caja/frasco] with its original colors, placed vertically, centered on the right half. The product has a vivid cyan-blue glow/light effect (#00CFFF) emanating from behind it, creating a premium halo effect against the black background. BOTTOM: A horizontal blue banner (#1877F2 or similar) spanning the full width with small white text indicating the product category or plan. Typography is modern, bold sans-serif (similar to Bebas Neue or Impact for headline, clean sans-serif for body). This is a polished, high-conversion Facebook/Instagram ad — NOT a photo, it is a professional graphic design composition. No people, no background scenes. Pure product ad layout. Do not add any text other than what is specified.",
  "negative_prompt": "photorealistic background, people, models, lifestyle, nature, gradients on background, white background, light background, blurry, low quality, text errors, extra elements, watermark",
  "api_parameters": {
    "aspect_ratio": "4:5",
    "resolution": "1K",
    "output_format": "jpg"
  }
}
```

Reemplazar `[HEADLINE_DERIVADO_DEL_GANCHO]`, `[SUBTITULO_DEL_BENEFICIO]`, `[CTA]`, y `[nombre-producto]` con los valores reales de la síntesis.

---

### Formato B — "Resultado Transformación"

**Concepto visual:** Fondo verde medio. Etiqueta amarilla top. Producto al centro con glow blanco. 4 badges circulares con beneficios. Banner inferior redondeado con oferta.

**Prompt JSON a guardar en** `scripts/nano-banana-images/prompt-[producto]-formato-b.json`:

```json
{
  "prompt": "Professional Meta Ads static image. Graphic design style, high resolution. EXACT LAYOUT: Solid medium green background (#2D7A4F or similar rich green), completely flat. TOP: A yellow rounded label/badge (#FFD700) near the top center with bold dark text — '1 [PERIODO] de [NOMBRE_PRODUCTO]'. Below it, a white or light text subtitle — '[BENEFICIO_PRINCIPAL_LOGRADO]'. CENTER: The product [nombre-producto] — a [descripción del producto] centered vertically in the composition, slightly large, with a soft white glow/halo effect behind it for premium feel. AROUND THE PRODUCT: 4 circular badge icons evenly spaced (top-left, top-right, bottom-left, bottom-right of the product), each a white or light-colored circle with a small icon and short text label underneath — the labels are: '[BENEFICIO_1]', '[BENEFICIO_2]', '[BENEFICIO_3]', '[BENEFICIO_4]'. BOTTOM: A dark green or white rounded pill/banner with text — '[OFERTA_O_PROMESA]'. Typography: bold modern sans-serif. This is a polished Facebook/Instagram ad graphic. No people, no background scenes. Do not add any text other than what is specified.",
  "negative_prompt": "photorealistic background, people, models, lifestyle, nature, gradients on background, white background, blurry, low quality, text errors, extra elements, watermark",
  "api_parameters": {
    "aspect_ratio": "4:5",
    "resolution": "1K",
    "output_format": "jpg"
  }
}
```

Reemplazar todos los placeholders con valores reales.

---

### Formato C — "Limpio Beneficios"

**Concepto visual:** Fondo crema/blanco roto. Headline verde centrado top. Producto izquierda full height. 5 badges teal apilados derecha. Footer con marca.

**Prompt JSON a guardar en** `scripts/nano-banana-images/prompt-[producto]-formato-c.json`:

```json
{
  "prompt": "Professional Meta Ads static image. Graphic design style, high resolution, clean minimal layout. EXACT LAYOUT: Cream or off-white background (#F5F0E8 or similar), completely flat. TOP CENTER: Bold green headline text (#2D7A4F) — '[HEADLINE_DEL_ANGULO_DE_MENSAJE]'. LEFT SIDE (60% of width): The product [nombre-producto] — a [descripción del producto] placed tall and prominent, almost full height of the image, showing the front face of the product clearly. RIGHT SIDE (40% of width): 5 teal rounded rectangle badges (#20B2AA or similar) stacked vertically with small white icons and short white text labels — the labels are: '[BENEFICIO_1]', '[BENEFICIO_2]', '[BENEFICIO_3]', '[BENEFICIO_4]', '[BENEFICIO_5]'. BOTTOM FOOTER: A thin footer bar with the brand name '[MARCA]' on the left and key ingredient or certifications text on the right, in small dark gray text. Typography: clean modern sans-serif. This is a polished Facebook/Instagram ad. No people, no background scenes. Do not add any text other than what is specified.",
  "negative_prompt": "photorealistic background, people, models, lifestyle, nature, dark background, blurry, low quality, text errors, extra elements, watermark",
  "api_parameters": {
    "aspect_ratio": "4:5",
    "resolution": "1K",
    "output_format": "jpg"
  }
}
```

Reemplazar todos los placeholders con valores reales.

---

## Paso 6 — Revisión y Canva

1. Mostrar las 3 imágenes generadas a Martin una por una
2. Preguntar: "¿Cuáles te quedas y cuáles descartamos?"
3. Eliminar las descartadas de la carpeta
4. Subir las aprobadas a Canva usando el MCP (`mcp__claude_ai_Canva__upload-asset-from-url`) para edición final

---

## Notas

- Los prompts de Nano Banana deben incluir los valores reales extraídos de la síntesis — no placeholders genéricos
- Textos siempre en español dominicano (tú, no usted)
- Si los documentos de investigación están vacíos, notificar a Martin antes de continuar
- Costo estimado: ~$0.04–0.09 por imagen, ~$0.12–0.27 por los 3 formatos
- Registrar gasto en `IA Master Resources/gastos-api/gastos-api.csv` después de generar
