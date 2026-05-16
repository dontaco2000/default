"""
Step 2: Regenerate Bold Modern in white, upscale both chosen designs to 2000x2000.
"""
import os, base64
from pathlib import Path
from PIL import Image
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client  = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
OUT_DIR = Path(r"D:\Streaming research\Merch\Concepts")
FINAL   = Path(r"D:\Streaming research\Merch\Offensive Dad")
FINAL.mkdir(parents=True, exist_ok=True)

# ── Step 1: Regenerate Bold Modern in white for dark shirts ────────────────────
print("Regenerating Bold Modern in white (for dark shirts)...")
prompt = (
    "T-shirt graphic design on a fully transparent background. "
    "Clean, bold, modern typographic poster style. ALL design elements are pure white only. "
    "The text OFFENSIVE DAD in massive all-caps condensed block letters, stacked tight, pure white. "
    "Below it a thin white horizontal rule line, then smaller white text: "
    "TRUST ME, THE KID HAS HEARD THIS BEFORE. "
    "Every element is white. No black, no gray, no color. Transparent background. "
    "Print-ready design for printing on dark colored shirts."
)
resp = client.images.generate(
    model="gpt-image-1",
    prompt=prompt,
    size="1024x1024",
    quality="high",
    n=1,
    background="transparent",
)
img_data = base64.b64decode(resp.data[0].b64_json)
white_raw = OUT_DIR / "offensive_dad_bold_modern_white.png"
white_raw.write_bytes(img_data)
print(f"  Saved -> {white_raw.name}")

# ── Step 2: Upscale both to 2000x2000 ─────────────────────────────────────────
def upscale(src: Path, dst: Path, size=(2000, 2000)):
    img = Image.open(src).convert("RGBA")
    img = img.resize(size, Image.LANCZOS)
    img.save(dst, "PNG")
    print(f"  Upscaled {src.name} -> {dst.name}")

print("\nUpscaling to 2000x2000...")
upscale(
    OUT_DIR / "offensive_dad_americana.png",
    FINAL   / "offensive_dad_americana_2000.png"
)
upscale(
    OUT_DIR / "offensive_dad_bold_modern_white.png",
    FINAL   / "offensive_dad_bold_white_2000.png"
)

print(f"\nBoth final files ready in: {FINAL}")
print("  1. offensive_dad_americana_2000.png      (light shirts)")
print("  2. offensive_dad_bold_white_2000.png     (dark shirts)")
os.startfile(str(FINAL))
