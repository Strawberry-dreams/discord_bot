import discord
import os
from dotenv import load_dotenv
from eventnotify_module import setup_event_commands
from makeparty_module import setup_party_commands
from forbidfilter_module import load_prohibited_words, reload_prohibited_words, on_message_filter, setup_filter_commands

# .env에서 토큰 로드
load_dotenv(dotenv_path="DISCORD_TOKEN.env")
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.guild_scheduled_events = True
intents.message_content = True
intents.members = True

# 클라이언트 클래스 정의
class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = discord.app_commands.CommandTree(self)
        self.banned_words = []

    async def setup_hook(self): # 모듈에서 명령어 등록
        await setup_event_commands(self)
        await setup_party_commands(self)
        self.banned_words = load_prohibited_words()

        reload_prohibited_words()
        setup_filter_commands(self.tree)
        await self.tree.sync()
    
    async def on_ready(self):
        print(f"✅ {self.user} 봇이 실행되었습니다!")
        activity = discord.Activity(type=discord.ActivityType.listening, name="Spotify") # Spotify 듣는 중
        await self.change_presence(status=discord.Status.online, activity=activity)

    async def on_message(self, message: discord.Message):
        await on_message_filter(message)

client = MyClient()

# 봇 실행
client.run(TOKEN)
