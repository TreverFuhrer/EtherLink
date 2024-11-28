from discord.ext import commands
from huggingface_hub import InferenceClient
from dotenv import load_dotenv
import os

load_dotenv()
HUGGING_FACE_API_TOKEN = os.getenv("HUGGING_FACE_API_TOKEN")
INPUT_CHANNEL_ID = 1306010586143916086
OUTPUT_CHANNEL_ID = 1303443844138008778

class LoreUpdate(commands.Cog):
    """ Commands related to daily lore generation """
    
    # Allows changes to the bot
    def __init__(self, bot):
        self.bot = bot

    """ Server Chat Command """
    @commands.hybrid_command(name="lore_update", description="Trev's test command for something secret")
    async def lore_update(self, ctx: commands.Context):
        await ctx.defer(ephemeral=True)

        # Check if user has "Admin" role
        if not any(role.name == "Admin" for role in ctx.author.roles):
            await ctx.reply("You don't have the required role to use this command.", ephemeral=True)
            return

        # Test prompt
        prompt = ("Write one large paragraph that is a creative, fantasy story of lore for the Neo SMP Minecraft server:")
        print(prompt + "\n\n\n")

        # Generate the lore update
        try:
            client = InferenceClient(token=HUGGING_FACE_API_TOKEN, model="mistralai/Mistral-7B-v0.1")
            lore_update = client.text_generation(
                prompt,
                max_new_tokens=300,  # Maximum tokens to generate
                temperature=0.8,     # Adjust randomness
                top_k=50,            # Top-k sampling
                top_p=0.9           # Top-p sampling for nucleus sampling
            )
            print(lore_update + "\n\n\n")
        except Exception as e:
            await ctx.reply(f"Error generating lore: {str(e)}", ephemeral=True)
            return

        # Get the output channel
        output_channel = self.bot.get_channel(OUTPUT_CHANNEL_ID)
        if not output_channel:
            await ctx.reply("Output channel not found.", ephemeral=True)
            return

        # Send the generated lore update to the output channel
        await output_channel.send(f"**Daily Lore Update:**\n{lore_update}")
        await ctx.reply("Lore update successfully generated and sent to the output channel.", ephemeral=True)




# Setup Cog
async def setup(bot):
    await bot.add_cog(LoreUpdate(bot))







'''
        input_channel = self.bot.get_channel(INPUT_CHANNEL_ID)
        messages = await input_channel.history(limit=30).flatten()

        # Process messages: extract author and embed description
        message_data = [
            f"{msg.author.name}: {msg.embeds[0].description if msg.embeds else msg.content}" 
            for msg in messages
        ]

        # Create a prompt for the AI model
        prompt = (
            "Here are the last 30 important messages from our Discord server:\n\n"
            + "\n".join(message_data)
            + "\n\nBased on this, write a creative daily lore update for this Minecraft server:"
        )'''