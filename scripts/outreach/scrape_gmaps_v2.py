"""Scrape Google Maps y guarda en la hoja correcta por especialidad.

Uso:
  python3 scrape_gmaps_v2.py --esp ginecologia
  python3 scrape_gmaps_v2.py --esp estetica
  python3 scrape_gmaps_v2.py --query "ginecologa santiago" --tab Ginecologia --especialidad ginecologia --ciudad Santiago
"""

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

DEFAULT_LIMIT = 50
SCROLL_WAIT_MS = 1500

# Queries por especialidad
QUERY_SETS = {
    "ginecologia": [
        ("ginecologa santo domingo", "ginecologia", "Santo Domingo", "Ginecologia"),
        ("ginecologa santiago republica dominicana", "ginecologia", "Santiago", "Ginecologia"),
        ("ginecologo santo domingo", "ginecologia", "Santo Domingo", "Ginecologia"),
        ("clinica ginecologica santo domingo", "ginecologia", "Santo Domingo", "Ginecologia"),
        ("obstetra santo domingo", "ginecologia", "Santo Domingo", "Ginecologia"),
    ],
    "estetica": [
        ("spa medico santo domingo", "medicina estetica", "Santo Domingo", "Estetica"),
        ("medspa santiago", "medicina estetica", "Santiago", "Estetica"),
        ("lipoescultura santo domingo", "cirugia plastica", "Santo Domingo", "Estetica"),
        ("aumento mamario santo domingo", "cirugia plastica", "Santo Domingo", "Estetica"),
        ("rinoplastia santo domingo", "cirugia plastica", "Santo Domingo", "Estetica"),
        ("botox santo domingo", "medicina estetica", "Santo Domingo", "Estetica"),
    ],
    "dermatologia": [
        ("dermatologa santo domingo", "dermatologia", "Santo Domingo", "Dermatologia"),
        ("clinica dermatologica santiago", "dermatologia", "Santiago", "Dermatologia"),
        ("dermatologo pediatra santo domingo", "dermatologia", "Santo Domingo", "Dermatologia"),
    ],
    "odontologia": [
        ("ortodoncista santo domingo", "odontologia estetica", "Santo Domingo", "Odontologia"),
        ("implantologo santo domingo", "odontologia estetica", "Santo Domingo", "Odontologia"),
        ("diseno de sonrisa santo domingo", "odontologia estetica", "Santo Domingo", "Odontologia"),
        ("carillas dentales santo domingo", "odontologia estetica", "Santo Domingo", "Odontologia"),
        ("blanqueamiento dental santiago", "odontologia estetica", "Santiago", "Odontologia"),
    ],
    "estetica_ext": [
        ("spa medico santo domingo", "medicina estetica", "Santo Domingo", "Estetica"),
        ("medspa santiago", "medicina estetica", "Santiago", "Estetica"),
        ("lipoescultura santo domingo", "cirugia plastica", "Santo Domingo", "Estetica"),
        ("aumento mamario santo domingo", "cirugia plastica", "Santo Domingo", "Estetica"),
        ("rinoplastia santo domingo", "cirugia plastica", "Santo Domingo", "Estetica"),
        ("botox santo domingo", "medicina estetica", "Santo Domingo", "Estetica"),
        ("rellenos faciales santo domingo", "medicina estetica", "Santo Domingo", "Estetica"),
        ("hilos tensores santo domingo", "medicina estetica", "Santo Domingo", "Estetica"),
        ("bbl santo domingo", "cirugia plastica", "Santo Domingo", "Estetica"),
        ("mommy makeover santo domingo", "cirugia plastica", "Santo Domingo", "Estetica"),
        ("abdominoplastia santo domingo", "cirugia plastica", "Santo Domingo", "Estetica"),
        ("cirujano plastico santiago republica dominicana", "cirugia plastica", "Santiago", "Estetica"),
    ],
    "gineco_ext": [
        ("obstetra santo domingo", "ginecologia", "Santo Domingo", "Ginecologia"),
        ("fertilidad santo domingo", "ginecologia", "Santo Domingo", "Ginecologia"),
        ("laparoscopia ginecologica santo domingo", "ginecologia", "Santo Domingo", "Ginecologia"),
        ("ginecologa punta cana", "ginecologia", "Punta Cana", "Ginecologia"),
        ("ginecologa la romana", "ginecologia", "La Romana", "Ginecologia"),
        ("menopausia santo domingo", "ginecologia", "Santo Domingo", "Ginecologia"),
    ],
    "derma_ext": [
        ("dermatologa pediatrica santo domingo", "dermatologia", "Santo Domingo", "Dermatologia"),
        ("dermatologia laser santo domingo", "dermatologia", "Santo Domingo", "Dermatologia"),
        ("tratamiento acne santo domingo", "dermatologia", "Santo Domingo", "Dermatologia"),
        ("dermatologa punta cana", "dermatologia", "Punta Cana", "Dermatologia"),
        ("dermatologo santiago cibao", "dermatologia", "Santiago", "Dermatologia"),
    ],
    "ticket_alto": [
        ("oftalmologo santo domingo", "oftalmologia", "Santo Domingo", "Otros"),
        ("lasik santo domingo", "oftalmologia", "Santo Domingo", "Otros"),
        ("nutriologa santo domingo", "nutricion", "Santo Domingo", "Otros"),
        ("bariatrica santo domingo", "medicina bariatrica", "Santo Domingo", "Otros"),
        ("balon gastrico santo domingo", "medicina bariatrica", "Santo Domingo", "Otros"),
        ("manga gastrica santo domingo", "cirugia bariatrica", "Santo Domingo", "Otros"),
        ("clinica capilar santo domingo", "tricologia", "Santo Domingo", "Otros"),
        ("trasplante capilar santo domingo", "cirugia capilar", "Santo Domingo", "Otros"),
        ("urologo santo domingo", "urologia", "Santo Domingo", "Otros"),
        ("medicina funcional santo domingo", "medicina funcional", "Santo Domingo", "Otros"),
        ("antiaging santo domingo", "medicina antiaging", "Santo Domingo", "Otros"),
        ("fisiatra santo domingo", "fisiatria", "Santo Domingo", "Otros"),
    ],
}

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

