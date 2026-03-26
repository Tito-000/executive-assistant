#!/usr/bin/env python3
"""
Final fix for sticky button:
- Desktop: compact single-line "QUIERO EL MÍO — PAGO AL RECIBIR", slim bar
- Mobile: "QUIERO EL MÍO" big + "Pago al recibir" small inside button, no sub-note
- Add missing CSS for sticky-desktop-suffix and sticky-btn-sub responsive behavior
- Reduce #sticky-bar padding to make it less tall
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

responsive_css = """
    /* ── Sticky button responsive ── */
    .sticky-desktop-suffix { display: inline; }
    .sticky-btn-sub { display: none; }
    @media (max-width: 768px) {
      .sticky-desktop-suffix { display: none; }
      .sticky-btn-sub { display: block; width: 100%; text-align: center; font-size: 10px; font-weight: 400; opacity: 0.65; margin-top: 1px; }
      .sticky-sub-note { display: none !important; }
      #sticky-bar { padding: 10px 16px; }
      .btn-whatsapp-sticky { font-size: 13px; padding: 10px 16px; }
    }"""

for filename in files:
    filepath = os.path.join(base_path, filename)
    if not os.path.exists(filepath):
        print(f"⚠️  {filename} — NOT FOUND")
        continue

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # Remove old responsive block if present
    content = re.sub(
        r'\n\s*/\* ── Sticky button responsive ── \*/.*?@media \(max-width: 768px\) \{.*?\.sticky-sub-note \{ display: none !important; \}.*?\}',
        '',
        content,
        flags=re.DOTALL
    )

    # Add correct responsive CSS before </style>
    if '/* ── Sticky button responsive ── */' not in content:
        content = content.replace('  </style>', responsive_css + '\n  </style>', 1)

    # Reduce #sticky-bar desktop padding to be slimmer
    content = re.sub(
        r'(#sticky-bar \{[^}]*padding:\s*)12px 24px;',
        r'\g<1>10px 24px;',
        content
    )

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ {filename}")
    else:
        print(f"⏭️  {filename} — no changes")

print("\n✅ Done!")
