"""
Brand Launch Template
─────────────────────
Copy this file, rename it to launch_yourbrand.py, fill in the three
config sections below, then run:

    python launch_yourbrand.py

What it does:
  1. Uploads your design files to Printify
  2. Creates every product in your PRODUCTS list
  3. Prices each variant at 25% margin from real Printify costs
  4. Publishes everything to your connected storefront
  5. Saves a mockups.json report with all product IDs
"""

import os, base64, math, time, json, requests
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

KEY  = os.getenv("PRINTIFY_API_KEY")
SHOP = os.getenv("PRINTIFY_SHOP_ID")
BASE = "https://api.printify.com/v1"
H    = {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}

# ── CONFIG: update these three sections ───────────────────────────────────────

# 1. Your brand name — used as the product title prefix
BRAND = "Your Brand Name"

# 2. Paths to your finalized design files (2000×2000 transparent PNGs)
#    Run finalize_concepts.py first to generate these.
DESIGNS = {
    "white_design": Path(r"C:\path\to\your\design_white_2000.png"),  # for dark apparel
    "color_design": Path(r"C:\path\to\your\design_color_2000.png"),  # for light apparel + accessories
}

# 3. Products to create
#    Format: (blueprint_id, "Suffix", "position", "design_key", "color_filter")
#    color_filter options: "dark" | "light" | "black" | "any"
#
#    Blueprint IDs:
#      6=Unisex Tee  77=Pullover Hoodie  68=Mug 11oz  425=Mug 15oz
#      400=Kiss-Cut Stickers  384=Square Stickers  553=Tote Bag
#      1447=Dad Hat  636=Can Cooler Sleeve  633=Pint Glass
#      1131=Frosted Beer Mug  787=Shot Glass  480=Cork Coaster  355=Can Holder
PRODUCTS = [
    (6,    "Unisex Tee",        "front", "white_design", "dark"),
    (77,   "Pullover Hoodie",   "front", "white_design", "dark"),
    (6,    "Unisex Tee (Color)","front", "color_design", "light"),
    (77,   "Pullover Hoodie (Color)", "front", "color_design", "light"),
    (1447, "Classic Dad Hat",   "front", "color_design", "any"),
    (68,   "Mug 11oz",          "front", "color_design", "any"),
    (400,  "Kiss-Cut Stickers", "front", "color_design", "any"),
    (384,  "Square Stickers",   "front", "color_design", "any"),
    (553,  "Tote Bag",          "front", "color_design", "any"),
]

# ── Color filters ──────────────────────────────────────────────────────────────
DARK_KEYWORDS  = {"black","navy","dark","charcoal","forest","maroon","midnight",
                  "graphite","slate","carbon","obsidian","heather gray","smoke"}
LIGHT_KEYWORDS = {"white","natural","ash","light","sand","ivory","cream",
                  "sport grey","silver","pale","vanilla"}

MARGIN = 0.25

# ── Helpers ───────────────────────────────────────────────────────────────────
def price_for_cost(cost):
    return math.ceil(cost / (1 - MARGIN) / 100) * 100 - 1

def upload_file(path):
    print(f"  Uploading {path.name}...")
    b64 = base64.b64encode(path.read_bytes()).decode()
    r = requests.post(f"{BASE}/uploads/images.json", headers=H,
                      json={"file_name": path.name, "contents": b64})
    r.raise_for_status()
    fid = r.json()["id"]
    print(f"  OK -> image ID {fid}")
    return fid

def filter_variants(variants, color_filter):
    if color_filter == "any":   return variants[:12]
    if color_filter == "black": return [v for v in variants if "black" in v.get("title","").lower()][:6] or variants[:3]
    if color_filter == "dark":  return [v for v in variants if any(k in v.get("title","").lower() for k in DARK_KEYWORDS)][:10] or variants[:5]
    if color_filter == "light": return [v for v in variants if any(k in v.get("title","").lower() for k in LIGHT_KEYWORDS)][:10] or variants[:5]
    return variants[:8]

def put_variants(pid, updated):
    resp = requests.put(f"{BASE}/shops/{SHOP}/products/{pid}.json", headers=H, json={"variants": updated})
    if resp.ok: return
    for v in updated:
        requests.put(f"{BASE}/shops/{SHOP}/products/{pid}.json", headers=H, json={"variants": [v]})
        time.sleep(0.15)

