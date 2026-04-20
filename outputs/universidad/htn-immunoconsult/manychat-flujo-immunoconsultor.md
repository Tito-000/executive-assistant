# Flujo ManyChat — ImmunoConsultor
## Automatización Instagram DM basada en calendarios de contenido

> **Propósito:** Demostrar cómo ManyChat captura leads desde el contenido del calendario,
> califica y deriva a WhatsApp. Montar en ManyChat y tomar screenshots para la presentación.
> **Tiempo estimado de montaje:** 20-30 min en ManyChat.

---

## PASO 1 — Crear cuenta y conectar Instagram

1. Ir a https://manychat.com → Sign up (plan Free)
2. Conectar la cuenta de Instagram de ImmunoConsultor
3. Aceptar permisos de Instagram DM

---

## PASO 2 — Triggers (disparadores)

Crear **3 triggers** que conectan con el calendario de contenido:

### Trigger 1: Comentario en post con keyword
- **Tipo:** Instagram Comment Reply
- **Keywords:** `info`, `precio`, `quiero`, `cómo`, `immunocal`, `interesada`
- **Aplica a:** Todos los posts (o seleccionar posts específicos del calendario)
- **Acción:** Enviar DM automático → inicia Flujo Principal

### Trigger 2: Respuesta a Story
- **Tipo:** Instagram Story Reply
- **Keywords:** cualquier respuesta (catch-all)
- **Acción:** Enviar DM automático → inicia Flujo Principal

### Trigger 3: DM directo con keyword
- **Tipo:** Instagram DM con keyword
- **Keywords:** `info`, `precio`, `immunocal`, `producto`, `salud`
- **Acción:** Inicia Flujo Principal

---

## PASO 3 — Flujo Principal (copiar estos mensajes exactos)

### Mensaje 1 — Bienvenida (envío inmediato)
```
¡Hola! 👋 Gracias por tu interés.

Soy el asistente de ImmunoConsultor. Te voy a ayudar a encontrar la mejor opción para ti en menos de 1 minuto.

¿Puedo hacerte 2 preguntas rápidas?
```
**Botones:**
- ✅ Sí, dale → va a Mensaje 2
- ❌ Solo quiero el precio → va a Mensaje 5 (precio directo)

---

### Mensaje 2 — Pregunta 1: Motivo (calificación)
```
¿Qué te motivó a buscar información?
```
**Botones:**
- 🏥 Condición de salud propia → Tag: `motivo_salud_propia`
- 👨‍👩‍👧 Salud de un familiar → Tag: `motivo_familiar`
- 💪 Rendimiento físico / deporte → Tag: `motivo_deporte`
- 🔍 Curiosidad / me lo recomendaron → Tag: `motivo_curiosidad`

→ Todas las opciones van a Mensaje 3

---

### Mensaje 3 — Pregunta 2: Urgencia
```
¿Hace cuánto estás buscando una solución?
```
**Botones:**
- 🔥 Ahora mismo, es urgente → Tag: `urgencia_alta` → va a Mensaje 4A
- ⏳ Hace semanas, investigando → Tag: `urgencia_media` → va a Mensaje 4B
- 💭 Recién empiezo a explorar → Tag: `urgencia_baja` → va a Mensaje 4B

---

### Mensaje 4A — Lead caliente (urgencia alta)
```
Entiendo la urgencia. Immunocal tiene más de 40 patentes y estudios clínicos que respaldan su efectividad para fortalecer tu sistema inmunológico desde adentro.

Te conecto ahora mismo con nuestro consultor para que te oriente personalmente.
```
**Botón:**
- 💬 Hablar por WhatsApp → Link: `https://wa.me/18091234567?text=Hola%2C%20vengo%20de%20Instagram%20y%20me%20interesa%20Immunocal`

**⚠️ IMPORTANTE:** Reemplazar `18091234567` con el número real de WhatsApp de Martín.

→ Después del click: Tag `lead_caliente` + notificar a admin

---

