#!/usr/bin/env python3
"""
Add mobile-only media query to make sticky button narrower on phones.
Desktop stays with flex:1 and width:100%.
Mobile gets flex:0 0 auto and max-width:260px.
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

mobile_query = '''
    @media (max-width: 768px) {
      .sticky-btn-wrap { flex: 0 0 auto; }
      .btn-whatsapp-sticky { width: auto; min-width: 200px; max-width: 260px; }
    }'''

for filename in files:
    filepath = os.path.join(base_path, filename)
    if not os.path.exists(filepath):
        print(f"⚠️  {filename} — NOT FOUND")
        continue

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if mobile override already exists
    if 'sticky-btn-wrap { flex: 0 0 auto' in content:
        print(f"⏭️  {filename} — ALREADY HAS MOBILE OVERRIDE")
        continue

    original_content = content

    # Add mobile override before </style>
    content = content.replace(
        '  </style>',
        mobile_query + '\n  </style>',
        1
    )

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ {filename}")
    else:
        print(f"⚠️  {filename} — COULD NOT MODIFY")

print("\n✅ Done!")
