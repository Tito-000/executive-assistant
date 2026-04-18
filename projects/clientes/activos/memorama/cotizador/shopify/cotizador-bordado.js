/* Memorama — Cotizador de bordado/personalización
   Se inicializa automáticamente en cada .mmr-cotizador del DOM */

(function() {
  'use strict';

  function initCotizador(root) {
    const productId = root.dataset.productId;
    const productHandle = root.dataset.productHandle;
    const productImage = root.dataset.productImage;
    const config = (window.MMR_INIT && window.MMR_INIT[productId]) || null;
    if (!config) { console.warn('MMR: config no encontrado para producto', productId); return; }

    const PRICING = config.PRICING;

    const state = {
      logoFile: null,
      logoDataUrl: null,
      technique: null,
      positions: [],
      quantity: 1,
      fabricCanvas: null,
      logoObj: null
    };

    const $ = sel => root.querySelector(sel);
    const $$ = sel => root.querySelectorAll(sel);

    const priceNumber = root.querySelector('#mmrPriceNumber-' + productId);
    const priceUnit = root.querySelector('#mmrPriceUnit-' + productId);
    const priceBreakdown = root.querySelector('#mmrPriceBreakdown-' + productId);
    const volumeTip = root.querySelector('#mmrVolumeTip-' + productId);
    const cta = root.querySelector('#mmrCtaBtn-' + productId);
    const qtyInput = root.querySelector('#mmrQty-' + productId);
    const previewWrap = root.querySelector('#mmrPreviewWrap-' + productId);
    const previewCtrls = root.querySelector('#mmrPreviewControls-' + productId);
    const uploadZone = root.querySelector('#mmrUploadZone-' + productId);
    const logoInput = root.querySelector('#mmrLogoInput-' + productId);

    // ---------- Pricing engine ----------
    function calculate() {
      if (!state.technique) return null;

      const base = PRICING.base;
      const techCost = PRICING.techniques[state.technique].cost;
      const posCost = state.positions.reduce((s, p) => s + (PRICING.positions[p] || 0), 0);
      const unit = base + techCost + posCost;
      const subtotal = unit * state.quantity;

      const tier = PRICING.volumeDiscounts.find(t => state.quantity >= t.min && state.quantity <= t.max) || PRICING.volumeDiscounts[0];
      const discountAmt = subtotal * tier.disc;
      const total = subtotal - discountAmt;

      return { base, techCost, posCost, unit, subtotal, tier, discountAmt, total };
    }

    function fmt(n) {
      return Math.round(n).toLocaleString('es-DO');
    }

    function renderPrice() {
      const p = calculate();

      if (!p) {
        priceNumber.textContent = '—';
        priceUnit.textContent = 'Elige técnica para ver tu precio';
        priceBreakdown.classList.remove('visible');
        cta.disabled = true;
        return;
      }

      priceNumber.textContent = fmt(p.total);
      priceUnit.textContent = state.quantity + ' un · RD$ ' + fmt(p.total / state.quantity) + ' c/u';

      // Breakdown
      let html = '';
      html += `<div class="mmr-bd-row"><span>Base × ${state.quantity}</span><span>RD$ ${fmt(p.base * state.quantity)}</span></div>`;
      html += `<div class="mmr-bd-row"><span>${capitalize(state.technique)} × ${state.quantity}</span><span>+RD$ ${fmt(p.techCost * state.quantity)}</span></div>`;
      if (state.positions.length) {
        html += `<div class="mmr-bd-row"><span>Posiciones × ${state.quantity}</span><span>+RD$ ${fmt(p.posCost * state.quantity)}</span></div>`;
      }
      if (p.tier.disc > 0) {
        html += `<div class="mmr-bd-row discount"><span>🎉 Descuento volumen (-${Math.round(p.tier.disc*100)}%)</span><span>-RD$ ${fmt(p.discountAmt)}</span></div>`;
      }
      priceBreakdown.innerHTML = html;
      priceBreakdown.classList.add('visible');

      // Volume tip
      const next = PRICING.volumeDiscounts.find(t => t.min > state.quantity && t.disc > (p.tier.disc || 0));
      if (next) {
        const need = next.min - state.quantity;
        volumeTip.textContent = `💡 Agrega ${need} más para ahorrar ${Math.round(next.disc*100)}%`;
        volumeTip.style.display = '';
      } else if (p.tier.disc > 0) {
        volumeTip.textContent = `✓ Descuento ${Math.round(p.tier.disc*100)}% aplicado`;
        volumeTip.style.display = '';
      } else {
        volumeTip.style.display = 'none';
      }

      // Highlight active tier
      $$('.mmr-tier').forEach(t => {
        const min = parseInt(t.dataset.min);
        const max = parseInt(t.dataset.max);
        t.classList.toggle('active', state.quantity >= min && state.quantity <= max);
      });

      // Enable CTA only if logo uploaded + technique + at least 1 position
      cta.disabled = !(state.logoDataUrl && state.technique && state.positions.length > 0);
    }

    function capitalize(s) { return s.charAt(0).toUpperCase() + s.slice(1); }

    // ---------- Logo upload ----------
    logoInput.addEventListener('change', e => {
      const file = e.target.files[0];
      if (!file) return;
      const reader = new FileReader();
      reader.onload = ev => {
        state.logoFile = file;
        state.logoDataUrl = ev.target.result;
        uploadZone.classList.add('has-file');
        uploadZone.querySelector('.mmr-upload-icon').textContent = '✓';
        uploadZone.querySelector('.mmr-upload-text').textContent = file.name;
        initPreview();
        renderPrice();
      };
      reader.readAsDataURL(file);
    });

    // Drag & drop
    ['dragover','dragleave','drop'].forEach(evt => {
      uploadZone.addEventListener(evt, e => {
        e.preventDefault();
        if (evt === 'drop') {
          const f = e.dataTransfer.files[0];
          if (f) { logoInput.files = e.dataTransfer.files; logoInput.dispatchEvent(new Event('change')); }
        }
      });
    });

    function initPreview() {
      previewWrap.innerHTML = '<canvas id="mmrCanvas-' + productId + '" width="400" height="400"></canvas>';
      previewCtrls.style.display = '';

      if (!window.fabric) {
        previewWrap.innerHTML = '<div class="mmr-preview-empty">Cargando preview...</div>';
        setTimeout(initPreview, 500);
        return;
      }

      const canvas = new fabric.Canvas('mmrCanvas-' + productId, { backgroundColor: '#f8f8f8' });
      state.fabricCanvas = canvas;

      fabric.Image.fromURL(productImage, img => {
        img.scaleToWidth(400);
        img.set({ selectable: false, evented: false });
        canvas.setBackgroundImage(img, canvas.renderAll.bind(canvas));
      }, { crossOrigin: 'anonymous' });

      fabric.Image.fromURL(state.logoDataUrl, img => {
        img.scaleToWidth(80);
        img.set({
          left: 160, top: 150,
          borderColor: '#ff6b35', cornerColor: '#ff6b35',
          cornerSize: 10, transparentCorners: false
        });
        canvas.add(img);
        canvas.setActiveObject(img);
        state.logoObj = img;
        canvas.renderAll();
      });
    }

    previewCtrls.addEventListener('click', e => {
      if (!state.logoObj) return;
      const canvas = state.fabricCanvas;
      const action = e.target.dataset.action;
      if (action === 'zoomIn') state.logoObj.scale(state.logoObj.scaleX * 1.15);
      else if (action === 'zoomOut') state.logoObj.scale(state.logoObj.scaleX * 0.85);
      else if (action === 'rotate') state.logoObj.rotate((state.logoObj.angle || 0) + 15);
      else if (action === 'reset') state.logoObj.set({ left: 160, top: 150, angle: 0, scaleX: 0.2, scaleY: 0.2 });
      canvas.renderAll();
    });

    // ---------- Técnica ----------
    $$('.mmr-tech-card').forEach(card => {
      card.addEventListener('click', () => {
        if (card.classList.contains('disabled')) return;
        $$('.mmr-tech-card').forEach(c => c.classList.remove('selected'));
        card.classList.add('selected');
        state.technique = card.dataset.tech;
        renderPrice();
      });
    });

    // ---------- Posiciones ----------
    $$('.mmr-pos-item input').forEach(cb => {
      cb.addEventListener('change', () => {
        if (cb.checked && !state.positions.includes(cb.value)) state.positions.push(cb.value);
        else state.positions = state.positions.filter(p => p !== cb.value);
        renderPrice();
      });
    });

    // ---------- Cantidad ----------
    root.querySelectorAll('[data-qty]').forEach(btn => {
      btn.addEventListener('click', () => {
        if (btn.dataset.qty === 'plus') state.quantity++;
        else state.quantity = Math.max(1, state.quantity - 1);
        qtyInput.value = state.quantity;
        renderPrice();
      });
    });

    qtyInput.addEventListener('input', () => {
      state.quantity = Math.max(1, parseInt(qtyInput.value) || 1);
      renderPrice();
    });

    // ---------- CTA: envía cotización ----------
    cta.addEventListener('click', async () => {
      const p = calculate();
      const payload = {
        product_id: productId,
        product_handle: productHandle,
        product_title: config.PRODUCT_TITLE,
        technique: state.technique,
        positions: state.positions,
        quantity: state.quantity,
        logo_filename: state.logoFile ? state.logoFile.name : null,
        pricing: {
          unit: p.unit,
          subtotal: p.subtotal,
          discount_pct: Math.round(p.tier.disc * 100),
          total: p.total
        },
        timestamp: new Date().toISOString()
      };

      console.log('MMR — Cotización enviada:', payload);

      // FASE 1: abre form de Shopify Contact/RFQ con datos pre-cargados
      // FASE 2: envía a endpoint que crea Draft Order automáticamente
      cta.textContent = '✓ Cotización enviada';
      cta.disabled = true;
      alert('Cotización enviada!\n\nTotal: RD$ ' + fmt(p.total) + '\n\nMemorama validará tu logo y te contactará con el link de pago.');
    });

    // Init
    renderPrice();
  }

  function initAll() {
    document.querySelectorAll('.mmr-cotizador').forEach(initCotizador);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAll);
  } else {
    initAll();
  }
})();
