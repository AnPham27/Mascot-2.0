from services.field_status import status
from discord.ext import commands

class Field(commands.Cog):
    """Cog for fetching and posting the field status from City of Guelph"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="field",
        help="Posts field status based on City of Guelph field status site",
        description="Example: !field",
    )
    async def field(self, ctx):
        """Posts the field status in the same channel"""
        try:
            message = status()
            await ctx.send(message)
        
        except Exception as e:
            print(f"Error in !field: {e}")


async def setup(bot):
    await bot.add_cog(Field(bot))