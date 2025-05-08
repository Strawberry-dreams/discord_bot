# Discord Bot / To run the Discord bot actually.

# A file that loads and runs a module
# This file uses the prefix command.

import discord
import os
from discord.ext import commands
from dotenv import load_dotenv

# Import functions registered in a module
from makeparty_module import register_makeparty_commands
from forbidfilter_module import register_prohibition_filter
from eventnotify_module import setup_event_commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.guild_scheduled_events = True

bot = commands.Bot(command_prefix='*', intents=intents)

# Set bot presence (only one can be active at a time)
@bot.event
async def on_ready():
    print(f'✅ {bot.user} bot has connected to Discord!')
    activity = discord.Activity(type=discord.ActivityType.listening, name="Spotify")
    await bot.change_presence(status=discord.Status.online, activity=activity)

# Import commands registered in module
register_makeparty_commands(bot)
register_prohibition_filter(bot)
setup_event_commands(bot)

# 1. Load token securely from .env file
load_dotenv(dotenv_path="DISCORD_TOKEN.env")
TOKEN = os.getenv('DISCORD_TOKEN')

bot.run(TOKEN)

# 2. Or directly enter the token here (not recommended for real deployments)
# bot.run("your_bot_token")
