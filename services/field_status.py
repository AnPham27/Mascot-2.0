import requests
from bs4 import BeautifulSoup

def stat():
    
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


    status_tag = soup.find("h2", class_="wp-block-heading", string=lambda text: text and "Sportsfields" in text)

    if status_tag:
        return status_tag.get_text(strip=True)
    else:
        return "Could not find field status."

def status():

    api_url = "https://guelph.ca/wp-json/wp/v2/seasonal/17897"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Referer": "https://www.google.com/"
    }
    
    try:
        response = requests.get(api_url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        html = data["content"]["rendered"]
        soup = BeautifulSoup(html, "html.parser")

        #Find <h2> tag mentioning sportsfields
        h2 = soup.find("h2", id=lambda v: v and "sportsfields" in v.lower())

        if h2:
            text = h2.get_text(separator=" ", strip=True)
            if "open" in text.lower():
                return f"☀️ {text}"
            elif "closed" in text.lower():
                return f"🚫 {text}"
            else:
                return text
        else:
            return "Could not find field status."

    except requests.exceptions.RequestException as e:
        return f"Error fetching field status: {e}"
    except ValueError:
        return "Error: Response was not JSON."