# Propuesta — Cotizador Custom estilo Vistaprint

**Cliente:** Memorama Bordado (memoramard.com)
**Proyecto:** Add-on al contrato actual — Configurador de personalización con precio en vivo
**Fecha:** 2026-04-14

---

## Problema que resuelve

Hoy tu Shopify recibe solicitudes de bordado por WhatsApp/formulario. Cada cotización la haces manual: el cliente escribe, tú respondes, él aprueba, tú cobras, él manda el logo. Este ida-y-vuelta:

- Te consume tiempo diario.
- Pierdes clientes en el camino (los que no responden el WhatsApp nunca compran).
- Tu marca se siente "artesanal", no nivel top player.

Vistaprint y los top players del sector resuelven esto con un **configurador en vivo**: el cliente elige todo, sube su logo, ve el precio al instante y compra solo.

## Qué vamos a construir

Un configurador/cotizador **dentro de tu misma Shopify** (no un sitio aparte, no una app externa), con este flujo:

1. **Elige producto** — polo, hoodie, gorra, tote, etc.
2. **Elige técnica** — bordado, serigrafía, DTF, sublimación
3. **Sube su logo + elige posición(es)** — pecho, espalda, manga (con preview sobre la prenda)
4. **Elige talla, color, cantidad** — precio se recalcula live con el descuento por volumen
5. **Envía solicitud** — te llega a tu admin de Shopify con logo adjunto + todas las specs
6. **Tú validas el logo y envías link de pago** — checkout normal de Shopify

**Estética:** top player (referencia: Vistaprint, Custom Ink, 4imprint).

## Beneficios concretos

- **Menos tiempo cotizando manual.** De 10-15 min por cotización → 0.
- **Más conversión.** La gente compra por impulso cuando ve precio al instante.
- **Experiencia de marca premium.** Memorama se siente "grande".
- **Cero cambio en tu operación.** Los pedidos siguen llegando a tu admin de Shopify como siempre.
- **Sin renta mensual de apps.** Todo custom, propiedad tuya.

## Alcance del proyecto

### Incluye
- Página dedicada `/personaliza` dentro de tu tema Shopify
- Wizard de 6 pasos con diseño custom estilo Vistaprint (desktop + mobile)
- Pricing engine en tiempo real con tu tabla de precios (base + técnica + posición + descuentos por volumen)
- Subida de logo con validación de formato
- Preview del logo sobre la prenda (canvas interactivo)
- Creación automática de Draft Order en Shopify con toda la info del pedido
- Notificación automática a ti (email + WhatsApp via GHL) cuando llega nueva solicitud
- Email transaccional al cliente confirmando que recibimos su solicitud
- Training para ti y tu equipo: cómo validar logos, enviar invoice, despachar

### NO incluye
- Pasarela de pago nueva (usamos la que ya tienes en Shopify)
- Nuevas fotos de producto (si las que tienes no sirven para preview, se producen aparte)
- Mantenimiento posterior (eso va en el retainer mensual si lo contratas)
- Traducción a inglés (es solo español en esta versión)

## Timeline

| Semana | Entregable |
|---|---|
| 1 | Tabla de precios finalizada + mockup HTML aprobatorio del flujo completo |
| 2 | Wizard funcional (pasos 1-4) + pricing engine con tu tabla |
| 3 | Preview del logo + subida de archivo + integración Draft Order |
| 4 | Integraciones (notificaciones), QA mobile+desktop, training, lanzamiento |

**Total: 4 semanas desde que entregues tabla de precios + accesos.**

## Bloqueantes (lo que necesito de ti para arrancar)

1. **Tabla de precios completa** (plantilla adjunta — `pricing-table.md`)
2. **Acceso Staff Collaborator** al Shopify
3. **Fotos limpias de productos** (PNG fondo transparente idealmente)

## Inversión

**[TBD — Martin: definir según MM Agency pricing + complejidad]**

Rango estimado a validar:
- **Opción setup único:** US$ 1,200 - 1,800
- **Opción setup + optimización mensual:** US$ 1,000 setup + US$ 200/mes (ajustes, nuevos productos, cambios de pricing)

Ad spend y costos de Shopify corren por tu cuenta (no hay rentas nuevas).

## Forma de pago sugerida
- 50% al inicio (semana 0)
- 50% al entregar (semana 4, con el sistema vivo en producción)

## Garantía
Si al final de la semana 4 el sistema no está vivo y funcionando por causas imputables a mí, extiendo sin costo hasta dejarlo operativo.

---

## Próximos pasos

1. Revisa esta propuesta
2. Llena la tabla de precios (plantilla adjunta)
3. Dame acceso Staff Collaborator al Shopify
4. Firmamos, pagas 50% y arrancamos

---

**Martin Mercedes** — MM Agency
