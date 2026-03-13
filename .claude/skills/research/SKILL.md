# Skill: /research

**Invocación:** `/research [tema o pregunta]`

Este skill ejecuta investigación profunda usando la API de Perplexity, con el contexto del negocio de Martin inyectado en cada query. Sigue los pasos en orden.

---

## PASO 1 — Verificar credencial

Lee el archivo `.env` en la raíz del proyecto. Extrae el valor de `PERPLEXITY_API_KEY`.

Si el archivo no existe, o el valor está vacío, o es `your_key_here`, detente y avisa:

> "No hay PERPLEXITY_API_KEY configurada. Abre el archivo `.env` en la raíz del proyecto y reemplaza `your_key_here` con tu clave de Perplexity."

---

## PASO 2 — Cargar contexto de forma selectiva

**Siempre leer:**
- `context/me.md`
- `context/work.md`

**Leer también si el tema se relaciona con negocio, ventas, marketing, funnels, embudos, clientes, agencia, Immunotec, productos, prospectos, ads, conversión, ingresos, rango, duplicación, equipo, kits:**
- `context/current-priorities.md`
- `context/goals.md`

**Leer también si el tema menciona un proyecto específico por nombre** (dra aurys, memorama, beatriz, fase 1, fase 2, fase 3, fase 4, battlefronts):
- `projects/[nombre-del-proyecto]/README.md`

**Temas personales puros** (salud general, meditación, relaciones, gastronomía, finanzas personales, lifestyle) → solo cargar `me.md` y `work.md`.

No cargar más archivos de los necesarios. El system prompt de Perplexity tiene límite de tokens y el contexto diluido produce peores resultados.

---

## PASO 3 — Construir el system prompt

Usando lo que leíste, construye el system prompt para Perplexity. La base siempre es:

```
You are a research analyst working for Martin Mercedes, an independent Immunotec consultant (Diamond rank, working toward Gold) and freelance digital marketer based in Santo Domingo, Dominican Republic.

His two revenue streams:
1. Immunotec — promotes wellness products and the business opportunity through digital sales funnels. Current revenue: ~100,000–130,000 DOP/month. Ad spend: ~$600 USD/month. Goal: sell 8 starter kits/month to reach Gold rank.
2. Digital marketing agency (unnamed, in formalization) — builds revenue-generating sales funnels for clients. Current clients: plastic surgeon (Dra. Aurys Mercedes) and an embroidery/personalization company (Memorama RD).

Martin operates solo from the Dominican Republic. Consider local market context where relevant: purchasing power, platform usage patterns (WhatsApp is primary communication), competitive landscape in RD and Latin America.
```

Si cargaste `current-priorities.md` y `goals.md`, agrega al final del system prompt:

```
Current priorities and deadlines (for relevance filtering):
[lista de prioridades y fechas clave del contexto cargado]
```

Cierra el system prompt con:

```
Your job: research the topic below with this lens. Prioritize non-obvious insights — things most people in his position would miss. Flag anything directly actionable for his specific situation. Be direct and specific, not generic.

Respond primarily in Spanish. Use English only when precision requires it (technical terms, direct quotes from sources, etc.).
```

---

## PASO 4 — Llamar a la API de Perplexity

Construye el JSON body y ejecuta la llamada via Bash/curl. Usa un archivo temporal para el JSON para evitar problemas de escape de caracteres especiales:

```bash
# Extraer la clave del .env
PERPLEXITY_KEY=$(grep 'PERPLEXITY_API_KEY' .env | cut -d '=' -f2 | tr -d ' \r')

# Construir el JSON en un archivo temporal
TMPFILE=$(mktemp /tmp/perplexity_request_XXXXXX.json)

# Escribir el JSON al archivo temporal usando Python para manejar el escape correctamente
python3 -c "
import json, sys

system_prompt = '''[SYSTEM PROMPT CONSTRUIDO EN PASO 3]'''
user_query = '''[TEMA EXACTAMENTE COMO LO ESCRIBIÓ MARTIN]'''

payload = {
    'model': 'sonar-deep-research',
    'messages': [
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': user_query}
    ]
}
print(json.dumps(payload))
" > \$TMPFILE

# Ejecutar la llamada
RESPONSE=\$(curl -s -w '\n%{http_code}' https://api.perplexity.ai/chat/completions \
  -H "Authorization: Bearer \$PERPLEXITY_KEY" \
  -H "Content-Type: application/json" \
  -d @\$TMPFILE)

# Limpiar archivo temporal
rm -f \$TMPFILE

# Separar cuerpo y código HTTP
HTTP_CODE=\$(echo "\$RESPONSE" | tail -1)
BODY=\$(echo "\$RESPONSE" | head -n -1)

# Verificar respuesta
if [ "\$HTTP_CODE" != "200" ]; then
  echo "Error HTTP \$HTTP_CODE:"
  echo "\$BODY"
  exit 1
fi

# Extraer el contenido
echo "\$BODY" | python3 -c "import json,sys; data=json.load(sys.stdin); print(data['choices'][0]['message']['content'])"
```

**Nota:** `sonar-deep-research` tarda entre 15 y 60 segundos — es normal. No es un error.

Si el curl falla, el HTTP code no es 200, o la extracción del contenido falla: muestra el error completo y detente. No reintentes automáticamente.

---

## PASO 5 — Sintetizar y presentar el output

No devuelvas el raw de Perplexity. Procesa y presenta con esta estructura:

---

**Investigación: [tema]**
*Perplexity sonar-deep-research — [fecha actual]*

**Lo que encontré**
[2–4 párrafos con los hallazgos principales, sintetizados. Datos concretos cuando los haya. Bullet points solo si hay 4+ ítems discretos que no conectan narrativamente.]

**Qué significa para tu situación**
[1–3 párrafos. Esta es la capa que Perplexity no puede dar solo — filtra los hallazgos a través del contexto de Martin: sus dos negocios, el mercado RD, su etapa actual. Señala lo que es directamente relevante y lo que no aplica a su caso.]

**Lo que puedes hacer con esto**
[Acciones concretas, ordenadas por impacto o urgencia. Máximo 5. Si no hay acciones claras todavía, explica brevemente qué faltaría para que las hubiera.]

**Fuentes**
[Si Perplexity incluye fuentes/citas en la respuesta, listarlas aquí. Si no incluye, omitir esta sección.]

---

**Reglas de formato:**
- Idioma: español por defecto. Mezcla según lo que sea más preciso.
- Tono: directo. Sin frases de IA. No empieces con "Aquí están los resultados" ni nada similar — ve directo a los hallazgos.
- No guardes el output en ningún archivo a menos que Martin lo pida explícitamente. Si lo pide, guarda en `references/research/[YYYY-MM-DD]-[slug-del-tema].md`.

---

## Comportamiento especial

**Si el tema es ambiguo** (ej. "investiga la competencia" sin especificar cuál de los dos negocios), pregunta antes de ejecutar la llamada. Una sola pregunta de clarificación, no un interrogatorio.

**Si el tema es muy amplio** y claramente generaría resultados dispersos (ej. "investiga marketing digital"), propón 2–3 enfoques más específicos y deja que Martin elija antes de ejecutar.

**Si Martin pide dos temas relacionados** (ej. "investiga X e Y"), evalúa si es mejor una sola llamada con ambos en el user message, o dos llamadas secuenciales con síntesis al final. Para temas que comparten contexto: una sola llamada. Para temas independientes: dos llamadas.
