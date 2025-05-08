# Discord Bot / Template for recruiting game party members (Editable)

# A file that gathers features for recruiting game party members
# This file uses the slash command.
# Example usage: Enter [/recruit] -> A message will be displayed allowing you to select a game.

import discord
import os
from discord.ui import View, Select, Button
from dotenv import load_dotenv

RECRUIT_CHANNEL_ID = 1234

GAMES = {
    "League of Legends": {
        "max_players": 5,
        "roles": ["TOP", "JGL", "MID", "ADC", "SUP"]
    },
    "PUBG": {
        "max_players": 4,
        "roles": []
    },
    "Overwatch": {
        "max_players": 5,
        "roles": ["Damage1", "Damage2", "Tank", "Support1", "Support2"]
    }
}

shared_views = {}
party_status = {game: {"players": {}} for game in GAMES}
user_parties = {}

# Initializing the client and command tree
intents = discord.Intents.default()
intents.message_content = True
intents.members = True

tree = None
class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=intents)
        self.tree = discord.app_commands.CommandTree(self)

    async def setup_hook(self):
        await setup_party_commands(self)
        await self.tree.sync()

client = MyClient()

# To check if the correct channel is selected
def ensure_recruit_channel(interaction):
    return interaction.channel_id == RECRUIT_CHANNEL_ID

# Set bot presence (only one can be active at a time)
@client.event
async def on_ready():
    print(f'✅ {client.user} bot has connected to Discord!')
    
    activity = discord.Game(name="game_title") # Fix this part
    # activity = discord.Streaming(name="broadcast_title", url="broadcast_link")
    # activity = discord.Activity(type=discord.ActivityType.listening, name="music_title")
    # activity = discord.Activity(type=discord.ActivityType.watching, name="video_title")

    await client.change_presence(status=discord.Status.online, activity=activity)
    # await client.change_presence(status=discord.Status.idle, activity=activity)
    # await client.change_presence(status=discord.Status.dnd, activity=activity)
    # await client.change_presence(status=discord.Status.invisible, activity=activity)

# Registering slash commands
async def setup_party_commands(client: discord.Client):
    tree = client.tree

    @tree.command(name="recruit", description="To create a game-specific party recruitment message.")
    async def recruit(interaction: discord.Interaction):
        if not ensure_recruit_channel(interaction):
            await interaction.response.send_message("❌ This command can only be used in the recruit channel.", ephemeral=True)
            return

        available_games = [game for game, info in party_status.items() if not info["players"]]
        embed = discord.Embed(
            title="🎮 Create Party",
            description="Create a party by selecting a game.\nParties that have already been created cannot be created again.",
            color=discord.Color.blue()
        )

        if not available_games:
            embed.description = "⚠️ For every game, a party is already created."
            await interaction.response.send_message(embed=embed)
            return

        view = View()
        view.add_item(GameSelect(interaction, available_games))
        await interaction.response.send_message(embed=embed, view=view)

    @tree.command(name="exit", description="To leave the party you are currently in.")
    async def exit(interaction: discord.Interaction):
        if not ensure_recruit_channel(interaction):
            await interaction.response.send_message("❌ This command can only be used in the recruit channel.", ephemeral=True)
            return
        
        user_id = interaction.user.id
        if user_id not in user_parties:
            await interaction.response.send_message("❌ There are currently no parties participating.", ephemeral=True)
            return

        game = user_parties[user_id]
        del party_status[game]["players"][user_id]
        del user_parties[user_id]

        if not party_status[game]["players"]:
            await interaction.response.send_message(
                f"👋 {interaction.user.mention} left the `{game}` party.\n💨 The `{game}` party has broken up.")
        else:
            await interaction.response.send_message(f"👋 {interaction.user.mention} left the `{game}` party.")

    @tree.command(name="party", description="To check the status of parties currently recruiting")
    async def party(interaction: discord.Interaction):
        if not ensure_recruit_channel(interaction):
            await interaction.response.send_message("❌ This command can only be used in the recruit channel.", ephemeral=True)
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
                member = interaction.guild.get_member(uid)
                if member:
                    display_name = member.mention
                    role_lower = role.strip().lower() if role else None
                    if role_lower:
                        player_lines.append(f"- {display_name} ({role_lower})")
                        role_members.setdefault(role_lower, []).append(display_name)
                    else:
                        player_lines.append(f"- {display_name}")

            embed = discord.Embed(
                title=f"{game} Party Status",
                description=f"Current Number of People: {len(players)} / {info['max_players']}",
                color=discord.Color.teal()
            )
            if player_lines:
                embed.add_field(name="👥 Participants", value="\n".join(player_lines), inline=False)

            if info["roles"]:
                role_lines = []
                for role in info["roles"]:
                    key = role.strip().lower()
                    members = role_members.get(key, [])
                    role_lines.append(f"{role}: {', '.join(members) if members else ''}")
                embed.add_field(name="🧙 Role Status", value="\n".join(role_lines), inline=False)

            embeds.append(embed)

        if has_party:
            for embed in embeds:
                await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("📭 There are currently no parties recruiting.")

    @tree.command(name="change", description="To change roles in the party you are currently in.")
    async def change(interaction: discord.Interaction):
        if not ensure_recruit_channel(interaction):
            await interaction.response.send_message("❌ This command can only be used in the recruit channel.", ephemeral=True)
            return

        user_id = interaction.user.id
        if user_id not in user_parties:
            await interaction.response.send_message("❌ There are currently no parties participating.", ephemeral=True)
            return

        game = user_parties[user_id]
        roles = GAMES[game]["roles"]
        if not roles:
            await interaction.response.send_message(f"⚠️ `{game}` party has no concept of roles.", ephemeral=True)
            return

        view = View()
        view.add_item(RoleUpdateSelect(game, user_id))
        await interaction.response.send_message(f"🎯 Select the role you want to change in party `{game}`:", view=view, ephemeral=True)

