# Plan: Landing Principal MM Agency — Estructura Estilo NoGood.io

## Context

MM Agency necesita su landing principal corporativa. Hoy solo existe un WordPress básico que no sirve. Sin esta landing, ni el inbound (Meta/Google Ads → landing) ni el outbound (firma de emails, link de credibilidad) pueden correr.

**Decisiones del usuario (esta sesión):**
- **Modelo de referencia:** Estructura y estética de **nogood.io** replicada sección por sección
- **Enfoque:** SOLO Meta Ads + Google Ads (NoGood ofrece 6 servicios; MM Agency ofrece 2)
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

**Objetivo:** Declarar la especialización en los primeros 3 segundos con impacto visual tipo NoGood.

**Elementos:**
- **H1 masivo (tipografía display):** *"Clientes nuevos con Meta Ads y Google Ads."*
  - Tamaño: clamp(64px, 10vw, 120px)
  - Peso bold, mayúsculas o sentence case, tracking amplio
  - Animación text reveal al cargar (fade-up palabra por palabra)
- **Sub-headline (opcional, más pequeña):** Solo si el H1 necesita contexto. Preferible omitirlo — NoGood no lo usa.
- **Media 16:9 al costado o debajo del H1:**
  - Video loopable corto (campaña real, dashboard animado, o B-roll de trabajo)
  - Si no hay video disponible → animación abstracta con gráficos de Meta/Google Ads
  - **NO usar foto de Martin** (decisión explícita del usuario)
- **CTA implícito:** el H1 entero linkea al formulario, o botón sutil debajo del media
- **Trust bar debajo del hero (bandera de credibilidad):** *"Certificados por Google Ads"* · *"Atención directa del fundador"* · *"Sin contratos trampa"* · *"Cuentas a tu nombre"*
  - El badge "Certificados por Google Ads" con el logo oficial de Google Partner / Google Ads Certified es el elemento de mayor impacto de confianza en el hero — va primero en la línea
- **Fondo:** dark con radial gradient oscuro, z-index de profundidad
- **Padding vertical grande** (`c-py-10` equivalente)

**Por qué funciona:** Replica el impacto del hero de NoGood. El H1 masivo declara la especialización en una frase corta. "Nada más" está implícito en la brevedad.

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
- **H2 (grande, text-left):** *"Tu equipo especialista en adquisición con publicidad digital."*
- **P (body grande):** *"En un mercado lleno de agencias que hacen de todo un poco, MM Agency hace una sola cosa: traerte clientes nuevos con Meta Ads y Google Ads. Nada de redes sociales. Nada de SEO. Nada de branding. Solo pauta que mueve la aguja."*
- Alineación izquierda, padding vertical top grande, sin imagen
- Fondo dark con shapes animadas sutiles de fondo (overflow hidden)

**Por qué funciona:** Replica exactamente el bloque de NoGood pero con el posicionamiento de MM Agency. La declaración "Nada de X. Solo Y." es la firma diferenciadora.

---

### Sección 4 — Services List (2 servicios, no 6)

**Objetivo:** Mostrar los servicios especializados. NoGood tiene 6 cards en grid 3×2; **MM Agency tiene 2 + 1 combo = 3 cards en grid 3×1**.

**Elementos:**
- **Card container grande** con `rounded-40` y border sutil "flotando" sobre fondo radial dark
- **H2 dentro de la card:** *"Lo único que hacemos. Y lo hacemos bien."*
- **Grid 3 columnas** (`col-lg-4` equivalente):

  **Card 1 — Meta Ads**
  - Icono/ilustración animada de Meta (Facebook + Instagram)
  - **H3:** "Meta Ads"
  - **P:** "Campañas en Facebook e Instagram diseñadas para traer clientes nuevos, no likes. Segmentación quirúrgica, creativos que paran el scroll, y métricas que miden lo único que importa: el cliente que entra a tu negocio."

  **Card 2 — Google Ads**
  - Icono/ilustración animada de Google Ads
  - **H3:** "Google Ads"
  - **P:** "Aparece en el momento exacto en que alguien busca lo que tú vendes. Campañas en Search, Performance Max y YouTube que convierten intención en clientes reales."

  **Card 3 — Meta + Google (Combo)**
  - Icono combinando ambos
  - **H3:** "Combo Meta + Google"
  - **P:** "Cobertura completa del embudo: descubrimiento en redes sociales + intención de compra en búsqueda. El stack completo de adquisición para negocios que están listos para escalar."

