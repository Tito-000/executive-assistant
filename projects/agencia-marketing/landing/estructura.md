# Plan: Landing Principal MM Agency — Estructura Estilo NoGood.io

## Context

MM Agency necesita su landing principal corporativa. Hoy solo existe un WordPress básico que no sirve. Sin esta landing, ni el inbound (embudos → landing) ni el outbound (firma de emails, link de credibilidad) pueden correr.

**Decisiones del usuario (esta sesión):**
- **Modelo de referencia:** Estructura y estética de **nogood.io** replicada sección por sección
- **Enfoque:** **Embudos de venta completos** — sistema landing + tráfico + CRM + seguimiento. NO "solo pauta". Meta Ads + Google Ads son UNA pieza del embudo, no el producto principal.
- **Objetivo único:** Llenar formulario de calificación completa (no agendar calendly directo)
- **Martin NO aparece al inicio** — la landing es 100% corporativa
- **Precios:** NO mostrar
- **Prueba social:** Mix (Memorama + Dra. Aurys con nombre + caso anónimo "85 pacientes en 60 días")
- **Estética objetivo:** Dark mode, tipografía display grande, marquees de logos, cards rounded, acento de color quirúrgico en CTAs

**Research completado:** Se extrajo la estructura exacta de nogood.io en vivo (10 secciones confirmadas desde el HTML real del sitio).

---

## Estructura de NoGood.io (referencia verificada)

```
0. Sticky Nav
1. Hero dark (H1 enorme en Microgramma + media 16:9)
2. Marquee #1 — Logos de clientes
3. What We Do — posicionamiento ("Your AI native growth squad")
4. Services List — grid 3×2 de 6 servicios en card rounded-40
5. Testimonials — slider con números grandes (879%)
6. How We Do It — 6 pilares en slider
7. Marquee #2 — Logos partners/VCs
8. FAQ accordion — 9 preguntas largas (SEO play)
9. Blog teaser + CTA final ("Ready to get up to NoGood?")
10. Footer dark con 4 ciudades + video decorativo
```

**Elementos icónicos a replicar:**
- H1 masivo en tipografía display sobre dark
- **Dos marquees infinitos de logos** (clientes arriba, partners/credenciales abajo)
- Cards `rounded-40` con border sutil "flotando" sobre fondos radiales dark
- Números grandes sueltos dentro de testimoniales
- Acento de color quirúrgico (solo en CTAs y hover)
- Wordplay con el nombre de la marca en CTAs
- FAQ larga al final como play SEO

---

## Sistema de Diseño MM Agency (adaptado de NoGood)

| Elemento | NoGood.io | MM Agency |
|---|---|---|
| Fondo principal | `#181818` (negro) | Dark (definir tono exacto en fase de diseño) |
| Fondo secundario | `#202020` (gris oscuro) | Gris oscuro un paso más claro |
| Acento CTA | `#FAFA00` (amarillo) | Color acento de MM Agency (definir — probable: un tono único del brand kit) |
| Acento secundario | `#713DFF` (morado) | Segundo color del brand kit MM Agency |
| Heading font | Microgramma D Extended | Display sans-serif condensada-wide (a elegir) |
| Body font | Suisse Int'l | Sans humanista legible (Inter/General Sans como base) |
| Border radius | `rounded-20` / `rounded-40` | Igual — radios grandes para cards "flotantes" |
| Padding vertical | `c-py-10` (~100px) | Igual — secciones respiradas |
| Animaciones | Text reveal, marquees, sliders, scroll fade, radial glows | Igual |

---

## Estructura Propuesta MM Agency — 10 Secciones (mapeo 1:1 con NoGood)

### Sección 0 — Sticky Nav

**Elementos:**
- Logo MM Agency a la izquierda
- Menú horizontal: **Servicios** · **Casos** · **Proceso** · **FAQ** · **Insights** (blog futuro)
- CTA a la derecha (botón acento): **"Contactar"** — ancla scroll al formulario
- Sticky con blur/transparencia al scroll

---

### Sección 1 — Hero Dark (equivalente a "The growth squad behind…")

**Objetivo:** Declarar la propuesta del embudo completo en los primeros 3 segundos con impacto visual tipo NoGood.

