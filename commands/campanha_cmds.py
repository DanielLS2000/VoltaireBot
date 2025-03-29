import discord
from discord.ext import commands
from utils.utils import salvar_campanhas, salvar_players, hora_valida, has_role, admin_only
from models.campanha import campanhas, Campanha
from models.player import players, Player
from models.membro_campanha import MembroCampanha
from chat_interface import GameView, WeekDayView
from config import *


@commands.command(name='criarcampanha')
@has_role()
async def criar_campanha(ctx):
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    # 1. Nome da Campanha
    await ctx.send("📜 Qual o **nome da campanha**?")
    nome_msg = await ctx.bot.wait_for('message', check=check)
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
        time_msg = await ctx.bot.wait_for('message', check=check)
        time_input = time_msg.content.strip()

        # Regex para validar HH:MM de 00:00 até 23:59
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


# Comando para listar as campanhas
@commands.command(name='listarcampanhas')
async def listar_campanhas(ctx):
    if not campanhas:
        await ctx.send("❌ Nenhuma campanha cadastrada.")
        return

    embed = discord.Embed(title="📜 Lista de Campanhas", color=discord.Color.blue())

    for c in campanhas:
        desc = f"🎮 Jogo: **{c.game}**\n📅 Dia: **{c.week_day.capitalize()}**\n⏰ Horário: **{c.time}**\n👥 Jogadores: **{len(c.players)}**"
        embed.add_field(name=f"🔹 {c.displayName} (ID: {c.id})", value=desc, inline=False)

    await ctx.send(embed=embed)


@commands.command(name='deletarcampanha')
@has_role()
async def deletar_campanha(ctx):
    if not campanhas:
        await ctx.send("❌ Não há campanhas cadastradas para deletar.")
        return

    # Mostra a lista de campanhas disponíveis
    resposta = "**📜 Lista de Campanhas:**\n"
    for campanha in campanhas:
        resposta += f"🆔 {campanha.id}: {campanha.displayName} ({campanha.game})\n"

    resposta += "\nDigite o **ID** da campanha que deseja deletar:"
    await ctx.send(resposta)

    # Espera o usuário responder
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        msg = await ctx.bot.wait_for('message', check=check, timeout=60.0)
        campanha_id = int(msg.content)

        # Procura pela campanha com o ID informado
        campanha_para_deletar = next((c for c in campanhas if c.id == campanha_id), None)

        if campanha_para_deletar:
            campanhas.remove(campanha_para_deletar)
            salvar_campanhas(campanhas)
            await ctx.send(f"✅ Campanha **{campanha_para_deletar.displayName}** deletada com sucesso!")
        else:
            await ctx.send("⚠️ Campanha com esse ID não foi encontrada.")
    except ValueError:
        await ctx.send("❌ ID inválido. Por favor, digite um número.")
    except TimeoutError:
        await ctx.send("⌛ Tempo esgotado! Tente novamente.")

