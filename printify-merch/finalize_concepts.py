"""
Design Finalizer — Step 2 of the merch workflow
─────────────────────────────────────────────────
After reviewing the concepts from generate_concepts.py, update the
CONFIG section below with your chosen files, then run:

    python finalize_concepts.py

What it does:
  - Optionally regenerates a concept in white (for dark-shirt products)
  - Upscales chosen designs to 2000x2000 px (print-ready)
  - Saves finals to your output folder
"""

import os, base64
from pathlib import Path
from PIL import Image
from dotenv import load_dotenv
load_dotenv()

# ── CONFIG: update these before running ───────────────────────────────────────

CONCEPTS_DIR = Path.home() / "Merch" / "Concepts"   # where generate_concepts.py saved files
FINALS_DIR   = Path.home() / "Merch" / "Finals"     # where to save the 2000x2000 outputs
FINALS_DIR.mkdir(parents=True, exist_ok=True)

# Files to upscale — update filenames to match your chosen concepts
# Format: "output_name.png": CONCEPTS_DIR / "source_name.png"
TO_UPSCALE = {
    "design_color_2000.png": CONCEPTS_DIR / "your_brand_americana.png",
    "design_white_2000.png": CONCEPTS_DIR / "your_brand_bold_modern.png",
}

# Optional: regenerate a concept in white for dark-shirt printing.
# Set REGENERATE_WHITE to None to skip, or provide a prompt string.
REGENERATE_WHITE = None
# Example prompt:
# REGENERATE_WHITE = (
#     "T-shirt graphic design on a fully transparent background. "
#     "ALL elements pure white only. YOUR DESIGN DESCRIPTION HERE. "
#     "No black, no gray, no color. Print-ready for dark colored shirts."
# )
REGENERATE_OUTPUT = CONCEPTS_DIR / "design_white_raw.png"

# ── Regenerate in white (optional) ────────────────────────────────────────────
if REGENERATE_WHITE:
    from openai import OpenAI
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    print("Regenerating design in white...")
    resp = client.images.generate(
        model="gpt-image-1",
        prompt=REGENERATE_WHITE,
        size="1024x1024",
        quality="high",
        n=1,
        background="transparent",
    )
    img_data = base64.b64decode(resp.data[0].b64_json)
    REGENERATE_OUTPUT.write_bytes(img_data)
    print(f"  Saved -> {REGENERATE_OUTPUT.name}")

# ── Upscale to 2000x2000 ──────────────────────────────────────────────────────
def upscale(src, dst, size=(2000, 2000)):
    img = Image.open(src).convert("RGBA")
    img = img.resize(size, Image.LANCZOS)
    img.save(dst, "PNG")
    print(f"  {src.name} -> {dst.name}")

print("Upscaling to 2000x2000...")
for output_name, source_path in TO_UPSCALE.items():
    if not source_path.exists():
        print(f"  [SKIP] Not found: {source_path}")
        continue
    upscale(source_path, FINALS_DIR / output_name)

print(f"\nFinals saved to: {FINALS_DIR}")
print("Update the DESIGNS paths in your launch script to point here.")
