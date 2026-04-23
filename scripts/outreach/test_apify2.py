"""Prueba del actor oficial apify/instagram-scraper (mas robusto)."""

import json
import os
from apify_client import ApifyClient

APIFY_TOKEN = os.environ.get("APIFY_TOKEN")
if not APIFY_TOKEN:
    raise SystemExit("Falta la variable de entorno APIFY_TOKEN. Exportala antes de correr el script.")

client = ApifyClient(APIFY_TOKEN)

run_input = {
    "directUrls": ["https://www.instagram.com/draaurysm/"],
    "resultsType": "details",
    "resultsLimit": 5,
    "addParentData": False,
}

print("Corriendo actor apify/instagram-scraper (oficial)...")
run = client.actor("apify/instagram-scraper").call(run_input=run_input)

print(f"Status: {run.get('status')}")

items = list(client.dataset(run["defaultDatasetId"]).iterate_items())
print(f"Total items: {len(items)}")

for i, item in enumerate(items):
    print(f"\n--- Item {i} ---")
    print(json.dumps(item, indent=2, ensure_ascii=False, default=str)[:2000])
