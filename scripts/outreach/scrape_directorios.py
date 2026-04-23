"""Scrape directorios medicos RD y agrega leads a las hojas por especialidad.

Fuentes:
  - doctoralia.com.do      (grande, todas las especialidades)
  - paginasamarillas.com.do
  - sodocipre.org          (cirujanos plasticos RD)
  - sododerma.org          (dermatologos RD)

Uso:
  python3 scrape_directorios.py --fuente doctoralia --esp ginecologia
  python3 scrape_directorios.py --fuente doctoralia --esp dermatologia
  python3 scrape_directorios.py --fuente sodocipre
  python3 scrape_directorios.py --fuente sododerma
"""

import re
import sys
import time
from pathlib import Path
from urllib.parse import quote_plus, urljoin

import requests
from bs4 import BeautifulSoup
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
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept-Language": "es-DO,es;q=0.9,en;q=0.8",
}

HEADERS_TPL = [
    "id", "nombre", "especialidad", "ciudad", "ig", "fb", "telefono", "web",
    "email", "whatsapp_directo", "seguidores_ig", "fuente", "texto_perfil",
    "ultimo_post", "detalle_unico", "gancho_humano", "investigado",
    "mensaje_listo", "estado", "nota"
]

DOCTORALIA_ESPS = {
    "ginecologia": "ginecologo-obstetra",
    "dermatologia": "dermatologo",
    "estetica": "medico-estetico",
    "cirugia-plastica": "cirujano-plastico",
    "odontologia": "dentista",
}

TAB_BY_ESP = {
    "ginecologia": ("Ginecologia", "ginecologia"),
    "dermatologia": ("Dermatologia", "dermatologia"),
    "estetica": ("Estetica", "medicina estetica"),
    "cirugia-plastica": ("Estetica", "cirugia plastica"),
    "odontologia": ("Odontologia", "odontologia estetica"),
}


def get_sheet():
    creds = Credentials.from_service_account_file(str(SERVICE_ACCOUNT_FILE), scopes=SCOPES)
    return gspread.authorize(creds).open_by_key(SHEET_ID)


def scrape_doctoralia(especialidad_key):
    """Doctoralia usa SPA con render cliente — usamos Playwright."""
    slug = DOCTORALIA_ESPS.get(especialidad_key)
    if not slug:
        print(f"Especialidad desconocida: {especialidad_key}")
        return []

    results = []
    base = f"https://www.doctoralia.com.do/buscar?q=&loc=Rep%C3%BAblica+Dominicana&filters%5Bspecializations%5D%5B%5D={slug}"
    print(f"Scraping: {base}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(
            locale="es-DO",
            user_agent=HTTP_HEADERS["User-Agent"],
        )
        page = ctx.new_page()

        page_num = 1
        seen = set()
        while page_num <= 10:
            url = base + f"&page={page_num}" if page_num > 1 else base
            try:
                page.goto(url, wait_until="networkidle", timeout=30000)
                page.wait_for_timeout(2500)
            except Exception as e:
                print(f"  page {page_num}: timeout/error — {str(e)[:60]}")
                break

            cards = page.locator('[data-test-id="search-result"]').all()
            if not cards:
                cards = page.locator('article').all()
            if not cards:
                print(f"  page {page_num}: sin resultados — fin")
                break

            new_on_page = 0
            for card in cards:
                try:
                    name_el = card.locator('h3, [data-test-id="doctor-card-name"]').first
                    name = name_el.inner_text(timeout=1000).strip() if name_el.count() else ""
                    if not name or name in seen:
                        continue
                    seen.add(name)

                    # URL del perfil
                    link_el = card.locator('a').first
                    perfil_url = link_el.get_attribute("href") if link_el.count() else ""
                    if perfil_url and not perfil_url.startswith("http"):
                        perfil_url = "https://www.doctoralia.com.do" + perfil_url

                    # Ciudad
                    ciudad = ""
                    loc_el = card.locator('[data-test-id*="address"], [class*="address"]').first
                    if loc_el.count():
                        ciudad_txt = loc_el.inner_text(timeout=500)
                        if "santo domingo" in ciudad_txt.lower():
                            ciudad = "Santo Domingo"
                        elif "santiago" in ciudad_txt.lower():
                            ciudad = "Santiago"

                    results.append({
                        "nombre": name,
                        "perfil_url": perfil_url,
                        "ciudad": ciudad,
                    })
                    new_on_page += 1
                except Exception:
                    continue

            print(f"  page {page_num}: +{new_on_page} nuevos (total: {len(results)})")
            if new_on_page == 0:
                break
            page_num += 1
            time.sleep(1.5)

        # Ahora visita cada perfil para sacar telefono + web
        print(f"\nEnriquciendo {len(results)} perfiles...")
        for i, r in enumerate(results, 1):
            if not r.get("perfil_url"):
                continue
            try:
                page.goto(r["perfil_url"], wait_until="domcontentloaded", timeout=20000)
                page.wait_for_timeout(1500)
                html = page.content()

                # telefono
                phone = ""
                phone_el = page.locator('[data-test-id*="phone"], a[href^="tel:"]').first
                if phone_el.count():
                    href = phone_el.get_attribute("href") or ""
                    if href.startswith("tel:"):
                        phone = href.replace("tel:", "").strip()
                    if not phone:
                        phone = phone_el.inner_text(timeout=500).strip()
                r["telefono"] = phone

                # web/redes en el body
                ig_match = re.search(r'instagram\.com/([a-zA-Z0-9_.]+)', html)
                if ig_match:
                    ig = ig_match.group(1).lower()
                    if ig not in ("explore", "p", "reel", "web", "static"):
                        r["ig"] = ig

                fb_match = re.search(r'facebook\.com/([a-zA-Z0-9_.\-]+)', html)
                if fb_match:
                    fb = fb_match.group(1).lower()
                    if fb not in ("tr", "sharer", "plugins", "dialog"):
                        r["fb"] = fb

                if i % 10 == 0:
                    print(f"  {i}/{len(results)}: {r['nombre'][:40]} | tel={r.get('telefono','-')}")
            except Exception as e:
                print(f"  {i}: error — {str(e)[:50]}")

        browser.close()

    return results


