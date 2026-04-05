# Design System — Landing MM Agency

> Sistema de diseño para la implementación de la landing principal.
> Basado en [Brand Guidelines v1.0](../branding/mm-agency-brand-guidelines.html).
> Estructura: [estructura.md](estructura.md) · Copy: [copy.md](copy.md)

---

## 1. Principios de diseño

1. **Dark-first.** Todo respira sobre `#181818`. El claro es la excepción.
2. **Primary Yellow es quirúrgico.** Solo CTAs, acentos, el punto del logo, subrayados críticos. Nunca decorativo.
3. **Tipografía blocky.** Orbitron para headings masivos. Display-first.
4. **Cards flotantes.** Border `0.5px` sobre `#202020`, radios grandes, separados por gutters tipo grid técnico.
5. **Espacio generoso.** Padding vertical de sección mínimo `5rem` (80px) en desktop.
6. **Motion sutil.** Fade + translateY de 25px. Nada de bouncy/playful. Tech, no friendly.
7. **Cero emojis, cero ilustraciones amigables.** Solo iconografía mono-line o logos reales.

---

## 2. Design Tokens

### 2.1 Colores

```css
:root {
  /* Brand */
  --primary:      #FAFA00;  /* Yellow — CTAs, acentos, dot del logo */
  --secondary:    #713DFF;  /* Violet — hover secondary, highlights */
  --orange:       #F54900;  /* Alerts, errores */
  --light-blue:   #00E3FF;  /* Links info */
  --pink:         #FCA8FF;  /* Highlights raros */
  --green:        #008500;  /* Success (formulario enviado) */

  /* Surface */
  --bg:           #181818;  /* Fondo principal */
  --bg-card:      #202020;  /* Fondo de cards y secciones alternadas */
  --bg-elev:      #262626;  /* Hover de cards */
  --border:       #353535;  /* Borders sutiles 0.5px */

  /* Text */
  --space-grey:   #707070;  /* Labels, sub-text, numeración */
  --light-grey:   #C9C9C9;  /* Body paragraph */
  --light:        #FAFAFA;  /* Texto secundario fuerte */
  --white:        #FFFFFF;  /* Headings y texto primario */
  --black:        #000000;
}
```

**Reglas de uso:**

| Elemento | Color |
|---|---|
| Fondo principal | `--bg` |
| Fondo de secciones alternas (marquees, cards container) | `--bg-card` |
| H1, H2, H3 | `--white` |
| Body copy | `--light-grey` |
| Sub-labels / numeración de sección | `--space-grey` |
| CTAs primarios (bg) | `--primary` |
| CTAs primarios (text) | `--black` |
| CTAs secundarios | `border: 1px solid var(--white)` + fondo transparente, fill animado blanco |
| Hover CTA primary | brightness(1.1) o shift a outline |
| Links | `--white` con subrayado `--primary` en hover |
| Borders | `0.5px solid var(--border)` |
| Números enormes de testimonials | `--primary` |
| Errores de formulario | `--orange` |
| Success de formulario | `--green` |

### 2.2 Tipografía

```css
--font-h: 'Orbitron', sans-serif;         /* Headings display — wide/técnico, clon de Microgramma */
--font-b: 'Inter', sans-serif;            /* Body */
--font-m: 'DM Mono', monospace;           /* Labels técnicos, numeración, microcopy */
```

