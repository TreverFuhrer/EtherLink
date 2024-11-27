from discord.ext import commands
from websocket_client import send_signal

class ServerChat(commands.Cog):
    """ Commands related to server chat """

    # Allows changes to the bot
    def __init__(self, bot):
        self.bot = bot

    """ Server Chat Command """
    @commands.hybrid_command(name="server_chat", description="Send a message to the Minecraft server")
    async def server_chat(self, ctx: commands.Context, message: str):
        if not any(role.name == "Admin" for role in ctx.author.roles):
            await ctx.reply("You don't have the required role to use this command.", ephemeral=True)
            return
        await ctx.reply(f"Message to server: {message}", ephemeral=True)
        await send_signal("SERVER_CHAT", {"message": message}, ctx)


async def setup(bot):
    await bot.add_cog(ServerChat(bot))