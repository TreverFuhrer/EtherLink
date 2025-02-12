import discord
from discord.ext import commands
from handlers import chat_handler
import requests

class Profile(commands.Cog):
    """ Commands related to server chat """
    
    # Allows changes to the bot
    def __init__(self, bot):
        self.bot = bot

    """ Server Chat Command """
    @commands.hybrid_command(name="profile", description="See a uses NeoSMP user profile!")
    async def profile(self, ctx: commands.Context, username: str):
        
        if str.startswith("."):
            str = str[1:] # Remove . from start of name
            url = chat_handler.get_head_image_bedrock(str)
        else:
            url = chat_handler.get_head_image_java(str)
            response = requests.get(url)
            if response.status_code == 404:
                # Not valid java player so try bedrock
                url = chat_handler.get_head_image_bedrock(str)

        response = requests.get(url)
        if response.status_code == 404:
            # Not valid java or bedrock
            await ctx.reply(f"{str} is not a valid java or bedrock username.", ephemeral=True)
            return

        # Create profile embed message
        embed = discord.Embed(
            embed.set_author(name=str, icon_url=url),
            color = chat_handler.name_to_color(str)
        )
        embed.add_field(name="Blocks Minded", value="1001", inline=True)
        
        # Send embed message
        await ctx.reply(embed=embed)


# Setup Cog
async def setup(bot):
    bot.remove_command("profile")
    await bot.add_cog(Profile(bot))