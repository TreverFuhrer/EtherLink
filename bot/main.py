import asyncio
from discord_bot import bot, DISCORD_TOKEN, load_cogs
from websocket_client import connect_to_websocket

# Start bot and WebSocket together
async def main():
    asyncio.create_task(connect_to_websocket())
    await load_cogs()
    await bot.start(DISCORD_TOKEN)

# Main Function
if __name__ == "__main__":
    asyncio.run(main())

