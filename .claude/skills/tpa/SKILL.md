---
name: tpa
description: Use when someone asks to generate a Top Player Analysis (TPA), analizar un competidor a profundidad, o hacer research competitivo estilo Ana Cantera (perfil completo + offer stack + value ladder + diagnóstico).
argument-hint: [top-player] [cliente opcional]
disable-model-invocation: true
---

# Skill: /tpa

**Invocación:** `/tpa [top-player] [cliente opcional]`

Ejemplos:
- `/tpa ana-cantera` — análisis standalone
- `/tpa frazer-brookes immunotec` — top player en contexto de un cliente
- `/tpa superior-fence-rail crystalline-dynamics` — competidor local de un cliente

Este skill genera un **Top Player Analysis (TPA) profundo de 1 top player** — perfil completo, ecosistema de negocio, value ladder, copy patterns, nurturing y diagnóstico estratégico. NO es comparativa superficial de 4 competidores — es autopsia de UNO para extraer lecciones.

El formato de referencia es `outputs/research/TPA-ana-cantera.md` (12 partes).

---

## PASO 0 — Verificar inputs y ubicación de output

1. **Confirmar el top player:** nombre completo, dominio principal, handles de redes principales.
2. **Confirmar si hay cliente asociado:**
   - Con cliente: `projects/clientes/activos/[cliente]/research/top-player-analysis/TPA-[top-player].md`
   - Sin cliente: `outputs/research/TPA-[top-player].md`
3. Si ya existe un TPA para ese top player, leerlo y preguntar: "Ya hay un TPA de [top player]. ¿Actualizar con research nuevo o empezar de cero?"

---

## PASO 1 — Entrevista de clarificación (solo si falta contexto)

Si el briefing del cliente o la solicitud ya cubre esto, saltar. Si no, preguntar con AskUserQuestion:

1. **¿Quién es el top player?** — nombre, dominio, handle principal
2. **¿Por qué este top player?** — ¿es competidor directo del cliente? ¿referente aspiracional? ¿player que queremos superar?
3. **¿Qué buscamos aprender?** — ¿su funnel? ¿su copy? ¿su pricing? ¿dónde es vulnerable?
4. **¿Mercado / geo?** — ¿local, nacional, internacional? ¿qué idioma?

---

## PASO 2 — Investigación web profunda (15-25 búsquedas mínimo)

No se llena el TPA con suposiciones. Se investiga en fuentes reales. Usar WebSearch + WebFetch agresivamente.

### 2A — Ejes de búsqueda obligatorios

1. **Biografía / perfil personal:**
   - `[nombre] biography age net worth`
   - `[nombre] wikipedia`
   - `[nombre] interview podcast`
   - Foros de la industria (ej: BusinessForHome para MLM, Clutch para agencias, Angi/HomeAdvisor para servicios)

2. **Trayectoria profesional:**
   - `[nombre] career history`
   - `[nombre] [industria] ranks rewards`
   - `[nombre] company [año actual]`

3. **Redes sociales y audiencia:**
   - `[nombre] instagram followers engagement`
   - `[nombre] youtube subscribers`
   - `[nombre] tiktok`
   - Usar herramientas/fuentes de stats (SpeakRJ, Social Blade, similarweb)

4. **Ecosistema de negocio (offer stack):**
   - `[nombre] products services pricing`
   - `[dominio] shop store courses`
   - `[nombre] programs courses membership`
   - Amazon shops, Linktree, vCards, landing pages de eventos

5. **Paid Ads:**
   - Meta Ad Library directo: `facebook.com/ads/library/?search=[nombre o marca]`
   - `[nombre] ads campaign`
   - Detectar pixels (Facebook, TikTok, Google) en los dominios via WebFetch

6. **Stack técnico de la web:**
   - WebFetch del dominio principal → buscar en HTML: WordPress/Shopify/Wix, theme, page builder, tracking scripts
   - Colores de marca (hex codes del CSS)

7. **Copy y tone of voice:**
   - Extraer taglines, CTAs, hero copy del sitio principal
   - Identificar frases recurrentes en sus redes
   - Transcripciones de videos clave si existen

