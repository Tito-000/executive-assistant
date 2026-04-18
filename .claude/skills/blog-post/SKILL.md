---
name: blog-post
description: Use when someone asks to create a blog post, write an article for SEO, generate blog content, or publish a new blog entry for MM Agency.
argument-hint: [keyword o tema del artículo]
disable-model-invocation: false
---

# Blog Post Generator — MM Agency

ultrathink

Genera un artículo de blog completo para MM Agency: keyword research, artículo de 3,000-4,000 palabras, infografías HTML con brand, imágenes IA, SEO completo. Estilo NoGood.io.

## Inputs

| Input | Fuente |
|-------|--------|
| **Keyword** | `$ARGUMENTS` o preguntar al usuario |
| **Template HTML** | `projects/agencia-marketing/landing/blog/_template.html` |
| **Blog post CSS** | `projects/agencia-marketing/landing/css/blog-post.css` |
| **Infographic CSS** | [infographic-styles.css](infographic-styles.css) — copiar a blog-post.css la primera vez |
| **Infographic templates** | [infographic-templates.md](infographic-templates.md) — HTML snippets para cada tipo |
| **Brand** | Violet `#713DFF`, Green `#008500`, Orange `#F54900`, Dark `#121214`. Fonts: Orbitron, Inter, DM Mono |

## Fases

### Fase 1: Keyword Research

Ejecutar 3-4 WebSearch queries:

1. `"[keyword] república dominicana"` — competencia directa
2. `"[keyword] santo domingo" OR "[keyword] RD" 2026"` — variaciones
3. `"cómo [keyword]" OR "[keyword] para pymes" OR "[keyword] para negocios"` — long-tail
4. Leer los top 3 resultados con WebFetch — extraer: extensión, estructura, qué cubren, qué NO cubren

Producir:
- Keyword principal
- 8-12 keywords secundarios (distribuir en H2s)
- 4 FAQ questions (de "People Also Ask")
- Plan: título H1 + 6-8 H2s + estimación de palabras

**PAUSA:** Presentar plan al usuario. No continuar sin aprobación.

### Fase 2: Escribir el Artículo (3,000-4,000 palabras)

Estructura obligatoria:

1. **Lead** (100 palabras) — Hook + keyword en las primeras 100 palabras
2. **Contexto RD** (150 palabras) — datos locales (82% internet, 7M Facebook, 78% WhatsApp)
3. **Secciones H2** (6-8, cada una 400-600 palabras):
   - Keyword secundario en cada H2
   - Párrafos de 2-3 oraciones
   - 1 callout cada 2 secciones
   - Mínimo 3 internal links (servicios, contacto, otros posts)
4. **Inline CTA** después de sección 2-3: `<a href="../contact.html" class="post-inline-cta">AGENDA UNA CONSULTA GRATIS</a>`
5. **Stats** — 3 datos numéricos con `.post-stats`
6. **FAQ** — 4 items con accordion
7. **Conclusión** + CTA suave

Tono: profesional pero accesible. Sin relleno. Cada párrafo aporta valor.

### Fase 3: Infografías HTML/CSS

Crear 3-5 infografías inline usando los templates de [infographic-templates.md](infographic-templates.md).

Tipos disponibles: tabla comparativa, diagrama de flujo, checklist, stats, hub diagram.

Verificar si los estilos de [infographic-styles.css](infographic-styles.css) ya están en `blog-post.css`. Si no, copiarlos al final del archivo (antes de `@media`). Solo la primera vez.

### Fase 4: Imágenes IA (2 obligatorias)

Cada blog post DEBE tener exactamente **2 imágenes IA** colocadas inline dentro del artículo.

**Reglas de colocación:**
- **Imagen 1 (cover.jpg):** Después del segundo párrafo del artículo (después del párrafo de contexto, antes de la primera infografía). Concepto general del tema del artículo.
- **Imagen 2 (mid.jpg):** Aproximadamente a la mitad del artículo, entre la sección H2 #4 y #5 (o entre #3 y #4 si solo hay 6 H2s). Concepto específico de una sección clave del artículo.

**HTML para insertar cada imagen:**
```html
<figure class="post-cover-inline">
  <img src="../assets/blog/[slug]/cover.jpg" alt="[keyword + descripción contextual]" loading="eager">
</figure>

<figure class="post-cover-inline">
  <img src="../assets/blog/[slug]/mid.jpg" alt="[keyword + descripción contextual]" loading="lazy">
</figure>
```

**Estilo de los prompts — IMPORTANTE:**
NO usar prompts minimalistas. Las imágenes deben ser vibrantes, coloridas, estilo editorial/magazine. Usar esta estructura:

