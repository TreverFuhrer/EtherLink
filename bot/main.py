import asyncio
import discord
from discord.ext import commands
from websocket_server import start_websocket_server  # Import the WebSocket server
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Initialize the Discord bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Define any bot commands here (optional)
@bot.command(name='hello')
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.name}!")

# Start both the bot and WebSocket server concurrently
async def main():
    # Run both bot and WebSocket server at the same time
    await asyncio.gather(
        bot.start(DISCORD_TOKEN),
        start_websocket_server()
    )

# Run the main function to launch everything
if __name__ == "__main__":
    asyncio.run(main())
