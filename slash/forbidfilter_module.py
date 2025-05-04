# Discord Bot / Template for banned_words filtering (Editable)

# A file that enables filtering of banned_words in all Discord channels.
# Discord bot will output a warning message when it detects chat containing banned_words.
# Create a banned_words list file yourself

import discord
import os
import json
from discord import app_commands
from dotenv import load_dotenv

# Load banned_words list
banned_words = []

# Server environment variables or your own .json file
def load_prohibited_words():
    banned_words_env = os.getenv("BANNED_WORDS")
    if not banned_words_env:
        print("⚠️ The banned_words file does not exist.")
        return []
    try:
        return json.loads(banned_words_env)
    except json.JSONDecodeError:
        print("❌ The JSON file format is incorrect.")
        return []

def reload_prohibited_words():
    global banned_words
    banned_words = load_prohibited_words()
    print("📥 Refreshed the banned_words list!")

# Message filtering logic
async def on_message_filter(message: discord.Message):
    if message.author.bot:
        return

    lowered = message.content.lower()
    detected_words = [word for word in banned_words if word in lowered]

    if detected_words:
        words_list = ", ".join(f"**{word}**" for word in detected_words)
        await message.channel.send(
            f"⚠️ {message.author.mention} Beep~~ No bad words {words_list}! No! 🛑🧸"
        )

# Registering slash commands
def setup_filter_commands(tree: app_commands.CommandTree):
    @tree.command(name="reloadbw", description="Reload the list of banned_words.")
    async def reload_banned_words_command(interaction: discord.Interaction):
        reload_prohibited_words()
        await interaction.response.send_message("📥 Refreshed the banned_words list!", ephemeral=True)
