#!/usr/bin/env python3
"""
Lincoln CA Meeting Scraper - Proof of Concept
Scrapes city council meetings from Lincoln, CA and generates summaries
"""

import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader
from datetime import datetime
import os
import re
from anthropic import Anthropic

class LincolnMeetingScraper:
    """Scrape and summarize Lincoln CA city council meetings"""
    
    def __init__(self, api_key=None):
        self.base_url = "https://lincoln.granicus.com"
        self.api_key = api_key
        if api_key:
            self.client = Anthropic(api_key=api_key)
    
    def fetch_recent_meetings(self, limit=10):
        """
        Fetch meeting data from Granicus
        Returns list of meeting dictionaries with title, date, agenda_url, video_url
        Looks for meetings from 3 months ago to 3 months in the future (6 month window)
        Dynamically updates daily - always shows past 90 days and future 90 days
        """
        from datetime import datetime, timedelta
        from bs4 import BeautifulSoup
        import re
        
        print(f"🔍 Searching for Lincoln CA City Council meetings (past 3 months + future 3 months)...")
        
        meetings = []
        
        # Calculate 6-month window (updates daily)
        from datetime import datetime, timedelta
        today = datetime.now()
        three_months_ago = today - timedelta(days=90)
        three_months_ahead = today + timedelta(days=90)
        
        print(f"   Date range: {three_months_ago.strftime('%B %d, %Y')} to {three_months_ahead.strftime('%B %d, %Y')}")
        
        try:
            # Try to scrape Granicus calendar
            print("   Accessing Granicus calendar...")
            response = requests.get(
                "https://lincoln.granicus.com/ViewPublisher.php?view_id=2",
                timeout=15,
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Find all table rows
                rows = soup.find_all('tr')
                
                for row in rows:
                    try:
                        # Get row text
                        row_text = row.get_text()
                        
                        # Look for date patterns
                        date_match = re.search(r'(\d{1,2}/\d{1,2}/\d{4})', row_text)
                        if not date_match:
                            continue
                        
                        date_str = date_match.group(1)
                        
                        try:
                            meeting_date = datetime.strptime(date_str, "%m/%d/%Y")
                        except:
                            continue
                        
                        # Check if within 6-month window
                        if not (three_months_ago <= meeting_date <= three_months_ahead):
                            continue
                        
                        # Find agenda link
                        agenda_link = row.find('a', text=re.compile('Agenda', re.I))
                        if not agenda_link:
                            continue
                        
                        href = agenda_link.get('href')
                        if not href:
                            continue
                        
                        # Build full URL
                        if href.startswith('http'):
                            full_url = href
                        elif href.startswith('/'):
                            full_url = f"https://lincoln.granicus.com{href}"
                        else:
                            full_url = f"https://lincoln.granicus.com/{href}"
                        
                        # Extract meeting title from row
                        title = "City Council Meeting"
                        cells = row.find_all(['td', 'th'])
                        for cell in cells:
                            cell_text = cell.get_text().strip()
                            if cell_text and len(cell_text) > 5 and cell_text != date_str:
                                title = cell_text
                                break
                        
                        meetings.append({
                            "title": title[:100],
                            "date": meeting_date.strftime("%Y-%m-%d"),
                            "agenda_url": full_url,
                            "type": "City Council" if "council" in title.lower() else "Meeting"
                        })
                        
                    except Exception as e:
                        continue
                
                print(f"   ✅ Scraped {len(meetings)} meetings from Granicus")
            
        except Exception as e:
            print(f"   ⚠️  Could not scrape Granicus: {e}")
        
        # If scraping failed or found nothing, use fallback
        if len(meetings) == 0:
            print("   Using fallback sample meetings...")
            meetings = [
                # Past meetings
                {
                    "title": "Regular City Council Meeting",
                    "date": "2026-01-14",
                    "agenda_url": "https://www.lincolnca.gov/media/bpqgyvdq/113-1142026-regular-city-council-and-edc-meeting-agendas.pdf",
                    "type": "City Council"
                },
                {
                    "title": "Special Meeting - Airport Committee",
                    "date": "2026-01-21",
                    "agenda_url": "https://www.lincolnca.gov/media/f2vp233c/120-1212026-special-city-council-airport-committee-fioc-parks-recreation-committee-meeting-agendas.pdf",
                    "type": "Special Meeting"
                },
                # Future meetings (from search results)
                {
                    "title": "Regular Council Meeting",
                    "date": "2026-01-27",
                    "agenda_url": "https://www.lincolnca.gov/",  # Agenda will be posted closer to date
                    "type": "City Council"
                },
                {
                    "title": "Regular City Council Meeting",
                    "date": "2026-02-18",
                    "agenda_url": "https://www.lincolnca.gov/",  # Agenda will be posted closer to date
                    "type": "City Council"
                },
                {
                    "title": "Special Meeting",
                    "date": "2026-04-15",
                    "agenda_url": "https://www.lincolnca.gov/",  # Agenda will be posted closer to date
                    "type": "Special Meeting"
                }
            ]
        
        # Sort by date (most recent first)
        meetings.sort(key=lambda x: x['date'], reverse=True)
        
        print(f"✅ Found {len(meetings)} meetings")
        return meetings[:limit]
        
        print(f"✅ Found {len(sample_meetings)} recent meetings")
        return sample_meetings[:limit]
    
    def download_pdf(self, url, filename):
        """Download PDF from URL"""
        print(f"📥 Downloading: {filename}")
        try:
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # Use temp directory that works on all OS
            import tempfile
            temp_dir = tempfile.gettempdir()
            filepath = os.path.join(temp_dir, filename)
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            
            print(f"✅ Downloaded: {filepath}")
            return filepath
        except Exception as e:
            print(f"❌ Error downloading {url}: {e}")
            return None
    
    def extract_text_from_pdf(self, pdf_path, max_pages=20):
        """Extract text from PDF, limiting to first N pages for POC"""
        print(f"📄 Extracting text from {pdf_path} (first {max_pages} pages)...")
        try:
            reader = PdfReader(pdf_path)
            text = ""
            pages_to_read = min(len(reader.pages), max_pages)
            
            for i in range(pages_to_read):
                page = reader.pages[i]
                text += page.extract_text() + "\n\n"
            
            print(f"✅ Extracted {len(text)} characters from {pages_to_read} pages")
            return text
        except Exception as e:
            print(f"❌ Error extracting PDF text: {e}")
            return None
    
    def clean_text(self, text):
        """Clean extracted text - remove excessive whitespace, etc."""
        # Remove multiple newlines
        text = re.sub(r'\n{3,}', '\n\n', text)
        # Remove multiple spaces
        text = re.sub(r' {2,}', ' ', text)
        return text.strip()
    
    def summarize_with_claude(self, meeting_text, meeting_info):
        """Generate AI summary of meeting using Claude"""
        if not self.api_key:
            print("⚠️  No API key provided - skipping AI summarization")
            return "AI summarization skipped (no API key provided)"
        
        print(f"🤖 Generating AI summary for {meeting_info['title']}...")
        
        prompt = f"""You are analyzing a city council meeting agenda for Lincoln, CA.

Meeting: {meeting_info['title']}
Date: {meeting_info['date']}
Type: {meeting_info['type']}

Please provide TWO summaries:

1. **BRIEF SUMMARY** (2-3 sentences max): The absolute essentials - what happened and what matters most to residents.

2. **DETAILED SUMMARY** (300-500 words): Cover:
   - Key Decisions & Votes: What major items are on the agenda or were decided?
   - Public Impact: Which items would most affect residents?
   - Financial Items: Any budget items, expenditures, or fiscal decisions?
   - Development/Planning: Any zoning, construction, or development items?
   - Upcoming Actions: What's coming next or needs public input?

Format your response EXACTLY like this:

BRIEF:
[2-3 sentence summary here]

DETAILED:
[Detailed summary here]

Make it accessible to everyday citizens. Use clear language, avoid jargon.

Here's the meeting agenda text:

{meeting_text[:15000]}  

"""
        
        try:
            message = self.client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1500,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            summary = message.content[0].text
            print(f"✅ Summary generated ({len(summary)} chars)")
            return summary
        
        except Exception as e:
            print(f"❌ Error generating summary: {e}")
            return f"Error generating summary: {e}"
    
    def process_meeting(self, meeting):
        """Full processing pipeline for a single meeting"""
        print(f"\n{'='*60}")
        print(f"Processing: {meeting['title']} ({meeting['date']})")
        print(f"{'='*60}\n")
        
        # Check if agenda is available (not just a placeholder URL)
        if meeting['agenda_url'].endswith('.gov/') or 'lincolnca.gov/' == meeting['agenda_url']:
            print(f"⏳ Agenda not yet published (future meeting)")
            print(f"   Check back closer to {meeting['date']}")
            return None
        
        # Download PDF
        pdf_filename = f"meeting_{meeting['date']}_{meeting['type'].replace(' ', '_')}.pdf"
        pdf_path = self.download_pdf(meeting['agenda_url'], pdf_filename)
        
        if not pdf_path:
            return None
        
        # Extract text
        raw_text = self.extract_text_from_pdf(pdf_path)
        if not raw_text:
            return None
        
        cleaned_text = self.clean_text(raw_text)
        
        # Generate summary
        summary = self.summarize_with_claude(cleaned_text, meeting)
        
        # Display summary in console
        if summary and summary != "AI summarization skipped (no API key provided)":
            # Extract brief and detailed summaries
            if "BRIEF:" in summary and "DETAILED:" in summary:
                parts = summary.split("DETAILED:")
                brief = parts[0].replace("BRIEF:", "").strip()
                detailed = parts[1].strip() if len(parts) > 1 else ""
                
                print(f"\n{'='*60}")
                print(f"📋 {meeting['title']}")
                print(f"{'='*60}")
                print(f"\n💡 BRIEF SUMMARY:")
                print(f"{brief}")
                print(f"\n📄 DETAILED SUMMARY:")
                print(f"{detailed}")
                print(f"{'='*60}\n")
            else:
                # Fallback if format doesn't match
                print(f"\n{'='*60}")
                print(f"📋 SUMMARY: {meeting['title']}")
                print(f"{'='*60}")
                print(summary)
                print(f"{'='*60}\n")
        
        return {
            "meeting": meeting,
            "summary": summary,
            "full_text_preview": cleaned_text[:500] + "..."
        }
    
    def generate_report(self, processed_meetings, output_file="lincoln_meetings_report.md"):
        """Generate a markdown report of all processed meetings"""
        print(f"\n📝 Generating report: {output_file}")
        
        report = f"""# Lincoln CA City Council Meetings Summary
Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}

This report summarizes recent Lincoln, CA city council meetings to help residents stay informed about local government decisions.

---

"""
        
        for item in processed_meetings:
            if not item:
                continue
            
            meeting = item['meeting']
            summary = item['summary']
            
            report += f"""
## {meeting['title']}
**Date:** {meeting['date']}  
**Type:** {meeting['type']}  
**Agenda:** [View PDF]({meeting['agenda_url']})

### Summary
{summary}

---

"""
        
        # Save to current directory
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"✅ Report saved to: {output_file}")
        return output_file


