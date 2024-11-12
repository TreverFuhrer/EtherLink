from discord_bot import bot

# Example chat_handler.py
async def process_chat_message(data):
    username = data["username"]
    message = data["message"]
    clean_message = message.strip('"')

    # Send message to designated Discord channel
    DISCORD_CHANNEL_ID = 1306010586143916086
    channel = bot.get_channel(DISCORD_CHANNEL_ID)
    await channel.send(f"{username}: {clean_message}")