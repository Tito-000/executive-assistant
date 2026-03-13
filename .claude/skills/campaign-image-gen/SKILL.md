# Skill: campaign-image-gen

Genera anuncios estáticos de suplementos/productos para Meta Ads usando los 3 formatos ganadores validados con Magistral.

## Cuándo usar este skill

Cuando Martin diga:
- "Genera anuncios para [producto]"
- "Crea los ads de [producto]"
- "Hazme las imágenes para [producto]"
- "Usa el skill de imágenes"

## Inputs requeridos

Antes de correr el skill, recopilar:

1. **nombre_producto** — Nombre del producto (ej: "Magistral", "Immunocal")
2. **foto_producto** — Ruta local a la foto del producto (buscar en `~/Desktop/Immuno Consultor/Productos Fotos/`)
3. **headline_1** — Línea principal (ej: "POTENCIA TU ENERGÍA")
4. **headline_2** — Segunda línea (ej: "RECUPERA TU CONFIANZA")
5. **beneficios** — Lista de 3-5 beneficios cortos (ej: ["Apoya la próstata", "Reduce inflamación"])
6. **oferta** — Texto del banner promo (ej: "PAGUE 2 Y LLEVE 3" o dejar vacío)
7. **color_fondo** — "teal" | "negro" | "verde" | "crema" (default: generar los 3 ganadores)

Si falta algún input, preguntar antes de continuar.

## Formatos ganadores (siempre generar estos 3)

### Formato A — "Atención Hombres" (fondo negro)
- Fondo negro sólido
- Titular grande izquierda (2 líneas mayúsculas)
- Subtítulo + botón CTA azul "CONÓCELO"
- Producto real derecha con glow azul
- Banner inferior azul claro con plan/categoría

### Formato B — "Essenz Verde" (fondo verde)
- Fondo verde medio
- Etiqueta amarilla arriba: "1 [período] de [producto]"
- Subtítulo: "[beneficio principal logrado]"
- Producto real al centro con glow blanco
- 4 badges circulares alrededor (beneficios)
- Banner inferior redondeado con oferta

### Formato C — "Limpio Badges" (fondo crema)
- Fondo crema/blanco roto
- Headline verde centrado arriba
- Producto real izquierda full height
- 5 badges teal apilados a la derecha (beneficios)
- Footer con marca + ingredientes clave

## Proceso de ejecución

1. Confirmar inputs con Martin
2. Ejecutar `python3 "/Users/martinmercedes/Desktop/Executive assistant/ejecutar_skill_ads.py"` con los parámetros
3. Las imágenes se guardan en `~/Desktop/Executive assistant/anuncios_[nombre_producto]/`
4. Registrar gasto en `gastos_ia.xlsx` si se usó Imagen 4
5. Preguntar si subir a Canva para edición final

## Archivos del skill

- `ejecutar_skill_ads.py` — Motor principal de generación
- `formatos/formato_a.py` — Template fondo negro
- `formatos/formato_b.py` — Template verde essenz
- `formatos/formato_c.py` — Template limpio badges

## Costo estimado

- Solo Pillow (sin IA): $0.00
- Con Imagen 4 fondos: ~$0.12 USD (3 imágenes × $0.04)
- Todo con Imagen 4: ~$0.48 USD (12 variantes)

## Notas

- Siempre usar la foto real del producto (no dejar que Imagen 4 la genere)
- El glow del producto se ajusta según el fondo: cyan para teal/negro, blanco para verde/crema
- Si la foto tiene fondo blanco, usar threshold=205 para remoción
- Los textos siempre en español dominicano (tú, no usted)
