from discord.ext import commands
from services.standings import standings
from services.schedule_scraper import play_short_embed
from utils.db_config import get_config_value, set_config_value
import discord
import json

class Schedule(commands.Cog):
    """Cog for fetching and posting game schedule and tracking attendance."""

    def __init__(self, bot):
        self.bot = bot
        self.attendance_data = get_config_value("attendance_data") or {}


    @commands.command(
        name="game",
        help="Posts the schedule for a given team and date.",
        description="Example: !game c2 0508 (for May 8th, team in C2 league)",
    )
    async def game(self, ctx, division: str, mmdd: str):
        """Posts the schedule as an embed with live attendance reactions."""
        try:
            embed = play_short_embed(division, mmdd)

            # Skip posting if this is a no-game / playoffs message
            if embed.description and any(
                phrase in embed.description.lower()
                for phrase in ["no games", "playoffs", "double check the date"]
            ):
                await ctx.send(embed=embed)
                return

            # add attendance fields
            embed.add_field(name="✅ Attending", value="(none)", inline=False)
            embed.add_field(name="❌ Not Attending", value="(none)", inline=False)

            # send embed and add reactions
            message = await ctx.send(embed=embed)
            await message.add_reaction("✅")
            await message.add_reaction("❌")

            # initialize state in DB and memory
            saved_state = get_config_value("attendance_state") or {}
            saved_state[str(message.id)] = {
                "channel_id": message.channel.id,
                "attending": [],
                "not_attending": [],
                "user_emojis": {}
            }
            set_config_value("attendance_state", saved_state)

            self.attendance_data[message.id] = {
                "attending": set(),
                "not_attending": set(),
                "user_emojis": {}
            }

        except Exception as e:
            print(f"Error in !game: {e}")

    @commands.command(name="at", help="Attendance check", description="Example: !at")
    async def at(self, ctx):
        """Manual attendance check."""
        try:
            embed = discord.Embed(title="Attendance check", color=0x93e9be)
            embed.add_field(name="✅ Attending", value="(none)", inline=False)
            embed.add_field(name="❌ Not Attending", value="(none)", inline=False)

            message = await ctx.send(embed=embed)
            await message.add_reaction("✅")
            await message.add_reaction("❌")

            saved_state = get_config_value("attendance_state") or {}
            saved_state[str(message.id)] = {
                "channel_id": message.channel.id,
                "attending": [],
                "not_attending": [],
                "user_emojis": {}
            }
            set_config_value("attendance_state", saved_state)

            self.attendance_data[message.id] = {
                "attending": set(),
                "not_attending": set(),
                "user_emojis": {}
            }

        except Exception as e:
            print(f"Error in !at: {e}")

    @commands.command(
        name="st",
        help="Posts the current standings for division",
        description="Example: !st c2 (standings for C2 division)",
    )
    async def st(self, ctx, division: str):
        """Posts the standings."""
        try:
            table, message = standings(division.lower().replace(' ', ''))
            await ctx.send(table)
            await ctx.send(message)
        except Exception as e:
            print(f"Error in !st: {e}")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.user_id == self.bot.user.id:
            return

        channel = self.bot.get_channel(payload.channel_id)
        if not channel:
            return

        try:
            message = await channel.fetch_message(payload.message_id)
            user = self.bot.get_user(payload.user_id) or await self.bot.fetch_user(payload.user_id)
        except Exception as e:
            print(f"⚠️ Could not fetch message or user: {e}")
            return

    
        if str(message.id) not in self.attendance_data:
            self.attendance_data[str(message.id)] = {"✅": [], "❌": []}

        await self.update_user_attendance(message)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.user_id == self.bot.user.id:
            return

        channel = self.bot.get_channel(payload.channel_id)
        if not channel:
            return

        try:
            message = await channel.fetch_message(payload.message_id)
            user = self.bot.get_user(payload.user_id) or await self.bot.fetch_user(payload.user_id)
        except Exception as e:
            print(f"⚠️ Could not fetch message or user: {e}")
            return

        # initialize memory if missing
        if str(message.id) not in self.attendance_data:
            self.attendance_data[str(message.id)] = {"✅": [], "❌": []}

        await self.update_user_attendance(message)
        
    async def update_user_attendance(self, message):
        """Update the attendance embed based on current reactions."""
        # initialize memory if missing
        if str(message.id) not in self.attendance_data:
            self.attendance_data[str(message.id)] = {"✅": [], "❌": []}

        attendance_data = {"✅": [], "❌": []}

        # build current lists from live reactions
        for reaction in message.reactions:
            emoji = str(reaction.emoji)
            if emoji not in ["✅", "❌"]:
                continue

            async for user in reaction.users():
                if user.bot:
                    continue
                attendance_data[emoji].append(user.display_name)

        # sort and save
        attendance_data["✅"].sort()
        attendance_data["❌"].sort()
        self.attendance_data[str(message.id)] = attendance_data
        set_config_value("attendance_data", self.attendance_data)

        #update the embed visually
        if not message.embeds:
            return
        embed = message.embeds[0]
        embed.clear_fields()
        embed.add_field(
            name="✅ Attending",
            value="\n".join(attendance_data["✅"]) or "(none)",
            inline=False,
        )
        embed.add_field(
            name="❌ Not Attending",
            value="\n".join(attendance_data["❌"]) or "(none)",
            inline=False,
        )
        await message.edit(embed=embed)

    async def update_embed(self, message, data):
        """Edit the embed with updated attendance lists."""
        
        if "attending" not in data:
            data["attending"] = []
        if "not_attending" not in data:
            data["not_attending"] = []

        embed = message.embeds[0]
        attending_list = "\n".join(sorted(data["attending"])) or "(none)"
        not_attending_list = "\n".join(sorted(data["not_attending"])) or "(none)"

        for i, field in enumerate(embed.fields):
            if field.name == "✅ Attending":
                embed.set_field_at(i, name="✅ Attending", value=attending_list, inline=False)
            elif field.name == "❌ Not Attending":
                embed.set_field_at(i, name="❌ Not Attending", value=not_attending_list, inline=False)
        await message.edit(embed=embed)
    
    async def restore_embeds(self):
        """Restore attendance embeds from DB or scan live channel messages if DB is empty."""
        data = get_config_value("attendance_state")

        if isinstance(data, str):
            try:
                data = json.loads(data)
            except json.JSONDecodeError:
                print("⚠️ Invalid JSON in attendance_state, resetting.")
                data = {}

        restored = 0
        self.bot.attendance_data = {}

        attendance_channel_ids = [
            123456789012345678, 
            1109852414972010586
        ]

        #if DB has attendance messages, use that as primary source
        if data:
            print("🧩 Restoring attendance embeds from database...")
            message_entries = [(int(mid), entry["channel_id"]) for mid, entry in data.items()]
        else:
            print("⚠️ No attendance state found, scanning channels for attendance messages...")
            message_entries = []

            for cid in attendance_channel_ids:
                channel = self.bot.get_channel(cid)
                if not channel:
                    print(f"⚠️ Channel {cid} not found or inaccessible.")
                    continue

                async for msg in channel.history(limit=50):
                    if not msg.embeds:
                        continue
                    embed = msg.embeds[0]
                    if "Attendance" in embed.title or "Attending" in [f.name for f in embed.fields]:
                        message_entries.append((msg.id, channel.id))
                        print(f"🔍 Found possible attendance message: {msg.id} in #{channel.name}")

        #process each message 
        for mid, channel_id in message_entries:
            channel = self.bot.get_channel(channel_id)
            if not channel:
                print(f"⚠️ Channel {channel_id} not found for message {mid}")
                continue

            try:
                msg = await channel.fetch_message(mid)
            except Exception as e:
                print(f"⚠️ Failed to fetch message {mid}: {e}")
                continue

            current_reactions = {}
            for r in msg.reactions:
                users = [u async for u in r.users()]
                current_reactions[str(r.emoji)] = users
            attending_now = {u.display_name for u in current_reactions.get("✅", []) if not u.bot}
            not_attending_now = {u.display_name for u in current_reactions.get("❌", []) if not u.bot}

            attendance_data = {
                "✅": sorted(attending_now),
                "❌": sorted(not_attending_now),
            }

            self.bot.attendance_data[str(mid)] = attendance_data

            # --- Update embed visually ---
            embed = msg.embeds[0]
            embed.clear_fields()
            embed.add_field(name="✅ Attending", value="\n".join(attendance_data["✅"]) or "(none)", inline=False)
            embed.add_field(name="❌ Not Attending", value="\n".join(attendance_data["❌"]) or "(none)", inline=False)
            await msg.edit(embed=embed)

            restored += 1
            print(f"✅ Restored message {mid}: {len(attending_now)} attending, {len(not_attending_now)} not attending.")

        if restored == 0:
            print("⚠️ No attendance messages found.")
        else:
            set_config_value("attendance_data", self.bot.attendance_data)
            print(f"✅ Fully restored {restored} attendance message(s).")

    @commands.command(name="rebuild_attendance", help="Rebuild attendance for a specific message or recent messages")
    async def rebuild_attendance(self, ctx, channel_id: int = None, message_id: int = None):
        """
        Rebuild attendance for a specific message.
        Usage:
        !rebuild_attendance                    -> rebuild latest attendance in current channel
        !rebuild_attendance <message_id>       -> rebuild message in current channel
        !rebuild_attendance <channel_id> <message_id> -> rebuild from another channel
        """
        # Case: channel + message IDs both provided
        if channel_id and message_id:
            channel = self.bot.get_channel(channel_id)
            if not channel:
                await ctx.send("⚠️ Could not find that channel.")
                return
            await self.rebuild_specific_message(ctx, message_id, channel)
            return

        # Case: only message ID
        if channel_id and not message_id:
            await self.rebuild_specific_message(ctx, channel_id, ctx.channel)
            return

        # Default: check latest attendance in this channel
        await self.check_old_attendance(ctx.channel)
        await ctx.send("✅ Checked and rebuilt attendance message(s).")

    async def check_old_attendance(self, channel: discord.TextChannel, limit: int = 10):
        """Check recent attendance messages and rebuild attendance from reactions."""
        print("🧩 Checking for old attendance messages...")

        async for message in channel.history(limit=limit):
            if message.author != self.bot.user or not message.embeds:
                continue

            embed = message.embeds[0]
            # Check if the embed has attendance fields (works for !game or !at)
            field_names = [f.name for f in embed.fields]
            if "✅ Attending" in field_names and "❌ Not Attending" in field_names:
                print(f"🔍 Found attendance message: {message.id}")

                # Initialize memory
                if str(message.id) not in self.attendance_data:
                    self.attendance_data[str(message.id)] = {"✅": [], "❌": []}

                # Rebuild attendance from reactions
                await self.update_user_attendance(message)

                print(f"✅ Rebuilt attendance for {message.id}")
                return  # stop after first attendance message

        print("⚠️ No recent attendance message found.")
        
    async def rebuild_specific_message(self, ctx, message_id: int, channel):
        """Rebuild attendance for a specific message in a given channel."""
        try:
            message = await channel.fetch_message(message_id)
        except Exception as e:
            await ctx.send(f"⚠️ Could not fetch message with ID `{message_id}`: {e}")
            return

        if not message.embeds:
            await ctx.send("⚠️ That message does not have an embed.")
            return

        embed = message.embeds[0]
        field_names = [f.name for f in embed.fields]
        if "✅ Attending" not in field_names or "❌ Not Attending" not in field_names:
            await ctx.send("⚠️ That message does not appear to be an attendance embed.")
            return

        print(f"🔍 Rebuilding attendance for message {message.id} in {channel.name}...")

        # Initialize memory if missing
        if str(message.id) not in self.attendance_data:
            self.attendance_data[str(message.id)] = {"✅": [], "❌": []}

        # Rebuild from reactions
        await self.update_user_attendance(message)

        await ctx.send(f"✅ Rebuilt attendance for message `{message.id}` in `{channel.name}`.")
        print(f"✅ Successfully rebuilt attendance for message {message.id} in {channel.name}.")

async def setup(bot):
    await bot.add_cog(Schedule(bot))
