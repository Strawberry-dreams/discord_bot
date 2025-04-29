import discord
from discord.ext import commands
from datetime import datetime, timezone

# ===========================
# 이벤트 모듈 (채널 ID 포함)
# ===========================

EVENT_CHANNEL_ID = 1336536074444603456 # 여기에 고정

def setup_event_commands(bot):
    
    @bot.command(name="이벤트")
    async def show_specific_event(ctx, index: int):
        if ctx.channel.id != EVENT_CHANNEL_ID:
            await ctx.send("❌ 이 명령어는 이벤트 채널에서만 사용할 수 있습니다.")
            return

        events = await ctx.guild.fetch_scheduled_events()

        now = datetime.now(timezone.utc)
        valid_events = [
            event for event in events
            if not event.end_time or event.end_time > now
        ]

        if not valid_events:
            await ctx.send("현재 진행 중이거나 예정된 이벤트가 없습니다!")
            return

        if index <= 0 or index > len(valid_events):
            await ctx.send(f"❌ 잘못된 번호입니다. (1 ~ {len(valid_events)} 사이로 입력하세요)")
            return

        event = valid_events[index - 1]

        embed = discord.Embed(
            title=f"이벤트 {index} - {event.name}",
            description=event.description or "설명 없음",
            color=discord.Color.blue()
        )

        if event.end_time:
            unix_timestamp = int(event.end_time.timestamp())
            remaining_str = f"<t:{unix_timestamp}:R>"
        else:
            remaining_str = "종료 시간 정보 없음"

        embed.add_field(name="⏳ 종료까지 남은 시간", value=remaining_str, inline=False)

        if event.creator:
            creator_mention = event.creator.mention
        else:
            creator_mention = "알 수 없음"

        embed.add_field(name="👤 이벤트 작성자", value=creator_mention, inline=False)

        if event.location:
            embed.add_field(name="📍 이벤트 장소", value=event.location, inline=False)

        if event.cover_image:
            embed.set_image(url=event.cover_image.url)

        await ctx.send(embed=embed)
