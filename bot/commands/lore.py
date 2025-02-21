import discord
from discord.ext import commands
from huggingface_hub import InferenceClient
from handlers import chat_handler
from dotenv import load_dotenv
import requests
import os

load_dotenv()
HUGGING_FACE_API_TOKEN = os.getenv("HUGGING_FACE_API_TOKEN")
INPUT_CHANNEL_ID = 1306010586143916086
OUTPUT_CHANNEL_ID = 1303443844138008778

# Generate lore for user
async def genLore(prompt):
        try:
            client = InferenceClient(token=HUGGING_FACE_API_TOKEN, model="HuggingFaceH4/zephyr-7b-beta")
            lore_update = client.text_generation(
                prompt,
                max_new_tokens=300,  # Maximum tokens to generate
                temperature=0.8,     # Adjust randomness
                top_k=50,            # Top-k sampling
                top_p=0.9           # Top-p sampling for nucleus sampling
            )
            return lore_update
        except Exception as e:
            return e
        
class Lore(commands.Cog):
    """ Commands related to server chat """
    
    # Allows changes to the bot
    def __init__(self, bot):
        self.bot = bot

    """ Server Chat Command """
    @commands.hybrid_command(name="lore", description="Generate funny lore about someone!")
    async def lore(self, ctx: commands.Context, username: str):
        await ctx.defer() # Delay discord response
        
        if username.startswith("."):
            username = username[1:] # Remove . from start of name
            url = chat_handler.get_head_image_bedrock(username)
        else:
            url = chat_handler.get_head_image_java(username)
            response = requests.get(url)
            if response.status_code == 404:
                # Not valid java player so try bedrock
                url = chat_handler.get_head_image_bedrock(username)

        response = requests.get(url)
        if response.status_code == 404:
            # Not valid java or bedrock
            await ctx.reply(f"{username} is not a valid java or bedrock username.", ephemeral=True)
            return
        
        # Generate Lore
        prompt = f"""Write a darkly humorous and unpredictable Cobblemon adventure story starring '{username}'.
            Begin with a classic, lighthearted Pokémon journey filled with excitement and optimism. As the story progresses, introduce a sudden, dramatic, and absurdly dark twist that adds an unexpected and entertaining dimension.

            Incorporate the following elements:
            - A wild Cobblemon exhibiting bizarre and unhinged behavior.
            - A battle that escalates from a simple match to complete chaos.
            - An encounter at a Pokémon Center or Gym that leads to unforeseen disaster.
            - A rival or NPC experiencing a series of hilariously unfortunate events.
            - A twist ending that leaves '{username}' either triumphantly absurd or deeply contemplative.

            Infuse the narrative with dry, sarcastic humor, ironic twists, and exaggerated scenarios. Ensure the dialogue is lively, filled with quick-witted exchanges, and embraces the story's absurdity.

            Aim for a story length of approximately 500-700 words to maintain engagement and coherence. Use proper grammar and punctuation to enhance readability and comedic effect."""


        lore = await genLore(prompt)

        if isinstance(lore, Exception):
            await ctx.reply(f"Error generating lore: {str(lore)}", ephemeral=True)
            return
        
        # Create profile embed message
        embed = discord.Embed(
            color = chat_handler.name_to_color(username)
        )
        embed.description = lore
        embed.set_author(name=username, icon_url=url)
        
        # Send embed message
        await ctx.reply(embed=embed)


# Setup Cog
async def setup(bot):
    await bot.add_cog(Lore(bot))