from discord.ext import commands
from models.campanha import campanhas
from models.player import players, Player
from models.membro_campanha import MembroCampanha
from utils.utils import salvar_campanhas, salvar_players, admin_only

@commands.command(name="entrar_campanha")
async def entrar_campanha(ctx):
    if not campanhas:
        await ctx.send("❌ Não há campanhas disponíveis no momento.")
        return

    # Lista as campanhas disponíveis
    resposta = "**📜 Campanhas Disponíveis:**\n"
    for campanha in campanhas:
        resposta += f"🆔 {campanha.id}: {campanha.displayName} ({campanha.game})\n"
    
    resposta += "\nDigite o **ID** da campanha que deseja entrar:"
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

        username = ctx.author.name  # Nome do jogador no Discord

        # Verifica se o jogador já está cadastrado
        player = next((p for p in players if p.username == username), None)
        if not player:
            player = Player(username=username)
            players.append(player)
            await ctx.send(f"✅ Jogador **{username}** registrado no sistema.")

        # Verifica se já está na campanha
        campanha_players = [p['user'] for p in campanha.players]
        ja_participa = any(mc.user == username for mc in campanha_players)
        if ja_participa:
            await ctx.send(f"⚠️ Você já está participando da campanha **{campanha.displayName}**.")
            return

        # Pergunta o país
        await ctx.send(f"🌍 Qual país você vai jogar na campanha **{campanha.displayName}**?")
        msg_country = await ctx.bot.wait_for('message', check=check, timeout=60.0)
        country = msg_country.content.strip()

        # Adiciona o jogador à campanha
        membro = MembroCampanha(campanha_id=campanha_id, user=username, country=country)
        campanha.players.append(membro)
        player.campanhas.append(campanha_id)

        # Salva as mudanças
        salvar_campanhas(campanhas)
        salvar_players(players)

        await ctx.send(f"✅ **{username}** entrou na campanha **{campanha.displayName}** jogando como **{country}**!")

    except ValueError:
        await ctx.send("❌ ID inválido. Digite um número válido.")
    except TimeoutError:
        await ctx.send("⌛ Tempo esgotado! Tente novamente.")


@commands.command(name="meu_perfil")
async def meu_perfil(ctx):
    username = ctx.author.name

    # Busca o jogador na lista de players
    player = next((p for p in players if p.username == username), None)

    if not player:
        await ctx.send("❌ Você ainda não está registrado em nenhuma campanha!")
        return

    # Monta a resposta
    resposta = (
        f"👤 **Perfil de {username.capitalize()}**\n"
        f"💰 **Crédito Social:** {player.credito_social}\n\n"
    )

    if not player.campanhas:
        resposta += "🚫 Você não participa de nenhuma campanha."
    else:
        resposta += "**📜 Campanhas:**\n"
        for campanha in player.campanhas:
            c = [c for c in campanhas if c.id == campanha][0]
            country = [p["country"] for p in c.players if p["user"] == player.username][0]
            resposta += f"- 🧭 {c.displayName} | 🌍 País: {country}\n"

    await ctx.send(resposta)


@commands.command(name="perfil")
@admin_only()
async def perfil(ctx, username: str):
    # Busca o jogador na lista de players
    player = next((p for p in players if p.username.lower() == username.lower()), None)

    if not player:
        await ctx.send(f"❌ O jogador **{username}** não foi encontrado.")
        return

    # Monta a resposta
    resposta = (
        f"👤 **Perfil de {username}**\n"
        f"💰 **Crédito Social:** {player.credito_social}\n\n"
    )

    if not player.campanhas:
        resposta += "🚫 O jogador não participa de nenhuma campanha."
    else:
        resposta += "**📜 Campanhas:**\n"
        for campanha in player.campanhas:
            c = [c for c in campanhas if c.id == campanha][0]
            country = [p["country"] for p in c.players if p["user"] == player.username][0]
            resposta += f"- 🧭 {c.displayName} | 🌍 País: {country}\n"

    await ctx.send(resposta)


@commands.command(name="marcar_presenca")
async def marcar_presenca(ctx):
    if not campanhas:
        await ctx.send("❌ Não há campanhas disponíveis.")
        return

    # Lista as campanhas disponíveis
    resposta = "**📜 Campanhas Disponíveis:**\n"
    for campanha in campanhas:
        resposta += f"🆔 {campanha.id}: {campanha.displayName} ({campanha.game})\n"
    
    resposta += "\nDigite o **ID** da campanha que deseja marcar presença:"
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

        await ctx.send(f"✅ Campanha **{campanha.displayName}** selecionada! Agora mencione os jogadores para marcar presença. Digite **'fim'** para encerrar.")

        # Loop para adicionar presenças
        while True:
            msg_player = await ctx.bot.wait_for('message', check=check, timeout=120.0)
            player_name = msg_player.content.strip()

            if player_name.lower() == "fim":
                break  # Sai do loop

            # Verifica se o jogador está na campanha
            membro = next((m for m in campanha.players if m.user == player_name), None)
            if not membro:
                await ctx.send(f"⚠️ O jogador **{player_name}** não está nesta campanha. Tente outro nome.")
                continue

            # Adiciona presença
            membro.presenca.append(1)
            await ctx.send(f"✅ Presença marcada para **{player_name}**!")

        # Salva mudanças
        salvar_campanhas(campanhas)
        await ctx.send("📌 **Presenças registradas com sucesso!**")

    except ValueError:
        await ctx.send("❌ ID inválido. Digite um número válido.")
    except TimeoutError:
        await ctx.send("⌛ Tempo esgotado! Tente novamente.")