def main():
    """Main execution"""
    print("🏛️  Lincoln CA Meeting Scraper")
    print("=" * 60)
    
    # Get API key from environment or config file
    api_key = os.getenv('ANTHROPIC_API_KEY')
    
    # Try to load from config.py if not in environment
    if not api_key:
        try:
            import config
            api_key = config.ANTHROPIC_API_KEY
            print("✅ Loaded API key from config.py")
        except (ImportError, AttributeError):
            pass
    
    if not api_key:
        print("\n⚠️  WARNING: No ANTHROPIC_API_KEY found")
        print("   Option 1: Set environment variable:")
        print("     Windows: $env:ANTHROPIC_API_KEY='your-key'")
        print("     Mac/Linux: export ANTHROPIC_API_KEY='your-key'")
        print("   Option 2: Create config.py from config.template.py")
        print("   Summaries will be skipped.\n")
        api_key = None
    
    # Initialize scraper
    scraper = LincolnMeetingScraper(api_key=api_key)
    
    # Fetch meetings (3 months past + 3 months future, up to 10 meetings)
    meetings = scraper.fetch_recent_meetings(limit=10)
    
    # Process each meeting
    processed = []
    for meeting in meetings:
        result = scraper.process_meeting(meeting)
        if result:
            processed.append(result)
    
    # Generate report
    if processed:
        report_path = scraper.generate_report(processed)
        print(f"\n✅ SUCCESS! Report generated at: {report_path}")
    else:
        print(f"\n❌ No meetings processed successfully")


if __name__ == "__main__":
    main()
