# Discord Bot / Template for banned_words filtering (Editable)

# A file that enables filtering of banned_words in all Discord channels.
# Discord bot will output a warning message when it detects chat containing banned_words.
# Create a banned_words list file yourself

import discord
import os
import json
from discord.ext import commands
from dotenv import load_dotenv

# Load banned_words list
banned_words = []

# load_dotenv(), which loads the DISCORD TOKEN, must be run before loading the banned_words list file.
load_dotenv(dotenv_path="DISCORD_TOKEN.env")

# 1. Banned_words list file extension: .txt
def load_prohibited_words():
    try:
        with open("prohibited_words.txt", "r", encoding="utf-8") as f:
            return [line.strip().lower() for line in f if line.strip()]
    except FileNotFoundError:
        print("⚠️ The banned_words file does not exist.")
        return []
    
"""
# 2. Banned_words list file extension: .json
def load_prohibited_words():
    try:
        with open("prohibited_words.json", "r", encoding="utf-8") as f:
            words = json.load(f)
            return [word.strip().lower() for word in words if isinstance(word, str) and word.strip()]
    except FileNotFoundError:
        print("⚠️ The banned_words file does not exist.")
        return []
    except json.JSONDecodeError:
        print("⚠️ The JSON file format is incorrect.")
        return []
"""

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='*', intents=intents)

# Set bot presence (only one can be active at a time)
@bot.event
async def on_ready():
    print(f'✅ {bot.user} bot has connected to Discord!')
    
    activity = discord.Game(name="game_title") # Fix this part
    # activity = discord.Streaming(name="broadcast_title", url="broadcast_link")
    # activity = discord.Activity(type=discord.ActivityType.listening, name="music_title")
    # activity = discord.Activity(type=discord.ActivityType.watching, name="video_title")

    await bot.change_presence(status=discord.Status.online, activity=activity)
    # await bot.change_presence(status=discord.Status.idle, activity=activity)
    # await bot.change_presence(status=discord.Status.dnd, activity=activity)
    # await bot.change_presence(status=discord.Status.invisible, activity=activity)

# Event: Message Watch Filtering
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    lowered = message.content.lower()
    detected_words = [word for word in banned_words if word in lowered]

    if detected_words:
        words_list = ", ".join(f"**{word}**" for word in detected_words)
        await message.channel.send(
            f"⚠️ {message.author.mention} Beep~~ No bad words {words_list}! No! 🛑🧸"
        )
        return

    await bot.process_commands(message)

# 1. Load token securely from .env file
TOKEN = os.getenv("DISCORD_TOKEN")

bot.run(TOKEN)

# 2. Or directly enter the token here (not recommended for real deployments)
# bot.run("your_bot_token")