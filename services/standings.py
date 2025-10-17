import requests
from bs4 import BeautifulSoup
from utils.config_manager import load_config


def standings(division):
    #divisions = ["b2", "ct"]
    #url_id = [2394, 2377]
    #dictionary = dict(zip())
    config = load_config()
    url_id_map = config.get("standings", {})

    url = f"https://data.perpetualmotion.org/web-app/standings/{url_id_map[division]}"
    
    try:
        source = requests.get(url)
        source.raise_for_status()

        soup = BeautifulSoup(source.text, 'html.parser')

    except Exception as e:
        print(e)

    # table = soup.find("table", class_="activeStandings table table-condensed table-striped f-small").find_all("th")


    teams = soup.find("tbody").find_all("a")
    names = []

    for i in teams:
        #shorten team names to abbreviations 
        names.append((i.text).replace("The ", '').replace("Birthday", "Bday").replace("With", "W/"))
    
    scores = soup.find("tbody").find_all("td", class_="text-center")

    points = []
    #wins, losses, ties, points, spirit points: ['2', '0', '0', '4', '1.000', '5.00', ...

    heading = soup.find("table", class_="activeStandings table table-condensed table-striped f-small").find_all("th")
    
    labels = []
    count = 0 # how many in the header

    for head in heading: 
        labels.append(head.text)
        count += 1


    for i in scores:
        points.append(i.text)
    
    count = count - 2 #for place and team name
    indices = 0
    row = []
    result = []
    print("Count: ", count)

    if count == 5:
        for i in range(len(names)):
            result.append(names[i])
            #[TEAM NAME, ]
            for j in range(count):
            
                result.append(points[indices])

                indices += 1
            row.append(result)
            result=[] 

        labels = ["PL", "TEAM", "W", "L", "SPRT"]
        #headers = ['PL', 'TEAM', 'W', 'L', 'POINT']

        header_format = '{:<3} {:<17} {:<2} {:<2} {:<6}'

        chart = f"```\n{header_format.format(*labels)}\n"
        
        place = 1
            #[team , W, L, T, P]
        for r in row:
            chart += f"{place:<3} {r[0][:17].strip():<17} {r[1]:<2} {r[2]:<2} {r[5][:4]:<6}\n"
            place += 1
        chart += "```"
        
        message = "Please note that not all scores have been submitted at this moment. Check again later!"

    #   Win  Loss  Tie  Points count = 4

        # 	Win	 Loss  Tie	Points	Win Pct	 Spirit Avg count = 6 
    elif count == 6: 
        for i in range(len(names)):
            result.append(names[i])
            #[TEAM NAME, ]
            for j in range(count):
            
                result.append(points[indices])

                indices += 1
            row.append(result)
            result=[] 

        labels = ["PL", "TEAM", "W", "L", "SPRT"]
        #headers = ['PL', 'TEAM', 'W', 'L', 'POINT']

        header_format = '{:<3} {:<17} {:<2} {:<2} {:<6}'

        chart = f"```\n{header_format.format(*labels)}\n"
        
        place = 1
            #[team , W, L, T, P]
        for r in row:
            chart += f"{place:<3} {r[0][:17].strip():<17} {r[1]:<2} {r[2]:<2} {r[6][:4]:<6}\n"
            place += 1
        chart += "```"
        
        message = "It is possible some teams may have not submitted their scores yet!"
        
    else:
        labels = ["PL", "TEAM", "W", "L", "PT"]
        for i in range(len(names)):
            result.append(names[i])
            #[TEAM NAME, ]
            for j in range(count):
            
                result.append(points[indices])

                indices += 1
            row.append(result)
            result=[] 

        #headers = ['PL', 'TEAM', 'W', 'L', 'POINT']

        header_format = '{:<3} {:<17} {:<2} {:<2} {:<6}'

        chart = f"```\n{header_format.format(*labels)}\n"
        place = 1
            #[team , W, L, T, P]
        for r in row:
            chart += f"{place:<3} {r[0][:17].strip():<17} {r[1]:<2} {r[2]:<2} {r[4][:3]:<6}\n"
            place += 1
        chart += "```"
        
        message = "It is possible some teams may have not submitted their scores yet!"

    return chart, message