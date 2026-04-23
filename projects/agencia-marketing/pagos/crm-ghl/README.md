# Servicio CRM GoHighLevel — Datos del plan

Producto de suscripción recurrente para cualquier cliente que contrate el servicio de CRM con MM Agency.

---

## Datos del plan (PayPal)

| Campo | Valor |
|---|---|
| **Nombre producto** | Mensualidad CRM GoHighLevel |
| **ID producto** | MMA-CRM-GHL-001 |
| **Plan ID** | `P-1T213860GK3052355NHTE67Y` |
| **Precio** | US$97.00 USD |
| **Frecuencia** | Cada 1 mes |
| **Ciclos** | Ilimitado |
| **Cancelable** | Sí, en cualquier momento |
| **Trial** | Ninguno |
| **Reintento pagos fallidos** | Activado (pausa tras 1 fallo) |

---

## Links de pago

### Link directo PayPal (fallback rápido)
```
https://www.paypal.com/webapps/billing/plans/subscribe?plan_id=P-1T213860GK3052355NHTE67Y
```

### Landing branded MM Agency ⭐ (usar este por defecto)
```
https://mm-agency-pagos.pages.dev
```

Hospedada en Cloudflare Pages — proyecto `mm-agency-pagos`. Para redeploy:
```bash
cd projects/agencia-marketing/pagos/crm-ghl/landing
npx wrangler pages deploy . --project-name=mm-agency-pagos --branch=main --commit-dirty=true
```

### Código embebible (botón PayPal para otras páginas)

```html
<div id="paypal-button-container-P-1T213860GK3052355NHTE67Y"></div>
<script src="https://www.paypal.com/sdk/js?client-id=AfzIwijgmMoUVP-pkEDVIfftPH1oUcaW30dQJ_C35v_-CZrW789QP1ZRG34WcvtcGRjOrekxxgXy3X_I&vault=true&intent=subscription" data-sdk-integration-source="button-factory"></script>
<script>
  paypal.Buttons({
      style: { shape: 'pill', color: 'black', layout: 'vertical', label: 'subscribe' },
      createSubscription: function(data, actions) {
        return actions.subscription.create({ plan_id: 'P-1T213860GK3052355NHTE67Y' });
      },
      onApprove: function(data, actions) {
        window.location.href = 'gracias.html?sub=' + data.subscriptionID;
      }
  }).render('#paypal-button-container-P-1T213860GK3052355NHTE67Y');
</script>
```

---

## Qué incluye el servicio

Lo que el cliente recibe a cambio de su US$97/mes:

1. **Acceso a la plataforma GoHighLevel** — CRM completo: agenda, contactos, leads, pipeline, seguimiento automatizado
2. **Configuración y mantenimiento** — cuenta configurada a medida + updates mensuales
3. **Soporte técnico directo** — WhatsApp para dudas y ajustes
4. **Capacitación en video** — biblioteca de tutoriales paso a paso
5. **Integración lista** — Meta Ads, Google Ads y formularios se conectan directo al CRM

---

## Mensaje de WhatsApp para enviar al cliente

```
Hola [Nombre],

Te dejo el link para activar el pago mensual de tu CRM. Solo tienes que
autorizar una vez, después se descuenta automático cada mes. Cancelable
en cualquier momento.

Mensualidad CRM GoHighLevel — US$97/mes

[PEGAR LINK DE LA LANDING BRANDED]

Cualquier duda me avisas.
```

---

## Proceso de cobro

1. Cliente entra al link branded
2. Ve la landing con el detalle + botón PayPal
3. Click en "Subscribe with PayPal"
4. Autoriza con su cuenta PayPal o tarjeta
5. Redirección automática a `gracias.html` con el ID de suscripción
6. Primer cobro se procesa al momento
7. Siguientes cobros automáticos cada mes el mismo día

---

## Gestión de suscripciones activas

- **Ver todas las subs activas:** https://www.paypal.com/billing/subscriptions
- **Cancelar una sub:** desde el dashboard → click en la suscripción → Cancelar
- **Ver pagos procesados:** Movimientos de PayPal filtrado por "Suscripción"
- **Clientes activos del servicio:** [clientes-activos.md](clientes-activos.md)

---

## Imagen del producto

`outputs/paypal-products/crm-ghl-mensualidad-600.png` (600x600, fondo negro, logo MM Agency)
