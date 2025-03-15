import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from utils import salvar_campanhas, hora_valida
from classes import Campanha, MembroCampanha, Player
from classes_menu import GameView, WeekDayView
# Setup
load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

campanhas = []

@bot.command(name='criarcampanha')
async def criar_campanha(ctx):
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    # 1. Nome da Campanha
    await ctx.send("📜 Qual o **nome da campanha**?")
    nome_msg = await bot.wait_for('message', check=check)
    display_name = nome_msg.content

    # 2. Escolha do Jogo via Select Menu
    game_view = GameView()
    await ctx.send("🎮 Selecione o **jogo** da campanha:", view=game_view)
    await game_view.wait()
    if not game_view.game:
        await ctx.send("⛔ Você não escolheu um jogo. Comando cancelado.")
        return
    game = game_view.game

    # 3. Escolha do Dia da Semana via Select Menu
    week_day_view = WeekDayView()
    await ctx.send("📆 Selecione o **dia da semana** da campanha:", view=week_day_view)
    await week_day_view.wait()
    if not week_day_view.week_day:
        await ctx.send("⛔ Você não escolheu um dia da semana. Comando cancelado.")
        return
    week_day = week_day_view.week_day

    # 4. Horário com validação (HH:MM)
    await ctx.send("🕒 Digite o **horário** no formato `HH:MM` (ex: 20:30):")
    while True:
        time_msg = await bot.wait_for('message', check=check)
        time_input = time_msg.content.strip()

        if hora_valida(time_input):
            time = time_input
            break
        else:
            await ctx.send("⛔ Formato inválido! Por favor, use o formato `HH:MM` (ex: 20:30).")

    # Cria o ID da campanha simples
    campanha_id = len(campanhas) + 1

    # Cria e salva a campanha
    nova_campanha = Campanha(
        id=campanha_id,
        displayName=display_name,
        game=game,
        time=time,
        week_day=week_day
    )

    campanhas.append(nova_campanha)
    salvar_campanhas(campanhas)

    await ctx.send(f"✅ Campanha **{display_name}** criada com sucesso!\n🎮 Jogo: {game}\n📆 Dia: {week_day}\n🕒 Horário: {time}")


bot.run(SECRET_KEY)