```json
{
  "prompt": "Bold graphic design illustration, [concepto específico]. [Descripción detallada de la composición con múltiples elementos visuales]. Rich color palette: electric violet #713DFF, bright green #00CC66, hot orange #F54900, cyan #00D4FF, magenta #FF2D78, golden yellow #FFB800. Glossy 3D elements with soft shadows on deep dark navy #0D0D1A background. Magazine cover quality, editorial illustration style, maximalist composition with balanced whitespace.",
  "negative_prompt": "text, labels, watermarks, stock photo, generic, blurry, dull colors, monochrome, minimalist, empty, realistic people, photographs",
  "api_parameters": { "aspect_ratio": "16:9", "resolution": "2K" }
}
```

**Paso 1:** Crear directorio de assets:
```bash
mkdir -p projects/agencia-marketing/landing/assets/blog/[slug]
```

**Paso 2:** Crear 2 prompt JSONs:
- `scripts/nano-banana-images/mm-agency/blog-[slug]/prompt-cover.json` — concepto general
- `scripts/nano-banana-images/mm-agency/blog-[slug]/prompt-mid.json` — concepto específico

**Paso 3:** Generar ambas imágenes (en paralelo si es posible):
```bash
python3 scripts/nano-banana-images/_python/generate_kie.py scripts/nano-banana-images/mm-agency/blog-[slug]/prompt-cover.json projects/agencia-marketing/landing/assets/blog/[slug]/cover.jpg "16:9"
python3 scripts/nano-banana-images/_python/generate_kie.py scripts/nano-banana-images/mm-agency/blog-[slug]/prompt-mid.json projects/agencia-marketing/landing/assets/blog/[slug]/mid.jpg "16:9"
```

### Fase 5: Ensamblar HTML

1. Leer `projects/agencia-marketing/landing/blog/_template.html`
2. Crear `projects/agencia-marketing/landing/blog/[slug].html`
3. Reemplazar ALL `{{placeholders}}`:
   - `{{TITULO DEL ARTICULO}}` → título real
   - `{{META DESCRIPTION}}` → 150-160 chars con keyword
   - `{{slug}}` → kebab-case, sin acentos
   - `{{YYYY-MM-DD}}` → fecha de hoy
   - `{{Mes DD, YYYY}}` → formato español (e.g. "Abril 17, 2026")
   - `{{CATEGORIA}}` → categoría principal
   - `{{WORD_COUNT}}` → conteo real
   - `{{tag1}}, {{tag2}}` → tags SEO
   - TOC → títulos reales de secciones
   - FAQ → preguntas y respuestas reales
   - Related articles → posts existentes o placeholders
4. Insertar infografías y `<figure>` images con alt text + keyword

### Fase 6: SEO Check

Verificar:
- [ ] Keyword en `<title>` (primeras palabras)
- [ ] Keyword en `<meta description>`
- [ ] Keyword en H1 y al menos 2 H2s
- [ ] Keyword en primeras 100 palabras
- [ ] Keyword en alt text de imagen principal
- [ ] 3+ internal links
- [ ] Schema.org: Article + FAQPage + BreadcrumbList
- [ ] OG tags con imagen
- [ ] Canonical URL correcta

### Fase 7: Actualizar Blog

1. Agregar card en `projects/agencia-marketing/landing/blog.html`
2. Agregar entrada en `projects/agencia-marketing/landing/sitemap.xml`
3. Actualizar related articles en posts existentes

### Fase 8: Entregar

```bash
open projects/agencia-marketing/landing/blog/[slug].html
```

Mostrar resumen: título, keywords, word count, # infografías, # imágenes, archivos creados.

## Output

| Archivo | Ubicación |
|---------|-----------|
| Post HTML | `projects/agencia-marketing/landing/blog/[slug].html` |
| Imágenes | `projects/agencia-marketing/landing/assets/blog/[slug]/` |
| Prompt JSON | `scripts/nano-banana-images/mm-agency/blog-[slug]/prompt.json` |
| Blog listing | `projects/agencia-marketing/landing/blog.html` (actualizado) |
| Sitemap | `projects/agencia-marketing/landing/sitemap.xml` (actualizado) |

## Notes

- **No continuar sin aprobación** del plan en Fase 1
- **Infografías = HTML/CSS, no imágenes.** Google lee el texto, carga rápido, es responsive
- **Imágenes IA = cover + soporte visual.** No para texto/datos
- **Mínimo 3,000 palabras.** Nadie en RD hace posts de esta extensión — es nuestra ventaja
- **Español para el artículo.** Labels UI (Table of contents, Share on) en inglés como NoGood
- **UN keyword principal por post.** No atacar todo en un artículo
- **Verificar CSS infografías** antes de crear. No duplicar si ya existen