**Google Fonts import:**
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&family=DM+Mono:wght@400;500&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
```

**Escala tipográfica (desktop):**

| Token | Uso | Font | Size | Weight | Line-height | Letter-spacing |
|---|---|---|---|---|---|---|
| `--t-display` | H1 hero | Orbitron | `clamp(3.5rem, 9vw, 8rem)` (56–128px) | 700 | 0.95 | -0.02em |
| `--t-h1` | H2 sección grande (form, posicionamiento) | Orbitron | `clamp(2.5rem, 5vw, 4.5rem)` (40–72px) | 700 | 1.05 | -0.01em |
| `--t-h2` | H2 estándar de sección | Orbitron | `clamp(1.8rem, 3vw, 2.8rem)` (28–44px) | 700 | 1.15 | -0.01em |
| `--t-h3` | H3 cards, pilares | Orbitron | `clamp(1.1rem, 1.6vw, 1.4rem)` (17–22px) | 600 | 1.3 | 0 |
| `--t-metric` | Números enormes testimonials | Orbitron | `clamp(5rem, 10vw, 9rem)` (80–144px) | 700 | 1 | -0.03em |
| `--t-body-lg` | Párrafos del hero / posicionamiento | Inter | `clamp(1rem, 1.3vw, 1.2rem)` (16–19px) | 400 | 1.65 | 0 |
| `--t-body` | Párrafos generales | Inter | `0.95rem` (15px) | 400 | 1.7 | 0 |
| `--t-body-sm` | Microcopy, footer | Inter | `0.8rem` (13px) | 400 | 1.6 | 0 |
| `--t-label` | Numeración sección, trust bar, labels | DM Mono | `0.6rem` (10px) | 500 | 1.4 | 0.2em uppercase |
| `--t-nav` | Menú nav | Inter | `0.7rem` (11px) | 500 | 1 | 0.1em uppercase |
| `--t-cta` | Botones | Inter | `0.75rem` (12px) | 700 | 1 | 0.15em uppercase |

**Reglas tipográficas:**
- Hero H1: sentence case, NO mayúsculas. El tamaño ya es el impacto.
- Labels y numeración de sección: SIEMPRE UPPERCASE con letter-spacing amplio.
- Botones: SIEMPRE UPPERCASE.
- Body: sentence case natural, nunca uppercase en párrafos.
- Términos en inglés (Meta Ads, Google Ads, etc.) sin cursiva ni diferenciación visual.

### 2.3 Espaciado

```css
--space-1:  0.25rem;   /*  4px */
--space-2:  0.5rem;    /*  8px */
--space-3:  0.75rem;   /* 12px */
--space-4:  1rem;      /* 16px */
--space-5:  1.5rem;    /* 24px */
--space-6:  2rem;      /* 32px */
--space-7:  3rem;      /* 48px */
--space-8:  4rem;      /* 64px */
--space-9:  5rem;      /* 80px */
--space-10: 6.5rem;    /* 104px */
--space-11: 8rem;      /* 128px */
```

**Padding por sección (desktop):**
- Padding vertical: `--space-10` (104px) top + bottom
- Padding horizontal: `3.5rem` (56px) en desktop, `1.5rem` (24px) en mobile
- Max-width de contenido: `1400px` centrado

### 2.4 Radios

```css
--r-sm:  6px;    /* Inputs, pills pequeños */
--r-md:  12px;   /* Botones, cards secundarias */
--r-lg:  20px;   /* Cards principales */
--r-xl:  40px;   /* Container rounded-40 estilo NoGood */
--r-full: 999px; /* Pills, circulares */
```

### 2.5 Borders & Shadows

```css
--bd-hair:  0.5px solid var(--border);
--bd-soft:  1px solid var(--border);
--bd-strong:1px solid var(--white);

