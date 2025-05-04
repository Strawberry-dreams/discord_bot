# Discord Bot Basic Integration Program
# If you type (*hello) in any chat window, the bot will output (Hello)

import discord # Reference the discord.py library (needs to be installed separately)
import os
from discord.ext import commands # Discord Extension Command Set Reference
from dotenv import load_dotenv

intents = discord.Intents.default() # Setting Intents
intents.message_content = True

# If you installed Python directly on macOS, you will need an SSL certificate issued by a trusted certificate authority (CA).
# Enter the command /Applications/Python\ 3.11/Install\ Certificates.command in the terminal (depending on the python version)

client = commands.Bot(command_prefix='*', intents=intents)

@client.command() # Actual Command Part
async def hello(ctx):
    await ctx.send('Hello')


# 1. Load token securely from .env file
load_dotenv(dotenv_path="DISCORD_TOKEN.env")
TOKEN = os.getenv("DISCORD_TOKEN")

client.run(TOKEN)

# 2. Or directly enter the token here (not recommended for real deployments)
# client.run("your_bot_token")
