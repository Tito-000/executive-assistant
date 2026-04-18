# Cotizador Custom — Memorama Bordados

Configurador tipo Vistaprint para memoramard.com: cálculo de precio en vivo + preview del logo + checkout híbrido (Draft Order).

**Estado:** Fase 0 — esperando inputs del cliente.
**Plan completo:** `~/.claude/plans/frolicking-soaring-dijkstra.md`

## Bloqueantes (lo que necesitamos del cliente)

- [ ] Tabla precio base por producto (RD$/unidad)
- [ ] Costo adicional por técnica (bordado, serigrafía, DTF, sublimación)
- [ ] Costo adicional por posición (pecho izq., pecho completo, espalda, manga)
- [ ] Tiers de descuento por volumen (1-9, 10-24, 25-49, 50-99, 100+)
- [ ] Mínimos de pedido por técnica
- [ ] Imágenes limpias de productos (PNG fondo transparente)
- [ ] Acceso Staff Collaborator a Shopify

## Fases

- [ ] **Fase 1 (sem 1)** — Discovery, tabla de precios, mockup HTML aprobatorio
- [ ] **Fase 2 (sem 2-3)** — Desarrollo wizard + pricing engine + Fabric.js preview + Draft Order API
- [ ] **Fase 3 (sem 4)** — Integraciones (GHL/WhatsApp/Resend), QA mobile+desktop, training

## Archivos del proyecto

- `pricing-table.md` — tabla de precios del cliente (a llenar)
- `spec.md` — spec técnica final (post Fase 1)
- `mockup.html` — mockup visual del wizard para aprobación
- `mensaje-cliente.md` — mensaje para pedir inputs al cliente

## Links

- Sitio: https://memoramard.com/
- Producto referencia: https://memoramard.com/products/poloshirt-dry-fit
- Top player referencia: https://www.vistaprint.com/clothing-bags/t-shirts/gildan-r-budget-unisex-t-shirt
- Propuesta comercial: [outputs/propuestas/memorama-bordado/](../../../../outputs/propuestas/memorama-bordado/)
