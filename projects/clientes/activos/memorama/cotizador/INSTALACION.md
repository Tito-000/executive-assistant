# Instalación del Cotizador en Shopify (Memorama)

## Qué es

Un **snippet de Liquid** que se renderiza DENTRO de cada product page existente.
No es una página nueva. No es un wizard. Vive abajo (o al lado) del producto en URLs como `/products/camisa-tipo-columbia-mujer`.

## Ver la demo primero

Abrir `demo/index.html` en el navegador. Ahí verás cómo se ve el cotizador **embebido** en una product page simulada de Memorama.

```bash
open projects/clientes/activos/memorama/cotizador/demo/index.html
```

## Archivos a subir a Shopify

| Archivo local | Dónde va en Shopify |
|---|---|
| `shopify/cotizador-bordado.liquid` | `snippets/cotizador-bordado.liquid` |
| `shopify/cotizador-bordado.css` | `assets/cotizador-bordado.css` |
| `shopify/cotizador-bordado.js` | `assets/cotizador-bordado.js` |

## Paso a paso (Shopify Admin)

1. **Entrar al editor de código del tema**
   - Admin → Online Store → Themes → (tema Trade activo) → `...` → Edit code

2. **Crear los 3 archivos**
   - `Snippets` → Add a new snippet → nombre: `cotizador-bordado` → pegar contenido de `cotizador-bordado.liquid`
   - `Assets` → Add a new asset → subir `cotizador-bordado.css`
   - `Assets` → Add a new asset → subir `cotizador-bordado.js`

3. **Insertar el render en el template de producto**
   - Abrir `sections/main-product.liquid` (tema Trade)
   - Pegar esta línea donde quieras que aparezca el cotizador (recomendado: después del bloque de descripción o al final de la info del producto):
   ```liquid
   {% render 'cotizador-bordado', product: product %}
   ```
   - Save

4. **(Opcional) Activar solo en productos personalizables**
   - En el admin, a cada producto personalizable agregar un tag: `personalizable`
   - En lugar del render simple, usar:
   ```liquid
   {% if product.tags contains 'personalizable' %}
     {% render 'cotizador-bordado', product: product %}
   {% endif %}
   ```

5. **(Opcional) Precio base por producto via metafield**
   - Settings → Custom data → Products → Add definition
     - Namespace: `memorama`
     - Key: `base_price`
     - Type: Number (integer)
   - En cada producto, llenar el metafield con el precio base en RD$
   - Si no se llena, el cotizador usa 450 RD$ por defecto (editable en el `.liquid`)

## Verificar

1. Visitar cualquier product page (ej. `/products/camisa-tipo-columbia-mujer`)
2. Scrollear — debe aparecer el bloque "Personaliza tu pedido"
3. Subir un logo → ver preview sobre la imagen del producto
4. Elegir técnica + posición + cantidad → precio live
5. Click en "Solicitar cotización" → por ahora solo hace `console.log` + alert (Fase 2 = Draft Order API)

## Personalizar precios (pricing engine)

Editar dentro de `cotizador-bordado.liquid` el bloque `const PRICING = {...}`:
- `techniques`: costo por técnica
- `positions`: costo por posición
- `volumeDiscounts`: tiers de descuento por cantidad

Cuando el cliente entregue su tabla real, solo actualizar esos valores.

## Fase 2 (pendiente)

- Conectar el CTA a la Admin API para crear Draft Order automáticamente
- Webhook → notificación a Memorama (email/WhatsApp vía GHL o Resend)
- Validación server-side del logo subido (tamaño, formato, DPI mínimo para bordado)
