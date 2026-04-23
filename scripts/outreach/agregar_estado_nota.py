"""Agrega columnas 'estado' y 'nota' editables a cada tab del Sheet.

Estados disponibles (validacion de datos en Sheets):
- Prospectos: NUEVO / INVESTIGADO / MENSAJE_LISTO / DESCARTADO
- En curso: ENVIADO / LLAMADO / AGENDADO / NO_RESPONDE / NO_INTERESA / FOLLOWUP
- Clientes: ACTIVO / PAUSADO / CANCELADO
- Archivados: (sin validacion)
"""

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

ESTADOS = {
    "Prospectos": ["NUEVO", "INVESTIGADO", "MENSAJE_LISTO", "DESCARTADO"],
    "En curso": ["ENVIADO", "LLAMADO", "AGENDADO", "NO_RESPONDE", "NO_INTERESA", "FOLLOWUP", "CERRADO"],
    "Clientes": ["ACTIVO", "PAUSADO", "CANCELADO"],
    "Archivados": [],
}


def col_letter(idx_0based):
    if idx_0based < 26:
        return chr(ord("A") + idx_0based)
    return chr(ord("A") + idx_0based // 26 - 1) + chr(ord("A") + idx_0based % 26)


def main():
    creds = Credentials.from_service_account_file(str(SERVICE_ACCOUNT_FILE), scopes=SCOPES)
    sh = gspread.authorize(creds).open_by_key(SHEET_ID)

    for tab_name in ["Prospectos", "En curso", "Clientes", "Archivados"]:
        ws = sh.worksheet(tab_name)
        headers = ws.row_values(1)

        if "estado" in headers and "nota" in headers:
            print(f"[{tab_name}] ya tiene estado+nota, skip")
            continue

        estado_col = len(headers)
        nota_col = len(headers) + 1
        nuevos_headers = headers + ["estado", "nota"]

        last_col = col_letter(nota_col)
        ws.update(range_name=f"A1:{last_col}1", values=[nuevos_headers])
        ws.format(f"{col_letter(estado_col)}1:{last_col}1", {
            "textFormat": {"bold": True, "foregroundColor": {"red": 1, "green": 1, "blue": 1}},
            "backgroundColor": {"red": 0.2, "green": 0.3, "blue": 0.5},
        })

        estado_col_letter = col_letter(estado_col)
        estado_range = f"{estado_col_letter}2:{estado_col_letter}1000"
        ws.format(estado_range, {
            "backgroundColor": {"red": 1, "green": 0.97, "blue": 0.85},
        })

        nota_col_letter = col_letter(nota_col)
        nota_range = f"{nota_col_letter}2:{nota_col_letter}1000"
        ws.format(nota_range, {
            "backgroundColor": {"red": 0.95, "green": 0.95, "blue": 1},
            "wrapStrategy": "WRAP",
        })

        opciones = ESTADOS.get(tab_name, [])
        if opciones:
            body = {
                "requests": [{
                    "setDataValidation": {
                        "range": {
                            "sheetId": ws.id,
                            "startRowIndex": 1,
                            "endRowIndex": 1000,
                            "startColumnIndex": estado_col,
                            "endColumnIndex": estado_col + 1,
                        },
                        "rule": {
                            "condition": {
                                "type": "ONE_OF_LIST",
                                "values": [{"userEnteredValue": v} for v in opciones],
                            },
                            "showCustomUi": True,
                            "strict": False,
                        },
                    }
                }]
            }
            sh.batch_update(body)

        print(f"[{tab_name}] agregado estado+nota (columnas {estado_col_letter} y {nota_col_letter}). Opciones: {opciones or 'libre'}")

    print("\nListo. Abre el Sheet para ver las columnas estado y nota editables.")
    print(f"URL: https://docs.google.com/spreadsheets/d/{SHEET_ID}")


if __name__ == "__main__":
    main()
