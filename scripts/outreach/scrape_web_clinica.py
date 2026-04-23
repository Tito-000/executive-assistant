"""Visita la web de cada clinica (columna 'web' del Sheet) y extrae email + @IG + @FB.

Uso:
  python3 scrape_web_clinica.py            # procesa todos los que tienen web pero no email/ig/fb
  python3 scrape_web_clinica.py --limit 20 # solo 20
  python3 scrape_web_clinica.py --dry-run  # no escribe al Sheet
"""

import re
import sys
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup
import gspread
from google.oauth2.service_account import Credentials

ROOT = Path(__file__).resolve().parents[2]
SERVICE_ACCOUNT_FILE = ROOT / "recursos-ia" / "api-keys" / "google-sheets-service-account.json"
SHEET_ID = (Path(__file__).parent / ".sheet_id").read_text().strip()

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "es-DO,es;q=0.9,en;q=0.8",
}

EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")
IG_RE = re.compile(r"(?:https?://)?(?:www\.)?instagram\.com/([a-zA-Z0-9_.]+)", re.I)
FB_RE = re.compile(r"(?:https?://)?(?:www\.|m\.)?facebook\.com/([a-zA-Z0-9_.\-]+)", re.I)

SKIP_EMAILS = {"example.com", "sentry.io", "wixpress.com", "godaddy.com", "wordpress.com", "dominio.com"}
SKIP_EMAIL_LOCAL = {"usuario", "email", "correo", "tuemail", "your", "noreply"}
SKIP_IG_USERS = {
    "explore", "accounts", "about", "p", "reel", "tv", "legal", "directory", "web",
    "rsrc.php", "rsrc", "vp", "static", "blog", "api", "developer", "developers",
    "stories", "reels", "ajax", "emails", "oauth", "data", "ads", "business",
}
SKIP_FB_USERS = {
    "tr", "sharer", "plugins", "dialog", "login", "help", "policies", "pages",
    "profile.php", "home.php", "home", "watch", "marketplace", "groups", "events",
    "ads", "business", "gaming", "bookmarks", "messages",
}


def get_sheet():
    creds = Credentials.from_service_account_file(str(SERVICE_ACCOUNT_FILE), scopes=SCOPES)
    return gspread.authorize(creds).open_by_key(SHEET_ID)


def fetch_html(url, timeout=10):
    if not url.startswith("http"):
        url = "https://" + url
    try:
        r = requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
        if r.status_code == 200 and len(r.text) > 500:
            return r.text, str(r.url)
    except Exception as e:
        print(f"    fetch error: {type(e).__name__}: {str(e)[:80]}")
    return None, url


def fetch_html_playwright(url, timeout=15000):
    if not url.startswith("http"):
        url = "https://" + url
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            ctx = browser.new_context(user_agent=HEADERS["User-Agent"], locale="es-DO")
            page = ctx.new_page()
            page.goto(url, wait_until="domcontentloaded", timeout=timeout)
            page.wait_for_timeout(2000)
            html = page.content()
            final_url = page.url
            browser.close()
            return html, final_url
    except Exception as e:
        print(f"    playwright error: {type(e).__name__}: {str(e)[:80]}")
    return None, url


def extract_ig_from_url(url):
    m = IG_RE.search(url or "")
    if m:
        handle = m.group(1).strip("/").lower()
        if handle and handle not in SKIP_IG_USERS:
            return handle
    return ""


def extract_fb_from_url(url):
    m = FB_RE.search(url or "")
    if m:
        handle = m.group(1).strip("/").lower()
        if handle and handle not in SKIP_FB_USERS and not handle.isdigit():
            return handle
    return ""


def find_contact_links(html, base_url):
    soup = BeautifulSoup(html, "html.parser")
    contact_urls = set()
    for a in soup.find_all("a", href=True):
        href = a["href"].lower()
        text = a.get_text(strip=True).lower()
        if any(k in href for k in ["contact", "contacto"]) or any(k in text for k in ["contact", "contacto"]):
            full = href if href.startswith("http") else _join(base_url, href)
            if full:
                contact_urls.add(full)
    return list(contact_urls)[:2]


def _join(base, href):
    if href.startswith("//"):
        return "https:" + href
    if href.startswith("/"):
        from urllib.parse import urlparse
        p = urlparse(base)
        return f"{p.scheme}://{p.netloc}{href}"
    return None


