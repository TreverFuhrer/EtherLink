import asyncio
from discord_bot import bot, DISCORD_TOKEN
from websocket_server import start_websocket_server

# Bot commands
@bot.command(name='hello')
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.name}!")

# Start bot and WebSocket together
async def main():
    await asyncio.gather(
        bot.start(DISCORD_TOKEN),
        start_websocket_server()
    )

# Main Function
if __name__ == "__main__":
    asyncio.run(main())
