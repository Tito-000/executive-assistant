---
name: cierre-dia
description: Revisión nocturna del día. Muestra tareas de mañana en Motion, permite agregar nuevos tasks o eventos, y cierra con un mensaje motivacional de metas. Invocar manualmente cada noche.
disable-model-invocation: true
---

# Skill: /cierre-dia

Revisión nocturna para preparar el día siguiente. Ejecutar cada noche a las 8 PM.

---

## PASO 1 — Obtener la fecha de mañana

Calcula la fecha de mañana en formato `YYYY-MM-DD`.

```bash
TOMORROW=$(python3 -c "from datetime import date, timedelta; print(date.today() + timedelta(days=1))")
echo $TOMORROW
```

---

## PASO 2 — Consultar Motion: tareas de mañana

Consulta la API de Motion para obtener las tareas agendadas y con vencimiento mañana.

```bash
MOTION_KEY="ZqTdrhNz66tfCcZVFYUkhj3fFEP92L0V6aai2ZtX5k4="
TOMORROW=$(python3 -c "from datetime import date, timedelta; print(date.today() + timedelta(days=1))")

curl -s "https://api.usemotion.com/v1/tasks" \
  -H "X-API-Key: $MOTION_KEY" | python3 -c "
import sys, json
data = json.load(sys.stdin)
tasks = data.get('tasks', [])
tomorrow = '$TOMORROW'

results = []
for t in tasks:
    if t.get('completed'): continue
    due = (t.get('dueDate') or '')[:10]
    scheduled_tomorrow = any(
        c.get('scheduledStart','')[:10] == tomorrow
        for c in t.get('chunks', [])
    )
    if due == tomorrow or scheduled_tomorrow:
        chunks = t.get('chunks', [])
        times = []
        for c in chunks:
            if c.get('scheduledStart','')[:10] == tomorrow:
                start = c.get('scheduledStart','')[11:16]
                end = c.get('scheduledEnd','')[11:16]
                times.append(f'{start}–{end}')
        results.append({
            'name': t.get('name',''),
            'priority': t.get('priority',''),
            'due': due,
            'times': times,
            'project': (t.get('project') or {}).get('name',''),
            'status': t.get('status',{}).get('name',''),
        })

# ordenar: ASAP > HIGH > MEDIUM > LOW
priority_order = {'ASAP': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3, '': 4}
results.sort(key=lambda x: (priority_order.get(x['priority'], 4), x['times'][0] if x['times'] else 'zz'))

if not results:
    print('SIN_TAREAS')
else:
    for r in results:
        time_str = ', '.join(r['times']) if r['times'] else 'sin hora agendada'
        proj = f\" | {r['project']}\" if r['project'] else ''
        print(f\"[{r['priority']}] {r['name']}{proj} | {time_str}\")
"
```

---

## PASO 3 — Presentar reporte de mañana

Presenta el resultado de forma clara:

---

**Revisión nocturna — Preparando el [día de la semana, fecha de mañana]**

**📋 Lo que ya tienes en Motion para mañana:**

[Si hay tareas: muestra la lista con hora, prioridad y proyecto]
[Si no hay tareas: "Motion no tiene nada agendado para mañana todavía."]

---

## PASO 4 — Preguntar por tasks o eventos nuevos

Pregunta exactamente esto:

> "¿Hay algo que quieras agregar para mañana? Puedes decirme tasks nuevos o eventos con hora específica y yo los agendo en Motion."

Espera la respuesta de Martin.

**Si Martin dice que no o que está bien:** pasa al PASO 6.

**Si Martin menciona uno o más tasks/eventos:** pasa al PASO 5.

---

## PASO 5 — Agregar tasks en Motion

Para cada task que Martin mencione, extrae:
- **Nombre** del task
- **Hora o deadline** (si mencionó una)
- **Prioridad** (si no la menciona, usar `MEDIUM` por default)
- **Duración estimada** (si no la menciona, usar 30 minutos por default)

Primero obtén el workspace ID:
```bash
MOTION_KEY="ZqTdrhNz66tfCcZVFYUkhj3fFEP92L0V6aai2ZtX5k4="
curl -s "https://api.usemotion.com/v1/workspaces" \
  -H "X-API-Key: $MOTION_KEY" | python3 -c "
import sys, json
data = json.load(sys.stdin)
for w in data.get('workspaces', []):
    print(w['id'], '|', w['name'])
"
```

Luego crea cada task:
```bash
MOTION_KEY="ZqTdrhNz66tfCcZVFYUkhj3fFEP92L0V6aai2ZtX5k4="
TOMORROW=$(python3 -c "from datetime import date, timedelta; print(date.today() + timedelta(days=1))")

curl -s -X POST "https://api.usemotion.com/v1/tasks" \
  -H "X-API-Key: $MOTION_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"name\": \"[NOMBRE DEL TASK]\",
    \"workspaceId\": \"[WORKSPACE_ID]\",
    \"dueDate\": \"${TOMORROW}T23:59:59.000Z\",
    \"priority\": \"MEDIUM\",
    \"duration\": 30
  }" | python3 -c "import sys,json; d=json.load(sys.stdin); print('✓ Creado:', d.get('name',''))"
```

Confirma cada task creado con un "✓ [nombre] — agendado para mañana."

Cuando termines de agregar todo, pregunta:
> "¿Algo más?"

Repite el PASO 5 hasta que Martin confirme que ya está todo.

---

## PASO 6 — Mensaje motivacional

Lee `context/goals.md`.

Selecciona la meta más relevante según el contexto actual (la que está más próxima en deadline o la que Martin mencionó más en la conversación reciente).

Escribe un mensaje motivacional corto (3–5 líneas máximo) que:
- Conecte lo que Martin va a hacer mañana con la meta grande
- Sea directo y personal, como un socio de confianza, no como un coach de Instagram
- Mencione la meta específica y el deadline si es inminente
- No use frases de relleno ni emojis exagerados

Formato:
```
---
[Mensaje motivacional aquí]
---
Buenas noches, Martin. Mañana es un buen día para avanzar.
```

---

## Comportamiento especial

**Si Motion no responde o hay error de API:** informa el error y continúa igual — pregunta los tasks manualmente y agrégalos cuando la API esté disponible.

**Si Martin dice que no hay nada nuevo:** no insistas, pasa directo al mensaje motivacional.

**Si Martin menciona un evento con hora fija** (reunión, llamada, cita): créalo con la duración exacta mencionada y `priority: HIGH` por default.
