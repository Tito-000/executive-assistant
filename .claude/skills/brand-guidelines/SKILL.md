---
name: brand-guidelines
description: Use when someone asks to create brand guidelines, a brand poster, a brand kit visual, or a style guide for a client or business.
argument-hint: [nombre del negocio o cliente]
disable-model-invocation: true
---

## What This Skill Does

Genera un poster visual de **Brand Guidelines** (HTML + PNG) para cualquier negocio o cliente. Produce dos archivos:
1. `brand-guidelines.html` — poster visual de una página con toda la identidad de marca
2. `brand-guidelines.png` — screenshot en alta resolución (2x) del HTML

## Inputs Requeridos

Antes de generar, recopilar del usuario (preguntar lo que falte):

| Input | Descripción | Ejemplo |
|-------|-------------|---------|
| **Nombre del negocio** | Nombre completo | "Anabel Mercedes" |
| **Logo** | Monograma, texto, o imagen. Si es monograma: letras + estilo | "AM" en DM Serif Display dentro de un círculo |
| **Colores** | Mínimo 4, máximo 8. Nombre + hex code | Navy #1A1F2E, Sage #6B8868 |
| **Tipografías** | 1-3 Google Fonts. Nombre + pesos usados | DM Serif Display (Regular), Montserrat (300-800) |
| **Estilo de botones** | Forma, colores, sombra, estados | Rectangular, sin border-radius, box-shadow brutalista |
| **Texto de CTA** | El texto que va en los botones de ejemplo | "Conoce la oportunidad →" |
| **Iconos** | Estilo de iconografía (outline, filled, stroke width) | Outline, stroke-width 1.5, sage color |

**Opcionales:**
- Tagline del negocio
- Clearspace rules
- Variaciones del logo (fondos claros/oscuros/color)

## Steps

### 1. Recopilar datos

Si `$ARGUMENTS` contiene el nombre del negocio, buscar si ya existe un proyecto en `projects/clientes/$ARGUMENTS/` con brand assets definidos (landing pages, logos, colores). Extraer lo que se pueda automáticamente.

Preguntar al usuario **solo lo que no se pueda inferir** de los archivos existentes.

### 2. Generar el HTML

Crear `brand-guidelines.html` siguiendo esta estructura exacta:

```
POSTER (max-width: 900px, fondo del color principal oscuro)
├── HEADER
│   ├── "BRAND" (bold) + "GUIDELINES" (light, color secundario)
│   └── Logo circle (esquina derecha)
│
├── GRID (2 columnas)
│   ├── LEFT
│   │   ├── Company Logo (logo principal grande + nombre debajo)
│   │   ├── Logo Clearspace (demo con zonas marcadas + regla)
│   │   └── Typography (preview "Ab" + nombre + pesos + caracteres × cada font)
│   │
│   └── RIGHT
│       ├── Logo Variations (3 variaciones: fondo oscuro, claro, color)
│       ├── Brand Palette (grid 2 cols: swatch circle + nombre + hex × cada color)
│       ├── Iconography Style (row de 6 icon boxes con SVG inline)
│       └── Button Style (3 estados: default, hover, secondary)
│
└── FOOTER
    ├── "[Nombre] — Brand Guidelines [año]"
    └── "Confidential"
```

**Reglas de diseño:**
- Google Fonts cargadas via `<link>` (preconnect + stylesheet)
- CSS variables para todos los colores de marca
- Fondo del poster: color más oscuro de la paleta
- Labels de sección: uppercase, letter-spacing 3px, con bullet circle antes
- Todo self-contained en un solo archivo HTML (inline CSS, SVG icons inline)
- Sin JavaScript
- Sin imágenes externas (todo CSS + SVG)

**Template de referencia:** Usar [brand-guidelines-template.html](brand-guidelines-template.html) como base y adaptar colores, tipografías, logo y contenido.

### 3. Generar el PNG

Usar Chrome headless para capturar el HTML:

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu \
  --screenshot="[ruta]/brand-guidelines.png" \
  --window-size=1200,2400 \
  --force-device-scale-factor=2 \
  "file://[ruta]/brand-guidelines.html"
```

Si Chrome no está disponible, intentar `qlmanage -t -s 1200 -o [dir] [archivo]` como fallback.

### 4. Guardar archivos

Ubicación por defecto: `projects/clientes/[nombre-cliente]/brand-kit/`

Archivos generados:
- `brand-guidelines.html`
- `brand-guidelines.png`

### 5. Abrir para revisión

Abrir el HTML en el navegador para que el usuario lo revise:
```bash
open "[ruta]/brand-guidelines.html"
```

Mostrar también el PNG inline para preview rápido.

## Output

Dos archivos en la carpeta `brand-kit/` del proyecto del cliente:

| Archivo | Descripción |
|---------|-------------|
| `brand-guidelines.html` | Poster visual interactivo (fonts cargadas, se ve en cualquier browser) |
| `brand-guidelines.png` | Imagen estática alta resolución (2x) para compartir/imprimir |

## Notes

- El HTML debe verse bien como poster estático — no necesita responsive ni interactividad
- Todos los colores deben usar CSS custom properties (`:root { --nombre: #hex; }`)
- Los iconos son SVG inline con el color de acento de la marca
- Si el negocio ya tiene una landing page o logo en el proyecto, extraer colores y tipografías de ahí automáticamente
- No inventar colores ni tipografías — usar solo los que el cliente tiene definidos
- El PNG se genera a 2x para alta resolución
