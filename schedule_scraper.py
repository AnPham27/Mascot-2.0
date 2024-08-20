import requests
from bs4 import BeautifulSoup
from datetime import date

def find_day(day, soup):
    dates = soup.find("table", class_="table table-condensed table-striped f-small").find_all("td")

    days = []

    for i in dates:
       
        days.append((i.text.replace("\t", "").replace("\n", "").replace("\r", "")))

    all_games = []
    for i in range(0, len(dates), 7):
        all_games.append(days[i:i+7])   

    #print(all_games)
    current_games = []
    for game in all_games:
        if day in game:
            current_games.append(game)
                

    print(current_games)
    return current_games

def play(division, day, month, date):

    divisions = ["ct", "c2"]
    url_id = [13552, 13402]
    
    dictionary = dict(zip(divisions, url_id))

    url = "https://data.perpetualmotion.org/web-app/team/" + str(dictionary[division])

    try:
        source = requests.get(url)
        source.raise_for_status()
        soup = BeautifulSoup(source.text, 'html.parser')

    except Exception as e:
        print(e)
    
    if len(date) == 1: 
        date = '0' + date
        print(date)
    
    today_date = f"{day} {month} {date}"
    print(today_date)
    current_games = find_day(today_date, soup)
    
    #need to set playoff dates
    playoff = ["Tue, Aug 20", "Thu, Aug 22"]

    if today_date in playoff:
        return(f"We have playoffs that day. Please check the schedule! (sorry i haven't had time to develop this lol)")
    elif len(current_games) == 0:
        return(f"Please double check the date - seems like it's not in the list of current games.")
    #['1', 'Thu, May 09', 'Frizzie McGuire(0-0-0) (0.00)', '', 'Margaret # 7', '6:30 PM', 'Light']
    
    message  = f"{today_date}: Our first game at **{current_games[0][5]}**, we are playing against **{current_games[0][2]}** wearing **{current_games[0][6]}** at **{current_games[0][4]}**. "
    message += f"For our second game at **{current_games[1][5]}**, we are playing against **{current_games[1][2]}** wearing **{current_games[1][6]}** at **{current_games[1][4]}**. "

    return message

