# Plan Detallado de Ejecución — Crystalline Dynamics
**Cliente:** Andri Ramírez · Crystalline Dynamics, Inc.
**Inicio:** 2026-04-16 · **Duración:** 12 semanas · **PM:** Martin Mercedes

---

# 🟢 FASE 1 · FOUNDATION (Semanas 1–2)

---

## TAREA 1 · Confirmar nombre comercial y dominio
**Assignee:** Martin · **Deadline:** 2026-04-16 · **Tiempo:** 30 min · **Dependencias:** Kickoff

**Subtareas:**
- [ ] 1.1 Abrir conversación de WhatsApp con Andri
- [ ] 1.2 Enviar mensaje con las 2 opciones: A) Davenport Fence Co. / davenportfence.com B) Polk County Fence Co. / polkcountyfence.co
- [ ] 1.3 Esperar respuesta (máx 4 horas, sino llamar)
- [ ] 1.4 Confirmar disponibilidad del dominio elegido en cloudflare.com/products/registrar
- [ ] 1.5 Si no está disponible: presentar 3 alternativas backup en 1 hora
- [ ] 1.6 Capturar screenshot de la confirmación de Andri
- [ ] 1.7 Actualizar README.md con la decisión final
- [ ] 1.8 Notificar al equipo (commit en git con mensaje "decisión: nombre + dominio confirmados")

---

## TAREA 2 · Registrar dominio en Cloudflare
**Assignee:** Martin · **Deadline:** 2026-04-17 · **Tiempo:** 30 min · **Dependencias:** Tarea 1

**Subtareas:**
- [ ] 2.1 Login Cloudflare con cuenta MM Agency (api key en cloudflare-api.md)
- [ ] 2.2 Navegar a Domain Registration
- [ ] 2.3 Buscar dominio confirmado en Tarea 1
- [ ] 2.4 Comprar (precio aprox $9.77/año .com / $30/año .co)
- [ ] 2.5 Activar WHOIS privacy (gratis)
- [ ] 2.6 Verificar nameservers Cloudflare activos
- [ ] 2.7 Crear registros DNS placeholder: A record @ → 192.0.2.1 (temporal hasta deploy)
- [ ] 2.8 Descargar factura PDF
- [ ] 2.9 Guardar en `contratos/gastos/dominio-crystalline.pdf`
- [ ] 2.10 Enviar screenshot a Andri vía WhatsApp con mensaje "Dominio registrado ✅"

---

## TAREA 3 · Briefing — envío y seguimiento
**Assignee:** Martin (envío) + Andri (completar) · **Deadline:** 2026-04-20 · **Tiempo:** 45 min M + 60 min A

**Subtareas:**
- [ ] 3.1 Localizar archivo: `briefing/briefing-crystalline-fence.docx`
- [ ] 3.2 Grabar Loom de 2 min explicando: "abre en Word, cada caja es clickeable, escribe dentro, guarda"
- [ ] 3.3 Subir Loom a unlisted
- [ ] 3.4 Enviar por WhatsApp: archivo .docx + link Loom + mensaje "tienes 3 días para llenarlo"
- [ ] 3.5 Enviar también por email como backup
- [ ] 3.6 Recordatorio en Día +2 (2026-04-18): "¿cómo va el briefing?"
- [ ] 3.7 Recordatorio en Día +3 (2026-04-19): proponer call de 20 min para llenarlo juntos
- [ ] 3.8 Al recibirlo: descargar y archivar en `briefing/briefing-lleno-andri.docx`
- [ ] 3.9 Leer completo y resaltar gaps de info
- [ ] 3.10 Anotar dudas para preguntar en próxima call

---

## TAREA 4 · Recopilar assets visuales del cliente
**Assignee:** Andri (envío) + Martin (organización) · **Deadline:** 2026-04-22 · **Tiempo:** 2h A + 1h M

**Subtareas:**
- [ ] 4.1 Crear carpeta Google Drive: "Crystalline Dynamics - Assets"
- [ ] 4.2 Estructura: `/fotos-cercos/{vinyl,chain-link,wood,aluminum,pool}/`, `/equipo/`, `/andri/`, `/logo/`, `/testimonios/`
- [ ] 4.3 Compartir link con Andri (permiso editor)
- [ ] 4.4 Enviar checklist exacto a Andri por WhatsApp:
  - 5 fotos vinyl fence (HD, mín 2000px ancho)
  - 5 fotos chain link
  - 5 fotos wood fence
  - 3 fotos aluminum
  - 3 fotos pool fence
  - 2 fotos equipo trabajando
  - 1 foto profesional de Andri
  - Logo actual (PNG/SVG si tiene)
  - 3 testimonios escritos o video de clientes pasados
