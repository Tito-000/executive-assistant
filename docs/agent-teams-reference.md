# Agent Teams — Guía de Referencia Maestra

> Fuente: https://code.claude.com/docs/en/agent-teams
> Requiere: Claude Code v2.1.32+

---

## Qué son los Agent Teams

Múltiples instancias de Claude Code trabajando juntas. Una sesión actúa como **team lead** (coordinador), los demás son **teammates** (trabajadores independientes, cada uno con su propio context window).

A diferencia de los subagentes, los teammates pueden:
- Comunicarse directamente entre sí (no solo reportar al lead)
- Ser abordados por el usuario directamente sin pasar por el lead
- Reclamar tareas de una lista compartida de forma autónoma

---

## Cuándo usar Agent Teams (y cuándo no)

### Usar cuando:
- **Investigación paralela**: múltiples ángulos de un problema simultáneamente
- **Módulos independientes**: cada teammate dueño de archivos distintos
- **Debugging con hipótesis competidoras**: testar teorías en paralelo
- **Cambios cross-layer**: frontend + backend + tests, cada uno en un teammate

### NO usar cuando:
- Las tareas son secuenciales (dependen unas de otras)
- Varios teammates editarían el mismo archivo
- La tarea es simple — un solo Claude es más eficiente
- Los tokens importan: cada teammate consume su propio context window

### Comparación con Subagentes

| | Subagentes | Agent Teams |
|---|---|---|
| Contexto | Propio; resultados regresan al caller | Propio; completamente independiente |
| Comunicación | Solo reportan al agente principal | Se mensajean directamente entre sí |
| Coordinación | El main agent gestiona todo | Lista de tareas compartida, auto-coordinación |
| Mejor para | Tareas focalizadas donde solo importa el resultado | Trabajo complejo que requiere debate y colaboración |
| Costo tokens | Menor | Mayor (cada teammate = instancia separada) |

---

## Activación

