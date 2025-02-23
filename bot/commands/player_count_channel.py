import discord
from discord.ext import commands
from database import get_channels, add_channel

class CreatePlayerCountChannel(commands.Cog):
    """ Commands related to server chat """
    
    # Allows changes to the bot
    def __init__(self, bot):
        self.bot = bot

    """ Server Chat Command """
    @commands.hybrid_command(name="createplayercountchannel", description="Creates a channel that displays online player count!")
    async def createplayercountchannel(self, ctx: commands.Context):

        # Check if user has permissions
        if not any(role.name in ["Admin"] for role in ctx.author.roles):
            await ctx.reply("You don't have the required role to use this command.", ephemeral=True)
            return

        # Check if channel already exists
        channels = get_channels(ctx.guild.id)
        channel_id = channels.get("player_count")
        if channel_id:
            await ctx.reply("⚠️ You already have a player count channel.", ephemeral=True)
            return
        
        guild = ctx.guild

        # Permissions for new channel
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=True, connect=False, speak=False)
        }

        # Create the voice channel
        new_channel = await guild.create_voice_channel(name="Online: #", overwrites=overwrites)
        
        # Add channel to database
        add_channel(ctx.guild.id, new_channel.id, "player_count")
        
        # Send embed message
        await ctx.reply("Created channel!", ephemeral=True)


# Setup Cog
async def setup(bot):
    await bot.add_cog(CreatePlayerCountChannel(bot))