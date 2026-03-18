---
name: buenos-dias
description: Briefing matutino de Martin. Lee el historial del día anterior, muestra tasks del día ordenados por prioridad, presenta objetivos y actualiza patrones de comportamiento en learning/patrones-martin.md.
disable-model-invocation: true
---

# Skill: /buenos-dias

Briefing completo para comenzar el día. Ejecutar cada mañana.

---

## PASO 1 — Obtener fechas

```bash
TODAY=$(python3 -c "from datetime import date; print(date.today())")
YESTERDAY=$(python3 -c "from datetime import date, timedelta; print(date.today() - timedelta(days=1))")
TOMORROW=$(python3 -c "from datetime import date, timedelta; print(date.today() + timedelta(days=1))")
DAY_NAME=$(python3 -c "
from datetime import date
days = ['Lunes','Martes','Miércoles','Jueves','Viernes','Sábado','Domingo']
print(days[date.today().weekday()])
")
```

---

## PASO 2 — Leer historial del día anterior

Lee el archivo `daily-feedback/[YESTERDAY].md`.

- Si existe: extrae tareas pendientes, tasa de completación y notas del cierre.
- Si no existe: continúa sin contexto previo (es el primer día o no se hizo el cierre).

---

## PASO 3 — Obtener tasks del día desde Motion

```bash
MOTION_KEY="augilx5IOiuSy0LqZfDZ+xf9+HgSAk5UFsa9R2c2Jd4="
TODAY=$(python3 -c "from datetime import date; print(date.today())")
TOMORROW=$(python3 -c "from datetime import date, timedelta; print(date.today() + timedelta(days=1))")

curl -s "https://api.usemotion.com/v1/tasks" \
  -H "X-API-Key: $MOTION_KEY" | python3 -c "
import sys, json
data = json.load(sys.stdin)
tasks = data.get('tasks', [])
today = '$TODAY'
tomorrow = '$TOMORROW'

results = []
for t in tasks:
    if t.get('completed'): continue
    due = (t.get('dueDate') or '')[:10]
    scheduled_today = any(c.get('scheduledStart','')[:10] == today for c in t.get('chunks', []))
    if due == today or due == tomorrow or scheduled_today or (due and due < today):
        chunks = t.get('chunks', [])
        times = []
        for c in chunks:
            if c.get('scheduledStart','')[:10] == today:
                start = c.get('scheduledStart','')[11:16]
                end = c.get('scheduledEnd','')[11:16]
                times.append(f'{start}–{end}')
        category = 'VENCIDA' if (due and due < today and not scheduled_today and due != today and due != tomorrow) else 'HOY'
        results.append({
            'name': t.get('name',''),
            'priority': t.get('priority',''),
            'due': due,
            'times': times,
            'project': (t.get('project') or {}).get('name',''),
            'category': category,
        })

priority_order = {'ASAP': 0, 'HIGH': 1, 'MEDIUM': 2, 'LOW': 3, '': 4}
results.sort(key=lambda x: (
    0 if x['category'] == 'VENCIDA' else 1,
    priority_order.get(x['priority'], 4),
    x['times'][0] if x['times'] else 'zz'
))

for r in results:
    time_str = ', '.join(r['times']) if r['times'] else 'sin hora'
    proj = f\"|{r['project']}\" if r['project'] else ''
    flag = ' ⚠️' if r['category'] == 'VENCIDA' else ''
    print(f\"{r['category']}|{r['priority']}|{r['name']}{proj}|{time_str}{flag}\")
"
```

---

## PASO 4 — Leer patrones y objetivos

Lee estos archivos:
- `learning/patrones-martin.md` — patrones de comportamiento acumulados
- `context/goals.md` — metas del trimestre
- `context/current-priorities.md` — foco actual

---

## PASO 5 — Actualizar patrones de comportamiento

Después de obtener las tareas del día, actualiza `learning/patrones-martin.md`:

**A. Blockers crónicos:**
- Para cada tarea vencida: si ya está en la tabla, incrementa "Veces aparecida". Si es nueva, agrégala.
- Si una tarea lleva 14+ días en la tabla, agrégala también a "Observaciones del comportamiento" como patrón confirmado.

**B. Tasa de completación:**
- Si existen datos del día anterior (del cierre o de Motion), agrega una fila a la tabla de tasas.
- Calcula: (completadas / total pendientes de ayer) * 100

**C. Logros recientes:**
- Si ayer se completó alguna tarea que llevaba 3+ días vencida, regístrala como logro con fecha.

**D. Racha de productividad:**
- Actualiza el contador de días consecutivos con >50% completación.

**E. Log de actualizaciones:**
- Agrega una línea al log con fecha y resumen de 1 línea (ej: "8 tareas vencidas, 1 nueva: X. Completadas ayer: 2/5").

---

## PASO 6 — Presentar el briefing completo

Presenta con este formato:

---

**Buenos días, Martin. [DAY_NAME] [TODAY]**

---

**📊 Cómo cerró ayer ([YESTERDAY]):**

[Si existe el historial de ayer:]
- Completado: N tasks (tasa: N%)
- Quedó pendiente: [lista breve de los más importantes]
- [Si hay notas del cierre: mostrarlas en 1 línea]

[Si no existe historial: omitir esta sección]

---

**📋 TUS TASKS DE HOY**

[Lista numerada ordenada. Vencidas primero con ⚠️, luego por prioridad.]

Formato por línea:
`N. [PRIORIDAD] Nombre | hora | proyecto`

Si no hay tasks: "Motion no tiene nada agendado para hoy."

---

**🎯 TUS OBJETIVOS**

**Urgente — próximas semanas:**
[2-3 prioridades más cercanas en deadline]

**Q2 2026:**
[Metas del trimestre con fecha y estado estimado]

**Meta grande:**
[Meta principal de ingresos en una línea]

---

**🧠 Patrón del día**
[1 observación concreta basada en `learning/patrones-martin.md`. Solo si hay algo relevante: un blocker crónico que se repite, una racha positiva, o un patrón que vale mencionar. Si no hay nada nuevo, omitir esta sección. Máximo 2 líneas. Sin moralizar.]

---

**💬 Para arrancar**
[1-2 líneas directas. Si ayer quedó algo pendiente importante, mencionarlo. Conecta la tarea más urgente de hoy con la meta más importante. Tono de socio, no de coach.]

---

## Reglas de formato

- Español siempre
- Sin frases de relleno
- Si hay más de 7 tasks, agrupar los menos urgentes bajo "Resto del día"
- El contexto de ayer debe ser breve — no más de 3 líneas
- Si la tasa de completación de ayer fue baja (<50%), mencionarlo directamente sin suavizarlo
- La sección "Patrón del día" solo aparece si hay algo que valga la pena decir — no inventar observaciones