8. **Nurturing y funnels:**
   - Suscribirse a su newsletter si posible (análisis de emails)
   - Probar formularios de captura (qué pide, qué pasa después)
   - Identificar WhatsApp/chat/call flows

### 2B — Fuentes priorizadas

- **WebFetch directo** al dominio del top player (home, about, pricing, checkout)
- **Trustpilot, BBB, Google Reviews, Glassdoor** — reseñas reales
- **Reddit, Quora, YouTube comments** — sentimiento genuino
- **Industry reports:** BusinessForHome (MLM), IBISWorld, SimilarWeb
- **Ad libraries:** Meta Ad Library, Google Ads Transparency Center, TikTok Creative Center

---

## PASO 3 — Escribir el TPA con la estructura de 12 partes

**Estructura obligatoria** (basada en TPA Ana Cantera como estándar de calidad):

```markdown
# Top Player Analysis (TPA) — [Nombre] ([@handle])

**Proyecto:** [contexto / cliente]
**Fecha de análisis:** [YYYY-MM-DD]
**Analista:** Martin Mercedes

---

## Parte 1 — Perfil Completo

### Datos Personales
- Nombre completo, fecha de nacimiento (edad), nacionalidad, ubicación
- Pareja, hijos, educación, estatura, net worth estimado

### Trayectoria Profesional
- Cronología de su carrera con fechas y logros específicos
- Rangos/títulos alcanzados, años en cada etapa
- Menciones en prensa, reality TV, reconocimientos

### Publicaciones / Libros / Cursos creados
- Ebooks, libros, cursos propios

### Fundación / Proyectos personales
- Trabajo filantrópico, proyectos paralelos

---

## Parte 2 — Presencia Digital y Audiencia

### Redes Sociales (tabla obligatoria)

| Plataforma | Handle | Seguidores | Notas |
|---|---|---|---|
| Instagram | @... | Xk | ... |
| YouTube | ... | Xk subs | ... |
| TikTok | @... | Xk | ... |
| Facebook | /... | Xk likes | ... |
| LinkedIn | ... | X conexiones | ... |

### Engagement Rate (plataforma principal)
- ER reportado
- Frecuencia de publicación
- Crecimiento estimado
- **Valoración:** benchmark vs su tamaño (ej: ER saludable para 200K es 1.5-3%)

### Observaciones Estructurales
- Fragmentación de cuentas, cross-posting, presencia subdesarrollada, etc.

---

## Parte 3 — Qué Vende (Offer Stack Completo)

**Cada línea de negocio con detalle:**

#### 1. [Línea principal de ingreso]
- Empresa, productos, modelo
- Precios específicos
- Links de compra/registro

#### 2. [Segunda línea]
- (ej: marca propia, cursos, coaching, eventos)

[...continuar con TODAS las líneas — típicamente 4-7]

---

## Parte 4 — Value Ladder / Funnels

### Value Ladder (ASCII tree de gratis → máximo valor)

```
GRATIS / BAJO COSTO
├── Contenido orgánico
├── Lead magnet
│
ENTRY LEVEL ($X-$X)
├── ...
│
MID TIER ($X-$X)
├── ...
│
HIGH TIER ($X+)
├── ...
│
MÁXIMO VALOR
├── ...
```

### Flujo de Conversión Principal (Funnel)
1. Atención
2. Interés
3. Contacto
4. Conversión inicial
5. Ascenso
6. Eventos / upsell

**Observación clave:** dependencias del funnel (WhatsApp, vivos, email, etc.)

---

## Parte 5 — Estrategia de Contenido Orgánico

### Tipo de Contenido Observado
- Categorías con ejemplos

### Frecuencia (por plataforma)

### Strengths del Contenido
### Weaknesses del Contenido

---

## Parte 6 — Paid Ads

### Meta Ad Library
- Ads activos (cantidad, tipo, creatividades)
- Si no accesible: explicar por qué

### Google Ads / Otros
- Evidencia de campañas activas

### Pixels / Tracking detectados
- Facebook Pixel ID, Google Analytics ID, TikTok Pixel, etc.

### Diagnóstico de Paid Ads
- ¿Invierte o no? ¿Estrategia evidente? ¿Oportunidad para nosotros?

---

## Parte 7 — Landing Page (dominio principal)

### Estructura Técnica
- Plataforma (WordPress/Shopify/Webflow/etc)
- Theme, page builder, LMS, e-commerce
- Tracking implementado

### Hero Section
- Tagline, subtema, CTA principal

### Colores de Marca
- Primario (#hex), Secundario (#hex), Acentos (#hex)

### Estructura del Sitio
- Páginas principales

### Puntos Fuertes
### Debilidades

---

## Parte 8 — Copy Patterns

### Frases y Ángulos Recurrentes
- Taglines, claims, frases-bandera con citas textuales

### Tone of Voice
- Registro, idioma, emociones dominantes

### Copy Angle Principal
- El mensaje central que repite (resumido en 1-2 oraciones)

---

## Parte 9 — Nurturing

### Email Marketing
- Evidencia de newsletters, secuencias automatizadas

### Remarketing Ads
- Pixels instalados ≠ remarketing activo. Verificar.

### WhatsApp / DM
- Canal de cierre, automatizaciones, flujos

### Sistema de retención interno
- Universidad, app, grupos, comunidad

---

## Parte 10 — Pricing (Tabla Resumen)

| Producto/Servicio | Precio |
|---|---|
| ... | ... |

---

## Parte 11 — Point of Parity (Qué Hace Igual Que Todos)

Lista de lo que hace como cualquier otro en su industria. Esto nos dice dónde NO diferenciarnos (es commodity) y qué damos por sentado.

---

## Parte 12 — Diagnóstico Final

### Fortalezas Principales
1. [Listado numerado 5-10 fortalezas con explicación breve]

### Debilidades (Oportunidades para Nosotros)
1. [Listado numerado 5-10 debilidades — explícitamente framed como oportunidades]

### Veredicto: ¿Mejor en Atención o Monetización?

[Párrafo analítico que responde: ¿dónde es realmente fuerte? ¿atraer audiencia o convertirla?]

**Quien implemente [X + Y + Z] puede competir directamente con [nombre] a una fracción de su audiencia.**

---

## Fuentes

- [Título del recurso](URL)
- [Título del recurso](URL)
- [...15-25 fuentes organizadas por tipo]
```

