#!/usr/bin/env python3
"""
Remove the mobile-only media query we added. The button already looks good
on desktop with full width. The mobile override was making it too narrow.
"""
import os

files = [
    'magistral.html', 'platinum.html', 'booster.html', 'multi-resveratrol.html',
    'immunocal-azul.html', 'immunocal-sport.html', 'k-21-nutrik.html',
    'immunocal-optimizer.html', 'omega-gen-v.html', 'paquete-alto-rendimiento.html',
    'paquete-bienestar-plus.html', 'paquete-inicio-abundancia.html',
    'paquete-inicio-duo.html', 'immunocal-landing-v4.html',
]

base_path = '/Users/martinmercedes/Desktop/Executive assistant 2/outputs/immunotec/'

mobile_query = """
    @media (max-width: 768px) {
      .sticky-btn-wrap { flex: 0 0 auto; }
      .btn-whatsapp-sticky { width: auto; min-width: 200px; max-width: 260px; }
    }"""

for filename in files:
    filepath = os.path.join(base_path, filename)
    if not os.path.exists(filepath):
        print(f"⚠️  {filename} — NOT FOUND")
        continue

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if mobile_query in content:
        content = content.replace(mobile_query, '')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ {filename}")
    else:
        print(f"⏭️  {filename} — query not found")

print("\n✅ Done!")
