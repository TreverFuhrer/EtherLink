import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
#from events.lore_book import daily_lore_update

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Initialize Discord Bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    activity = discord.Activity(type=discord.ActivityType.playing, name="Minecraft")
    await bot.change_presence(status=discord.Status.dnd, activity=activity)
    print("------")
    print(f"{bot.user} is online!!")
    print("------")
    try:
        await bot.tree.sync()  # Sync commands with Discord
        print("Slash commands synchronized.")
    except Exception as e:
        print(f"Error synchronizing commands: {e}")


@bot.tree.command(name="server_chat", description="Send a message to the Minecraft server")
async def server_chat(interaction: discord.Interaction, message: str):
    if not any(role.name == "Admin" for role in interaction.user.roles):
        await interaction.response.send_message("You don't have the required role to use this command.", ephemeral=True)
    else:
        from websocket_client import send_signal
        await interaction.response.send_message(f"Message to server: {message}", ephemeral=True)
        await send_signal("SERVER_CHAT", {"message": message})


'''@bot.tree.command(name="lore_update", description="Trev's test command for something secret")
async def server_chat(interaction: discord.Interaction):
    # Check if user has "Admin" role
    if not any(role.name == "Admin" for role in interaction.user.roles):
        await interaction.response.send_message("You don't have the required role to use this command.", ephemeral=True)
    else:
        # Send immediate response to avoid delay
        await interaction.response.send_message("Making a lore update...", ephemeral=True)
        
        # Run the blocking daily_lore_update function in a separate thread
        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, daily_lore_update)
        
        # Optionally, send a follow-up message once the task is complete (if necessary)
        await interaction.followup.send("Lore update complete.", ephemeral=True)'''