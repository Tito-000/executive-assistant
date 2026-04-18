# Tabla de Precios — Memorama Cotizador

> Llenar con el cliente antes de arrancar Fase 2 (desarrollo).
> Todos los precios en RD$ salvo indicación contraria.

## 1. Precio base por producto (RD$ / unidad)

| Producto | Precio base | Notas |
|---|---|---|
| Poloshirt Dry Fit | — | |
| T-shirt algodón | — | |
| Hoodie con zipper | — | |
| Abrigo escolar sin capucha | — | |
| Gorra | — | |
| Tote bag polipropileno | — | |
| Bolso de yute | — | |
| ... | — | |

## 2. Costo adicional por técnica (RD$ / unidad)

| Técnica | Costo adicional | Mínimo de pedido |
|---|---|---|
| Bordado | — | — |
| Serigrafía | — | — |
| DTF (impresión directa) | — | — |
| Sublimación | — | — |

## 3. Costo adicional por posición (RD$ / unidad / posición)

| Posición | Costo adicional | Aplica a técnicas |
|---|---|---|
| Pecho izquierdo | — | |
| Pecho completo | — | |
| Espalda completa | — | |
| Manga izquierda | — | |
| Manga derecha | — | |
| Gorra frente | — | |
| Gorra lateral | — | |

## 4. Descuentos por volumen (% sobre total)

| Cantidad | Descuento |
|---|---|
| 1-9 | 0% |
| 10-24 | — |
| 25-49 | — |
| 50-99 | — |
| 100-249 | — |
| 250+ | — |

## 5. Reglas especiales

- ¿Aplican los descuentos solo al base o también a técnica + posición?
- ¿Hay productos con descuentos distintos?
- ¿Hay costos fijos (ej. digitalización de logo para bordado una sola vez)?
- ¿ITBIS incluido o se suma al final?

## Fórmula asumida (a validar con cliente)

```
Precio unitario = base + técnica + Σ(posiciones)
Subtotal = Precio unitario × cantidad
Total = Subtotal × (1 - descuento_volumen)
+ ITBIS si aplica
```