- **Microanimaciones en hover** sobre cada card
- Debajo del grid: frase pequeña que ancla al formulario: *"El canal exacto para tu negocio lo definimos juntos en el diagnóstico gratuito."*

---

### Sección 5 — Testimonials con Números Grandes (estilo NoGood "879%")

**Objetivo:** Replicar la jugada más icónica de NoGood: slider de testimoniales con **números enormes dentro de cada card**.

**Elementos:**
- **H2:** *"Negocios que ya están adquiriendo clientes con MM Agency"*
  - (Alternativa wordplay opcional: *"Esto dicen nuestros clientes"*)
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
  - Subtítulo del número: "pacientes interesados en 60 días con Google Ads"
  - Quote: *"El formulario no paraba de llenarse."*
  - Párrafo: contexto de la campaña (sin revelar nombre/especialidad/monto)

  **Card 2 — Memorama (con permiso)**
  - Logo: Memorama
  - Número enorme: [métrica concreta a confirmar con Martin — ej. ROAS, leads, revenue]
  - Quote: corta del dueño
  - Párrafo: resultado concreto

  **Card 3 — Dra. Aurys Mercedes (con permiso)**
  - Logo/foto: Dra. Aurys
  - Número enorme: [métrica concreta a confirmar]
  - Quote: corta
  - Párrafo: resultado concreto

**Nota crítica:** Martin debe confirmar permiso + métricas reales antes de publicar.

**Por qué funciona:** El número gigante dentro de la card es el elemento visual más memorable de NoGood. Copiarlo literalmente es la jugada.

---

### Sección 6 — How We Do It (5 pilares diferenciadores)

**Objetivo:** Equivalente a "A differentiated approach to Growth" de NoGood. NoGood usa 6 pilares; MM Agency usará **5** porque el diferenciador se concentra mejor.

**Elementos:**
- **H2:** *"Por qué MM Agency es diferente al resto de agencias en RD."*
- **Sub P:** *"No somos una agencia más. Aquí está lo que nos hace distintos:"*
- **Slider horizontal** con 5 cards (drag, sin dots) — misma mecánica que NoGood

- **Los 5 pilares exactos:**

  **Pilar 1 — Especialización real**
  - Ilustración/icono
  - **H3:** "Solo pauta. Nada más."
  - **P:** "Mientras otras agencias hacen 10 servicios a medias, nosotros hacemos dos bien: Meta Ads y Google Ads. Esa especialización es lo que nos permite entregar resultados reales donde otros fallan."

  **Pilar 2 — Atención directa del fundador**
  - **H3:** "El que vende es el que ejecuta."
  - **P:** "Cuando contratas MM Agency, Martin Mercedes es quien atiende tu cuenta directamente. No hay equipo de vendedores que te pasa a un junior después de firmar. Hablas con la persona que ejecuta."

  **Pilar 3 — Cuentas a tu nombre**
  - **H3:** "Tu pauta, tu dinero, tus cuentas."
  - **P:** "La pauta se paga desde tus propias cuentas de Meta Business Manager y Google Ads. Tú eres el dueño. Si un día decides irte, te vas con todo — nada de quedarte atado a una agencia que controla tus activos."

  **Pilar 4 — Sin contratos trampa**
  - **H3:** "Sin permanencia mínima."
  - **P:** "No creemos en atarte con contratos largos. Te quedas con nosotros porque funciona, no porque tienes que."

  **Pilar 5 — Reportes de clientes, no de vanity metrics**
  - **H3:** "Reportes que miden lo que importa."
  - **P:** "Cada semana recibes un reporte claro que muestra cuántos clientes nuevos entraron, cuánto costó cada uno, y qué ajustes estamos haciendo. Nada de reportes llenos de likes y alcance."

**Por qué funciona:** Esta sección neutraliza las 5 objeciones principales del avatar (quemaduras previas, trato impersonal, miedo al contrato, pérdida de control, reportes falsos) convirtiéndolas en pilares de diferenciación.

---

### Sección 7 — Marquee #2: Credenciales / Herramientas

**Objetivo:** Segundo marquee estilo NoGood. NoGood usa logos de VCs/investors. MM Agency no tiene VCs → usar **certificaciones, plataformas y herramientas** que dan credibilidad.

