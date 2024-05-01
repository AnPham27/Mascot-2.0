import settings
import discord 
from discord.ext import commands
from schedule import get_upcoming_schedule
from standings import standings

logger = settings.logging.getLogger("bot")

def run():
    # Running the bot
    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        print(f"{bot.user} is Ready")
        logger.info(f"User: {bot.user} (ID: {bot.user.id})")

    #!upc day month date team num - (no @everyone) responds to same text channel with respective date and team number
    @bot.command(
            help="I am still under development!",
            description="Posting the schedule based on the league division, date, and team number",
            brief="Posts the schedule",
            hidden=True
    )
    async def upc(ctx, division, day, month, date, team_num):
        """ 
        Upcoming schedule to same channel: 
        FORMAT: !upc c2 Thursday, July 5 4
        """
        
        message = get_upcoming_schedule(division, day, month, date, team_num)

        await ctx.send(message)
        

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

  
    bot.run(settings.DISCORD_API_SECRET)
    #bot.run("") #for quick testing

if __name__ == '__main__':
    run()