```json
// ~/.claude/settings.json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

O como variable de entorno en el shell.

---

## Cómo crear un equipo

Describir en lenguaje natural la tarea y la estructura deseada:

```
I'm designing a CLI tool that helps developers track TODO comments across
their codebase. Create an agent team to explore this from different angles: one
teammate on UX, one on technical architecture, one playing devil's advocate.
```

Claude crea el equipo, asigna tareas y coordina. El lead no actúa sin tu aprobación.

---

## Modos de display

| Modo | Descripción | Requisito |
|---|---|---|
| **in-process** (default) | Todos los teammates en el terminal principal. `Shift+Down` para ciclar. | Cualquier terminal |
| **split panes** | Cada teammate en su propio panel. Ver todo simultáneamente. | tmux o iTerm2 |

Para forzar in-process:
```bash
claude --teammate-mode in-process
```

O permanentemente en `~/.claude.json`:
```json
{ "teammateMode": "in-process" }
```

---

## Controles clave

| Acción | Cómo |
|---|---|
| Ciclar entre teammates | `Shift+Down` (in-process) |
| Ver sesión de un teammate | `Enter` en su prompt |
| Interrumpir turno actual | `Escape` |
| Ver lista de tareas | `Ctrl+T` |
| Mensajear al lead directamente | Escribir en su terminal |
| Mensajear a un teammate | `Shift+Down` hasta llegar, luego escribir |

---

## Arquitectura interna

```
Team Lead (sesión principal)
├── Teammates (instancias independientes)
├── Task List (lista compartida de trabajo)
└── Mailbox (mensajería entre agentes)
```

Almacenamiento local:
- Team config: `~/.claude/teams/{team-name}/config.json`
- Task list: `~/.claude/tasks/{team-name}/`

> No editar estos archivos manualmente — se sobreescriben en cada actualización de estado.

---

## Gestión de tareas

- Estados: `pending` → `in progress` → `completed`
- Las tareas pueden tener dependencias (una tarea bloqueada se desbloquea automáticamente cuando su dependencia se completa)
- El lead asigna tareas o los teammates las reclaman solos
- File locking previene race conditions cuando varios teammates reclaman la misma tarea

---

## Aprobación de planes (para tareas críticas)

```
Spawn an architect teammate to refactor the authentication module.
Require plan approval before they make any changes.
```

Flujo:
1. Teammate trabaja en modo read-only (plan mode)
2. Envía plan al lead para aprobación
3. Lead aprueba o rechaza con feedback
4. Si rechazado → teammate revisa y reenvía
5. Si aprobado → teammate implementa

Para influir en las decisiones del lead: "only approve plans that include test coverage"

---

## Especificar teammates y modelos

```
Create a team with 4 teammates to refactor these modules in parallel.
Use Sonnet for each teammate.
```

También se puede referenciar un subagent type predefinido:
```
Spawn a teammate using the security-reviewer agent type to audit the auth module.
```

---

## Shutdown y limpieza

```
Ask the researcher teammate to shut down
```
```
Clean up the team
```

> Siempre limpiar desde el lead. Los teammates no deben correr cleanup (puede dejar recursos en estado inconsistente).

---

## Hooks para control de calidad

| Hook | Cuándo corre | Uso |
|---|---|---|
| `TeammateIdle` | Cuando un teammate está por quedar idle | Exit code 2 para enviar feedback y mantenerlo trabajando |
| `TaskCreated` | Cuando se crea una tarea | Exit code 2 para prevenir creación con feedback |
| `TaskCompleted` | Cuando se marca una tarea como completa | Exit code 2 para prevenir cierre con feedback |

---

## Best Practices

### Tamaño del equipo
- **Empezar con 3-5 teammates** — balance entre paralelismo y overhead de coordinación
- 5-6 tareas por teammate es el punto óptimo
- Escalar solo cuando el trabajo genuinamente se beneficia de paralelismo
- Tres teammates enfocados > cinco dispersos

### Contexto en el spawn prompt
Los teammates NO heredan el historial del lead. Incluir todo el contexto necesario en el spawn prompt:

```
Spawn a security reviewer teammate with the prompt: "Review the authentication module
at src/auth/ for security vulnerabilities. Focus on token handling, session
management, and input validation. The app uses JWT tokens stored in
httpOnly cookies. Report any issues with severity ratings."
```

### Tamaño de tareas
- **Muy pequeñas**: el overhead de coordinación supera el beneficio
- **Muy grandes**: demasiado tiempo sin check-ins = riesgo de trabajo desperdiciado
- **Ideal**: unidades auto-contenidas con entregable claro (una función, un archivo de tests, un review)

### Evitar conflictos de archivos
Dos teammates editando el mismo archivo = sobreescrituras. Dividir trabajo para que cada teammate sea dueño de archivos distintos.

### Si el lead empieza a implementar en vez de delegar
```
Wait for your teammates to complete their tasks before proceeding
```

### Empezar con research/review
Si es la primera vez con agent teams, empezar con tareas sin escritura de código: revisar un PR, investigar una librería, debuggear un bug.

---

## Ejemplos de uso

### Code review paralelo

```
Create an agent team to review PR #142. Spawn three reviewers:
- One focused on security implications
- One checking performance impact
- One validating test coverage
Have them each review and report findings.
```

### Investigación con hipótesis competidoras

```
Users report the app exits after one message instead of staying connected.
Spawn 5 agent teammates to investigate different hypotheses. Have them talk to
each other to try to disprove each other's theories, like a scientific
debate. Update the findings doc with whatever consensus emerges.
```

La estructura de debate es clave: evita el anchoring de la investigación secuencial.

---

## Limitaciones actuales (experimental)

| Limitación | Detalle |
|---|---|
| Sin resumption in-process | `/resume` y `/rewind` no restauran teammates in-process |
| Task status puede lagear | Verificar manualmente si una tarea parece stuck |
| Shutdown lento | Los teammates terminan su turno actual antes de apagarse |
| Un equipo por sesión | Limpiar el equipo actual antes de crear uno nuevo |
| Sin equipos anidados | Solo el lead puede crear teammates |
| Lead fijo | No se puede promover un teammate a lead |
| Permisos en spawn | Todos los teammates heredan los permisos del lead; no se pueden configurar por teammate en el spawn |
| Split panes: solo tmux/iTerm2 | No funciona en VS Code terminal, Windows Terminal, o Ghostty |

---

## Troubleshooting

| Problema | Solución |
|---|---|
| Teammates no aparecen | Presionar `Shift+Down`; verificar que la tarea sea suficientemente compleja; verificar que tmux esté instalado |
| Demasiados prompts de permisos | Pre-aprobar operaciones comunes en permission settings antes de crear el equipo |
| Teammate se detiene en error | Darle instrucciones directamente o crear un teammate de reemplazo |
| Lead cierra antes de terminar | Decirle explícitamente que continúe o que espere a los teammates |
| Sesiones tmux huérfanas | `tmux ls` → `tmux kill-session -t <session-name>` |

---

## Permisos

Los teammates heredan los permisos del lead al momento del spawn. Si el lead corre con `--dangerously-skip-permissions`, todos los teammates también. Se pueden cambiar los modos de teammates individuales después del spawn.

---

## Tokens y costo

- Los tokens escalan linealmente con el número de teammates
- Cada teammate tiene su propio context window completo
- Para research, review y features nuevas: el costo extra generalmente vale la pena
- Para tareas rutinarias: una sola sesión es más eficiente
