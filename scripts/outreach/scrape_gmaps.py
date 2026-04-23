"""Scrape Google Maps para sacar clinicas medicas/esteticas RD con nombre + telefono + web + direccion.

Uso:
  python3 scrape_gmaps.py "medicina estetica santo domingo"
  python3 scrape_gmaps.py "dermatologo santiago" --limit 30
  python3 scrape_gmaps.py --batch  # corre la lista predefinida de queries
"""

import json
import re
import sys
import time
from pathlib import Path
from urllib.parse import quote_plus

from playwright.sync_api import sync_playwright
import gspread
from google.oauth2.service_account import Credentials

ROOT = Path(__file__).resolve().parents[2]
SERVICE_ACCOUNT_FILE = ROOT / "recursos-ia" / "api-keys" / "google-sheets-service-account.json"
SHEET_ID = (Path(__file__).parent / ".sheet_id").read_text().strip()

DEFAULT_LIMIT = 40
SCROLL_WAIT_MS = 1500

QUERIES_BATCH = [
    ("medicina estetica santo domingo", "medicina estetica", "Santo Domingo"),
    ("medicina estetica santiago republica dominicana", "medicina estetica", "Santiago"),
    ("cirugia plastica santo domingo", "cirugia plastica", "Santo Domingo"),
    ("dermatologo santo domingo", "dermatologia", "Santo Domingo"),
    ("dermatologo santiago", "dermatologia", "Santiago"),
    ("odontologia estetica santo domingo", "odontologia estetica", "Santo Domingo"),
    ("clinica estetica santo domingo", "estetica", "Santo Domingo"),
]

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


def get_sheet():
    creds = Credentials.from_service_account_file(str(SERVICE_ACCOUNT_FILE), scopes=SCOPES)
    return gspread.authorize(creds).open_by_key(SHEET_ID)


def scrape_gmaps(query, limit=DEFAULT_LIMIT):
    results = []
    url = f"https://www.google.com/maps/search/{quote_plus(query)}"

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            locale="es-DO",
            user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
        )
        page = context.new_page()
        page.goto(url, wait_until="domcontentloaded", timeout=30000)

        try:
            page.wait_for_selector('[role="feed"]', timeout=10000)
        except Exception:
            print("  WARN: no aparecio feed de resultados")
            browser.close()
            return results

        feed = page.locator('[role="feed"]')

        prev_count = 0
        stable_rounds = 0
        for _ in range(40):
            links = page.locator('[role="feed"] a[href*="/maps/place/"]').all()
            count = len(links)
            if count >= limit:
                break
            if count == prev_count:
                stable_rounds += 1
                if stable_rounds >= 3:
                    break
            else:
                stable_rounds = 0
            prev_count = count
            feed.evaluate("el => el.scrollBy(0, 2000)")
            page.wait_for_timeout(SCROLL_WAIT_MS)

        place_urls = []
        for link in page.locator('[role="feed"] a[href*="/maps/place/"]').all()[:limit]:
            href = link.get_attribute("href")
            if href and href not in place_urls:
                place_urls.append(href)

        print(f"  {len(place_urls)} resultados encontrados. Extrayendo detalles...")

        for i, place_url in enumerate(place_urls, 1):
            try:
                page.goto(place_url, wait_until="domcontentloaded", timeout=30000)
                page.wait_for_timeout(1500)

                name = ""
                try:
                    name = page.locator('h1').first.inner_text(timeout=3000).strip()
                except Exception:
                    pass

                phone = ""
                web = ""
                address = ""
                category = ""

                try:
                    phone_btn = page.locator('button[data-item-id^="phone"]').first
                    if phone_btn.count() > 0:
                        phone = phone_btn.get_attribute("aria-label") or ""
                        phone = re.sub(r"^(Teléfono|Phone):\s*", "", phone).strip()
                except Exception:
                    pass

                try:
                    web_btn = page.locator('a[data-item-id="authority"]').first
                    if web_btn.count() > 0:
                        web = web_btn.get_attribute("href") or ""
                except Exception:
                    pass

                try:
                    addr_btn = page.locator('button[data-item-id="address"]').first
                    if addr_btn.count() > 0:
                        address = addr_btn.get_attribute("aria-label") or ""
                        address = re.sub(r"^(Dirección|Address):\s*", "", address).strip()
                except Exception:
                    pass

                try:
                    cat_btn = page.locator('button[jsaction*="category"]').first
                    if cat_btn.count() > 0:
                        category = cat_btn.inner_text(timeout=2000).strip()
                except Exception:
                    pass

                result = {
                    "nombre": name,
                    "telefono": phone,
                    "web": web,
                    "direccion": address,
                    "categoria": category,
                    "gmaps_url": place_url,
                }
                print(f"  [{i}/{len(place_urls)}] {name[:50]} | {phone} | {web[:40]}")
                if name:
                    results.append(result)
            except Exception as e:
                print(f"  [{i}] ERROR: {type(e).__name__}: {e}")

        browser.close()

    return results