- [ ] 4.5 Recordatorio Día +3 si no ha subido nada
- [ ] 4.6 Al recibir: revisar calidad (descartar borrosas, baja luz, watermark ajeno)
- [ ] 4.7 Renombrar archivos con convención: `vinyl-01.jpg`, `pool-02.jpg`, etc
- [ ] 4.8 Comprimir con TinyPNG si están sobre 2MB
- [ ] 4.9 Copiar a `assets/fotos/{tipo}/` en repo del proyecto
- [ ] 4.10 Si faltan fotos: hacer lista de stock photos backup en Unsplash/Pexels

---

## TAREA 5 · Keyword Research profundo (50+ keywords)
**Assignee:** Martin · **Deadline:** 2026-04-22 · **Tiempo:** 4h · **API:** Keywords Everywhere `49bc2a219b8ee31c6424`

**Subtareas:**
- [ ] 5.1 Crear archivo Excel: `research/keyword-research/keywords-maestro.xlsx`
- [ ] 5.2 Columnas: keyword | volumen mensual | difficulty | CPC | intención (info/trans/local) | tipo (ciudad/servicio/long-tail) | prioridad (1-5) | URL destino
- [ ] 5.3 **Ronda 1 — Keywords de ciudad** (buscar cada una en Google con Keywords Everywhere activo):
  - "fence contractor Davenport FL"
  - "fence contractor Haines City FL"
  - "fence contractor Lakeland FL"
  - "fence contractor Winter Haven FL"
  - "fence contractor Kissimmee FL"
  - "fence contractor Polk County FL"
  - "fence company Davenport"
  - "fence installation Davenport"
- [ ] 5.4 **Ronda 2 — Keywords de servicio** (combinar cada tipo con Davenport):
  - "vinyl fence installation Davenport FL"
  - "wood fence Davenport FL"
  - "chain link fence Davenport FL"
  - "aluminum fence Davenport FL"
  - "pool fence Davenport FL"
  - "commercial fence Davenport FL"
  - "fence repair Davenport FL"
- [ ] 5.5 **Ronda 3 — Long-tail (para blog):**
  - "how much does a vinyl fence cost in Florida"
  - "best fence for hurricane Florida"
  - "pool fence requirements Florida law"
  - "wood vs vinyl fence Florida"
  - "permit fence Davenport FL"
  - "how long does it take to install a fence"
  - "fence company near me reviews"
  - 20 long-tail más usando "People Also Ask" de Keywords Everywhere
- [ ] 5.6 Exportar CSV de cada búsqueda → guardar en `research/keyword-research/csv-exports/`
- [ ] 5.7 Consolidar todo en el Excel maestro
- [ ] 5.8 Filtrar: descartar keywords con volumen <10/mes O dificultad >50
- [ ] 5.9 Marcar top 15 "money keywords" (alta intención + volumen razonable) → estas van a páginas
- [ ] 5.10 Marcar top 30 long-tail → estas van a blog posts
- [ ] 5.11 Asignar URL destino a cada money keyword (ej: "vinyl fence Davenport" → /vinyl-fence)

---

## TAREA 6 · Top Player Analysis (TPA) de los 5 competidores
**Assignee:** Martin · **Deadline:** 2026-04-25 · **Tiempo:** 6h

**Subtareas:**
- [ ] 6.1 Lista de los 5 competidores a analizar:
  - Fence Central (fencecentralfl.com) — líder en reseñas
  - Pro Master Fencing — local directo
  - Evu Cleaning & Fence — local directo
  - Summerlin Fence — veterano
  - Superior Fence & Rail — cadena nacional
- [ ] 6.2 Para cada competidor, capturar y documentar:
  - **Estructura del sitio:** mapa de todas las páginas (sitemap.xml o Screaming Frog)
  - **Home page:** screenshot full + extraer hero, propuesta de valor, CTA principal, prueba social
  - **Página de servicio principal:** copy completo, fotos usadas, FAQs
  - **Página de ciudad si tiene:** copy y estructura
  - **Reseñas en Google:** leer top 20 reseñas y extraer 5 quotes que mejor venden
  - **Pricing:** ¿lo muestran? ¿en rangos? ¿oculto?
  - **Ofertas/promos:** descuentos, garantías, financiamiento
  - **Tracking instalado:** revisar source code → ¿tienen GA4? GTM? Pixel? CallRail?
- [ ] 6.3 Crear archivo `research/top-player-analysis/tpa-competidor-01-fence-central.md`
- [ ] 6.4 Repetir para 02, 03, 04, 05
- [ ] 6.5 Crear `research/top-player-analysis/tpa-resumen-ejecutivo.md` con:
  - Patrones que repiten todos (ej: "todos ofrecen Free Estimate")
  - Gaps que nadie cubre (oportunidades para Crystalline)
  - Mejores hooks de copy encontrados (lista de 10)
  - Mejores CTAs encontrados (lista de 5)
  - Servicios que no estamos ofreciendo y deberíamos

