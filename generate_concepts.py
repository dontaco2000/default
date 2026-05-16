"""
Design concept generator — Step 1 of the Offensive Dad merch workflow.
Generates 4 style variations via DALL-E 3, saves locally for review.
"""
import os, sys, requests
from pathlib import Path
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ── CONFIG ─────────────────────────────────────────────────────────────────────
IDEA      = sys.argv[1] if len(sys.argv) > 1 else "OFFENSIVE DAD"
OUT_DIR   = Path(r"D:\Streaming research\Merch\Concepts")
OUT_DIR.mkdir(parents=True, exist_ok=True)
SLUG      = IDEA.lower().replace(" ", "_")[:30]

CONCEPTS = [
    {
        "name": "retro_badge",
        "label": "Retro Badge / Patch",
        "prompt": (
            'T-shirt graphic design on a plain white background. '
            'Vintage distressed iron-on patch style. Circular badge shape with a thick border and grunge texture. '
            'Center large bold text "OFFENSIVE DAD" in a classic slab-serif font. '
            'Below it, in a smaller curved banner ribbon, the text "TRUST ME, THE KID HAS HEARD THIS BEFORE". '
            'Aged, worn look with distressed edges. Color palette: cream, dark brown, rust orange. '
            'Isolated design on white, no shadows, print-ready.'
        ),
    },
    {
        "name": "bold_modern",
        "label": "Bold Modern Typographic",
        "prompt": (
            'T-shirt graphic design on a plain white background. '
            'Clean, bold, modern typographic poster style. '
            '"OFFENSIVE DAD" in massive all-caps condensed block letters stacked tight, filling the frame. '
            'Below it a thin ruled line, then smaller text "TRUST ME, THE KID HAS HEARD THIS BEFORE". '
            'Black and white high-contrast graphic design, strong hierarchy, minimal layout. '
            'No background elements, no shadows, print-ready on white.'
        ),
    },
    {
        "name": "comedy_club",
        "label": "Comedy Club Poster",
        "prompt": (
            'T-shirt graphic design on a plain white background. '
            '1970s comedy club show poster style. Spotlight burst radiating behind the title. '
            '"OFFENSIVE DAD" in large retro showbiz lettering with a drop shadow. '
            'Below it in a marquee-style arch or ticket banner: "TRUST ME, THE KID HAS HEARD THIS BEFORE". '
            'Color palette: deep red, yellow gold, black, white. Bold and theatrical. '
            'Isolated on white, no drop shadows outside the design, print-ready.'
        ),
    },
    {
        "name": "americana",
        "label": "Vintage Americana",
        "prompt": (
            'T-shirt graphic design on a plain white background. '
            'Vintage Americana style, like a classic 1950s roadside diner sign or trucker tee. '
            'Stars, lightning bolts, or small decorative elements framing the text. '
            '"OFFENSIVE DAD" in a bold retro script or western font, large and proud. '
            'Below it in a straight-edged banner: "TRUST ME, THE KID HAS HEARD THIS BEFORE". '
            'Color palette: navy blue, red, white, gold. Worn and proud. '
            'Isolated on white background, print-ready.'
        ),
    },
]

print(f"\nGenerating 4 concept variations for: {IDEA}\n")
paths = []

for i, concept in enumerate(CONCEPTS, 1):
    print(f"  [{i}/4] {concept['label']}...")
    try:
        response = client.images.generate(
            model="gpt-image-1",
            prompt=concept["prompt"],
            size="1024x1024",
            quality="medium",
            n=1,
            background="transparent",
        )
        import base64
        img_data = base64.b64decode(response.data[0].b64_json)
        out_path = OUT_DIR / f"{SLUG}_{concept['name']}.png"
        out_path.write_bytes(img_data)
        paths.append((concept["label"], out_path))
        print(f"         Saved -> {out_path.name}")
    except Exception as e:
        print(f"         ERROR: {e}")

print(f"\nAll concepts saved to: {OUT_DIR}")
print("\nOpen the folder to review, then tell me which number you want to use:")
for i, (label, path) in enumerate(paths, 1):
    print(f"  {i}. {label}  ({path.name})")

# Open the folder in Explorer
os.startfile(str(OUT_DIR))
