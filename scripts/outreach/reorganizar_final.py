"""Reorganiza TODAS las hojas de outreach para uso diario.

Cambios:
1. Nuevas columnas limpias (sin 'nota' con direccion, sin 'investigado' duplicado)
2. Estructura: PRIORIDAD | DATOS CONTACTO | TRACKING | IA
3. Dropdown de estado con colores
4. Congela header + columnas clave
5. Orden: decision makers con WhatsApp arriba
6. Dashboard resumen actualizado

Uso:
  python3 reorganizar_final.py
  python3 reorganizar_final.py --dry-run
"""

import re
import sys
from pathlib import Path

import gspread
from google.oauth2.service_account import Credentials

ROOT = Path(__file__).resolve().parents[2]
SERVICE_ACCOUNT_FILE = ROOT / "recursos-ia" / "api-keys" / "google-sheets-service-account.json"
SHEET_ID = (Path(__file__).parent / ".sheet_id").read_text().strip()

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

TABS = ["Estetica", "Ginecologia", "Dermatologia", "Odontologia", "Otros"]

# Nueva estructura de columnas — orden pensado para uso
NEW_HEADERS = [
    "prioridad",          # A — 🔥 ALTA / 🟡 MEDIA / ⚪ BAJA (auto por formula/import)
    "estado",             # B — NUEVO / CONTACTADO / LLAMADO / AGENDADO / CERRADO / DESCARTADO
    "nombre",             # C — decision maker o clinica
    "especialidad",       # D
    "ciudad",             # E
    "whatsapp_directo",   # F — NUMERO DEL DOCTOR (wa.me del bio IG)
    "ig",                 # G — @handle
    "fb",                 # H
    "telefono",           # I — tel recepcion Gmaps
    "email",              # J
    "web",                # K
    "seguidores_ig",      # L
    "direccion",          # M — movido desde 'nota'
    "fecha_contacto",     # N — dia que enviaste DM/email
    "canales_usados",     # O — IG / FB / Email / WA
    "fecha_llamada",      # P — dia que llamaste (WWP: cierre real)
    "resultado_llamada",  # Q — agendo / no contesta / no interesa / callback
    "nota_seguimiento",   # R — notas tuyas libres
    "texto_perfil",       # S — pegas bio+posts IG aqui para IA
    "ultimo_post",        # T — IA llena
    "detalle_unico",      # U — IA llena
    "gancho_humano",      # V — IA llena
    "mensaje_generado",   # W — SI/NO (auto cuando compones)
    "fuente",             # X — gmaps / sodocipre / etc
]

# Estados con colores (valor -> RGB)
ESTADOS = {
    "NUEVO":       {"red": 0.95, "green": 0.95, "blue": 0.95},  # gris claro
    "INVESTIGADO": {"red": 0.85, "green": 0.93, "blue": 1.00},  # azul claro
    "MENSAJE_LISTO": {"red": 1.00, "green": 0.95, "blue": 0.80}, # amarillo claro
    "CONTACTADO":  {"red": 0.80, "green": 0.88, "blue": 1.00},  # azul
    "LLAMADO":     {"red": 1.00, "green": 0.85, "blue": 0.70},  # naranja
    "AGENDADO":    {"red": 0.75, "green": 0.92, "blue": 0.75},  # verde claro
    "CERRADO":     {"red": 0.50, "green": 0.85, "blue": 0.55},  # verde fuerte
    "NO_RESPONDE": {"red": 0.90, "green": 0.90, "blue": 0.90},  # gris
    "NO_INTERESA": {"red": 0.95, "green": 0.80, "blue": 0.80},  # rojo claro
    "DESCARTADO":  {"red": 0.80, "green": 0.80, "blue": 0.80},  # gris oscuro
}

PRIORIDAD_COLORS = {
    "🔥 ALTA":  {"red": 1.00, "green": 0.75, "blue": 0.75},
    "🟡 MEDIA": {"red": 1.00, "green": 0.95, "blue": 0.80},
    "⚪ BAJA":  {"red": 0.95, "green": 0.95, "blue": 0.95},
}


def get_sheet():
    creds = Credentials.from_service_account_file(str(SERVICE_ACCOUNT_FILE), scopes=SCOPES)
    return gspread.authorize(creds).open_by_key(SHEET_ID)


