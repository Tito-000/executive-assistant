# Catálogo de Servicios — Colaboradores

Catálogo confidencial de MM Agency para compartir con colaboradores y referidos. **No compartir con clientes finales.**

## Archivos

- `servicios-y-precios.html` — fuente editable
- `servicios-y-precios.pdf` — PDF listo para compartir por WhatsApp / email

## Modelo de negocio

- **Colaborador ejecutor:** cobra lo que quiera encima de los precios del catálogo. El margen es 100% suyo.
- **Colaborador referidor:** recibe 15% del primer cobro por cada cliente cerrado que refiera.

## Cómo actualizar los precios

1. Editar directamente las tablas en `servicios-y-precios.html` (secciones `<section class="page">`)
2. Regenerar el PDF con el comando de abajo
3. Enviar el nuevo PDF a los colaboradores

## Regenerar el PDF

Desde la carpeta `colaboradores/`:

```bash
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --headless --disable-gpu \
  --no-pdf-header-footer \
  --print-to-pdf="servicios-y-precios.pdf" \
  --no-margins \
  "file://$(pwd)/servicios-y-precios.html"
```

Verificar que el PDF tiene **12 páginas** y que los fondos dark + logos se ven correctamente.

## Estructura del PDF

1. Portada
2. Cómo funciona (el modelo)
3. Diseño & Web
4. Branding
5. Publicidad Pagada
6. CRM, Automatización & Lead Generation
7. Email Marketing
8. Tracking & Analítica
9. Contenido
10. Estrategia, Consultoría & SEO
11. Reglas del juego
12. Contacto
