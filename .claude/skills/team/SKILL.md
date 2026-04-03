---
name: team
description: Use when someone asks to create an agent team, spawn teammates, coordinate parallel work, launch agents in parallel, or uses /team.
argument-hint: [descripción del objetivo o proyecto]
---

## Goal

Dado un objetivo, diseña y lanza directamente un agent team siguiendo las mejores prácticas: cada teammate owns archivos específicos, los entregables son concretos, los mensajes entre teammates tienen recipients nombrados, y cada uno recibe contexto completo al hacer spawn.

---

## Reglas obligatorias

### DO
- **Own specific files** — cada teammate trabaja en archivos distintos, sin overlap
- **Define output** — cada teammate tiene un entregable concreto y medible
- **Name recipients** — los mensajes entre teammates nombran explícitamente a quién van (ej: "message Frontend Dev with the API contract")
- **3-5 teammates** — tamaño óptimo para balance entre paralelismo y coordinación
- **Give full context** — el spawn prompt incluye: objetivo, archivos a tocar, qué esperar de otros teammates, y entregable final

### DON'T
- **Share same file** — dos teammates editando el mismo archivo = sobreescrituras
- **Vague deliverables** — "haz lo que puedas" no es un entregable
- **Assume the plan** — no crear el equipo sin definir roles, archivos y mensajes
- **10+ teammates** — demasiado overhead de coordinación
- **No history given** — nunca hacer spawn sin contexto del proyecto

---

## Cuándo NO crear un team

- Las tareas son secuenciales (B depende de A que depende de otro)
- Todos los cambios van al mismo archivo
- La tarea la puede hacer un solo Claude en minutos
- No hay paralelismo real — solo trabajo serial disfrazado

---

## Pasos de ejecución

### Paso 1: Analizar el objetivo

Antes de crear el equipo, responder:
- ¿Hay trabajo genuinamente paralelizable?
- ¿Se pueden dividir los archivos sin overlap?
- ¿Cuántos roles distintos requiere la tarea? (= número de teammates)
- ¿Qué información necesita pasar de un teammate a otro, y cuándo?

Si la respuesta a "¿hay paralelismo real?" es no → hacer la tarea directamente sin crear un team.

### Paso 2: Diseñar los roles

Para cada teammate definir:
1. **Nombre del rol** — descriptivo y funcional (ej: "Backend Dev", "Security Reviewer", "QA")
2. **Responsabilidad** — una oración clara de qué hace
3. **Archivos propios** — rutas exactas que solo este teammate toca
4. **Dependencias** — si debe esperar un mensaje de otro teammate antes de empezar
5. **Mensaje a enviar** — qué información pasa a quién cuando termina
6. **Entregable** — output concreto (archivo, reporte, endpoint, etc.)

### Paso 3: Construir el prompt estructurado

Usar esta plantilla exacta:

```
Goal: [objetivo en 1-2 oraciones. Incluir URL, puerto, o contexto técnico clave si aplica.]

Create a team of [N] teammates using Sonnet:

1. **[Nombre Rol]** — [responsabilidad en 1 oración].
   Files: [rutas exactas].
   When done, message [Nombre Recipient] with [información específica a pasar].

2. **[Nombre Rol]** — [responsabilidad en 1 oración].
   Files: [rutas exactas].
   Wait for [Nombre Sender]'s message with [qué espera], then [acción].

3. **[Nombre Rol]** — [responsabilidad en 1 oración].
   Files: [rutas exactas].
   Start with [tarea inicial independiente], then [tarea que depende de otros] once [condición].

Final deliverables:
- [ruta/archivo] — [descripción de qué contiene]
- [ruta/archivo] — [descripción de qué contiene]
- [URL o endpoint] — [qué debe funcionar]
```

### Paso 4: Lanzar el team

Con el prompt estructurado listo, ejecutar directamente — no mostrar el prompt al usuario y preguntar si procede. **Crear el equipo de inmediato.**

Si el usuario provee `$ARGUMENTS`, usarlos como descripción del objetivo para el Paso 1.

---

## Ejemplos de referencia

### Full-stack app

```
Goal: Build a working full-stack app with a REST API and React frontend.
Everything running at http://localhost:3000.

Create a team of 3 teammates using Sonnet:

1. **Backend Dev** — Build the REST API in src/api/. Create routes for users and posts.
   Files: src/api/.
   When done, message Frontend Dev with the API endpoints and request/response schemas.

2. **Frontend Dev** — Build the React UI in src/components/. Wire up fetch calls to the API.
   Files: src/components/.
   Wait for Backend Dev's message with the API contract, then implement the UI.

3. **QA** — Write tests in tests/. Start with unit test scaffolding, then add integration tests once Backend and Frontend are done.
   Files: tests/.
   Start independently, coordinate with both devs when ready for integration.

Final deliverables:
- http://localhost:3000 — running app
- tests/report.md — pass/fail test results
- docs/build-summary.md — what was built, key decisions, how to run it
```

### Code review paralelo