---

## PASO 4 — Guardar el output

**Ruta con cliente:**
```
projects/clientes/activos/[cliente]/research/top-player-analysis/TPA-[top-player].md
```

**Ruta standalone:**
```
outputs/research/TPA-[top-player].md
```

Si la carpeta no existe, crearla.

---

## PASO 5 — Validación final

Checklist antes de entregar:

- [ ] Las 12 partes están presentes (ninguna vacía o en placeholder)
- [ ] Parte 1 tiene datos personales verificables con fuentes
- [ ] Parte 2 tiene tabla de TODAS las redes con números reales
- [ ] Parte 3 lista ecosistema completo (mínimo 3 líneas de negocio si existen)
- [ ] Parte 4 tiene value ladder visual + funnel paso a paso
- [ ] Parte 6 tiene diagnóstico explícito de paid ads (sí/no/cómo)
- [ ] Parte 7 incluye colores de marca con hex codes extraídos del sitio
- [ ] Parte 8 tiene citas textuales de copy real (no inventado)
- [ ] Parte 10 es tabla — no prosa
- [ ] Parte 12 termina con veredicto claro "mejor en atención o monetización"
- [ ] Mínimo 15 fuentes linkeadas al final
- [ ] Output guardado en la ruta correcta

---

## Notas

- **No inventar data.** Si no encuentras algo, escribir: "No se encontraron datos verificables — requiere validación directa" o similar.
- **Citas textuales** en el idioma original (inglés/español). No traducir a menos que se pida.
- **Un TPA = un top player.** Si el cliente quiere analizar 3 competidores, ejecutar el skill 3 veces, no mezclar.
- **Tiempo esperado:** 25-45 minutos (la mayor parte es WebSearch + WebFetch).
- **Integración con modus operandi:** TPA alimenta WWP. Sin TPA (y MKR) el WWP se construye sobre suposiciones.
