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

@bot.event
async def on_ready():
    print(f"{bot.user} is now online and connected to Discord!")
    print(f"Logged in as: {bot.user.name}#{bot.user.discriminator}")
    print(f"Bot ID: {bot.user.id}")
    print("------")