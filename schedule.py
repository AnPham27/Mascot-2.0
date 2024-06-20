import requests
from bs4 import BeautifulSoup
from datetime import date
import calendar

def find_day(division, soup):

    if division in ("b7", "b2", "c", "c2"):

        day = soup.find("div", class_="d-flex justify-content-between border-bottom fw-bold pb-1").find_all("div")
        
    if division in ("ct", "b2/c1"):
        day = soup.find_all("td", class_="xl7725052")

    
    return day

    
def find_time_slot(todays_games, team_num, division):
    
    if division == "b7":

        time_slot = 2 #first time slot

        for i in range(1):
            if f'{team_num}' in todays_games[i]:
                #[['Monday, May 6', 'Centennial Soccer Dome', '2', '5'], 'White', 'White']
                if f'{team_num}' in todays_games[i][2] or f'{team_num}' in todays_games[i][3]:
                    time_slot = 0
                    print("yuh")
                elif f'{team_num}' in todays_games[i][5] or f'{team_num}' in todays_games[i][4]:
                    time_slot = 1 # second time slot 
                    print("meep")

                
                return time_slot
    return time_slot

def find_team_dictionary(division, soup):
    numbers = []
    teams = []

    if division in ("b7", "b2", "c", "c2"):

        numbers = soup.find("table", class_="ms-sm-auto").find_all(class_="team-num")
        teams = soup.find("table", class_="ms-sm-auto").find_all("a")

        columns = soup.find_all(class_="col-12 col-sm-6")
        
        # Check if there are at least two occurrences
        if len(columns) >= 2:
            # Access the second occurrence
            second_column = columns[1]
            
            # Process the second column
            numbers_second_column = second_column.find_all(class_="team-num")
            teams_second_column = second_column.find_all("a")

            # Append data from the second column to the existing lists
            numbers.extend(numbers_second_column)
            teams.extend(teams_second_column)
        
    if division == "ct":
        numbers = soup.find("table").find_all(class_="xl7525052")
        teams = soup.find("table").find_all(class_="xl7425052")
    
    if division == "b2/c1":
        numbers = soup.find("table").find_all(class_="xl7525052")
        teams = soup.find("table").find_all(class_="xl6926374")

    number = []
    team = []

    for i in numbers:
        number.append(i.text)

    for i in teams:
        team.append(i.text.replace("The ", '').replace('Team ', ''))

    dictionary = dict(zip(number, team))
    
    if division == "ct":
        dictionary['12'] = 'The Sackler Family Team for Evidence-Based Frisbee'
        dictionary.popitem()
        dictionary['13'] = 'The Frizzly Bears'
        #this site is not right. excuse this please 
    
    if division == "c":
        dictionary['7'] = "Team Dump Truck"
    
    print(dictionary)
    return dictionary

def find_time_index(time_dictionary, today_date, todays_games, team_num, division):

    time_index = []
    time_index.append(0)
    time_index.append(1)

    if division == "b7":

        #if there are more than 1 games that day
        if len(time_dictionary[today_date]) > 1:
            # if flagged, take second time group 
            time_slot = find_time_slot(todays_games, team_num, division)
            #if 0 = first time slot, if 1 = second time slot, 2 = third time slot

            if time_slot == 1:
                time_index = []
                time_index.append(1)
                #time_index.append(3)
            
            if time_slot == 2:
                time_index=[]
                time_index.append(2)
            
            #if time_slot == 0:
                
                

            
            
    return time_index

def find_field_num(division, soup):
    
    if division in ("b7", "b2", "c", "c2"):
        nums =[]

        field_num = soup.find_all("a", target="_blank")
        for i in field_num:
            nums.append(i.text)

    if division in ("ct", "b2/c1"):
        nums = []

        field_num = soup.find_all(class_="xl7625052", style="height:12.75pt;border-top:none")

        for i in field_num:
            nums.append(i.text.replace("\r\n ", ""))
           
        print(nums)
    return nums

