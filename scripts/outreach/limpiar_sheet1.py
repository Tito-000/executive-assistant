"""Elimina el tab 'Hoja 1' / 'Sheet1' default si existe."""

import json
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

creds = Credentials.from_service_account_file(str(SERVICE_ACCOUNT_FILE), scopes=SCOPES)
sh = gspread.authorize(creds).open_by_key(SHEET_ID)

tabs = [ws.title for ws in sh.worksheets()]
print(f"Tabs actuales: {tabs}")

for name in ["Sheet1", "Hoja 1", "Hoja1"]:
    if name in tabs:
        try:
            sh.del_worksheet(sh.worksheet(name))
            print(f"  Eliminado: {name}")
        except Exception as e:
            print(f"  Error eliminando {name}: {e}")
