import requests, time, os, math
from dotenv import load_dotenv
load_dotenv()

KEY  = os.getenv("PRINTIFY_API_KEY")
SHOP = os.getenv("PRINTIFY_SHOP_ID")
BASE = os.getenv("PRINTIFY_BASE_URL", "https://api.printify.com/v1")
H    = {"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"}

MARGIN = 0.25  # 25% profit margin


def price_for_cost(cost_cents, margin=MARGIN):
    """Per-variant price at 25% margin, rounded up to next .99.
    Same cost across any product = same displayed price on storefront."""
    retail = cost_cents / (1 - margin)
    return math.ceil(retail / 100) * 100 - 1


def put_variants(pid, updated):
    """Try bulk PUT first; fall back to one-at-a-time for products that reject bulk updates."""
    resp = requests.put(f"{BASE}/shops/{SHOP}/products/{pid}.json",
                        headers=H, json={"variants": updated})
    if resp.ok:
        return "OK", ""
    failures = []
    for v in updated:
        r2 = requests.put(f"{BASE}/shops/{SHOP}/products/{pid}.json",
                          headers=H, json={"variants": [v]})
        if not r2.ok:
            failures.append(v["id"])
        time.sleep(0.15)
    if failures:
        return "FAIL", f"  --> bulk+individual failed for {len(failures)} variant(s)"
    return "OK*", ""


# Fetch product list
r = requests.get(f"{BASE}/shops/{SHOP}/products.json?limit=50", headers=H)
product_list = r.json().get("data", [])
print(f"Repricing {len(product_list)} products at {int(MARGIN*100)}% margin (per-variant)...\n")
print(f"{'Product':<45} {'Base Price':>11} {'Max Price':>10} {'Variants':>9}")
print("-" * 80)

for stub in product_list:
    pid   = stub["id"]
    title = stub["title"]

    detail   = requests.get(f"{BASE}/shops/{SHOP}/products/{pid}.json", headers=H).json()
    variants = detail.get("variants", [])

    enabled = [v for v in variants if v.get("is_enabled")]
    if not any(v.get("cost") for v in enabled):
        print(f"  [SKIP] {title} -- no cost data")
        continue

    # Price every variant individually based on its own cost
    updated = []
    for v in variants:
        cost = v.get("cost") or 0
        if cost:
            price = price_for_cost(cost)
        else:
            # disabled variant with no cost — carry its current price unchanged
            price = v.get("price", 999)
        updated.append({"id": v["id"], "price": price, "is_enabled": v.get("is_enabled", True)})

    enabled_prices = [u["price"] for u, v in zip(updated, variants) if v.get("is_enabled")]
    base_price = min(enabled_prices)
    max_price  = max(enabled_prices)

    status, detail_str = put_variants(pid, updated)

    short = title[:43]
    print(f"  [{status}] {short:<43} ${base_price/100:>8.2f}   ${max_price/100:>7.2f}   {len(enabled_prices):>5} vars")
    if detail_str:
        print(detail_str)
    time.sleep(0.5)

print("\nDone.")
