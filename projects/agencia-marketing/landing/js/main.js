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

})();
