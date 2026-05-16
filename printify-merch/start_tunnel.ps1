# Printify tunnel launcher for Windows (PowerShell)
# Right-click → "Run with PowerShell", or run from terminal:
#   powershell -ExecutionPolicy Bypass -File start_tunnel.ps1
# Stop with Ctrl+C.

$PORT      = 8765
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

# ── Start proxy ───────────────────────────────────────────────────────────────
Write-Host ""
Write-Host "  [1/3] Starting Printify proxy on port $PORT..."
$proxy = Start-Process python -ArgumentList "proxy.py $PORT" -PassThru -WindowStyle Hidden
Start-Sleep 1

# ── Start tunnel ──────────────────────────────────────────────────────────────
Write-Host "  [2/3] Opening tunnel..."
$tmpFile = [System.IO.Path]::GetTempFileName()
$sshArgs = "-o StrictHostKeyChecking=no -o ServerAliveInterval=30 -R 80:localhost:$PORT nokey@localhost.run"
$ssh = Start-Process ssh -ArgumentList $sshArgs `
       -RedirectStandardOutput $tmpFile -RedirectStandardError $tmpFile `
       -PassThru -WindowStyle Hidden

# ── Wait for URL ──────────────────────────────────────────────────────────────
$url = $null
for ($i = 0; $i -lt 25; $i++) {
    Start-Sleep 1
    $content = Get-Content $tmpFile -Raw -ErrorAction SilentlyContinue
    if ($content -match 'https://[a-zA-Z0-9_-]+\.localhost\.run') {
        $url = $Matches[0]
        break
    }
}

if (-not $url) {
    Write-Host ""
    Write-Host "  ERROR: Could not detect tunnel URL. Output was:"
    Get-Content $tmpFile
    Stop-Process -Id $proxy.Id, $ssh.Id -Force -ErrorAction SilentlyContinue
    exit 1
}

# ── Push URL to repo so Claude can read it ────────────────────────────────────
Write-Host "  [3/3] Pushing tunnel URL to repo..."
$baseUrl = "$url/v1"
Set-Content -Path "tunnel.url" -Value $baseUrl -NoNewline
git add tunnel.url
$diff = git diff --cached --name-only
if ($diff) { git commit -m "tunnel: update URL" }
git push origin HEAD --quiet

Write-Host ""
Write-Host "  OK  Proxy:  http://localhost:$PORT"
Write-Host "  OK  Tunnel: $baseUrl"
Write-Host "  OK  Claude can now connect automatically."
Write-Host ""
Write-Host "  Keep this window open. Ctrl+C to stop."
Write-Host ""

# ── Wait and cleanup on exit ──────────────────────────────────────────────────
try {
    Wait-Process -Id $ssh.Id
} finally {
    Write-Host "  Shutting down..."
    Stop-Process -Id $proxy.Id, $ssh.Id -Force -ErrorAction SilentlyContinue
    Remove-Item $tmpFile -Force -ErrorAction SilentlyContinue
    git rm -f tunnel.url 2>$null
    git commit -m "tunnel: closed" 2>$null
    git push origin HEAD --quiet 2>$null
}
