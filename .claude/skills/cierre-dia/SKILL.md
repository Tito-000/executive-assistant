---
name: cierre-dia
description: Revisión nocturna del día. Muestra tareas de mañana en Motion, permite agregar nuevos tasks o eventos, guarda historial del día en daily-feedback/, y cierra con mensaje motivacional.
disable-model-invocation: true
---

# Skill: /cierre-dia

Revisión nocturna para preparar el día siguiente. Ejecutar cada noche a las 8 PM.

---

## PASO 1 — Obtener fechas

```bash
TODAY=$(python3 -c "from datetime import date; print(date.today())")
TOMORROW=$(python3 -c "from datetime import date, timedelta; print(date.today() + timedelta(days=1))")
DAY_NAME=$(python3 -c "
from datetime import date
days = ['Lunes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo']
print(days[date.today().weekday()])
")
```

---

## PASO 2 — Obtener resumen del día desde Motion

Consulta qué se completó y qué quedó pendiente hoy.

```bash
MOTION_KEY="ZqTdrhNz66tfCcZVFYUkhj3fFEP92L0V6aai2ZtX5k4="
TODAY=$(python3 -c "from datetime import date; print(date.today())")
TOMORROW=$(python3 -c "from datetime import date, timedelta; print(date.today() + timedelta(days=1))")

curl -s "https://api.usemotion.com/v1/tasks" \
  -H "X-API-Key: $MOTION_KEY" | python3 -c "
import sys, json
data = json.load(sys.stdin)
tasks = data.get('tasks', [])
today = '$TODAY'
tomorrow = '$TOMORROW'

completados = []
pendientes_hoy = []
para_manana = []

for t in tasks:
    due = (t.get('dueDate') or '')[:10]
    scheduled_today = any(c.get('scheduledStart','')[:10] == today for c in t.get('chunks', []))
    scheduled_tomorrow = any(c.get('scheduledStart','')[:10] == tomorrow for c in t.get('chunks', []))
    name = t.get('name','')
    priority = t.get('priority','')
    is_completed = t.get('completed') or t.get('status',{}).get('isResolvedStatus', False)

    if is_completed and (due == today or scheduled_today):
        completados.append({'name': name, 'priority': priority})
    elif not is_completed and (due and due <= today) or scheduled_today:
        pendientes_hoy.append({'name': name, 'priority': priority, 'due': due})
    elif not is_completed and (due == tomorrow or scheduled_tomorrow):
        chunks = t.get('chunks', [])
        times = [f\"{c['scheduledStart'][11:16]}–{c['scheduledEnd'][11:16]}\" for c in chunks if c.get('scheduledStart','')[:10] == tomorrow]
        para_manana.append({'name': name, 'priority': priority, 'times': times})

priority_order = {'ASAP': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3, '': 4}
pendientes_hoy.sort(key=lambda x: priority_order.get(x['priority'], 4))
para_manana.sort(key=lambda x: (priority_order.get(x['priority'], 4), x['times'][0] if x['times'] else 'zz'))

print('=== COMPLETADOS ===')
for t in completados:
    print(f\"[{t['priority']}] {t['name']}\")
print('=== PENDIENTES ===')
for t in pendientes_hoy:
    print(f\"[{t['priority']}] {t['name']} | venció: {t['due']}\")
print('=== MANANA ===')
for t in para_manana:
    time_str = ', '.join(t['times']) if t['times'] else 'sin hora'
    print(f\"[{t['priority']}] {t['name']} | {time_str}\")
"
```

---

## PASO 3 — Presentar reporte del día y mañana

Presenta el resultado:

---

**Cierre del día — [DAY_NAME] [TODAY]**

**✅ Completado hoy:**
[Lista de tasks completados o "Ninguno registrado en Motion"]

**⏳ Quedó pendiente:**
[Lista de tasks que vencían hoy y no se completaron]

**📋 Mañana en agenda:**
[Tasks para mañana con hora si tienen]

---

## PASO 4 — Preguntar por tasks o eventos nuevos para mañana

> "¿Hay algo que quieras agregar para mañana? Tasks nuevos o eventos con hora específica."

**Si Martin dice que no:** pasa al PASO 6.
**Si menciona tasks:** ejecuta PASO 5.

---

## PASO 5 — Agregar tasks en Motion

Workspace: `ws_qDBVZf3CLkJfmE3UDZeHxt`

Para cada task extraer nombre, hora/deadline, prioridad (default: MEDIUM), duración (default: 30 min).

```bash
MOTION_KEY="ZqTdrhNz66tfCcZVFYUkhj3fFEP92L0V6aai2ZtX5k4="
TOMORROW=$(python3 -c "from datetime import date, timedelta; print(date.today() + timedelta(days=1))")

curl -s -X POST "https://api.usemotion.com/v1/tasks" \
  -H "X-API-Key: $MOTION_KEY" \
  -H "Content-Type: application/json" \
  -d "{
    \"name\": \"[NOMBRE]\",
    \"workspaceId\": \"ws_qDBVZf3CLkJfmE3UDZeHxt\",
    \"dueDate\": \"${TOMORROW}T23:59:59.000Z\",
    \"priority\": \"MEDIUM\",
    \"duration\": 30
  }" | python3 -c "import sys,json; d=json.load(sys.stdin); print('✓ Creado:', d.get('name',''))"
```

Pregunta "¿Algo más?" hasta que Martin confirme.

---

## PASO 6 — Guardar historial del día

Genera el resumen del día y guárdalo en `daily-feedback/[TODAY].md`.

El archivo debe tener este formato exacto:

```markdown
# Resumen del día — [DAY_NAME] [TODAY]

## ✅ Completado
[lista de completados, o "Ninguno registrado"]

## ⏳ Pendiente (no completado)
[lista de pendientes con prioridad]

## 📋 Agendado para mañana
[lista de tasks de mañana]

## 📊 Métricas
- Tasks completados: N
- Tasks pendientes: N
- Tasa de completación: N%

## 💬 Notas del cierre
[Si Martin agregó comentarios o contexto durante la conversación, inclúyelos aquí. Si no dijo nada especial, escribe "Sin notas adicionales."]
```

Ejecuta:
```bash
# Claude escribe el archivo con Write tool
# Ruta: /Users/martinmercedes/Desktop/Executive assistant/daily-feedback/[TODAY].md
```

---

## PASO 7 — Mensaje motivacional

Lee `context/goals.md`.

Escribe un mensaje motivacional corto (3–5 líneas) directo y personal:
- Conecta lo de hoy con la meta grande
- Menciona el deadline más próximo si es inminente
- Tono de socio, no de coach

```
---
[Mensaje aquí]
---
Buenas noches, Martin. Mañana es un buen día para avanzar.
```

---

## Comportamiento especial

**Error de API Motion:** continúa igual, guarda lo que tengas en el historial.
**Nada completado:** escríbelo honestamente en el historial — es información útil.
**Martin agrega contexto** (ej: "no pude porque..."): inclúyelo en las Notas del cierre del historial.
