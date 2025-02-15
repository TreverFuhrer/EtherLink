from database import get_channels, remove_channel
from discord_bot import bot

async def update_player_count_channel(data, discord_id):
    print("Updating player count!")
    channels = get_channels(discord_id)
    channel_id = channels.get("player_count")

    if channel_id == None:
        print("channel_id not found")
        return
    
    channel = bot.get_channel(channel_id)

    # If channel doesn't exist, but is in database then remove
    if channel == None:
        print("Channel doesnt exist")
        remove_channel(discord_id, "player_count")
        return

    # Rename channel to new player count
    new_name = f"Online: {data.get("player_count", -2)}"
    await channel.edit(name=new_name)