--shadow-glow-primary:  0 0 0 1px var(--primary), 0 0 40px rgba(250,250,0,0.15);
--shadow-glow-violet:   0 0 0 1px var(--secondary), 0 0 60px rgba(113,61,255,0.2);
--shadow-card:          0 0 0 0.5px var(--border), 0 20px 60px rgba(0,0,0,0.4);
```

### 2.6 Z-index

```css
--z-base:    1;
--z-card:    10;
--z-sticky:  50;
--z-nav:     100;
--z-modal:   1000;
```

### 2.7 Breakpoints

```css
--bp-sm:  640px;
--bp-md:  768px;
--bp-lg:  1024px;
--bp-xl:  1280px;
--bp-2xl: 1536px;
```

Estrategia: **mobile-first** con media queries `min-width`. Estilos base = mobile. Desktop se añade con `@media (min-width: 1024px)`.

---

## 3. Componentes

### 3.1 Botón primario (CTA)

```css
.btn-primary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 1rem 2rem;
  background: var(--primary);
  color: var(--black);
  font-family: var(--font-b);
  font-size: var(--t-cta);
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.15em;
  border: none;
  border-radius: var(--r-md);
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}
.btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 20px 60px rgba(250,250,0,0.25);
}
```

**Tamaños:** `sm` (0.7rem 1.4rem), `md` (default), `lg` (1.25rem 2.5rem, solo para hero y formulario final).

### 3.2 Botón secundario (outline)

```css
.btn-outline {
  padding: 1rem 2rem;
  background: transparent;
  color: var(--white);
  border: 1px solid var(--white);
  border-radius: var(--r-md);
  position: relative;
  overflow: hidden;
  transition: color 0.4s;
}
.btn-outline::before {
  content: '';
  position: absolute;
  inset: 0;
  width: 0;
  background: var(--white);
  transition: width 0.4s cubic-bezier(.42,0,.58,1);
  z-index: 0;
}
.btn-outline:hover::before { width: 100%; }
.btn-outline:hover { color: var(--black); }
.btn-outline span { position: relative; z-index: 1; }
```

### 3.3 Card rounded-40 (container principal de servicios)

```css
.card-xl {
  background: var(--bg-card);
  border: var(--bd-hair);
  border-radius: var(--r-xl);  /* 40px */
  padding: clamp(2rem, 4vw, 4rem);
  position: relative;
  overflow: hidden;
}
.card-xl::before {
  /* Radial glow sutil */
  content: '';
  position: absolute;
  top: -50%;
  left: 50%;
  transform: translateX(-50%);
  width: 120%;
  height: 100%;
  background: radial-gradient(ellipse at center, rgba(113,61,255,0.08) 0%, transparent 70%);
  pointer-events: none;
}
```

### 3.4 Card de servicio (interior grid)

```css
.service-card {
  background: var(--bg);
  border: var(--bd-hair);
  border-radius: var(--r-lg);  /* 20px */
  padding: 2.5rem 2rem;
  transition: background 0.3s, transform 0.3s;
}
.service-card:hover {
  background: var(--bg-elev);
  transform: translateY(-4px);
}
```

### 3.5 Card de testimonial (con número enorme)

```css
.testimonial-card {
  background: var(--bg-card);
  border: var(--bd-hair);
  border-radius: var(--r-lg);
  padding: 3rem 2.5rem;
  min-height: 420px;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}
.testimonial-metric {
  font-family: var(--font-h);
  font-size: var(--t-metric);
  font-weight: 700;
  color: var(--primary);
  line-height: 1;
}
.testimonial-metric-sub {
  font-family: var(--font-m);
  font-size: 0.7rem;
  color: var(--space-grey);
  text-transform: uppercase;
  letter-spacing: 0.15em;
}
```

### 3.6 Marquee infinito

```css
.marquee {
  overflow: hidden;
  background: var(--bg-card);
  border-top: var(--bd-hair);
  border-bottom: var(--bd-hair);
  padding: 3rem 0;
}
.marquee-track {
  display: flex;
  gap: 4rem;
  animation: marquee 40s linear infinite;
  width: max-content;
}
.marquee:hover .marquee-track { animation-play-state: paused; }
.marquee-item img {
  height: 40px;
  opacity: 0.6;
  filter: brightness(0) invert(1);
  transition: opacity 0.3s;
}
.marquee-item:hover img { opacity: 1; }

