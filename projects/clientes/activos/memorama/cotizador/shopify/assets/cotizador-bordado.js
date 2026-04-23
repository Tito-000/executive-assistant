/* Memorama — Cotizador de bordado/personalización (SIN preview canvas)
   Se inicializa automáticamente en cada .mmr-cotizador del DOM */

(function() {
  'use strict';

  function initCotizador(root) {
    const productId = root.dataset.productId;
    const productHandle = root.dataset.productHandle;
    const config = (window.MMR_INIT && window.MMR_INIT[productId]) || null;
    if (!config) { console.warn('MMR: config no encontrado para producto', productId); return; }

    const PRICING = config.PRICING;

    const state = {
      logoFile: null,
      technique: null,
      positions: [],
      quantity: 1,
      selectedOptions: {},
      selectedVariant: null,
      // Matriz color x talla: { 'Rojo': { 'S': 2, 'M': 3 }, 'Azul': { 'L': 5 } }
      matrix: {}
    };

    const variantsScript = root.querySelector('#mmrVariants-' + productId);
    const PRODUCT_VARIANTS = variantsScript ? JSON.parse(variantsScript.textContent) : [];

    // ---------- Precio base provisional según tipo de prenda ----------
    // Se usa si product.metafields.memorama.base_price no existe
    function detectGarmentBase() {
      const title = (config.PRODUCT_TITLE || '').toLowerCase();
      if (/sudadera|hoodie|buzo|capucha/.test(title)) return 1200;
      if (/polo/.test(title)) return 650;
      if (/gorra|cap\b/.test(title)) return 350;
      if (/t-?shirt|camiseta|camisa|playera/.test(title)) return 450;
      return 500;
    }

    // ---------- Ajustes de precio genéricos ----------
    function colorMultFor(name) {
      const n = (name || '').toLowerCase();
      const isWhite = /blanc|white|natural|crudo|marfil/.test(n);
      const hasColor = /negr|rojo|azul|verde|amarill|gris|rosa|morad|naranj|marr[oó]n|beige|caf[eé]|vinotinto|turquesa|celeste|fucsia|lila|mostaza|oliva|lima|magenta|violeta/.test(n);
      return (!isWhite && hasColor) ? 1.10 : 1.00;
    }
    function sizeAddFor(size) {
      const s = (size || '').toLowerCase();
      if (/\b(3xl|xxxl)\b/.test(s)) return 90;
      if (/\b(2xl|xxl)\b/.test(s)) return 60;
      if (/\bxl\b/.test(s)) return 30;
      return 0;
    }
    // Legacy: variant ya seleccionado (cuando no hay matriz)
    function variantAdjustment() {
      if (!state.selectedVariant) return { colorMult: 1, sizeAdd: 0 };
      const opts = [state.selectedVariant.option1, state.selectedVariant.option2, state.selectedVariant.option3]
        .filter(Boolean);
      let colorMult = 1, sizeAdd = 0;
      for (const o of opts) {
        const cm = colorMultFor(o); if (cm > colorMult) colorMult = cm;
        const sa = sizeAddFor(o); if (sa > sizeAdd) sizeAdd = sa;
      }
      return { colorMult, sizeAdd };
    }

    const $ = sel => root.querySelector(sel);
    const $$ = sel => root.querySelectorAll(sel);

    const priceNumber = root.querySelector('#mmrPriceNumber-' + productId);
    const priceUnit = root.querySelector('#mmrPriceUnit-' + productId);
    const priceBreakdown = root.querySelector('#mmrPriceBreakdown-' + productId);
    const volumeTip = root.querySelector('#mmrVolumeTip-' + productId);
    const cta = root.querySelector('#mmrCtaBtn-' + productId);
    const qtyInput = root.querySelector('#mmrQty-' + productId);
    const uploadZone = root.querySelector('#mmrUploadZone-' + productId);
    const logoInput = root.querySelector('#mmrLogoInput-' + productId);

    // ---------- Matriz helpers ----------
    function matrixTotalQty() {
      let total = 0;
      for (const color in state.matrix) {
        for (const size in state.matrix[color]) {
          total += state.matrix[color][size] || 0;
        }
      }
      return total;
    }

    // ---------- Pricing engine ----------
    function calculate() {
      if (!state.technique) return null;

      const rawBase = PRICING.base > 0 ? PRICING.base : detectGarmentBase();
      const techCost = PRICING.techniques[state.technique].cost;
      const posCost = state.positions.reduce((s, p) => s + (PRICING.positions[p] || 0), 0);

      let qty = 0;
      let baseSubtotal = 0;

      const usingMatrix = Object.keys(state.matrix).length > 0;
      if (usingMatrix) {
        for (const color in state.matrix) {
          const cm = colorMultFor(color);
          for (const size in state.matrix[color]) {
            const n = state.matrix[color][size] || 0;
            if (!n) continue;
            const unitBase = Math.round(rawBase * cm) + sizeAddFor(size);
            baseSubtotal += unitBase * n;
            qty += n;
          }
        }
      } else {
        const adj = variantAdjustment();
        const unitBase = Math.round(rawBase * adj.colorMult) + adj.sizeAdd;
        qty = state.quantity;
        baseSubtotal = unitBase * qty;
      }

      if (qty < 1) qty = 1;
      const addonsSubtotal = (techCost + posCost) * qty;
      const subtotal = baseSubtotal + addonsSubtotal;

      const tier = PRICING.volumeDiscounts.find(t => qty >= t.min && qty <= t.max) || PRICING.volumeDiscounts[0];
      const discountAmt = subtotal * tier.disc;
      const total = subtotal - discountAmt;

      const unit = qty > 0 ? total / qty : 0;
      const base = qty > 0 ? baseSubtotal / qty : rawBase;

      return { base, rawBase, techCost, posCost, unit, subtotal, tier, discountAmt, total, qty, baseSubtotal };
    }

    function fmt(n) {
      return Math.round(n).toLocaleString('es-DO');
    }

    function renderPrice() {
      const p = calculate();

      if (!p) {
        priceNumber.textContent = '---';
        priceUnit.textContent = 'Elige t\u00e9cnica para ver tu precio';
        priceBreakdown.classList.remove('visible');
        cta.disabled = true;
        return;
      }

      const qty = p.qty;
      priceNumber.textContent = fmt(p.total);
      priceUnit.textContent = qty + ' un · RD$ ' + fmt(p.unit) + ' c/u';

      // Breakdown
      let html = '';
      html += `<div class="mmr-bd-row"><span>Base × ${qty}</span><span>RD$ ${fmt(p.baseSubtotal)}</span></div>`;
      html += `<div class="mmr-bd-row"><span>${capitalize(state.technique)} × ${qty}</span><span>+RD$ ${fmt(p.techCost * qty)}</span></div>`;
      if (state.positions.length) {
        html += `<div class="mmr-bd-row"><span>Posiciones × ${qty}</span><span>+RD$ ${fmt(p.posCost * qty)}</span></div>`;
      }
      if (p.tier.disc > 0) {
        html += `<div class="mmr-bd-row discount"><span>Descuento volumen (-${Math.round(p.tier.disc*100)}%)</span><span>-RD$ ${fmt(p.discountAmt)}</span></div>`;
      }
      priceBreakdown.innerHTML = html;
      priceBreakdown.classList.add('visible');

      // Volume tip
      if (volumeTip) {
        const next = PRICING.volumeDiscounts.find(t => t.min > qty && t.disc > (p.tier.disc || 0));
        if (next) {
          const need = next.min - qty;
          volumeTip.textContent = `Agrega ${need} mas para ahorrar ${Math.round(next.disc*100)}%`;
          volumeTip.style.display = '';
        } else if (p.tier.disc > 0) {
          volumeTip.textContent = `Descuento ${Math.round(p.tier.disc*100)}% aplicado`;
          volumeTip.style.display = '';
        } else {
          volumeTip.style.display = 'none';
        }
      }

      // Highlight active tier
      $$('.mmr-tier').forEach(t => {
        const min = parseInt(t.dataset.min);
        const max = parseInt(t.dataset.max);
        t.classList.toggle('active', qty >= min && qty <= max);
      });

      // Enable CTA: logo + tecnica + posicion + cantidad > 0
      cta.disabled = !(state.logoFile && state.technique && state.positions.length > 0 && qty > 0);
    }

    function capitalize(s) { return s.charAt(0).toUpperCase() + s.slice(1); }

    // ---------- Logo upload (sin preview canvas) ----------
    logoInput.addEventListener('change', e => {
      const file = e.target.files[0];
      if (!file) return;
      state.logoFile = file;
      uploadZone.classList.add('has-file');
      uploadZone.querySelector('.mmr-upload-icon').innerHTML = '<svg width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><polyline points="20 6 9 17 4 12"></polyline></svg>';
      uploadZone.querySelector('.mmr-upload-text').textContent = file.name;
      uploadZone.querySelector('.mmr-upload-hint').textContent = 'Logo cargado correctamente';
      renderPrice();
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
    $$('.mmr-pos-card input').forEach(cb => {
      cb.addEventListener('change', () => {
        if (cb.checked && !state.positions.includes(cb.value)) state.positions.push(cb.value);
        else state.positions = state.positions.filter(p => p !== cb.value);
        renderPrice();
      });
    });

    // ---------- Variantes ----------
    const COLOR_MAP = {
      'blanco': '#ffffff', 'white': '#ffffff', 'natural': '#f5f0e6', 'crudo': '#f5f0e6', 'marfil': '#fff8e7',
      'negro': '#111111', 'black': '#111111',
      'gris': '#808080', 'grey': '#808080', 'gray': '#808080',
      'rojo': '#d32f2f', 'red': '#d32f2f', 'vinotinto': '#5c1a1b', 'vino': '#5c1a1b',
      'azul': '#1e40af', 'azul royal': '#1d4ed8', 'azul royale': '#1d4ed8', 'royal': '#1d4ed8',
      'azul marino': '#0b1f4d', 'marino': '#0b1f4d', 'navy': '#0b1f4d',
      'celeste': '#7dd3fc', 'turquesa': '#14b8a6', 'cyan': '#06b6d4',
      'verde': '#16a34a', 'oliva': '#6b7b3a', 'militar': '#4b5320',
      'amarillo': '#facc15', 'mostaza': '#d4a017',
      'naranja': '#f97316', 'naranjo': '#f97316',
      'rosa': '#ec4899', 'rosado': '#ec4899', 'fucsia': '#d946ef',
      'morado': '#7c3aed', 'lila': '#c084fc', 'violeta': '#8b5cf6',
      'marron': '#78350f', 'marrón': '#78350f', 'cafe': '#6b3410', 'café': '#6b3410', 'beige': '#d4b896'
    };

    function resolveColor(name) {
      const key = (name || '').toLowerCase().trim();
      if (COLOR_MAP[key]) return COLOR_MAP[key];
      for (const k in COLOR_MAP) {
        if (key.includes(k)) return COLOR_MAP[k];
      }
      return '#cccccc';
    }

    // Pintar swatches con su color real
    root.querySelectorAll('.mmr-swatch-dot').forEach(dot => {
      dot.style.background = resolveColor(dot.dataset.colorName);
    });

    // ---------- MATRIZ color x talla ----------
    const sizesScript = root.querySelector('#mmrSizes-' + productId);
    const SIZES = sizesScript ? JSON.parse(sizesScript.textContent) : [];
    const matrixWrap = root.querySelector('#mmrMatrixWrap-' + productId);
    const matrixRowsEl = root.querySelector('#mmrMatrixRows-' + productId);
    const matrixEmptyEl = root.querySelector('#mmrMatrixEmpty-' + productId);
    const matrixTotalEl = root.querySelector('#mmrMatrixTotal-' + productId);
    const colorPicker = root.querySelector('#mmrColorPicker-' + productId);

    function renderMatrix() {
      if (!matrixRowsEl) return;
      const colors = Object.keys(state.matrix);
      if (!colors.length) {
        matrixRowsEl.innerHTML = '';
        if (matrixEmptyEl) matrixEmptyEl.style.display = '';
      } else {
        if (matrixEmptyEl) matrixEmptyEl.style.display = 'none';
        matrixRowsEl.innerHTML = colors.map(color => {
          const row = state.matrix[color] || {};
          let rowTotal = 0;
          const cells = (SIZES && SIZES.length ? SIZES : ['U']).map(size => {
            const v = row[size] || '';
            if (v) rowTotal += parseInt(v) || 0;
            return `<div class="mmr-matrix-cell"><input type="number" min="0" value="${v}" data-color="${color}" data-size="${size}" placeholder="0"></div>`;
          }).join('');
          const removeBtn = singleColor ? '' : `<button type="button" class="mmr-matrix-remove" data-color="${color}" aria-label="Quitar color">×</button>`;
          return `
            <div class="mmr-matrix-row" data-color="${color}">
              <div class="mmr-matrix-color">
                <span class="mmr-swatch-dot" style="background:${resolveColor(color.toLowerCase())}"></span>
                <span class="mmr-matrix-color-name">${color}</span>
                ${removeBtn}
              </div>
              ${cells}
              <div class="mmr-matrix-row-total-val">${rowTotal}</div>
            </div>`;
        }).join('');
      }
      const total = matrixTotalQty();
      if (matrixTotalEl) matrixTotalEl.textContent = total;
    }

    function bindMatrixInputs() {
      if (!matrixRowsEl) return;
      matrixRowsEl.querySelectorAll('input[type="number"]').forEach(inp => {
        inp.addEventListener('input', () => {
          const color = inp.dataset.color;
          const size = inp.dataset.size;
          const v = Math.max(0, parseInt(inp.value) || 0);
          if (!state.matrix[color]) state.matrix[color] = {};
          if (v > 0) state.matrix[color][size] = v;
          else delete state.matrix[color][size];
          const rowEl = inp.closest('.mmr-matrix-row');
          if (rowEl) {
            let rt = 0;
            rowEl.querySelectorAll('input[type="number"]').forEach(i => { rt += parseInt(i.value) || 0; });
            const rtEl = rowEl.querySelector('.mmr-matrix-row-total-val');
            if (rtEl) rtEl.textContent = rt;
          }
          if (matrixTotalEl) matrixTotalEl.textContent = matrixTotalQty();
          renderPrice();
        });
      });
      matrixRowsEl.querySelectorAll('.mmr-matrix-remove').forEach(btn => {
        btn.addEventListener('click', () => {
          const color = btn.dataset.color;
          delete state.matrix[color];
          const sw = colorPicker && colorPicker.querySelector(`.mmr-variant-swatch[data-color="${CSS.escape(color)}"]`);
          if (sw) sw.classList.remove('selected');
          renderMatrix();
          bindMatrixInputs();
          renderPrice();
        });
      });
    }

    if (colorPicker) {
      colorPicker.querySelectorAll('.mmr-variant-swatch').forEach(sw => {
        sw.addEventListener('click', () => {
          const color = sw.dataset.color;
          if (state.matrix[color]) {
            delete state.matrix[color];
            sw.classList.remove('selected');
          } else {
            state.matrix[color] = {};
            sw.classList.add('selected');
          }
          renderMatrix();
          bindMatrixInputs();
          renderPrice();
        });
      });
    }

    // Set CSS var con número de tallas para grid
    if (matrixWrap) {
      matrixWrap.style.setProperty('--mmr-size-count', (SIZES && SIZES.length) ? SIZES.length : 1);
    }

    // Detectar single-color: o hay 1 swatch, o no hay picker en absoluto (producto sin color option)
    let singleColor = false;
    const swatches = colorPicker ? colorPicker.querySelectorAll('.mmr-variant-swatch') : [];
    if (colorPicker && swatches.length === 1) {
      const onlySw = swatches[0];
      const onlyColor = onlySw.dataset.color;
      state.matrix[onlyColor] = {};
      onlySw.classList.add('selected');
      colorPicker.classList.add('mmr-single-color');
      singleColor = true;
    } else if (!colorPicker || swatches.length === 0) {
      // Producto sin opción color — inferir del título (ej: "Camiseta blanca" → Blanco)
      const title = (config.PRODUCT_TITLE || '').toLowerCase();
      let inferred = 'Blanco';
      const colorMatches = {
        'blanc|white': 'Blanco', 'negr|black': 'Negro', 'gris|grey|gray': 'Gris',
        'rojo|red': 'Rojo', 'azul|blue': 'Azul', 'verde|green': 'Verde',
        'amarill|yellow': 'Amarillo', 'naranj|orange': 'Naranja', 'rosa|pink': 'Rosa',
        'morad|purple': 'Morado', 'marr[oó]n|brown|caf[eé]': 'Marrón', 'beige': 'Beige',
        'natural': 'Natural', 'crudo': 'Crudo', 'marino|navy': 'Azul marino'
      };
      for (const k in colorMatches) {
        if (new RegExp(k).test(title)) { inferred = colorMatches[k]; break; }
      }
      state.matrix[inferred] = {};
      if (colorPicker) colorPicker.classList.add('mmr-single-color');
      singleColor = true;
    }

    // Ajustar label + mensaje si es single-color
    if (singleColor) {
      const labelTxt = root.querySelector('#mmrMatrixLabel-' + productId + ' .mmr-matrix-label-text');
      const labelHint = root.querySelector('#mmrMatrixLabel-' + productId + ' .mmr-hint');
      if (labelTxt) labelTxt.textContent = 'Elige la cantidad por talla';
      if (labelHint) labelHint.textContent = '(ingresa unidades en las tallas que necesites)';
      if (matrixEmptyEl) matrixEmptyEl.textContent = 'Ingresa la cantidad en cada talla que necesites.';
    }

    // Init matriz
    renderMatrix();
    bindMatrixInputs();

    // Resaltar matriz cuando no hay cantidades todavía
    function highlightMatrixIfEmpty() {
      if (!matrixWrap) return;
      const needsQty = Object.keys(state.matrix).length > 0 && matrixTotalQty() === 0;
      matrixWrap.classList.toggle('mmr-matrix-needs-qty', needsQty);
    }
    highlightMatrixIfEmpty();
    if (matrixRowsEl) {
      matrixRowsEl.addEventListener('input', highlightMatrixIfEmpty);
    }

    // ---------- Cantidad legacy (solo si NO hay variantes) ----------
    if (qtyInput) {
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
    }

    // ---------- Modal de contacto ----------
    const POSITION_LABELS = {
      center_front: 'Pecho centro',
      center_back: 'Espalda centro',
      left_chest: 'Pecho izquierdo',
      right_chest: 'Pecho derecho',
      left_sleeve: 'Manga izquierda',
      right_sleeve: 'Manga derecha',
      bespoke: 'Personalizada (ubicacion libre)'
    };
    const TECHNIQUE_LABELS = {
      bordado: 'Bordado',
      serigrafia: 'Serigrafia',
      dtf: 'DTF',
      sublimacion: 'Sublimacion'
    };

    const modalOverlay = root.querySelector('#mmrModalOverlay-' + productId);
    // Mover modal al body para evitar conflictos con overflow/transform del theme
    if (modalOverlay && modalOverlay.parentElement !== document.body) {
      document.body.appendChild(modalOverlay);
    }
    const modalClose = modalOverlay ? modalOverlay.querySelector('#mmrModalClose-' + productId) : null;
    const modalForm = modalOverlay ? modalOverlay.querySelector('#mmrModalForm-' + productId) : null;
    const modalSummary = modalOverlay ? modalOverlay.querySelector('#mmrModalSummary-' + productId) : null;
    const modalSubmit = modalOverlay ? modalOverlay.querySelector('#mmrModalSubmit-' + productId) : null;

    function buildSummary(p) {
      const matrixRows = Object.keys(state.matrix).map(color => {
        const sizes = state.matrix[color];
        const parts = Object.keys(sizes).filter(s => sizes[s] > 0).map(s => s + ':' + sizes[s]);
        const total = Object.values(sizes).reduce((a, b) => a + (b || 0), 0);
        return { color: color, detail: parts.join(', '), total: total };
      }).filter(r => r.total > 0);

      let html = '';
      html += '<div class="mmr-modal-summary-row"><span class="mmr-modal-summary-label">Producto</span><span class="mmr-modal-summary-value">' + escapeHtml(config.PRODUCT_TITLE) + '</span></div>';
      if (state.technique) html += '<div class="mmr-modal-summary-row"><span class="mmr-modal-summary-label">Tecnica</span><span class="mmr-modal-summary-value">' + (TECHNIQUE_LABELS[state.technique] || state.technique) + '</span></div>';
      if (state.positions.length) {
        const posNames = state.positions.map(p => POSITION_LABELS[p] || p).join(', ');
        html += '<div class="mmr-modal-summary-row"><span class="mmr-modal-summary-label">Posiciones</span><span class="mmr-modal-summary-value">' + posNames + '</span></div>';
      }
      if (matrixRows.length) {
        const colorText = matrixRows.map(r => r.color + ' (' + r.detail + ')').join('<br>');
        html += '<div class="mmr-modal-summary-row"><span class="mmr-modal-summary-label">Colores y tallas</span><span class="mmr-modal-summary-value">' + colorText + '</span></div>';
      }
      html += '<div class="mmr-modal-summary-row"><span class="mmr-modal-summary-label">Cantidad total</span><span class="mmr-modal-summary-value">' + p.qty + ' un</span></div>';
      if (p.tier && p.tier.disc > 0) {
        html += '<div class="mmr-modal-summary-row"><span class="mmr-modal-summary-label">Descuento volumen</span><span class="mmr-modal-summary-value">-' + Math.round(p.tier.disc * 100) + '%</span></div>';
      }
      html += '<div class="mmr-modal-summary-total"><span>Total estimado</span><strong>RD$ ' + fmt(p.total) + '</strong></div>';
      return html;
    }

    function escapeHtml(str) {
      return String(str || '').replace(/[&<>"']/g, function(c) {
        return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
      });
    }

    function openModal() {
      const p = calculate();
      modalSummary.innerHTML = buildSummary(p);
      modalOverlay.hidden = false;
      document.body.classList.add('mmr-modal-open');
    }

    function closeModal() {
      modalOverlay.hidden = true;
      document.body.classList.remove('mmr-modal-open');
    }

    // ---------- CTA: abre el modal ----------
    cta.addEventListener('click', () => {
      if (cta.disabled) return;
      openModal();
    });

    if (modalClose) modalClose.addEventListener('click', closeModal);
    if (modalOverlay) {
      modalOverlay.addEventListener('click', (e) => {
        if (e.target === modalOverlay) closeModal();
      });
    }
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && !modalOverlay.hidden) closeModal();
    });

    // ---------- Buscar variant_id por color/size ----------
    function findVariantId(color, size) {
      const norm = s => String(s || '').trim().toLowerCase();
      const c = norm(color);
      const sz = norm(size);
      for (const v of PRODUCT_VARIANTS) {
        const opts = [v.option1, v.option2, v.option3].filter(Boolean).map(norm);
        const matchColor = !c || opts.includes(c);
        const matchSize = !sz || opts.includes(sz);
        if (matchColor && matchSize) return v.id;
      }
      return null;
    }

    // Construir line_items con variant_id real para cada combinación color/size
    function buildVariantLineItems() {
      const p = calculate();
      const items = [];
      const colors = Object.keys(state.matrix);

      if (!colors.length) {
        // Sin matriz: un solo item custom
        return [{
          title: `${config.PRODUCT_TITLE} — ${state.technique || 'personalizado'}`,
          quantity: p.qty,
          price: p.unit
        }];
      }

      for (const color of colors) {
        const sizes = state.matrix[color] || {};
        for (const size in sizes) {
          const qty = sizes[size] || 0;
          if (qty <= 0) continue;
          const techLabel = state.technique ? ` (${state.technique})` : '';
          // Shopify ignora price override si mandas variant_id —
          // usamos custom items con título descriptivo para respetar el precio del cotizador
          items.push({
            title: `${config.PRODUCT_TITLE} — ${color} / ${size}${techLabel}`,
            quantity: qty,
            price: p.unit
          });
        }
      }

      if (!items.length) {
        return [{
          title: `${config.PRODUCT_TITLE} — ${state.technique || 'personalizado'}`,
          quantity: p.qty,
          price: p.unit
        }];
      }

      return items;
    }

    // ---------- Submit del formulario ----------
    const WORKER_BASE = 'https://memorama-cotizador.martinmercedes100.workers.dev';

    if (modalForm) {
      modalForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const fd = new FormData(modalForm);
        const p = calculate();
        const payload = {
          product_id: productId,
          product_handle: productHandle,
          product_title: config.PRODUCT_TITLE,
          matrix: state.matrix,
          technique: state.technique,
          positions: state.positions,
          quantity: p.qty,
          logo_filename: state.logoFile ? state.logoFile.name : null,
          contact: {
            name: fd.get('name'),
            phone: fd.get('phone'),
            email: fd.get('email'),
            company: fd.get('company') || null,
            deadline: fd.get('deadline') || null,
            comments: fd.get('comments') || null
          },
          pricing: {
            unit: p.unit,
            subtotal: p.subtotal,
            discount_pct: Math.round(p.tier.disc * 100),
            total: p.total
          },
          timestamp: new Date().toISOString()
        };

        console.log('MMR — Cotizacion enviada:', payload);

        modalSubmit.textContent = 'Enviando...';
        modalSubmit.disabled = true;

        try {
          sessionStorage.setItem('mmr_last_quote', JSON.stringify(payload));
        } catch (e) { /* ignore */ }

        // 1. Subir logo a R2 si existe
        let logoUrl = null;
        if (state.logoFile) {
          try {
            modalSubmit.textContent = 'Subiendo logo...';
            const logoFd = new FormData();
            logoFd.append('file', state.logoFile);
            const logoRes = await fetch(WORKER_BASE + '/logo', {
              method: 'POST',
              body: logoFd
            });
            const logoData = await logoRes.json().catch(() => ({}));
            if (logoRes.ok && logoData.url) {
              logoUrl = logoData.url;
              console.log('MMR — Logo subido:', logoUrl);
            } else {
              console.warn('MMR — Error subiendo logo:', logoRes.status, logoData);
            }
          } catch (err) {
            console.warn('MMR — No se pudo subir el logo:', err);
          }
        }

        // 2. Payload para el Worker (crea Draft Order en Shopify)
        const workerPayload = {
          contact: payload.contact,
          config: {
            productName: config.PRODUCT_TITLE,
            productHandle: productHandle,
            color: Object.keys(state.matrix).join(', '),
            sizes: state.matrix,
            positions: state.positions,
            quantity: p.qty,
            deadline: payload.contact.deadline
          },
          totals: {
            unitPrice: p.unit,
            total: p.total
          },
          items: buildVariantLineItems(),
          logoFilename: payload.logo_filename,
          logoUrl: logoUrl
        };

        // 3. Enviar cotización al Worker → crea Draft Order
        try {
          modalSubmit.textContent = 'Enviando cotización...';
          const res = await fetch(WORKER_BASE + '/cotizacion', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(workerPayload)
          });
          const data = await res.json().catch(() => ({}));
          if (res.ok) {
            console.log('MMR — Draft Order creada:', data.draft_order_id);
          } else {
            console.warn('MMR — Worker respondió error:', res.status, data);
          }
        } catch (err) {
          console.warn('MMR — No se pudo conectar con el Worker:', err);
        }

        window.location.href = '/pages/gracias';
      });
    }

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