---

## TAREA 7 · Market Research (MKR)
**Assignee:** Martin + Andri · **Deadline:** 2026-04-25 · **Tiempo:** 5h · **Dep:** Tarea 3

**Subtareas:**
- [ ] 7.1 Agendar call de 45 min con Andri (Zoom, grabar)
- [ ] 7.2 Preguntas guion para la entrevista:
  - ¿Quién fue tu mejor cliente del último año? Descríbemelo
  - ¿Qué tipo de cerco compró? ¿Por cuánto?
  - ¿Cómo te encontró?
  - ¿Qué le dolía antes de llamarte?
  - ¿Por qué te eligió a ti y no a otro?
  - ¿Qué objeciones más comunes te ponen?
  - ¿Cuál es la queja típica que escuchas sobre tu competencia?
  - ¿Hombre o mujer suelen llamar? Edad promedio
  - ¿Casa propia o renta?
  - ¿Compran solos o consultan con pareja?
  - ¿En qué época del año vendes más?
- [ ] 7.3 Transcribir entrevista (Otter.ai o Whisper)
- [ ] 7.4 Leer 30+ reseñas en Google de los 5 competidores top
- [ ] 7.5 Extraer en Excel: palabras exactas que usa la audiencia para describir dolor y deseo (voice of customer)
- [ ] 7.6 Definir Avatar #1 — Homeowner típico:
  - Demográfico: género, edad, ingresos, hijos
  - Psicográfico: miedos, deseos, valores
  - Trigger event que dispara la compra
  - Objeciones top 3
  - Dónde busca info (Google, Facebook groups, Nextdoor)
- [ ] 7.7 Definir Avatar #2 — si aplica (ej: contractor que subcontrata, dueño de Airbnb)
- [ ] 7.8 Documentar en `research/market-research/mkr-crystalline.md` siguiendo template

---

## TAREA 8 · Winner's Writing Process (WWP)
**Assignee:** Martin · **Deadline:** 2026-04-27 · **Tiempo:** 4h · **Dep:** Tareas 6 y 7

**Subtareas:**
- [ ] 8.1 Definir 3 niveles de conciencia de la audiencia:
  - Frío: no sabe que necesita cerco (raro en fence)
  - Tibio: sabe que quiere cerco, está comparando opciones/empresas
  - Caliente: ya pidió 2 cotizaciones, está listo para decidir
- [ ] 8.2 Mecanismo único de Crystalline (qué los hace diferentes):
  - Brainstorm 10 candidatos (ej: "instalación en 7 días garantizada", "garantía 10 años en vinyl", etc)
  - Validar con Andri cuál es real y sostenible
  - Elegir 1 mecanismo principal + 2 secundarios
- [ ] 8.3 Customer Journey (5 etapas):
  - Awareness: cómo llega al sitio (Google search, ad, referido)
  - Interest: qué lee primero (home, página de servicio)
  - Consideration: qué compara (precio, reviews, fotos)
  - Decision: qué empuja a llamar (CTA, urgencia, oferta)
  - Action: qué pasa post-formulario (auto-respuesta, llamada de Andri)
- [ ] 8.4 Crear 10 ángulos de copy para Google Ads:
  - "Free estimate in 24 hours"
  - "Licensed & insured Davenport fence pros"
  - "10-year warranty on vinyl"
  - 7 más basados en MKR
- [ ] 8.5 Crear 5 hooks principales para headlines del sitio
- [ ] 8.6 Documentar en `research/wwp/wwp-crystalline.md`

---

## TAREA 9 · Crear Google Business Profile (GBP)
**Assignee:** Martin · **Deadline:** 2026-04-25 · **Tiempo:** 2.5h · **Dep:** Tareas 1, 4

**Subtareas:**
- [ ] 9.1 Ir a business.google.com → "Add business"
- [ ] 9.2 **Nombre exacto:** el confirmado en Tarea 1 (sin extras)
- [ ] 9.3 **Categoría primaria:** Fence contractor
- [ ] 9.4 **Categorías secundarias:** Service establishment + Repair service
- [ ] 9.5 **Dirección:** 43344 US-27 S, Unit H, Davenport, FL 33837
- [ ] 9.6 **Teléfono:** (863) 377-0928
- [ ] 9.7 **Web:** dominio comprado en Tarea 2
- [ ] 9.8 **Horario:** Lun-Sáb 7am–7pm, Dom cerrado (confirmar con Andri)
- [ ] 9.9 **Service Areas:** Davenport, Haines City, Lakeland, Winter Haven, Kissimmee, Polk County
- [ ] 9.10 **Descripción 750 caracteres** con keywords principales (escribir tipo: "Crystalline Fence is Davenport's trusted fence contractor specializing in vinyl, chain link, wood, aluminum and pool fence installation. Serving Polk County since [año]. Free estimates. Licensed & insured.")
- [ ] 9.11 **Servicios** (cargar los 15 del Local Scan):
  - Vinyl fence installation
  - Chain link fence installation
  - Wood fence installation
  - Aluminum fence installation
  - Pool fence installation
  - Privacy fence installation
  - Commercial fencing
  - Gate installation & repair
  - Fence repair
  - (otros 6 del Local Scan)
