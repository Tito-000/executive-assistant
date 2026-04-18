# Plan de Ejecución — Crystalline Dynamics (Fence Growth System)

**Cliente:** Andri Ramírez · Crystalline Dynamics, Inc.
**Contrato:** 2026-04-15
**Duración:** 12 semanas
**Fecha inicio:** 2026-04-16 (día después del kickoff)
**PM:** Martin Mercedes
**Tool:** Motion

---

## Cómo usar este documento

Cada tarea tiene:
- **Título** (exacto para pegar a Motion)
- **Descripción** (objetivo + por qué)
- **Subtareas** (checklist ejecutable)
- **Deadline** relativo al inicio del proyecto
- **Assignee** (Martin o Andri)
- **Tiempo estimado**
- **Dependencias** (qué tiene que estar listo antes)
- **Recursos** (links, templates, paths)

Copia cada bloque tarea-por-tarea a Motion AI. Formato en Markdown — Motion AI lo lee directo.

---

# FASE 1 · FOUNDATION (Semanas 1–2)

---

## TAREA 1 · Confirmar nombre comercial y dominio con el cliente

**Descripción:** Cerrar la decisión entre "Davenport Fence Co." (davenportfence.com) vs "Polk County Fence Co." (polkcountyfence.co). Sin esto nada arranca.

**Subtareas:**
- [ ] Enviar WhatsApp a Andri con las 2 opciones + explicación corta
- [ ] Confirmar decisión por escrito
- [ ] Verificar disponibilidad final del dominio elegido en Cloudflare
- [ ] Documentar decisión en `projects/clientes/activos/crystalline-dynamics/README.md`

**Assignee:** Martin
**Deadline:** Día 1 (2026-04-16)
**Tiempo:** 30 min
**Dependencias:** Kickoff completado
**Recursos:** slide 6 del kickoff deck

---

## TAREA 2 · Registrar dominio en Cloudflare

**Descripción:** Comprar el dominio elegido y dejarlo apuntando a Cloudflare. Esto habilita DNS, SSL y CDN gratis.

**Subtareas:**
- [ ] Login en Cloudflare con cuenta MM Agency
- [ ] Domain Registration → comprar dominio elegido
- [ ] Configurar WHOIS privacy (gratis en Cloudflare)
- [ ] Confirmar DNS nameservers activos
- [ ] Guardar factura en `contratos/gastos/dominio-crystalline.pdf`
- [ ] Enviar confirmación a Andri con screenshot

**Assignee:** Martin
**Deadline:** Día 2 (2026-04-17)
**Tiempo:** 30 min
**Dependencias:** Tarea 1
**Recursos:** API key Cloudflare en memoria (cloudflare-api.md)

---

## TAREA 3 · Enviar briefing (.docx) a Andri y hacer seguimiento

**Descripción:** Que Andri llene el briefing de 15 secciones. Sin briefing completo el copy, el research y la estrategia van a ciegas.

**Subtareas:**
- [ ] Enviar `briefing-crystalline-fence.docx` por WhatsApp + email
- [ ] Grabar Loom corto (2 min) explicando cómo llenarlo
- [ ] Deadline claro: 3 días hábiles
- [ ] Follow-up día 2 si no hay respuesta
- [ ] Follow-up día 3 con call de 20 min si sigue sin llenarlo
- [ ] Archivar briefing lleno en `briefing/briefing-lleno-andri.docx`

**Assignee:** Martin (envío) + Andri (completar)
**Deadline:** Día 5 (2026-04-20)
**Tiempo:** 45 min Martin + 60 min Andri
**Dependencias:** Ninguna
**Recursos:** `projects/clientes/activos/crystalline-dynamics/briefing/briefing-crystalline-fence.docx`

---

## TAREA 4 · Recopilar assets del cliente (fotos + logo si existe)

**Descripción:** Necesitamos mínimo 20 fotos HD de trabajos de fence terminados. Sin fotos reales, web y GMB se ven genéricos y convierten mal.

