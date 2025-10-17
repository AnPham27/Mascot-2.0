import requests
from bs4 import BeautifulSoup
from datetime import datetime
import discord
from utils.embed_formatter import sch_embed
from utils.config_manager import load_config

def play_short(division, mmdd):
    if len(mmdd) == 3:
        mmdd = '0' + mmdd  #829 = 0829

    try:
        current_year = datetime.now().year
        dt = datetime.strptime(f"{current_year}{mmdd}", "%Y%m%d")

        # if the date already passed this year, assume it's next year
        today = datetime.now()
        if dt < today and dt.month < today.month:
            dt = datetime.strptime(f"{current_year + 1}{mmdd}", "%Y%m%d")
            
        # Format exactly like "Thu, May 08"
        full_date_str = dt.strftime("%a, %b %d")  # Thu, May 08
        #print(full_date_str)
        day_str, month_str, day_num = full_date_str.split()    # "Thu,", "May", "08"

        return play(division, day_str, month_str, day_num)
    except ValueError:
        return "Invalid date format. Use MMDD (e.g. 0508 for May 8)."
    

def play_short_embed(division, mmdd):
    if len(mmdd) == 3:
        mmdd = '0' + mmdd  #829 = 0829

    try:
        current_year = datetime.now().year
        dt = datetime.strptime(f"{current_year}{mmdd}", "%Y%m%d")

        # if the date already passed this year, assume it's next year
        today = datetime.now()
        if dt < today and dt.month < today.month:
            dt = datetime.strptime(f"{current_year + 1}{mmdd}", "%Y%m%d")

        # Format exactly like "Thu, May 08"
        full_date_str = dt.strftime("%a, %b %d")  # Thu, May 08
        #print(full_date_str)
        day_str, month_str, day_num = full_date_str.split()    # "Thu,", "May", "08"

        return play_embed(division, day_str, month_str, day_num)
    except ValueError:
        return "Invalid date format. Use MMDD (e.g. 0508 for May 8)."
    

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
                

    #print(current_games)
    return current_games

def play(division, day, month, date):

    divisions = ["b2", "ct"]
    url_id = [16259, 16039]
    
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
        #print(date)
    
    today_date = f"{day} {month} {date}"
    print(today_date)
    current_games = find_day(today_date, soup)

    print(len(current_games))
    
    #need to set playoff dates
    playoff = ["Sun, Jan 11"]
    holidays = ["Sun, Dec 21", "Sun, Dec 28"]

    if today_date in playoff:
        return(f"We have playoffs that day. Please check the schedule! (sorry i haven't had time to develop this lol)")
    elif today_date in holidays:
        return(f"No games! Enjoy the holidays!")
    elif len(current_games) == 0:
        return(f"Please double check the date - seems like it's not in the list of current games.")
    #['1', 'Thu, May 09', 'Frizzie McGuire(0-0-0) (0.00)', '', 'Margaret # 7', '6:30 PM', 'Light']

    elif len(current_games) % 2 == 0: #two games
        message  = f"{today_date}: Our first game at **{current_games[0][5]}**, we are playing against **{current_games[0][2]}** wearing **{current_games[0][6]}** at **{current_games[0][4]}**. "
        message += f"For our second game at **{current_games[1][5]}**, we are playing against **{current_games[1][2]}** wearing **{current_games[1][6]}** at **{current_games[1][4]}**. "
    
    elif len(current_games) % 2 == 1: #one game
        message = f"{today_date}: At **{current_games[0][5]}**, we are playing against **{current_games[0][2]}** wearing **{current_games[0][6]}** at **{current_games[0][4]}**. "
    return message



def play_embed(division, day, month, date):
    """Returns a discord.Embed for the games on a given day."""

    today_date = f"{day} {month} {date}"

    config = load_config()
    #url_id_map = {"b2": 16259, "ct": 16039}
    url_id_map = config.get("divisions", {})
    playoff = config.get("playoff_dates", [])
    holidays = config.get("holidays", [])
    url = f"https://data.perpetualmotion.org/web-app/team/{url_id_map[division]}"


    try:
        source = requests.get(url)
        source.raise_for_status()
        soup = BeautifulSoup(source.text, 'html.parser')
    except Exception as e:
        print(e)
        return None
    
    if len(date) == 1: 
        date = '0' + date
    #print(date)
    
    today_date = f"{day} {month} {date}"
    #print(today_date)
    current_games = find_day(today_date, soup)

    #print(len(current_games))
    
    #need to set playoff dates
    #playoff = ["Sun, Jan 11"]
    #holidays = ["Sun, Dec 21", "Sun, Dec 28"]
    current_games = find_day(today_date, soup)

    #print(len(current_games))

    print(today_date)

    #playoff check
    if today_date in playoff:
        
        embed = discord.Embed(
            title=today_date,
            description="We have playoffs that day. Please check the schedule! (sorry i haven't had time to develop this lol)",
            color=0xffaa00
        )
        return embed

    #holiday check
    elif today_date in holidays:
        
        embed = discord.Embed(
            title=today_date,
            description="No games! Enjoy the holidays!",
            color=0x00ffaa
        )
        return embed

    #incorrect date? no games
    if not current_games:
        embed = discord.Embed(
            title=today_date,
            description="Please double check the date - seems like it's not in the list of current games.",
            color=0xd52079
        )
        return embed

    # Normal game logic
    if len(current_games) % 2 == 1:  # one game
        matches = [{
            "time": current_games[0][5],
            "location": current_games[0][4],
            "colour": current_games[0][6],
            "opponent": current_games[0][2]
        }]
        return sch_embed(today_date, matches)

    elif len(current_games) % 2 == 0:  # two games
        matches = [
            {
                "time": current_games[0][5],
                "location": current_games[0][4],
                "colour": current_games[0][6],
                "opponent": current_games[0][2]
            },
            {
                "time": current_games[1][5],
                "location": current_games[1][4],
                "colour": current_games[1][6],
                "opponent": current_games[1][2]
            }
        ]
        return sch_embed(today_date, matches)
