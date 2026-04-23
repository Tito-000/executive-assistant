"""Crea el Google Sheet 'Prospectos Medicos RD' con tabs, columnas y formulas.

Uso: python3 crear_sheet_prospectos.py

Si el Sheet ya existe (marcado en .sheet_id), no lo recrea. Para forzar nuevo: borra .sheet_id.
"""

import json
import sys
from pathlib import Path

import gspread
from google.oauth2.service_account import Credentials

ROOT = Path(__file__).resolve().parents[2]
SERVICE_ACCOUNT_FILE = ROOT / "recursos-ia" / "api-keys" / "google-sheets-service-account.json"
SHEET_ID_FILE = Path(__file__).parent / ".sheet_id"

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

SHEET_NAME = "Prospectos Medicos RD - MM Agency"
OWNER_EMAIL = "martinmercedes100@gmail.com"

TABS = {
    "Prospectos": [
        "id", "nombre", "especialidad", "ciudad", "ig", "fb", "telefono", "web", "email",
        "seguidores_ig", "ultimo_post", "detalle_unico", "gancho_humano",
        "investigado", "mensaje_listo",
    ],
    "En curso": [
        "id", "nombre", "ig", "fb", "telefono", "ciudad",
        "fecha_envio", "canales_usados",
        "dia_llamada", "estado_llamada",
        "respondio_dm", "agendado_diagnostico", "fecha_diagnostico",
        "followup_dia4", "followup_dia10",
        "notas",
    ],
    "Clientes": [
        "id", "nombre", "ig", "telefono", "ciudad",
        "fecha_cierre", "pago_setup_usd", "pago_mensual_usd",
        "paypal_subscription_id", "notas",
    ],
    "Archivados": [
        "id", "nombre", "ig", "motivo_archivo", "fecha_archivo", "notas",
    ],
    "Dashboard": [],
}


def get_client():
    creds = Credentials.from_service_account_file(str(SERVICE_ACCOUNT_FILE), scopes=SCOPES)
    return gspread.authorize(creds)


def build_dashboard(ws):
    ws.update(range_name="A1", values=[["DASHBOARD OUTREACH MM AGENCY - MEDICOS RD"]])
    ws.format("A1", {"textFormat": {"bold": True, "fontSize": 14}})

    ws.update(range_name="A3", values=[["KPIs Semana Actual (desde WWP outbound)"]])
    ws.format("A3", {"textFormat": {"bold": True, "fontSize": 12}})

    kpis = [
        ["Metrica", "Valor", "Meta"],
        ['Prospectos investigados (total)', '=COUNTA(Prospectos!A2:A)-COUNTIF(Prospectos!N2:N,"")', 15],
        ['Rastros enviados (total)', '=COUNTA(\'En curso\'!G2:G)-COUNTIF(\'En curso\'!G2:G,"")', 15],
        ['Llamadas realizadas', '=COUNTA(\'En curso\'!J2:J)-COUNTIF(\'En curso\'!J2:J,"")', 15],
        ['Respondieron DM', '=COUNTIF(\'En curso\'!K2:K,"SI")', 6],
        ['Agendaron diagnostico', '=COUNTIF(\'En curso\'!L2:L,"SI")', 3],
        ['Clientes cerrados', '=COUNTA(Clientes!A2:A)-1', 1],
    ]
    ws.update(range_name="A5", values=kpis, value_input_option="USER_ENTERED")
    ws.format("A5:C5", {"textFormat": {"bold": True}, "backgroundColor": {"red": 0.9, "green": 0.9, "blue": 0.9}})

    ws.update(range_name="A14", values=[["Call list HOY (prospectos enviados ayer con telefono)"]])
    ws.format("A14", {"textFormat": {"bold": True, "fontSize": 12}})

    call_list_headers = [["nombre", "telefono", "ciudad", "canales_usados", "fecha_envio"]]
    ws.update(range_name="A15", values=call_list_headers)
    ws.format("A15:E15", {"textFormat": {"bold": True}, "backgroundColor": {"red": 0.95, "green": 0.88, "blue": 0.7}})

    call_formula = (
        '=QUERY(\'En curso\'!B2:O, '
        '"select B,E,F,H,G where G=date \'"&TEXT(TODAY()-1,"yyyy-mm-dd")&"\' and E is not null", 0)'
    )
    ws.update(range_name="A16", values=[[call_formula]], value_input_option="USER_ENTERED")

    ws.update(range_name="A30", values=[["Sin contactar (tienen mensaje listo pero no se ha enviado)"]])
    ws.format("A30", {"textFormat": {"bold": True, "fontSize": 12}})
    sin_contactar_headers = [["nombre", "ig", "ciudad", "especialidad"]]
    ws.update(range_name="A31", values=sin_contactar_headers)
    ws.format("A31:D31", {"textFormat": {"bold": True}, "backgroundColor": {"red": 0.88, "green": 0.95, "blue": 0.88}})

    sin_contactar_formula = (
        '=QUERY(Prospectos!A2:O, '
        '"select B,E,D,C where O=\'SI\' and A is not null", 0)'
    )
    ws.update(range_name="A32", values=[[sin_contactar_formula]], value_input_option="USER_ENTERED")

    ws.update(range_name="A45", values=[["Follow-up DIA 4 (enviados hace 4 dias sin respuesta)"]])
    ws.format("A45", {"textFormat": {"bold": True, "fontSize": 12}})
    ws.update(range_name="A46", values=[["nombre", "ig", "fecha_envio"]])
    fu4 = (
        '=QUERY(\'En curso\'!B2:O, '
        '"select B,C,G where G=date \'"&TEXT(TODAY()-4,"yyyy-mm-dd")&"\' and K is null and L is null", 0)'
    )
    ws.update(range_name="A47", values=[[fu4]], value_input_option="USER_ENTERED")

    ws.update(range_name="A58", values=[["Follow-up DIA 10 (enviados hace 10 dias sin respuesta)"]])
    ws.format("A58", {"textFormat": {"bold": True, "fontSize": 12}})
    ws.update(range_name="A59", values=[["nombre", "ig", "fecha_envio"]])
    fu10 = (
        '=QUERY(\'En curso\'!B2:O, '
        '"select B,C,G where G=date \'"&TEXT(TODAY()-10,"yyyy-mm-dd")&"\' and K is null and L is null", 0)'
    )
    ws.update(range_name="A60", values=[[fu10]], value_input_option="USER_ENTERED")


