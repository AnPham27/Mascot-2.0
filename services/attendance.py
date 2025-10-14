import discord

def attendance():

    message = "**Attendance Check**\n"
    message += "👍 = attending OR "
    message += "👎 = not attending"

    return message


def attendance_embed():

    embed = discord.Embed(
        title="Attendance Check",
        description="Mark your status",
        color=0x0ad543
    )

    return embed