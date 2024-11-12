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


# Commands

# Define a slash command to send a chat message to the Minecraft server
@bot.tree.command(name="server_chat", description="Send a chat message to the Minecraft server from the bot")
async def server_chat(interaction: discord.Interaction, message: str):
    await interaction.response.send_message(f"Sending message to server: {message}", ephemeral=True)
    await send_signal("SERVER_CHAT", {"message": message})