def find_game_header(division, soup):
    if division in ("b7"):
        game_header = soup.find(class_="schedule-times-header-row").find_all(class_="fw-bold border-bottom border-dark")
        times = []

        columns = soup.find_all(class_="schedule-times-header-row")   
        # Access the second occurrence
        second_column = columns[1]
        
        # Process the second column
        times_second_column = second_column.find_all(class_="fw-bold border-bottom border-dark")
    

        # Append data from the second column to the existing lists
        game_header.extend(times_second_column)

    if division in ("b2", "c", "c2"):
        game_header = soup.find(class_="schedule-times-header-row").find_all(class_="fw-bold border-bottom border-dark")
        times = []

        columns = soup.find_all(class_="schedule-times-header-row")  

    for i in game_header:
        times.append(i.text)

    return times

def find_opponents(division, soup, days, field_num):

    #['Thursday, August 10', 'Margaret # 4', '1', '12', '12', '9'], 'Dark', 'White']
    if division == ("b7"):
        opponent = soup.find("tbody").find_all_next("a", class_="team-link")
        opponents = []
        count = 0
        for i in opponent:
            #opponents.append(days[len(opponents)])
            opponents.append(i.text) 
            count+= 1  
        #print(opponents)
        #['1', '4', '2', '5', '3', '6']
        count = 0
        # Field #, LEFT , RIGHT, LEFT, RIGHT 
        #      0 ,   1 ,    2,     3 ,   4

        split_arrays = []
        chunk_size = 4
        n = len(opponents)


        for i in range(0, n, chunk_size):
            sub_array = []

            for j in range(i, min(i + chunk_size, n)):
                
                sub_array.append(opponents[j])
            

            #sub_array.insert(0, days[count])
            split_arrays.append(sub_array)
    
        #date each game: 
        # DATE, Field #, LEFT , RIGHT, LEFT, RIGHT 
        # 0  ,    1 ,     2,     3 ,    4 ,   5
        for i, group in enumerate(split_arrays):
            field_index = i % len(field_num)
            group.insert(0, field_num[field_index])
            group.insert(0, days[i // 7])
    
        #print(split_arrays)
    
    if division in ("b2", "c", "c2"):
        opponent = soup.find("tbody").find_all_next("a", class_="team-link")
        opponents = []
        count = 0
        for i in opponent:
            #opponents.append(days[len(opponents)])
            opponents.append(i.text) 
            count+= 1
            print(i.text.replace("\xa0", ""))
        #print(opponents)
        #['1', '4', '2', '5', '3', '6']
        count = 0
        # Field #, LEFT , RIGHT, LEFT, RIGHT 
        #      0 ,   1 ,    2,     3 ,   4

        split_arrays = []
        chunk_size = 4
        n = len(opponents)


        for i in range(0, n, chunk_size):
            sub_array = []

            for j in range(i, min(i + chunk_size, n)):
                
                sub_array.append(opponents[j])
            

            #sub_array.insert(0, days[count])
            split_arrays.append(sub_array)
    
        #date each game: 
        # DATE, Field #, LEFT , RIGHT, LEFT, RIGHT 
        # 0  ,    1 ,     2,     3 ,    4 ,   5
        for i, group in enumerate(split_arrays):
            field_index = i % len(field_num)
            group.insert(0, field_num[field_index])
            group.insert(0, days[i // 8])
        
    
    if division in ("ct", "b2/c1"):
        opponents = []
        index_0 = soup.find_all(class_="xl8225052", style="border-left:none")
        index_1 = soup.find_all(class_="x18225052", style="border-left:none")
        index_2 = soup.find_all(class_="x17025052", style="border-left:none")
        index_3 =soup.find_all(class_="x18025052", style="border-left:none")

        
        # index_0.extend(index_1)
        # index_0.extend(index_2)
        # index_0.extend(index_3)

        for i in index_0:
            #opponents.append(days[len(opponents)])
            # opponents.append(i.text.replace("\xa0", "")) 
            print(i.text.replace("\xa0", ""))

        split_arrays = []
        chunk_size = 4
        n = len(opponents)


        for i in range(0, n, chunk_size):
            sub_array = []

            for j in range(i, min(i + chunk_size, n)):
                
                sub_array.append(opponents[j])
            

            #sub_array.insert(0, days[count])
            split_arrays.append(sub_array)
    
        #date each game: 
        # DATE, Field #, LEFT , RIGHT, LEFT, RIGHT 
        # 0  ,    1 ,     2,     3 ,    4 ,   5
        for i, group in enumerate(split_arrays):
            field_index = i % len(field_num)
            group.insert(0, field_num[field_index])
            group.insert(0, days[i // 8])


    print(sub_array)
    print(split_arrays)
    return sub_array, split_arrays

def colour(division, team_num, first, second):
    flag = 0
    #they play 1 game in the night
    if division == "b7":
        if not first:
            first=second
            second=[]
            #print(len(current_games))
            first[0].pop(2)
            first[0].pop(2)
            colour = ''
           
            #first game colour
            if f'{team_num}' == first[0][2]:
                colour = 'Dark'
                first.append(colour)
                

            if f'{team_num}' == first[0][3]:
                colour = 'White'
                
                first.append(colour)
            flag = 1

            
    if first:
        if f'{team_num}' == first[0][2]:
            colour = 'Dark'
            first.append(colour)
            

        if f'{team_num}' == first[0][3]:
            colour = 'White'
            
            first.append(colour)
    
    if second:
        if f'{team_num}' == second[0][4]:
            second_colour = 'Dark'
            second.append(second_colour)

        if f'{team_num}' == second[0][5]:
            second_colour = 'White'
            second.append(second_colour)
  
    return first, second, flag
            


    
def get_upcoming_schedule(division, day, month, date, team_num):

    divisions = ["b7", "ct", "b2", "c", "b2/c1", "c2"]
    url_id = [2037, 2045, 2051, 2052, 2057, 2058]
    #url_id = [2037, 2045, 2051, 2052, 2057, 2011]
    dictionary = dict(zip(divisions, url_id))

    url = "https://data.perpetualmotion.org/allSports/schedule.php?leagueID=" + str(dictionary[division])
    
    try:
       
        source = requests.get(url)
        
        source.raise_for_status()

        soup = BeautifulSoup(source.text, 'html.parser')
        
        """
        with open("Ultimate Frisbee - B7 Division - Monday.html", "r") as f:
            soup = BeautifulSoup(f, "html.parser")
        """
    except Exception as e:
        print(e)
    
    #print(soup.prettify())

    today_date = f"{day} {month} {date}"
    print(today_date)
    #lists team number and name 
    dictionary = find_team_dictionary(division, soup)

    day = find_day(division, soup)
    #day = soup.find("table").find_all("th", id="week_header")
    print(day)
    days = []

    for i in day:
        print(i.text)
        if not (i.text).startswith("Week "):
            days.append(i.text)
        
    print(days)
    
    #need to set playoff dates
    playoff = ["Mon, Jun 24", "Tue, Jun 25", "Wed, Jun 26", "Thu, Jun 27"]

    if today_date in playoff:
        return(f"We have playoffs that day. Please check the schedule! (sorry i haven't had time to develop this lol)")
    elif today_date in days:
        print("yes")
    else:
        return(f"There are no games on {today_date}. Check for a different date")

    #print(days)

    fields_num = find_field_num(division, soup)
    #print(fields_num)

    #print(nums)

    # left_team = soup.find("tbody").find_all_next("a")

    #print(split_arrays)
    sub_array, split_arrays = find_opponents(division, soup, days, fields_num)

    #games we are playing
    flagged_arrays = []
    todays_games = []

    for sub_array in split_arrays:
        if f'{today_date}' in sub_array:
            todays_games.append(sub_array)
        
        if f'{team_num}' in sub_array:
            flagged_arrays.append(sub_array)

    #print(flagged_arrays)
    #print(todays_games)

    #today_date = "Thursday, May 18"

    current_games = []

    for array in flagged_arrays:
        if array[0] == today_date:
            current_games.append(array)

    #print(current_games)
    #print(current_games)
    #[['Thursday, August 10', 'Margaret # 4', '1', '12', '12', '9'], 'Dark', 'White']
    # DATE, Field #, LEFT , RIGHT, LEFT, RIGHT 
    # 0  ,    1 ,     2,     3 ,    4 ,   5
    
    times = find_game_header(division, soup)
    #find the times of each game and append it. 
  
    
    scheduled_time = []

    # Initialize a list to store the current group of times
    current_group = []

    if division == "b7":
        for time in times:
        #check if the time starts with '6' (for 6pm)
            if time.startswith('6') or time.startswith('7'):
                #if the current group is not empty, append it to scheduled_time
                if current_group:
                    scheduled_time.append(current_group)
                #start a new group with the current time
                current_group = [time]
            else:
                #append the current time to the current group
                current_group.append(time)
    else:

        for time in times:
            #check if the time starts with '6' (for 6pm)
            if time.startswith('6'):
                #if the current group is not empty, append it to scheduled_time
                if current_group:
                    scheduled_time.append(current_group)
                #start a new group with the current time
                current_group = [time]
            else:
                #append the current time to the current group
                current_group.append(time)

    #append the last group to scheduled_time if it's not empty
    if current_group:
        scheduled_time.append(current_group)

  
    #print(scheduled_time)

    time_dictionary = dict(zip(days, scheduled_time))
    #print(time_dictionary)

    #print(time_dictionary)
    time_index = find_time_index(time_dictionary, today_date, todays_games, team_num, division)
    
    print("time index", time_index)
    first = []
    second = []
    flag = 0 

    for i in range (len(current_games)):
        for j in range (len(current_games[0])):

            if j < 4 and current_games[i][j] == f'{team_num}':
                first.append(current_games[i])
            
            if j > 3 and current_games[i][j] == f'{team_num}':
                second.append(current_games[i])


    first, second, flag = colour(division, team_num, first, second)



    print(first)
    
    print(second)
    print("times", times)

    print("Time dictionary: ", time_dictionary)
    
    #print(time_dictionary)
    #[['Thursday, August 10', 'Margaret # 4', '1', '12', '12', '9'], 'Dark', 'White', time]
    # DATE, Field #, LEFT , RIGHT, LEFT, RIGHT 
    # 0  ,    1 ,     2,     3 ,    4 ,   5

    #four cases:
    # if games are on separate fields 
    # if games are on the same field
    # if first game is practice
    # if second game is practice

    message = ""
    #print(first)
    # First game
    if first[0][1] != "Practice Area":
        if first[1] == 'Dark':
            message = f"{today_date}: our first game at **{time_dictionary[today_date][time_index[0]]}**, we are playing against **{dictionary[first[0][3]].strip()}** wearing **{first[1]}** on **{first[0][1]}**. "
        elif first[1] == 'White':
            message = f"{today_date}: our first game at **{time_dictionary[today_date][time_index[0]]}**, we are playing against **{dictionary[first[0][2]].strip()}** wearing **{first[1]}** on **{first[0][1]}**. "

    else:
        message = f"{today_date}: our first game we are practicing at **{first[0][1]}**."

    # Second game
    if second:
        if second[0][1] != "Practice Area":

            if second[1] == 'Dark':
                message += f"In our second game at **{time_dictionary[today_date][time_index[1]]}**, we are playing against **{dictionary[second[0][5]].strip()}** wearing **{second[1]}** on **{second[0][1]}**. "
            elif second[1] == 'White':
                message += f"In our second game at **{time_dictionary[today_date][time_index[1]]}**, we are playing against **{dictionary[second[0][4]].strip()}** wearing **{second[1]}** on **{second[0][1]}**. "
                
        else:
            message += f"In our second game, we are practicing at **{second[0][1]}**."
    else:
        message += "There is no second game"

    return message
