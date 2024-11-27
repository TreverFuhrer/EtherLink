import discord
from discord.ext import commands
from events.whitelist_command import get_whitelist_delim
from websocket_client import send_signal


class Whitelist(commands.Cog):
    """ Commands related to whitelisting players """

    # Allows changes to the bot
    def __init__(self, bot):
        self.bot = bot

    """ Whitelist Command """
    @commands.hybrid_command(name="whitelist", description="Whitelist a Java or Bedrock player")
    async def whitelist(self, ctx: commands.Context, username: str):

        # Check if user has permissions
        if not any(role.name in ["Admin", "SMP Mod"] for role in ctx.author.roles):
            await ctx.reply("You don't have the required role to use this command.", ephemeral=True)
            return
        
        # Check if message with username exists in channel
        found_message = None
        async for message in ctx.channel.history(limit=30):
            # Find the message with the username
            if username in message.content:
                found_message = message
                break

        if found_message:
            try:
                # React to users username message
                await found_message.add_reaction("✅")
            except discord.Forbidden:
                await ctx.reply("I lack permission to add reactions to messages.", ephemeral=True)

        await ctx.reply(f"Whitelisting {username}!", ephemeral=True)
        await send_signal("WHITELIST", {"message": f"{ctx.author.name}|{get_whitelist_delim(username)}"}, ctx)



# Setup Cog
async def setup(bot):
    await bot.add_cog(Whitelist(bot))