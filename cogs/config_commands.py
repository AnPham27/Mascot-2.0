from discord.ext import commands
from utils.db_config import get_config_value, set_config_value


class ConfigCommands(commands.Cog):
    """Manage team IDs, playoffs, and holidays via Discord commands"""

    def __init__(self, bot):
        self.bot = bot

    #divisions
    @commands.command(name="set_div") 
    @commands.has_permissions(administrator=True)
    async def set_div(self, ctx, division: str, team_id: int):
        """Set or uupdate a division's team ID"""
        #example !set_div b2 16259 OR !set_div ct 16039
        divisions = get_config_value("divisions") or {}
        divisions[division] = team_id
        set_config_value("divisions", divisions)
        await ctx.send(f"✅ Division `{division}` set to team ID `{team_id}`")

    @commands.command(name="list_div")
    async def list_div(self, ctx):
        divisions = get_config_value("divisions") or {}
        if not divisions:
            await ctx.send("No divisions configured yet.")
            return
        formatted = "\n".join([f"**{k}** → `{v}`" for k, v in divisions.items()])
        await ctx.send(f"**Current divisions:**\n{formatted}")


    #standings
    @commands.command(name="set_st")
    @commands.has_permissions(administrator=True)
    async def set_st(self, ctx, div: str, standings_id: int):
        """Set standings ID for division"""
        standings = get_config_value("standings") or {}
        standings[div] = standings_id
        set_config_value("standings", standings)
        await ctx.send(f"✅ Standings ID for division {div} is set to {standings_id}")

    
    @commands.command(name="list_st")
    async def list_st(self, ctx):
        """Lists standings ID per division"""
        standings = get_config_value("standings") or {}
        if not standings:
            await ctx.send("No standings divisions configured yet.")
            return
        formatted = "\n".join([f"**{k}** → `{v}`" for k, v in standings.items()])
        await ctx.send(f"**Current standings:**\n{formatted}")

    #playoff dates
    @commands.command(name="add_playoff")
    @commands.has_permissions(administrator=True)
    async def add_playoff(self, ctx, *, date: str):
        """Add a playoff date (e.g. Sun, Jan 11)"""
        playoffs = get_config_value("playoff_dates") or []
        if date not in playoffs:
            playoffs.append(date)
            set_config_value("playoff_dates", playoffs)
            await ctx.send(f"✅ Added playoff date: {date}")
        else:
            await ctx.send("That playoff date already exists")


    
    @commands.command(name="list_playoffs")
    async def list_playoffs(self, ctx):
        """Lists all playoff dates"""
        playoffs = get_config_value("playoff_dates") or []
        if not playoffs:
            await ctx.send("No playoff dates set.")
            return
        await ctx.send("**Playoff Dates:**\n" + "\n".join(playoffs))
    

    @commands.command(name="add_holiday")
    @commands.has_permissions(administrator=True)
    async def add_holiday(self, ctx, *, date: str):
        """Add a holiday date (e.g., Sun, Dec 28)"""
        holidays = get_config_value("holidays") or []
        if date not in holidays:
            holidays.append(date)
            set_config_value("holidays", holidays)
            await ctx.send(f"✅ Added holiday: {date}")
        else:
            await ctx.send("That holiday already exists")
        
    
    @commands.command(name="list_holidays")
    async def list_holidays(self, ctx):
        """Lists holidays"""
        holidays = get_config_value("holidays") or []
        if not holidays:
            await ctx.send("No holidays set.")
            return
        await ctx.send("**Holidays:**\n" + "\n".join(holidays))


    @commands.command(name="clear")
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx, category: str = None):
        """Clears all or specific configuration data.
            !clear                → clears everything
            !clear divisions      → clears only divisions
            !clear playoffs       → clears only playoff_dates
            !clear holidays       → clears only holidays
            !clear standings      → clears only standings
            """

        default_config = {
            "divisions": {},
            "playoff_dates": [],
            "holidays": [],
            "standings": {}
        }

        if category is None:
            #clear all
            for key, value in default_config.items():
                set_config_value(key, value)
            await ctx.send("🧹 All configuration data has been cleared!")
            return

        #normalize user input
        category = category.lower().strip()

        #map possible shorthand names
        aliases = {
            "divs": "divisions",
            "playoffs": "playoff_dates",
            "holiday": "holidays",
            "stand": "standings"
        }

        category = aliases.get(category, category)

        if category not in default_config:
            await ctx.send("⚠️ Invalid category. Please choose from: divisions, playoff_dates, holidays, standings.")
            return

        # Clear just the chosen category
        set_config_value(category, default_config[category])
        await ctx.send(f"✅ Cleared `{category}` configuration.")
    
    
async def setup(bot):
    await bot.add_cog(ConfigCommands(bot))