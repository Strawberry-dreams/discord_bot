# Discord Bot / Template for event notification messages (Editable)

# A file that outputs event information in a Discord event channel.
# This file uses the prefix command.
# Example usage: Enter [*event 1] -> Output the first registered event

import discord
import os
from discord.ext import commands
from datetime import datetime, timezone
from dotenv import load_dotenv

EVENT_CHANNEL_ID = 1234 # Replace with your actual channel ID

intents = discord.Intents.default()
intents.guild_scheduled_events = True
intents.message_content = True

bot = commands.Bot(command_prefix="*", intents=intents)

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

# Registering prefix commands
@bot.command(name="event")
async def show_specific_event(ctx, index: int):
    if ctx.channel.id != EVENT_CHANNEL_ID:
        await ctx.send("❌ This command can only be used on event channels.", ephemeral=True)
        return

    events = await ctx.guild.fetch_scheduled_events()

    # Filter only valid events
    now = datetime.now(timezone.utc)
    valid_events = [
        event for event in events
        if not event.end_time or event.end_time > now
    ]

    if not valid_events:
        await ctx.send("There are no current or upcoming events.", ephemeral=True)
        return

    if index <= 0 or index > len(valid_events):
        await ctx.send(f"❌ Incorrect number. Please enter betwennt (1 ~ {len(valid_events)})", ephemeral=True)
        return

    # Select from valid events
    event = valid_events[index - 1]

    embed = discord.Embed(
        title=f"event {index} - {event.name}",
        description=event.description or "No description",
        color=discord.Color.blue()
    )

    # Show end-time timestamp
    if event.end_time:
        unix_timestamp = int(event.end_time.timestamp())
        remaining_str = f"<t:{unix_timestamp}:R>"
    else:
        remaining_str = "No end-time information"

    embed.add_field(name="⏳ Time left until the end", value=remaining_str, inline=False)

    # Show event creator
    if event.creator:
        creator_mention = event.creator.mention
    else:
        creator_mention = "Unknown"

    embed.add_field(name="👤 Event Creator", value=creator_mention, inline=False)

    # Show event location
    if event.location:
        embed.add_field(name="📍 Event Location", value=event.location, inline=False)

    # Insert cover image
    if event.cover_image:
        embed.set_image(url=event.cover_image.url)

    await ctx.send(embed=embed)

# 1. Load token securely from .env file
load_dotenv(dotenv_path="DISCORD_TOKEN.env")
TOKEN = os.getenv("DISCORD_TOKEN")

bot.run(TOKEN)

# 2. Or directly enter the token here (not recommended for real deployments)
# bot.run("your_bot_token")
