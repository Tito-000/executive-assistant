# Skill: campaign-image-gen

Genera anuncios estáticos de suplementos/productos para Meta Ads usando los 3 formatos ganadores. Antes de generar, investiga los documentos del producto para aplicar las mejores técnicas de copy, ángulos de mensaje y ganchos emocionales.

## Cuándo usar este skill

Cuando Martin diga:
- "Genera anuncios para [producto]"
- "Crea los ads de [producto]"
- "Hazme las imágenes para [producto]"
- "Usa el skill de imágenes"
- "campaign-image-gen"

---

## Paso 1 — Preguntar el producto

Cuando se active el skill, preguntar:

> "¿Para cuál producto genero los anuncios?"
> - Immunocal
> - Magistral
> - Platinum
> - Multy-Resveratrol

La carpeta raíz del producto es:
`projects/immunotec/fase-1-embudos-por-producto/productos/[nombre-producto]/`

---

## Paso 2 — Investigar los documentos del producto

Antes de generar nada, leer TODOS los archivos disponibles en estas carpetas del producto:

1. `WWP/` — Winning Writing Process: estructura del mensaje, gancho, historia, oferta, CTA
2. `Market Reaserch/` — investigación de mercado: dolores, deseos, objeciones, lenguaje del avatar
3. `Top player analisis/` — análisis de top players: qué están haciendo los mejores, formatos ganadores, ángulos de ataque

**Si alguna carpeta está vacía, continuar con las que tengan contenido.**

### Síntesis obligatoria antes de generar

Después de leer los documentos, hacer un análisis interno y extraer:

- **Gancho principal** — la idea más poderosa para captar atención en 1-2 segundos
- **Ángulo de mensaje** — el eje emocional o racional que más resuena con el avatar
- **Beneficios top 3-5** — los que aparecen con más fuerza en los documentos
- **Headline 1 y Headline 2** — derivados del WWP y del lenguaje del mercado
- **CTA** — el llamado a la acción más alineado con la etapa del funnel
- **Oferta / promesa** — si hay una oferta activa o promesa de transformación clara

Todo el copy de la imagen debe salir de esta síntesis — no inventar nada que no esté respaldado por los documentos.

---

## Paso 3 — Obtener la imagen del producto

Buscar automáticamente la foto del producto en:
`projects/immunotec/fase-1-embudos-por-producto/productos/[nombre-producto]/recursos/Imagenes de producto/`

Si hay varias imágenes, usar la de mayor resolución o preguntar a Martin cuál prefiere.

---

## Paso 4 — Generar los 3 formatos ganadores

### Formato A — "Atención Directa" (fondo negro)
- Fondo negro sólido
- Titular grande izquierda (2 líneas mayúsculas) — derivado del gancho principal
- Subtítulo + botón CTA azul
- Producto real derecha con glow azul
- Banner inferior azul claro con plan/categoría

### Formato B — "Resultado Transformación" (fondo verde)
- Fondo verde medio
- Etiqueta amarilla arriba: "1 [período] de [producto]"
- Subtítulo: "[beneficio principal logrado]" — del Market Research
- Producto real al centro con glow blanco
- 4 badges circulares alrededor (beneficios top del análisis)
- Banner inferior redondeado con oferta o promesa

### Formato C — "Limpio Beneficios" (fondo crema)
- Fondo crema/blanco roto
- Headline verde centrado arriba — del ángulo de mensaje
- Producto real izquierda full height
- 5 badges teal apilados a la derecha (beneficios del producto)
- Footer con marca + ingredientes clave

---

## Paso 5 — Generar el copy completo para Meta Ads

Para cada formato de imagen generado, crear el copy completo del anuncio aplicando técnicas de los mejores copywriters del mundo (David Ogilvy, Gary Halbert, Eugene Schwartz, Alex Hormozi, entre otros).

### Estructura del copy por anuncio

