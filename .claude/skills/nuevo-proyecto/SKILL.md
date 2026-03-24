---
name: nuevo-proyecto
description: Use when Martin wants to create a new project, do reverse engineering of a goal, plan a project from scratch, or convert a binary objective into a full action plan with tasks in Motion.
disable-model-invocation: true
argument-hint: [objetivo binario del proyecto]
---

# Skill: /nuevo-proyecto

Toma un objetivo binario, lo convierte en SMART, hace reverse engineering completo y opcionalmente crea el proyecto con todas las tareas en Motion.

---

## PASO 1 — Recibir el objetivo

Si el objetivo viene como argumento (`$1`), usarlo directamente.

Si no viene, preguntar:

> "Dame el objetivo binario del proyecto. Ejemplo: 'Facturar $5,000/mes antes del 30 sep 2026. ¿Cumplido? ✅ / ❌'"

---

## PASO 2 — Convertir a objetivo SMART

Analizar el objetivo y reformularlo en formato SMART. Presentar así:

---

**🎯 OBJETIVO SMART**

[Versión reformulada en 1-2 oraciones]

| Dimensión | Detalle |
|-----------|---------|
| Específico | ... |
| Medible | ... |
| Alcanzable | ... (honesto con el contexto real de Martin) |
| Relevante | ... |
| Tiempo | ... |

**¿Ajustamos algo o arrancamos con el reverse engineering?**

---

Esperar confirmación antes de continuar.

---

## PASO 3 — Reverse Engineering completo

Trabajar hacia atrás desde el objetivo hasta hoy. Presentar en estos niveles:

### Nivel 1 — Estado final
¿Qué tiene que ser verdad el día del deadline para que el objetivo esté cumplido?

### Nivel 2 — Hitos clave (milestones)
3-6 hitos intermedios con fecha aproximada cada uno.

### Nivel 3 — Palancas críticas
3-5 acciones/decisiones que si no ocurren, el objetivo falla.

### Nivel 4 — Obstáculos reales
Riesgos concretos basados en el contexto de Martin (opera solo, RD, ingresos actuales).

### Nivel 5 — Recursos necesarios
Qué hace falta: herramientas, dinero, personas, tiempo semanal.

### Nivel 6 — Tareas de las próximas 2 semanas
Acciones concretas, ordenadas por prioridad, con fecha y duración estimada.

---

Al terminar preguntar:

> **¿Quieres que cree este proyecto en Motion con todas las tareas organizadas por fases?** (sí / no / ajustar primero)

---

## PASO 4 — Crear en Motion (solo si Martin confirma)

### 4a — Crear el proyecto

```bash
MOTION_KEY="DZ4rBKFQPEQdT1etPajO+ECXJym97X+Iu0FDF3kKG0Y="

curl -s -X POST "https://api.usemotion.com/v1/projects" \
  -H "X-API-Key: $MOTION_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "[NOMBRE DEL PROYECTO]",
    "workspaceId": "ws_qDBVZf3CLkJfmE3UDZeHxt",
    "dueDate": "[FECHA LÍMITE ISO 8601]",
    "description": "[OBJETIVO SMART]"
  }'
```

Guardar el `id` del proyecto.

### 4b — Crear tareas como PM profesional

Estructura de PM: cada tarea lleva prefijo de fase `[F0-1]`, prioridad correcta y duración en minutos.

Para cada tarea:

```bash
MOTION_KEY="DZ4rBKFQPEQdT1etPajO+ECXJym97X+Iu0FDF3kKG0Y="

curl -s -X POST "https://api.usemotion.com/v1/tasks" \
  -H "X-API-Key: $MOTION_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "[NOMBRE CON PREFIJO DE FASE]",
    "workspaceId": "ws_qDBVZf3CLkJfmE3UDZeHxt",
    "projectId": "[PROJECT_ID]",
    "dueDate": "[FECHA ISO 8601]",
    "priority": "[ASAP | HIGH | MEDIUM | LOW]",
    "duration": [MINUTOS]
  }'
```

Confirmar cada tarea creada con ✅.

### 4c — Confirmar al final

Mostrar resumen:
- Proyecto creado
- N tareas por fase
- Tarea más urgente hoy

---

## PASO 5 — Guardar en el proyecto local

Crear `projects/[nombre-kebab]/README.md` con:
- Objetivo binario original
- Objetivo SMART
- Hitos clave
- Deadline
- Fecha de creación

---

## Reglas

- Español siempre
- El SMART debe ser honesto — si el objetivo es muy ambicioso dado el contexto real, decirlo
- El reverse engineering debe ser realista, no motivacional
- Esperar confirmación explícita antes de tocar Motion
- Si falla la API de Motion, reportar el error exacto
- Estructurar tareas como PM profesional: prefijos de fase, prioridades reales, duraciones estimadas
