# Discord 채팅 채널의 금지어 필터링 기능을 작동하는 프로그램 (Module 방식)
# 채팅 채널에서 금지어가 포함된 채팅을 발견하면 경고 메시지를 출력함
# 금지어 목록은 prohibited_words.txt 파일 참조

import discord
from discord.ext import commands

def load_prohibited_words():
    try:
        file_path = r"C:\Users\jh080\OneDrive\바탕 화면\discord bot\module\prohibited_words.txt"
        with open(file_path, "r", encoding="utf-8") as f:
            return [line.strip().lower() for line in f if line.strip()]
    except FileNotFoundError:
        print("⚠️ 금칙어 파일이 존재하지 않습니다.")
        return []

def register_prohibition_filter(bot):
    prohibited_words = load_prohibited_words()

    @bot.event
    async def on_ready():
        print(f"✅ {bot.user} 봇이 실행되었습니다!")

    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return

        lowered = message.content.lower()
        for word in prohibited_words:
            if word in lowered:
                await message.channel.send(
                    f"⚠️ {message.author.mention} 삐삑~~ 나쁜 단어 [**{word}**] 금지! 금지! 🛑🧸"
                )
                return  # 명령어 처리 중단

        await bot.process_commands(message)
