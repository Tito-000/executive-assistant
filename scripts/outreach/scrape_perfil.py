"""Scrape IG profiles con instaloader + cuenta scout y llena columna texto_perfil del Sheet.

Flujo:
1. Se loguea una vez con @martinmercedesaqui (sesion cacheada en ~/.config/instaloader/)
2. Lee @IGs del Sheet que NO tienen texto_perfil lleno
3. Por cada uno: lee bio + ultimos 5 posts y concatena
4. Escribe a columna texto_perfil
5. Throttle 45s entre perfiles (anti-ban)

Uso:
  python3 scrape_perfil.py                    # todos los que estan sin texto_perfil
  python3 scrape_perfil.py draaurysm          # un @IG especifico
  python3 scrape_perfil.py --dry-run          # no escribe al Sheet
  python3 scrape_perfil.py --limit 5          # solo 5 perfiles
"""

import sys
import time
from pathlib import Path

import instaloader
import gspread
from google.oauth2.service_account import Credentials

ROOT = Path(__file__).resolve().parents[2]
SERVICE_ACCOUNT_FILE = ROOT / "recursos-ia" / "api-keys" / "google-sheets-service-account.json"
SHEET_ID = (Path(__file__).parent / ".sheet_id").read_text().strip()

SCOUT_USER = "martinmercedesaqui"
SCOUT_PASS = "Martin-31"

POSTS_TO_READ = 5
THROTTLE_SECONDS = 45

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]


def get_sheet():
    creds = Credentials.from_service_account_file(str(SERVICE_ACCOUNT_FILE), scopes=SCOPES)
    return gspread.authorize(creds).open_by_key(SHEET_ID)


def get_loader():
    L = instaloader.Instaloader(
        download_pictures=False,
        download_videos=False,
        download_video_thumbnails=False,
        download_geotags=False,
        download_comments=False,
        save_metadata=False,
        compress_json=False,
        quiet=True,
    )
    session_file = Path.home() / ".config" / "instaloader" / f"session-{SCOUT_USER}"
    if session_file.exists():
        print(f"Cargando sesion cacheada de @{SCOUT_USER}...")
        L.load_session_from_file(SCOUT_USER)
    else:
        print(f"Login inicial como @{SCOUT_USER}...")
        L.login(SCOUT_USER, SCOUT_PASS)
        L.save_session_to_file()
        print("Sesion guardada para futuras corridas.")
    return L


def scrape_profile(L, ig_username):
    profile = instaloader.Profile.from_username(L.context, ig_username)

    bio = profile.biography or ""
    full_name = profile.full_name or ""
    external = profile.external_url or ""
    category = profile.business_category_name or ""
    followers = profile.followers
    is_private = profile.is_private

    parts = [
        f"NOMBRE: {full_name}",
        f"BIO: {bio}",
        f"CATEGORIA: {category}" if category else "",
        f"WEB: {external}" if external else "",
        f"SEGUIDORES: {followers}",
        f"PRIVADA: {is_private}",
        "",
        "=== ULTIMOS POSTS ===",
    ]

    if is_private:
        parts.append("(cuenta privada, posts no accesibles)")
    else:
        count = 0
        for post in profile.get_posts():
            count += 1
            caption = (post.caption or "").strip()
            date = post.date_utc.strftime("%Y-%m-%d")
            parts.append(f"\nPOST {count} ({date}) — {post.likes} likes")
            parts.append(caption[:800] if caption else "(sin caption)")
            if count >= POSTS_TO_READ:
                break

    return "\n".join(p for p in parts if p != "")


def main():
    args = sys.argv[1:]
    dry_run = "--dry-run" in args
    limit = None
    if "--limit" in args:
        i = args.index("--limit")
        limit = int(args[i + 1])
        args = args[:i] + args[i + 2:]
    args = [a for a in args if not a.startswith("--")]

    sheet = get_sheet()
    ws = sheet.worksheet("Prospectos")
    rows = ws.get_all_records()
    headers = ws.row_values(1)

    if "texto_perfil" not in headers:
        print("ERROR: columna 'texto_perfil' no existe. Corre agregar_texto_perfil.py primero.")
        return

    texto_col = headers.index("texto_perfil") + 1

    if args:
        target_igs = [a.lstrip("@").lower() for a in args]
        targets = [(i, r) for i, r in enumerate(rows, 2)
                   if r.get("ig", "").lstrip("@").lower() in target_igs]
    else:
        targets = [(i, r) for i, r in enumerate(rows, 2)
                   if r.get("ig") and not r.get("texto_perfil")]

    if limit:
        targets = targets[:limit]

    if not targets:
        print("No hay prospectos para scrapear.")
        return

    print(f"Scrapeando {len(targets)} perfil(es)...")
    L = get_loader()

    for idx, (row_num, p) in enumerate(targets, 1):
        ig = p.get("ig", "").lstrip("@")
        nombre = p.get("nombre", "")
        print(f"\n[{idx}/{len(targets)}] @{ig} ({nombre})")

        try:
            texto = scrape_profile(L, ig)
            preview = texto[:200].replace("\n", " | ")
            print(f"  OK ({len(texto)} chars): {preview}...")

            if dry_run:
                print("  DRY RUN: no escribo al Sheet")
            else:
                ws.update_cell(row_num, texto_col, texto)
                print(f"  Sheet fila {row_num} actualizado")

        except instaloader.exceptions.ProfileNotExistsException:
            print(f"  SKIP: perfil @{ig} no existe")
        except instaloader.exceptions.LoginRequiredException:
            print(f"  FAIL: Instagram pide login de nuevo — sesion expirada")
            print(f"  Borra ~/.config/instaloader/session-{SCOUT_USER} y reintenta")
            break
        except instaloader.exceptions.ConnectionException as e:
            print(f"  FAIL: conexion/baneo: {e}")
            print(f"  Pausando 5 min antes de continuar...")
            time.sleep(300)
        except Exception as e:
            print(f"  ERROR: {type(e).__name__}: {e}")

        if idx < len(targets):
            print(f"  Throttle {THROTTLE_SECONDS}s...")
            time.sleep(THROTTLE_SECONDS)


if __name__ == "__main__":
    main()
