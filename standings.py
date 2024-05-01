import requests
from bs4 import BeautifulSoup



def standings(division):
    divisions = ["b7", "ct", "b2", "c", "b2/c1", "c2"]
    url_id = [2037, 2045, 2051, 2052, 2057, 2058]

    dictionary = dict(zip(divisions, url_id))

    url = "https://data.perpetualmotion.org/web-app/standings/" + str(dictionary[division])

    try:
        source = requests.get(url)
        source.raise_for_status()

        soup = BeautifulSoup(source.text, 'html.parser')

    except Exception as e:
        print(e)

    # table = soup.find("table", class_="activeStandings table table-condensed table-striped f-small").find_all("th")


    teams = soup.find("tbody").find_all("a")

    waiting = False
    names = []

    for i in teams:
        #shorten team names to abbreviations 
        names.append((i.text).replace("The ", '').replace("Birthday", "Bday").replace("With", "W/"))
        
        next_element = i.next_sibling.strip()
        #print(next_element)
        if "**" in next_element:
            waiting = True

    
    scores = soup.find("tbody").find_all("td", class_="text-center")

    point = []
    #wins, losses, ties, points, spirit points

    for i in scores:
        point.append(i.text)
        
    #no spirit score yet ~ less than 24 hours

    if len(point) == (len(names) * 4):
        count = 0
        total_num_scores = 4
        total_scores = len(names) * total_num_scores
        result = []

        #[team , W, L, T, P]
        row = []
        for i in range(len(names)):
            result.append(names[i])
            #[TEAM NAME, ]
            for j in range(total_num_scores):
                
                result.append(point[count])

                count += 1
            row.append(result)
            result=[]  


        headers = ['PL', 'TEAM', 'W', 'L', 'PTS']
        header_format = '{:<3} {:<17} {:<2} {:<2} {:<6}'

        chart = f"```\n{header_format.format(*headers)}\n"
        message = ""
        place = 1
            #[team , W, L, T, P]
        for r in row:
            chart += f"{place:<3} {r[0][:17].strip():<17} {r[1]:<2} {r[2]:<2} {r[4]:<6}\n"

            if waiting == True:
                message+= "Please note: Not all scores have been submitted at this moment. Check again later!"

    
        chart += "```"

    #spirit points are available
    else:
        count = 0
        total_num_scores = 5
        total_scores = len(names) * total_num_scores
        result = []

        #[team , W, L, T, P, SPIRIT]
        row = []
        for i in range(len(names)):
            result.append(names[i])
            #[TEAM NAME, ]
            for j in range(total_num_scores):
                
                result.append(point[count])

                count += 1
            row.append(result)
            result=[]  
            

        headers = ['PL', 'TEAM', 'W', 'L', 'SPRT']
        header_format = '{:<3} {:<17} {:<2} {:<2} {:<6}'

        chart = f"```\n{header_format.format(*headers)}\n"
        message = ""
        place = 1
            #[team , W, L, T, P]
        for r in row:
            chart += f"{place:<3} {r[0][:17].strip():<17} {r[1]:<2} {r[2]:<2} {r[5]:<6}\n"

            message += "\nPlease note: Not all scores have been submitted at this moment. Please check again later!"

            place += 1
        chart += "```"
    
    return(chart, message)