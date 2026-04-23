# Pagos — MM Agency

Esta carpeta contiene todos los productos de **suscripción recurrente** de MM Agency, con sus landings de pago branded y los datos de PayPal para cobrar a clientes.

Cada producto tiene:
- `landing/` — página HTML de pago branded con botón PayPal embebido
- `README.md` — datos del plan (ID, precio, link directo, deployment)
- `clientes-activos.md` — lista de clientes pagando ese servicio

---

## Servicios activos

| Servicio | Precio | Frecuencia | Plan ID PayPal | Landing |
|---|---|---|---|---|
| [CRM GoHighLevel](crm-ghl/) | US$97/mes | Mensual | `P-1T213860GK3052355NHTE67Y` | `crm-ghl/landing/` |

---

## Cómo usar esto con un nuevo cliente

1. Entra a la carpeta del servicio (ej: `crm-ghl/`)
2. Abre el `README.md` del servicio — ahí está el link público
3. Mándaselo al cliente por WhatsApp
4. Cuando autorice el pago, anótalo en `clientes-activos.md`

---

## Cuenta PayPal

- **Cuenta Business:** MMagency
- **Email principal:** martinmercedes100@gmail.com
- **Dashboard planes:** https://www.paypal.com/billing/plans
- **Dashboard suscripciones activas:** https://www.paypal.com/billing/subscriptions

---

## Crear un nuevo servicio de suscripción

Ver [../../pagos/guia-crear-servicio.md](guia-crear-servicio.md)
