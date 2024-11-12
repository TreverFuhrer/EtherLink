import discord
from discord.ext import commands
from websocket_client import send_signal
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
    print("------")
    print(f"{bot.user} is online!!")
    print("------")


# Commands

# Define a slash command to send a chat message to the Minecraft server
@bot.tree.command(name="server_chat", description="Send a chat message to the Minecraft server from the bot")
async def server_chat(interaction: discord.Interaction, message: str):
    await interaction.response.send_message(f"Sending message to server: {message}", ephemeral=True)
    await send_signal("SERVER_CHAT", {"message": message})