@commands.command(name='editarcampanha')
@has_role()
async def editar_campanha(ctx):
    if not campanhas:
        await ctx.send("❌ Não há campanhas cadastradas para editar.")
        return

    # Mostra a lista de campanhas
    resposta = "**📜 Lista de Campanhas:**\n"
    for campanha in campanhas:
        resposta += f"🆔 {campanha.id}: {campanha.displayName} ({campanha.game})\n"

    resposta += "\nDigite o **ID** da campanha que deseja editar:"
    await ctx.send(resposta)

    # Espera o ID da campanha
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        msg = await ctx.bot.wait_for('message', check=check, timeout=60.0)
        campanha_id = int(msg.content)

        campanha = next((c for c in campanhas if c.id == campanha_id), None)

        if not campanha:
            await ctx.send("⚠️ Campanha com esse ID não foi encontrada.")
            return

        await ctx.send(f"✏️ Editando campanha **{campanha.displayName}**.")
        
        continuar_editando = True
        while continuar_editando:
            # Pergunta o que o usuário quer editar
            await ctx.send("O que deseja editar? Escolha uma opção:\n"
                           "1️⃣ Nome da Campanha\n"
                           "2️⃣ Jogo\n"
                           "3️⃣ Dia da Semana\n"
                           "4️⃣ Horário\n"
                           "Digite o número da opção:")

            opcao_msg = await ctx.bot.wait_for('message', check=check, timeout=60.0)
            opcao = opcao_msg.content.strip()

            if opcao == '1':
                await ctx.send("Digite o novo nome da campanha:")
                nome_msg = await ctx.bot.wait_for('message', check=check, timeout=60.0)
                campanha.displayName = nome_msg.content.strip()
                await ctx.send(f"✅ Nome alterado para **{campanha.displayName}**")

            elif opcao == '2':
                game_view = GameView()
                await ctx.send("🎮 Selecione o **jogo** da campanha:", view=game_view)
                await game_view.wait()
                if not game_view.game:
                    await ctx.send("⛔ Você não escolheu um jogo. Comando cancelado.")
                    return
                game = game_view.game

                campanha.game = game
                await ctx.send(f"✅ Jogo alterado para **{campanha.game}**")

            elif opcao == '3':
                week_day_view = WeekDayView()
                await ctx.send("📆 Selecione o **dia da semana** da campanha:", view=week_day_view)
                await week_day_view.wait()
                if not week_day_view.week_day:
                    await ctx.send("⛔ Você não escolheu um dia da semana. Comando cancelado.")
                    return
                week_day = week_day_view.week_day

                campanha.week_day = week_day
                await ctx.send(f"✅ Dia alterado para **{campanha.week_day}**")

            elif opcao == '4':
                await ctx.send("🕒 Digite o **horário** no formato `HH:MM` (ex: 20:30):")
                while True:
                    time_msg = await ctx.bot.wait_for('message', check=check)
                    time_input = time_msg.content.strip()

                    # Regex para validar HH:MM de 00:00 até 23:59
                    if hora_valida(time_input):
                        time = time_input
                        break
                    else:
                        await ctx.send("⛔ Formato inválido! Por favor, use o formato `HH:MM` (ex: 20:30).")
                campanha.time = time
                await ctx.send(f"✅ Horário alterado para **{campanha.time}**")
            else:
                await ctx.send("❌ Opção inválida. Tente novamente.")

            # Pergunta se o usuário quer editar mais alguma coisa
            await ctx.send("Deseja editar mais alguma coisa nesta campanha? (sim/não):")
            continuar_msg = await ctx.bot.wait_for('message', check=check, timeout=60.0)
            resposta_continuar = continuar_msg.content.strip().lower()

            if resposta_continuar not in ['sim', 's']:
                continuar_editando = False

        # Salva as alterações após encerrar a edição
        salvar_campanhas(campanhas)
        await ctx.send("✅ Todas as alterações foram salvas com sucesso!")

    except ValueError:
        await ctx.send("❌ ID inválido. Por favor, digite um número.")
    except TimeoutError:
        await ctx.send("⌛ Tempo esgotado! Tente novamente.")

