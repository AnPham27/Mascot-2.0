import discord
from discord.ext import commands

class CommandList(commands.Cog):
    """Displays a list of all available bot commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="commands", aliases=["help"])
    async def commands_list(self, ctx):
        """Shows the list of available commands"""

        embed = discord.Embed(
            title="Bot Commands!",
            description="Here’s everything you can do with me:",
            color=discord.Color.blue()
        )

        # Game & Attendance
        embed.add_field(
            name="🏟️ Game & Attendance",
            value=(
                "`!game <division> <date>` — Upcoming game info - Example: !game b2 1026\n"
                "`!st <division>` — Show current standings\n"
                "`!field` — Check field status\n"
                "`!at` — Attendance check with ✅/❌"
            ),
            inline=False
        )

        # Config
        embed.add_field(
            name="⚙️ Config & Admin",
            value=(

                "`!set_div <division> <id>` — Set team ID\n"
                "`!list_div` — List all divisions\n\n"

                "`!set_st <division> <id>` — Set standings ID \n"
                "`!list_st` — List standings divisions\n\n"

                "`!add_playoff <Day, Mon DD>` — Add playoff date \n"
                "`!list_playoffs` — List playoff dates\n\n"

                "`!add_holiday <Day, Mon DD>` — Add holiday\n"
                "`!list_holidays` — List holidays \n\n"

                "`!clear` — Clear all or specific section"
            ),
            inline=False
        )
        await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(CommandList(bot))