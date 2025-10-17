def list_commands():
    msg = "```List of Commands:\n\n"

    msg += "!game MMDD- messages the upcoming game information to the same channel.  Example: !game c2 Thu, Aug 29\n\n"
    msg += "!everyone MMDD - messages the upcoming game information to the same channel with attendance but @everyone. Example: !everyone c2 Thu, Aug 29\n\n"
    msg += "!st division - current standings of the division. Example: !st c2\n\n"
    msg += "!field - current field status via City of Guelph site. Example: !field\n\n"
    msg += "!at - attendance check with ✅ and ❌ reaction. Example: !at\n\n"

    
    #playoffs 
    msg += "!add_playoff Day, MM DD - set division playoffs date. Example: !add_playoff Sun, Jan 11\n\n"
    msg += "!list_playoffs - lists added playoff dates\n\n"
    #i should probably add remove features

    #holidays
    msg += "!add_holidays Day, MM DD - set holidays. Example: !set_holidays Sun, Dec 28\n\n"
    msg += "!list_holidays - lists added holidays. Example: !list_holidays\n\n"

    #team 
    msg += "!set_div - set team ID for schedule Example !set_div - b2 16259\n\n"
    msg += "!list_div - lists current divisions with team IDs - !list_div\n\n"

    #standings
    msg += "!set_st - set team ID for standings Example !set_st - b2 2394\n\n"
    msg += "!list_st - lists current standings divisions with team IDs - !list_st\n\n"


    msg += "```"

    return msg