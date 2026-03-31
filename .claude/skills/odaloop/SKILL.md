---
name: odaloop
description: Retrospectiva semanal de Martin. Guía conversacional por el template Oda Loop (6 preguntas), da coaching estilo Tony Robbins basado en las respuestas, guarda cada sesión en udaloop sunday/sesiones/, y actualiza el análisis de patrones automáticamente.
disable-model-invocation: true
---

# Skill: /odaloop

Retrospectiva semanal. Ejecutar cada domingo.

---

## PASO 1 — Obtener fecha y cargar contexto histórico

```bash
TODAY=$(python3 -c "from datetime import date; print(date.today())")
WEEK_NUM=$(python3 -c "from datetime import date; print(date.today().isocalendar()[1])")
```

Lee el archivo `udaloop sunday/patrones/analisis.md`.

- Si existe y tiene contenido: extrae los 1-2 patrones más recurrentes para mencionarlos en la apertura.
- Si no existe o está vacío: es la primera sesión.

---

## PASO 2 — Apertura

Si hay sesiones previas:
```
Domingo de retrospectiva, Martin.

[Mencionar 1-2 patrones del historial en 2 líneas — directo, sin suavizar. Ej: "La semana pasada dijiste que la dopamina barata fue tu mayor obstáculo — veamos cómo te fue esta vez."]

Empecemos.
```

Si es la primera sesión:
```
Primera retrospectiva. Vamos a construir desde aquí.

Te voy a hacer 6 preguntas una por una. Respóndelas con honestidad — eso es lo único que funciona.

Empecemos con el objetivo general.
```

---

## PASO 3 — Preguntas conversacionales (una a la vez, en orden)

**REGLA CRÍTICA:** Hacer UNA sola pregunta. Esperar respuesta. Luego la siguiente. NUNCA hacer dos preguntas juntas.

Si una respuesta abre algo importante, hacer máximo 1 pregunta de seguimiento antes de continuar.

**Orden exacto:**

**[0]** Objetivo General de la Semana: ¿qué quieres lograr esta semana específicamente? (Leer `context/goals.md` y Motion para tener contexto — pero dejar que Martin lo declare con sus palabras.)

**[1]** ¿Cuál es tu Meta concreta esta semana? (El resultado medible más importante — el que, si lo logras, hace que la semana valga la pena.)
*(No asumir que es la misma de la semana anterior — dejar que Martin la declare.)*

**[2]** ¿Por qué es importante para ti?

**[3]** ¿Qué lograste hacer esta semana para acercarte a tus metas?

**[4]** ¿Cuáles son los mayores obstáculos que debes superar para lograr tus metas?

**[5]** ¿Cuál es tu plan de acción específico para esta semana?

**[6]** ¿Qué lecciones aprendiste esta semana?

---

## PASO 4 — Coaching

Al terminar las 6 preguntas, dar el coaching. Basarse en las respuestas de hoy + patrones históricos si existen.

**Formato del coaching:**

```
---

Lo que escuché:
[2-3 frases que sintetizan lo más importante de lo que dijo Martin. Sin repetir textualmente — interpretar.]

Lo que veo en ti:
[1-2 insights poderosos y específicos. No genéricos. Conectar lo que dijo con el patrón real que se ve. Ej: "Sigues declarando la misma meta pero los obstáculos son los mismos — eso no es mala suerte, es una decisión que estás evitando tomar."]

El patrón que noto:
[Solo si hay sesiones previas — señalar 1 patrón que se repite entre semanas. Sin suavizar.]

Esta semana tu trabajo es:
[1 desafío concreto y específico para la semana. No una lista — UNA cosa. La más importante.]

---
```

**Tono:** Directo. Como un coach de alto rendimiento que respeta a Martin lo suficiente para decirle la verdad. Sin frases motivacionales vacías.

---

## PASO 5 — Guardar la sesión

Crear el archivo `udaloop sunday/sesiones/[TODAY].md`.

Ruta completa: `/Users/martinmercedes/Desktop/Executive assistant 2/udaloop sunday/sesiones/[TODAY].md`

Formato del archivo:

```markdown
# Odaloop — [TODAY] (Semana [WEEK_NUM])

## Objetivo General de la Semana
[respuesta]

## 1. ¿Cuál es mi Meta?
[respuesta]

## 2. ¿Por qué es importante?
[respuesta]

## 3. ¿Qué logré hacer esta semana para acercarme a mis metas?
[respuesta]

## 4. ¿Cuáles son los mayores obstáculos que debo superar?
[respuesta]

## 5. ¿Cuál es mi plan de acción específico para esta semana?
[respuesta]

## 6. ¿Qué lecciones aprendí esta semana?
[respuesta]

---

## Coaching

[Incluir el coaching completo tal como se presentó]
```

---

## PASO 6 — Actualizar análisis de patrones

Leer **todas** las sesiones en `udaloop sunday/sesiones/` y actualizar `udaloop sunday/patrones/analisis.md`.

Ruta completa: `/Users/martinmercedes/Desktop/Executive assistant 2/udaloop sunday/patrones/analisis.md`

El archivo debe tener esta estructura y actualizarse cada semana:

```markdown
# Análisis de Patrones — Odaloop

_Última actualización: [TODAY]_
_Sesiones registradas: [N]_

---

## Metas declaradas

[Tabla con las metas que Martin ha declarado semana a semana. Si la misma meta aparece 2+ semanas = blocker potencial.]

| Semana | Fecha | Meta |
|--------|-------|------|

---

## Obstáculos recurrentes

[Obstáculos que aparecen más de una vez. Ordenados por frecuencia.]

| Obstáculo | Veces mencionado | Primera vez | Nota |
|-----------|-----------------|-------------|------|

---

## Lecciones acumuladas

[Lecciones únicas extraídas de todas las sesiones. Si la misma lección se repite = no se está implementando.]

- [fecha] [lección]

---

## Patrones de comportamiento

[Observaciones consolidadas. Solo agregar cuando hay evidencia de 2+ sesiones.]

- **[patrón]:** [descripción + evidencia]

---

## Victorias registradas

[Logros mencionados en las sesiones. Cronológico.]

- [fecha] [logro]

---

## Evolución del plan de acción

[¿Las tareas del plan de acción de la semana anterior se completaron? ¿Se repiten?]

| Semana | Plan declarado | ¿Ejecutado? |
|--------|---------------|-------------|

---

## Coaching acumulado — Temas recurrentes

[Lo que el coaching ha señalado semana a semana. Identifica qué problemas persisten a pesar del feedback.]

- [fecha] [tema del coaching]
```

**Reglas de actualización:**
- Si un obstáculo ya existe en la tabla: incrementar contador
- Si una lección ya fue mencionada antes: agregar nota "(repetida)"
- Si la meta es la misma que la semana anterior: señalarlo
- Si el plan de acción de la semana pasada aparece en los logros de esta: marcarlo como ejecutado
- Nunca borrar entradas — solo agregar

---

## Comportamiento especial

**Martin dice que no tiene tiempo para responder todo:** Continuar con las preguntas que respondió, guardar la sesión parcial y marcarla como "(incompleta)".

**Martin responde muy corto:** Hacer la pregunta de seguimiento permitida antes de continuar.

**Es la primera sesión:** No inventar patrones. El archivo de patrones se inicializa con la primera sesión.

**Martin quiere hacer el odaloop de una semana pasada:** Ajustar la fecha del archivo de sesión a la fecha correcta.
