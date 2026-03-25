#!/bin/bash
# sync-netlify.sh — Sincroniza todas las páginas y sus imágenes locales a netlify-azul/
# Uso: bash scripts/sync-netlify.sh

set -e

SRC="outputs/immunotec"
DEST="outputs/immunotec/netlify-azul"

echo "🔄 Sincronizando páginas a netlify-azul/..."

# 1. Copiar todos los HTML de outputs/immunotec/ a netlify-azul/
# (excepto versiones viejas como v1, v2, v3, v4)
for html in "$SRC"/*.html; do
  filename=$(basename "$html")
  # Saltar versiones antiguas
  if [[ "$filename" =~ -v[0-9]+\.html$ ]]; then
    echo "  ⏭  Saltando versión vieja: $filename"
    continue
  fi
  cp "$html" "$DEST/$filename"
  echo "  ✅ $filename"
done

# 2. Detectar todas las imágenes locales referenciadas en los HTML
echo ""
echo "🔍 Buscando imágenes locales referenciadas..."

MISSING=0
COPIED=0

for html in "$DEST"/*.html; do
  # Extraer src="..." que NO empiecen con http o data:
  grep -oP 'src="(?!https?://|data:)[^"]+' "$html" 2>/dev/null | sed 's/src="//' | while read -r img; do
    # Ruta completa en destino
    img_dest="$DEST/$img"

    if [ ! -f "$img_dest" ]; then
      # Buscar en outputs/immunotec/
      img_src="$SRC/$img"
      if [ -f "$img_src" ]; then
        # Crear subdirectorio si es necesario
        mkdir -p "$(dirname "$img_dest")"
        cp "$img_src" "$img_dest"
        echo "  📷 Copiado: $img"
      else
        # Buscar en todo el proyecto
        found=$(find . -name "$(basename "$img")" -not -path "*/node_modules/*" -not -path "*/.next/*" -print -quit 2>/dev/null)
        if [ -n "$found" ]; then
          mkdir -p "$(dirname "$img_dest")"
          cp "$found" "$img_dest"
          echo "  📷 Encontrado y copiado: $img (desde $found)"
        else
          echo "  ❌ FALTANTE: $img (referenciado en $(basename "$html"))"
        fi
      fi
    fi
  done
done

echo ""
echo "✅ Sync completo. Folder listo para deploy:"
echo "   $DEST/"
echo ""
echo "📊 Contenido:"
echo "   HTMLs: $(ls "$DEST"/*.html 2>/dev/null | wc -l | tr -d ' ')"
echo "   Imágenes: $(find "$DEST" -type f \( -name '*.png' -o -name '*.jpg' -o -name '*.webp' -o -name '*.gif' -o -name '*.svg' -o -name '*.avif' \) | wc -l | tr -d ' ')"
echo ""
echo "🚀 Arrastra la carpeta netlify-azul/ a Netlify para deployar."
