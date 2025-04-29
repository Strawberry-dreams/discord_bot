# Discord 모집 채널의 멤버 모집용 기능을 모아놓은 프로그램 (Module 방식)
# 모집 채널에서 (*모집), (*파티), (*변경), (*나가기), (*명령어)를 입력하면 각각의 기능을 실행함

import discord
from discord.ext import commands
from discord.ui import View, Select, Button

RECRUIT_CHANNEL_ID = 1361245403147931669 # 실제 모집 채널 ID로 교체

GAMES = {
    "League of Legends": {
        "max_players": 5,
        "roles": ["탑", "정글", "미드", "원딜", "서포터"]
    },
    "PUBG": {
        "max_players": 4,
        "roles": []
    },
    "Overwatch": {
        "max_players": 5,
        "roles": ["딜러1", "딜러2", "탱커", "힐러1", "힐러2"]
    }
}

party_status = {game: {"players": {}, "id": None} for game in GAMES}
user_parties = {}

shared_views = {}

async def send_party_embed(interaction, game):
    info = GAMES[game]
    embed = discord.Embed(
        title=f"{game} 파티 모집",
        description=f"최대 인원: {info['max_players']}명\n현재 참가자: {len(party_status[game]['players'])}명",
        color=discord.Color.green()
    )
    if info["roles"]:
        embed.add_field(name="역할 목록", value=", ".join(info["roles"]), inline=False)

    if game not in shared_views:
        view = View(timeout=600)
        view.add_item(JoinButton(game))
        shared_views[game] = view
    else:
        view = shared_views[game]

    await interaction.response.send_message(embed=embed, view=view)

def register_makeparty_commands(bot):
    @bot.event
    async def on_ready():
        print(f"✅ {bot.user} 봇이 실행되었습니다!")

    @bot.command()
    async def 모집(ctx):
        if ctx.channel.id != RECRUIT_CHANNEL_ID:
            return

        embed = discord.Embed(
            title="🎮 파티 생성",
            description="게임을 선택하여 파티를 생성합니다.\n이미 생성된 파티는 다시 만들 수 없습니다.",
            color=discord.Color.blue()
        )

        available_games = [
            game for game, info in party_status.items()
            if not info["players"]
        ]

        if not available_games:
            embed.description = "⚠️ 모든 게임에 대해 파티가 이미 생성되어 있습니다."
            await ctx.send(embed=embed)
            return

        view = View()
        view.add_item(GameSelect(ctx, available_games))
        await ctx.send(embed=embed, view=view)

    @bot.command()
    async def 나가기(ctx):
        user_id = ctx.author.id

        if user_id not in user_parties:
            await ctx.send("❌ 참가 중인 파티가 없습니다.")
            return

        game = user_parties[user_id]
        del party_status[game]["players"][user_id]
        del user_parties[user_id]

        if not party_status[game]["players"]:
            party_status[game]["id"] = None  # 파티 해산
            await ctx.send(f"👋 {ctx.author.display_name} 님이 `{game}` 파티에서 나갔습니다.\n💨 `{game}` 파티가 해산되었습니다.")
        else:
            await ctx.send(f"👋 {ctx.author.display_name} 님이 `{game}` 파티에서 나갔습니다.")

    @bot.command()
    async def 명령어(ctx):
        embed = discord.Embed(
            title="📘 멤버 모집 채널 안내",
            description="아래는 땅끝소초 서버의 파티 모집 기능을 위한 명령어 목록입니다.",
            color=discord.Color.green()
        )
        embed.add_field(name="`*모집`", value="게임별 파티 모집 메시지를 생성합니다.", inline=False)
        embed.add_field(name="`*파티`", value="현재 모집 중인 파티의 참가자 및 역할 정보를 확인합니다.", inline=False)
        embed.add_field(name="`*변경`", value="현재 참가 중인 파티에서 내 역할을 변경합니다.", inline=False)
        embed.add_field(name="`*나가기`", value="현재 참가 중인 파티에서 나갑니다.", inline=False)
        embed.add_field(name="`*명령어`", value="모집 채널에서 사용 가능한 명령어를 알려줍니다.", inline=False)

        await ctx.send(embed=embed)

    @bot.command()
    async def 파티(ctx):
        if ctx.channel.id != RECRUIT_CHANNEL_ID:
            return

        has_party = False
        embeds = []

        for game, info in GAMES.items():
            players = party_status[game]["players"]
            if not players:
                continue

            has_party = True
            role_members = {}
            player_lines = []

            for uid, role in players.items():
                member = ctx.guild.get_member(uid)
                if member:
                    display_name = member.display_name
                    normalized_role = role.strip().lower() if role else None
                    if normalized_role:
                        player_lines.append(f"- {display_name} ({normalized_role})")
                        if normalized_role not in role_members:
                            role_members[normalized_role] = []
                        role_members[normalized_role].append(display_name)
                    else:
                        player_lines.append(f"- {display_name}")

            embed = discord.Embed(
                title=f"{game} 파티 현황",
                description=f"현재 인원: {len(players)} / {info['max_players']}",
                color=discord.Color.teal()
            )

            if player_lines:
                embed.add_field(name="👥 참가자", value="\n".join(player_lines), inline=False)

            if info["roles"]:
                role_lines = []
                for role in info["roles"]:
                    role_key = role.strip().lower()
                    members = role_members.get(role_key, [])
                    if members:
                        role_lines.append(f"{role}: {', '.join(members)}")
                    else:
                        role_lines.append(f"{role}: ")
                embed.add_field(name="🧙 역할 현황", value="\n".join(role_lines), inline=False)

            embeds.append(embed)

        if has_party:
            for embed in embeds:
                await ctx.send(embed=embed)
        else:
            await ctx.send("📭 현재 모집 중인 파티가 없습니다.")

    @bot.command()
    async def 변경(ctx):
        user_id = ctx.author.id
        if user_id not in user_parties:
            await ctx.send("❌ 현재 참가 중인 파티가 없습니다.")
            return

        game = user_parties[user_id]
        roles = GAMES[game]["roles"]
        if not roles:
            await ctx.send(f"⚠️ `{game}` 파티에는 역할 개념이 없습니다.")
            return

        view = View()
        view.add_item(RoleUpdateSelect(game, user_id))
        await ctx.send(f"🎯 `{game}` 파티에서 변경할 역할을 선택하세요:", view=view)


