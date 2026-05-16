# Printify Merch Automation — Workflow Guide

AI-generated designs → Printify products → live storefront. Full automation in Python.

---

## Stack

- **Platform:** Printify API v1 (`https://api.printify.com/v1`)
- **Image AI:** OpenAI `gpt-image-1` (transparent PNG, 2000×2000)
- **Language:** Python 3 + `requests`, `openai`, `Pillow`, `python-dotenv`
- **Store:** Shopify connected to Printify

## Setup

```
pip install requests openai pillow python-dotenv
```

Create `.env` in the project root:
```
PRINTIFY_API_KEY=...
PRINTIFY_SHOP_ID=...
OPENAI_API_KEY=...
```

---

## The Workflow (end to end)

### Step 1 — Generate design concepts
```
python generate_concepts.py "YOUR BRAND TAGLINE"
```
- Generates 4 style variations (retro badge, bold modern, comedy club, americana) via gpt-image-1
- Saves transparent PNGs to `~/Merch/Concepts/`
- Opens the folder automatically — review and pick your favorites

### Step 2 — Finalize chosen designs
Edit `finalize_concepts.py` with the filenames you chose, then:
```
python finalize_concepts.py
```
- Regenerates the chosen design in white (for dark-shirt products)
- Upscales both designs to 2000×2000 PNG using PIL LANCZOS
- Saves finals to `~/Merch/Finals/`

### Step 3 — Launch all products
Copy `launch_brand.py`, rename it for your brand, then update the three config sections at the top:
```python
BRAND = "Your Brand Name"
DESIGNS = {
    "white_design": Path(r"~/Merch/Finals/design_white_2000.png"),
    "color_design": Path(r"~/Merch/Finals/design_color_2000.png"),
}
PRODUCTS = [
    # (blueprint_id, suffix, position, design_key, color_filter)
    (6,   "Unisex Tee",      "front", "white_design", "dark"),
    (77,  "Pullover Hoodie", "front", "white_design", "dark"),
    ...
]
```
Then run:
```
python launch_yourbrand.py
```
- Uploads designs to Printify
- Creates all products with $1 placeholder price
- Fetches real variant costs, reprices at 25% margin per-variant
- Publishes everything to the storefront

### Step 4 — Add SEO descriptions
Add your product descriptions to `update_descriptions.py` (keyed by exact product title), then:
```
python update_descriptions.py
```

### Step 5 — Verify pricing
```
python reprice.py
```
Reprices every product in the store at the correct 25% per-variant margin and prints a full audit table.

---

## Pricing Formula

```python
import math
def price_for_cost(cost_cents, margin=0.25):
    retail = cost_cents / (1 - margin)
    return math.ceil(retail / 100) * 100 - 1  # rounds up to next .99
```

- Price **each variant on its own cost** (not the max across all variants)
- This keeps all products of the same type showing identical "from" prices on the storefront
- Always fetch costs from the **detail endpoint** (`/products/{pid}.json`) — the list endpoint returns bad data

---

## Placement Standards

| Product | x | y | scale |
|---|---|---|---|
| Unisex Tee | 0.5 | 0.5 | 1.0 |
| Pullover Hoodie | 0.5 | 0.45 | 0.68–0.75 |
| Dad Hat | 0.5 | 0.5 | 0.45 |
| Mug (each side) | 0.25 / 0.75 | 0.5 | 0.35 |

**Mugs:** always place two logos (one per side). scale=1.0 massively overflows dye-sub mugs. Set the handle-side mockup (`camera_label=left`) as `is_default=True`.

---

## Color Strategy

| Design type | Best on |
|---|---|
| Bold white / high-contrast | Black, charcoal, navy, dark chocolate, forest, maroon |
| Americana / full-color | White, natural, ash, sand, sport grey |
| Color logo | White mugs, clear pint glasses, white hats, cork coasters |

```python
DARK_KEYWORDS  = {"black","navy","dark","charcoal","forest","maroon","midnight",
                  "graphite","slate","carbon","obsidian","heather gray","smoke"}
LIGHT_KEYWORDS = {"white","natural","ash","light","sand","ivory","cream",
                  "sport grey","silver","pale","vanilla"}
```

---

## Known Printify Quirks

- **Stickers reject bulk variant PUT** → always fall back to one-at-a-time updates with 0.15s sleep
- **Catalog blueprint variants have cost=0** → create with `price=100` placeholder, fetch real costs after creation, then reprice
- **List endpoint costs are wrong** → always use the detail endpoint for accurate cost data
- **Printify enables all variants on publish** regardless of what you sent — verify and disable unwanted colors after creation
- **Black variants are disabled by default** on dark-design products — must explicitly enable them

---

## Blueprint IDs (confirmed working)

| Product | Blueprint ID |
|---|---|
| Unisex Tee (Gildan 5000) | 6 |
| Pullover Hoodie | 77 |
| Mug 11oz | 68 |
| Mug 15oz | 425 |
| Kiss-Cut Stickers | 400 |
| Square Stickers | 384 |
| Tote Bag | 553 |
| Dad Hat | 1447 |
| Can Cooler Sleeve | 636 |
| Pint Glass 16oz | 633 |
| Frosted Beer Mug | 1131 |
| Shot Glass | 787 |
| Cork Coaster | 480 |
| Can Holder | 355 |

---

## Active Scripts

| File | What it does |
|---|---|
| `generate_concepts.py` | 4 design variations via gpt-image-1 |
| `finalize_concepts.py` | Upscale chosen designs to 2000×2000 |
| `launch_brand.py` | Full brand launch template |
| `reprice.py` | Reprice all live products at 25% margin |
| `update_descriptions.py` | Push SEO descriptions to all products |