**Subtareas:**
- [ ] Lista clara a Andri de lo que necesitamos:
  - 20+ fotos HD de cercos instalados (vinyl, chain link, wood, aluminum, pool)
  - Fotos antes/después si hay
  - Foto del equipo trabajando
  - Foto de Andri (para sección "About")
  - Logo actual si existe (cualquier formato)
  - Testimonios en video/texto de clientes pasados
- [ ] Crear carpeta compartida en Google Drive
- [ ] Recibir assets
- [ ] Revisar calidad (descartar fotos borrosas/mala luz)
- [ ] Organizar en `assets/fotos/{tipo-de-fence}/`

**Assignee:** Andri (envío) + Martin (organización)
**Deadline:** Día 7 (2026-04-22)
**Tiempo:** 2h Andri + 1h Martin
**Dependencias:** Ninguna
**Recursos:** Google Drive MM Agency

---

## TAREA 5 · Keyword Research profundo

**Descripción:** Identificar 30-50 keywords objetivo clasificadas por intención (informacional/transaccional/local) y por tipo de fence.

**Subtareas:**
- [ ] Buscar en Keywords Everywhere + SERP Checker:
  - "fence contractor [ciudad]" × 6 ciudades (Davenport, Haines City, Lakeland, Winter Haven, Kissimmee, Polk County)
  - "vinyl fence installation [ciudad]"
  - "pool fence [ciudad]"
  - "chain link fence [ciudad]"
  - "wood fence [ciudad]"
  - "aluminum fence [ciudad]"
  - "fence repair [ciudad]"
  - "fence company near me"
- [ ] Exportar CSVs de cada búsqueda
- [ ] Consolidar en Excel con columnas: keyword, volumen, dificultad, CPC, intención, prioridad
- [ ] Clasificar top 15 keywords principales (para páginas)
- [ ] Clasificar top 30 long-tail (para blog)
- [ ] Documentar en `research/keyword-research/keywords-maestro.xlsx`

**Assignee:** Martin
**Deadline:** Día 7 (2026-04-22)
**Tiempo:** 4h
**Dependencias:** Ninguna
**Recursos:** API Keywords Everywhere: 49bc2a219b8ee31c6424

---

## TAREA 6 · Top Player Analysis (TPA) completo

**Descripción:** Analizar los 5 competidores top identificados para extraer su estrategia ganadora: qué páginas tienen, qué ofertas usan, qué copy, qué CTAs, qué reseñas.

**Subtareas:**
- [ ] Scrape manual de los 5 sitios top
- [ ] Mapear estructura de páginas de cada uno
- [ ] Extraer copy de home, página de servicio, página de ciudad
- [ ] Identificar CTAs y ofertas principales
- [ ] Capturar pricing (si está público)
- [ ] Analizar reseñas más valiosas de cada uno (qué dicen los clientes)
- [ ] Identificar gaps y oportunidades
- [ ] Documentar en `research/top-player-analysis/tpa-completo.md` siguiendo template TPA

**Assignee:** Martin
**Deadline:** Día 10 (2026-04-25)
**Tiempo:** 6h
**Dependencias:** Ninguna
**Recursos:** `templates/TPA-top-player-analysis.md`

---

## TAREA 7 · Market Research (MKR) completo

**Descripción:** Definir audiencia, dolor, deseo, creencias, objeciones y avatar del cliente ideal de Andri. Esto alimenta todo el copy y ads.

**Subtareas:**
- [ ] Entrevistar a Andri por 45 min (grabar)
- [ ] Preguntar: ¿quiénes son tus mejores clientes? ¿qué les dolió antes de contratarte? ¿qué esperaban? ¿qué objeciones te ponen?
- [ ] Leer 30+ reseñas de competidores en Davenport (qué valoran, qué odian)
- [ ] Definir 1-2 avatares específicos con demográficos, psicográficos, dolor, deseo
- [ ] Documentar en `research/market-research/mkr-crystalline.md`

**Assignee:** Martin + Andri (entrevista)
**Deadline:** Día 10 (2026-04-25)
**Tiempo:** 5h
**Dependencias:** Tarea 3 (briefing base)
**Recursos:** `templates/MKR-market-research.md`

---

## TAREA 8 · Winner's Writing Process (WWP)