def publish(pid):
    requests.post(f"{BASE}/shops/{SHOP}/products/{pid}/publish.json", headers=H,
                  json={"title":True,"description":True,"images":True,"variants":True,"tags":True})

def create_product(title, bp_id, prov_id, variants, image_id, position):
    vids = [v["id"] for v in variants]
    payload = {
        "title": title,
        "blueprint_id": bp_id,
        "print_provider_id": prov_id,
        "variants": [{"id": vid, "price": 100, "is_enabled": True} for vid in vids],
        "print_areas": [{"variant_ids": vids, "placeholders": [
            {"position": position,
             "images": [{"id": image_id, "x": 0.5, "y": 0.5, "scale": 1, "angle": 0}]}
        ]}],
    }
    r = requests.post(f"{BASE}/shops/{SHOP}/products.json", headers=H, json=payload)
    r.raise_for_status()
    product = r.json()
    pid = product["id"]
    time.sleep(1)

    detail   = requests.get(f"{BASE}/shops/{SHOP}/products/{pid}.json", headers=H).json()
    updated  = []
    for v in detail.get("variants", []):
        cost  = v.get("cost") or 0
        price = price_for_cost(cost) if cost else 199
        updated.append({"id": v["id"], "price": price, "is_enabled": v.get("is_enabled", True)})
    put_variants(pid, updated)

    enabled_prices = [u["price"] for u, v in zip(updated, detail.get("variants", [])) if v.get("is_enabled")]
    return product, min(enabled_prices) if enabled_prices else 0

# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    print(f"\n{'='*52}")
    print(f"  {BRAND} — Full Launch")
    print(f"{'='*52}\n")

    # Upload designs
    print("Step 1: Uploading designs")
    image_ids = {}
    for key, path in DESIGNS.items():
        if not path.exists():
            print(f"  [SKIP] Not found: {path}")
            continue
        try:
            image_ids[key] = upload_file(path)
            time.sleep(0.5)
        except Exception as e:
            print(f"  [ERROR] {key}: {e}")

    if not image_ids:
        print("No designs uploaded. Check file paths in DESIGNS config.")
        return

    # Create products
    print(f"\nStep 2: Creating products")
    created, failed = [], []

    for (bp_id, suffix, position, design_key, color_filter) in PRODUCTS:
        if design_key not in image_ids:
            print(f"  [SKIP] {suffix} — design '{design_key}' not uploaded")
            continue
        title = f"{BRAND} — {suffix}"
        try:
            r = requests.get(f"{BASE}/catalog/blueprints/{bp_id}/print_providers.json", headers=H)
            providers = r.json()
            if not providers:
                print(f"  [SKIP] {title} — no providers")
                continue
            prov_id = providers[0]["id"]

            r = requests.get(f"{BASE}/catalog/blueprints/{bp_id}/print_providers/{prov_id}/variants.json", headers=H)
            variants = r.json().get("variants", [])
            chosen   = filter_variants(variants, color_filter)
            if not chosen:
                print(f"  [SKIP] {title} — no matching variants")
                continue

            print(f"  Creating: {title} ({len(chosen)} variants)...")
            product, base_price = create_product(title, bp_id, prov_id, chosen, image_ids[design_key], position)
            mockups = [img["src"] for img in product.get("images", [])[:2]]
            publish(product["id"])
            created.append({"id": product["id"], "title": title, "base_price": base_price / 100, "mockups": mockups})
            print(f"  [OK] Published — from ${base_price/100:.2f}")
            time.sleep(0.6)
        except Exception as e:
            print(f"  [ERROR] {title}: {e}")
            failed.append(title)

    # Summary
    print(f"\n{'='*52}")
    print(f"  Done: {len(created)} published, {len(failed)} failed")
    print(f"{'='*52}")
    for p in created:
        print(f"  ${p['base_price']:.2f}+  {p['title']}")
    if failed:
        print("\nFailed:")
        for f in failed: print(f"  x {f}")

    report = Path(__file__).parent / "mockups.json"
    report.write_text(json.dumps(created, indent=2))
    print(f"\n  Product IDs saved to: {report}")

if __name__ == "__main__":
    main()