**Elementos:**
- **H1 masivo (tipografía display):** *"Embudos de venta para negocios que sí quieren crecer."*
  - Tamaño: clamp(64px, 10vw, 120px)
  - Peso bold, mayúsculas o sentence case, tracking amplio
  - Animación text reveal al cargar (fade-up palabra por palabra)
- **Sub-headline:** *"Diseñamos el sistema completo — landing, tráfico, CRM y seguimiento — para que dejes de pagar ads sin ver resultados."*
- **Media 16:9 al costado o debajo del H1:**
  - Video loopable del embudo en acción (landing → ad creative → WhatsApp entrando)
  - Si no hay video disponible → animación abstracta del flujo de conversión
  - **NO usar foto de Martin** (decisión explícita del usuario)
- **CTA implícito:** el H1 entero linkea al formulario, o botón sutil debajo del media
- **Trust bar debajo del hero (bandera de credibilidad):** *"Sistema completo, no servicios sueltos"* · *"Atención directa del fundador"* · *"Sin contratos trampa"* · *"Cuentas a tu nombre"*
- **Fondo:** dark con radial gradient oscuro, z-index de profundidad
- **Padding vertical grande** (`c-py-10` equivalente)

**Por qué funciona:** Replica el impacto del hero de NoGood. El H1 masivo declara la propuesta en una frase. El sub-headline confirma que es un sistema completo, no un servicio suelto.

---

### Sección 2 — Marquee #1: Logos de Clientes

**Objetivo:** Prueba social inmediata con logos reconocibles.

**Elementos:**
- **H2 centrado encima:** *"Negocios reales en República Dominicana que ya confían en MM Agency"*
  - Tipografía sans suisse equivalente, tamaño medio (32–48px)
- **Marquee infinito horizontal** de logos en blanco:
  - Memorama
  - Dra. Aurys Mercedes
  - Anabel Mercedes
  - (Y otros clientes actuales con permiso de uso de logo)
  - Si solo hay 3–4 logos, duplicar el array para que el marquee se sienta lleno
- **Fondo:** `bg-dark-grey-2` (un paso más claro que el hero) con border top y bottom sutiles
- **Animación:** scroll automático infinito CSS/JS, pausa en hover

**Nota crítica:** Martin debe confirmar permiso escrito de cada cliente antes de usar su logo.

---

### Sección 3 — What We Do (Posicionamiento)

**Objetivo:** Equivalente a "Your AI native growth squad" — declaración de posicionamiento en 1 frase + párrafo.

**Elementos:**
- **H2 (grande, text-left):** *"Armamos el sistema completo. Tú cuentas las ventas."*
- **P (body grande):** *"En un mercado lleno de agencias que te venden pauta suelta, MM Agency hace algo distinto: diseñamos el embudo completo que convierte visitas en clientes. Landing page que captura. Tráfico pagado que califica. CRM que organiza. Seguimiento automático que cierra. Todo conectado, todo medido, todo optimizado mes a mes. No pedazos sueltos — el sistema entero."*
- Alineación izquierda, padding vertical top grande, sin imagen
- Fondo dark con shapes animadas sutiles de fondo (overflow hidden)

**Por qué funciona:** Replica exactamente el bloque de NoGood pero con el posicionamiento de MM Agency. La declaración "todo conectado, todo medido, todo optimizado" es la firma diferenciadora del sistema completo vs servicios sueltos.

---

### Sección 4 — Services List (4 piezas del embudo)

**Objetivo:** Mostrar los 4 componentes del embudo como un sistema único. NoGood tiene 6 cards en grid 3×2; **MM Agency tiene 4 piezas = grid 2×2 o 4×1**.