**Elementos:**
- **H2 centrado:** *"Certificados por Google Ads y trabajando con las plataformas líderes de la industria."*
- **Destaque especial arriba del marquee:** badge grande con el logo oficial de **Google Ads Certified / Google Partner** + texto: *"MM Agency está oficialmente certificada por Google Ads — garantía de ejecución profesional según los estándares de Google."*
- **Marquee infinito** con logos en blanco de:
  - **Google Ads Certified / Google Partner** (destacado como primer logo del marquee)
  - Meta Business Partner / Facebook Ads
  - Google Ads
  - GoHighLevel (GHL)
  - Koomo CRM
  - Shopify
  - Google Analytics 4
  - Google Tag Manager
  - WhatsApp Business API
- **Fondo:** `bg-dark-grey-2` con borders sutiles
- Mismo comportamiento de scroll automático

**Nota:** Solo usar logos de plataformas donde MM Agency tiene cuenta/experiencia real. No inventar partnerships que no existen.

---

### Sección 8 — FAQ Accordion (play SEO)

**Objetivo:** Replicar el FAQ largo de NoGood como play SEO + neutralización de objeciones previo al formulario.

**Elementos:**
- **H2:** *"Preguntas que todos hacen antes de contactarnos."*
- **Fondo:** radial dark con círculos decorativos (`bg-img-dark-radial-circles` equivalente)
- **Accordeón con 9 preguntas** (imitando la longitud de NoGood por SEO):

  1. **¿Qué servicios ofrece MM Agency?**
     *Solo Meta Ads y Google Ads. No hacemos manejo de redes sociales, SEO, branding ni content marketing. Nos especializamos en pauta paga porque es lo que genera clientes medibles.*

  2. **¿Para qué tipo de negocios trabajan?**
     *Negocios en crecimiento en República Dominicana que facturan entre RD$5M y RD$50M al año y están listos para invertir en adquisición de clientes nuevos. Trabajamos con clínicas, restaurantes, retail, servicios B2B y e-commerce.*

  3. **¿Cuánto cuesta trabajar con MM Agency?**
     *Depende del canal (Meta, Google o ambos), la industria y los objetivos. Por eso existe el diagnóstico gratuito de 20 minutos: te damos un rango realista sin compromiso. Importante: el presupuesto de pauta (lo que pagas a Meta/Google) es separado del fee de agencia y siempre lo controlas tú.*

  4. **¿Cuánto debo invertir en pauta además del fee de la agencia?**
     *Eso se define en el diagnóstico según tu industria y objetivos. El presupuesto de pauta siempre lo decides tú y se paga directamente desde tu cuenta de Meta/Google — nosotros solo ejecutamos.*

  5. **¿Cuánto tiempo toma ver resultados?**
     *Las primeras campañas están activas en 5–10 días después de firmar. Los primeros resultados medibles se ven entre semana 2 y 4. Los resultados estables y optimizados llegan entre el mes 2 y 3.*

  6. **¿Tengo que firmar un contrato de permanencia?**
     *No. Sin permanencia mínima. Si después de los primeros meses decides irte, te vas con tus cuentas de Meta y Google intactas. Nos quedamos contigo porque funciona, no porque tienes que.*

  7. **¿Quién va a manejar mis campañas realmente?**
     *Martin Mercedes, el fundador, maneja directamente la cuenta. No hay equipo de junior. Si contratas MM Agency, Martin ejecuta.*

  8. **¿Qué pasa si las campañas no dan resultados?**
     *Si después de 60 días no hay resultados medibles, te lo decimos directo y ajustamos o cerramos el contrato. Sin letra chica, sin excusas.*

  9. **¿Cómo empezamos a trabajar juntos?**
     *Llenas el formulario abajo → Martin te contacta en menos de 24 horas laborables → Agendamos el diagnóstico gratuito de 20 minutos → Propuesta personalizada en 48 horas → Si hay fit, empezamos.*

  10. **¿Están certificados oficialmente por Google?**
      *Sí. MM Agency está certificada por Google Ads — lo que significa que cumplimos con los estándares oficiales de Google para ejecutar campañas de publicidad. Esta certificación no es un adorno: es un requisito que Google exige con exámenes y métricas de rendimiento reales. Es una capa extra de garantía de que tu inversión está en manos profesionales.*

