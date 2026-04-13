# ManyChat — Guía de Setup

> Guía paso a paso para configurar ManyChat para el Instagram de Anabel Mercedes.
> Tiempo estimado: 30-45 minutos.

---

## Requisitos previos

- [ ] Instagram de Anabel es cuenta **Business** (no personal ni creator)
- [ ] Facebook Page vinculada al Instagram de Anabel
- [ ] Email para crear la cuenta de ManyChat

> **Si el Instagram es personal/creator:** Ir a Settings > Account > Switch to Professional Account > Business. Requiere Facebook Page.

---

## Paso 1 — Crear cuenta ManyChat

1. Ir a [manychat.com](https://manychat.com)
2. Click "Get Started Free"
3. Seleccionar **Instagram** como canal
4. Iniciar sesión con el Facebook de Anabel (o el Facebook que administra la Page)
5. Seleccionar la Facebook Page vinculada al Instagram
6. Autorizar permisos: `instagram_manage_messages`, `pages_messaging`
7. Plan: **Free** (soporta hasta 1,000 contactos — suficiente para empezar)

---

## Paso 2 — Configurar Custom Fields y Tags

### Tags (Automation > Tags):
| Tag | Descripción |
|-----|-------------|
| `negocio` | Prospecto interesado en oportunidad de negocio |
| `producto` | Interesado en productos de salud |
| `curiosidad` | Solo quiere información |

### Custom Fields (Settings > Custom Fields):
| Campo | Tipo | Descripción |
|-------|------|-------------|
| `whatsapp_number` | Text | Número de WhatsApp (si lo da en el chat) |
| `interes` | Text | Qué le interesa (negocio/producto/curiosidad) |

---

## Paso 3 — Crear los 2 flujos

### Flujo A: Keyword en Comentarios

1. Ir a **Automation > New Automation**
2. Trigger: **Instagram > Comment Contains Keyword**
3. Configurar:
   - Keywords: `CÓMO`, `QUIERO`, `INFO` (case insensitive)
   - Apply to: **All Posts** (o seleccionar posts específicos después)
4. Construir el flujo siguiendo el copy de `flujos-copy.md`
5. En el Paso 1, usar **Randomizer** con las 3 variaciones (33% cada una)
6. En cada botón de calificación, agregar acción: **Add Tag** correspondiente
7. Después de calificación, agregar acción: **Enable Live Chat**
8. Delays: 30 seg antes del primer mensaje, 5 seg entre mensajes

### Flujo B: DM con Keyword

1. Ir a **Automation > New Automation**
2. Trigger: **Instagram > Direct Message Contains Keyword**
3. Keywords: `CÓMO`, `QUIERO`, `INFO`
4. Mismo flujo que A, con el mensaje inicial alternativo (ver `flujos-copy.md`)

---

## Paso 4 — Configurar links

Reemplazar `[LINK a sesion-descubre.html]` en los flujos con la URL real:

- **Si usa GitHub Pages:** `https://tito-000.github.io/anabel-mercedes-landing/sesion-descubre.html`
- **Si usa anabelmercedes.com:** `https://anabelmercedes.com/sesion-descubre.html`
- **Si usa Cloudflare Pages:** la URL que genere el deployment

Reemplazar `[LINK al Reel P1]` con el link real del Reel "De Tímida a Diamante" cuando se publique.

---

## Paso 5 — Testing

1. Usar una cuenta secundaria de Instagram (no la de Anabel)
2. Comentar **CÓMO** en un post de Anabel
3. Verificar que llega el DM en <60 segundos
4. Seguir el flujo completo: elegir "ingresos extra" → "quiero agendar" → verificar que llega el link
5. Abrir el link → llenar formulario → verificar que redirige a WhatsApp con mensaje correcto
6. Probar el Flujo B: enviar "INFO" por DM directo
7. Probar el Flujo C: mencionar @anabelmercedes en una Story

---

## Paso 6 — Activar

1. En cada flujo (A y B), cambiar status a **Active**
2. Verificar que Live Chat está habilitado (Settings > Live Chat > Toggle ON)
3. Descargar la app de ManyChat en el teléfono de Anabel para recibir notificaciones

---

## Mantenimiento

- **Semanal:** Revisar tags y conversaciones en ManyChat para ver cuántos prospectos entran
- **Mensual:** Revisar si los keywords siguen funcionando con el contenido nuevo
- **Cuando se llene:** Al llegar a 1,000 contactos, upgrade a Pro ($15/mes)

---

## Keywords por video (referencia rápida)

| Video | Keyword CTA |
|-------|-------------|
| P1 — De Tímida a Diamante | CÓMO |
| P2 — El 75% No Gana Nada | CÓMO |
| P3 — No Persigo a Nadie | INFO |
| P4 — Lo Construí Mientras Vivía | QUIERO |
| O1 — 3 Cosas Que NUNCA Hago | INFO |
| O2 — Me Temblaban Las Manos | CÓMO |
| O3 — "Eso Es Pirámide" | INFO |
| O4 — Lo Que Nadie Te Dice | QUIERO |

---

## Archivos relacionados

- `flujos-copy.md` — Copy exacto de todos los mensajes
- `../guiones/guiones-produccion.md` — Guiones de los 4 videos de producción
- `../guiones/guiones-organicos.md` — Guiones de los 4 videos orgánicos
- `../landing/sesion-descubre.html` — Landing de captura
- `../WWP/WWP-anabel-mercedes.md` — Estrategia completa del funnel