- [ ] 9.12 **Atributos:** Family-owned, Veteran-owned (si aplica), Free estimates, Online estimates
- [ ] 9.13 Subir logo (de Tarea 4)
- [ ] 9.14 Subir 20 fotos categorizadas (exterior, interior, team, work)
- [ ] 9.15 Solicitar verificación (postal recomendado, llega en 5–14 días)
- [ ] 9.16 Documentar credenciales en `recursos-ia/api-keys/crystalline-gbp.md`
- [ ] 9.17 Compartir acceso con Andri como "Manager" (no Owner)

---

# 🟡 FASE 2 · LANZAMIENTO (Semanas 3–4)

---

## TAREA 10 · Wireframe + arquitectura de información
**Assignee:** Martin · **Deadline:** 2026-04-29 · **Tiempo:** 6h · **Dep:** Tarea 8

**Subtareas:**
- [ ] 10.1 Crear archivo Figma: "Crystalline Dynamics - Wireframes"
- [ ] 10.2 Definir sitemap final:
  - / (Home)
  - /davenport-fl, /haines-city-fl, /lakeland-fl, /winter-haven-fl, /kissimmee-fl, /polk-county-fl
  - /vinyl-fence, /chain-link-fence, /wood-fence, /aluminum-fence, /pool-fence, /commercial-fence
  - /about, /contact, /gallery, /free-estimate, /reviews
  - /blog (estructura)
  - /thank-you (post form submit)
- [ ] 10.3 Wireframe Home (secciones): Hero + Trust bar + Servicios + Why us + Process + Reviews + Gallery + FAQ + Final CTA + Footer
- [ ] 10.4 Wireframe template Página de Ciudad
- [ ] 10.5 Wireframe template Página de Servicio
- [ ] 10.6 Wireframe About, Contact, Free Estimate, Gallery
- [ ] 10.7 Definir CTAs primarios (Free Estimate form) y secundarios (call, WhatsApp)
- [ ] 10.8 Definir lead magnet si aplica (ej: "Pricing Guide PDF")
- [ ] 10.9 Compartir Figma con Andri y pedir feedback en 24h
- [ ] 10.10 Iterar 1 ronda de cambios

---

## TAREA 11 · Copywriting completo del sitio
**Assignee:** Martin · **Deadline:** 2026-05-01 · **Tiempo:** 10h · **Dep:** Tarea 10

**Subtareas:**
- [ ] 11.1 Crear doc Google: "Crystalline Copy - Master"
- [ ] 11.2 **Home (1 versión):**
  - Hero headline (10 palabras max) + subheadline + CTA primario
  - Trust bar: licensed/insured/years/jobs done
  - 6 cards de servicios (1 frase cada uno)
  - Why Crystalline (3-5 puntos diferenciadores del WWP)
  - Process en 4 pasos (call → estimate → install → enjoy)
  - 6 reviews (sacar de las que se vayan recolectando)
  - FAQ con 8 preguntas (sacadas de Google "People Also Ask")
  - CTA final
- [ ] 11.3 **Template Página de Ciudad** (6 variaciones):
  - Hero específico: "Fence Contractor in [CIUDAD], FL"
  - Por qué [ciudad] necesita Crystalline (1 párrafo local)
  - Servicios disponibles
  - Mapa + service area
  - Reviews de clientes en [ciudad]
  - CTA
- [ ] 11.4 **Template Página de Servicio** (6 variaciones):
  - Hero: "[TIPO] Fence Installation in Davenport"
  - Beneficios del tipo de fence (5 bullets)
  - Materiales y opciones
  - Pricing range si aplica
  - Galería de proyectos de ese tipo
  - FAQ específica
  - CTA
- [ ] 11.5 About: historia de Andri, misión, foto, equipo
- [ ] 11.6 Contact: form + info + mapa + horario
- [ ] 11.7 Free Estimate page: form expandido + qué esperar
- [ ] 11.8 Gallery: estructura grid con categorías
- [ ] 11.9 Thank you page: confirmación + qué sigue + WhatsApp
- [ ] 11.10 Meta titles y meta descriptions de las 20+ páginas (optimizadas para keyword + CTR)
- [ ] 11.11 Revisar con Andri y aprobar

