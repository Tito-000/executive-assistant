#!/usr/bin/env python3
"""
Hacer el script global de Purchase más estricto:
- SOLO dispara en links que contengan 'wa.me' en el href
- NO captura window.open (para evitar falsos positivos)
- Elimina duplicados
"""
import os

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

# Script anterior (a reemplazar)
old_script = """
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

# Script nuevo (más estricto)
new_script = """
  <!-- Purchase Event: SOLO dispara en click a links wa.me -->
  <script>
  document.addEventListener('click', function(e) {
    var link = e.target.closest('a');
    if (!link) return;
    var href = link.getAttribute('href') || '';
    if (href.indexOf('wa.me/') !== -1) {
      if (typeof fbq !== 'undefined') {
        fbq('track', 'Purchase');
      }
    }
  });
  </script>
"""

changes = 0
for filename in files:
    filepath = os.path.join(base_path, filename)
    if not os.path.exists(filepath):
        print(f"⚠️  {filename} — NOT FOUND")
        continue

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original = content
    content = content.replace(old_script, new_script)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        changes += 1
        print(f"✅ {filename}")
    else:
        print(f"⏭️  {filename} — sin cambios")

print(f"\n✅ Done! {changes} archivos actualizados.")
