@echo off
setlocal EnableDelayedExpansion
title Printify Merch Automation — Installer

echo.
echo  =====================================================
echo   Printify Merch Automation — Windows Installer
echo  =====================================================
echo.

:: ── Check Python ──────────────────────────────────────────────────────────────
echo [1/5] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo  ERROR: Python not found.
    echo  Download and install Python 3.9+ from https://www.python.org/downloads/
    echo  Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)
for /f "tokens=*" %%v in ('python --version 2^>^&1') do echo  Found: %%v
echo.

:: ── Install dependencies ───────────────────────────────────────────────────────
echo [2/5] Installing Python dependencies...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo.
    echo  ERROR: pip install failed. Try running as Administrator.
    pause
    exit /b 1
)
echo  Done.
echo.

:: ── Set up .env ───────────────────────────────────────────────────────────────
echo [3/5] Setting up environment...
if exist .env (
    echo  .env already exists — skipping key setup.
    echo  To update your keys, edit .env manually.
) else (
    copy .env.example .env >nul
    echo.
    echo  You need three API keys. Enter them below.
    echo  (Keys are saved locally in .env — they are never uploaded anywhere)
    echo.

    set /p PRINTIFY_KEY= "  Printify API Key: "
    set /p PRINTIFY_SHOP= "  Printify Shop ID: "
    set /p OPENAI_KEY=   "  OpenAI API Key:   "

    :: Write the .env file
    (
        echo PRINTIFY_API_KEY=!PRINTIFY_KEY!
        echo PRINTIFY_SHOP_ID=!PRINTIFY_SHOP!
        echo OPENAI_API_KEY=!OPENAI_KEY!
    ) > .env

    echo.
    echo  Keys saved to .env
)
echo.

:: ── Create Merch output directory ─────────────────────────────────────────────
echo [4/5] Creating design output folder...
if not exist "%USERPROFILE%\Merch\Concepts" (
    mkdir "%USERPROFILE%\Merch\Concepts"
    echo  Created: %USERPROFILE%\Merch\Concepts
) else (
    echo  Already exists: %USERPROFILE%\Merch\Concepts
)
echo.

:: ── Verify Claude Code context ────────────────────────────────────────────────
echo [5/5] Verifying Claude Code project context...

:: CLAUDE.md lives in the project root — Claude Code reads it automatically
:: when this folder is opened. No files are written to ~/.claude/.
if exist "CLAUDE.md" (
    echo  CLAUDE.md is present. Claude Code will load it automatically
    echo  when you open this folder — no further setup needed.
) else (
    echo  WARNING: CLAUDE.md not found. Claude won't have project context.
)

:DONE
echo.
echo  =====================================================
echo   Installation complete!
echo  =====================================================
echo.
echo  Next steps:
echo    1. Open this folder in Claude Code
echo    2. Tell Claude: "generate concepts for [your brand idea]"
echo    3. Claude will walk you through the full workflow
echo.
echo  Or run scripts directly:
echo    python generate_concepts.py "YOUR BRAND TAGLINE"
echo    python reprice.py
echo.
pause
