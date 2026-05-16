#!/bin/bash
# Printify tunnel launcher — double-click or run from terminal.
# Starts the local proxy, opens a free SSH tunnel, and pushes the
# tunnel URL to the repo so Claude can connect automatically.
# Stop with Ctrl+C.

set -e
cd "$(dirname "$0")"

PORT=8765

# ── Start proxy ───────────────────────────────────────────────────────────────
echo ""
echo "  [1/3] Starting Printify proxy on port $PORT..."
python3 proxy.py $PORT &
PROXY_PID=$!
sleep 1

# ── Start tunnel ──────────────────────────────────────────────────────────────
echo "  [2/3] Opening tunnel..."
TMPFILE=$(mktemp)
ssh -o StrictHostKeyChecking=no \
    -o ServerAliveInterval=30 \
    -R 80:localhost:$PORT nokey@localhost.run \
    > "$TMPFILE" 2>&1 &
SSH_PID=$!

# ── Wait for URL ──────────────────────────────────────────────────────────────
URL=""
for i in $(seq 1 25); do
    sleep 1
    URL=$(grep -oE 'https://[a-zA-Z0-9_-]+\.localhost\.run' "$TMPFILE" 2>/dev/null | head -1)
    [ -n "$URL" ] && break
done

if [ -z "$URL" ]; then
    echo ""
    echo "  ERROR: Could not detect tunnel URL. Output was:"
    cat "$TMPFILE"
    kill $PROXY_PID $SSH_PID 2>/dev/null
    exit 1
fi

# ── Push URL to repo so Claude can read it ────────────────────────────────────
echo "  [3/3] Pushing tunnel URL to repo..."
echo "${URL}/v1" > tunnel.url
git add tunnel.url
git diff --cached --quiet || git commit -m "tunnel: update URL"
git push origin HEAD --quiet

echo ""
echo "  ✓ Proxy:  http://localhost:$PORT"
echo "  ✓ Tunnel: ${URL}/v1"
echo "  ✓ Claude can now connect automatically."
echo ""
echo "  Keep this window open. Ctrl+C to stop."
echo ""

# ── Cleanup on exit ───────────────────────────────────────────────────────────
cleanup() {
    echo ""
    echo "  Shutting down..."
    kill $PROXY_PID $SSH_PID 2>/dev/null
    rm -f "$TMPFILE"
    git rm -f tunnel.url 2>/dev/null && git commit -m "tunnel: closed" && git push origin HEAD --quiet || true
}
trap cleanup EXIT INT TERM

wait $SSH_PID