def clasificar_prioridad(row):
    wa = str(row.get("whatsapp_directo", "") or "").strip()
    ig = str(row.get("ig", "") or "").strip()
    tel = str(row.get("telefono", "") or "").strip()
    nombre = str(row.get("nombre", "") or "").lower()

    es_doctor_individual = bool(re.search(r"^\s*(dra?\.?|doctora?)\s+", nombre))

    if wa and ig:
        return "🔥 ALTA"
    if wa or (ig and es_doctor_individual):
        return "🔥 ALTA"
    if ig and tel:
        return "🟡 MEDIA"
    if tel:
        return "🟡 MEDIA"
    return "⚪ BAJA"


def score_sort(row):
    """Para ordenar: prioridad alta arriba, luego completitud."""
    p_order = {"🔥 ALTA": 0, "🟡 MEDIA": 1, "⚪ BAJA": 2}.get(row.get("prioridad", ""), 3)
    completitud = sum(1 for k in ["whatsapp_directo", "ig", "telefono", "email", "fb", "web"] if row.get(k))
    return (p_order, -completitud, row.get("nombre", ""))


def transform_row(old_row):
    """Convierte fila vieja a nueva estructura."""
    # 'nota' antigua contenía dirección — muévela
    direccion = old_row.get("nota", "") or old_row.get("direccion", "")

    def s(v):
        return str(v) if v is not None else ""

    new = {
        "prioridad": "",  # se calcula despues
        "estado": s(old_row.get("estado")) or "NUEVO",
        "nombre": s(old_row.get("nombre")),
        "especialidad": s(old_row.get("especialidad")),
        "ciudad": s(old_row.get("ciudad")),
        "whatsapp_directo": s(old_row.get("whatsapp_directo")),
        "ig": s(old_row.get("ig")).lstrip("@"),
        "fb": s(old_row.get("fb")),
        "telefono": s(old_row.get("telefono")),
        "email": s(old_row.get("email")),
        "web": s(old_row.get("web")),
        "seguidores_ig": s(old_row.get("seguidores_ig")),
        "direccion": s(direccion),
        "fecha_contacto": "",
        "canales_usados": "",
        "fecha_llamada": "",
        "resultado_llamada": "",
        "nota_seguimiento": "",
        "texto_perfil": s(old_row.get("texto_perfil")),
        "ultimo_post": s(old_row.get("ultimo_post")),
        "detalle_unico": s(old_row.get("detalle_unico")),
        "gancho_humano": s(old_row.get("gancho_humano")),
        "mensaje_generado": "SI" if old_row.get("mensaje_listo") else "",
        "fuente": s(old_row.get("fuente")) or "gmaps",
    }
    new["prioridad"] = clasificar_prioridad(new)
    return new


