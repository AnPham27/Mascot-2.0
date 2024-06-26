import settings
import discord 
from discord.ext import commands
from schedule import get_upcoming_schedule
from standings import standings
from field_status import status
from schedule_scraper import play

logger = settings.logging.getLogger("bot")

def run():
    # Running the bot
    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        print(f"{bot.user} is Ready")
        logger.info(f"User: {bot.user} (ID: {bot.user.id})")
        
    @bot.command(
            help="I am still under development!",
            description="Posting the schedule based on the league division, date, and team number",
            brief="Posts the schedule",
            hidden=True
    )
    async def game(ctx, division, day, month, date):
        """ 
        Upcoming schedule to same channel: 
        FORMAT: !game c2 Thu, May 09
        """
        
        message = play(division, day, month, date)
        
        await ctx.send(message)
    
    @bot.command(
            help="I am still under development!",
            description="Posting the schedule based on the league division, date, and team number",
            brief="Posts the schedule",
            hidden=True
    )
    async def everyone(ctx, division, day, month, date):
        """ 
        Upcoming schedule to same channel: 
        FORMAT: !everyone c2 Thu, May 09
        """
        
        message = play(division, day, month, date)
        
        await ctx.send("@everyone " + message)


    #!st division - (no @everyone) responds to same text channel with current standings     
    @bot.command(
            help="I am still under development!",
            description="Posting the standings for the league division",
            brief="Posts the standings",
            hidden=True
    )
    async def st(ctx, division):
        """
        Current standing to the same channel: 
        FORMAT: !st c2
        """
        table, message = standings(division.lower().replace(' ', ''))
        
        await ctx.send(table)
        await ctx.send(message)

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

  
    bot.run(settings.DISCORD_API_SECRET)
    #bot.run("") #for quick testing

if __name__ == '__main__':
    run()