**Elementos:**
- **Card container grande** con `rounded-40` y border sutil "flotando" sobre fondo radial dark
- **H2 dentro de la card:** *"Las 4 piezas del embudo. Funcionan juntas."*
- **Grid 4 columnas** (`col-lg-3` equivalente):

  **Card 1 — Landing de conversión**
  - Icono/ilustración de página/layout
  - **H3:** "Landing de conversión"
  - **P:** "La página donde entra todo el tráfico. Copy que enganchaba al tipo de cliente correcto, diseño rápido y móvil, formulario que no espanta. Optimizada con data real de cada visita — no con plantillas genéricas. Es la puerta de entrada al embudo."

  **Card 2 — Tráfico pagado**
  - Icono/ilustración de audiencia/target
  - **H3:** "Tráfico pagado"
  - **P:** "Meta Ads y Google Ads para llevar a la persona correcta a tu landing en el momento correcto. Segmentación quirúrgica, creativos que paran el scroll, y campañas de intención de compra en Search. La pauta no es el producto — es el combustible del sistema."

  **Card 3 — CRM + automatización**
  - Icono/ilustración de nodos conectados
  - **H3:** "CRM + automatización"
  - **P:** "Cada lead que entra cae en tu CRM organizado y dispara automáticamente mensajes de WhatsApp, emails de seguimiento y recordatorios al equipo. El 80% de las ventas se pierden porque nadie da seguimiento en las primeras 2 horas. Automatizado, eso no pasa."

  **Card 4 — Optimización continua**
  - Icono/ilustración de gráfica ascendente
  - **H3:** "Optimización continua"
  - **P:** "Mes a mes ajustamos landing, creativos, audiencias y secuencias con data real. Cada mes el embudo cierra más barato y más rápido. No es 'prender campañas y olvidarse' — es un sistema vivo que mejora con cada lead que entra."

- **Microanimaciones en hover** sobre cada card
- Debajo del grid: frase pequeña que ancla al formulario: *"Los 4 juntos son el embudo. Los 4 juntos es lo que contratas. En el diagnóstico gratuito definimos cómo se arma para tu negocio."*

---

### Sección 5 — Testimonials con Números Grandes (estilo NoGood "879%")

**Objetivo:** Replicar la jugada más icónica de NoGood: slider de testimoniales con **números enormes dentro de cada card**.

**Elementos:**
- **H2:** *"Negocios que ya están cerrando ventas con el embudo de MM Agency"*
- **Slider horizontal** estilo `tiny-slider` con drag (no dots tradicionales)
- **Cards rounded-20 con `bg-dark-grey` y border sutil**, padding grande
- **Estructura de cada card:**
  1. Logo del cliente arriba
  2. **NÚMERO ENORME** (tipografía display, 80–120px, acento de color)
  3. **H3 con quote corta** (1 oración)
  4. Párrafo más largo con el testimonio extendido
  5. Nombre del autor + cargo
  6. Link "Leer caso completo" (si hay caso study)

- **Cards propuestas:**

  **Card 1 — Clínica médica (caso anónimo — activo diferenciador)**
  - Logo: placeholder anónimo o "Clínica médica · RD"
  - Número enorme: **"85"**
  - Subtítulo del número: "pacientes calificados en 60 días con el embudo completo"
  - Quote: *"El formulario no paraba de llenarse."*
  - Párrafo: contexto del embudo completo (landing + tráfico + automatización de WhatsApp + CRM), sin revelar nombre/especialidad/monto

  **Card 2 — Memorama (con permiso)**
  - Logo: Memorama
  - Número enorme: [métrica concreta a confirmar con Martin]
  - Quote: corta del dueño
  - Párrafo: resultado concreto del embudo armado

  **Card 3 — Dra. Aurys Mercedes (con permiso)**
  - Logo/foto: Dra. Aurys
  - Número enorme: [métrica concreta a confirmar]
  - Quote: corta
  - Párrafo: resultado concreto del embudo armado

**Nota crítica:** Martin debe confirmar permiso + métricas reales antes de publicar.

**Por qué funciona:** El número gigante dentro de la card es el elemento visual más memorable de NoGood. Copiarlo literalmente es la jugada.

---

### Sección 6 — How We Do It (5 pilares diferenciadores)

**Objetivo:** Equivalente a "A differentiated approach to Growth" de NoGood. NoGood usa 6 pilares; MM Agency usará **5** porque el diferenciador se concentra mejor.

**Elementos:**
- **H2:** *"Por qué MM Agency es diferente al resto de agencias en RD."*
- **Sub P:** *"No vendemos servicios sueltos. Diseñamos el sistema completo que convierte visitas en clientes."*
- **Slider horizontal** con 5 cards (drag, sin dots) — misma mecánica que NoGood

