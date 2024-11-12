from discord_bot import bot

# Example chat_handler.py
async def process_chat_message(data):
    username = data["username"]
    message = data["message"]

    # Send message to designated Discord channel
    DISCORD_CHANNEL_ID = 1303443844138008778
    channel = bot.get_channel(DISCORD_CHANNEL_ID)
    await channel.send(f"{username}: {message}")