#!/usr/bin/env python3
"""
Desktop: revert button to original "QUIERO EL MÍO — PAGO AL RECIBIR" + sub-note below, but slimmer padding.
Mobile: keep "QUIERO EL MÍO" + <span class="sticky-btn-sub">Pago al recibir</span> inside button.

Approach:
1. Revert HTML button text back to "QUIERO EL MÍO — PAGO AL RECIBIR" (remove the span)
2. Re-add .sticky-sub-note <p> below the button with "Pago al recibir en casa · Envío gratis"
3. Keep .sticky-btn-sub CSS (used in mobile override)
4. Reduce button padding from 12px 20px to 10px 20px (slimmer)
5. Add mobile media query that:
   - Shows "QUIERO EL MÍO" only (hides "— PAGO AL RECIBIR" part)
   - Shows sticky-btn-sub span inside button
   - Hides the .sticky-sub-note below
   - Keeps button full width

Actually simpler approach:
- Desktop: button says "QUIERO EL MÍO — PAGO AL RECIBIR", sub-note below, slim padding
- Mobile: button says "QUIERO EL MÍO" + sticky-btn-sub inside, no sub-note

Use a span for the "— PAGO AL RECIBIR" part and hide it on mobile.
The sticky-btn-sub span is shown only on mobile.
"""
import os
import re

files = [
    'magistral.html', 'platinum.html', 'booster.html', 'multi-resveratrol.html',
    'immunocal-azul.html', 'immunocal-sport.html', 'k-21-nutrik.html',
    'immunocal-optimizer.html', 'omega-gen-v.html', 'paquete-alto-rendimiento.html',
    'paquete-bienestar-plus.html', 'paquete-inicio-abundancia.html',
    'paquete-inicio-duo.html', 'immunocal-landing-v4.html',
]

base_path = '/Users/martinmercedes/Desktop/Executive assistant 2/outputs/immunotec/'

# CSS to add before </style>
mobile_css = """
    /* ── Sticky button responsive ── */
    .sticky-desktop-suffix { display: inline; }
    .sticky-btn-sub { display: none; width: 100%; text-align: center; font-size: 10px; font-weight: 400; opacity: 0.6; margin-top: 2px; }
    @media (max-width: 768px) {
      .sticky-desktop-suffix { display: none; }
      .sticky-btn-sub { display: block; }
      .sticky-sub-note { display: none; }
    }"""

for filename in files:
    filepath = os.path.join(base_path, filename)
    if not os.path.exists(filepath):
        print(f"⚠️  {filename} — NOT FOUND")
        continue

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # Step 1: Fix button text - replace current "QUIERO EL MÍO\n          <span class="sticky-btn-sub">Pago al recibir</span>"
    # with "QUIERO EL MÍO<span class="sticky-desktop-suffix"> — PAGO AL RECIBIR</span><span class="sticky-btn-sub">Pago al recibir</span>"
    content = re.sub(
        r'QUIERO EL MÍO\s*\n\s*<span class="sticky-btn-sub">Pago al recibir</span>',
        'QUIERO EL MÍO<span class="sticky-desktop-suffix"> — PAGO AL RECIBIR</span>\n          <span class="sticky-btn-sub">Pago al recibir</span>',
        content
    )

    # Also handle case where button still says "QUIERO EL MÍO — PAGO AL RECIBIR" (not yet updated)
    # and add the spans
    content = re.sub(
        r'QUIERO EL MÍO — PAGO AL RECIBIR(?!\s*</span>)(?!.*sticky-desktop-suffix)',
        'QUIERO EL MÍO<span class="sticky-desktop-suffix"> — PAGO AL RECIBIR</span>\n          <span class="sticky-btn-sub">Pago al recibir</span>',
        content
    )

    # Step 2: Re-add sticky-sub-note if missing
    # Find the closing </a> of btn-whatsapp-sticky and add <p> after it if not present
    if 'sticky-sub-note' not in content:
        content = re.sub(
            r'(class="btn-whatsapp-sticky"[^>]*>.*?</a>)(\s*</div>\s*</div>\s*</div>)',
            r'\1\n        <p class="sticky-sub-note">Pago al recibir en casa · Envío gratis</p>\2',
            content,
            flags=re.DOTALL
        )

    # Step 3: Update .sticky-sub-note CSS if it exists, or it'll be handled by mobile_css
    # Update padding to be slimmer
    content = re.sub(
        r'(\.btn-whatsapp-sticky\s*\{[^}]*padding:\s*)12px 20px;',
        r'\g<1>9px 20px;',
        content
    )

    # Step 4: Add mobile responsive CSS before </style> if not already there
    if 'sticky-desktop-suffix' not in content:
        content = content.replace('  </style>', mobile_css + '\n  </style>', 1)
    else:
        # Update the CSS block if already there
        pass

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ {filename}")
    else:
        print(f"⏭️  {filename} — NO CHANGES")

print("\n✅ Done!")