- **Los 5 pilares exactos:**

  **Pilar 1 — Sistema completo, no pedazos sueltos**
  - Ilustración/icono
  - **H3:** "El embudo entero. No pedazos."
  - **P:** "Mientras otras agencias te venden 'manejo de Meta Ads' suelto, nosotros armamos el sistema completo: landing + tráfico + CRM + seguimiento. Porque una buena campaña sin embudo detrás es dinero tirado. Esa es la razón por la que los números cierran donde otros fallan."

  **Pilar 2 — Atención directa del fundador**
  - **H3:** "El que vende es el que ejecuta."
  - **P:** "Cuando contratas MM Agency, Martin Mercedes es quien atiende tu cuenta directamente. No hay equipo de vendedores que te pasa a un junior después de firmar. Hablas con la persona que diseña y ejecuta el embudo."

  **Pilar 3 — Cuentas a tu nombre**
  - **H3:** "Tu embudo, tu dinero, tus cuentas."
  - **P:** "La pauta se paga desde tus propias cuentas de Meta Business Manager y Google Ads. La landing vive en tu dominio. El CRM es tuyo. Tú eres el dueño del sistema completo — si un día decides irte, te vas con todo y el embudo sigue funcionando sin nosotros."

  **Pilar 4 — Sin contratos trampa**
  - **H3:** "Sin permanencia mínima."
  - **P:** "No creemos en atarte con contratos largos. Te quedas con nosotros porque el embudo funciona, no porque tienes que."

  **Pilar 5 — Reportes de clientes, no de vanity metrics**
  - **H3:** "Reportes que miden lo que importa."
  - **P:** "Cada semana recibes un reporte claro que muestra cuántos leads entraron al embudo, cuántos cerraron, cuánto costó cada uno, y qué estamos ajustando. Nada de reportes llenos de likes y alcance."

**Por qué funciona:** Esta sección neutraliza las 5 objeciones principales del avatar (quemaduras previas con pauta suelta, trato impersonal, miedo al contrato, pérdida de control, reportes falsos) convirtiéndolas en pilares de diferenciación.

---

### Sección 7 — Marquee #2: Stack del Embudo

**Objetivo:** Segundo marquee estilo NoGood. NoGood usa logos de VCs/investors. MM Agency no tiene VCs → usar **las plataformas y herramientas con las que armamos el embudo**.

**Elementos:**
- **H2 centrado:** *"El stack con el que armamos tu embudo."*
- **Destaque especial arriba del marquee:** badge grande con el logo oficial de **Google Ads Certified / Google Partner** + texto: *"MM Agency está oficialmente certificada por Google Ads. No es un adorno — es el estándar que exige Google para ejecutar tráfico pagado profesional. Una de las piezas del embudo, con las credenciales que la plataforma exige."*
- **Marquee infinito** con logos en blanco de:
  - **Google Ads Certified / Google Partner** (destacado como primer logo del marquee)
  - Meta Business Partner
  - GoHighLevel (GHL)
  - Koomo CRM
  - Shopify
  - Google Analytics 4
  - Google Tag Manager
  - WhatsApp Business API
  - ManyChat
- **Fondo:** `bg-dark-grey-2` con borders sutiles
- Mismo comportamiento de scroll automático

**Nota:** Solo usar logos de plataformas donde MM Agency tiene cuenta/experiencia real. No inventar partnerships que no existen.

---

### Sección 8 — FAQ Accordion (play SEO)

**Objetivo:** Replicar el FAQ largo de NoGood como play SEO + neutralización de objeciones previo al formulario.

