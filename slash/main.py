# Discord Bot / To run the Discord bot actually.

# A file that loads and runs a module
# This file uses the slash command.

import discord
import os
from dotenv import load_dotenv

# Import functions registered in a module
from eventnotify_module import setup_event_commands
from makeparty_module import setup_party_commands
from forbidfilter_module import load_prohibited_words, reload_prohibited_words, on_message_filter, setup_filter_commands

# Load tokens from .env file
load_dotenv(dotenv_path="DISCORD_TOKEN.env")
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.guild_scheduled_events = True
intents.message_content = True
intents.members = True

# Initializing the client and command tree
class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = discord.app_commands.CommandTree(self)
        self.banned_words = []

    # Register commands in module
    async def setup_hook(self):
        await setup_event_commands(self)
        await setup_party_commands(self)
        self.banned_words = load_prohibited_words()

        reload_prohibited_words()
        setup_filter_commands(self.tree)
        await self.tree.sync()
    
    # Set bot presence (only one can be active at a time)
    async def on_ready(self):
        print(f'✅ {self.user} bot has connected to Discord!')
        activity = discord.Activity(type=discord.ActivityType.listening, name="Spotify")
        await self.change_presence(status=discord.Status.online, activity=activity)

    async def on_message(self, message: discord.Message):
        await on_message_filter(message)

client = MyClient()

client.run(TOKEN)

# Or directly enter the token here (not recommended for real deployments)
# client.run("your_bot_token")
