import settings
import discord
from discord.ext import commands
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()
logger = settings.logging.getLogger("bot")

# Running the bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)
# remove the default help command to use my own
bot.remove_command("help")

@bot.event
async def on_ready():
    print(f"{bot.user} is Ready!")
    logger.info(f"User: {bot.user} (ID: {bot.user.id})")

    #restore attendance data after reboot
    schedule_cog = bot.get_cog("Schedule")
    if schedule_cog:
        await schedule_cog.restore_embeds()
        print("🧩 Attendance embeds restored from database.")

async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py") and filename != "__init__.py":
            extension = f"cogs.{filename[:-3]}"
            try:
                await bot.load_extension(extension)
                print(f"✅ Loaded cog: {extension}")
            except Exception as e:
                print(f"❌ Failed to load cog {extension}: {e}")

async def main():
    
    #main asynchronous entry point
    await load_cogs()
    await bot.start(settings.DISCORD_API_SECRET)
    #await bot.start("")


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot shut down manually.")