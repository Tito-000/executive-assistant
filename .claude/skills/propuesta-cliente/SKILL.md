---
name: propuesta-cliente
description: Genera una propuesta de marketing digital premium para un cliente, basada en la información recogida en la reunión de discovery. Hace preguntas SPIN, elige el estilo visual, y genera la propuesta en HTML con imágenes de apoyo.
disable-model-invocation: true
---

# Skill: /propuesta-cliente

Crea una propuesta visual profesional para presentar a un cliente después de la reunión de discovery.

---

## PASO 0 — Elegir la plantilla de marca

**Antes de cualquier pregunta sobre el cliente**, preguntar:

---

**¿Qué plantilla de marca usamos para esta propuesta?**

| # | Plantilla | Cuándo usarla |
|---|-----------|---------------|
| 1 | **Flexo Media** ⭐ | Propuestas de Flexo Media — verde/dorado, premium |
| 2 | **Brand del cliente** | El cliente tiene sus propios colores — tú los indicas |

Las imágenes de apoyo se generan siempre con `excalidraw-visuals` usando la plantilla elegida.

Esperar respuesta antes de continuar.

---

## PASO 1 — Recopilar información del cliente

Hacer las siguientes preguntas en un solo bloque. No generar nada hasta tener las respuestas.

---

**Ahora cuéntame sobre el cliente y la reunión:**

### 🏢 El cliente
1. ¿Cómo se llama la empresa y a qué se dedican?
2. ¿Cuál es su producto o servicio más rentable?
3. ¿Cómo consiguen clientes hoy? (referidos, ads, nada, etc.)
4. ¿Cuántos clientes nuevos consiguen al mes aproximadamente?
5. ¿Cuánto ganan por cliente? (comisión, ticket promedio, etc.)

### 🎯 Sus problemas y metas (SPIN)
6. ¿Cuál es su mayor problema de marketing hoy? *(Problem)*
7. ¿Cuántos clientes nuevos quieren conseguir al mes? *(Need)*
8. ¿Qué pasa si no lo resuelven — qué dijeron en la llamada? *(Implication)*
9. ¿Qué valor específico tendría para ellos resolver esto? *(Payoff)*

### 💡 La solución que vas a proponer
10. ¿Qué paquete(s) vas a ofrecer? (describir brevemente)
11. ¿Cuáles son los precios? (fee de gestión — pauta siempre aparte)
12. ¿Hay algún combo u oferta especial?

### 📊 Los números (project math)
13. ¿Tienes datos de forecast o proyección? (leads esperados, CPA, etc.)
14. ¿Cuál es la tasa de cierre que vas a usar para el cálculo?
15. ¿Cuál es la comisión o ingreso estimado por cliente nuevo?

---

Esperar todas las respuestas antes de continuar.

---

## PASO 2 — Confirmar la estructura

Con las respuestas, proponer la estructura de la propuesta adaptada al cliente:

```
1. Portada — nombre cliente + Flexo Media + fecha
2. Diagnóstico — situación actual + oportunidad de mercado
3. El problema — lo que dijeron en la llamada (sus palabras)
4. La solución — paquete(s) propuesto(s) con detalle
5. Project Math — leads → conversiones → ingresos estimados
6. Inversión — precios claros (fee separado de pauta siempre)
7. Por qué Flexo Media — diferenciadores
8. Próximos pasos / CTA — two-way close
```

Preguntar: **¿Quieres agregar, quitar o cambiar alguna sección?**

Esperar confirmación antes de generar.

---

## PASO 3 — Generar imágenes de apoyo (si aplica)

### Si el estilo es Excalidraw:
Para cada sección que necesite imagen, construir el prompt siguiendo el workflow completo de `excalidraw-visuals`:
- Elegir template de layout
- Minimizar texto (max 30 palabras por imagen)
- Especificar colores por significado
- Ejecutar: `node scripts/excalidraw-visuals/generate-visual.js "<PROMPT>" "outputs/propuestas/[cliente]/[seccion].png" "16:9" --input "brand-assets/excalidraw-style-reference.png"`

### Si el estilo es Nano Banana:
Construir prompts JSON siguiendo el workflow de `nano-banana-images` y ejecutar con `generate_kie.py`.

### Si el estilo es Flexo Media o Personalizado:
Saltar este paso — todo el diseño va en HTML/CSS.

---

## PASO 4 — Generar la propuesta en HTML

### Estilo Flexo Media ⭐
- Colores: `--green: #2d4a3e`, `--gold: #b5943a`
- Tipografía: Cormorant Garamond (títulos) + DM Sans (cuerpo)
- Logo Flexo Media: incrustar base64 desde `/Users/martinmercedes/Desktop/knsak.png` con `mix-blend-mode: screen`
- Animaciones: IntersectionObserver scroll reveal
- Secciones alternadas dark/light/deep
- 100% responsivo

### Estilo Personalizado
- Usar los colores y fuentes que Martin indicó en el Paso 0
- Misma estructura HTML base

### Reglas de contenido (todos los estilos)
- Español siempre
- Tono: directo, ejecutivo, sin relleno
- Los números del project math deben cuadrar matemáticamente
- **La pauta SIEMPRE separada del fee** — visualmente con recuadro distinto y texto "va directo a [plataforma]"
- Sección "¿Qué pasa si no hacen nada?" basada en lo que dijeron en la llamada
- Two-way close al final: columna Sí vs columna No

### Reglas de precios
- Fee de gestión: número grande y prominente
- Pauta: recuadro punteado separado con etiqueta "aparte · va directo a [Google/Meta]"
- Si hay combo: mostrar ahorro en badge dorado
- Nunca sumar fee + pauta en un solo precio sin desglose

### Archivo de salida
```
outputs/propuestas/[nombre-cliente-kebab]-propuesta-marketing.html
```

---

## PASO 5 — Subir a Netlify (si Martin lo pide)

```bash
mkdir -p /tmp/[cliente]-deploy
cp outputs/propuestas/[cliente]-propuesta-marketing.html /tmp/[cliente]-deploy/index.html
npx netlify-cli deploy --dir /tmp/[cliente]-deploy --prod --create-site
```

Mostrar el link público al terminar.

---

## Reglas generales del skill

- Español siempre
- PASO 0 primero — elegir estilo visual antes de cualquier pregunta
- No generar nada antes de tener las respuestas del Paso 1
- La pauta SIEMPRE va separada del fee en todas partes
- Los números del project math deben cuadrar (leads × tasa cierre = clientes; clientes × ticket = ingresos)
- Si Martin no da un dato clave, preguntar antes de inventar
- Esperar confirmación de estructura antes de generar el HTML
- Si las imágenes de Excalidraw o Nano Banana fallan, reportar el error exacto y continuar con el HTML sin ellas
