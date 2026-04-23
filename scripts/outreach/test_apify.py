"""Test rapido de Apify: ver que devuelve el scraper para draaurysm."""

import json
import os
from apify_client import ApifyClient

APIFY_TOKEN = os.environ.get("APIFY_TOKEN")
if not APIFY_TOKEN:
    raise SystemExit("Falta la variable de entorno APIFY_TOKEN. Exportala antes de correr el script.")

client = ApifyClient(APIFY_TOKEN)

run_input = {
    "usernames": ["draaurysm"],
    "resultsLimit": 5,
}

print("Corriendo actor apify/instagram-profile-scraper...")
run = client.actor("apify/instagram-profile-scraper").call(run_input=run_input)

print(f"Run ID: {run.get('id')}")
print(f"Status: {run.get('status')}")
print(f"Dataset ID: {run.get('defaultDatasetId')}")

print("\nItems del dataset:")
items = list(client.dataset(run["defaultDatasetId"]).iterate_items())
print(f"Total items: {len(items)}")

for i, item in enumerate(items):
    print(f"\n--- Item {i} ---")
    print(json.dumps(item, indent=2, ensure_ascii=False, default=str)[:3000])
