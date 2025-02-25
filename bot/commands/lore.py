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
                max_new_tokens=300,  # Keep as is unless you want shorter output
                temperature=1.2,     # Increase randomness for more absurdity
                top_k=20,            # Lower k to allow more surprising word choices
                top_p=0.7,           # Reduce p slightly to limit safe predictions
                repetition_penalty=1.1  # Helps prevent looping or overly structured responses
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
    async def lore(self, ctx: commands.Context, username: str, gender:str):
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
        prompt = f"""Extremely FUNNY, DARK stories about people: 
            Write about (He) Gregory, Gregory the Bug Catcher once tripped over his own net, accidentally unleashing a swarm of Beedrill into a preschool, then tried to blame it on a Pidgey. It killed all the children.
            Write about (She) Nurse Joy, Nurse Joy lost her license after using an unconscious trainer’s Pokémon for underground fight clubs, claiming it was "for their own growth." She then killed the pokemon and comitted suicide.
            Write about (He) Rival Dennis, Rival Dennis once tried to steal a rare Cobblemon, only to find out it secretes hallucinogenic slime, leaving him naked in a fountain, screaming about the moon and pissing all over.
            Write about (They) Gym Leader Cassidy, Gym Leader Cassidy installed a trapdoor under the battlefield, challengers who stepped on the wrong tile. They fell into a pit of horny donkeys that use them till they died.
            Write about (Her) Professor Elm's intern, Kylie, Professor Elm's intern, Kylie, accidentally created a Cobblemon so genetically unstable, it phases in and out of existence—stealing souls with each return and ate shit.
            Write ONE FINAL story similar to these, but 10x longer and darker: Write about ({gender}) {username}, """


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