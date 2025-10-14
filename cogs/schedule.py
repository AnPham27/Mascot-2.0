from discord.ext import commands
from services.standings import standings
from services.schedule_scraper import play_short
from services.attendance import attendance
from services.schedule_scraper import play_short_embed
from services.schedule_scraper import play_embed

class Schedule(commands.Cog):
    """Cog for fetching and posting game schedule and standings."""

    def __init__(self, bot):
        self.bot = bot


    @commands.command(
            name="game_embed",
            help="Posts the schedule as an embed for the given division and date",
            description="Exmaple: !game_embed b2 1026"
    )
    async def game_embed(self, ctx, division: str, mmdd: str):
        """ Sends a game schedule as an embed for the given division and date"""
    
        embed = play_short_embed(division, mmdd) 

        if not embed:
            await ctx.send("No matches found for that date/team.")
            return

        await ctx.send(embed=embed)


    @commands.command(
        name="game",
        help="Posts the schedule for a given team and date.",
        description="Example: !game c2 0508 (for May 8th, team in C2 league)",
    )
    async def game(self, ctx, division: str, mmdd:str ):
        """Posts the schedule to the same channel"""
        try:
            message = play_short(division, mmdd)
            await ctx.send(message)
        except Exception as e:
            print(f"Error in !game: {e}")

    
    @commands.command(
        name="e",
        help="Posts the schedule, standings, and attendance check with @everyone mention.",
        description="Example !e c2 0508",
    )
    async def e(self, ctx, division:str, mmdd:str):
        """
        Posts schedule, standings, and attendance, pinging everyone
        FORMAT: !e division mmdd
        """
        try:
            #schedule
            message = play_short(division, mmdd)
            await ctx.send("@everyone " + message)

            #standings
            table, message = standings(division.lower().replace(' ', ''))
            await ctx.send(table)
            await ctx.send(message)

            #attendance
            message = attendance()
            new_msg = await ctx.send(message)
            await new_msg.add_reaction("👎")
            await new_msg.add_reaction("👍")

        except Exception as e:
            print(f"Error in !e: {e}")

    @commands.command(
        name="st",
        help="Posts the current standings for division",
        description="Example: !st c2 (standings for C2 division)",
    )
    async def st(self, ctx, division: str):
        """Posts the standing in the same channel"""
        try:
            table, message = standings(division.lower().replace(' ', ''))
            await ctx.send(table)
            await ctx.send(message)

        except Exception as e:
            print(f"Error in !st: {e}")


    @commands.command(
        name="at",
        help="Attendance check using emojis",
        description="Example: !at",
    )
    async def at(self, ctx, division: str, mmdd:str ):
        """Attendance check sent in the same channel"""
        try:
            message = attendance()
            new_msg = await ctx.send(message)
            await new_msg.add_reaction('👍')
            await new_msg.add_reaction('👎')
        
        except Exception as e:
            print(f"Error in !at: {e}")

async def setup(bot):
    await bot.add_cog(Schedule(bot))