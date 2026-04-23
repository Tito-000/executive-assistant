---
name: wwp
description: Use when someone asks to generate a Winner's Writing Process (WWP), crear copy estratégico basado en MKR+TPA, o hacer WWP para SEO/Google Ads/GMB/Meta Ads/landing.
argument-hint: [cliente] [canal: seo|google-ads|gmb|meta|landing|otro]
disable-model-invocation: true
---

# Skill: /wwp

**Invocación:** `/wwp [cliente] [canal]`

Ejemplos:
- `/wwp crystalline-dynamics seo`
- `/wwp anabel-mercedes landing`
- `/wwp memorama google-ads`

Este skill genera un Winner's Writing Process (WWP) específico por canal, usando el MKR y TPA existentes del proyecto como input. NO se inventa nada — se lee avatares, objeciones, lenguaje de mercado y ángulos ganadores de los docs ya producidos.

---

## PASO 0 — Verificar inputs obligatorios

Antes de arrancar, localiza estos archivos en el proyecto del cliente:

1. **MKR (Market Research):**
   - `projects/clientes/activos/[cliente]/research/market-research/MKR-*.md`
   - O `projects/[cliente]/**/MKR-*.md`

2. **TPA (Top Player Analysis):**
   - `projects/clientes/activos/[cliente]/research/top-player-analysis/TPA-*.md`

3. **Briefing del cliente:**
   - `projects/clientes/activos/[cliente]/briefing/respuestas-briefing.md` o equivalente

4. **Template WWP:** `templates/WWP-winners-writing-process.md`

**Si falta MKR o TPA:** detener y avisar al usuario. El WWP sin esos docs se construye sobre suposiciones, no sobre investigación.

**Si falta briefing:** continuar pero avisar que se construye con info limitada.

---

## PASO 1 — Clarificar el canal y objetivo

Si el usuario ya especificó canal en `$2`, usarlo. Si no, preguntar con AskUserQuestion:

**¿Para qué canal es este WWP?**
- `seo` — Posicionamiento orgánico en Google (service pages, blog, pillar content)
- `google-ads` — Campañas pagadas (Search + LSA + Retargeting)
- `gmb` — Google My Business (Map Pack, reviews, posts, Q&A)
- `meta` — Facebook/Instagram Ads (creativos + copy)
- `landing` — Una landing page específica
- `otro` — Especificar (ej: email, WhatsApp, YouTube)

Cada canal tiene su propio flujo de awareness y sofisticación → se adapta el template.

---

## PASO 2 — Leer los inputs

Leer (en paralelo cuando sea posible):
- MKR completo del cliente
- TPA completo del cliente
- Briefing del cliente
- Template WWP base

Extraer y anotar:
- **Avatares** (con nombre, edad, historia, lenguaje interno)
- **Estado doloroso** (citas textuales)
- **Estado de ensueño** (citas textuales)
- **Objeciones** (frase textual + cómo neutralizar)
- **Ángulo ganador** (de Parte 3 del TPA)
- **USPs del cliente** (del briefing)
- **Must-haves del funnel** (del TPA)
- **Gaps del mercado** (del TPA)

---

## PASO 3 — Escribir el WWP adaptado al canal

Usar el template `templates/WWP-winners-writing-process.md` como base, pero adaptar las secciones según el canal:

### Si canal = `seo`
- **Business Objective:** rankear en top 3 orgánico para keywords comerciales + informacionales del cliente
- **Funnel:** Google Search → Landing orgánica → Form/Call → Estimado → Cierre
- **Market Awareness:** típicamente 2-3 (conocen el problema, investigando soluciones)
- **Secciones extra obligatorias al final:**
  - **Keyword Mapping** — tabla: keyword | volumen | intent | página target | H1 sugerido
  - **Pillars + Clusters** — arquitectura de contenido (pillar pages + artículos satélites)
  - **Schema Markup recomendado** — LocalBusiness, Service, FAQ, BreadcrumbList
  - **Meta titles + meta descriptions** por página crítica (60/160 caracteres)
  - **On-page checklist** — H1, H2s, alt text, internal linking, CTA placement

