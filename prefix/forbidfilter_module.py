# Discord Bot / Template for banned_words filtering (Editable)

# A file that enables filtering of banned_words in all Discord channels.
# Discord bot will output a warning message when it detects chat containing banned_words.
# Create a banned_words list file yourself

import discord
import os
import json
from discord.ext import commands

# Load banned_words list
banned_words = []

# Server environment variables or your own .json file
def load_banned_words():
    banned_words_raw = os.getenv("BANNED_WORDS")
    if not banned_words_raw:
        print("⚠️ The banned_words file does not exist.")
        return []
    try:
        return json.loads(banned_words_raw)
    except json.JSONDecodeError:
        print("❌ The JSON file format is incorrect.")
        return []

def register_prohibition_filter(bot):
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix='*', intents=intents)

    banned_words = load_banned_words()

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

    return bot