HEADERS_TPL = [
    "id", "nombre", "especialidad", "ciudad", "ig", "fb", "telefono", "web",
    "email", "whatsapp_directo", "seguidores_ig", "fuente", "texto_perfil",
    "ultimo_post", "detalle_unico", "gancho_humano", "investigado",
    "mensaje_listo", "estado", "nota"
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
            browser.close()
            return results

        feed = page.locator('[role="feed"]')
        prev_count = 0
        stable = 0
        for _ in range(40):
            links = page.locator('[role="feed"] a[href*="/maps/place/"]').all()
            count = len(links)
            if count >= limit:
                break
            if count == prev_count:
                stable += 1
                if stable >= 3:
                    break
            else:
                stable = 0
            prev_count = count
            feed.evaluate("el => el.scrollBy(0, 2000)")
            page.wait_for_timeout(SCROLL_WAIT_MS)

        place_urls = []
        for link in page.locator('[role="feed"] a[href*="/maps/place/"]').all()[:limit]:
            href = link.get_attribute("href")
            if href and href not in place_urls:
                place_urls.append(href)

        print(f"  {len(place_urls)} resultados. Extrayendo...")

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

                result = {
                    "nombre": name,
                    "telefono": phone,
                    "web": web,
                    "direccion": address,
                }
                print(f"  [{i}/{len(place_urls)}] {name[:45]} | {phone}")
                if name:
                    results.append(result)
            except Exception as e:
                print(f"  [{i}] ERROR: {str(e)[:60]}")

        browser.close()

    return results


def save_to_tab(leads, tab_name, especialidad, ciudad, fuente="gmaps"):
    sh = get_sheet()
    existing_tabs = {ws.title: ws for ws in sh.worksheets()}

    if tab_name not in existing_tabs:
        ws = sh.add_worksheet(title=tab_name, rows=1000, cols=len(HEADERS_TPL))
        ws.update(range_name="A1", values=[HEADERS_TPL])
        ws.freeze(rows=1)
    else:
        ws = existing_tabs[tab_name]

    headers = ws.row_values(1)

    # Dedupe: lee TODAS las hojas de especialidad para no duplicar cross-tab
    all_names = set()
    all_phones = set()
    for t in ["Estetica", "Ginecologia", "Dermatologia", "Odontologia", "Otros", "Prospectos_Archivo"]:
        if t in existing_tabs:
            try:
                rs = existing_tabs[t].get_all_records()
                for r in rs:
                    if r.get("nombre"):
                        all_names.add(r["nombre"].strip().lower())
                    if r.get("telefono"):
                        all_phones.add(re.sub(r"\D", "", r["telefono"]))
            except Exception:
                pass

    added = 0
    skipped = 0
    new_rows = []
    for lead in leads:
        nombre = lead.get("nombre", "").strip()
        phone_clean = re.sub(r"\D", "", lead.get("telefono", ""))
        if nombre.lower() in all_names:
            skipped += 1
            continue
        if phone_clean and phone_clean in all_phones:
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
        setv("fuente", fuente)
        setv("estado", "NUEVO")
        setv("nota", lead.get("direccion", "")[:100])
        new_rows.append(row)
        all_names.add(nombre.lower())
        if phone_clean:
            all_phones.add(phone_clean)
        added += 1

    if new_rows:
        ws.append_rows(new_rows, value_input_option="USER_ENTERED")
    return added, skipped


def main():
    args = sys.argv[1:]
    esp_key = None
    if "--esp" in args:
        i = args.index("--esp")
        esp_key = args[i + 1].lower()

    if esp_key and esp_key in QUERY_SETS:
        queries = QUERY_SETS[esp_key]
        all_add = 0
        all_skip = 0
        for q, esp, ciudad, tab in queries:
            print(f"\n=== {q} ===")
            leads = scrape_gmaps(q)
            a, s = save_to_tab(leads, tab, esp, ciudad)
            print(f"  +{a} nuevos / {s} dup")
            all_add += a
            all_skip += s
            time.sleep(3)
        print(f"\nTOTAL {esp_key}: +{all_add} / dup: {all_skip}")
        return

    print("Uso:")
    print("  python3 scrape_gmaps_v2.py --esp ginecologia")
    print("  python3 scrape_gmaps_v2.py --esp estetica")
    print("  python3 scrape_gmaps_v2.py --esp dermatologia")
    print("  python3 scrape_gmaps_v2.py --esp odontologia")


if __name__ == "__main__":
    main()