**Descripción:** Definir niveles de conciencia, mecanismo único, customer journey y ángulos de copy basado en MKR + TPA.

**Subtareas:**
- [ ] Niveles de conciencia (frío/tibio/caliente) de la audiencia
- [ ] Mecanismo único de Crystalline (qué los hace diferentes)
- [ ] Customer journey completo (awareness → conversion)
- [ ] 10 ángulos de copy para ads
- [ ] 5 hooks principales para headlines
- [ ] Documentar en `research/wwp/wwp-crystalline.md`

**Assignee:** Martin
**Deadline:** Día 12 (2026-04-27)
**Tiempo:** 4h
**Dependencias:** Tareas 6 y 7
**Recursos:** `templates/WWP-winners-writing-process.md`

---

## TAREA 9 · Crear Google Business Profile (GBP)

**Descripción:** GBP es el activo #1 para rankear en Map Pack. Sin GBP Crystalline es invisible en 70% de búsquedas.

**Subtareas:**
- [ ] Crear cuenta en business.google.com
- [ ] Nombre: definitivo (según Tarea 1)
- [ ] Categoría primaria: Fence contractor
- [ ] Categorías secundarias: Service establishment, Repair service
- [ ] Dirección: 43344 US-27 S, Unit H, Davenport, FL 33837
- [ ] Teléfono: (863) 377-0928
- [ ] Web: dominio elegido (una vez comprado)
- [ ] Horario completo
- [ ] Service Areas: Davenport, Haines City, Lakeland, Winter Haven, Kissimmee
- [ ] Descripción 750 caracteres con keywords principales
- [ ] Cargar 15 servicios identificados en Local Scan
- [ ] Cargar 20+ fotos (Tarea 4)
- [ ] Solicitar verificación (postal/video)
- [ ] Documentar accesos en `recursos-ia/api-keys/crystalline-gbp.md`

**Assignee:** Martin
**Deadline:** Día 10 (2026-04-25)
**Tiempo:** 2.5h
**Dependencias:** Tareas 1 y 4
**Recursos:** `research/top-player-analysis/local-scan-davenport-2026-04-15.md`

---

# FASE 2 · LANZAMIENTO (Semanas 3–4)

---

## TAREA 10 · Wireframe + estructura del sitio

**Descripción:** Definir qué páginas tiene el sitio y qué contiene cada una antes de programar nada.

**Subtareas:**
- [ ] Estructura hub-and-spoke:
  - Home (/)
  - Páginas de ciudad: /davenport-fl, /haines-city-fl, /lakeland-fl, /winter-haven-fl, /kissimmee-fl, /polk-county-fl
  - Páginas de servicio: /vinyl-fence, /chain-link-fence, /wood-fence, /aluminum-fence, /pool-fence, /commercial-fence
  - Páginas utility: /about, /contact, /gallery, /free-estimate
  - Blog: /blog (estructura, sin posts aún)
- [ ] Wireframe en Figma de cada tipo de página
- [ ] Definir CTAs (formulario + click-to-call + WhatsApp)
- [ ] Aprobar con Andri

**Assignee:** Martin
**Deadline:** Día 14 (2026-04-29)
**Tiempo:** 6h
**Dependencias:** Tarea 8

---

## TAREA 11 · Copywriting completo del sitio

**Descripción:** Escribir todo el copy basado en WWP. Home, 6 páginas de ciudad, 6 páginas de servicio, utility pages.

**Subtareas:**
- [ ] Home: hero, servicios, por qué Crystalline, proceso, testimonios, FAQ, CTA final
- [ ] Templates de páginas de ciudad (se duplica con variación local)
- [ ] Templates de páginas de servicio (se duplica con variación de producto)
- [ ] About page con historia de Andri
- [ ] Contact page con formulario + mapa
- [ ] Revisar con Andri

**Assignee:** Martin
**Deadline:** Día 16 (2026-05-01)
**Tiempo:** 10h
**Dependencias:** Tarea 10

---

## TAREA 12 · Desarrollo web

**Descripción:** Construir el sitio. Stack: HTML/CSS/JS puro + Cloudflare Pages (igual que Anabel).

