import json
import re
from discord.ext import commands
import discord
from config import *
from utils.picks import ck_tiers, eu4_tiers, vic_tiers, hoi_tiers, country_mapping
from fuzzywuzzy import process

def salvar_campanhas(campanhas):
    with open('campanhas.json', 'w', encoding='utf-8') as f:
        json.dump([campanha.to_dict() for campanha in campanhas], f, ensure_ascii=False, indent=4)

def salvar_players(players):
    with open('players.json', 'w', encoding='utf-8') as f:
        json.dump([player.to_dict() for player in players], f, ensure_ascii=False, indent=4)

def hora_valida(time_input):
    return re.match(r'^[0-2][0-9]:[0-5][0-9]$', time_input)

def has_role():
    async def predicate(ctx):
        return any(role.name in ALLOWED_ROLES for role in ctx.author.roles)
    return commands.check(predicate)

def admin_only():
    async def predicate(ctx):
        return ctx.author.guild_permissions.administrator
    return commands.check(predicate)

def has_protection(presenca):
    faltas = sum([1 for p in presenca if p == 0])
    ultima_sessao = presenca[-1] if len(presenca) > 0 else 1
    
    if faltas < 3 and ultima_sessao != 0:
        return True
    else:
        return False

def gerar_embed_campanhas(campanhas, guild):
    embed = discord.Embed(
        title="📋 Campanhas Ativas",
        description="Aqui estão todas as campanhas em andamento.",
        color=discord.Color.blurple()
    )

    if not campanhas:
        embed.description = "🚫 **Nenhuma campanha ativa no momento.**"
    else:
        for campanha in campanhas:
            organizador = campanha.organizador or "Desconhecido"
            membro_org = discord.utils.get(guild.members, name=organizador)
            mention_org = membro_org.mention if membro_org else organizador

            players_info = ""
            for membro in campanha.players:
                if membro:
                    membro_discord = discord.utils.get(guild.members, name=membro.user)
                    mention = membro_discord.mention if membro_discord else f"@{membro.user}"
                    players_info += f"{mention} - {membro.country}\n"
                else:
                    players_info += "N/A\n"

            embed.add_field(
                name=f"{campanha.displayName} ({campanha.week_day} às {campanha.time})",
                value=f"**Organizador:** {mention_org}\n**{len(campanha.players)} Players:**\n{players_info}",
                inline=False
            )

    return embed

def can_pick_country(player_credit, country_tag):
    for tier, countries in eu4_tiers.items():
        if country_tag in countries:
            required_credit = 750 if tier == 1 else (500 if tier == 2 else 0)
            return player_credit >= required_credit
    return True  # If country not found, assume it's allowed

def get_country_tag(user_input):
    user_input = user_input.lower().strip()
    # First, check exact matches
    if user_input in country_mapping:
        return country_mapping[user_input]
    # If no exact match, try fuzzy search
    best_match, score = process.extractOne(user_input, country_mapping.keys())
    if score > 70:  # 70% confidence threshold
        return country_mapping[best_match]
    return None  # No match found

