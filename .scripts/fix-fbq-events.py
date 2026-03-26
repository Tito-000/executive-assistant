#!/usr/bin/env python3
"""
Estandarizar todos los eventos fbq a 'Lead' en las páginas que usan 'Purchase'.
También corregir content_name genérico en immunocal-azul.html.
"""
import os

base_path = '/Users/martinmercedes/Desktop/Executive assistant 2/outputs/immunotec/'

# Páginas que usan Purchase → cambiar a Lead
purchase_to_lead = [
    'magistral.html',
    'immunocal-azul.html',
    'multi-resveratrol.html',
    'k-21-nutrik.html',
    'omega-gen-v.html',
    'immunocal-optimizer.html',
]

# Correcciones de content_name genérico en immunocal-azul.html
azul_content_names = [
    ("content_name:'nav_whatsapp'",          "content_name:'nav_whatsapp_immunocal_azul'"),
    ("content_name:'nav_mobile_whatsapp'",   "content_name:'nav_mobile_whatsapp_immunocal_azul'"),
    ("content_name:'hero-cta'",              "content_name:'hero-cta-immunocal_azul'"),
    ("content_name:'final-cta'",             "content_name:'final-cta-immunocal_azul'"),
    ("content_name:'sticky-bar'",            "content_name:'sticky-bar-immunocal_azul'"),
]

for filename in purchase_to_lead:
    filepath = os.path.join(base_path, filename)
    if not os.path.exists(filepath):
        print(f"⚠️  {filename} — NOT FOUND")
        continue

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    content = content.replace("fbq('track','Purchase',", "fbq('track','Lead',")

    # Corregir content_names genéricos en immunocal-azul
    if filename == 'immunocal-azul.html':
        for find, replace in azul_content_names:
            content = content.replace(find, replace)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ {filename}")
    else:
        print(f"⏭️  {filename} — no changes")

print("\n✅ Done!")
