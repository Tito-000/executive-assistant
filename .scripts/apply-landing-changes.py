#!/usr/bin/env python3
"""
Apply sticky button and announcement bar changes to all landing pages.
Changes:
1. Move announcement bar OUTSIDE sticky-header (before it)
2. Update button text from "QUIERO EL MÍO — PAGO AL RECIBIR" to "QUIERO EL MÍO" + <span class="sticky-btn-sub">Pago al recibir</span>
3. Remove .sticky-sub-note <p> tags
4. Replace .sticky-sub-note CSS with .sticky-btn-sub CSS
5. Add flex-wrap: wrap to .btn-whatsapp-sticky
"""
import os
import re

files = [
    'platinum.html',
    'magistral.html',
    'booster.html',
    'multi-resveratrol.html',
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

    # Step 1: Move announcement bar OUTSIDE sticky-header
    # Pattern: <div id="sticky-header">[\n\s]*<!-- ══ 1. ANNOUNCEMENT BAR ══ -->[\n\s]*<div id="announcement-bar">...
    announcement_pattern = r'<div id="sticky-header">\s*<!-- ══ 1\. ANNOUNCEMENT BAR ══ -->\s*<div id="announcement-bar">([^<]*(?:<[^>]*>[^<]*)*?)</div>\s*<!-- ══ 2\. NAVIGATION ══ -->'
    match = re.search(announcement_pattern, content)
    if match:
        announcement_content = match.group(0).split('<!-- ══ 1. ANNOUNCEMENT BAR ══ -->')[1]
        announcement_content = announcement_content.split('<!-- ══ 2. NAVIGATION ══ -->')[0]

        # Remove announcement from inside sticky-header and add it before
        content = re.sub(
            r'<div id="sticky-header">\s*<!-- ══ 1\. ANNOUNCEMENT BAR ══ -->\s*<div id="announcement-bar">([^<]*(?:<[^>]*>[^<]*)*?)</div>\s*<!-- ══ 2\. NAVIGATION ══ -->',
            f'  <!-- ══ 1. ANNOUNCEMENT BAR ══ -->{announcement_content}  <!-- ══ 2. NAVIGATION ══ -->\n\n  <div id="sticky-header">',
            content
        )

    # Step 2: Update button text - find and replace the long button text with short version
    # Pattern: QUIERO EL MÍO — PAGO AL RECIBIR  with   QUIERO EL MÍO + <span>
    button_pattern = r'QUIERO EL MÍO — PAGO AL RECIBIR'
    if button_pattern in content:
        content = content.replace(
            button_pattern,
            'QUIERO EL MÍO\n          <span class="sticky-btn-sub">Pago al recibir</span>'
        )

    # Step 3: Remove <p class="sticky-sub-note">...</p> tags
    content = re.sub(
        r'\s*<p class="sticky-sub-note">[^<]*</p>',
        '',
        content
    )

    # Step 4: Replace .sticky-sub-note CSS rule with .sticky-btn-sub
    sticky_sub_note_pattern = r'\.sticky-sub-note\s*\{[^}]*\}'
    if re.search(sticky_sub_note_pattern, content):
        content = re.sub(
            sticky_sub_note_pattern,
            '.sticky-btn-sub { width:100%; text-align:center; font-size:10px; font-weight:400; opacity:0.6; margin-top:2px; }',
            content
        )

    # Step 5: Add flex-wrap: wrap to .btn-whatsapp-sticky if not already there
    if '.btn-whatsapp-sticky' in content and 'flex-wrap: wrap' not in content.split('.btn-whatsapp-sticky')[1].split('}')[0]:
        content = re.sub(
            r'(\.btn-whatsapp-sticky\s*\{[^}]*display:\s*flex;[^}]*gap:\s*8px;)',
            r'\1\n      flex-wrap: wrap;',
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
