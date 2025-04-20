from discord.ext import commands
from models.campanha import campanhas
from models.player import players, Player
from models.membro_campanha import MembroCampanha
from utils.utils import salvar_campanhas, salvar_players, admin_only, get_country_tag, can_pick_country

@commands.command(name="entrar_campanha", aliases=["join", "joinCampanha", "entrarCampanha", "entrar"])
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
        campanha_players = [p.user for p in campanha.players]
        ja_participa = username in campanha_players
        if ja_participa:
            await ctx.send(f"⚠️ Você já está participando da campanha **{campanha.displayName}**.")
            return

        # Pergunta o país
        await ctx.send(f"🌍 Qual país você vai jogar na campanha **{campanha.displayName}**?")
        msg_country = await ctx.bot.wait_for('message', check=check, timeout=60.0)
        country = msg_country.content.strip()

        # Verifica se o jogador tem credito o suficiente para pegar o país
        country_tag = get_country_tag(country)
        if not can_pick_country(player.credito_social, country_tag):
            await ctx.send(f"Erro: o Jogador não possui credito o suficiente para pegar a tag {country_tag}.\nVocê possui apenas {player.credito_social} creditos.")
            return

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


@commands.command(name="meu_perfil", aliases=["myProfile", "meuPerfil"])
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
            country = [p.country for p in c.players if p.user == player.username][0]
            resposta += f"- 🧭 {c.displayName} | 🌍 País: {country}\n"

    await ctx.send(resposta)


@commands.command(name="perfil", aliases=["verPerfil"])
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
            country = [p.country for p in c.players if p.user == player.username][0]
            resposta += f"- 🧭 {c.displayName} | 🌍 País: {country}\n"

    await ctx.send(resposta)
