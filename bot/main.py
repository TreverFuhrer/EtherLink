import asyncio
from discord_bot import bot, DISCORD_TOKEN, load_cogs
from websocket_client import start_websocket_client

# Start bot and WebSocket together
async def main():
    await start_websocket_client()
    await load_cogs()
    await bot.start(DISCORD_TOKEN)

# Main Function
if __name__ == "__main__":
    asyncio.run(main())