**Subtareas:**
- [ ] Setup repo GitHub
- [ ] Implementar home
- [ ] Implementar templates de ciudad y servicio
- [ ] Implementar páginas utility
- [ ] Formulario con GHL webhook
- [ ] Click-to-call + WhatsApp buttons
- [ ] SEO on-page: title, meta, H1, schema markup LocalBusiness
- [ ] Sitemap.xml + robots.txt
- [ ] Deploy a Cloudflare Pages
- [ ] Apuntar dominio
- [ ] Test mobile/desktop

**Assignee:** Martin
**Deadline:** Día 22 (2026-05-07)
**Tiempo:** 20h
**Dependencias:** Tareas 10, 11, 4
**Recursos:** GitHub token en memoria (github-token.md)

---

## TAREA 13 · Tracking: GA4 + Google Tag Manager + eventos

**Descripción:** Sin tracking no sabemos qué funciona. Instalar antes de lanzar ads.

**Subtareas:**
- [ ] Crear propiedad GA4 para el dominio
- [ ] Crear contenedor GTM
- [ ] Instalar GTM en el sitio
- [ ] Configurar eventos clave:
  - Form submit (lead)
  - Click en WhatsApp
  - Click en teléfono
  - Scroll 75%
  - Time on page > 60s
- [ ] Configurar conversiones en GA4
- [ ] Conectar GA4 con Google Ads
- [ ] Test con Tag Assistant

**Assignee:** Martin
**Deadline:** Día 23 (2026-05-08)
**Tiempo:** 3h
**Dependencias:** Tarea 12

---

## TAREA 14 · Setup de Google Ads (campañas)

**Descripción:** Estructurar campañas búsqueda geo-targeted con grupos de anuncios por tipo de fence.

**Subtareas:**
- [ ] Crear cuenta Google Ads (si no existe)
- [ ] Conectar con tarjeta de Andri directo
- [ ] Campaign structure:
  - Campaign 1: Search — Davenport FL (broad)
  - Campaign 2: Search — Tipos de fence específicos
  - Campaign 3: Performance Max (después de 30 días con data)
- [ ] Ad groups por tipo (vinyl, chain link, wood, pool, aluminum)
- [ ] 3 anuncios responsive por ad group
- [ ] Keywords: phrase + exact match
- [ ] Negative keywords (diy, cheap, free, jobs, etc.)
- [ ] Geo-targeting: 25 millas de Davenport
- [ ] Conversion tracking conectado
- [ ] Budget inicial: $30–50/día = $1,000–1,500/mes
- [ ] Lanzar en horario 7am–9pm

**Assignee:** Martin
**Deadline:** Día 25 (2026-05-10)
**Tiempo:** 5h
**Dependencias:** Tareas 12 y 13

---

## TAREA 15 · Cobrar segundo desembolso ($550)

**Descripción:** Al entregar sitio en vivo se cobra el 50% restante del setup.

**Subtareas:**
- [ ] Preparar factura
- [ ] Enviar link de pago (Stripe o transferencia)
- [ ] Confirmar pago recibido
- [ ] Actualizar tracking de ingresos

**Assignee:** Martin + Andri
**Deadline:** Día 25 (2026-05-10)
**Tiempo:** 30 min
**Dependencias:** Tarea 12 (sitio en vivo)

---

# FASE 3 · OPTIMIZACIÓN (Semanas 5–8) — menos detalle, ajustar con data

---

## TAREA 16 · Citations en 15 directorios principales

**Descripción:** Sembrar NAP (nombre, dirección, teléfono) consistente en 15+ directorios para backlinks locales.

**Subtareas:** crear perfil completo en: Yelp, BBB, Angi, HomeAdvisor, Yellow Pages, Foursquare, Nextdoor, Manta, Chamber of Commerce Davenport, MapQuest, Bing Places, Apple Maps, Thumbtack, Porch, Houzz.

**Assignee:** Martin
**Deadline:** Semana 6
**Tiempo:** 6h

---

## TAREA 17 · Sistema de reseñas

**Descripción:** QR + link directo + automatización WhatsApp post-servicio. Meta: 10 reseñas mes 1, 50 en 90 días.

