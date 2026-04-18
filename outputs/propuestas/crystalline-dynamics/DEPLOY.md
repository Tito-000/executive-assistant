# Deploy — Fence Growth System

## 🌐 Link público para presentar

**URL principal (deck):** https://tito-000.github.io/crystalline-fence-growth-system/

**PDFs descargables desde la URL pública:**
- Deck: https://tito-000.github.io/crystalline-fence-growth-system/deck-fence-growth-system.pdf
- Contrato: https://tito-000.github.io/crystalline-fence-growth-system/contrato-fence-growth-system.pdf

---

## 📦 Entregables generados

| Archivo | Tamaño | Uso |
|---|---|---|
| `presentacion-fence-growth-system.html` | — | Deck full-screen (21 slides) para presentar en laptop |
| `deck-fence-growth-system.pdf` | 10 MB | Respaldo para adjuntar por email/WhatsApp |
| `contrato-fence-growth-system.html` | — | Versión editable del contrato |
| `contrato-fence-growth-system.pdf` | 255 KB | Contrato firmable (imprimible en Letter) |

---

## 💰 Pricing (consistente en todos los documentos)

- **Setup:** $1,497 USD (50% adelantado = $748.50)
- **Mensual:** $397 USD/mes (mínimo 3 meses)
- **Ad spend:** $1,000 – $1,500 USD/mes (tarjeta del cliente, directo a Google)

---

## 🔄 Cómo re-deployar si actualizas el HTML

```bash
# Desde la carpeta del proyecto
cd "outputs/propuestas/crystalline-dynamics"

# 1. Regenerar PDF del deck si editaste el HTML
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --headless --disable-gpu --no-sandbox \
  --print-to-pdf="deck-fence-growth-system.pdf" \
  --no-pdf-header-footer \
  --virtual-time-budget=8000 \
  --window-size=1440,810 \
  "file://$(pwd)/presentacion-fence-growth-system.html"

# 2. Clonar el repo remoto, reemplazar archivos, y push
git clone https://github.com/Tito-000/crystalline-fence-growth-system.git /tmp/cd-redeploy
cp presentacion-fence-growth-system.html /tmp/cd-redeploy/index.html
cp deck-fence-growth-system.pdf contrato-fence-growth-system.pdf /tmp/cd-redeploy/
cd /tmp/cd-redeploy
git add -A
git commit -m "Update deck"
git push
```

GitHub Pages reconstruye automáticamente en ~60-90 segundos.

---

## 🎯 Flujo de la reunión

1. **Abrir en laptop:** https://tito-000.github.io/crystalline-fence-growth-system/
2. **Navegar con flechas** (← →) — las 21 slides cargan full-screen
3. **Si pide "mándame algo":** compartes el link directamente o adjuntas los 2 PDFs
4. **Si cierra en la reunión:** abre `contrato-fence-growth-system.pdf` en iPad o imprime → firma en el momento
5. **Primer cobro:** $748.50 USD (50% setup) vía Stripe / Wise / PayPal

---

## 📁 Repo

- **GitHub:** https://github.com/Tito-000/crystalline-fence-growth-system
- **Cuenta:** Tito-000
- **Branch:** main
- **Deploy:** GitHub Pages desde `/` root
