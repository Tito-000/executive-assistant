"""Re-ordena cada hoja por prioridad para outreach.

Orden de prioridad (mas alto arriba):
  1. Tiene whatsapp_directo + @IG + nombre suena a doctor/doctora individual
  2. Tiene whatsapp_directo + @IG (clinica)
  3. Tiene whatsapp_directo
  4. Tiene @IG + telefono
  5. Solo telefono
  6. Sin datos utiles

Uso:
  python3 ordenar_por_decision_maker.py            # todas las hojas
  python3 ordenar_por_decision_maker.py --tab Estetica
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


def get_sheet():
    creds = Credentials.from_service_account_file(str(SERVICE_ACCOUNT_FILE), scopes=SCOPES)
    return gspread.authorize(creds).open_by_key(SHEET_ID)


def score(row):
    """Mas alto = mas prioridad. Score es tupla para ordenamiento estable."""
    nombre = row.get("nombre", "").lower()
    wa = row.get("whatsapp_directo", "")
    ig = row.get("ig", "")
    tel = row.get("telefono", "")
    email = row.get("email", "")

    # Detector: nombre suena a doctor/doctora individual (no clinica)
    is_individual = bool(re.search(r"^\s*(dr[a]?\.?|dra\.?)\s+", nombre)) or any(k in nombre for k in ["dr.", "dra.", "doctor", "doctora"])

    # Score compuesto
    s = 0
    if wa:
        s += 1000
    if ig:
        s += 500
    if is_individual:
        s += 300
    if email:
        s += 100
    if tel:
        s += 50
    # Mas completo = mas arriba
    filled = sum(1 for k in ["nombre", "ig", "fb", "telefono", "web", "email", "whatsapp_directo"] if row.get(k))
    s += filled * 10

    return -s  # negativo porque sorted es ascendente


def process_tab(sh, tab_name):
    ws = sh.worksheet(tab_name)
    headers = ws.row_values(1)
    rows = ws.get_all_records()

    if not rows:
        print(f"{tab_name}: vacio")
        return

    # Ordenar
    sorted_rows = sorted(rows, key=score)

    # Reescribir todo el contenido
    new_values = []
    for r in sorted_rows:
        new_values.append([r.get(h, "") for h in headers])

    # Limpia todo excepto header
    last_col = chr(ord("A") + len(headers) - 1)
    ws.batch_clear([f"A2:{last_col}{len(rows) + 1}"])
    if new_values:
        ws.update(range_name=f"A2:{last_col}{len(new_values) + 1}", values=new_values)

    # Stats
    with_wa = sum(1 for r in sorted_rows if r.get("whatsapp_directo"))
    with_ig = sum(1 for r in sorted_rows if r.get("ig"))
    individuales = sum(1 for r in sorted_rows if re.search(r"^\s*dr[a]?\.?\s+", r.get("nombre", "").lower()))

    print(f"{tab_name}: {len(rows)} filas ordenadas | WhatsApp: {with_wa} | IG: {with_ig} | Individuales: {individuales}")


def main():
    args = sys.argv[1:]
    specific_tab = None
    if "--tab" in args:
        specific_tab = args[args.index("--tab") + 1]

    sh = get_sheet()
    tabs_to_process = [specific_tab] if specific_tab else TABS

    for tab in tabs_to_process:
        try:
            process_tab(sh, tab)
        except gspread.WorksheetNotFound:
            print(f"  tab '{tab}' no existe, saltando")
        except Exception as e:
            print(f"  ERROR en {tab}: {type(e).__name__}: {e}")


if __name__ == "__main__":
    main()
