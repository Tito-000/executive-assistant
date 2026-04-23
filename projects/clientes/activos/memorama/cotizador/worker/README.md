# Memorama Cotizador Worker

Cloudflare Worker que recibe cotizaciones del cotizador de bordado en Shopify y crea Draft Orders automáticamente via Shopify Admin API.

## Setup inicial (una sola vez)

```bash
cd projects/clientes/activos/memorama/cotizador/worker
npm install

# Login en Cloudflare
npx wrangler login

# Crear namespace KV para guardar el token
npx wrangler kv:namespace create TOKENS
# Copiar el id que devuelve y pegarlo en wrangler.toml en REPLACE_WITH_KV_ID

# Guardar el Client Secret como secret
npx wrangler secret put SHOPIFY_CLIENT_SECRET
# Pegar el Client Secret de la app (ver recursos-ia/api-keys/shopify-memorama-app.md)

# Desplegar
npx wrangler deploy
```

## Después del primer deploy

1. Toma la URL del Worker (ej. `https://memorama-cotizador.<tu-subdominio>.workers.dev`)
2. En Shopify Dev Dashboard → app "Cotizador Draft Orders" → Configuration:
   - **App URL:** `https://memorama-cotizador.<tu-subdominio>.workers.dev/install`
   - **Allowed redirection URL:** `https://memorama-cotizador.<tu-subdominio>.workers.dev/auth/callback`
3. Release la nueva versión
4. Visita `https://memorama-cotizador.<tu-subdominio>.workers.dev/install` → te manda a Shopify para instalar
5. Acepta la instalación → callback guarda token en KV → app lista

## Endpoints

- `GET /health` — status del worker y si está instalado
- `GET /install` — inicia OAuth install
- `GET /auth/callback` — recibe el callback de Shopify post-install
- `POST /cotizacion` — recibe cotización del cotizador, crea Draft Order

## Payload esperado en POST /cotizacion

```json
{
  "contact": {
    "name": "Juan Pérez",
    "email": "juan@ejemplo.com",
    "phone": "+18095551234",
    "company": "ACME",
    "comments": "Necesito 50 uniformes"
  },
  "config": {
    "productName": "Polo bordado",
    "color": "Azul",
    "sizes": {"S": 10, "M": 20, "L": 20},
    "positions": ["left_chest", "center_back"],
    "stitches": 8000,
    "quantity": 50,
    "deadline": "2026-05-15"
  },
  "totals": {
    "unitPrice": 450,
    "total": 22500
  },
  "logoUrl": "https://cdn.shopify.com/..."
}
```