class GameSelect(Select):
    def __init__(self, ctx, game_options):
        self.ctx = ctx
        options = [
            discord.SelectOption(label=game, description=f"{game} 파티 모집", value=game)
            for game in game_options
        ]
        super().__init__(placeholder="게임을 선택하세요", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        selected_game = self.values[0]
        await send_party_embed(interaction, selected_game)

class JoinButton(Button):
    def __init__(self, game):
        super().__init__(label="참가하기", style=discord.ButtonStyle.primary)
        self.game = game

    async def callback(self, interaction: discord.Interaction):
        game = self.game
        user_id = interaction.user.id

        if user_id in user_parties:
            await interaction.response.send_message("⚠️ 이미 다른 파티에 참가 중입니다. 먼저 나가주세요.", ephemeral=True)
            return

        if len(party_status[game]["players"]) >= GAMES[game]["max_players"]:
            await interaction.response.send_message("⚠️ 파티가 가득 찼습니다.", ephemeral=True)
            return

        if GAMES[game]["roles"]:
            view = View()
            view.add_item(RoleSelect(game, GAMES[game]["roles"]))
            await interaction.response.send_message("🎯 역할을 선택하세요:", view=view, ephemeral=True)
        else:
            party_status[game]["players"][user_id] = None
            user_parties[user_id] = game
            await interaction.response.send_message(f"✅ {interaction.user.display_name} 님이 `{game}` 파티에 참가했습니다!", ephemeral=False)

class RoleSelect(Select):
    def __init__(self, game, roles):
        options = [discord.SelectOption(label=role, value=role) for role in roles]
        super().__init__(placeholder="역할을 선택하세요", options=options, min_values=1, max_values=1)
        self.game = game

    async def callback(self, interaction: discord.Interaction):
        game = self.game
        role = self.values[0].strip().lower()
        user_id = interaction.user.id

        if len(party_status[game]["players"]) >= GAMES[game]["max_players"]:
            await interaction.response.send_message("⚠️ 파티가 이미 가득 찼어요!", ephemeral=True)
            return

        if user_id in user_parties:
            await interaction.response.send_message("⚠️ 이미 다른 파티에 참가 중입니다. 먼저 나가주세요.", ephemeral=True)
            return

        for uid, assigned_role in party_status[game]["players"].items():
            if assigned_role == role:
                await interaction.response.send_message(f"⚠️ `{role}` 역할은 이미 다른 참가자가 선택했습니다.", ephemeral=True)
                return

        party_status[game]["players"][user_id] = role
        user_parties[user_id] = game
        await interaction.response.send_message(f"✅ {interaction.user.display_name} 님이 `{game}` 파티에 역할 `{role}`로 참가했어요!", ephemeral=False)

class RoleUpdateSelect(Select):
    def __init__(self, game, user_id):
        options = [discord.SelectOption(label=role, value=role) for role in GAMES[game]["roles"]]
        super().__init__(placeholder="새 역할을 선택하세요", options=options, min_values=1, max_values=1)
        self.game = game
        self.user_id = user_id

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ 상호작용 불가", ephemeral=True)
            return

        role = self.values[0].strip().lower()
        game = self.game

        for uid, assigned_role in party_status[game]["players"].items():
            if uid != self.user_id and assigned_role == role:
                await interaction.response.send_message(f"⚠️ `{role}` 역할은 이미 다른 참가자가 선택했습니다.", ephemeral=True)
                return

        party_status[game]["players"][self.user_id] = role
        await interaction.response.send_message(f"🔄 역할이 `{role}`(으)로 변경되었습니다!", ephemeral=True)
