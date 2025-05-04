# Discord Bot / Template for recruiting game party members (Editable)

# A file that gathers features for recruiting game party members
# This file uses the prefix command.
# Example usage: Enter [*recruit] -> A message will be displayed allowing you to select a game.

import discord
from discord.ext import commands
from discord.ui import View, Select, Button

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
party_status = {game: {"players": {}, "id": None} for game in GAMES}
user_parties = {}

# To check if the correct channel is selected
def ensure_recruit_channel(ctx):
    return ctx.channel_id == RECRUIT_CHANNEL_ID

# Registering prefix commands
def register_makeparty_commands(bot):
    @bot.command()
    async def recruit(ctx):
        if not ensure_recruit_channel(ctx):
            await ctx.send("❌ This command can only be used in the recruit channel.", ephemeral=True)
            return
        
        embed = discord.Embed(
            title="🎮 Create Party",
            description="Create a party by selecting a game.\nParties that have already been created cannot be created again.",
            color=discord.Color.blue()
        )

        available_games = [
            game for game, info in party_status.items()
            if not info["players"]
        ]

        if not available_games:
            embed.description = "⚠️ For every game, a party is already created."
            await ctx.send(embed=embed)
            return

        view = View()
        view.add_item(GameSelect(ctx, available_games))
        await ctx.send(embed=embed, view=view)

    @bot.command()
    async def exit(ctx):
        if not ensure_recruit_channel(ctx):
            await ctx.send("❌ This command can only be used in the recruit channel.", ephemeral=True)
            return
        
        user_id = ctx.author.id
        if user_id not in user_parties:
            await ctx.send("❌ There are no parties currently attending.")
            return

        game = user_parties[user_id]
        del party_status[game]["players"][user_id]
        del user_parties[user_id]

        if not party_status[game]["players"]:
            party_status[game]["id"] = None # Party break up
            await ctx.send(f"👋 {ctx.author.display_name} left the `{game}` party.\n💨 The `{game}` party has broken up.")
        else:
            await ctx.send(f"👋 {ctx.author.display_name} left the `{game}` party.")

    @bot.command()
    async def party(ctx):
        if not ensure_recruit_channel(ctx):
            await ctx.send("❌ This command can only be used in the recruit channel.", ephemeral=True)
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
                title=f"{game} Party Status",
                description=f"Current Number of People: {len(players)} / {info['max_players']}",
                color=discord.Color.teal()
            )

            if player_lines:
                embed.add_field(name="👥 Participants", value="\n".join(player_lines), inline=False)

            if info["roles"]:
                role_lines = []
                for role in info["roles"]:
                    role_key = role.strip().lower()
                    members = role_members.get(role_key, [])
                    if members:
                        role_lines.append(f"{role}: {', '.join(members)}")
                    else:
                        role_lines.append(f"{role}: ")
                embed.add_field(name="🧙 Role Status", value="\n".join(role_lines), inline=False)

            embeds.append(embed)

        if has_party:
            for embed in embeds:
                await ctx.send(embed=embed)
        else:
            await ctx.send("📭 There are currently no parties recruiting.")

    @bot.command()
    async def change(ctx):
        if not ensure_recruit_channel(ctx):
            await ctx.send("❌ This command can only be used in the recruit channel.", ephemeral=True)
            return
        
        user_id = ctx.author.id
        if user_id not in user_parties:
            await ctx.send("❌ There are currently no parties participating.")
            return

        game = user_parties[user_id]
        roles = GAMES[game]["roles"]
        if not roles:
            await ctx.send(f"⚠️ `{game}` party has no concept of roles.")
            return

        view = View()
        view.add_item(RoleUpdateSelect(game, user_id))
        await ctx.send(f"🎯 Select the role you want to change in party `{game}`:", view=view)

# Setting up interactive UI components
class GameSelect(Select):
    def __init__(self, ctx, game_options):
        self.ctx = ctx
        options = [
            discord.SelectOption(label=game, description=f"{game} Party Recruitment", value=game)
            for game in game_options
        ]
        super().__init__(placeholder="Choose a game", min_values=1, max_values=1, options=options)

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
        view = View(timeout=600) # Disable button after 10 minutes
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
            await interaction.response.send_message(f"✅ {interaction.user.display_name} joined the `{game}` party!", ephemeral=False)

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
            await interaction.response.send_message("⚠️ You are already in another party. Please leave first..", ephemeral=True)
            return

        for uid, assigned_role in party_status[game]["players"].items():
            if assigned_role == role:
                await interaction.response.send_message(f"⚠️ Role `{role}` has already been chosen by another participant.", ephemeral=True)
                return

        party_status[game]["players"][user_id] = role
        user_parties[user_id] = game
        await interaction.response.send_message(f"✅ {interaction.user.display_name} joined the `{game}` party as role `{role}`!", ephemeral=False)

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
