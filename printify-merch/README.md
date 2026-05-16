# Printify Merch Automation

Turn a design idea into live products on your Printify storefront in minutes. Uses OpenAI's `gpt-image-1` to generate print-ready designs and the Printify API to create, price, and publish your full product lineup automatically.

Built for use with **Claude Code** — Claude understands the full workflow and can run every step for you conversationally.

**[⬇ Download Latest Release](https://github.com/dontaco2000/default/releases/download/v1.2.0/printify-merch.zip)** · **[All Releases](https://github.com/dontaco2000/default/releases)**

---

## What It Does

1. **Generates** 4 design concept variations from a text description using AI
2. **Upscales** your chosen design to a print-ready 2000×2000 transparent PNG
3. **Launches** a full product line (tees, hoodies, mugs, hats, stickers, etc.) in one command
4. **Prices** every variant automatically at 25% margin based on real Printify costs
5. **Publishes** everything live to your connected storefront

---

## Prerequisites

- Python 3.9 or higher — [python.org/downloads](https://www.python.org/downloads/)
- A Printify account with a connected store — [printify.com](https://printify.com)
- An OpenAI API key — [platform.openai.com](https://platform.openai.com)
- Claude Code (optional but recommended) — [claude.ai/code](https://claude.ai/code)

---

## Quick Install

### Windows
```
install.bat
```

### Mac / Linux
```bash
chmod +x install.sh && ./install.sh
```

The installer will:
- Verify Python is installed
- Install all dependencies
- Walk you through entering your API keys
- Set up Claude Code project context automatically

---

## Manual Setup

**1. Clone the repo**
```bash
git clone https://github.com/dontaco2000/default.git printify-merch
cd printify-merch
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Configure your keys**

Copy the example env file and fill in your credentials:
```bash
cp .env.example .env
```

Edit `.env`:
```
PRINTIFY_API_KEY=your_key_here
PRINTIFY_SHOP_ID=your_shop_id_here
OPENAI_API_KEY=your_key_here
```

**Finding your Printify credentials:**
- API Key: Printify dashboard → My Profile → Connections → API
- Shop ID: Printify dashboard → the number in your store's URL (`printify.com/app/shop/XXXXXXX/...`)

---

## Step-by-Step Workflow

### Step 1 — Generate Design Concepts

```bash
python generate_concepts.py "YOUR BRAND TAGLINE"
```

**Example:**
```bash
python generate_concepts.py "COOL BRAND — YOUR TAGLINE HERE"
```

What happens:
- AI generates **4 style variations**: Retro Badge, Bold Modern, Comedy Club, Vintage Americana
- Saves transparent PNGs to `~/Merch/Concepts/` (Mac/Linux) or `%USERPROFILE%\Merch\Concepts\` (Windows)
- Opens the folder automatically so you can review

> **Tip:** The Bold Modern style works best on dark apparel (renders in white). The Americana style works best on light apparel and accessories.

---

### Step 2 — Finalize Your Design

Once you've picked your favorite(s), open `finalize_concepts.py` and update the file paths at the top:

```python
# Edit these to match your chosen concept filenames
upscale(
    OUT_DIR / "your_brand_chosen_concept.png",   # your picked concept
    FINAL   / "your_brand_design_2000.png"        # output filename
)
```

Then run:
```bash
python finalize_concepts.py
```

What happens:
- Upscales your design to 2000×2000 pixels using high-quality LANCZOS resampling
- Saves the print-ready PNG to `~/Merch/Finals/`

---

### Step 3 — Launch Your Product Line

Copy `launch_brand.py` and rename it for your brand:
```bash
cp launch_brand.py launch_yourbrand.py
```

Open the file and update the three config sections at the top:

```python
# 1. Your brand name (used as the product title prefix)
BRAND = "Your Brand Name"

# 2. Paths to your finalized design files
DESIGNS = {
    "white_design": Path(r"~/Merch/Finals/design_white_2000.png"),
    "color_design": Path(r"~/Merch/Finals/design_color_2000.png"),
}

# 3. Which products to create
# Format: (blueprint_id, "Product Suffix", "position", "design_key", "color_filter")
PRODUCTS = [
    (6,   "Unisex Tee",         "front", "white_design", "dark"),
    (77,  "Pullover Hoodie",    "front", "white_design", "dark"),
    (6,   "Unisex Tee (Color)", "front", "color_design", "light"),
    (68,  "Mug 11oz",           "front", "color_design", "any"),
    (1447,"Classic Dad Hat",    "front", "color_design", "any"),
    (400, "Kiss-Cut Stickers",  "front", "color_design", "any"),
    (553, "Tote Bag",           "front", "color_design", "any"),
]
```

Then run:
```bash
python launch_yourbrand.py
```

What happens:
- Uploads your designs to Printify
- Creates every product in your list
- Fetches real production costs and prices each variant at 25% margin
- Publishes everything to your connected storefront
- Saves a mockup report JSON with all product IDs

---

### Step 4 — Add SEO Descriptions

Open `update_descriptions.py` and add an entry to the `DESCRIPTIONS` dict for each product, keyed by its **exact title**:

```python
DESCRIPTIONS = {
    "Your Brand Name — Unisex Tee": """
Your SEO description here. Include relevant keywords naturally.
Describe the product, who it's for, and why they'd want it.
""".strip(),

    "Your Brand Name — Pullover Hoodie": """
Another description here.
""".strip(),
    # ... one entry per product
}
```

Then run:
```bash
python update_descriptions.py
```

---

### Step 5 — Verify Pricing

Run this any time you want to audit or correct all product prices:
```bash
python reprice.py
```

Prints a full table of every product, its base price, max price, and variant count. Automatically corrects any pricing errors.

---

## Blueprint IDs (Product Types)

Use these in your `PRODUCTS` list when setting up a launch script:

| Product | Blueprint ID |
|---|---|
| Unisex Tee (Gildan 5000) | 6 |
| Pullover Hoodie | 77 |
| Mug 11oz | 68 |
| Mug 15oz | 425 |
| Kiss-Cut Stickers | 400 |
| Square Stickers | 384 |
| Tote Bag | 553 |
| Classic Dad Hat | 1447 |
| Can Cooler Sleeve | 636 |
| Pint Glass 16oz | 633 |
| Frosted Beer Mug | 1131 |
| Shot Glass | 787 |
| Cork Coaster | 480 |
| Can Holder | 355 |

---

## Color Filters

When adding products to your `PRODUCTS` list, the `color_filter` argument controls which color variants are enabled:

| Filter | What it enables |
|---|---|
| `"dark"` | Black, navy, charcoal, forest, maroon, dark chocolate, etc. |
| `"light"` | White, natural, ash, sand, sport grey, ivory, etc. |
| `"black"` | Black only |
| `"any"` | First 12 variants (used for accessories, mugs, stickers) |

---

## Placement Standards

These values are pre-configured in the launch scripts. Reference them if building your own:

| Product | x | y | scale | Notes |
|---|---|---|---|---|
| Unisex Tee | 0.5 | 0.5 | 1.0 | Standard front placement |
| Pullover Hoodie | 0.5 | 0.45 | 0.68–0.75 | High chest, avoids drawstring |
| Classic Dad Hat | 0.5 | 0.5 | 0.45 | Embroidery area is small |
| Mug (each side) | 0.25 / 0.75 | 0.5 | 0.35 | Two logos, one per side |

> ⚠️ **Mugs:** `scale=1.0` massively overflows dye-sublimation mugs. Always use `scale ≤ 0.35`.

---

## Pricing Formula

Each variant is priced on its own cost at a 25% profit margin:

```python
import math
def price_for_cost(cost_cents, margin=0.25):
    retail = cost_cents / (1 - margin)
    return math.ceil(retail / 100) * 100 - 1  # rounds up to next .99
```

This means every product of the same type (e.g. all hoodies) shows the same "from" price on your storefront, since the same size costs the same across all hoodie products.

---

## Known Printify Quirks

- **Catalog variants have no cost data** — always create with a `$1` placeholder price, fetch real costs after creation, then reprice
- **Stickers reject bulk variant updates** — the scripts fall back to updating one variant at a time automatically
- **The list endpoint returns wrong costs** — always use the detail endpoint (`/products/{pid}.json`) for accurate data
- **Printify may enable extra variants on publish** — verify and disable unwanted colors after launching
- **Black variants are disabled by default** — must be explicitly enabled in the variant PUT call

---

## Using With Claude Code

Open this project folder in Claude Code. Claude will read the `CLAUDE.md` file automatically and understand the full workflow, all the scripts, the pricing rules, and the Printify quirks — no explanation needed.

Just describe what you want:
- *"Launch a new brand called X with this tagline"*
- *"Check and fix all my prices"*
- *"Add black variants to all the dark-design products"*
- *"Generate concept designs for a new idea"*

---

## File Structure

```
printify-merch/
├── .env                    # Your API keys (never committed)
├── .env.example            # Key names — copy to .env and fill in
├── CLAUDE.md               # Claude Code project context (auto-loaded)
├── ONBOARDING.md           # Shareable workflow summary
├── README.md               # This file
├── requirements.txt        # pip dependencies
├── generate_concepts.py    # Step 1: AI design generation
├── finalize_concepts.py    # Step 2: upscale to print-ready PNG
├── launch_brand.py         # Step 3: full product launch template
├── reprice.py              # Pricing audit and correction
├── update_descriptions.py  # SEO description updater
└── mockups.json            # Generated after launch — your product IDs
```

---

## License

MIT — use it, fork it, build on it.