**Primaria (texto principal del ad):**
- Hook de apertura — primera línea que detiene el scroll (máx. 1-2 líneas, basado en el dolor o deseo más fuerte del avatar)
- Desarrollo — agitar el problema o amplificar el deseo, usar el lenguaje exacto del Market Research
- Credibilidad / prueba — ingrediente, mecanismo único, o resultado específico del producto
- CTA — llamado a la acción claro y directo

**Titular (headline del ad):**
- Versión corta y poderosa del gancho principal
- Máx. 40 caracteres si es posible
- Derivado del análisis de top players y el WWP

**Descripción (link description):**
- 1 línea que refuerza el beneficio principal o la oferta

### Técnicas a aplicar (según lo que dicten los documentos)

- **Interrupción de patrón** — abrir con algo inesperado o contraintuitivo
- **Especificidad** — números concretos son más creíbles que generalidades ("en 21 días" > "en poco tiempo")
- **Lenguaje del avatar** — usar las palabras exactas que el mercado usa para describir su problema
- **Future pacing** — llevar al lector a imaginar su vida con el resultado
- **Mecanismo único** — explicar POR QUÉ este producto funciona diferente
- **Urgencia / escasez** — si aplica y es verdad

### Output del copy

Guardar un archivo `copy-ads-[producto]-[fecha].md` en `Creativos nuevos para test/` con el copy de los 3 formatos. Formato del archivo:

```
# Copy Meta Ads — [Producto] — [Fecha]

## Formato A — Atención Directa
**Titular:** ...
**Texto principal:**
...
**Descripción:**
...

## Formato B — Resultado Transformación
**Titular:** ...
**Texto principal:**
...
**Descripción:**
...

## Formato C — Limpio Beneficios
**Titular:** ...
**Texto principal:**
...
**Descripción:**
...
```

---

## Paso 6 — Guardar todo en la carpeta del producto

Imágenes + archivo de copy se guardan juntos en:
`projects/immunotec/fase-1-embudos-por-producto/productos/[nombre-producto]/Creativos nuevos para test/`

Crear la carpeta si no existe.

---

## Proceso de ejecución técnica

1. Preguntar producto (Paso 1)
2. Leer documentos del producto (Paso 2) — obligatorio antes de continuar
3. Presentar síntesis a Martin para validación (opcional si hay prisa, preguntar)
4. Obtener imagen del producto (Paso 3)
5. Ejecutar el generador de imágenes con Gemini:
   ```bash
   source ~/.zshenv && python3 "/Users/martinmercedes/Desktop/Executive assistant 2/.claude/skills/campaign-image-gen/generar_imagenes_gemini.py" \
     --producto [nombre-producto] \
     --output "[ruta/Creativos nuevos para test]" \
     --datos '{"nombre":"[Nombre]","beneficios":["ben1","ben2","ben3","ben4","ben5"],"mecanismo":"[mecanismo único]","oferta":"[oferta activa]"}'
   ```
6. Generar el copy completo para los 3 formatos (Paso 5)
7. Guardar imágenes + archivo `copy-ads-[producto]-[fecha].md` en `Creativos nuevos para test/` (Paso 6)
8. Mostrar todas las imágenes generadas a Martin una por una
9. Preguntar: "¿Cuáles te quedas y cuáles descartamos?" — esperar respuesta
10. Eliminar las descartadas de la carpeta
11. Subir las aprobadas a Canva usando el MCP de Canva (`mcp__claude_ai_Canva__upload-asset-from-url` o importar desde path local) para edición final
12. Registrar gasto en `gastos_ia.xlsx` si se usó Imagen 4

---

## Costo estimado

- Solo Pillow (sin IA): $0.00
- Con Imagen 4 Ultra fondos: ~$0.18 USD (3 imágenes)
- Todo con Imagen 4 Ultra: ~$0.72 USD (12 variantes)

---

## Notas

- Siempre usar la foto real del producto — nunca dejar que la IA la genere
- El glow del producto se ajusta según el fondo: cyan para teal/negro, blanco para verde/crema
- Si la foto tiene fondo blanco, usar threshold=205 para remoción
- Textos siempre en español dominicano (tú, no usted)
- Si los documentos de investigación están vacíos o incompletos, notificar a Martin antes de continuar
