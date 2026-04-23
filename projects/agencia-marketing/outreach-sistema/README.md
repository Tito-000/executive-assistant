# Sistema de Outreach MM Agency — Médicos RD

**Estado:** Fase 1 (Infraestructura) en construcción
**Inicio:** 2026-04-20
**Deadline piloto:** 2026-05-04 (14 días)
**Meta:** 5-6 clientes a $1,000/mes en 90 días (para cerrar gap hacia $8k/mes netos)

---

## Estrategia (resumen)

- **Nicho:** Clínicas de salud y estética en RD (dermatología, medicina estética, odontología estética, etc.)
- **Canales:** Instagram DM + Facebook Messenger (principales) + llamada telefónica 24h después
- **Tracking:** Google Sheets (NO GHL — decisión Martin 2026-04-20)
- **Mensajes:** Híper-personalizados, generados desde cero con Claude API por cada prospecto. Nunca plantilla genérica.
- **Envío:** Manual al inicio (copy-paste) para evitar baneo de IG/FB
- **Destino único:** Calendly de 20 min (llamada de diagnóstico)

Base estratégica: [`../WWP/WWP-mm-agency-outbound.md`](../WWP/WWP-mm-agency-outbound.md)
Plan operativo: [`~/.claude/plans/hagamos-uns-sitema-automatizado-snappy-key.md`](../../../../.claude/plans/hagamos-uns-sitema-automatizado-snappy-key.md)

---

## Google Sheet Operativo

- **URL:** https://docs.google.com/spreadsheets/d/1KTWFLgH2eDi-H-J7I1IFyr1p6pRxavp6FYI_kxRccjo
- **Owner:** martinmercedes100@gmail.com
- **Service account (bots):** mm-agency-sheets@mm-agency-493723.iam.gserviceaccount.com

### Tabs

| Tab | Propósito |
|-----|-----------|
| **Prospectos** | Lista raw con investigación (detalle_unico, gancho_humano, mensaje_listo) |
| **En curso** | Prospectos ya contactados — tracking de fecha_envio, canales, llamadas, respuestas |
| **Clientes** | Cerrados — pago setup, pago mensual, PayPal subscription |
| **Archivados** | Descartados por cualquier motivo |
| **Dashboard** | KPIs semanales + listas automáticas: Call list HOY, Sin contactar, Follow-up día 4/10 |

### Fórmulas clave del Dashboard

- **Call list HOY:** filtra de "En curso" los prospectos con `fecha_envio = ayer` y teléfono
- **Follow-up día 4:** prospectos con `fecha_envio = hace 4 días` sin respuesta ni agenda
- **Follow-up día 10:** prospectos con `fecha_envio = hace 10 días` sin respuesta ni agenda

---

## Scripts

| Script | Estado | Propósito |
|--------|--------|-----------|
| `scripts/outreach/crear_sheet_prospectos.py` | ✅ Listo | Crea/actualiza el Sheet con tabs y fórmulas |
| `scripts/outreach/limpiar_sheet1.py` | ✅ Listo | Elimina tab default tras crear |
| `scripts/outreach/investigar_prospecto.py` | ⏳ Por construir | Claude API lee IG + extrae detalles únicos |
| `scripts/outreach/componer_mensaje.py` | ⏳ Por construir | Compone mensajes híper-personalizados desde cero |
| `scripts/outreach/followup_composer.py` | ⏳ Por construir | Genera mensajes de follow-up diferentes al primero |

---

## Próximos pasos

**Esta semana (20-26 abr):**
- [x] Día 1-2: Google Sheet operativo con tabs y fórmulas
- [ ] Día 3-4: `investigar_prospecto.py` (Claude API + IG profile scraper)
- [ ] Día 5-7: `componer_mensaje.py` (Claude API compone desde cero usando WWP como guía)

**Semana 2 (27 abr - 4 may):**
- [ ] Día 8-9: Captura manual-asistida de 50 prospectos iniciales
- [ ] Día 10-12: Investigación + composición piloto
- [ ] Día 13: Envío del primer batch (10 prospectos)
- [ ] Día 14: Primera ronda de llamadas + **gate de decisión**

**Gate de decisión al día 14:**
- Si ≥1 agendó diagnóstico → escalar a 20/sem
- Si 0 agendaron → pausar y rehacer mensaje/hook

---

## KPIs (del WWP outbound, sección 9)

| Métrica | Meta |
|---------|------|
| Prospectos investigados/sem | 15-20 |
| Rastros enviados/sem | 15-20 |
| Llamadas realizadas/sem | 15-20 |
| Tasa de contacto efectivo (tel) | 40-60% |
| Reuniones agendadas/sem | 3-6 |
| Clientes cerrados/mes | 1-2 |
