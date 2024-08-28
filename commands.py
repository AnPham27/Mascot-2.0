def list_commands():
    msg = "```List of Commands:\n\n"

    msg += "!game division DoW, Month Day - messages the upcoming game information to the same channel.  Example: !game c2 Thu, Aug 29\n\n"
    msg += "!everyone division DoW, Month Day - messages the upcoming game information to the same channel with attendance but @everyone. Example: !everyone c2 Thu, Aug 29\n\n"
    msg += "!st division - current standings of the division. Example: !st c2\n\n"
    msg += "!field - current field status via City of Guelph site. Example: !field\n\n"
    msg += "!at - attendance check with 👍 and 👎 reaction. Example: !at\n\n"
    
    msg += "```"

    return msg