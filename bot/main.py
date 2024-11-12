import asyncio
import discord
from discord.ext import commands
from websocket_server import start_websocket_server  # Import the WebSocket server
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Initialize Discord Bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Bot commands
@bot.command(name='hello')
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.name}!")

# Start bot and WebSocket together
async def main():
    await asyncio.gather(
        bot.start(DISCORD_TOKEN),
        start_websocket_server()
    )

# Main Function
if __name__ == "__main__":
    asyncio.run(main())
