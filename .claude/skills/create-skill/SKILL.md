---
name: create-skill
description: Crea un nuevo skill para este asistente ejecutivo. Usar cuando Martin quiere automatizar una tarea repetitiva o formalizar un flujo de trabajo como skill invocable.
disable-model-invocation: true
---

# Skill: /create-skill

Crea el mejor skill posible para el asistente ejecutivo de Martin. Sigue los pasos en orden.

---

## PASO 1 — Entender qué hace el skill

Si Martin no proporcionó suficiente contexto con `$ARGUMENTS`, haz exactamente **una sola pregunta** que cubra todo:

> "Dime: ¿qué hace el skill, cuándo lo usarías (qué situación lo dispara), qué inputs necesita y qué output esperas?"

No hagas múltiples preguntas. Una sola vez.

Si el contexto es suficiente, continúa al PASO 2.

---

## PASO 2 — Revisar skills existentes

Lee los skills actuales para evitar duplicados y entender el estilo del proyecto:

```bash
ls .claude/skills/
```

Lee el `SKILL.md` de cualquier skill relacionado con lo que Martin quiere crear.

---

## PASO 3 — Decidir la configuración del frontmatter

Evalúa estas preguntas y define el frontmatter apropiado:

**¿El skill tiene efectos secundarios?** (crea archivos, llama APIs, manda mensajes, modifica datos)
→ Sí: agrega `disable-model-invocation: true` para que Claude no lo dispare solo

**¿El skill es solo contexto de referencia?** (convenciones, guías de estilo, reglas)
→ Sí: agrega `user-invocable: false` para que no aparezca en el menú `/`

**¿El skill necesita aislamiento?** (investigación profunda, tareas que no deben contaminar el contexto principal)
→ Sí: agrega `context: fork` y elige `agent: Explore` o `agent: general-purpose`

**¿El skill usa herramientas específicas?**
→ Lista solo las necesarias en `allowed-tools`

**¿El skill recibe argumentos del usuario?**
→ Usa `$ARGUMENTS` en el contenido del skill
→ Agrega `argument-hint` para mostrar en el autocompletado (ej: `[producto] [formato]`)

---

## PASO 4 — Diseñar la estructura del skill

Un skill de alta calidad tiene estas partes:

### Para skills de TAREA (pasos a ejecutar):
```
1. Cuándo usarlo — frases exactas que disparan el skill
2. Inputs requeridos — qué necesita antes de ejecutar
3. Pasos numerados — instrucciones claras y ejecutables
4. Output esperado — qué debe producir
5. Comportamiento especial — casos edge, errores, ambigüedad
```

### Para skills de REFERENCIA (conocimiento):
```
1. Contexto / propósito
2. Reglas o convenciones
3. Ejemplos concretos
4. Cuándo NO aplica
```

**Reglas de calidad:**
- Cada paso debe ser una instrucción ejecutable, no una descripción vaga
- Si el skill llama una API externa: incluye el comando exacto de curl/fetch
- Si el skill crea archivos: especifica la ruta exacta donde guardarlos
- Si el skill tiene inputs opcionales: documentar el default
- Máximo 500 líneas en SKILL.md — mover docs extensas a archivos separados en la carpeta del skill

---

## PASO 5 — Crear los archivos

**Ubicación correcta:**
- Si el skill es para este proyecto específico: `.claude/skills/[nombre]/SKILL.md`
- Si el skill debe estar disponible en todos los proyectos de Martin: `~/.claude/skills/[nombre]/SKILL.md`

Pregunta a Martin cuál prefiere si no está claro.

**Nombre del skill:**
- Solo letras minúsculas, números y guiones
- Máximo 64 caracteres
- Debe ser descriptivo y fácil de recordar (ej: `crear-propuesta`, `seguimiento-cliente`, `resumen-semana`)

Crea la carpeta y el `SKILL.md`. Si el skill requiere archivos de soporte (scripts, templates, ejemplos), créalos en subcarpetas dentro del directorio del skill.

---

## PASO 6 — Actualizar el backlog de skills

Lee `references/skills-backlog.md` y marca el skill como construido si estaba en el backlog. Si no estaba, agrega una nota de que fue creado hoy.

---

## PASO 7 — Confirmar y probar

Muestra a Martin:
1. El frontmatter elegido y por qué
2. El contenido del `SKILL.md` creado
3. Cómo invocarlo: `/nombre-del-skill [argumentos]`
4. Si aplica: qué archivos de soporte se crearon y para qué sirven

Pregunta: "¿Quieres ajustar algo antes de probarlo?"

---

## Comportamiento especial

**Si Martin describe algo muy amplio** (ej: "crea un skill para clientes") — identifica si debería ser uno o varios skills. Propón la división antes de crear nada.

**Si el skill ya existe** — no sobreescribas. Pregunta si quiere actualizar el existente o crear una variante.

**Si el skill necesita credenciales o API keys** — documenta claramente en el `SKILL.md` cómo configurarlas. Nunca hardcodear credenciales en el skill.