---

## TAREA 12 · Desarrollo web
**Assignee:** Martin · **Deadline:** 2026-05-07 · **Tiempo:** 20h · **Dep:** 10, 11, 4

**Subtareas:**
- [ ] 12.1 Crear repo GitHub privado: `crystalline-fence-site`
- [ ] 12.2 Setup local: HTML/CSS/JS puro (mismo stack que Anabel)
- [ ] 12.3 Estructura de carpetas: `/`, `/css/`, `/js/`, `/img/`, `/blog/`
- [ ] 12.4 Diseñar sistema de design tokens (colores, fuentes, spacing)
- [ ] 12.5 Implementar Header (sticky, con nav + CTA)
- [ ] 12.6 Implementar Footer (contact + service areas + social)
- [ ] 12.7 Construir Home page completa
- [ ] 12.8 Construir template Página de Ciudad → duplicar 6 veces con variación
- [ ] 12.9 Construir template Página de Servicio → duplicar 6 veces
- [ ] 12.10 Construir About, Contact, Gallery, Free Estimate, Thank You
- [ ] 12.11 Estructura blog: index + post template (sin posts aún)
- [ ] 12.12 Form de contacto con webhook a GHL (lead → CRM)
- [ ] 12.13 Botones flotantes: WhatsApp + click-to-call
- [ ] 12.14 SEO on-page: title, meta, H1, alt en imágenes, schema.org LocalBusiness JSON-LD
- [ ] 12.15 Crear sitemap.xml con todas las URLs
- [ ] 12.16 Crear robots.txt
- [ ] 12.17 Optimizar imágenes (WebP + lazy load)
- [ ] 12.18 Test Lighthouse: Performance >85, SEO >95, Accessibility >90
- [ ] 12.19 Test mobile responsive (iPhone, iPad, Android)
- [ ] 12.20 Test cross-browser (Chrome, Safari, Firefox)
- [ ] 12.21 Deploy a Cloudflare Pages
- [ ] 12.22 Conectar dominio (DNS records en Cloudflare)
- [ ] 12.23 Forzar HTTPS + WWW redirect
- [ ] 12.24 Validar sitemap en Google Search Console
- [ ] 12.25 Submit a indexación

---

## TAREA 13 · Tracking — GA4 + GTM + Conversiones
**Assignee:** Martin · **Deadline:** 2026-05-08 · **Tiempo:** 3h · **Dep:** Tarea 12

**Subtareas:**
- [ ] 13.1 Crear cuenta GA4 para el dominio
- [ ] 13.2 Crear contenedor GTM (Web)
- [ ] 13.3 Instalar snippet GTM en `<head>` y `<body>` del sitio
- [ ] 13.4 Configurar GA4 base tag dentro de GTM
- [ ] 13.5 Crear los siguientes triggers en GTM:
  - Form Submit (selector del form de contacto)
  - Click en botón WhatsApp
  - Click en link `tel:`
  - Scroll 75%
  - Time on page > 60s
  - Click en CTA Free Estimate
- [ ] 13.6 Crear tags GA4 Event para cada trigger:
  - `lead_form_submit`
  - `whatsapp_click`
  - `phone_click`
  - `engaged_scroll`
  - `engaged_time`
  - `cta_estimate_click`
- [ ] 13.7 Marcar `lead_form_submit`, `whatsapp_click`, `phone_click` como conversiones en GA4
- [ ] 13.8 Conectar GA4 con Google Ads (linking)
- [ ] 13.9 Importar conversiones de GA4 a Google Ads
- [ ] 13.10 Test con Tag Assistant + GA4 DebugView
- [ ] 13.11 Publicar contenedor GTM
- [ ] 13.12 Verificar 24h después que data fluye correctamente
- [ ] 13.13 Documentar IDs en `web/tracking-ids.md`

---

## TAREA 14 · Setup de Google Ads (3 campañas, 5 ad groups, 15 anuncios)
**Assignee:** Martin · **Deadline:** 2026-05-10 · **Tiempo:** 5h · **Dep:** 12, 13

**Subtareas:**

### Estructura
- [ ] 14.1 Crear cuenta Google Ads (si Andri no tiene)
- [ ] 14.2 Conectar tarjeta de Andri (billing directo a su cuenta)
- [ ] 14.3 Conectar GA4 + Search Console
- [ ] 14.4 Linkear GBP (para ext de location)

