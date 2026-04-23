/**
 * Memorama Cotizador Worker
 *
 * Routes:
 *   GET  /install              - Redirects to Shopify OAuth install
 *   GET  /auth/callback        - Shopify redirects here after install, saves token in KV
 *   POST /cotizacion           - Cotizador posts quote JSON; creates Draft Order in Shopify
 *   GET  /health               - Health check
 *
 * Secrets (set via `wrangler secret put`):
 *   SHOPIFY_CLIENT_SECRET
 *
 * KV bindings:
 *   TOKENS - stores offline access token under key "access_token"
 */

const ALLOWED_ORIGINS = [
  'https://memoramard.com',
  'https://www.memoramard.com',
  'https://memorama-2.myshopify.com',
];

function corsHeaders(origin) {
  const allow = ALLOWED_ORIGINS.includes(origin) ? origin : ALLOWED_ORIGINS[0];
  return {
    'Access-Control-Allow-Origin': allow,
    'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '86400',
  };
}

function json(data, status = 200, origin = '') {
  return new Response(JSON.stringify(data), {
    status,
    headers: {
      'Content-Type': 'application/json',
      ...corsHeaders(origin),
    },
  });
}

function html(body, status = 200) {
  return new Response(body, {
    status,
    headers: { 'Content-Type': 'text/html; charset=utf-8' },
  });
}

async function verifyHmac(params, secret) {
  const hmac = params.get('hmac');
  if (!hmac) return false;
  const message = [];
  for (const [k, v] of [...params.entries()].sort()) {
    if (k === 'hmac' || k === 'signature') continue;
    message.push(`${k}=${v}`);
  }
  const data = message.join('&');
  const key = await crypto.subtle.importKey(
    'raw',
    new TextEncoder().encode(secret),
    { name: 'HMAC', hash: 'SHA-256' },
    false,
    ['sign']
  );
  const sig = await crypto.subtle.sign('HMAC', key, new TextEncoder().encode(data));
  const hex = [...new Uint8Array(sig)]
    .map((b) => b.toString(16).padStart(2, '0'))
    .join('');
  return hex === hmac;
}

async function handleInstall(url, env) {
  const shopParam = url.searchParams.get('shop');
  let shop = shopParam || env.SHOPIFY_SHOP;
  if (!shop.endsWith('.myshopify.com')) {
    shop = `${shop}.myshopify.com`;
  }
  const redirectUri = `${url.origin}/auth/callback`;
  const nonce = crypto.randomUUID();
  const installUrl =
    `https://${shop}/admin/oauth/authorize` +
    `?client_id=${env.SHOPIFY_CLIENT_ID}` +
    `&scope=${encodeURIComponent(env.SHOPIFY_SCOPES)}` +
    `&redirect_uri=${encodeURIComponent(redirectUri)}` +
    `&state=${nonce}`;
  return Response.redirect(installUrl, 302);
}

async function handleCallback(url, env) {
  const params = url.searchParams;
  const shop = params.get('shop');
  const code = params.get('code');

  if (!shop || !code) {
    return html('<h1>Error</h1><p>Missing shop or code.</p>', 400);
  }

  const ok = await verifyHmac(params, env.SHOPIFY_CLIENT_SECRET);
  if (!ok) {
    return html('<h1>Error</h1><p>Invalid HMAC.</p>', 400);
  }

  const tokenRes = await fetch(`https://${shop}/admin/oauth/access_token`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      client_id: env.SHOPIFY_CLIENT_ID,
      client_secret: env.SHOPIFY_CLIENT_SECRET,
      code,
    }),
  });

  if (!tokenRes.ok) {
    const t = await tokenRes.text();
    return html(`<h1>Error</h1><pre>${t}</pre>`, 500);
  }

  const tokenData = await tokenRes.json();
  await env.TOKENS.put('access_token', tokenData.access_token);
  await env.TOKENS.put('shop', shop);

  return html(`
    <h1>✅ Instalación completa</h1>
    <p>La app ya está conectada a <code>${shop}</code>.</p>
    <p>Ya puedes usar el cotizador — las solicitudes se guardarán como Draft Orders en Shopify.</p>
  `);
}