**Elementos:**
- **H2:** *"Preguntas que todos hacen antes de contactarnos."*
- **Fondo:** radial dark con círculos decorativos (`bg-img-dark-radial-circles` equivalente)
- **Accordeón con 10 preguntas** (imitando la longitud de NoGood por SEO):

  1. **¿Qué servicios ofrece MM Agency?**
     *Embudos de venta completos. No vendemos pauta suelta. No hacemos manejo de redes sociales. No hacemos SEO. No hacemos branding. Lo que hacemos es diseñar y operar el sistema completo que convierte visitas en clientes: landing de conversión, tráfico pagado (Meta Ads + Google Ads), CRM con automatización, y optimización continua. Si buscas contratar "un community manager" o "alguien que te maneje Facebook", no somos nosotros. Si quieres un sistema que traiga clientes nuevos de forma medible y automatizada, sí.*

  2. **¿Para qué tipo de negocios trabajan?**
     *Negocios en crecimiento en República Dominicana que facturan entre RD$5M y RD$50M al año y están listos para invertir en un sistema de adquisición de clientes real. Trabajamos con clínicas, restaurantes, retail, servicios B2B y e-commerce.*

  3. **¿Cuánto cuesta armar un embudo con MM Agency?**
     *Depende del tamaño del negocio, la industria y qué piezas del embudo ya tienes armadas (algunos clientes ya tienen landing o CRM y solo necesitan el resto). Por eso existe el diagnóstico gratuito de 20 minutos: te damos un rango realista sin compromiso. Importante: el presupuesto de pauta (lo que pagas a Meta/Google) es separado del fee de agencia y siempre lo controlas tú.*

  4. **¿Cuánto debo invertir en pauta además del fee de la agencia?**
     *Eso se define en el diagnóstico según tu industria y objetivos. El presupuesto de pauta siempre lo decides tú y se paga directamente desde tu cuenta de Meta/Google — nosotros ejecutamos el embudo completo.*

  5. **¿Cuánto tiempo toma ver resultados?**
     *El embudo se arma en 2–3 semanas. Las campañas entran en aire entre la semana 3 y 4. Los primeros resultados medibles se ven entre la semana 4 y 6. Los resultados estables y optimizados llegan entre el mes 2 y 3.*

  6. **¿Tengo que firmar un contrato de permanencia?**
     *No. Sin permanencia mínima. Si después de los primeros meses decides irte, te vas con el embudo completo funcionando a tu nombre — tus cuentas, tu landing, tu CRM, todo el historial. Nos quedamos contigo porque funciona, no porque tienes que.*

  7. **¿Quién va a manejar mi embudo realmente?**
     *Martin Mercedes, el fundador, diseña y opera directamente el embudo. No hay equipo de junior. Si contratas MM Agency, Martin ejecuta.*

  8. **¿Qué pasa si el embudo no da resultados?**
     *Si después de 60 días no hay resultados medibles, te lo decimos directo y ajustamos la pieza que está fallando, o cerramos el contrato. Sin letra chica, sin excusas.*

  9. **¿Cómo empezamos a trabajar juntos?**
     *Llenas el formulario abajo → Martin te contacta en menos de 24 horas laborables → Agendamos el diagnóstico gratuito de 20 minutos → Propuesta personalizada en 48 horas → Si hay fit, empezamos a armar el embudo.*

  10. **¿Están certificados oficialmente por Google?**
      *Sí. MM Agency está certificada por Google Ads, que es una de las 4 piezas del embudo que armamos. Esta certificación no es un adorno: es un requisito que Google exige con exámenes oficiales y métricas reales de rendimiento. Es una capa extra de garantía de que la parte de tráfico pagado del embudo está en manos profesionales.*

**Por qué funciona:** Responde las objeciones en la página (fricción más baja para el formulario) + genera contenido indexable en Google (SEO orgánico a largo plazo).

---

### Sección 9 — Formulario de Calificación (reemplaza el blog teaser de NoGood)

**Objetivo:** Este es **EL ÚNICO objetivo real de la landing**. Es donde NoGood pone su blog teaser; aquí MM Agency pone el formulario completo porque es el objetivo único.

**Elementos visuales:**
- **Headline enorme estilo CTA de NoGood:** *"Listo para armar el embudo de tu negocio."*
  - Tamaño display grande (64–96px)
  - Tipografía heading display
- **Sub-headline:** *"Cuéntanos de tu negocio. Martin revisa cada formulario personalmente y responde en menos de 24 horas laborables."*
- **Fondo:** `gradient-top-secondary-black-medium` equivalente — degradado sutil con el acento del brand

**Formulario de calificación completa — 10 campos:**

