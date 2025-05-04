# filter.py — 금지어 필터 기능 모듈화
import discord
import os
from discord import app_commands

banned_words = []

# 금지어 로드 함수
"""
def load_prohibited_words():
    try:
        with open("prohibited_words.txt", "r", encoding="utf-8") as f:
            return [line.strip().lower() for line in f if line.strip()]
    except FileNotFoundError:
        print("⚠️ 금칙어 파일이 존재하지 않습니다.")
        return []
"""

def load_prohibited_words():
    prohibited_words_env = os.getenv("BANNED_WORDS")
    if not prohibited_words_env:
        print("⚠️ 환경변수 'BANNED_WORDS'가 설정되어 있지 않습니다.")
        return []
    return [word.strip().lower() for word in prohibited_words_env.split(",") if word.strip()]


def reload_prohibited_words():
    global banned_words
    banned_words = load_prohibited_words()
    print("📥 금지어 목록을 새로 불러왔습니다.")

# 메시지 필터링 로직
async def on_message_filter(message: discord.Message):
    if message.author.bot:
        return

    lowered = message.content.lower()
    detected_words = [word for word in banned_words if word in lowered]

    if detected_words:
        words_list = ", ".join(f"**{word}**" for word in detected_words)
        await message.channel.send(
            f"⚠️ {message.author.mention} 삐삑~~ 나쁜 단어 {words_list} 금지! 금지! 🛑🧸"
        )

# 슬래시 명령어 등록 함수
def setup_filter_commands(tree: app_commands.CommandTree):
    @tree.command(name="금지어리로드", description="금지어 목록을 다시 불러옵니다.")
    async def reload_banned_words_command(interaction: discord.Interaction):
        reload_prohibited_words()
        await interaction.response.send_message("📥 금지어 목록을 새로 불러왔습니다!", ephemeral=True)
