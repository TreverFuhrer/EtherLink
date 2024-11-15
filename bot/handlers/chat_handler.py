import discord
from discord_bot import bot
import hashlib
import aiohttp
#from events.lore_book import store_chat_log

DISCORD_CHANNEL_ID = 1306010586143916086
player_head_cache = {}

# Example chat_handler.py
async def process_chat_message(data):
    username = data["username"]
    message = data["message"]
    clean_message = message.strip('"')

    #store_chat_log(username, clean_message)

    # Get player skin head if not in cache
    if not username in player_head_cache:
        if username.startswith("."):
            username = username[1:]
            head_image_url = get_head_image_bedrock(username)
            player_head_cache['.'+username] = head_image_url
        else:
            head_image_url = get_head_image_java(username)
            player_head_cache[username] = head_image_url
    else:
        head_image_url = player_head_cache[username]
    
    # Create embed message
    embed = discord.Embed(
            title = clean_message,
            color = name_to_color(username)
    )
    if username.startswith("."): username = username[1:]
    embed.set_author(name=username, icon_url=head_image_url)

    # Send embed in discord
    channel = bot.get_channel(DISCORD_CHANNEL_ID)
    await channel.send(embed=embed)


# Get player head image URL
def get_head_image_java(username):
    return f"https://minotar.net/avatar/{username}/100.png"

# Get player head image URL
def get_head_image_bedrock(username):
    return f"https://api.mcheads.org/head/*{username}.png"


# Get player color
def name_to_color(username):
    # Hash the username to get a consistent integer
    hash_int = int(hashlib.md5(username.encode()).hexdigest(), 16)
    
    # Extract RGB values by shifting bits
    red = (hash_int >> 16) & 0xFF
    green = (hash_int >> 8) & 0xFF
    blue = hash_int & 0xFF
    
    return discord.Color.from_rgb(red, green, blue)