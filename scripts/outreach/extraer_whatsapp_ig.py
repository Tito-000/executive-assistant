"""Visita perfil IG publico (sin login) y extrae wa.me/numero del bio.

Por que: Google Maps da el tel de recepcion. El bio IG del doctor suele tener
wa.me/XXXX con el numero DIRECTO del decision maker.

Uso:
  python3 extraer_whatsapp_ig.py --tab Estetica
  python3 extraer_whatsapp_ig.py --tab Ginecologia --limit 30
  python3 extraer_whatsapp_ig.py --tab Estetica --dry-run
"""

import re
import sys
import time
from pathlib import Path

import requests
from playwright.sync_api import sync_playwright
import gspread
from google.oauth2.service_account import Credentials

ROOT = Path(__file__).resolve().parents[2]
SERVICE_ACCOUNT_FILE = ROOT / "recursos-ia" / "api-keys" / "google-sheets-service-account.json"
SHEET_ID = (Path(__file__).parent / ".sheet_id").read_text().strip()

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

HTTP_HEADERS = {
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
    "Accept-Language": "es-DO,es;q=0.9",
}

WA_RE = re.compile(r"(?:wa\.me|api\.whatsapp\.com/send\?phone=|whatsapp\.com/send\?phone=)/?\??(?:phone=)?(\+?\d[\d\s\-]{7,})", re.I)
PHONE_RE = re.compile(r"(?:\+?1[\s\-]?)?\(?(?:809|829|849)\)?[\s\-]?\d{3}[\s\-]?\d{4}")


def get_sheet():
    creds = Credentials.from_service_account_file(str(SERVICE_ACCOUNT_FILE), scopes=SCOPES)
    return gspread.authorize(creds).open_by_key(SHEET_ID)


def fetch_ig_html_requests(username):
    url = f"https://www.instagram.com/{username}/"
    try:
        r = requests.get(url, headers=HTTP_HEADERS, timeout=15)
        if r.status_code == 200 and len(r.text) > 1000:
            return r.text
    except Exception:
        pass
    return None


def fetch_ig_html_playwright(page, username):
    url = f"https://www.instagram.com/{username}/"
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=20000)
        page.wait_for_timeout(2000)
        return page.content()
    except Exception as e:
        print(f"    pw error: {str(e)[:60]}")
        return None


def extract_wa_and_phone(html):
    """Busca wa.me en bio + numeros RD sueltos. Retorna wa_directo, bio_text, followers."""
    wa = ""
    bio = ""
    followers = ""

    # 1. Buscar wa.me directo
    m = WA_RE.search(html)
    if m:
        num = re.sub(r"[^\d]", "", m.group(1))
        if len(num) >= 10:
            wa = num

    # 2. Extraer bio del meta description
    meta_match = re.search(r'<meta property="og:description" content="([^"]+)"', html)
    if meta_match:
        bio = meta_match.group(1)

    # 3. Seguidores del meta
    follow_match = re.search(r'([\d,\.]+[KMk])\s*Followers', html)
    if follow_match:
        followers = follow_match.group(1)

    # 4. Si no hay wa.me pero hay numero RD en el HTML (bio o link in bio)
    if not wa:
        phones = PHONE_RE.findall(html)
        for p in phones[:3]:
            clean = re.sub(r"[^\d]", "", p)
            if len(clean) == 10 and clean.startswith(("809", "829", "849")):
                wa = "1" + clean
                break

    return wa, bio, followers


def process_tab(tab_name, limit=None, dry_run=False):
    sh = get_sheet()
    ws = sh.worksheet(tab_name)
    rows = ws.get_all_records()
    headers = ws.row_values(1)

    if "whatsapp_directo" not in headers:
        print(f"ERROR: columna 'whatsapp_directo' no existe en tab {tab_name}")
        return

    wa_col = headers.index("whatsapp_directo") + 1
    seguidores_col = headers.index("seguidores_ig") + 1 if "seguidores_ig" in headers else None

    targets = []
    for i, r in enumerate(rows, 2):
        ig = r.get("ig", "").strip().lstrip("@")
        if not ig:
            continue
        if r.get("whatsapp_directo"):
            continue
        targets.append((i, r, ig))

    if limit:
        targets = targets[:limit]

    if not targets:
        print(f"{tab_name}: nada por procesar")
        return

    print(f"{tab_name}: procesando {len(targets)} perfiles IG...")

    # Stats
    found_wa = 0
    with_requests = 0
    with_playwright = 0

    # Playwright como fallback
    pw = sync_playwright().start()
    browser = pw.chromium.launch(headless=True)
    ctx = browser.new_context(
        locale="es-DO",
        user_agent=HTTP_HEADERS["User-Agent"],
        viewport={"width": 390, "height": 844},
    )
    page = ctx.new_page()

    for idx, (row_num, r, ig) in enumerate(targets, 1):
        # Intento 1: requests (rapido)
        html = fetch_ig_html_requests(ig)
        source = "req"

        # Intento 2: playwright (si requests fallo o no hay wa.me en resultado)
        if not html:
            html = fetch_ig_html_playwright(page, ig)
            source = "pw"

        if not html:
            print(f"  [{idx}/{len(targets)}] @{ig} — FAIL")
            continue

        wa, bio, followers = extract_wa_and_phone(html)

        # Si requests no encontro wa, reintentamos con playwright
        if not wa and source == "req":
            html2 = fetch_ig_html_playwright(page, ig)
            if html2:
                wa2, bio2, followers2 = extract_wa_and_phone(html2)
                if wa2:
                    wa = wa2
                if bio2 and len(bio2) > len(bio):
                    bio = bio2
                if followers2 and not followers:
                    followers = followers2
                source = "pw-fb"

        status = "OK" if wa else "sin wa"
        print(f"  [{idx}/{len(targets)}] @{ig} ({source}) {status}: wa={wa or '-'} | followers={followers or '-'}")

        if wa:
            found_wa += 1
        if source == "req":
            with_requests += 1
        else:
            with_playwright += 1

        if not dry_run:
            try:
                if wa:
                    ws.update_cell(row_num, wa_col, wa)
                if followers and seguidores_col:
                    ws.update_cell(row_num, seguidores_col, followers)
            except Exception as e:
                print(f"    sheet update error: {e}")

        time.sleep(1.5)

    browser.close()
    pw.stop()

    print(f"\n{tab_name} resumen: {found_wa}/{len(targets)} con WhatsApp directo encontrado")


def main():
    args = sys.argv[1:]
    tab = None
    limit = None
    dry_run = "--dry-run" in args

    if "--tab" in args:
        tab = args[args.index("--tab") + 1]
    if "--limit" in args:
        limit = int(args[args.index("--limit") + 1])

    if not tab:
        print("Uso: python3 extraer_whatsapp_ig.py --tab Estetica [--limit N] [--dry-run]")
        print("Tabs: Estetica, Ginecologia, Dermatologia, Odontologia, Otros")
        return

    process_tab(tab, limit=limit, dry_run=dry_run)


if __name__ == "__main__":
    main()
