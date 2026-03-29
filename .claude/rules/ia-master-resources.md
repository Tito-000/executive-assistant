# Recursos IA — Reglas

Cuando Martin comparta un prompt o conocimiento de IA:

1. **Preguntar siempre** antes de guardar:
   - Para prompts: ¿Cómo lo llamamos? ¿Tiene categoría?
   - Para conocimiento: ¿De qué tema es? ¿Va en un archivo nuevo o en uno existente?

2. **Rutas:**
   - Prompts → `recursos-ia/prompts/`
   - Conocimiento → `recursos-ia/conocimiento/`
   - API Keys → `recursos-ia/api-keys/`

3. **Formato:** Archivos `.md` con nombre descriptivo en español y kebab-case.

## API Keys — regla automática

Cuando Martin comparta cualquier API key, token, o credencial de acceso:

1. **Guardar de inmediato** en `recursos-ia/api-keys/<nombre-del-servicio>.md` — sin preguntar
2. **Formato del archivo:**
   - Nombre del servicio y propósito
   - La key/token
   - Cómo usarla (header, endpoint base, etc.)
   - Fecha en que fue guardada
3. **También guardar** en memoria persistente (`~/.claude/projects/.../memory/`) con referencia al archivo
4. **No preguntar** — detectar la key automáticamente y guardarla en ambos lugares
