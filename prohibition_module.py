# Discord 채팅 채널의 금지어 필터링 기능을 작동하는 프로그램 (Module 방식)
# 채팅 채널에서 금지어가 포함된 채팅을 발견하면 경고 메시지를 출력함
# 금지어 목록은 prohibited_words.json 파일 참조

import discord
import os
import json
from discord.ext import commands

def load_banned_words():
    banned_words_raw = os.getenv("BANNED_WORDS")
    if not banned_words_raw:
        print("⚠️ 금칙어 목록이 존재하지 않습니다.")
        return []
    return json.loads(banned_words_raw)

def register_prohibition_filter(bot):
    intents = discord.Intents.default()
    intents.message_content = True
    bot = commands.Bot(command_prefix='*', intents=intents)

    banned_words = load_banned_words()

    @bot.event
    async def on_ready():
        print(f"✅ {bot.user} 봇이 실행되었습니다!")

    @bot.event
    async def on_message(message):
        if message.author.bot:
            return

        lowered = message.content.lower()
        detected_words = [word for word in banned_words if word in lowered]

        if detected_words:
            words_list = ", ".join(f"**{word}**" for word in detected_words)
            await message.channel.send(
                f"⚠️ {message.author.mention} 삐삑~~ 나쁜 단어 {words_list} 금지! 금지! 🛑🧸"
            )
            return

        await bot.process_commands(message)

    return bot