def extract_contacts(html):
    emails = set()
    igs = set()
    fbs = set()

    for m in EMAIL_RE.findall(html):
        m_low = m.lower()
        local, _, domain = m_low.partition("@")
        if domain in SKIP_EMAILS:
            continue
        if local in SKIP_EMAIL_LOCAL:
            continue
        if domain.endswith((".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp")):
            continue
        emails.add(m_low)

    for m in IG_RE.findall(html):
        m = m.strip("/").lower()
        if not m or m in SKIP_IG_USERS or len(m) < 2:
            continue
        if m.startswith(".") or m.endswith("."):
            continue
        if "/" in m or "?" in m:
            continue
        igs.add(m)

    for m in FB_RE.findall(html):
        m = m.strip("/").lower()
        if not m or m in SKIP_FB_USERS or len(m) < 2:
            continue
        if "/" in m or "?" in m:
            continue
        if m.isdigit():
            continue
        fbs.add(m)

    return emails, igs, fbs


def pick_best(emails, igs, fbs, web_domain):
    email = ""
    if emails:
        email = sorted(emails, key=lambda e: (
            "info@" not in e and "contact" not in e and "hola@" not in e,
            len(e)
        ))[0]

    ig = ""
    if igs:
        ig = sorted(igs, key=lambda x: (-len(x),))[0]
        ig = next(iter(igs))

    fb = ""
    if fbs:
        fb = next(iter(fbs))

    return email, ig, fb


def process_row(web_url):
    # Caso 1: la "web" ya es un IG directo
    ig_direct = extract_ig_from_url(web_url)
    fb_direct = extract_fb_from_url(web_url)
    if ig_direct:
        return "", ig_direct, ""
    if fb_direct:
        return "", "", fb_direct

    html, final_url = fetch_html(web_url)

    # Fallback a Playwright si requests falló (sitio con JS)
    if not html:
        html, final_url = fetch_html_playwright(web_url)

    if not html:
        return "", "", ""

    emails, igs, fbs = extract_contacts(html)

    if not emails or not igs or not fbs:
        contact_urls = find_contact_links(html, final_url)
        for curl in contact_urls:
            chtml, _ = fetch_html(curl)
            if chtml:
                e2, i2, f2 = extract_contacts(chtml)
                emails.update(e2)
                igs.update(i2)
                fbs.update(f2)

    return pick_best(emails, igs, fbs, final_url)


def main():
    args = sys.argv[1:]
    dry_run = "--dry-run" in args
    limit = None
    tab = "Prospectos"
    if "--limit" in args:
        i = args.index("--limit")
        limit = int(args[i + 1])
        args = args[:i] + args[i + 2:]
    if "--tab" in args:
        i = args.index("--tab")
        tab = args[i + 1]
        args = args[:i] + args[i + 2:]

    sheet = get_sheet()
    ws = sheet.worksheet(tab)
    rows = ws.get_all_records()
    headers = ws.row_values(1)

    targets = []
    for i, r in enumerate(rows, 2):
        web = r.get("web", "").strip()
        if not web:
            continue
        if r.get("email") and r.get("ig") and r.get("fb"):
            continue
        targets.append((i, r))

    if limit:
        targets = targets[:limit]

    if not targets:
        print("No hay filas con web pendientes de scrapear.")
        return

    print(f"Procesando {len(targets)} web(s)...")

    email_col = headers.index("email") + 1 if "email" in headers else None
    ig_col = headers.index("ig") + 1 if "ig" in headers else None
    fb_col = headers.index("fb") + 1 if "fb" in headers else None

    for idx, (row_num, p) in enumerate(targets, 1):
        nombre = p.get("nombre", "")[:40]
        web = p.get("web", "")
        print(f"\n[{idx}/{len(targets)}] {nombre} — {web[:60]}")

        try:
            email, ig, fb = process_row(web)
            print(f"  email={email or '-'} | ig={ig or '-'} | fb={fb or '-'}")

            if dry_run:
                continue

            if email and not p.get("email") and email_col:
                ws.update_cell(row_num, email_col, email)
            if ig and not p.get("ig") and ig_col:
                ws.update_cell(row_num, ig_col, ig)
            if fb and not p.get("fb") and fb_col:
                ws.update_cell(row_num, fb_col, fb)

        except Exception as e:
            print(f"  ERROR: {type(e).__name__}: {e}")

        time.sleep(1)


if __name__ == "__main__":
    main()
