import settings
import discord 
import asyncio
from discord.ext import commands
from services.standings import standings
from services.field_status import status
from services.schedule_scraper import play_short
from services.attendance import attendance
from services.commands import list_commands



def run():

    #!field division - (no @everyone) responds to same text channel with current standings     
    @bot.command(
            help="I am still under development!",
            description="Posting the field status from City of Guelph site",
            brief="Posts field status",
            hidden=True
    )
    async def field(ctx):
        """
        Current field status to same channel: 
        FORMAT: !field
        """
        message = status()
        await ctx.send(message)

  
    @bot.command(
        help="I am still under development",
        description="Taking attendance for this week's games",
        brief="Attendance check",
        hidden=True
    )
    async def at(ctx):
        """
        Attendance check with emoji selection
        👍 or 👎
        Format: !at
        """
        message = attendance()
        new_msg = await ctx.send(message)
        await new_msg.add_reaction("👍")
        await new_msg.add_reaction("👎")

    @bot.command(
        help="I am still under development",
        description="lists all the current commands of this bot",
        brief="Command list",
        hidden=True
    )
    async def command(ctx):
        """
        List all the commands
        """
        message = list_commands()
        await ctx.send(message)