**Subtareas:** crear QR code, plantilla WhatsApp, automatización GHL, tarjetas impresas para equipo de campo, tracking semanal.

**Assignee:** Martin (setup) + Andri (ejecución con cada cliente)
**Deadline:** Semana 5
**Tiempo:** 3h setup

---

## TAREA 18 · Posts GMB semanales

**Descripción:** 2-3 posts por semana en Google Business Profile (promos, trabajos recientes, Q&A).

**Subtareas:** calendario editorial, templates de posts, imágenes, publicar.

**Assignee:** Martin
**Deadline:** Continuo desde Semana 5
**Tiempo:** 30 min/semana

---

## TAREA 19 · Optimización de Google Ads

**Descripción:** Revisar data semanal y ajustar bids, keywords negativas, ads con bajo CTR.

**Subtareas:** revisión semanal de search terms, pausar keywords sin conversión, ajustar pujas, A/B test de anuncios.

**Assignee:** Martin
**Deadline:** Continuo desde Semana 5
**Tiempo:** 2h/semana

---

## TAREA 20 · Primer blog post SEO

**Descripción:** Escribir y publicar primer blog sobre tema long-tail (ej: "How much does a vinyl fence cost in Davenport FL").

**Subtareas:** keyword research specific, brief de 1500 palabras, redacción, imágenes, interlink, publicar.

**Assignee:** Martin
**Deadline:** Semana 7
**Tiempo:** 4h

---

# FASE 4 · ESCALAMIENTO (Semanas 9–12)

---

## TAREA 21 · Link building local

**Descripción:** Conseguir 5-10 backlinks de calidad de negocios locales (pool builders, realtors, landscapers, Davenport Chamber).

**Subtareas:** lista de targets, outreach con propuesta de intercambio, confirmar links publicados, tracking.

**Assignee:** Martin
**Deadline:** Semana 10
**Tiempo:** 8h

---

## TAREA 22 · Segundo y tercer blog post

**Descripción:** Mantener ritmo de contenido SEO (2 posts por mes).

**Assignee:** Martin
**Deadline:** Semanas 9 y 11
**Tiempo:** 4h cada uno

---

## TAREA 23 · Primer reporte trimestral

**Descripción:** Reporte completo de KPIs: leads, CPL, conversiones, rankings, reseñas, tráfico. Entregar en video Loom + PDF.

**Subtareas:** data collection, análisis, gráficos, conclusiones, recomendaciones fase 2, video Loom presentando.

**Assignee:** Martin
**Deadline:** Semana 12
**Tiempo:** 4h

---

## TAREA 24 · Call de renovación + plan Fase 2

**Descripción:** Presentar reporte, mostrar ROI y cerrar renovación para próximos 3 meses con ajustes.

**Subtareas:** agendar call, preparar deck de renovación, propuesta de scope fase 2, cerrar.

**Assignee:** Martin
**Deadline:** Semana 12
**Tiempo:** 1.5h call + 2h prep

---

# RESUMEN DE CARGA

| Fase | Semanas | Tareas | Horas Martin | Horas Andri |
|------|---------|--------|--------------|-------------|
| 1 · Foundation | 1–2 | 9 | ~30h | ~4h |
| 2 · Lanzamiento | 3–4 | 6 | ~45h | ~2h |
| 3 · Optimización | 5–8 | 5 | ~25h (ongoing) | ~2h/sem |
| 4 · Escalamiento | 9–12 | 4 | ~20h | ~1h |
| **TOTAL** | **12 sem** | **24** | **~120h** | **~15h** |

---

# HITOS CRÍTICOS (no pueden fallar)

1. **Día 2** — Dominio registrado
2. **Día 10** — GBP creado y en verificación
3. **Día 22** — Sitio en vivo
4. **Día 25** — Google Ads lanzadas + $550 cobrado
5. **Día 60** — Primeras 10 reseñas
6. **Día 90** — Top 10 orgánico en Davenport
7. **Día 84** — Reporte trimestral + renovación

---

**Fecha de creación:** 2026-04-15
**Última actualización:** 2026-04-15
**Próxima revisión:** después del kickoff call
