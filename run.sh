#!/bin/bash

echo "============================================================"
echo "TownSquare: Lincoln"
echo "AI-Powered City Council Meeting Summaries"
echo "============================================================"
echo

# Check for API key
if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "WARNING: ANTHROPIC_API_KEY not set"
    echo
    read -p "Enter your Anthropic API key: " ANTHROPIC_API_KEY
    export ANTHROPIC_API_KEY
    echo
fi

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python not installed"
    echo "Install from python.org/downloads"
    exit 1
fi

echo "Starting Lincoln scraper..."
echo "This will take 1-2 minutes..."
echo

# Run scraper
python3 lincoln_scraper.py

if [ $? -ne 0 ]; then
    echo
    echo "============================================================"
    echo "ERROR: Scraper failed"
    echo "============================================================"
    echo
    echo "Check error messages above"
    echo "Common issues:"
    echo "- Run: pip3 install -r requirements.txt"
    echo "- Check internet connection"
    echo "- Verify API key is set"
    echo
else
    echo
    echo "============================================================"
    echo "SUCCESS!"
    echo "============================================================"
    echo
    echo "Check lincoln_meetings_report.md for summaries"
    echo
fi