def scrape_sodocipre():
    """Sociedad Dominicana de Cirugia Plastica — directorio de socios."""
    url = "https://sodocipre.org/socios/"
    results = []
    try:
        r = requests.get(url, headers=HTTP_HEADERS, timeout=15)
        if r.status_code != 200:
            print(f"sodocipre: HTTP {r.status_code}")
            return []
        soup = BeautifulSoup(r.text, "html.parser")
        # Extraer bloques de socios (a ajustar segun estructura real)
        texto = soup.get_text("\n", strip=True)
        # Extraer nombres tipo "Dr./Dra. NOMBRE APELLIDO"
        pattern = re.compile(r"(Dr[a]?\.\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+){1,3})")
        for m in pattern.finditer(texto):
            name = m.group(1).strip()
            if len(name) < 10 or name in {r["nombre"] for r in results}:
                continue
            results.append({"nombre": name})
        print(f"sodocipre: {len(results)} nombres extraidos (sin telefono)")
    except Exception as e:
        print(f"sodocipre error: {e}")
    return results


def scrape_sododerma():
    """Sociedad Dominicana de Dermatologia — estructura similar."""
    urls = [
        "https://sododerma.org/socios/",
        "https://sododerma.org/directorio/",
        "https://www.sododerma.org/socios",
    ]
    results = []
    for url in urls:
        try:
            r = requests.get(url, headers=HTTP_HEADERS, timeout=15)
            if r.status_code != 200:
                continue
            soup = BeautifulSoup(r.text, "html.parser")
            texto = soup.get_text("\n", strip=True)
            pattern = re.compile(r"(Dr[a]?\.\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñ]+){1,3})")
            for m in pattern.finditer(texto):
                name = m.group(1).strip()
                if len(name) < 10 or name in {r["nombre"] for r in results}:
                    continue
                results.append({"nombre": name})
            if results:
                print(f"sododerma ({url}): {len(results)} nombres")
                return results
        except Exception:
            continue
    print("sododerma: no se pudo acceder")
    return results


def save_to_tab(leads, tab_name, especialidad, fuente):
    sh = get_sheet()
    existing_tabs = {ws.title: ws for ws in sh.worksheets()}
    if tab_name not in existing_tabs:
        ws = sh.add_worksheet(title=tab_name, rows=1000, cols=len(HEADERS_TPL))
        ws.update(range_name="A1", values=[HEADERS_TPL])
        ws.freeze(rows=1)
    else:
        ws = existing_tabs[tab_name]

    headers = ws.row_values(1)

    # Dedup cross-tabs
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
            if k in headers and v:
                row[headers.index(k)] = v
        setv("nombre", nombre)
        setv("especialidad", especialidad)
        setv("ciudad", lead.get("ciudad", ""))
        setv("ig", lead.get("ig", ""))
        setv("fb", lead.get("fb", ""))
        setv("telefono", lead.get("telefono", ""))
        setv("web", lead.get("perfil_url", ""))
        setv("fuente", fuente)
        setv("estado", "NUEVO")
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
    fuente = None
    esp = None

    if "--fuente" in args:
        fuente = args[args.index("--fuente") + 1]
    if "--esp" in args:
        esp = args[args.index("--esp") + 1]

    if fuente == "doctoralia":
        if not esp or esp not in DOCTORALIA_ESPS:
            print(f"Especialidades validas: {list(DOCTORALIA_ESPS.keys())}")
            return
        leads = scrape_doctoralia(esp)
        tab, especialidad_label = TAB_BY_ESP[esp]
        a, s = save_to_tab(leads, tab, especialidad_label, f"doctoralia:{esp}")
        print(f"\nTOTAL: +{a} en {tab} / dup: {s}")
        return

    if fuente == "sodocipre":
        leads = scrape_sodocipre()
        a, s = save_to_tab(leads, "Estetica", "cirugia plastica", "sodocipre")
        print(f"\nTOTAL: +{a} en Estetica / dup: {s}")
        return

    if fuente == "sododerma":
        leads = scrape_sododerma()
        a, s = save_to_tab(leads, "Dermatologia", "dermatologia", "sododerma")
        print(f"\nTOTAL: +{a} en Dermatologia / dup: {s}")
        return

    print("Uso:")
    print("  python3 scrape_directorios.py --fuente doctoralia --esp ginecologia")
    print("  python3 scrape_directorios.py --fuente doctoralia --esp dermatologia")
    print("  python3 scrape_directorios.py --fuente doctoralia --esp cirugia-plastica")
    print("  python3 scrape_directorios.py --fuente sodocipre")
    print("  python3 scrape_directorios.py --fuente sododerma")


if __name__ == "__main__":
    main()