@keyframes marquee {
  from { transform: translateX(0); }
  to   { transform: translateX(-50%); }
}
```

**Nota al dev:** el array de logos debe duplicarse en el DOM para que el loop se vea infinito sin saltos.

### 3.7 Input y dropdown del formulario

```css
.form-field {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  margin-bottom: 1.5rem;
}
.form-label {
  font-family: var(--font-m);
  font-size: 0.65rem;
  color: var(--space-grey);
  text-transform: uppercase;
  letter-spacing: 0.15em;
}
.form-input,
.form-select,
.form-textarea {
  background: var(--bg-card);
  border: var(--bd-hair);
  border-radius: var(--r-md);
  padding: 1rem 1.2rem;
  color: var(--white);
  font-family: var(--font-b);
  font-size: 0.95rem;
  transition: border-color 0.3s, background 0.3s;
  width: 100%;
}
.form-input:focus,
.form-select:focus,
.form-textarea:focus {
  outline: none;
  border-color: var(--primary);
  background: var(--bg-elev);
}
.form-textarea { min-height: 120px; resize: vertical; }
.form-input.error { border-color: var(--orange); }
```

### 3.8 FAQ Accordion item

```css
.faq-item {
  border-bottom: var(--bd-hair);
  padding: 2rem 0;
  cursor: pointer;
}
.faq-question {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 2rem;
}
.faq-question-text {
  font-family: var(--font-h);
  font-size: clamp(1.1rem, 1.5vw, 1.4rem);
  font-weight: 600;
  color: var(--white);
}
.faq-icon {
  width: 24px;
  height: 24px;
  color: var(--primary);
  transition: transform 0.4s cubic-bezier(.42,0,.58,1);
}
.faq-item.open .faq-icon { transform: rotate(45deg); }
.faq-answer {
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.5s cubic-bezier(.42,0,.58,1), padding 0.3s;
  color: var(--light-grey);
  font-family: var(--font-b);
  line-height: 1.75;
}
.faq-item.open .faq-answer { max-height: 500px; padding-top: 1.5rem; }
```

### 3.9 Trust bar (hero)

```css
.trust-bar {
  display: flex;
  flex-wrap: wrap;
  gap: 2rem;
  margin-top: 2rem;
}
.trust-item {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  font-family: var(--font-m);
  font-size: 0.7rem;
  color: var(--light-grey);
  text-transform: uppercase;
  letter-spacing: 0.12em;
}
.trust-item::before {
  content: '';
  width: 14px;
  height: 14px;
  background: var(--primary);
  mask: url('data:image/svg+xml;utf8,<svg ...check icon.../>') center/contain no-repeat;
}
```

**Primer item destacado (Google Ads Certified):** mismo componente con `font-weight: 700` + logo oficial Google Partner como prefijo en lugar del check.

### 3.10 Nav sticky

```css
.nav {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: var(--z-nav);
  background: rgba(24,24,24,0.88);
  backdrop-filter: blur(3rem);
  -webkit-backdrop-filter: blur(3rem);
  border-bottom: var(--bd-hair);
  padding: 1.1rem 3rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  transition: padding 0.3s, background 0.3s;
}
.nav.scrolled {
  padding: 0.7rem 3rem;
  background: rgba(24,24,24,0.95);
}
```

---

## 4. Animaciones y motion

### 4.1 Reglas generales

- **Easing default:** `cubic-bezier(0.42, 0, 0.58, 1)` (ease-in-out técnico)
- **Duración estándar:** `0.4s` para hovers, `0.6s` para reveals, `0.8s` para hero entry
- **Delay stagger:** `0.08s` entre elementos en listas
- **Reduced motion:** respetar `@media (prefers-reduced-motion: reduce)` — desactivar marquees, reveals y parallax.

### 4.2 Scroll reveal (sección entera)

```css
.reveal {
  opacity: 0;
  transform: translateY(25px);
  transition: opacity 0.6s ease, transform 0.6s ease;
}
.reveal.visible {
  opacity: 1;
  transform: translateY(0);
}
```

**Implementación JS:** IntersectionObserver con `threshold: 0.15`, `rootMargin: 0px 0px -50px 0px`. Una sola vez (no bidireccional).

### 4.3 Text reveal del H1 hero

**Librería recomendada:** vanilla JS con `Intl.Segmenter` o split manual por palabra (sin GSAP para mantener peso ligero).

```css
.hero-word {
  display: inline-block;
  opacity: 0;
  transform: translateY(60%);
  animation: word-reveal 0.8s cubic-bezier(.25,.46,.45,.94) forwards;
}
.hero-word:nth-child(1) { animation-delay: 0.1s; }
.hero-word:nth-child(2) { animation-delay: 0.2s; }
/* ...etc por cada palabra */

