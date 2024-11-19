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


@bot.tree.command(name="whitelist", description="Whitelist any java or bedrock player on the NeoSMP server!")
async def whitelist(interaction: discord.Interaction, username: str):
    # Check if user has appropriate role
    if not any(role.name in ["Admin", "SMP Mod"] for role in interaction.user.roles):
        await interaction.response.send_message("You don't have the required role to use this command.", ephemeral=True)
    else:
        from websocket_client import send_signal
        invoker_username = interaction.user.name
        await interaction.response.send_message(f"Whitelisting {username}!", ephemeral=True)
        await send_signal("WHITELIST", {"message": invoker_username+"|"+get_whitelist_delim(username)}, interaction)


@bot.tree.command(name="whitelist", description="Whitelist a Java or Bedrock player by replying to their message!")
async def whitelist(interaction: discord.Interaction):
    # Check if user has appropriate role
    if not any(role.name in ["Admin", "SMP Mod"] for role in interaction.user.roles):
        await interaction.response.send_message("You don't have the required role to use this command.", ephemeral=True)
        return

    # Check if the command is a reply to a message
    if not interaction.message or not interaction.message.reference:
        await interaction.response.send_message(
            "Reply to a message containing the player's username.\nThen type /whitelist", ephemeral=True)
        return

    # Get the referenced message
    referenced_message = interaction.message.reference.resolved
    if not referenced_message or not isinstance(referenced_message, discord.Message):
        await interaction.response.send_message("Could not retrieve the referenced message.", ephemeral=True)
        return
    
    # Extract username from referenced message
    username = referenced_message.content.strip()
    
    # Send the signal to the plugin
    from websocket_client import send_signal
    await interaction.response.send_message(f"Whitelisting {username}!", ephemeral=True)
    await send_signal("WHITELIST", {"message": {interaction.user.name}+"|"+get_whitelist_delim(username)}, interaction)

    # Add the green checkmark reaction
    try:
        await referenced_message.add_reaction("✅")
    except discord.Forbidden:
        await interaction.response.send_message("I lack permission to add reactions to messages.", ephemeral=True)
        return








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