### Campaña 1 — Search General Davenport
- [ ] 14.5 Crear Campaign 1: "SRC - Davenport - General"
- [ ] 14.6 Tipo: Search · Goal: Leads · Budget: $20/día
- [ ] 14.7 Geo: 25 millas around Davenport, FL 33837
- [ ] 14.8 Schedule: Lun-Sáb 7am-9pm
- [ ] 14.9 Bidding: Maximize Conversions (cambiar a tCPA después de 30 conv)
- [ ] 14.10 Ad group "Fence Contractor General":
  - Keywords (phrase + exact):
    - "fence contractor davenport"
    - "fence company davenport"
    - "fence installation davenport"
    - "fence installer near me"
    - "davenport fence company"
  - Negative keywords: diy, cheap, free, jobs, salary, parts, supplies, repair only

### Campaña 2 — Search por Tipo de Fence
- [ ] 14.11 Crear Campaign 2: "SRC - Davenport - Fence Types"
- [ ] 14.12 Budget: $25/día
- [ ] 14.13 Mismo geo y schedule
- [ ] 14.14 Ad group "Vinyl":
  - Keywords: "vinyl fence davenport", "vinyl fence installation florida", "white vinyl fence"
  - Anuncio 1: HL "Vinyl Fence Davenport FL" / "Free Estimate Today" / "Licensed & Insured"
  - Anuncio 2: HL "Premium Vinyl Fence" / "10-Year Warranty" / "Local Davenport Pros"
  - Anuncio 3: HL "Vinyl Fence Installation" / "Fast Install in 7 Days" / "Get Your Free Quote"
- [ ] 14.15 Ad group "Pool Fence":
  - Keywords: "pool fence davenport", "pool safety fence florida", "child safe pool fence"
  - Anuncio 1: HL "Pool Safety Fence" / "Florida Code Compliant" / "Protect Your Family"
  - Anuncio 2: HL "Pool Fence Installation" / "Mesh & Aluminum Options" / "Free On-Site Estimate"
  - Anuncio 3: HL "Davenport Pool Fence Pros" / "Same Week Install" / "Licensed & Insured"
- [ ] 14.16 Ad group "Wood":
  - Keywords + 3 anuncios similares
- [ ] 14.17 Ad group "Chain Link":
  - Keywords + 3 anuncios similares
- [ ] 14.18 Ad group "Aluminum":
  - Keywords + 3 anuncios similares

### Extensiones (aplica a ambas campañas)
- [ ] 14.19 Sitelinks: Free Estimate, Vinyl, Pool, Reviews, Gallery, Contact
- [ ] 14.20 Callouts: Licensed & Insured, Free Estimates, 10-Year Warranty, Local Davenport
- [ ] 14.21 Structured snippets (Services): Vinyl, Wood, Chain Link, Pool, Aluminum, Commercial
- [ ] 14.22 Call extension con teléfono de Andri (861-377-0928)
- [ ] 14.23 Location extension (linkeado a GBP)
- [ ] 14.24 Lead form extension con campos: Name, Phone, Type of Fence

### Tracking
- [ ] 14.25 Conversion: Lead Form Submit (importada de GA4)
- [ ] 14.26 Conversion: Phone Call (call extension)
- [ ] 14.27 Conversion: WhatsApp Click

### Lanzamiento
- [ ] 14.28 Pausar Campaign 3 (PMax) — esperar 30 días con data
- [ ] 14.29 Activar Campaign 1 y 2
- [ ] 14.30 Notificar a Andri: "Ads en vivo, esperar primeros leads en 24-48h"
- [ ] 14.31 Configurar reporte automático semanal a su email

---

## TAREA 15 · Cobrar segundo desembolso ($550)
**Assignee:** Martin + Andri · **Deadline:** 2026-05-10 · **Tiempo:** 30 min · **Dep:** Tarea 12

**Subtareas:**
- [ ] 15.1 Confirmar que sitio está vivo y accesible
- [ ] 15.2 Generar invoice $550 (Stripe Invoice o factura manual)
- [ ] 15.3 Enviar por WhatsApp + email con mensaje "Sitio en vivo ✅ — link de pago adjunto"
- [ ] 15.4 Si paga por transferencia: enviar info bancaria
- [ ] 15.5 Confirmar pago recibido
- [ ] 15.6 Enviar recibo
- [ ] 15.7 Actualizar tracking de ingresos: `references/gastos-api.csv` o sheet de revenue MM Agency

---

# 🟠 FASE 3 · OPTIMIZACIÓN (Semanas 5–8)

---

## TAREA 16 · Citations en 15 directorios
**Assignee:** Martin · **Deadline:** Semana 6 · **Tiempo:** 6h

**Subtareas:**
- [ ] 16.1 Crear "NAP card" — documento con datos exactos a usar en todos los directorios:
  - Nombre exacto + dirección + teléfono + web + categoría + horario + descripción de 250 char
