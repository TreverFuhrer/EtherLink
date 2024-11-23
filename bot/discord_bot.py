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
        #await bot.tree.sync()
        print("Slash commands synchronized.")
    except Exception as e:
        print(f"Error synchronizing commands: {e}")


""" Server Chat Command"""
@bot.tree.command(name="server_chat", description="Send a message to the Minecraft server")
async def server_chat(interaction: discord.Interaction, message: str):
    if not any(role.name == "Admin" for role in interaction.user.roles):
        await interaction.response.send_message("You don't have the required role to use this command.", ephemeral=True)
    else:
        from websocket_client import send_signal
        await interaction.response.send_message(f"Message to server: {message}", ephemeral=True)
        await send_signal("SERVER_CHAT", {"message": message})


""" White List Command """
@bot.tree.command(name="whitelist", description="Whitelist a Java or Bedrock player by replying to their message!")
async def whitelist(interaction: discord.Interaction, username: str):
    if not any(role.name in ["Admin", "SMP Mod"] for role in interaction.user.roles):
        # Check if user has appropriate role
        await interaction.response.send_message("You don't have the required role to use this command.", ephemeral=True)
        return

    found_message = None
    async for message in interaction.channel.history(limit=30):
        # Find the message with the username
        if username in message.content:
            found_message = message
            break

    if found_message:
        # React to users username message
        try:
            await found_message.add_reaction("✅")
        except discord.Forbidden:
            await interaction.response.send_message(
                "I lack permission to add reactions to messages.", ephemeral=True
            )
    else:
        # No message found containing the username
        await interaction.response.send_message(
            f"Did not react to message with ✅.\n Reaction will be given if command used in channel with users username message.",
            ephemeral=True
        )
    
    # Send the signal to the plugin
    from websocket_client import send_signal
    await interaction.response.send_message(f"Whitelisting {username}!", ephemeral=True)
    await send_signal("WHITELIST", {"message": f"{interaction.user.name}|{get_whitelist_delim(username)}"}, interaction)






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