def format_tab(ws, num_rows):
    """Aplica formato visual a una hoja."""
    total_cols = len(NEW_HEADERS)
    last_col_letter = chr(ord("A") + total_cols - 1) if total_cols <= 26 else "A" + chr(ord("A") + total_cols - 27)

    # Header con color fuerte
    ws.format(f"A1:{last_col_letter}1", {
        "textFormat": {
            "bold": True,
            "foregroundColor": {"red": 1, "green": 1, "blue": 1},
            "fontSize": 11,
        },
        "backgroundColor": {"red": 0.12, "green": 0.20, "blue": 0.40},
        "horizontalAlignment": "CENTER",
        "verticalAlignment": "MIDDLE",
    })

    # Congela header + primeras 3 cols (prioridad, estado, nombre)
    ws.freeze(rows=1, cols=3)

    # Anchos recomendados (aproximados)
    # prioridad 90, estado 110, nombre 250, esp 130, ciudad 110, wa 130, ig 140, fb 140,
    # tel 120, email 180, web 180, seg 80, direccion 250, fechas 100, canales 110,
    # resultado 130, nota 250, texto 200, ia fields 150, mensaje 90, fuente 100

    # Auto-resize: gspread no permite setear ancho directo en v6+, pero podemos ajustar con batch
    # Skipear anchos explicitos por simplicidad, quedan default

    # Validacion de datos (dropdown) para estado — columna B
    if num_rows > 0:
        try:
            ws.spreadsheet.batch_update({
                "requests": [{
                    "setDataValidation": {
                        "range": {
                            "sheetId": ws.id,
                            "startRowIndex": 1,
                            "endRowIndex": num_rows + 1,
                            "startColumnIndex": 1,  # estado = B
                            "endColumnIndex": 2,
                        },
                        "rule": {
                            "condition": {
                                "type": "ONE_OF_LIST",
                                "values": [{"userEnteredValue": e} for e in ESTADOS.keys()],
                            },
                            "showCustomUi": True,
                            "strict": True,
                        },
                    }
                }, {
                    "setDataValidation": {
                        "range": {
                            "sheetId": ws.id,
                            "startRowIndex": 1,
                            "endRowIndex": num_rows + 1,
                            "startColumnIndex": 0,  # prioridad = A
                            "endColumnIndex": 1,
                        },
                        "rule": {
                            "condition": {
                                "type": "ONE_OF_LIST",
                                "values": [{"userEnteredValue": p} for p in PRIORIDAD_COLORS.keys()],
                            },
                            "showCustomUi": True,
                            "strict": False,
                        },
                    }
                }]
            })
        except Exception as e:
            print(f"    validation warn: {e}")

    # Conditional formatting - estado con colores
    try:
        rules_requests = []
        for estado, color in ESTADOS.items():
            rules_requests.append({
                "addConditionalFormatRule": {
                    "rule": {
                        "ranges": [{
                            "sheetId": ws.id,
                            "startRowIndex": 1,
                            "startColumnIndex": 1,
                            "endColumnIndex": 2,
                        }],
                        "booleanRule": {
                            "condition": {
                                "type": "TEXT_EQ",
                                "values": [{"userEnteredValue": estado}],
                            },
                            "format": {
                                "backgroundColor": color,
                                "textFormat": {"bold": estado in ("AGENDADO", "CERRADO")},
                            },
                        },
                    },
                    "index": 0,
                }
            })
        # Prioridad con colores
        for prio, color in PRIORIDAD_COLORS.items():
            rules_requests.append({
                "addConditionalFormatRule": {
                    "rule": {
                        "ranges": [{
                            "sheetId": ws.id,
                            "startRowIndex": 1,
                            "startColumnIndex": 0,
                            "endColumnIndex": 1,
                        }],
                        "booleanRule": {
                            "condition": {
                                "type": "TEXT_EQ",
                                "values": [{"userEnteredValue": prio}],
                            },
                            "format": {
                                "backgroundColor": color,
                                "textFormat": {"bold": True},
                            },
                        },
                    },
                    "index": 0,
                }
            })
        ws.spreadsheet.batch_update({"requests": rules_requests})
    except Exception as e:
        print(f"    conditional format warn: {e}")

    # Wrap de texto para direccion y notas
    ws.format(f"M2:M{num_rows + 1}", {"wrapStrategy": "CLIP"})
    ws.format(f"R2:R{num_rows + 1}", {"wrapStrategy": "WRAP"})
    ws.format(f"S2:S{num_rows + 1}", {"wrapStrategy": "CLIP"})


def process_tab(sh, tab_name, dry_run=False):
    try:
        ws = sh.worksheet(tab_name)
    except gspread.WorksheetNotFound:
        print(f"{tab_name}: no existe, saltando")
        return

    old_rows = ws.get_all_records()
    if not old_rows:
        print(f"{tab_name}: vacio")
        return

    # Transformar
    new_rows = [transform_row(r) for r in old_rows]

    # Ordenar por prioridad
    new_rows.sort(key=score_sort)

    # Stats
    alta = sum(1 for r in new_rows if r["prioridad"] == "🔥 ALTA")
    media = sum(1 for r in new_rows if r["prioridad"] == "🟡 MEDIA")
    baja = sum(1 for r in new_rows if r["prioridad"] == "⚪ BAJA")
    wa = sum(1 for r in new_rows if r.get("whatsapp_directo"))
    print(f"{tab_name}: {len(new_rows)} | 🔥{alta} 🟡{media} ⚪{baja} | WhatsApp directo: {wa}")

    if dry_run:
        print(f"  DRY RUN — muestra top 3:")
        for r in new_rows[:3]:
            print(f"    {r['prioridad']} | {r['nombre'][:40]} | wa={r.get('whatsapp_directo','-')} | ig={r.get('ig','-')}")
        return

    # Limpiar hoja y reescribir con nuevo schema
    ws.clear()
    ws.update(range_name="A1", values=[NEW_HEADERS])

    # Batch write
    values = [[r.get(h, "") for h in NEW_HEADERS] for r in new_rows]
    if values:
        last_col_letter = chr(ord("A") + len(NEW_HEADERS) - 1)
        ws.update(range_name=f"A2:{last_col_letter}{len(values) + 1}", values=values)

    # Formato
    format_tab(ws, len(values))
    print(f"  {tab_name} reorganizado")