### Mensaje 4B — Lead tibio/frío (urgencia media o baja)
```
¡Perfecto! Te comparto algo que te va a interesar.

Immunocal es el único suplemento con más de 40 patentes médicas para optimizar tu glutatión — la molécula que tu cuerpo usa para protegerse, desintoxicarse y recuperarse.

No es una promesa, es ciencia. Miles de familias en RD ya lo usan.
```
**Botones:**
- 📋 Ver más información → Link a landing page de Lovable (cuando esté lista) o link de producto
- 💬 Hablar con un consultor → Link WhatsApp (mismo que arriba)
- 📱 Seguir viendo contenido → Tag: `lead_tibio`, fin del flujo

→ Tag `lead_tibio` + programar follow-up

---

### Mensaje 5 — Precio directo (para quienes solo quieren precio)
```
¡Claro! Immunocal tiene varias presentaciones:

💊 Immunocal Regular — desde RD$ X,XXX
⭐ Immunocal Platinum — desde RD$ X,XXX
⚡ Immunocal Sport — desde RD$ X,XXX

El precio incluye asesoría personalizada de nuestro consultor certificado.

¿Cuál te interesa?
```
**Botones:**
- 💊 Regular → Tag: `interes_regular`
- ⭐ Platinum → Tag: `interes_platinum`
- ⚡ Sport → Tag: `interes_sport`
- 🤔 No sé cuál me conviene → Tag: `necesita_asesoria`

→ Todas las opciones van a Mensaje 6

**⚠️ RELLENAR:** Martín pone los precios reales en RD$ donde dice X,XXX

---

### Mensaje 6 — Cierre → WhatsApp
```
¡Buena elección! Para darte la mejor atención y resolver tus dudas, te conecto con nuestro consultor.

Él te puede explicar cómo funciona el producto, dosis recomendada y opciones de envío a toda RD.
```
**Botón:**
- 💬 Conectar por WhatsApp → Link WhatsApp con texto pre-armado según producto elegido

---

## PASO 4 — Secuencias de Follow-up (para leads que NO compraron)

### Follow-up 1 — A las 24 horas
**Condición:** Tiene tag `lead_tibio` y NO tiene tag `compra_realizada`
```
Hola de nuevo 👋

Ayer mostraste interés en Immunocal. ¿Sabías que es el suplemento #1 recomendado por médicos en Canadá para fortalecer el sistema inmunológico?

Si tienes alguna duda, estamos para ayudarte.
```
**Botón:**
- 💬 Tengo una pregunta → conecta con live chat / WhatsApp

---

### Follow-up 2 — A las 72 horas
**Condición:** Tiene tag `lead_tibio` y NO tiene tag `compra_realizada`
```
Solo quería compartirte esto:

"Mi mamá tenía problemas articulares hace 2 años. Empezó con Immunocal y hoy camina sin dolor." — Cliente real, Santiago, RD

Si quieres conocer más historias como esta, escríbenos. Sin compromiso.
```
**Botón:**
- 📖 Ver más testimonios → Link landing o highlights de Instagram
- 💬 Me interesa → WhatsApp

---

### Follow-up 3 — A los 7 días
**Condición:** Tiene tag `lead_tibio` y NO tiene tag `compra_realizada`
```
Última vez que te escribo sobre esto, lo prometo 😊

Esta semana tenemos disponibilidad para envíos a toda RD. Si decides probarlo, te damos seguimiento personalizado durante tus primeros 30 días.

¿Te gustaría aprovechar?
```
**Botones:**
- ✅ Sí, quiero ordenar → WhatsApp
- ❌ Ahora no, gracias → Tag: `no_interesado`, retirar de secuencia

---

## PASO 5 — Tags y segmentos (crear en ManyChat)

