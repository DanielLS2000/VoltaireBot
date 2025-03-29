import json
import re
from discord.ext import commands
from config import *

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

