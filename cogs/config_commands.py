from discord.ext import commands
from utils.config_manager import load_config, save_config


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
        config = load_config()
        config["divisions"][division] = team_id
        save_config(config)

        await ctx.send(f"✅ Division `{division}` set to team ID `{team_id}`")

    @commands.command(name="list_div")
    async def list_div(self, ctx):
        config = load_config()
        divisions = config.get("divisions", {})
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
        config = load_config()
        config["standings"][div] = standings_id
        save_config(config)

        await ctx.send(f"✅ Standings ID for division {div} is set to {standings_id}")

    
    @commands.command(name="list_st")
    async def list_st(self, ctx):
        """Lists standings ID per division"""
        config = load_config()
        divisions = config.get("standings", {})
        if not divisions:
            await ctx.send("No standings divisions configured yet.")
            return
        formatted = "\n".join([f"**{k}** → `{v}`" for k, v in divisions.items()])
        await ctx.send(f"**Current standings:**\n{formatted}")

    #playoff dates
    @commands.command(name="add_playoff")
    @commands.has_permissions(administrator=True)
    async def add_playoff(self, ctx, *, date: str):
        """Add a playoff date (e.g. Sun, Jan 11)"""
        config = load_config()

        if date not in config["playoff_dates"]:
            config["playoff_dates"].append(date)
            save_config(config)
            await ctx.send(f"✅ Added playoff date: {date}")
        
        else:
            await ctx.send("That playoff date already exists")

    
    @commands.command(name="list_playoffs")
    async def list_playoffs(self, ctx):
        """Lists all playoff dates"""
        config = load_config()
        playoffs = config.get("playoff_dates", [])

        if not playoffs:
            await ctx.send("No playoff dates set")
        
        await ctx.send("**Playoff Dates:**\n" + "n".join(playoffs))
    

    @commands.command(name="add_holiday")
    @commands.has_permissions(administrator=True)
    async def add_holiday(self, ctx, *, date: str):
        """Add a holiday date (e.g., Sun, Dec 28)"""
        config = load_config()

        if date not in config["holidays"]:
            config["holidays"].append(date)
            save_config(config)
            await ctx.send(f"✅ Added holiday: {date}")
        else:
            await ctx.send("That holiday already exists")
        
    
    @commands.command(name="list_holidays")
    async def list_holidays(self, ctx):
        """Lists holidays"""
        config = load_config()
        holidays = config.get("holidays", [])
        if not holidays:
            await ctx.send("No holidays set.")
            return
        await ctx.send("**Holidays:**\n"+ "\n".join(holidays))

async def setup(bot):
    await bot.add_cog(ConfigCommands(bot))