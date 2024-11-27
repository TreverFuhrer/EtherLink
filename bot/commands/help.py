import discord
from discord.ext import commands

class ServerChat(commands.Cog):
    """ Commands related to helping """

    # Allows changes to the bot
    def __init__(self, bot):
        self.bot = bot

    """ Help Command """
    @commands.hybrid_command(name="help", description="Command inoformation!")
    async def help(self, ctx: commands.Context, message: str):
        # Create new embed message
        embed = discord.Embed(
            title = "Commands",
            color = discord.Color.green()
        )
        embed.add_field(name="/help", value="This shows all your available commands!", inline=True)
        
         # Send embed message
        await ctx.reply(embed=embed, ephemeral=True)


    """ Help Mpd Command """
    @commands.hybrid_command(name="helpmod", description="Command inoformation!")
    async def helpmod(self, ctx: commands.Context, message: str):

        # Check if user has permissions
        if not any(role.name in ["Admin", "SMP Mod"] for role in ctx.author.roles):
            await ctx.reply("You don't have the required role to use this command.", ephemeral=True)
            return
        
        # Create new embed message
        embed = discord.Embed(
            title = "Mod Commands",
            color = discord.Color.dark_green()
        )
        embed.add_field(name="/whitelist", value="This whitelists a Java or Bedrock user. If used in same chat they typed their username, will react to it with a green checkmark.", inline=True)
        
         # Send embed message
        await ctx.reply(embed=embed, ephemeral=True)