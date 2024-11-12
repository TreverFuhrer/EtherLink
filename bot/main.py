import asyncio
from discord_bot import discord, bot, DISCORD_TOKEN
from websocket_client import start_websocket_client, send_signal

# Start bot and WebSocket together
async def main():
    start_websocket_client()
    await bot.start(DISCORD_TOKEN)

# Main Function
if __name__ == "__main__":
    asyncio.run(main())