### Si canal = `google-ads`
- **Business Objective:** leads calificados al costo más bajo por conversión
- **Funnel:** Google Search/LSA → Landing dedicada → Form/Call → Estimado → Cierre
- **Market Awareness:** típicamente 3-4 (conocen solución, buscan proveedor)
- **Secciones extra obligatorias al final (según tipo de campaña decidido):**
  - **LSA (Local Services Ads):** perfil copy, categorías, highlights, respuestas rápidas plantillas
  - **Search Ads:** ad groups (por intención) → 15 headlines + 4 descriptions responsive + extensiones (callout, sitelink, structured snippet, call)
  - **Retargeting Display:** audiencias (visitors, abandoned form) + creativos banner estáticos con copy
  - **Negative keywords** — lista inicial
  - **Landing page mapping** — qué campaña manda a qué URL
  - **Budget split** por tipo de campaña

### Si canal = `gmb`
- **Business Objective:** aparecer en top 3 del Map Pack de Google para queries locales
- **Funnel:** Google Search (mobile principalmente) → GMB listing → Call/Directions/Website
- **Market Awareness:** típicamente 3-4 (alta intención local inmediata)
- **Secciones extra obligatorias al final:**
  - **Categoría primaria + secundarias** recomendadas
  - **Business description** (750 caracteres máximo, bilingüe si aplica)
  - **Services** listados con descripciones cortas
  - **Posts template** — 4 tipos: Update, Offer, Event, Product — con ejemplos de 1 mes de cadencia
  - **Reviews strategy** — template de pedido al cliente + templates de respuesta (5★, 4★, ≤3★)
  - **Q&A preemptivo** — preguntas sembradas y respondidas
  - **Photos strategy** — qué tipo, cuántas, cadencia
  - **Attributes** a activar (accessibility, amenities, etc.)

### Si canal = `meta`
- **Business Objective:** leads o ventas desde audiencias frías/tibias/calientes
- **Funnel:** Ad → Landing/DM → Qualify → Cierre
- **Market Awareness:** típicamente 1-2 (interrupción en feed, bajo intent)
- **Secciones extra obligatorias al final:**
  - **3 ángulos creativos** (dolor / deseo / urgencia) — 3 hooks cada uno
  - **Audiencias** (intereses, lookalikes, custom, geo, demografía)
  - **Formatos creativos** (imagen, carrusel, reel si hay video) + copy primary/headline/description
  - **Placements** recomendados
  - **UGC / testimoniales** a grabar

### Si canal = `landing`
- **Business Objective:** convertir visitante en lead calificado
- **Funnel:** Tráfico (ads/orgánico) → Landing → Form/WhatsApp → Cierre
- **Market Awareness:** depende del origen del tráfico
- **Secciones extra obligatorias al final:**
  - **Wireframe sección por sección** con copy textual en cada bloque
  - **Hero** (headline, subhead, CTA, hero image)
  - **CTAs secundarios** distribuidos
  - **Prueba social** (dónde, qué tipo)
  - **FAQ** con 6-10 preguntas clave
  - **Form fields** mínimos vs nice-to-have
  - **Mobile-first considerations**

### Si canal = `otro`
- Pedir al usuario que especifique el canal y ajustar template en conversación.

---

## PASO 4 — Guardar el output

**Ruta de output:**
```
projects/clientes/activos/[cliente]/research/wwp/WWP-[NN]-[canal].md
```

Numeración:
- 01 → SEO orgánico
- 02 → Google Ads
- 03 → GMB
- 04 → Meta Ads
- 05 → Landing principal
- (numerar en orden de creación si hay múltiples landings/canales)

Si la carpeta `wwp/` no existe, crearla.

---

## PASO 5 — Validación final

Checklist antes de entregar:

- [ ] El WWP referencia al menos 1 avatar específico del MKR (con nombre)
- [ ] Incluye 3+ objeciones textuales del MKR con su respuesta
- [ ] El ángulo ganador del TPA está reflejado en headlines/copy
- [ ] Usa el lenguaje del mercado (citas reales, no genérico)
- [ ] La sección específica del canal está completa (keywords para SEO, ad groups para Ads, etc.)
- [ ] Cada pieza de copy es usable tal cual (no placeholder)
- [ ] Output guardado en la ruta correcta

---

## Notas

- **No inventar data.** Si el MKR/TPA no cubre algo, escribir: "No hay data para esto — requiere validación con cliente".
- **Idioma:** español por defecto. Si el mercado target es inglés (ej: Ocala FL), el copy del canal se escribe en inglés pero las secciones de análisis pueden estar en español.
- **Bilingüe:** si el briefing especifica audiencia bilingüe, generar copy en ambos idiomas explícitamente.
- **Reusar investigación:** NO volver a hacer research web. El MKR/TPA ya cubrió eso. Si Martin pide research adicional, usar `/market-research` o `/top-player-analysis` aparte.
- **Tiempo esperado:** 15-25 minutos por WWP canal.
