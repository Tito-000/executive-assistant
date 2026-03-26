#!/usr/bin/env python3
"""
Revert sticky button width changes on desktop, keep them only on mobile.
- Revert .sticky-btn-wrap back to flex:1
- Revert .btn-whatsapp-sticky back to width:100%
- Add mobile-only media query with the narrow button styles
"""
import os
import re

files = [
    'magistral.html',
    'platinum.html',
    'booster.html',
    'multi-resveratrol.html',
    'immunocal-azul.html',
    'immunocal-sport.html',
    'k-21-nutrik.html',
    'immunocal-optimizer.html',
    'omega-gen-v.html',
    'paquete-alto-rendimiento.html',
    'paquete-bienestar-plus.html',
    'paquete-inicio-abundancia.html',
    'paquete-inicio-duo.html',
    'immunocal-landing-v4.html',
]

base_path = '/Users/martinmercedes/Desktop/Executive assistant 2/outputs/immunotec/'

mobile_override = """
    @media (max-width: 768px) {
      .sticky-btn-wrap { flex: 0 0 auto; }
      .btn-whatsapp-sticky { width: auto; min-width: 200px; max-width: 280px; }
    }"""

for filename in files:
    filepath = os.path.join(base_path, filename)
    if not os.path.exists(filepath):
        print(f"⚠️  {filename} — NOT FOUND")
        continue

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # Revert sticky-btn-wrap back to flex:1
    content = re.sub(
        r'(\.sticky-btn-wrap\s*\{[^}]*?)flex:\s*0 0 auto;',
        r'\1flex: 1;',
        content
    )

    # Revert btn-whatsapp-sticky back to width:100%
    content = re.sub(
        r'(\.btn-whatsapp-sticky\s*\{[^}]*?)width:\s*auto;\s*min-width:\s*200px;\s*max-width:\s*280px;',
        r'\1width: 100%;',
        content
    )

    # Add mobile override before </style> if not already present
    if 'max-width: 280px' not in content and mobile_override.strip() not in content:
        content = content.replace('  </style>', mobile_override + '\n  </style>', 1)

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ {filename}")
    else:
        print(f"⏭️  {filename} — NO CHANGES NEEDED")

print("\n✅ Done!")