**Por qué funciona:** Responde las objeciones en la página (fricción más baja para el formulario) + genera contenido indexable en Google (SEO orgánico a largo plazo).

---

### Sección 9 — Formulario de Calificación (reemplaza el blog teaser de NoGood)

**Objetivo:** Este es **EL ÚNICO objetivo real de la landing**. Es donde NoGood pone su blog teaser; aquí MM Agency pone el formulario completo porque es el objetivo único.

**Elementos visuales:**
- **Headline enorme estilo CTA de NoGood:** *"Listo para traer clientes nuevos a tu negocio."*
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
7. **¿Ya has invertido en pauta digital antes?** — dropdown:
   - Nunca
   - Sí, pero sin resultados claros
   - Sí, con resultados regulares
   - Sí, con buenos resultados (queremos escalar)
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
- Los campos 5–8 dan a Martin contexto antes de la llamada → llamada 10x más útil
- El campo 10 detecta urgencia → priorización automática de leads

---

### Sección 10 — Footer Dark (estilo NoGood con 1 ciudad)

**Objetivo:** Footer mínimo pero con la misma estética dark de NoGood.

**Elementos:**
- **Top del footer:** bloque con border y `bg-img-dark-radial`
- **Columnas:**
  - **MM Agency** — sobre, filosofía, contacto
  - **Servicios** — Meta Ads, Google Ads, Combo
  - **Recursos** — FAQ, blog (futuro), casos de éxito
  - **Contacto** — WhatsApp, email
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
3. WHAT WE DO (posicionamiento en 1 frase)
   ↓
4. SERVICES LIST (3 cards rounded-40)
   ↓
5. TESTIMONIALS SLIDER (con números enormes)
   ↓
6. HOW WE DO IT (5 pilares en slider)
   ↓
7. MARQUEE #2 (plataformas/herramientas)
   ↓
8. FAQ ACCORDION (9 preguntas largas)
   ↓
9. FORMULARIO DE CALIFICACIÓN  ← objetivo único de toda la landing
   ↓
10. FOOTER DARK
```

---

## Diferencias Clave con NoGood.io

| Sección | NoGood | MM Agency |
|---|---|---|
| Hero | Video loopable de brand reel | Video de campaña real o animación abstracta (sin foto de Martin) |
| Servicios | 6 servicios (grid 3×2) | 3 opciones: Meta, Google, Combo (grid 3×1) |
| Pilares | 6 pilares en slider | 5 pilares en slider |
| Marquee #2 | Logos de VCs/investors | Logos de plataformas/herramientas |
| CTA final | Blog teaser + newsletter | **Formulario de calificación completo** |
| Footer | 4 ciudades (NYC, Miami, LA, Dubai) | 1 ciudad (Santo Domingo) |
| Wordplay | "Deemed SoGood" / "Ready to get up to NoGood?" | Opcional — explorar wordplay con "MM" o "Mercedes" en fase de copy |

---

## Alineación con Sistema de Ventas Existente

- **Formulario → Koomo CRM** (automatización del lead)
- **Notificación automática a Martin por WhatsApp** al recibir formulario
- **Email de confirmación al prospecto** con lo que sigue
- **Lead calificado** → Martin agenda llamada de 20 min por WhatsApp → diagnóstico → propuesta → cierre
- **Posicionamiento consistente** con WWP inbound + WWP outbound (especialista, no generalista, solo Meta + Google)

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
- ¿Hay 2 marquees infinitos de logos (clientes arriba, plataformas abajo)?
- ¿Los testimoniales tienen números enormes dentro de cada card (estilo "85", "879%")?
- ¿Las 3 cards de servicios están en container rounded-40 con border sutil?
- ¿Los 5 pilares diferenciadores neutralizan las objeciones del avatar?
- ¿El FAQ tiene 9 preguntas largas (play SEO + neutralización previa al formulario)?
- ¿El formulario tiene los 10 campos de calificación completa?
- ¿No aparecen precios en ninguna parte?
- ¿Martin NO aparece en el hero?
- ¿El badge "Certificados por Google Ads" aparece en el hero (trust bar) + marquee #2 (destacado) + FAQ (pregunta 10)?
- ¿La estética dark + tipografía display + cards rounded + acento quirúrgico se siente coherente con NoGood?
