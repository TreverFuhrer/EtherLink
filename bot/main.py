import os
import discord
from discord.ext import commands
from flask import Flask, request
from dotenv import load_dotenv
import asyncio
import threading

# Load the environment variables from .env
load_dotenv()
token = os.getenv("DISCORD_TOKEN")  # Retrieve the token

# Set up Discord bot with command prefix and intents
intents = discord.Intents.default()
intents.message_content = True  # Required to read messages in newer versions of discord.py
bot = commands.Bot(command_prefix='?', intents=intents)

# Initialize Flask app
app = Flask(__name__)

DISCORD_CHANNEL_ID = 1303443844138008778

# Flask route to handle incoming messages from Minecraft
@app.route('/minecraft_chat', methods=['POST'])
def minecraft_chat():
    data = request.get_json()
    if not data:
        return {"status": "error", "message": "Invalid JSON data"}, 400

    username = data.get('username')
    message = data.get('message')

    if not username or not message:
        return {"status": "error", "message": "Missing 'username' or 'message' fields"}, 400

    print(username + " tryed to say " + message) # Test 1

    asyncio.run_coroutine_threadsafe(send_discord_message(username, message), bot.loop)

    return {"status": "success"}, 200

# Helper method to send messages in Discord channel
async def send_discord_message(username, message):
    channel = bot.get_channel(DISCORD_CHANNEL_ID)
    if channel:
        await channel.send(f"{username}: {message}")


# Event: When the bot is ready and connected to the server
@bot.event
async def on_ready():
    print(f'Bot is ready and logged in as {bot.user}')

# A basic command that the bot will respond to
@bot.command(name='hello')
async def hello(ctx):
    await ctx.send(f'Hello {ctx.author.name}!')

# Event: Respond to messages directly (optional)
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  # Ignore bot's own messages

    if 'hi bot' in message.content.lower():
        await message.channel.send('Hello there!')

    await bot.process_commands(message)  # Ensures other commands still work

# Function to run Flask in a separate thread
def run_flask():
    app.run(host='127.0.0.1', port=5000)

# Start Flask server in a new thread
flask_thread = threading.Thread(target=run_flask)
flask_thread.start()

# Run the Discord bot
bot.run(token)