def update_dashboard(sh):
    """Dashboard con resumen ejecutivo."""
    try:
        ws = sh.worksheet("Dashboard")
    except gspread.WorksheetNotFound:
        ws = sh.add_worksheet(title="Dashboard", rows=50, cols=8)

    ws.clear()

    dashboard = [
        ["📊 DASHBOARD OUTREACH MM AGENCY", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["Especialidad", "Total leads", "🔥 ALTA", "WhatsApp directo", "Con IG", "Contactados", "Llamados", "Agendados"],
    ]

    for tab in TABS:
        try:
            wsx = sh.worksheet(tab)
            rows = wsx.get_all_records()
            total = len(rows)
            alta = sum(1 for r in rows if "ALTA" in (r.get("prioridad") or ""))
            wa = sum(1 for r in rows if r.get("whatsapp_directo"))
            ig = sum(1 for r in rows if r.get("ig"))
            cont = sum(1 for r in rows if (r.get("estado") or "") in ("CONTACTADO", "LLAMADO", "AGENDADO", "CERRADO"))
            llam = sum(1 for r in rows if (r.get("estado") or "") in ("LLAMADO", "AGENDADO", "CERRADO"))
            ag = sum(1 for r in rows if (r.get("estado") or "") in ("AGENDADO", "CERRADO"))
            dashboard.append([tab, total, alta, wa, ig, cont, llam, ag])
        except Exception:
            dashboard.append([tab, "-", "-", "-", "-", "-", "-", "-"])

    dashboard.extend([
        ["", "", "", "", "", "", "", ""],
        ["🎯 PROCESO DE OUTREACH:", "", "", "", "", "", "", ""],
        ["1. Filtra por prioridad 🔥 ALTA (arriba de cada hoja)", "", "", "", "", "", "", ""],
        ["2. Abre IG del prospecto y pega bio+posts en 'texto_perfil'", "", "", "", "", "", "", ""],
        ["3. Corre: python3 scripts/outreach/investigar_prospecto.py @ig", "", "", "", "", "", "", ""],
        ["4. Corre: python3 scripts/outreach/componer_mensaje.py @ig", "", "", "", "", "", "", ""],
        ["5. Envia DMs manuales + email, marca estado CONTACTADO y fecha_contacto", "", "", "", "", "", "", ""],
        ["6. Al dia siguiente: llama al whatsapp_directo, marca estado LLAMADO", "", "", "", "", "", "", ""],
        ["", "", "", "", "", "", "", ""],
        ["💡 PRIORIDADES:", "", "", "", "", "", "", ""],
        ["🔥 ALTA = tiene WhatsApp directo O es doctor(a) individual con IG", "", "", "", "", "", "", ""],
        ["🟡 MEDIA = tiene IG o telefono de clinica", "", "", "", "", "", "", ""],
        ["⚪ BAJA = solo datos basicos", "", "", "", "", "", "", ""],
    ])

    ws.update(range_name="A1", values=dashboard)
    ws.format("A1:H1", {
        "textFormat": {"bold": True, "fontSize": 14, "foregroundColor": {"red": 1, "green": 1, "blue": 1}},
        "backgroundColor": {"red": 0.12, "green": 0.20, "blue": 0.40},
        "horizontalAlignment": "CENTER",
    })
    ws.format("A3:H3", {
        "textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}},
        "backgroundColor": {"red": 0.25, "green": 0.35, "blue": 0.55},
    })
    ws.merge_cells("A1:H1")
    ws.freeze(rows=3)
    print("Dashboard actualizado")


def main():
    dry_run = "--dry-run" in sys.argv

    sh = get_sheet()
    for tab in TABS:
        try:
            process_tab(sh, tab, dry_run=dry_run)
        except Exception as e:
            print(f"  ERROR en {tab}: {type(e).__name__}: {e}")

    if not dry_run:
        update_dashboard(sh)

    print(f"\nSheet: https://docs.google.com/spreadsheets/d/{SHEET_ID}")


if __name__ == "__main__":
    main()