function buildDraftOrderPayload(quote) {
  const data = quote || {};
  const contact = data.contact || {};
  const config = data.config || {};
  const totals = data.totals || {};

  const items = Array.isArray(data.items) && data.items.length
    ? data.items
    : [{
        title: config.productName || 'Cotización bordado',
        quantity: config.quantity || 1,
        price: totals.unitPrice || totals.total || 0,
      }];

  // NOTA: Shopify ignora el price override cuando mandas variant_id —
  // usa siempre el price del variant en la tienda. Como los variants
  // de Memorama están a $0 (cotización por encargo), tenemos que usar
  // custom items para que respete el precio del cotizador.
  const line_items = items.map((it) => {
    const qty = Number(it.quantity || 1);
    const price = String(it.price || 0);

    return {
      title: String(it.title || config.productName || 'Cotización bordado'),
      quantity: qty,
      price: price,
      requires_shipping: true,
      taxable: false,
    };
  });

  const lines = [];
  lines.push(`Producto: ${config.productName || '—'}`);
  if (config.color) lines.push(`Color: ${config.color}`);
  if (config.sizes) lines.push(`Tallas: ${JSON.stringify(config.sizes)}`);
  if (config.positions) {
    lines.push(`Posiciones: ${Array.isArray(config.positions) ? config.positions.join(', ') : config.positions}`);
  }
  if (config.stitches) lines.push(`Puntadas estimadas: ${config.stitches}`);
  if (config.deadline) lines.push(`Fecha deseada: ${config.deadline}`);
  if (contact.company) lines.push(`Empresa: ${contact.company}`);
  if (contact.comments) lines.push(`Comentarios: ${contact.comments}`);
  if (data.logoUrl) lines.push(`Logo: ${data.logoUrl}`);

  const note = lines.join('\n');

  const tags = ['cotizador', 'memorama-cotizador'];

  const payload = {
    draft_order: {
      line_items,
      note,
      tags: tags.join(', '),
      email: contact.email || undefined,
      use_customer_default_address: false,
    },
  };

  if (contact.name || contact.email || contact.phone) {
    payload.draft_order.customer = {
      first_name: (contact.name || '').split(' ')[0] || 'Cotización',
      last_name: (contact.name || '').split(' ').slice(1).join(' ') || '',
      email: contact.email || undefined,
      phone: contact.phone || undefined,
    };
  }

  return payload;
}

async function handleLogoUpload(request, env, origin) {
  const MAX_SIZE = 10 * 1024 * 1024; // 10MB
  const ALLOWED = ['image/png', 'image/jpeg', 'image/jpg', 'image/webp', 'image/svg+xml', 'application/pdf', 'image/vnd.adobe.photoshop', 'application/postscript', 'application/illustrator'];

  const contentType = request.headers.get('Content-Type') || '';
  if (!contentType.includes('multipart/form-data')) {
    return json({ error: 'expected_multipart' }, 400, origin);
  }

  let formData;
  try {
    formData = await request.formData();
  } catch (e) {
    return json({ error: 'invalid_form' }, 400, origin);
  }

  const file = formData.get('file');
  if (!file || typeof file.arrayBuffer !== 'function') {
    return json({ error: 'no_file' }, 400, origin);
  }

  if (file.size > MAX_SIZE) {
    return json({ error: 'file_too_large', max: MAX_SIZE }, 413, origin);
  }

  // Generate unique key
  const originalName = (file.name || 'logo').replace(/[^a-zA-Z0-9._-]/g, '_');
  const timestamp = Date.now();
  const rand = crypto.randomUUID().split('-')[0];
  const key = `${timestamp}-${rand}-${originalName}`;

  try {
    const buffer = await file.arrayBuffer();
    await env.LOGOS.put(key, buffer, {
      httpMetadata: {
        contentType: file.type || 'application/octet-stream',
      },
    });
  } catch (e) {
    return json({ error: 'upload_failed', details: String(e) }, 500, origin);
  }

  const publicUrl = `${env.LOGOS_PUBLIC_URL}/${key}`;
  return json({ ok: true, url: publicUrl, key }, 200, origin);
}

async function handleCotizacion(request, env, origin) {
  let body;
  try {
    body = await request.json();
  } catch (e) {
    return json({ error: 'invalid_json' }, 400, origin);
  }

  const token = await env.TOKENS.get('access_token');
  const shop = (await env.TOKENS.get('shop')) || env.SHOPIFY_SHOP;
  if (!token) {
    return json({ error: 'app_not_installed', install_url: '/install' }, 503, origin);
  }

  const payload = buildDraftOrderPayload(body);

  const res = await fetch(`https://${shop}/admin/api/2024-10/draft_orders.json`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-Shopify-Access-Token': token,
    },
    body: JSON.stringify(payload),
  });

  const text = await res.text();
  if (!res.ok) {
    return json({ error: 'shopify_error', status: res.status, details: text }, 502, origin);
  }

  let parsed;
  try { parsed = JSON.parse(text); } catch { parsed = {}; }
  const draftId = parsed?.draft_order?.id;

  return json({ ok: true, draft_order_id: draftId }, 200, origin);
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const origin = request.headers.get('Origin') || '';

    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: corsHeaders(origin) });
    }

    if (url.pathname === '/health') {
      const hasToken = !!(await env.TOKENS.get('access_token'));
      return json({ ok: true, installed: hasToken }, 200, origin);
    }

    if (url.pathname === '/install' && request.method === 'GET') {
      return handleInstall(url, env);
    }

    if (url.pathname === '/auth/callback' && request.method === 'GET') {
      return handleCallback(url, env);
    }

    if (url.pathname === '/cotizacion' && request.method === 'POST') {
      return handleCotizacion(request, env, origin);
    }

    if (url.pathname === '/logo' && request.method === 'POST') {
      return handleLogoUpload(request, env, origin);
    }

    return new Response('Not found', { status: 404 });
  },
};
