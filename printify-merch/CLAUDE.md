# Printify Merch Automation

AI design → Printify product launch pipeline. Read this before doing anything.

## Platform
- **Printify** API v1 at `https://api.printify.com/v1` (NOT Printful)
- Env vars: `PRINTIFY_API_KEY`, `PRINTIFY_SHOP_ID`, `OPENAI_API_KEY` — loaded from `.env`
- Image model: `gpt-image-1`, `background="transparent"`, `quality="medium"` (concepts) / `"high"` (finals), returns `b64_json`

## Cloud Session / Tunnel Setup
This project may run in a cloud environment where Printify blocks datacenter IPs.
Before making any Printify API call, Claude must:
1. Run `git pull origin HEAD` to get the latest `tunnel.url` if it exists
2. If `tunnel.url` exists and is non-empty, read it and set `PRINTIFY_BASE_URL` in `.env`
3. If `tunnel.url` does not exist, tell the user: "Run `start_tunnel.sh` (Mac/Linux) or `start_tunnel.ps1` (Windows) in the printify-merch folder, then come back."
Scripts read `PRINTIFY_BASE_URL` from `.env` and fall back to the real Printify URL automatically.

## Active Scripts

| Script | Purpose |
|---|---|
| `generate_concepts.py` | Step 1 — generate 4 AI design variations |
| `finalize_concepts.py` | Step 2 — upscale chosen design to 2000×2000 |
| `launch_brand.py` | Step 3 — full brand launch template (copy + configure per brand) |
| `reprice.py` | Reprice all live products at 25% per-variant margin |
| `update_descriptions.py` | Push SEO descriptions to all mapped products |

## Pricing — Non-Negotiable Rule
Per-variant 25% margin. Each variant priced on its own cost, not the max.
```python
import math
def price_for_cost(cost_cents, margin=0.25):
    return math.ceil(cost_cents / (1 - margin) / 100) * 100 - 1
```
Always fetch costs from the **detail endpoint** (`/products/{pid}.json`) — list endpoint is inaccurate.

## Create → Reprice Pattern (required)
Catalog blueprint variants return cost=0. Always:
1. Create product with `"price": 100` placeholder
2. Fetch the created product to get real costs
3. PUT repriced variants

## Bulk PUT with Fallback (required for stickers)
```python
resp = requests.put(f"{BASE}/shops/{SHOP}/products/{pid}.json", headers=H, json={"variants": updated})
if not resp.ok:
    for v in updated:
        requests.put(f"{BASE}/shops/{SHOP}/products/{pid}.json", headers=H, json={"variants": [v]})
        time.sleep(0.15)
```

## Placement Standards

| Product | x | y | scale |
|---|---|---|---|
| Unisex Tee | 0.5 | 0.5 | 1.0 |
| Pullover Hoodie | 0.5 | 0.45 | 0.68–0.75 |
| Dad Hat | 0.5 | 0.5 | 0.45 |
| Mug (each side) | 0.25 / 0.75 | 0.5 | 0.35 |

Mugs: two logos (x=0.25 and x=0.75). scale=1.0 overflows dye-sub mugs. Set `camera_label=left` image as `is_default=True`.

## Color Filters
```python
DARK_KEYWORDS  = {"black","navy","dark","charcoal","forest","maroon","midnight",
                  "graphite","slate","carbon","obsidian","heather gray","smoke"}
LIGHT_KEYWORDS = {"white","natural","ash","light","sand","ivory","cream",
                  "sport grey","silver","pale","vanilla"}
```

## Blueprint IDs (confirmed working)
6=Unisex Tee, 77=Pullover Hoodie, 68=Mug 11oz, 425=Mug 15oz, 400=Kiss-Cut Stickers,
384=Square Stickers, 553=Tote Bag, 1447=Dad Hat, 636=Can Cooler Sleeve, 633=Pint Glass,
1131=Frosted Beer Mug, 787=Shot Glass, 480=Cork Coaster, 355=Can Holder

## Publish Call
```python
requests.post(f"{BASE}/shops/{SHOP}/products/{pid}/publish.json", headers=H,
    json={"title":True,"description":True,"images":True,"variants":True,"tags":True})
```

## Known Quirks
- Black variants are **disabled by default** — must be explicitly enabled via PUT
- Printify may enable extra colors on publish — verify after launch
- Storefront shows the **lowest enabled variant price** as the "from" price
