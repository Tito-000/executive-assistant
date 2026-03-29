#!/usr/bin/env python3
"""
Make sticky button narrower - remove flex:1 from sticky-btn-wrap so button
doesn't stretch full width. Also adjust padding to be more compact.
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

for filename in files:
    filepath = os.path.join(base_path, filename)
    if not os.path.exists(filepath):
        print(f"⚠️  {filename} — NOT FOUND")
        continue

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # Replace flex:1 on sticky-btn-wrap to auto width
    content = re.sub(
        r'(\.sticky-btn-wrap\s*\{[^}]*?)flex:\s*1;',
        r'\1flex: 0 0 auto;',
        content
    )

    # Change btn-whatsapp-sticky width: 100% to auto and add min/max width
    content = re.sub(
        r'(\.btn-whatsapp-sticky\s*\{[^}]*?)width:\s*100%;',
        r'\1width: auto; min-width: 200px; max-width: 280px;',
        content
    )

    # Write back if changed
    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ {filename}")
    else:
        print(f"⏭️  {filename} — NO CHANGES NEEDED")

print("\n✅ Done!")
