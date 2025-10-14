import discord

def schedule_embed(title: str, matches: list):
    """
    Returns a discord.Embed object for schedule in this format: 
    Sun, Oct 26
    GAME 1
    8:30 PM @ Guelph Lake #2 wearing Dark
    Against Hammer Heads (6-0-0) (4.92)
    GAME 2
    9:15 PM @ Guelph Lake # 2 wearing Dark
    Against Game of Throws (1-3-2) (4.92)

    matches: list of dicts like:
    [{"time": 8:30 PM", "location": "Guelph Lake # 2", "colour": "Dark", "opponent": "Hammer Heads"}] 
    """

    embed = discord.Embed(title=title, color=0xBC9FFF)

    for match in matches:
        name = f"{match['time']} @ {match['location']} wearing {match['colour']}"
        value = f"Against {match['opponent']}"
        embed.add_field(name=name, value=value, inline=False)

    return embed 


def sch_embed(title: str, matches: list):
    """
    Returns discord.Embed object for schedule in this format:
    Sun, Oct 26
    GAME 1
    TIME 8:30 PM
    LOCATION: Guelph Lake #2
    COLOUR: Dark
    OPPONENT: Hammer Heads (6-0-0) (4.92)

    GAME 2
    TIME 9:15 PM
    LOCATION:  Guelph Lake #2 
    COLOUR: Dark
    OPPONENT: Game of Throws (1-3-2) (4.92)
    """
    embed = discord.Embed(title=title, color=0xBC9FFF)

    des_lines = []
    for idx, match in enumerate(matches, start=1):
        des_lines.append(f"**Game {idx}**")
        des_lines.append(f"**Time:** {match['time']}")
        des_lines.append(f"**Location:** {match['location']}")
        des_lines.append(f"**Colour:** {match['colour']}")
        des_lines.append(f"**Opponent:** {match['opponent']}")
        des_lines.append("")  # blank line between games

    embed.description = "\n".join(des_lines)
    
    return embed