#!/bin/bash
set -e

echo ""
echo " ====================================================="
echo "  Printify Merch Automation — Mac/Linux Installer"
echo " ====================================================="
echo ""

# ── Colors ────────────────────────────────────────────────────────────────────
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

ok()   { echo -e "  ${GREEN}✓${NC} $1"; }
warn() { echo -e "  ${YELLOW}!${NC} $1"; }
fail() { echo -e "  ${RED}✗${NC} $1"; exit 1; }

# ── Check Python ──────────────────────────────────────────────────────────────
echo "[1/5] Checking Python..."

if command -v python3 &>/dev/null; then
    PYTHON=python3
    PIP=pip3
elif command -v python &>/dev/null; then
    PYTHON=python
    PIP=pip
else
    fail "Python not found. Install Python 3.9+ from https://www.python.org/downloads/"
fi

VERSION=$($PYTHON --version 2>&1)
ok "Found: $VERSION"
echo ""

# ── Install dependencies ───────────────────────────────────────────────────────
echo "[2/5] Installing Python dependencies..."
$PIP install -r requirements.txt --quiet || fail "pip install failed. Try: sudo pip3 install -r requirements.txt"
ok "Dependencies installed."
echo ""

# ── Set up .env ───────────────────────────────────────────────────────────────
echo "[3/5] Setting up environment..."

if [ -f .env ]; then
    warn ".env already exists — skipping key setup. Edit .env manually to update keys."
else
    cp .env.example .env

    echo ""
    echo "  You need three API keys. Enter them below."
    echo "  (Saved locally to .env — never uploaded anywhere)"
    echo ""

    read -p "  Printify API Key:   " PRINTIFY_KEY
    read -p "  Printify Shop ID:   " PRINTIFY_SHOP
    read -p "  OpenAI API Key:     " OPENAI_KEY

    cat > .env <<EOF
PRINTIFY_API_KEY=$PRINTIFY_KEY
PRINTIFY_SHOP_ID=$PRINTIFY_SHOP
OPENAI_API_KEY=$OPENAI_KEY
EOF

    ok "Keys saved to .env"
fi
echo ""

# ── Create output directories ──────────────────────────────────────────────────
echo "[4/5] Creating design output folder..."
MERCH_DIR="$HOME/Merch/Concepts"
mkdir -p "$MERCH_DIR"
ok "Output folder ready: $MERCH_DIR"
echo ""

# ── Install Claude Code context ───────────────────────────────────────────────
echo "[5/5] Verifying Claude Code project context..."

# CLAUDE.md lives in the project root — Claude Code reads it automatically
# when this folder is opened. Nothing is written to ~/.claude/.
if [ -f "CLAUDE.md" ]; then
    ok "CLAUDE.md is present. Claude Code will load it automatically when you open this folder."
else
    warn "CLAUDE.md not found. Claude won't have project context."
fi

# ── Done ──────────────────────────────────────────────────────────────────────
echo ""
echo " ====================================================="
echo -e "  ${GREEN}Installation complete!${NC}"
echo " ====================================================="
echo ""
echo "  Next steps:"
echo "    1. Open this folder in Claude Code"
echo "    2. Tell Claude: \"generate concepts for [your brand idea]\""
echo "    3. Claude will walk you through the full workflow"
echo ""
echo "  Or run scripts directly:"
echo "    $PYTHON generate_concepts.py \"YOUR BRAND TAGLINE\""
echo "    $PYTHON reprice.py"
echo ""