# Setting up interactive UI components
class GameSelect(Select):
    def __init__(self, interaction, game_options):
        self.interaction = interaction
        options = [
            discord.SelectOption(label=game, description=f"{game} Party Recruitment", value=game)
            for game in game_options
        ]
        super().__init__(placeholder="Choose a game", options=options, min_values=1, max_values=1)

    async def callback(self, interaction: discord.Interaction):
        selected_game = self.values[0]
        await send_party_embed(interaction, selected_game)

async def send_party_embed(interaction, game):
    info = GAMES[game]
    embed = discord.Embed(
        title=f"{game} Party Recruitment",
        description=f"Maximum Number of People: {info['max_players']}\nCurrent Participants: {len(party_status[game]['players'])}",
        color=discord.Color.green()
    )
    if info["roles"]:
        embed.add_field(name="Role List", value=", ".join(info["roles"]), inline=False)

    if game not in shared_views:
        view = View(timeout=600)
        view.add_item(JoinButton(game))
        shared_views[game] = view
    else:
        view = shared_views[game]

    await interaction.response.send_message(embed=embed, view=view)

class JoinButton(Button):
    def __init__(self, game):
        super().__init__(label="Participate", style=discord.ButtonStyle.primary)
        self.game = game

    async def callback(self, interaction: discord.Interaction):
        game = self.game
        user_id = interaction.user.id

        if user_id in user_parties:
            await interaction.response.send_message("⚠️ You are already in another party. Please leave first.", ephemeral=True)
            return

        if len(party_status[game]["players"]) >= GAMES[game]["max_players"]:
            await interaction.response.send_message("⚠️ The party is already full!", ephemeral=True)
            return

        if GAMES[game]["roles"]:
            view = View()
            view.add_item(RoleSelect(game, GAMES[game]["roles"]))
            await interaction.response.send_message("🎯 Select your role:", view=view, ephemeral=True)
        else:
            party_status[game]["players"][user_id] = None
            user_parties[user_id] = game
            await interaction.response.send_message(f"✅ {interaction.user.mention} joined the `{game}` party!", ephemeral=False)

class RoleSelect(Select):
    def __init__(self, game, roles):
        options = [discord.SelectOption(label=role, value=role) for role in roles]
        super().__init__(placeholder="Choose a role", options=options, min_values=1, max_values=1)
        self.game = game

    async def callback(self, interaction: discord.Interaction):
        game = self.game
        role = self.values[0].strip().lower()
        user_id = interaction.user.id

        if len(party_status[game]["players"]) >= GAMES[game]["max_players"]:
            await interaction.response.send_message("⚠️ The party is already full!", ephemeral=True)
            return

        if user_id in user_parties:
            await interaction.response.send_message("⚠️ You are already in another party. Please leave first.", ephemeral=True)
            return

        for uid, assigned_role in party_status[game]["players"].items():
            if assigned_role == role:
                await interaction.response.send_message(f"⚠️ Role `{role}` has already been chosen by another participant.", ephemeral=True)
                return

        party_status[game]["players"][user_id] = role
        user_parties[user_id] = game
        await interaction.response.send_message(f"✅ {interaction.user.mention} joined the `{game}` party as role `{role}`!", ephemeral=False)

class RoleUpdateSelect(Select):
    def __init__(self, game, user_id):
        options = [discord.SelectOption(label=role, value=role) for role in GAMES[game]["roles"]]
        super().__init__(placeholder="Choose a new role", options=options, min_values=1, max_values=1)
        self.game = game
        self.user_id = user_id

    async def callback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user_id:
            await interaction.response.send_message("❌ No interaction possible", ephemeral=True)
            return

        role = self.values[0].strip().lower()
        game = self.game

        for uid, assigned_role in party_status[game]["players"].items():
            if uid != self.user_id and assigned_role == role:
                await interaction.response.send_message(f"⚠️ Role `{role}` has already been chosen by another participant.", ephemeral=True)
                return

        party_status[game]["players"][self.user_id] = role
        await interaction.response.send_message(f"🔄 Role changed to `{role}`!", ephemeral=True)

# 1. Load token securely from .env file
load_dotenv(dotenv_path="DISCORD_TOKEN.env")
TOKEN = os.getenv("DISCORD_TOKEN")

client.run(TOKEN)

# 2. Or directly enter the token here (not recommended for real deployments)
# client.run("your_bot_token")
