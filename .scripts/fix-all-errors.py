#!/usr/bin/env python3
"""
Fix all critical, moderate, and minor errors found in the audit.
"""
import os
import re

base_path = '/Users/martinmercedes/Desktop/Executive assistant 2/outputs/immunotec/'

files_to_fix = {
    'magistral.html': [
        # Fix sticky bar price — change from RD$5,500/RD$4,400 to RD$7,000/RD$3,495
        {
            'find': r'<div class="sticky-price-old">RD\$5,500</div>\s*<div class="sticky-price-new">RD\$4,400</div>',
            'replace': '<div class="sticky-price-old">RD$7,000</div>\n    <div class="sticky-price-new">RD$3,495</div>',
            'note': 'Fix sticky bar price to match hero'
        },
        # Fix ahorro RD$3,495 → RD$3,505
        {
            'find': 'Ahorras RD\\$3,495',
            'replace': 'Ahorras RD$3,505',
            'note': 'Fix incorrect savings amount',
            'replace_all': True
        },
        # Fix content_name platinum → magistral in nav buttons
        {
            'find': "content_name:'nav_whatsapp_platinum'",
            'replace': "content_name:'nav_whatsapp_magistral'",
            'note': 'Fix nav fbq content_name'
        },
        {
            'find': "content_name:'nav_mobile_whatsapp_platinum'",
            'replace': "content_name:'nav_mobile_whatsapp_magistral'",
            'note': 'Fix mobile nav fbq content_name'
        }
    ],
    'booster.html': [
        # Fix content_name platinum → booster in nav buttons
        {
            'find': "content_name:'nav_whatsapp_platinum'",
            'replace': "content_name:'nav_whatsapp_booster'",
            'note': 'Fix nav fbq content_name'
        },
        {
            'find': "content_name:'nav_mobile_whatsapp_platinum'",
            'replace': "content_name:'nav_mobile_whatsapp_booster'",
            'note': 'Fix mobile nav fbq content_name'
        }
        # Note: vs.png issue is visual, not code — would need design decision from Martin
    ],
    'multi-resveratrol.html': [
        # Fix "seras" → "serás"
        {
            'find': 'Al hacer clic seras dirigido a WhatsApp',
            'replace': 'Al hacer clic serás dirigido a WhatsApp',
            'note': 'Fix typo: seras → serás',
            'replace_all': True
        },
        # Fix "QUIERO EL MIO" → "QUIERO EL MÍO"
        {
            'find': 'QUIERO EL MIO — PAGO AL RECIBIR',
            'replace': 'QUIERO EL MÍO — PAGO AL RECIBIR',
            'note': 'Fix accent on MÍO in sticky button',
            'replace_all': True
        }
    ],
    'k-21-nutrik.html': [
        # Fix "seras" → "serás"
        {
            'find': 'Al hacer clic seras dirigido a WhatsApp',
            'replace': 'Al hacer clic serás dirigido a WhatsApp',
            'note': 'Fix typo: seras → serás',
            'replace_all': True
        },
        # Fix "QUIERO EL MIO" → "QUIERO EL MÍO"
        {
            'find': 'QUIERO EL MIO — PAGO AL RECIBIR',
            'replace': 'QUIERO EL MÍO — PAGO AL RECIBIR',
            'note': 'Fix accent on MÍO in sticky button',
            'replace_all': True
        }
    ],
    'omega-gen-v.html': [
        # Fix "seras" → "serás"
        {
            'find': 'Al hacer clic seras dirigido a WhatsApp',
            'replace': 'Al hacer clic serás dirigido a WhatsApp',
            'note': 'Fix typo: seras → serás',
            'replace_all': True
        },
        # Fix "QUIERO EL MIO" → "QUIERO EL MÍO"
        {
            'find': 'QUIERO EL MIO — PAGO AL RECIBIR',
            'replace': 'QUIERO EL MÍO — PAGO AL RECIBIR',
            'note': 'Fix accent on MÍO in sticky button',
            'replace_all': True
        }
    ],
    'paquete-bienestar-plus.html': [
        # Fix H1 desktop "8 productos premium" → "10 productos premium"
        {
            'find': '<span class="h1-blue">8 productos premium</span>',
            'replace': '<span class="h1-blue">10 productos premium</span>',
            'note': 'Fix H1 desktop product count'
        },
        # Fix meta description "8 productos" → "10 productos"
        {
            'find': '8 productos premium con 42% OFF',
            'replace': '10 productos premium con 42% OFF',
            'note': 'Fix meta description product count',
            'replace_all': True
        }
    ],
    'paquete-inicio-abundancia.html': [
        # Fix H1 desktop "8 productos premium" → "6 cajas de los más vendidos"
        {
            'find': '<span class="h1-blue">8 productos premium</span>',
            'replace': '<span class="h1-blue">6 cajas de los más vendidos</span>',
            'note': 'Fix H1 desktop'
        },
        # Fix meta description
        {
            'find': '8 productos premium con 35% OFF',
            'replace': '6 cajas de los más vendidos con 35% OFF',
            'note': 'Fix meta description',
            'replace_all': True
        }
    ],
    'paquete-inicio-duo.html': [
        # Fix H1 desktop "8 productos premium" → "6 productos esenciales"
        {
            'find': '<span class="h1-blue">8 productos premium</span>',
            'replace': '<span class="h1-blue">6 productos esenciales</span>',
            'note': 'Fix H1 desktop'
        },
        # Fix meta description
        {
            'find': '8 productos premium con 35% OFF',
            'replace': '6 productos esenciales con 35% OFF',
            'note': 'Fix meta description',
            'replace_all': True
        }
    ],
    'immunocal-landing-v4.html': [
        # Add product name to all fbq content_name values
        {
            'find': "content_name:'nav_whatsapp'",
            'replace': "content_name:'nav_whatsapp_immunocal_azul'",
            'note': 'Add product name to fbq tracking'
        },
        {
            'find': "content_name:'nav_mobile_whatsapp'",
            'replace': "content_name:'nav_mobile_whatsapp_immunocal_azul'",
            'note': 'Add product name to mobile fbq'
        },
        {
            'find': "content_name:'hero-cta'",
            'replace': "content_name:'hero-cta-immunocal_azul'",
            'note': 'Add product name to hero fbq'
        },
        {
            'find': "content_name:'final-cta'",
            'replace': "content_name:'final-cta-immunocal_azul'",
            'note': 'Add product name to final CTA fbq'
        },
        {
            'find': "content_name:'sticky-bar'",
            'replace': "content_name:'sticky-bar-immunocal_azul'",
            'note': 'Add product name to sticky fbq'
        }
    ]
}

# Apply fixes
for filename, fixes in files_to_fix.items():
    filepath = os.path.join(base_path, filename)
    if not os.path.exists(filepath):
        print(f"⚠️  {filename} — NOT FOUND")
        continue

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    applied_count = 0

    for fix in fixes:
        find_text = fix['find']
        replace_text = fix['replace']
        is_replace_all = fix.get('replace_all', False)

        if is_replace_all:
            if find_text in content:
                content = content.replace(find_text, replace_text)
                applied_count += 1
        else:
            if re.search(find_text, content):
                content = re.sub(find_text, replace_text, content, count=1)
                applied_count += 1

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ {filename} — {applied_count} fix(es) applied")
    else:
        print(f"⏭️  {filename} — no changes")

print("\n✅ All fixes applied!")
