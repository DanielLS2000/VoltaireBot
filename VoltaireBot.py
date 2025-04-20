import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from commands import campanha_cmds, player_cmds, adm_cmds, credito_cmds, general

# Setup
load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

# general
bot.add_command(general.ping)
bot.add_command(general.help_command)

# Comandos de Campanha
bot.add_command(campanha_cmds.criar_campanha)
bot.add_command(campanha_cmds.listar_campanhas)
bot.add_command(campanha_cmds.deletar_campanha)
bot.add_command(campanha_cmds.editar_campanha)
bot.add_command(campanha_cmds.adicionar_player)
bot.add_command(campanha_cmds.remover_player)
bot.add_command(campanha_cmds.analisar_campanha)

# Comandos de Player
bot.add_command(player_cmds.entrar_campanha)
bot.add_command(player_cmds.meu_perfil)
bot.add_command(player_cmds.perfil)

# Comandos de ADM
bot.add_command(adm_cmds.reset_db)
bot.add_command(adm_cmds.atualizar_info)
bot.add_command(adm_cmds.marcar_presenca_adm)

# Comandos de Credito
bot.add_command(credito_cmds.add_credito)
bot.add_command(credito_cmds.rm_credito)



bot.run(SECRET_KEY)