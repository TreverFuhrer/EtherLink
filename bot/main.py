import asyncio
from bot import bot
from websocket_server import start_websocket_server  # Import the WebSocket server

# Bot commands
@bot.command(name='hello')
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.name}!")

# Start bot and WebSocket together
async def main():
    await asyncio.gather(
        bot.start(bot.DISCORD_TOKEN),
        start_websocket_server()
    )

# Main Function
if __name__ == "__main__":
    asyncio.run(main())
