/* ============================================= */
/* MM AGENCY — LANDING JS                           */
/* ============================================= */

(function () {
  'use strict';

  // ---------- NAV SCROLL STATE ----------
  const nav = document.getElementById('nav');
  let lastScroll = 0;
  window.addEventListener('scroll', () => {
    const currentScroll = window.scrollY;
    if (currentScroll > 50) {
      nav.classList.add('scrolled');
    } else {
      nav.classList.remove('scrolled');
    }
    lastScroll = currentScroll;
  }, { passive: true });

  // ---------- SCROLL REVEAL ----------
  const reveals = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add('visible');
          observer.unobserve(entry.target);
        }
      });
    }, {
      threshold: 0.1,
      rootMargin: '0px 0px -80px 0px'
    });
    reveals.forEach(el => observer.observe(el));
  } else {
    reveals.forEach(el => el.classList.add('visible'));
  }

  // ---------- COUNT UP (hero metric) ----------
  const countEl = document.querySelector('[data-count-to]');
  if (countEl) {
    const target = parseInt(countEl.dataset.countTo, 10);
    let started = false;
    const startCount = () => {
      if (started) return;
      started = true;
      const duration = 2000;
      const start = performance.now();
      const step = (now) => {
        const elapsed = now - start;
        const progress = Math.min(elapsed / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3);
        countEl.textContent = Math.floor(target * eased);
        if (progress < 1) requestAnimationFrame(step);
        else countEl.textContent = target;
      };
      setTimeout(() => requestAnimationFrame(step), 1400);
    };
    if ('IntersectionObserver' in window) {
      const countObs = new IntersectionObserver((entries) => {
        entries.forEach(entry => { if (entry.isIntersecting) startCount(); });
      }, { threshold: 0.3 });
      countObs.observe(countEl);
    } else {
      startCount();
    }
  }

  // ---------- FAQ (only one open at a time) ----------
  const faqItems = document.querySelectorAll('.faq-item');
  faqItems.forEach(item => {
    item.addEventListener('toggle', () => {
      if (item.open) {
        faqItems.forEach(other => {
          if (other !== item) other.open = false;
        });
      }
    });
  });

  // ---------- SMOOTH SCROLL for anchors ----------
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', (e) => {
      const href = anchor.getAttribute('href');
      if (href === '#' || href.length < 2) return;
      const target = document.querySelector(href);
      if (!target) return;
      e.preventDefault();
      const navHeight = nav.offsetHeight;
      const targetPos = target.getBoundingClientRect().top + window.scrollY - navHeight - 20;
      window.scrollTo({ top: targetPos, behavior: 'smooth' });
    });
  });

  // ---------- FORM VALIDATION & SUBMIT ----------
  const form = document.getElementById('contact-form');
  const successEl = document.getElementById('form-success');

  if (form) {
    form.addEventListener('submit', (e) => {
      e.preventDefault();

      // Clear errors
      form.querySelectorAll('.error').forEach(el => el.classList.remove('error'));

      // Validate required fields
      let hasError = false;
      const fields = form.querySelectorAll('[required]');
      fields.forEach(field => {
        if (!field.value.trim()) {
          field.classList.add('error');
          hasError = true;
        }
        if (field.type === 'email' && field.value) {
          const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
          if (!emailRegex.test(field.value)) {
            field.classList.add('error');
            hasError = true;
          }
        }
      });

      if (hasError) {
        const firstError = form.querySelector('.error');
        if (firstError) {
          firstError.focus();
          firstError.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
        return;
      }

      // Collect form data
      const formData = new FormData(form);
      const data = {};
      formData.forEach((value, key) => { data[key] = value; });

      // TODO: integrar con backend (Koomo CRM webhook + notificación WhatsApp a Martin)
      console.log('Form data ready for submission:', data);

      // Hide form fields, show success state
      const fieldsToHide = form.querySelectorAll('.form-row, .form-field, .btn, .form-microcopy, .form-legal');
      fieldsToHide.forEach(el => el.style.display = 'none');
      if (successEl) {
        successEl.hidden = false;
        successEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    });

    // Remove error state on input
    form.querySelectorAll('input, select, textarea').forEach(field => {
      field.addEventListener('input', () => {
        field.classList.remove('error');
      });
      field.addEventListener('change', () => {
        field.classList.remove('error');
      });
    });
  }

  // ---------- SQUADS GLOBE — gradient colors shift with mouse (círculo fijo) ----------
  const squadsStage = document.querySelector('.squads-stage');
  const glowGradient = document.getElementById('sqGlow');
  if (squadsStage && glowGradient) {
    const stops = glowGradient.querySelectorAll('stop');
    // Paletas base (colores por defecto del gradient)
    const basePalettes = [
      // [core, mid1, mid2, deep]
      ['#F54900', '#E0348E', '#7A2DC0', '#2E1A6B'], // default: naranja → magenta → morado
      ['#FF6B1A', '#D13A7E', '#6B2AB8', '#251560'], // un poco más rojo
      ['#E83E7A', '#A82DB0', '#5A2DC0', '#2B1A6B'], // magenta dominante
      ['#8A2BE2', '#6A2DC0', '#4A2AA0', '#201555'], // morado dominante
      ['#F54900', '#F06A1A', '#9A2DC0', '#2E1A6B'], // naranja dominante
    ];

    // Interpola entre dos hex
    const lerpColor = (a, b, t) => {
      const ah = parseInt(a.slice(1), 16);
      const bh = parseInt(b.slice(1), 16);
      const ar = (ah >> 16) & 255, ag = (ah >> 8) & 255, ab = ah & 255;
      const br = (bh >> 16) & 255, bg = (bh >> 8) & 255, bb = bh & 255;
      const r = Math.round(ar + (br - ar) * t);
      const g = Math.round(ag + (bg - ag) * t);
      const b2 = Math.round(ab + (bb - ab) * t);
      return 'rgb(' + r + ',' + g + ',' + b2 + ')';
    };

    let targetT = 0;        // posición objetivo en el ciclo de paletas (0..basePalettes.length-1)
    let currentT = 0;       // posición interpolada actual
    // Centro del glow (en %) — se mueve un poquito con el mouse
    const BASE_CX = 50;
    const BASE_CY = 50;
    const MAX_OFFSET = 8;   // máximo desplazamiento desde el centro (en %)
    let targetCX = BASE_CX, targetCY = BASE_CY;
    let currentCX = BASE_CX, currentCY = BASE_CY;
    let rafId = null;
    let active = false;

    const applyPalette = (t) => {
      const n = basePalettes.length;
      const i = Math.floor(t) % n;
      const j = (i + 1) % n;
      const f = t - Math.floor(t);
      const a = basePalettes[i];
      const b = basePalettes[j];
      stops[0].setAttribute('stop-color', lerpColor(a[0], b[0], f));
      stops[1].setAttribute('stop-color', lerpColor(a[1], b[1], f));
      stops[2].setAttribute('stop-color', lerpColor(a[2], b[2], f));
      stops[3].setAttribute('stop-color', lerpColor(a[3], b[3], f));
    };

    const animate = () => {
      currentT += (targetT - currentT) * 0.06; // lerp lento → cambio de color sutil
      currentCX += (targetCX - currentCX) * 0.08;
      currentCY += (targetCY - currentCY) * 0.08;
      applyPalette(currentT);
      glowGradient.setAttribute('cx', currentCX + '%');
      glowGradient.setAttribute('cy', currentCY + '%');
      glowGradient.setAttribute('fx', currentCX + '%');
      glowGradient.setAttribute('fy', currentCY + '%');
      if (
        Math.abs(targetT - currentT) > 0.002 ||
        Math.abs(targetCX - currentCX) > 0.05 ||
        Math.abs(targetCY - currentCY) > 0.05 ||
        active
      ) {
        rafId = requestAnimationFrame(animate);
      } else {
        rafId = null;
      }
    };

    squadsStage.addEventListener('mousemove', (e) => {
      const rect = squadsStage.getBoundingClientRect();
      const nx = (e.clientX - rect.left) / rect.width;   // 0..1
      const ny = (e.clientY - rect.top) / rect.height;   // 0..1
      // Paletas cambian según la posición
      targetT = (nx * 0.6 + ny * 0.4) * (basePalettes.length - 1);
      // El centro del glow se desplaza un poquito hacia el mouse (±MAX_OFFSET %)
      targetCX = BASE_CX + (nx - 0.5) * 2 * MAX_OFFSET;
      targetCY = BASE_CY + (ny - 0.5) * 2 * MAX_OFFSET;
      active = true;
      if (!rafId) rafId = requestAnimationFrame(animate);
    });

    squadsStage.addEventListener('mouseleave', () => {
      targetT = 0;
      targetCX = BASE_CX;
      targetCY = BASE_CY;
      active = false;
      if (!rafId) rafId = requestAnimationFrame(animate);
    });
  }

  // ---------- PILLARS SLIDER (differentiated approach) ----------
  const pillarsTrack = document.querySelector('.pillars-track');
  const pillarsViewport = document.querySelector('.pillars-viewport');
  const pillarsArrows = document.querySelectorAll('.pillars-arrow');
  if (pillarsTrack && pillarsViewport && pillarsArrows.length) {
    const slides = Array.from(pillarsTrack.querySelectorAll('.pillar-slide'));
    let index = 0;
    let currentTx = 0;

    const getStep = () => {
      if (slides.length < 2) return 0;
      const a = slides[0].getBoundingClientRect().left;
      const b = slides[1].getBoundingClientRect().left;
      return b - a;
    };

    const getMaxIndex = () => {
      const step = getStep();
      if (!step) return 0;
      const viewportW = pillarsViewport.clientWidth;
      const slideW = slides[0].offsetWidth;
      return Math.max(0, slides.length - 1 - Math.floor((viewportW - slideW) / step));
    };

    const setTransform = (tx, animate) => {
      if (!animate) pillarsTrack.classList.add('is-dragging');
      else pillarsTrack.classList.remove('is-dragging');
      pillarsTrack.style.transform = 'translate3d(' + tx + 'px, 0, 0)';
      currentTx = tx;
    };

    const update = (animate = true) => {
      const step = getStep();
      const max = getMaxIndex();
      if (index > max) index = max;
      if (index < 0) index = 0;
      setTransform(-index * step, animate);
      slides.forEach((s, i) => {
        s.classList.toggle('is-active', i === index);
      });
      pillarsArrows.forEach(btn => {
        const dir = btn.dataset.dir;
        if (dir === 'prev') btn.disabled = index <= 0;
        if (dir === 'next') btn.disabled = index >= max;
      });
    };

    pillarsArrows.forEach(btn => {
      btn.addEventListener('click', () => {
        const dir = btn.dataset.dir;
        if (dir === 'next') index++;
        else index--;
        update(true);
      });
    });

    // ---- Drag / swipe ----
    let dragging = false;
    let startX = 0;
    let startTx = 0;
    let moved = 0;

    const onDown = (e) => {
      dragging = true;
      moved = 0;
      startX = (e.touches ? e.touches[0].clientX : e.clientX);
      startTx = currentTx;
      pillarsTrack.classList.add('is-dragging');
    };
    const onMove = (e) => {
      if (!dragging) return;
      const x = (e.touches ? e.touches[0].clientX : e.clientX);
      moved = x - startX;
      setTransform(startTx + moved, false);
    };
    const onUp = () => {
      if (!dragging) return;
      dragging = false;
      const step = getStep() || 1;
      const threshold = step * 0.18;
      if (moved < -threshold) index++;
      else if (moved > threshold) index--;
      update(true);
    };

    pillarsTrack.addEventListener('mousedown', onDown);
    window.addEventListener('mousemove', onMove);
    window.addEventListener('mouseup', onUp);
    pillarsTrack.addEventListener('touchstart', onDown, { passive: true });
    pillarsTrack.addEventListener('touchmove', onMove, { passive: true });
    pillarsTrack.addEventListener('touchend', onUp);

    // Prevent text selection while dragging
    pillarsTrack.addEventListener('dragstart', (e) => e.preventDefault());

    // Keyboard nav
    window.addEventListener('keydown', (e) => {
      const rect = pillarsViewport.getBoundingClientRect();
      if (rect.top > window.innerHeight || rect.bottom < 0) return;
      if (e.key === 'ArrowRight') { index++; update(true); }
      if (e.key === 'ArrowLeft')  { index--; update(true); }
    });

    window.addEventListener('resize', () => update(false), { passive: true });
    requestAnimationFrame(() => update(true));
  }

  // ---------- MOBILE HAMBURGER MENU ----------
  const hamburger = document.getElementById('navHamburger');
  const mobileMenu = document.getElementById('navMobile');
  if (hamburger && mobileMenu) {
    const toggleMenu = () => {
      const isOpen = mobileMenu.classList.toggle('is-open');
      document.body.classList.toggle('nav-open', isOpen);
      // Swap icon: hamburger ↔ X
      hamburger.innerHTML = isOpen
        ? '<svg viewBox="0 0 24 24"><line x1="6" y1="6" x2="18" y2="18"/><line x1="6" y1="18" x2="18" y2="6"/></svg>'
        : '<svg viewBox="0 0 24 24"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>';
    };
    hamburger.addEventListener('click', toggleMenu);
    // Close on link click
    mobileMenu.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        mobileMenu.classList.remove('is-open');
        document.body.classList.remove('nav-open');
        hamburger.innerHTML = '<svg viewBox="0 0 24 24"><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="18" x2="21" y2="18"/></svg>';
      });
    });
  }

  // Home blog carousel arrows
  var homeBlogGrid = document.getElementById('homeBlogGrid');
  var homeBlogPrev = document.getElementById('homeBlogPrev');
  var homeBlogNext = document.getElementById('homeBlogNext');
  if (homeBlogGrid && homeBlogPrev && homeBlogNext) {
    var blogScrollAmount = function() {
      var card = homeBlogGrid.querySelector('.blog-card-link') || homeBlogGrid.querySelector('.blog-card');
      return card ? card.offsetWidth + 16 : 300;
    };
    homeBlogPrev.addEventListener('click', function() {
      homeBlogGrid.scrollBy({ left: -blogScrollAmount(), behavior: 'smooth' });
    });
    homeBlogNext.addEventListener('click', function() {
      homeBlogGrid.scrollBy({ left: blogScrollAmount(), behavior: 'smooth' });
    });
  }

})();
