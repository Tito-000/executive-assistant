# ManyChat — Copy de Flujos

> Este documento contiene el copy exacto de cada mensaje de ManyChat.
> Usa este archivo para configurar los flujos en la plataforma.

---

## Keywords activos

| Keyword | Intención | Cuándo usarlo |
|---------|-----------|---------------|
| **CÓMO** | Curiosidad (top funnel) | Reels de historia personal y educativos |
| **QUIERO** | Deseo activo (mid funnel) | Contenido de lifestyle y CTAs directos |
| **INFO** | General (fallback) | Stories diarias, cualquier post |

---

## Flujo A — Keyword en Comentarios

**Trigger:** Alguien comenta CÓMO, QUIERO o INFO en cualquier Reel/Post.

### Paso 1 — DM inicial (delay 30-60 seg)

> Variación 1:

```
Hola {first_name}! Gracias por escribirme. Me encanta que te hayas interesado.

Antes de contarte más, me gustaría saber un poco de ti. ¿Qué te llamó la atención?
```

> Variación 2:

```
Hola {first_name}! Qué bueno que escribiste.

Me encantaría saber un poco más de ti antes de contarte. ¿Qué te llamó la atención?
```

> Variación 3:

```
Hola {first_name}! Gracias por tu interés.

Cuéntame, ¿qué fue lo que te llamó la atención?
```

**Botones (Quick Reply):**

| Botón | Tag |
|-------|-----|
| Busco una forma de generar ingresos extra | `negocio` |
| Me interesan los productos de salud | `producto` |
| Solo quiero saber más | `curiosidad` |

---

### Paso 2A — Si elige "Ingresos extra" (tag: negocio)

**Delay: 5 seg**

```
Perfecto. Te cuento brevemente:

Yo empecé desde cero, sin experiencia y sin contactos. Hoy tengo un negocio que me genera ingresos todos los meses y me da libertad de tiempo.

Tengo una sesión gratuita de 15 minutos donde te explico cómo funciona. Sin compromiso. Si tiene sentido para ti, hablamos. Si no, todo bien.

¿Te gustaría agendar tu sesión?
```

**Botones:**

| Botón | Acción |
|-------|--------|
| Sí, quiero agendar | → Paso 3A |
| Todavía no, cuéntame más | → Paso 3B |

---

### Paso 3A — Quiere agendar

**Delay: 3 seg**

```
Genial! Entra aquí y completa tus datos. Te confirmo por WhatsApp:

👉 [LINK a sesion-descubre.html]

Nos vemos pronto!
```

**Acción:** Activar Live Chat (Anabel recibe notificación).

---

### Paso 3B — Quiere más info primero

**Delay: 5 seg**

```
Entiendo, sin apuro.

Te dejo un video corto donde cuento mi historia — de tímida a construir un negocio real. Si después quieres saber más, escríbeme.

👉 [LINK al Reel P1 "De Tímida a Diamante"]

Y si en algún momento te interesa la sesión gratuita, solo escríbeme QUIERO y te mando el link.
```

**Acción:** Activar Live Chat.

---

### Paso 2B — Si elige "Productos de salud" (tag: producto)

**Delay: 5 seg**

```
Genial! Tenemos productos de salud basados en glutatión y sistema inmune.

¿Tienes algún tema de salud específico que te interese? Escríbeme y te cuento.
```

**Acción:** Activar Live Chat inmediatamente. Anabel toma la conversación.

---

### Paso 2C — Si elige "Solo quiero saber más" (tag: curiosidad)

**Delay: 5 seg**

```
Me alegra la curiosidad!

Te dejo este video donde cuento mi historia — cómo pasé de ser la más tímida del salón a construir algo real. Sin promesas, sin hype. Solo la verdad.

👉 [LINK al Reel P1 "De Tímida a Diamante"]

Si después quieres saber más, escríbeme. Aquí estoy.
```

**Acción:** No hacer follow-up automático. Si responde, Anabel toma manualmente.

---

## Flujo B — DM con Keyword

**Trigger:** Alguien escribe CÓMO, QUIERO o INFO directamente en DM.

**Flujo idéntico al Flujo A**, con una diferencia en el mensaje inicial:

### Paso 1 (reemplaza el del Flujo A)

```
Hola {first_name}! Vi tu mensaje. Me encanta que te hayas animado a escribirme.

Antes de contarte más, me gustaría saber un poco de ti. ¿Qué te llamó la atención?
```

**Resto del flujo: igual que Flujo A (Pasos 2A/2B/2C → 3A/3B).**

---

## Notas técnicas

- **{first_name}** = variable de ManyChat que toma el nombre del perfil de Instagram
- **Delays** entre mensajes: 30-60 seg para el primer mensaje, 3-5 seg para los siguientes
- **Randomizer** en Paso 1: configurar las 3 variaciones con distribución igual (33% cada una)
- **Live Chat:** siempre activar después de la calificación para que Anabel reciba notificación
- **Tags:** asignar automáticamente al momento de elegir botón
- Los [LINK] se reemplazan con las URLs reales una vez que la landing esté publicada

---

## Camino alternativo (sin landing)

Si un prospecto dice "sí quiero agendar" pero no quiere llenar formulario, enviar directamente:

```
Perfecto! Escríbele directo a Anabel por WhatsApp y agenda tu sesión:

👉 https://wa.me/18292812978?text=Hola%20Anabel%2C%20vengo%20de%20tu%20Instagram%20y%20quiero%20agendar%20mi%20Sesi%C3%B3n%20Descubre.
```