def save_to_sheet(leads, especialidad, ciudad):
    sheet = get_sheet()
    ws = sheet.worksheet("Prospectos")
    headers = ws.row_values(1)
    existing = ws.get_all_records()
    existing_names = {r.get("nombre", "").strip().lower() for r in existing}
    existing_phones = {re.sub(r"\D", "", r.get("telefono", "")) for r in existing if r.get("telefono")}

    added = 0
    skipped = 0
    new_rows = []
    for lead in leads:
        nombre = lead.get("nombre", "").strip()
        phone_clean = re.sub(r"\D", "", lead.get("telefono", ""))
        if nombre.lower() in existing_names:
            skipped += 1
            continue
        if phone_clean and phone_clean in existing_phones:
            skipped += 1
            continue

        row = [""] * len(headers)

        def setv(k, v):
            if k in headers:
                row[headers.index(k)] = v

        setv("nombre", nombre)
        setv("especialidad", especialidad)
        setv("ciudad", ciudad)
        setv("telefono", lead.get("telefono", ""))
        setv("web", lead.get("web", ""))
        setv("estado", "NUEVO")
        setv("nota", f"gmaps: {lead.get('categoria', '')} | {lead.get('direccion', '')[:100]}")

        new_rows.append(row)
        existing_names.add(nombre.lower())
        if phone_clean:
            existing_phones.add(phone_clean)
        added += 1

    if new_rows:
        ws.append_rows(new_rows, value_input_option="USER_ENTERED")

    return added, skipped


def main():
    args = sys.argv[1:]

    if "--batch" in args:
        all_added = 0
        all_skipped = 0
        for query, especialidad, ciudad in QUERIES_BATCH:
            print(f"\n=== Query: {query} ({especialidad} / {ciudad}) ===")
            leads = scrape_gmaps(query, limit=DEFAULT_LIMIT)
            added, skipped = save_to_sheet(leads, especialidad, ciudad)
            print(f"  +{added} nuevos / {skipped} duplicados")
            all_added += added
            all_skipped += skipped
            time.sleep(3)
        print(f"\nTOTAL: +{all_added} leads nuevos en Sheet (dup: {all_skipped})")
        return

    limit = DEFAULT_LIMIT
    if "--limit" in args:
        i = args.index("--limit")
        limit = int(args[i + 1])
        args = args[:i] + args[i + 2:]

    args = [a for a in args if not a.startswith("--")]
    if not args:
        print("Uso: python3 scrape_gmaps.py 'query' [--limit N]")
        print("O:   python3 scrape_gmaps.py --batch")
        return

    query = " ".join(args)
    # Detectar especialidad y ciudad del query (heuristica)
    especialidad = "otro"
    if "estetica" in query.lower() or "esteti" in query.lower():
        especialidad = "medicina estetica"
    if "dermatol" in query.lower():
        especialidad = "dermatologia"
    if "cirugia plastica" in query.lower() or "plastico" in query.lower():
        especialidad = "cirugia plastica"
    if "odonto" in query.lower() or "dental" in query.lower():
        especialidad = "odontologia estetica"

    ciudad = ""
    if "santo domingo" in query.lower():
        ciudad = "Santo Domingo"
    elif "santiago" in query.lower():
        ciudad = "Santiago"

    print(f"=== Query: {query} ===")
    print(f"Especialidad: {especialidad} | Ciudad: {ciudad}")
    leads = scrape_gmaps(query, limit=limit)
    added, skipped = save_to_sheet(leads, especialidad, ciudad)
    print(f"\nOK: +{added} leads nuevos en Sheet (dup: {skipped})")


if __name__ == "__main__":
    main()