1. **Nombre completo** — input texto
2. **Email corporativo** — input email
3. **WhatsApp** — input teléfono (con código RD por defecto)
4. **Nombre de tu empresa** — input texto
5. **Industria / tipo de negocio** — dropdown:
   - Clínicas de salud y estética
   - Restaurantes / hospitalidad
   - Retail / tiendas físicas
   - E-commerce
   - Servicios B2B
   - Servicios profesionales
   - Otro
6. **Tamaño del negocio** — dropdown:
   - 1–5 empleados
   - 6–20 empleados
   - 21–50 empleados
   - 50+ empleados
7. **¿Qué piezas del embudo ya tienes armadas?** — dropdown:
   - Nada — empezamos desde cero
   - Tengo landing pero sin tráfico
   - Tengo campañas pero sin landing ni seguimiento
   - Tengo todo pero los números no cuadran
   - Todavía explorando
8. **¿Cuál es tu presupuesto mensual aproximado para pauta (separado del fee de agencia)?** — dropdown:
   - Menos de RD$15k
   - RD$15k – RD$50k
   - RD$50k – RD$150k
   - RD$150k+
   - Todavía no lo sé
9. **¿Cuál es el principal reto con tu marketing hoy?** — textarea (3–4 líneas)
10. **¿Cuándo te gustaría empezar?** — dropdown:
    - Lo antes posible
    - En las próximas 2–4 semanas
    - En 1–3 meses
    - Todavía explorando

**CTA del botón:** **"Solicitar diagnóstico gratuito"** (botón grande con color acento)

**Microcopy debajo del botón:** *"Sin compromiso. Sin vendedores. Martin te contactará en menos de 24 horas laborables."*

**Legal micro:** *"Tus datos son privados. No los compartimos con nadie. Solo Martin los ve."*

**Por qué funciona:**
- 10 campos califica automáticamente (curiosos se filtran solos)
- Dropdowns reducen fricción vs. texto libre
- El campo 7 (qué tienes armado) permite a Martin dimensionar el alcance del embudo antes de la llamada
- Los campos 5–8 dan a Martin contexto antes de la llamada → llamada 10x más útil
- El campo 10 detecta urgencia → priorización automática de leads

---

### Sección 10 — Footer Dark (estilo NoGood con 1 ciudad)

**Objetivo:** Footer mínimo pero con la misma estética dark de NoGood.

**Elementos:**
- **Top del footer:** bloque con border y `bg-img-dark-radial`
- **Columnas:**
  - **MM Agency** — sobre, filosofía, contacto
  - **Servicios** — Embudo completo, Landing de conversión, Tráfico pagado, CRM + automatización
  - **Recursos** — FAQ, blog (futuro), casos de éxito
  - **Contacto** — WhatsApp, email
- **Filosofía (bloque principal):** *"Embudos de venta completos para negocios en crecimiento en República Dominicana. Landing, tráfico, CRM, seguimiento — el sistema entero."*
- **Headquarters:** *"Basados en Santo Domingo, República Dominicana"* (equivalente al "NYC + Miami + LA + Dubai" de NoGood pero con una sola ciudad — honesto a la realidad de MM Agency hoy)
- **Video decorativo fullwidth opcional** al fondo (loop silencioso, estilo NoGood) — se puede omitir en v1
- **Bottom del footer:**
  - Copyright MM Agency © 2026
  - Links legales: Política de privacidad, Términos
  - Redes sociales: Instagram, LinkedIn

---

## Mapa Visual del Flujo

```
0. STICKY NAV (logo + menú + CTA)
   ↓
1. HERO DARK (H1 masivo + media 16:9)
   ↓
2. MARQUEE #1 (logos clientes infinitos)
   ↓
3. WHAT WE DO (posicionamiento embudo completo)
   ↓
4. SERVICES LIST (4 piezas del embudo en grid)
   ↓
5. TESTIMONIALS SLIDER (con números enormes)
   ↓
6. HOW WE DO IT (5 pilares en slider)
   ↓
7. MARQUEE #2 (stack del embudo)
   ↓
8. FAQ ACCORDION (10 preguntas largas)
   ↓
9. FORMULARIO DE CALIFICACIÓN  ← objetivo único de toda la landing
   ↓
10. FOOTER DARK
```

