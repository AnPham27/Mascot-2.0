def list_commands():
    msg = "```List of Commands:\n\n"

    msg += "!game MMDD- messages the upcoming game information to the same channel.  Example: !game c2 Thu, Aug 29\n\n"
    msg += "!everyone MMDD - messages the upcoming game information to the same channel with attendance but @everyone. Example: !everyone c2 Thu, Aug 29\n\n"
    msg += "!st division - current standings of the division. Example: !st c2\n\n"
    msg += "!field - current field status via City of Guelph site. Example: !field\n\n"
    msg += "!at - attendance check with 👍 and 👎 reaction. Example: !at\n\n"

    #manual changes 

    msg += "!set_playoffs - set division playoffs date. Example: !set_playoffs Sun, Jan 11-Mon, Jan 12\n\n"
    msg += "!set_holidays - set holidays. Example: !set_holidays Sun, Dec 23-Sun, Dec 30\n\n"
    msg += "!set_team - set team ID for schedule and standings Example !set_team - b2,16259,2394-ct,16039,2377\n\n"


    msg += "!get_playoffs - reads playoffs file\n\n"
    msg += "!get_holidays - reads holidays file\n\n"
    msg += "!get_team division - reads team file\n\n"


    msg += "```"

    return msg