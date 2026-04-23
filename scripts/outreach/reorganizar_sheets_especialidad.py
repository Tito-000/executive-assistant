"""Reorganiza el Sheet: crea una hoja por especialidad y migra los 227 leads existentes.

Hojas destino:
  - Estetica (medicina estetica + cirugia plastica + clinicas esteticas)
  - Ginecologia
  - Dermatologia
  - Odontologia
  - Otros

Mantiene 'En curso', 'Clientes', 'Archivados', 'Dashboard'.
La hoja 'Prospectos' original se renombra a 'Prospectos_Archivo' para no perder data.
"""

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

ESPECIALIDADES = [
    "Estetica",
    "Ginecologia",
    "Dermatologia",
    "Odontologia",
    "Otros",
]

HEADERS = [
    "id", "nombre", "especialidad", "ciudad", "ig", "fb", "telefono", "web",
    "email", "whatsapp_directo", "seguidores_ig", "fuente", "texto_perfil",
    "ultimo_post", "detalle_unico", "gancho_humano", "investigado",
    "mensaje_listo", "estado", "nota"
]


def get_sheet():
    creds = Credentials.from_service_account_file(str(SERVICE_ACCOUNT_FILE), scopes=SCOPES)
    return gspread.authorize(creds).open_by_key(SHEET_ID)


def clasificar(esp):
    esp = (esp or "").lower().strip()
    if any(k in esp for k in ["ginec", "gyn", "obstetri"]):
        return "Ginecologia"
    if "derma" in esp:
        return "Dermatologia"
    if any(k in esp for k in ["odonto", "dental"]):
        return "Odontologia"
    if any(k in esp for k in ["estet", "plastic", "lipo", "cirug"]):
        return "Estetica"
    return "Otros"


def main():
    sh = get_sheet()

    # 1. Renombrar Prospectos -> Prospectos_Archivo (backup)
    existing = {ws.title: ws for ws in sh.worksheets()}
    if "Prospectos" in existing and "Prospectos_Archivo" not in existing:
        existing["Prospectos"].update_title("Prospectos_Archivo")
        print("Renombrado: Prospectos -> Prospectos_Archivo (backup)")
        existing = {ws.title: ws for ws in sh.worksheets()}

    # 2. Leer datos viejos
    ws_old = existing.get("Prospectos_Archivo")
    old_rows = ws_old.get_all_records() if ws_old else []
    old_headers = ws_old.row_values(1) if ws_old else []
    print(f"Leyendo {len(old_rows)} leads del archivo...")

    # 3. Crear tabs por especialidad con headers
    for esp in ESPECIALIDADES:
        if esp in existing:
            print(f"  Tab '{esp}' ya existe (saltando creacion)")
            continue
        ws = sh.add_worksheet(title=esp, rows=1000, cols=len(HEADERS))
        ws.update(range_name="A1", values=[HEADERS])
        ws.format(f"A1:{chr(ord('A')+len(HEADERS)-1)}1", {
            "textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}},
            "backgroundColor": {"red": 0.2, "green": 0.3, "blue": 0.5},
        })
        ws.freeze(rows=1)
        print(f"  Tab '{esp}' creado")

    # 4. Refrescar existing
    existing = {ws.title: ws for ws in sh.worksheets()}

    # 5. Clasificar y repartir
    buckets = {esp: [] for esp in ESPECIALIDADES}
    for r in old_rows:
        bucket = clasificar(r.get("especialidad", ""))
        row_data = []
        for h in HEADERS:
            if h == "fuente":
                row_data.append("gmaps")
            else:
                row_data.append(r.get(h, ""))
        buckets[bucket].append(row_data)

    # 6. Escribir a cada tab
    for esp, rows in buckets.items():
        ws = existing[esp]
        if rows:
            ws.append_rows(rows, value_input_option="USER_ENTERED")
        print(f"  {esp}: {len(rows)} leads migrados")

    print("\nListo. Abre el Sheet y verifica que las pestanas tengan los leads correctos.")
    print(f"Sheet: https://docs.google.com/spreadsheets/d/{SHEET_ID}")


if __name__ == "__main__":
    main()
