import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
from events.whitelist_command import get_whitelist_delim
#from events.lore_book import daily_lore_update

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Initialize Discord Bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

""" On Bot Startup Event """
@bot.event
async def on_ready():
    activity = discord.Activity(type=discord.ActivityType.playing, name="Minecraft")
    await bot.change_presence(status=discord.Status.dnd, activity=activity)
    print("------")
    print(f"NeoSMP is online!!")
    print("------")
    try:
        # Sync commands with Discord
        GUILD_ID = 1298047553530626058
        guild = discord.Object(id=GUILD_ID)
        await bot.tree.sync(guild=guild)
        await bot.tree.sync()
        print("Slash commands synchronized.")
    except Exception as e:
        print(f"Error synchronizing commands: {e}")


""" Load all discord commands """
async def load_cogs():
    """Dynamically load all cogs from the commands folder."""
    # Get the absolute path to the current file (discord_bot.py)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    commands_dir = os.path.join(base_dir, "commands")  # Navigate to the commands directory

    if not os.path.exists(commands_dir):
        raise FileNotFoundError(f"Commands directory not found: {commands_dir}")

    for filename in os.listdir(commands_dir):
        if filename.endswith(".py") and filename != "__init__.py":
            try:
                # Load cogs using the path relative to the bot package
                await bot.load_extension(f"commands.{filename[:-3]}")
                print(f"Loaded cog: {filename}")
            except Exception as e:
                print(f"Failed to load cog {filename}: {e}")










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