---

## Diferencias Clave con NoGood.io

| Sección | NoGood | MM Agency |
|---|---|---|
| Hero | Video loopable de brand reel | Video del embudo en acción (sin foto de Martin) |
| Servicios | 6 servicios (grid 3×2) | 4 piezas del embudo (grid 4×1 o 2×2) |
| Pilares | 6 pilares en slider | 5 pilares en slider |
| Marquee #2 | Logos de VCs/investors | Stack del embudo (plataformas/herramientas) |
| CTA final | Blog teaser + newsletter | **Formulario de calificación completo** |
| Footer | 4 ciudades (NYC, Miami, LA, Dubai) | 1 ciudad (Santo Domingo) |
| Wordplay | "Deemed SoGood" / "Ready to get up to NoGood?" | Opcional — explorar wordplay con "MM" o "Mercedes" en fase de copy |

---

## Alineación con Sistema de Ventas Existente

- **Formulario → Koomo CRM** (automatización del lead)
- **Notificación automática a Martin por WhatsApp** al recibir formulario
- **Email de confirmación al prospecto** con lo que sigue
- **Lead calificado** → Martin agenda llamada de 20 min por WhatsApp → diagnóstico → propuesta → cierre
- **Posicionamiento consistente** con WWP inbound + WWP outbound (especialista en embudos completos, no en servicios sueltos)

---

## Archivos a Crear (cuando el usuario autorice ejecución)

1. **CREAR:** `projects/agencia-marketing/landing/estructura.md` — este documento estructural como referencia maestra
2. **CREAR (fase posterior):** `projects/agencia-marketing/landing/copy.md` — copy completo expandido palabra por palabra
3. **CREAR (fase posterior):** `projects/agencia-marketing/landing/design-system.md` — sistema de diseño (colores, tipografía, animaciones)
4. **CREAR (fase posterior):** `projects/agencia-marketing/landing/index.html` + assets — implementación técnica real
5. **ACTUALIZAR:** `projects/agencia-marketing/README.md` — agregar referencia a la landing estructurada

---

## Fuera de Alcance de Este Plan

- Diseño visual detallado (colores específicos, tipografías finales, animaciones exactas)
- Desarrollo técnico HTML/CSS/JS
- Integración del formulario con backend (Koomo CRM, email, WhatsApp)
- Producción del video del hero
- Creación de iconos/ilustraciones de servicios
- Dominio, hosting, SSL
- Permisos escritos de clientes (Memorama, Dra. Aurys) para usar logos + quotes + métricas
- Copy final palabra por palabra (este plan es estructural, no copy final)
- SEO técnico profundo (meta tags, schema.org, sitemap)

---

## Verificación (cuando se ejecute)

- ¿Las 10 secciones están en el mismo orden que NoGood.io?
- ¿El hero tiene H1 masivo en tipografía display sobre fondo dark SIN foto de Martin?
- ¿El H1 habla de "embudos" / "sistema completo", NO de "solo pauta" o "Meta Ads y Google Ads" como producto principal?
- ¿Hay 2 marquees infinitos de logos (clientes arriba, stack abajo)?
- ¿Los testimoniales tienen números enormes dentro de cada card (estilo "85", "879%")?
- ¿Las 4 cards de las piezas del embudo están en container rounded-40 con border sutil?
- ¿Los 5 pilares diferenciadores neutralizan las objeciones del avatar (especialmente la de "me vendieron pauta suelta y no funcionó")?
- ¿El FAQ tiene 10 preguntas largas (play SEO + neutralización previa al formulario)?
- ¿El formulario tiene los 10 campos de calificación completa (incluyendo el nuevo campo 7 sobre qué piezas del embudo ya tiene)?
- ¿No aparecen precios en ninguna parte?
- ¿Martin NO aparece en el hero?
- ¿Meta Ads + Google Ads se mencionan SOLO como parte de "Tráfico pagado" (pieza 2 del embudo), nunca como propuesta de valor principal?
- ¿La estética dark + tipografía display + cards rounded + acento quirúrgico se siente coherente con NoGood?