def main():
    if not SERVICE_ACCOUNT_FILE.exists():
        print(f"ERROR: no existe {SERVICE_ACCOUNT_FILE}")
        sys.exit(1)

    with open(SERVICE_ACCOUNT_FILE) as f:
        sa = json.load(f)
    service_email = sa["client_email"]
    print(f"Service account: {service_email}")

    client = get_client()

    if SHEET_ID_FILE.exists():
        sheet_id = SHEET_ID_FILE.read_text().strip()
        print(f"Sheet ya existe (id={sheet_id}). Para recrear, borra .sheet_id")
        sh = client.open_by_key(sheet_id)
    else:
        print(f"Creando Sheet '{SHEET_NAME}'...")
        sh = client.create(SHEET_NAME)
        SHEET_ID_FILE.write_text(sh.id)
        print(f"Creado. ID: {sh.id}")

        print(f"Compartiendo con {OWNER_EMAIL} como editor...")
        sh.share(OWNER_EMAIL, perm_type="user", role="writer", notify=True)

    existing_tabs = [ws.title for ws in sh.worksheets()]

    for tab_name, columns in TABS.items():
        if tab_name in existing_tabs:
            print(f"  Tab '{tab_name}' ya existe, saltando")
            continue

        print(f"  Creando tab '{tab_name}'...")
        rows = 1000 if tab_name != "Dashboard" else 100
        cols = max(len(columns), 10)
        ws = sh.add_worksheet(title=tab_name, rows=rows, cols=cols)

        if tab_name == "Dashboard":
            build_dashboard(ws)
        else:
            ws.update(range_name="A1", values=[columns])
            header_range = f"A1:{chr(ord('A') + len(columns) - 1)}1"
            ws.format(header_range, {
                "textFormat": {"bold": True},
                "backgroundColor": {"red": 0.2, "green": 0.3, "blue": 0.5},
            })
            ws.format(header_range, {"textFormat": {"foregroundColor": {"red": 1, "green": 1, "blue": 1}, "bold": True}})

    if "Sheet1" in [ws.title for ws in sh.worksheets()]:
        try:
            sh.del_worksheet(sh.worksheet("Sheet1"))
            print("  Sheet1 default eliminado")
        except Exception as e:
            print(f"  No se pudo eliminar Sheet1: {e}")

    print("\nSheet listo:")
    print(f"  URL: https://docs.google.com/spreadsheets/d/{sh.id}")
    print(f"  Compartido con: {OWNER_EMAIL}")


if __name__ == "__main__":
    main()
