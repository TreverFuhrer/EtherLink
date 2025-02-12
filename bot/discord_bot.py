import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Initialize Discord Bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

""" On Bot Startup Event """
@bot.event
async def on_ready():
    activity = discord.Activity(type=discord.ActivityType.playing, name="Minecraft")
    await bot.change_presence(status=discord.Status.dnd, activity=activity)
    print("------")
    print(f"NeoSMP is online!!")
    print("------")


""" Load all discord commands """
async def load_cogs():
    """Dynamically load all cogs from the commands folder."""
    
    # Get the absolute path to the current file (discord_bot.py)
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Navigate to the commands directory
    commands_dir = os.path.join(base_dir, "commands")

    if not os.path.exists(commands_dir):
        raise FileNotFoundError(f"Commands directory not found: {commands_dir}")

    for filename in os.listdir(commands_dir):
        if filename.endswith(".py") and filename != "__init__.py":
            try:
                # Load cogs using the path relative to the bot package
                await bot.load_extension(f"commands.{filename[:-3]}")
                print(f"Loaded cog: {filename}")
            except Exception as e:
                print(f"Failed to load cog {filename}: {e}")

