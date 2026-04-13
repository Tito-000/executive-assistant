#!/usr/bin/env python3
"""
Cambiar TODOS los eventos fbq de 'Lead' a 'Purchase' en los botones de WhatsApp
de todas las páginas de immuno-consult.com.

Además, agregar un script global que detecte cualquier click en links de WhatsApp
y dispare fbq('track','Purchase') automáticamente, como respaldo.
"""
import os
import re

base_path = '/Users/martinmercedes/Desktop/Executive assistant 2/outputs/immunotec/'

files = [
    'index.html',
    'immunocal-azul.html',
    'platinum.html',
    'immunocal-sport.html',
    'booster.html',
    'immunocal-optimizer.html',
    'magistral.html',
    'k-21-nutrik.html',
    'multi-resveratrol.html',
    'omega-gen-v.html',
    'paquete-alto-rendimiento.html',
    'paquete-bienestar-plus.html',
    'paquete-inicio-abundancia.html',
    'paquete-inicio-duo.html',
]

# Script global que captura TODOS los clicks de WhatsApp y dispara Purchase
purchase_script = """
  <!-- Purchase Event: dispara en cualquier click a WhatsApp -->
  <script>
  document.addEventListener('click', function(e) {
    var link = e.target.closest('a, button');
    if (!link) return;
    var href = link.getAttribute('href') || '';
    var onclick = link.getAttribute('onclick') || '';
    // Detectar links de WhatsApp o botones que abren WhatsApp
    if (href.indexOf('wa.me') !== -1 || href.indexOf('whatsapp') !== -1 || onclick.indexOf('wa.me') !== -1) {
      if (typeof fbq !== 'undefined') {
        fbq('track', 'Purchase');
      }
    }
  });
  // También capturar window.open de WhatsApp (formulario distribuidor)
  var originalOpen = window.open;
  window.open = function(url) {
    if (url && (url.indexOf('wa.me') !== -1 || url.indexOf('whatsapp') !== -1)) {
      if (typeof fbq !== 'undefined') {
        fbq('track', 'Purchase');
      }
    }
    return originalOpen.apply(this, arguments);
  };
  </script>
"""

changes_made = 0

for filename in files:
    filepath = os.path.join(base_path, filename)
    if not os.path.exists(filepath):
        print(f"⚠️  {filename} — NOT FOUND")
        continue

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content

    # 1. Cambiar todos los fbq Lead a Purchase en onclick de botones WhatsApp
    content = content.replace("fbq('track','Lead',", "fbq('track','Purchase',")
    content = content.replace('fbq("track","Lead",', 'fbq("track","Purchase",')
    content = content.replace("fbq('track', 'Lead',", "fbq('track', 'Purchase',")
    content = content.replace("fbq('track','Lead')", "fbq('track','Purchase')")
    content = content.replace("fbq('track', 'Lead')", "fbq('track', 'Purchase')")

    # 2. Agregar script global de Purchase antes del </body>
    if 'Purchase Event: dispara en cualquier click' not in content:
        content = content.replace('</body>', purchase_script + '\n</body>')

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        changes_made += 1
        print(f"✅ {filename} — actualizado")
    else:
        print(f"⏭️  {filename} — sin cambios")

print(f"\n✅ Done! {changes_made} archivos actualizados.")
