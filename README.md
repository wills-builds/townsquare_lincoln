# 🏛️ TownSquare: Lincoln

**AI-powered summaries of Lincoln, CA city council meetings**

Never miss what's happening in local government. Get plain-English summaries delivered automatically.

---

## What It Does

Automatically scrapes Lincoln city council meetings and generates:
- **Brief Summary** (2-3 sentences) - The essentials
- **Detailed Summary** (300-500 words) - Full breakdown of decisions, impact, and next steps

**Searches for meetings:**
- 3 months in the past (October 2025)
- 3 months in the future (April 2026)  
- 6-month window total

No more reading 50-page PDF agendas.

**Note:** The scraper fetches meetings from Lincoln's Granicus calendar. If Granicus is blocked on your network, it falls back to sample meetings. Try a different network (mobile hotspot, VPN) if scraping fails.

---

## Quick Start

### 1. Install Python & Dependencies

**Install Python:**
- Download Python 3.12+ from **python.org/downloads**
- **Windows:** Check "Add Python to PATH" during installation
- **Mac:** Python 3 is usually pre-installed, or use Homebrew: `brew install python3`

**Install Dependencies:**

Windows:
```powershell
# If pip works:
pip install -r requirements.txt

# If pip doesn't work:
python -m pip install -r requirements.txt

# Or try:
py -m pip install -r requirements.txt
```

Mac/Linux:
```bash
pip3 install -r requirements.txt

# Or:
python3 -m pip install -r requirements.txt
```

**If you need Visual Studio Build Tools (Windows only):**
1. Go to **visualstudio.microsoft.com/downloads/**
2. Download "Build Tools for Visual Studio 2022"
3. Install "Desktop development with C++"
4. Restart terminal and try again

### 2. Set Your API Key

```bash
# Windows
$env:ANTHROPIC_API_KEY="your-key-here"

# Mac/Linux
export ANTHROPIC_API_KEY="your-key-here"
```

Get your key at: **console.anthropic.com** (free credits to start)

### 3. Run It

**Windows:**
```bash
python lincoln_scraper.py
```

**Mac/Linux:**
```bash
python3 lincoln_scraper.py
```

**Output:** `lincoln_meetings_report.md` in the same folder

---

## What You Get

### Console Output:
```
============================================================
📋 Regular City Council Meeting
============================================================

💡 BRIEF SUMMARY:
Lincoln City Council will vote on board appointments, recognize 
Black History Month, and hear economic development updates.

📄 DETAILED SUMMARY:
The January 14th meeting covers several key items...
[Full detailed summary here]
============================================================
```

### File Output:
- `lincoln_meetings_report.md` - Markdown file with all summaries
- Easy to read, share, or publish

---

## Automate It

### Windows Task Scheduler:
1. Open Task Scheduler
2. Create Basic Task
3. Weekly trigger: Monday 9am
4. Action: `python C:\path\to\lincoln_scraper.py`

### Mac/Linux Cron:
```bash
# Edit crontab
crontab -e

# Add this line (runs every Monday at 9am)
0 9 * * 1 cd /path/to/townsquare_lincoln && python3 lincoln_scraper.py
```

### Cloud (Railway):
Deploy to Railway for $5/month:
1. Sign up at railway.app
2. `railway init`
3. `railway up`
4. Set cron: `0 9 * * 1`

Runs even when your computer is off.

---

## Customization

### Change Number of Meetings:
Edit `lincoln_scraper.py` line ~234:
```python
meetings = scraper.fetch_recent_meetings(limit=5)  # Default is 2
```

### Change Summary Style:
Edit the prompt in `summarize_with_claude()` function around line ~95

### Add More Meeting Types:
Currently scrapes City Council. Add Planning Commission, etc. by editing `fetch_recent_meetings()`

---

## Cost

**Free tier:**
- Anthropic gives $5 in free credits
- Each meeting costs ~$0.30-0.50 to summarize
- 10-15 free meetings to test

**After free tier:**
- ~$3-5/month for weekly summaries
- Claude API pricing: anthropic.com/pricing

---

## Project Structure

```
townsquare_lincoln/
├── lincoln_scraper.py        # Main scraper
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── LICENSE
└── assets/
    └── icons/
        ├── townsquare-icon.png
        └── townsquare-icon.ico
```

---

## Troubleshooting

### "No module named 'requests'"
```bash
pip install -r requirements.txt
```

### "ANTHROPIC_API_KEY not found"
Set it as environment variable (see Quick Start step 2)

### "Network error" / "403 Forbidden"
Lincoln's website blocks some networks. Try:
- Different WiFi
- Mobile hotspot
- VPN

### Summaries seem off
The AI reads the agenda, not the meeting minutes. For best results, run after meetings happen and minutes are posted.

---

## What's Next

This is the Lincoln-focused version. Want to expand?

Check out the full **TownSquare** project:
- Multi-city support
- Web interface
- Database storage
- Email alerts

GitHub: https://github.com/wills-builds/townsquare
---

## Contributing

Found a bug? Have an idea?
- Open an issue
- Submit a PR
- Fork it and make it yours

---

## License

MIT - Do whatever you want with it

---

## About

Built to make local government more accessible.

**Why Lincoln?**
Started here to prove the concept. Once this works smoothly, we'll expand to other cities.

**Questions?**
Open an issue on GitHub.

---

**Stay informed. Stay engaged. 🏛️**
