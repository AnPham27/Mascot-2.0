import requests
from bs4 import BeautifulSoup

def status():
    
    # try:
    #     source = requests.get("https://guelph.ca/seasonal/sports-field-status/")
    #     source.raise_for_status()
    #     soup = BeautifulSoup(source.text, 'html.parser')
    # except Exception as e:
    #     print(e)

    headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"}
    source = requests.get("https://guelph.ca/seasonal/sports-field-status/", headers=headers)
    source.raise_for_status()
    soup = BeautifulSoup(source.text, 'html.parser')

    statement = soup.find(id="primary", class_="site-content").find("p")

    stat = []
    sent = ""

    for i in statement:
        sent += f"{i}"

    sent = sent.replace("<strong>", "").replace("</strong>", "")
    return sent
    