- [ ] 16.2 Crear perfiles uno por uno (30 min cada uno):
  - Yelp Business
  - BBB (Better Business Bureau)
  - Angi (antes Angie's List)
  - HomeAdvisor
  - Yellow Pages
  - Foursquare
  - Nextdoor Business
  - Manta
  - Davenport Chamber of Commerce
  - MapQuest
  - Bing Places for Business
  - Apple Maps Business Connect
  - Thumbtack
  - Porch
  - Houzz Pro
- [ ] 16.3 En cada uno: usar el mismo NAP exacto (consistencia es clave para Google)
- [ ] 16.4 Subir mismo logo + 5 fotos
- [ ] 16.5 Documentar credenciales de cada perfil en `seo/citations-credenciales.md`
- [ ] 16.6 Crear tracker en Excel: directorio | URL del perfil | fecha creado | status verificación

---

## TAREA 17 · Sistema de captura de reseñas
**Assignee:** Martin (setup) + Andri (ejecución) · **Deadline:** Semana 5 · **Tiempo:** 3h setup

**Subtareas:**
- [ ] 17.1 Generar URL corta de Google Reviews del GBP
- [ ] 17.2 Generar QR code apuntando a esa URL (usar qr-code-generator.com)
- [ ] 17.3 Diseñar tarjeta física tamaño business card: "¿Te gustó nuestro trabajo? Escanea y déjanos una reseña" + QR
- [ ] 17.4 Imprimir 200 tarjetas (Vistaprint)
- [ ] 17.5 Crear plantilla mensaje WhatsApp post-instalación: "Hola [name], gracias por confiar en nosotros! Si quedaste contento ¿podrías dejarnos una reseña? Aquí el link: [url]"
- [ ] 17.6 Crear automatización en GHL: cuando job se marca "completed" → envía WhatsApp en 24h
- [ ] 17.7 Crear plantilla email follow-up 5 días después si no dejó reseña
- [ ] 17.8 Entrenar a Andri y equipo: dar tarjeta + pedir reseña al terminar cada job
- [ ] 17.9 Tracker semanal: # reseñas nuevas, # estrellas promedio
- [ ] 17.10 Meta: 10 reseñas en 30 días, 50 en 90 días

---

## TAREA 18 · Posts GMB semanales (calendario editorial)
**Assignee:** Martin · **Deadline:** Continuo desde Semana 5 · **Tiempo:** 30 min/semana

**Subtareas:**
- [ ] 18.1 Crear calendario editorial 4 semanas adelantado en Google Sheets
- [ ] 18.2 Plantillas de tipos de posts:
  - Lunes: "Job of the week" (foto antes/después + breve descripción)
  - Miércoles: Q&A o tip ("Did you know vinyl fence lasts 30+ years?")
  - Viernes: Promo/CTA ("Free estimates this week — book now")
- [ ] 18.3 Banco de imágenes para reusar (de Tarea 4)
- [ ] 18.4 Cada post debe incluir: imagen + 100-150 palabras + CTA + 2-3 emojis
- [ ] 18.5 Programar 4 semanas en una sola sesión cada mes (1.5h)
- [ ] 18.6 Tracking: views, clicks, calls por post

---

## TAREA 19 · Optimización semanal de Google Ads
**Assignee:** Martin · **Deadline:** Continuo desde Semana 5 · **Tiempo:** 2h/semana

**Subtareas (cada lunes):**
- [ ] 19.1 Revisar Search Terms report → agregar nuevas negative keywords
- [ ] 19.2 Pausar keywords con 0 conversiones después de $50 invertidos
- [ ] 19.3 Aumentar bids en keywords con CPA bajo
- [ ] 19.4 Revisar performance por anuncio → pausar el peor de cada ad group
- [ ] 19.5 Crear nuevo anuncio para reemplazar el pausado (A/B testing continuo)
- [ ] 19.6 Revisar Auction Insights → ¿quién compite más?
- [ ] 19.7 Ajustar geo bidding (subir % en zonas que convierten más)
- [ ] 19.8 Documentar cambios en log: `ads/log-optimizaciones.md`

---

## TAREA 20 · Primer blog post SEO
**Assignee:** Martin · **Deadline:** Semana 7 · **Tiempo:** 4h

**Subtareas:**
- [ ] 20.1 Elegir keyword del top 30 long-tail (Tarea 5) — ej: "vinyl fence cost Davenport FL"
- [ ] 20.2 Brief del post (objetivo, audiencia, ángulo, keyword principal + 5 LSI, CTA)
- [ ] 20.3 Investigar top 5 resultados de Google para esa keyword
- [ ] 20.4 Outline con 8-12 H2 que cubra todo lo que cubren los competidores + un ángulo único
- [ ] 20.5 Escribir 1500-2000 palabras
- [ ] 20.6 Insertar 3-5 imágenes con alt text optimizado
- [ ] 20.7 Internal links a 3 páginas relevantes del sitio
- [ ] 20.8 CTA al final + form embebido
- [ ] 20.9 Meta title + meta description + URL friendly
- [ ] 20.10 Publicar + submit a indexación
- [ ] 20.11 Compartir en GBP como post

---

# 🔴 FASE 4 · ESCALAMIENTO (Semanas 9–12)

---

## TAREA 21 · Link building local (5-10 backlinks)
**Assignee:** Martin · **Deadline:** Semana 10 · **Tiempo:** 8h

**Subtareas:**
- [ ] 21.1 Crear lista target (30 negocios complementarios):
  - 10 pool builders en Polk County
  - 10 realtors locales
  - 5 landscapers
  - 5 home builders
- [ ] 21.2 Identificar contacto + email de cada uno
- [ ] 21.3 Plantilla outreach de intercambio:
  - "Hola [nombre], soy de Crystalline. Vi que ustedes hacen [servicio]. Cuando un cliente nos pide cerco para piscina, los recomendaríamos. ¿Estás abierto a intercambio de referidos + link en nuestras webs?"
- [ ] 21.4 Enviar 30 outreach
- [ ] 21.5 Seguimiento día 3 y día 7
- [ ] 21.6 Negociar links con los que respondan
- [ ] 21.7 Confirmar links publicados (verificar URL en su sitio)
- [ ] 21.8 Tracker: backlinks conseguidos | DA del sitio | tipo de link (dofollow/nofollow)
- [ ] 21.9 Inscribirse en Davenport Chamber of Commerce ($250 inversión)
- [ ] 21.10 Verificar que el link de la cámara está activo

---

## TAREA 22 · Blog posts #2 y #3
**Assignee:** Martin · **Deadline:** Semanas 9 y 11 · **Tiempo:** 4h cada uno

**Subtareas (replicar de Tarea 20 con 2 keywords nuevas):**
- [ ] 22.1 Post #2: "Wood vs Vinyl Fence in Florida — Which is Better?"
- [ ] 22.2 Post #3: "Pool Fence Requirements in Florida (2026 Guide)"

---

## TAREA 23 · Reporte trimestral
**Assignee:** Martin · **Deadline:** Semana 12 · **Tiempo:** 4h

**Subtareas:**
- [ ] 23.1 Recopilar data:
  - Total leads generados (form + WhatsApp + call)
  - CPL (costo por lead)
  - Conversion rate del sitio
  - Total invertido en ads
  - Ranking actual de top 10 keywords
  - Reseñas conseguidas
  - Tráfico orgánico vs paid
- [ ] 23.2 Crear deck PDF (10 slides): summary, KPIs, qué funcionó, qué no, recomendaciones fase 2
- [ ] 23.3 Grabar video Loom de 10 min presentando el reporte
- [ ] 23.4 Enviar reporte + Loom por WhatsApp y email
- [ ] 23.5 Agendar call de 30 min para discutir

---

## TAREA 24 · Call de renovación + plan Fase 2
**Assignee:** Martin · **Deadline:** Semana 12 · **Tiempo:** 1.5h call + 2h prep

**Subtareas:**
- [ ] 24.1 Preparar deck de renovación: ROI mostrado + propuesta scope fase 2
- [ ] 24.2 Calcular ROI honesto (leads × valor promedio - inversión)
- [ ] 24.3 Definir scope fase 2 con ajustes basados en data:
  - ¿Más ad spend?
  - ¿Más blog posts?
  - ¿Email marketing?
  - ¿Retargeting?
- [ ] 24.4 Pricing fase 2 (mantener $397/mo o ajustar)
- [ ] 24.5 Enviar contrato renovación
- [ ] 24.6 Cobrar primer mes
- [ ] 24.7 Si no renueva: hacer offboarding limpio + pedir testimonio

---

# 📊 RESUMEN

| Fase | Tareas | Subtareas totales | Horas Martin | Horas Andri |
|------|--------|-------------------|--------------|-------------|
| 1 | 9 | ~85 | ~30h | ~4h |
| 2 | 6 | ~95 | ~45h | ~2h |
| 3 | 5 | ~50 | ~25h+ongoing | ~2h/sem |
| 4 | 4 | ~25 | ~20h | ~1h |
| **TOTAL** | **24** | **~255** | **~120h** | **~15h** |

# 🎯 HITOS CRÍTICOS

1. **Día 2 (2026-04-17)** — Dominio registrado
2. **Día 5 (2026-04-20)** — Briefing devuelto
3. **Día 10 (2026-04-25)** — GBP creado + en verificación
4. **Día 22 (2026-05-07)** — Sitio en vivo
5. **Día 25 (2026-05-10)** — Google Ads lanzadas + $550 cobrado
6. **Día 60 (2026-06-15)** — 10 reseñas en GBP
7. **Día 84 (2026-07-09)** — Reporte trimestral + renovación cerrada
