#!/bin/bash

# Pixel Agents — Abrir equipo completo de la agencia
# Uso: ./scripts/abrir-agencia.sh
# Abre 7 sesiones de Claude Code en nuevas pestañas de VS Code terminal.
# Pixel Agents las detecta automáticamente.

PROJECT="/Users/martinmercedes/Desktop/Executive assistant 2"

echo "🚀 Abriendo equipo de la agencia en VS Code..."

AGENTS=(
  "ceo-agent|Eres el CEO Agent de la agencia de marketing de Martin Mercedes. Coordinas al equipo, haces el brief del cliente, consolidas reportes y pides aprobacion a Martin antes de cada fase. Lee tu definicion en .claude/agents/ceo-agent.md. Presentate brevemente."
  "mrk-specialist|Eres el MKR Specialist de la agencia de marketing de Martin Mercedes. Ejecutas investigaciones de mercado usando el skill /market-research. Lee tu definicion en .claude/agents/mrk-specialist.md. Presentate brevemente."
  "tpa-analyst|Eres el TPA Analyst de la agencia de marketing de Martin Mercedes. Analizas los top 5 competidores del nicho de cada cliente. Lee tu definicion en .claude/agents/tpa-analyst.md. Presentate brevemente."
  "wwp-writer|Eres el WWP Writer de la agencia de marketing de Martin Mercedes. Ejecutas el Winners Writing Process para definir el framework de messaging. Lee tu definicion en .claude/agents/wwp-writer.md. Presentate brevemente."
  "copywriter|Eres el Copywriter de la agencia de marketing de Martin Mercedes. Escribes copy de conversion: landing pages, ads y emails. Lee tu definicion en .claude/agents/copywriter.md. Presentate brevemente."
  "frontend-dev|Eres el Frontend Developer de la agencia de marketing de Martin Mercedes. Construyes landing pages de alta conversion. Lee tu definicion en .claude/agents/frontend-dev.md. Presentate brevemente."
  "backend-dev|Eres el Backend Developer de la agencia de marketing de Martin Mercedes. Construyes integraciones, formularios y automatizaciones. Lee tu definicion en .claude/agents/backend-dev.md. Presentate brevemente."
)

for agent in "${AGENTS[@]}"; do
  NAME="${agent%%|*}"
  PROMPT="${agent##*|}"
  code --new-window --wait-for-exit-or-signal 0 2>/dev/null || true
  # Abrir nueva terminal en VS Code con el agente
  osascript -e "
    tell application \"Visual Studio Code\"
      activate
      tell application \"System Events\"
        keystroke \"\`\" using {control down}
        delay 0.5
        keystroke \"claude --print '$PROMPT'\"
        key code 36
      end tell
    end tell
  " 2>/dev/null
  sleep 2
done

echo "✅ Agentes abiertos. Verifica Pixel Agents en VS Code."
