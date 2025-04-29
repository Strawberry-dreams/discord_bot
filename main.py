# 명령 프롬프트에서 main.py 단독 실행하는 코드
# python "C:\Users\jh080\OneDrive\바탕 화면\discord bot\module\main.py"

import discord
import os
from discord.ext import commands

# 등록 함수 불러오기
from makeparty_module import register_makeparty_commands
from prohibition_module import register_prohibition_filter
from eventalert_module import setup_event_commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
intents.guild_scheduled_events = True

bot = commands.Bot(command_prefix='*', intents=intents)

@bot.event
async def on_ready():
    print(f'✅ {bot.user} 봇이 실행되었습니다!')
    print("🔍 등록된 명령어 목록:")
    for cmd in bot.commands:
        print(f" - {cmd.name}")

# 모듈별 명령어 등록
register_makeparty_commands(bot)
register_prohibition_filter(bot)
setup_event_commands(bot)

TOKEN = os.getenv('DISCORD_TOKEN')

bot.run(TOKEN)
