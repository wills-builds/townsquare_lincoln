@echo off
echo ============================================================
echo TownSquare: Lincoln
echo AI-Powered City Council Meeting Summaries
echo ============================================================
echo.

REM Check for API key
if "%ANTHROPIC_API_KEY%"=="" (
    echo WARNING: ANTHROPIC_API_KEY not set
    echo.
    set /p ANTHROPIC_API_KEY="Enter your Anthropic API key: "
    echo.
)

REM Check Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python not installed
    echo Install from python.org/downloads
    echo.
    pause
    exit /b 1
)

echo Starting Lincoln scraper...
echo This will take 1-2 minutes...
echo.

REM Run scraper
python lincoln_scraper.py

echo.
if %errorlevel% neq 0 (
    echo ============================================================
    echo ERROR: Scraper failed
    echo ============================================================
    echo.
    echo Check error messages above
    echo Common issues:
    echo - Run: pip install -r requirements.txt
    echo - Check internet connection
    echo - Verify API key is set
    echo.
) else (
    echo ============================================================
    echo SUCCESS!
    echo ============================================================
    echo.
    echo Check lincoln_meetings_report.md for summaries
    echo.
)

pause
