import requests
from bs4 import BeautifulSoup

def status():
    
    url = "https://guelph.ca/seasonal/sports-field-status/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/"
    }

    source = requests.get(url, headers=headers)
    source.raise_for_status()

    soup = BeautifulSoup(source.text, "html.parser")
    status_tag = soup.find("h2", id="h-sportsfields-are-open")

    if status_tag:
        return status_tag.get_text(strip=True)
    else:
        return "Could not find field status"
    