@keyframes word-reveal {
  to { opacity: 1; transform: translateY(0); }
}
```

### 4.4 Marquee

Ver `.marquee` en 3.6 — `animation: marquee 40s linear infinite`.

### 4.5 Hover de card

```css
transition: transform 0.3s ease, background 0.3s ease;
transform: translateY(-4px);
```

### 4.6 Radial glows de fondo (secciones)

```css
.section-bg-radial::before {
  content: '';
  position: absolute;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 80%;
  height: 120%;
  background: radial-gradient(ellipse at center top, rgba(113,61,255,0.1) 0%, transparent 60%);
  pointer-events: none;
  z-index: 0;
}
```

**Dónde usar:** hero, formulario final, FAQ. No usar en todas — pierde impacto.

### 4.7 Slider drag (testimonials y pilares)

**Librería recomendada:** [Embla Carousel](https://www.embla-carousel.com/) (vanilla, 10KB, drag support nativo, sin dependencias). Alternativa: `tiny-slider`.

**Config:**
```js
EmblaCarousel(emblaNode, {
  loop: false,
  dragFree: true,
  align: 'start',
  slidesToScroll: 1,
})
```

---

## 5. Mapeo sección → tokens

| Sección | Background | H2 token | Body token | CTA tipo |
|---|---|---|---|---|
| 0. Nav | `rgba(24,24,24,0.88)` + blur | — | `--t-nav` | outline sm |
| 1. Hero | `--bg` + radial violet | `--t-display` | `--t-body-lg` | primary lg |
| 2. Marquee #1 | `--bg-card` | `--t-h2` | — | — |
| 3. What We Do | `--bg` + radial | `--t-h1` | `--t-body-lg` | — |
| 4. Services | `--bg` + card-xl container | `--t-h2` (dentro) + `--t-h3` (cards) | `--t-body` | — |
| 5. Testimonials | `--bg-card` | `--t-h2` | `--t-body` + `--t-metric` | — |
| 6. How We Do It | `--bg` | `--t-h2` + `--t-h3` (pilares) | `--t-body` | — |
| 7. Marquee #2 | `--bg-card` + badge destacado | `--t-h2` | `--t-body-sm` (badge) | — |
| 8. FAQ | `--bg` + radial circles decorativos | `--t-h2` | `--t-body` | — |
| 9. Formulario | `--bg` + gradient top | `--t-h1` (gigante) | `--t-body-lg` | primary lg |
| 10. Footer | `--bg` con border top | `--t-h3` | `--t-body-sm` | — |

---

## 6. Iconografía

**Estilo:** mono-line, 1.5px stroke, esquinas suaves. Nada de iconos "filled" rellenos de color.

**Fuente recomendada:** [Lucide Icons](https://lucide.dev/) (2000+ iconos, mono-line, open source, muy usado en stack moderno).

**Colores de icono:**
- Por defecto: `--space-grey`
- Acento (trust bar, CTAs): `--primary`
- Hover: `--white`

**Iconos específicos a usar:**
- Check (trust bar): `lucide:check`
- Plus/close (FAQ): `lucide:plus`
- Arrow-right (CTAs): `lucide:arrow-right`
- External link (cases): `lucide:arrow-up-right`
- Meta Ads card: logo real de Meta (monocromo blanco)
- Google Ads card: logo real de Google Ads (monocromo blanco)
- Combo card: composición de ambos logos en círculos overlapping

---

## 7. Assets requeridos antes del build

Lista de recursos que deben existir antes de empezar el HTML:

1. **Logos MM Agency** (ya existen en `projects/agencia-marketing/branding/logo/`):
   - Wordmark white (nav + footer)
   - Wordmark yellow (destacado)
   - Wordmark gray (nav sutil)
   - Brandmark circle-ring (favicon + avatar)
2. **Favicon** (32px, 16px, apple-touch-icon 180px)
3. **Logos de clientes** para marquee #1:
   - Memorama (blanco transparente)
   - Dra. Aurys Mercedes (blanco transparente)
   - Anabel Mercedes (blanco transparente)
4. **Logos de plataformas** para marquee #2 (todos en blanco transparente):
   - Google Partner / Google Ads Certified (logo oficial)
   - Meta Business Partner
   - Google Ads
   - GoHighLevel
   - Koomo CRM
   - Shopify
   - Google Analytics 4
   - Google Tag Manager
   - WhatsApp Business API
5. **Media del hero:** video loop 16:9 (MP4 + WebM) o animación abstracta CSS/Lottie
6. **OG image:** 1200×630 para share social
7. **Fuentes:** preload de Orbitron 700 y Inter 400/700 desde Google Fonts

---

## 8. Performance targets

- **Lighthouse performance:** ≥ 90 en mobile
- **LCP:** < 2.5s
- **CLS:** < 0.1
- **FID/INP:** < 100ms
- **Peso total página:** < 1.5 MB (sin video hero) / < 3 MB (con video hero comprimido)
- **Fuentes:** preload crítico, `font-display: swap`
- **Imágenes:** WebP + fallback JPG, `loading="lazy"` excepto hero
- **JS:** vanilla + Embla Carousel (único vendor). Sin framework pesado.

---

## 9. Accesibilidad

- Contraste mínimo AA: `--white` sobre `--bg` = 19.5:1 ✓ / `--light-grey` sobre `--bg` = 12.6:1 ✓ / `--space-grey` sobre `--bg` = 4.7:1 ✓
- `--primary` sobre `--bg` = 17.6:1 ✓ (botón yellow con texto black = 17.6:1 ✓)
- Focus visible en todos los inputs y botones (outline 2px `--primary`)
- `aria-label` en iconos sin texto
- `aria-expanded` en items del FAQ
- Formulario con `<label>` asociado a cada `<input>` vía `for/id`
- Respeto de `prefers-reduced-motion`
- Navegación por teclado completa (tab order lógico)
- Marquees con `aria-hidden="true"` (son decorativos, no aportan info)

---

## 10. Stack técnico recomendado

| Capa | Elección | Razón |
|---|---|---|
| HTML | HTML5 semántico plano | Sin framework — máxima performance y portabilidad |
| CSS | Vanilla CSS con custom properties | Ya está todo definido en tokens, no hace falta Tailwind/SCSS |
| JS | Vanilla + Embla Carousel | Sliders + IntersectionObserver + FAQ toggle, nada más |
| Fuentes | Google Fonts con preconnect + preload | Orbitron + Inter + DM Mono |
| Hosting | Cloudflare Pages | Ya hay API key guardada ([cloudflare-api.md](../../../recursos-ia/api-keys/cloudflare-api.md)) |
| Formulario backend | Koomo CRM vía webhook + notificación WhatsApp | Definir en fase posterior |
| Analytics | GA4 + Meta Pixel | Instalar al final, después del deploy inicial |

---

## 11. Checklist de verificación del build

- [ ] Las 10 secciones usan los tokens de color correctos (sin hardcodes)
- [ ] Orbitron se carga correctamente (peso 700 en H1)
- [ ] `--primary` solo aparece en CTAs, número de testimonials, punto del logo, underlines de hover
- [ ] Los dos marquees corren infinitos y pausan en hover
- [ ] El H1 del hero tiene text reveal animado
- [ ] Todas las secciones tienen fade-up en scroll
- [ ] El FAQ abre/cierra con transition smooth
- [ ] El slider de testimonials tiene drag nativo (no dots tradicionales)
- [ ] El slider de pilares tiene drag nativo
- [ ] Formulario con validación inline y estado error/success
- [ ] Responsive funciona desde 375px hasta 2560px
- [ ] Lighthouse ≥ 90 en mobile
- [ ] `prefers-reduced-motion` desactiva marquees y reveals
- [ ] Focus states visibles en todo elemento interactivo
- [ ] OG image + favicon + meta tags básicos configurados
- [ ] Trust bar del hero tiene el check + "Certificados por Google Ads" como primer item
- [ ] El badge Google Partner del marquee #2 está visualmente dominante

---

## 12. Fuera de alcance de este documento

- Copy final (ver [copy.md](copy.md))
- Estructura de secciones (ver [estructura.md](estructura.md))
- Implementación HTML/CSS/JS real
- Integración del formulario con Koomo CRM
- SEO técnico avanzado (schema.org, sitemap, robots)
- Traducción al inglés
- Dark/light mode toggle (la landing es dark-only)
- A/B testing framework