```
Goal: Review PR #142 for security, performance, and test coverage. Report findings with severity ratings.

Create a team of 3 teammates using Sonnet:

1. **Security Reviewer** — Audit authentication, input validation, and data handling.
   Files: Read-only review of src/auth/, src/api/.
   When done, message Lead with findings list (HIGH/MEDIUM/LOW severity).

2. **Performance Reviewer** — Profile query patterns, N+1 risks, and bundle size impact.
   Files: Read-only review of src/db/, src/components/.
   When done, message Lead with findings list.

3. **Test Coverage Reviewer** — Check test coverage, missing edge cases, and integration gaps.
   Files: Read-only review of tests/.
   When done, message Lead with coverage gaps and recommendations.

Final deliverables:
- docs/pr-review.md — consolidated findings from all three reviewers
```

### Agencia Pixel Agents — nuevo cliente

Trigger: `/team agencia [nombre-cliente]`

Este template lanza el equipo completo de la agencia. El CEO Agent hace el brief primero, luego coordina a todos los especialistas en 3 fases con aprobación de Martin entre cada una.

```
Goal: Launch full agency workflow for client [NOMBRE] in [NICHO].
All files under projects/clientes/[NOMBRE]/.
CEO Agent runs client brief first, then coordinates 3 phases with Martin's approval between each.

Create a team of 7 teammates using Sonnet:

1. **CEO Agent** (agent type: ceo-agent) — Run the client brief with Martin first (10 clarification questions). Save answers to projects/clientes/[NOMBRE]/brief.md. Then coordinate the full team across 3 phases. Consolidate reports and request Martin's plan approval before Phase 2 and Phase 3. Final output: CEO-report.md.
   Files: projects/clientes/[NOMBRE]/brief.md, projects/clientes/[NOMBRE]/CEO-report.md
   Require plan approval before advancing to Phase 2 and Phase 3.

2. **MKR Specialist** (agent type: mrk-specialist) — Run /market-research skill for [NOMBRE]. Read brief at projects/clientes/[NOMBRE]/brief.md first.
   Files: projects/clientes/[NOMBRE]/market-research/
   Wait for CEO Agent's Phase 1 go signal, then start.
   When done, message CEO Agent with: key audience insights, top 3 pain points, primary desire, and #1 actionable insight.

3. **TPA Analyst** (agent type: tpa-analyst) — Analyze top 5 competitors in [NICHO] using template at templates/TPA-top-player-analysis.md. Read brief first.
   Files: projects/clientes/[NOMBRE]/top-player-analysis/
   Wait for CEO Agent's Phase 1 go signal, then start (parallel with MKR Specialist).
   When done, message CEO Agent with: top 3 replicable patterns and #1 market gap.

4. **WWP Writer** (agent type: wwp-writer) — Execute Winner's Writing Process using template at templates/WWP-winners-writing-process.md. Read MKR + TPA outputs first.
   Files: projects/clientes/[NOMBRE]/WWP/
   Wait for CEO Agent's Phase 2 approval, then start.
   When done, message CEO Agent AND Copywriter with the full messaging framework.

5. **Copywriter** (agent type: copywriter) — Write landing copy, 3 ad variations, and 3-email sequence.
   Files: projects/clientes/[NOMBRE]/copy/
   Wait for WWP Writer's message with the messaging framework, then start.
   When done, message CEO Agent AND Frontend Dev: "Copy ready at projects/clientes/[NOMBRE]/copy/"

6. **Frontend Dev** (agent type: frontend-dev) — Build landing page using /frontend-design skill. Use copy from Copywriter verbatim.
   Files: projects/clientes/[NOMBRE]/landing/
   Wait for Copywriter's message, then start.
   When done, message CEO Agent AND Backend Dev with all form element IDs.

7. **Backend Dev** (agent type: backend-dev) — Build form integrations and automations based on client's tools (from brief).
   Files: projects/clientes/[NOMBRE]/integraciones/
   Wait for Frontend Dev's message with form IDs, then start.
   When done, message CEO Agent: "Backend complete."

Final deliverables:
- projects/clientes/[NOMBRE]/brief.md — client brief
- projects/clientes/[NOMBRE]/CEO-report.md — executive summary
- projects/clientes/[NOMBRE]/market-research/ — full MKR
- projects/clientes/[NOMBRE]/top-player-analysis/ — full TPA
- projects/clientes/[NOMBRE]/WWP/ — messaging framework
- projects/clientes/[NOMBRE]/copy/ — all copy assets
- projects/clientes/[NOMBRE]/landing/index.html — landing page
- projects/clientes/[NOMBRE]/integraciones/ — integrations
```

---

## Notas

- Los teammates NO heredan el historial de conversación del lead. Todo el contexto necesario debe ir en el spawn prompt.
- Si una tarea se puede hacer en < 10 minutos con un solo Claude, no crear team.
- Después del spawn, usar `Shift+Down` para ciclar entre teammates y hablarles directamente.
- Para tareas de investigación (no escritura de código), los teams son especialmente efectivos: un teammate por ángulo del problema.