@commands.command(name='adicionarplayer')
@has_role()
async def adicionar_player(ctx):
    if not campanhas:
        await ctx.send("❌ Não há campanhas cadastradas para adicionar players.")
        return

    # Lista as campanhas disponíveis
    resposta = "**📜 Lista de Campanhas:**\n"
    for campanha in campanhas:
        resposta += f"🆔 {campanha.id}: {campanha.displayName} ({campanha.game})\n"

    resposta += "\nDigite o **ID** da campanha para adicionar um player:"
    await ctx.send(resposta)

    # Espera a resposta do ID
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        msg_id = await ctx.bot.wait_for('message', check=check, timeout=60.0)
        campanha_id = int(msg_id.content)

        campanha = next((c for c in campanhas if c.id == campanha_id), None)

        if not campanha:
            await ctx.send("⚠️ Campanha com esse ID não foi encontrada.")
            return

        # Pergunta quem é o player (mencionando o user)
        await ctx.send("Mencione o usuário que deseja adicionar à campanha:")
        msg_user = await ctx.bot.wait_for('message', check=check, timeout=60.0)

        if not msg_user.mentions:
            await ctx.send("❌ Você precisa mencionar um usuário!")
            return

        member = msg_user.mentions[0]
        username = member.name

        # Verifica se o player já existe
        player = next((p for p in players if p.username == username), None)
        if not player:
            player = Player(username=username)
            players.append(player)
            await ctx.send(f"✅ Jogador **{username}** foi registrado no sistema.")

        # Verifica se já está na campanha
        campanha_players = [p['user'] for p in campanha.players]
        ja_participa = any(mc.user == username for mc in campanha_players)
        if ja_participa:
            await ctx.send(f"⚠️ O jogador **{username}** já está participando dessa campanha.")
            return

        # Pergunta o país do jogador
        await ctx.send(f"Qual país **{username}** vai jogar na campanha **{campanha.displayName}**?")
        msg_country = await ctx.bot.wait_for('message', check=check, timeout=60.0)
        country = msg_country.content.strip()

        # Cria o membro e adiciona
        membro = MembroCampanha(campanha_id=campanha_id, user=username, country=country)
        campanha.players.append(membro)
        player.campanhas.append(campanha_id)

        salvar_campanhas(campanhas)
        salvar_players(players)

        await ctx.send(f"✅ O jogador **{username}** foi adicionado à campanha **{campanha.displayName}** controlando **{country}**!")

    except ValueError:
        await ctx.send("❌ ID inválido. Digite um número válido.")
    except TimeoutError:
        await ctx.send("⌛ Tempo esgotado! Tente novamente.")

@commands.command(name="analisar_campanha")
async def analisar_campanha(ctx):
    if not campanhas:
        await ctx.send("❌ Não há campanhas disponíveis.")
        return

    # Lista as campanhas disponíveis
    resposta = "**📜 Campanhas Disponíveis:**\n"
    for campanha in campanhas:
        resposta += f"🆔 {campanha.id}: {campanha.displayName} ({campanha.game})\n"
    
    resposta += "\nDigite o **ID** da campanha que deseja analisar:"
    await ctx.send(resposta)

    # Aguarda resposta do ID
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        msg_id = await ctx.bot.wait_for('message', check=check, timeout=60.0)
        campanha_id = int(msg_id.content)

        campanha = next((c for c in campanhas if c.id == campanha_id), None)
        if not campanha:
            await ctx.send("⚠️ Campanha não encontrada. Digite um ID válido.")
            return

        # Detalhes da campanha
        detalhes = (
            f"📌 **Campanha:** {campanha.displayName}\n"
            f"🎮 **Jogo:** {campanha.game}\n"
            f"📅 **Dia:** {campanha.week_day}\n"
            f"⏰ **Horário:** {campanha.time}\n\n"
        )

        # Listando jogadores
        if not campanha.players:
            detalhes += "🚫 **Nenhum jogador cadastrado nesta campanha.**"
        else:
            detalhes += "**👥 Jogadores:**\n"
            for membro in campanha.players:
                membro = MembroCampanha.create(membro)
                presencas = len(membro.presenca)  # Conta quantas presenças ele teve
                detalhes += f"- 👤 **{membro.country}** | **{membro.user}** | 📌 Presenças: {presencas}\n"

        await ctx.send(detalhes)

    except ValueError:
        await ctx.send("❌ ID inválido. Digite um número válido.")
    except TimeoutError:
        await ctx.send("⌛ Tempo esgotado! Tente novamente.")
# Função auxiliar para gerar um ID único para cada campanha
def gerar_id_campanha():
    if not campanhas:
        return 1
    return max(c.id for c in campanhas) + 1