| Tag | Significado | Uso |
|---|---|---|
| `motivo_salud_propia` | Busca para sí mismo | Segmentar contenido |
| `motivo_familiar` | Busca para familiar | Contenido de cuidadores |
| `motivo_deporte` | Deportista | Contenido Sport |
| `motivo_curiosidad` | Explorador | Nutrir con educación |
| `urgencia_alta` | Quiere comprar ya | Prioridad WhatsApp |
| `urgencia_media` | Investigando | Follow-up activo |
| `urgencia_baja` | Solo mirando | Nutrición lenta |
| `lead_caliente` | Derivado a WhatsApp urgente | Seguimiento inmediato |
| `lead_tibio` | Interesado no convencido | Secuencia follow-up |
| `interes_regular` | Quiere Immunocal Regular | Personalizar oferta |
| `interes_platinum` | Quiere Platinum | Personalizar oferta |
| `interes_sport` | Quiere Sport | Personalizar oferta |
| `necesita_asesoria` | No sabe cuál producto | Llamada consultiva |
| `compra_realizada` | Ya compró | Excluir de follow-up |
| `no_interesado` | Dijo no | Excluir de secuencia |

---

## CONEXIÓN CON EL CALENDARIO DE CONTENIDO

El calendario de Nguyen define posts con CTAs específicos. Así se conecta:

| Tipo de post (calendario) | CTA del post | Trigger ManyChat |
|---|---|---|
| Post educativo (Sabio) | "Comenta INFO para saber más" | Trigger 1: keyword `info` |
| Story con sticker pregunta | Cualquier respuesta | Trigger 2: Story Reply |
| Post testimonial (Cuidador) | "Escríbenos QUIERO por DM" | Trigger 3: keyword `quiero` |
| Reel producto | "Comenta PRECIO" | Trigger 1: keyword `precio` |
| Ad Meta (tráfico mensajes) | CTA "Enviar mensaje" | Trigger 3: DM automático |

---

## CONEXIÓN CON HUBSPOT

Cuando un lead llega a WhatsApp:
1. Martín registra manualmente el contacto en HubSpot (plan free)
2. Asigna etapa del pipeline: Nuevo → Calificado → Propuesta → Cliente
3. Si compra: tag `compra_realizada` en ManyChat para excluir de follow-up
4. A los 25 días: HubSpot dispara email de recordatorio de recompra

---

## DIAGRAMA DEL FLUJO (para referencia visual)

```
INSTAGRAM (post/story/ad/DM)
        │
        ▼
  ┌─────────────┐
  │  TRIGGER     │  Keywords: info, precio, quiero, immunocal
  │  ManyChat    │
  └──────┬──────┘
         ▼
  ┌─────────────┐
  │  MSG 1       │  Bienvenida + ¿2 preguntas rápidas?
  │  Bienvenida  │
  └──┬───────┬──┘
     │       │
   "Sí"   "Solo precio"
     │       │
     ▼       ▼
  ┌──────┐  ┌──────┐
  │MSG 2 │  │MSG 5 │  Lista de precios
  │Motivo│  │Precio│
  └──┬───┘  └──┬───┘
     ▼         ▼
  ┌──────┐  ┌──────┐
  │MSG 3 │  │MSG 6 │  → WhatsApp
  │Urgenc│  │Cierre│
  └─┬──┬─┘  └──────┘
    │  │
  Alta  Media/Baja
    │     │
    ▼     ▼
  ┌────┐ ┌────┐
  │4A  │ │4B  │
  │WApp│ │Info│
  └────┘ └─┬──┘
           │
     ┌─────┼─────┐
     ▼     ▼     ▼
   Landing WhatsApp  Seguir IG
     │     │         │
     │     │    ┌────┴────┐
     │     │    │Follow-up│
     │     │    │24h/72h/ │
     │     │    │7 días   │
     │     │    └─────────┘
     │     │
     └──┬──┘
        ▼
  ┌───────────┐
  │  HUBSPOT   │  CRM + Pipeline + Email recompra
  └───────────┘
```

---

## QUÉ CAPTURAR EN SCREENSHOTS (para la presentación)

1. **Pantalla de Triggers** — mostrando los 3 triggers con keywords
2. **Flujo visual** — el flow builder con los mensajes conectados
3. **Mensaje de bienvenida** — preview del mensaje 1 con botones
4. **Preguntas de calificación** — mensajes 2 y 3
5. **Derivación a WhatsApp** — mensaje 4A con botón de WhatsApp
6. **Secuencia follow-up** — mostrando los 3 mensajes programados
7. **Tags creados** — lista de tags en la sección de segmentos

---

*Flujo diseñado 2026-04-18 · Para montaje en ManyChat Free*
