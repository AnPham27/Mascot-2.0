from discord.ext import commands
from services.standings import standings
from services.schedule_scraper import play_short
from services.attendance import attendance
from services.schedule_scraper import play_short_embed
from services.schedule_scraper import play_embed
import discord

class Schedule(commands.Cog):
    """Cog for fetching and posting game schedule and standings."""

    def __init__(self, bot):
        self.bot = bot
        self.attendance_data = {}


    @commands.command(
        name="game",
        help="Posts the schedule for a given team and date.",
        description="Example: !game c2 0508 (for May 8th, team in C2 league)",
    )
    async def game(self, ctx, division: str, mmdd: str):
        """Posts the schedule as an embed with live attendance reactions."""
        try:
            embed = play_short_embed(division, mmdd)

            #check for special cases (holiday/playoffs)
            if embed.description and any(
                phrase in embed.description.lower()
                for phrase in ["no games", "playoffs", "double check the date"]
            ):
                await ctx.send(embed=embed)
                return

            #Add attendance fields
            embed.add_field(name="✅ Attending", value="(none)", inline=False)
            embed.add_field(name="❌ Not Attending", value="(none)", inline=False)
            
            #send embed and add reactions
            message = await ctx.send(embed=embed)
            await message.add_reaction("✅")
            await message.add_reaction("❌")

            #initialize attendance tracking
            self.attendance_data[message.id] = {
                "attending": set(),
                "not_attending": set(),
                "user_emojis": {} 
            }

        except Exception as e:
            print(f"Error in !game: {e}")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        if user.bot:
            return
        if reaction.message.id not in self.attendance_data:
            return
        await self.update_user_attendance(reaction.message, user, str(reaction.emoji), added=True)

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction, user):
        if user.bot:
            return
        if reaction.message.id not in self.attendance_data:
            return
        await self.update_user_attendance(reaction.message, user, str(reaction.emoji), added=False)

    async def update_user_attendance(self, message, user, emoji, added: bool):
        """Update a single user's emoji reaction and update embed instantly."""
        data = self.attendance_data[message.id]
        name = getattr(user, "display_name", None) or user.name

        # Initialize this user's emoji set if missing
        if name not in data["user_emojis"]:
            data["user_emojis"][name] = set()

        # Update user's emoji set
        if added:
            data["user_emojis"][name].add(emoji)
        else:
            data["user_emojis"][name].discard(emoji)

        # Rebuild attending / not_attending lists
        attending = {user_name for user_name, emojis in data["user_emojis"].items() if "✅" in emojis}
        not_attending = {user_name for user_name, emojis in data["user_emojis"].items() if "❌" in emojis}

        data["attending"] = attending
        data["not_attending"] = not_attending

        await self.update_embed(message, data)

    async def update_embed(self, message, data):
        """Edit the embed with updated attendance lists."""
        embed = message.embeds[0]

        attending_list = "\n".join(sorted(data["attending"])) or "(none)"
        not_attending_list = "\n".join(sorted(data["not_attending"])) or "(none)"

        # Update the correct fields
        for i, field in enumerate(embed.fields):
            if field.name == "✅ Attending":
                embed.set_field_at(i, name="✅ Attending", value=attending_list, inline=False)
            elif field.name == "❌ Not Attending":
                embed.set_field_at(i, name="❌ Not Attending", value=not_attending_list, inline=False)

        await message.edit(embed=embed)

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

    @commands.command(name="at", help="Attendance check", description="Example: !at")
    async def at(self, ctx):
        """Attendance check"""
        try:
            
            embed = discord.Embed(
                title="Attendance check",
                color=0x93e9be
            )
            
            #Add attendance fields
            embed.add_field(name="✅ Attending", value="(none)", inline=False)
            embed.add_field(name="❌ Not Attending", value="(none)", inline=False)
            
            #send embed and add reactions
            message = await ctx.send(embed=embed)
            await message.add_reaction("✅")
            await message.add_reaction("❌")

            #initialize attendance tracking
            self.attendance_data[message.id] = {
                "attending": set(),
                "not_attending": set(),
                "user_emojis": {} 
            }

        except Exception as e:
            print(f"Error in !game: {e}")

async def setup(bot):
    await bot.add_cog(Schedule(bot))