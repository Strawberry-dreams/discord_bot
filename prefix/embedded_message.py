# Discord Bot / Template for embedded messages (Editable)

# A file that outputs embedded messages in a Discord channel
# Since this is for one-time message output, the prefix command is used
# Example usage: Enter [*rule] -> Output rule embedded message.

import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

CHANNEL_ID = 1234 # Replace with your actual channel ID

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='*', intents=intents) # Use the prefix you want

# Set bot presence (only one can be active at a time)
@client.event
async def on_ready():
    print(f'✅ {client.user} bot has connected to Discord!')

    activity = discord.Game(name="game_title") # Fix this part
    # activity = discord.Streaming(name="broadcast_title", url="broadcast_link")
    # activity = discord.Activity(type=discord.ActivityType.listening, name="music_title")
    # activity = discord.Activity(type=discord.ActivityType.watching, name="video_title")

    await bot.change_presence(status=discord.Status.online, activity=activity)
    # await bot.change_presence(status=discord.Status.idle, activity=activity)
    # await bot.change_presence(status=discord.Status.dnd, activity=activity)
    # await bot.change_presence(status=discord.Status.invisible, activity=activity)

# Registering prefix commands
@client.command(name="instruction_name") # Fix this part
async def command_list(ctx):
    if ctx.channel.id != CHANNEL_ID:
        await ctx.send("❌ This command can only be used on XXX channels.", ephemeral=True)
        return
        
    embed = discord.Embed(
        title="title_name", # Fix this part
        description=(
            "content1\n" # Fix this part
            "content2\n"
            "content3\n"
            "content4\n"
        ),
        color=discord.Color.green() # Use the color word you want
    )

    embed.add_field(
        name="subtitle_name1", # Fix this part
        value=(
            "content1\n" # Fix this part
            "content2\n"
            "content3\n"
            "content4\n"
        ),
        inline=False
    )

    embed.add_field(
        name="subtitle_name2", # Fix this part
        value=(
            "content1\n" # Fix this part
            "content2\n"
            "content3\n"
            "content4\n"
        ),
        inline=False
    )

    # If you are not using a footer, you can just delete this line.
    embed.set_footer(text="footer_content")
    # Timestamp for this embed message
    embed.timestamp = ctx.message.created_at

    await ctx.send(embed=embed)

# 1. Load token securely from .env file
load_dotenv(dotenv_path="DISCORD_TOKEN.env")
TOKEN = os.getenv("DISCORD_TOKEN")

client.run(TOKEN)

# 2. Or directly enter the token here (not recommended for real deployments)
# bot.run("your_bot_token")
