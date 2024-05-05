import requests
from bs4 import BeautifulSoup
from datetime import date
import calendar
  
def find_time_slot(todays_games, team_num, division):
    
    if division == "b7":

        time_slot = 1 #first time slot

        for i in range(1):
            if f'{team_num}' in todays_games[i]:
                time_slot = 0
                print("meep")
                return time_slot
    return time_slot

def find_team_dictionary(division, soup):

    if division in ("b7", "b2", "c", "c2"):
        
        numbers = []
        teams = []


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

    number = []
    team = []

    for i in numbers:
        number.append(i.text)

    for i in teams:
        
        team.append(i.text.replace("The ", ''))

    dictionary = dict(zip(number, team))
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
            #if 0 = first time slot, if 1 = second time slots

            if time_slot == 1:
                time_index = []
                time_index.append(2)
                #time_index.append(3)

            
            
    return time_index

def find_field_num(division, soup):
    
    if division in ("b7", "b2", "c", "c2"):
        nums =[]

        field_num = soup.find_all("a", target="_blank")
        for i in field_num:
            nums.append(i.text)
           

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
    opponent = soup.find("tbody").find_all_next("a", class_="team-link")
    opponents = []
    count = 0
    for i in opponent:
        #opponents.append(days[len(opponents)])
        opponents.append(i.text) 
        count+= 1  
    #['Thursday, August 10', 'Margaret # 4', '1', '12', '12', '9'], 'Dark', 'White']
    if division == ("b7"):
 
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
        
    
    return sub_array, split_arrays

def colour(division, team_num, first, second):

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
  
    return first, second
            


    
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
    
    #lists team number and name 
    dictionary = find_team_dictionary(division, soup)

    
    #day = soup.find("table").find_all("th", id="week_header")
    day = soup.find("div", class_="d-flex justify-content-between border-bottom fw-bold pb-1").find_all("div")
    days = []


    for i in day:
        if not (i.text).startswith("Week"):
            days.append(i.text)
        
    
    
    #need to set playoff dates
    playoff = ["Monday, June 24", "Tuesday, June 25", "Wednesday, June 26", "Thursday, June 27"]

    if today_date in playoff:
        return(f"We have playoffs that day, and there is no schedule for that yet.")
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

    for time in times:
        #check if the time starts with '6' (for 6pm)
        if time.startswith('6') or (time.startswith('7') and division=="b7"):
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

    #print(current_games)
    #print(scheduled_time)

    time_dictionary = dict(zip(days, scheduled_time))
    #print(time_dictionary)

    #print(time_dictionary)
    time_index = find_time_index(time_dictionary, today_date, todays_games, team_num, division)
    
    print(time_index)
    first = []
    second = []


    for i in range (len(current_games)):
        for j in range (len(current_games[0])):

            if j < 4 and current_games[i][j] == f'{team_num}':
                first.append(current_games[i])
            
            if j > 3 and current_games[i][j] == f'{team_num}':
                second.append(current_games[i])


    first, second = colour(division, team_num, first, second)


    print(first)
    
    print(second)
    print(times)
    print(time_dictionary)
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
