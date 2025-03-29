import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from commands import campanha_cmds, player_cmds

# Setup
load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# @bot.event
# async def on_ready():
#     global campanhas
#     campanhas = campanha_cmds.load_campanhas()
#     print(campanhas[0])
#     print(f'✅ {bot.user.name} está online e pronto pra gerenciar suas campanhas!')

# Comandos de Campanha
bot.add_command(campanha_cmds.criar_campanha)
bot.add_command(campanha_cmds.listar_campanhas)
bot.add_command(campanha_cmds.deletar_campanha)
bot.add_command(campanha_cmds.editar_campanha)
bot.add_command(campanha_cmds.adicionar_player)
bot.add_command(campanha_cmds.analisar_campanha)

# Comandos de Player
bot.add_command(player_cmds.entrar_campanha)
bot.add_command(player_cmds.marcar_presenca)
bot.add_command(player_cmds.meu_perfil)
bot.add_command(player_cmds.perfil)



bot.run(SECRET_KEY)