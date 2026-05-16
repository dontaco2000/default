"""
SEO Description Updater
────────────────────────
Add one entry to DESCRIPTIONS for each product, keyed by its exact
title as it appears in Printify. Then run:

    python update_descriptions.py

Tips for good SEO descriptions:
  - 2–3 short paragraphs
  - Describe who it's for and when they'd wear/use it
  - End with a keyword list: "Keywords: funny tee, gift for dad, ..."
"""

import os, time, requests
from dotenv import load_dotenv
load_dotenv()

KEY  = os.getenv("PRINTIFY_API_KEY")
SHOP = os.getenv("PRINTIFY_SHOP_ID")
BASE = os.getenv("PRINTIFY_BASE_URL", "https://api.printify.com/v1")
H    = {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}

# ── Add your descriptions here ────────────────────────────────────────────────
# Key = exact product title in Printify
# Value = SEO description string
DESCRIPTIONS = {

    "Your Brand — Unisex Tee": """
Your description here. Two to three paragraphs works well. Describe the
product, who it's for, and when they'd wear it.

Great as a gift for X, Y, and Z. Available in sizes S through 3XL.

Keywords: keyword one, keyword two, keyword three.
""".strip(),

    "Your Brand — Pullover Hoodie": """
Your hoodie description here.

Keywords: funny hoodie, gift idea, graphic sweatshirt.
""".strip(),

    # Add more products below — one entry per product title

}

# ── Run ───────────────────────────────────────────────────────────────────────
r = requests.get(f"{BASE}/shops/{SHOP}/products.json?limit=50", headers=H)
products = r.json().get("data", [])
print(f"Updating descriptions for {len(products)} products...\n")

ok = skip = 0
for p in products:
    title = p["title"]
    pid   = p["id"]
    desc  = DESCRIPTIONS.get(title)
    if not desc:
        print(f"  [SKIP] {title}")
        skip += 1
        continue
    resp = requests.put(f"{BASE}/shops/{SHOP}/products/{pid}.json", headers=H,
                        json={"description": desc})
    if resp.ok:
        requests.post(f"{BASE}/shops/{SHOP}/products/{pid}/publish.json", headers=H,
                      json={"title":True,"description":True,"images":True,"variants":True,"tags":True})
        print(f"  [OK]   {title}")
        ok += 1
    else:
        print(f"  [FAIL] {title} — {resp.status_code}")
    time.sleep(0.5)

print(f"\nDone: {ok} updated, {skip} skipped.")
