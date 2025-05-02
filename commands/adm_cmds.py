from discord.ext import commands
from models.campanha import campanhas
from models.player import players
from utils.utils import gerar_info, has_role, salvar_campanhas, salvar_players, admin_only
import json
import asyncio

@admin_only()
async def atualizar_info_jogos(ctx, campanhas):
    canal = ctx.channel
    mensagens = [msg async for msg in canal.history(limit=10)]
    
    # Busca uma mensagem antiga do bot (agora com content, não mais embed)
    mensagem_antiga = next(
        (msg for msg in mensagens if msg.author == ctx.bot.user and not msg.embeds), None
    )

    conteudo = gerar_info(campanhas, ctx.guild)

    if mensagem_antiga:
        await mensagem_antiga.edit(content=conteudo)
        confirm = await canal.send("✅ Mensagem de campanhas **atualizada**.")
    else:
        await canal.send(content=conteudo)
        confirm = await canal.send("✅ Mensagem de campanhas **enviada**.")

    await asyncio.sleep(5)
    await ctx.message.delete()
    await confirm.delete()



@commands.command(name="atualizar_info", aliases=["attInfo", "atualizarInfoCampanhas"])
@admin_only()
async def atualizar_info(ctx):
    """Comando para atualizar as informações das campanhas no servidor atual."""
    await atualizar_info_jogos(ctx, campanhas)



@commands.command(name="reset_db")
@admin_only()
async def reset_db(ctx):
    await ctx.send("Limpando as informações do server.")
    
    campanhas = []
    salvar_campanhas(campanhas)
    await ctx.send("Informação das campanhas deletas.")
    
    players = []
    salvar_players(players)
    await ctx.send("Informação dos players deletas.")

@commands.command(name="marcar_presenca_adm", aliases=["presenca", "mp", "registrarPresenca"])
@has_role()
async def marcar_presenca_adm(ctx):
    # Se não houver campanhas, avisa e sai
    if not campanhas:
        await ctx.send("🚫 Nenhuma campanha registrada no momento.")
        return

    # Exibe campanhas disponíveis com ID
    msg_lista = "**📋 Campanhas disponíveis:**\n"
    for campanha in campanhas:
        msg_lista += f"🆔 {campanha.id}: {campanha.displayName} ({campanha.game})\n"
    await ctx.send(msg_lista)
    await ctx.send("✍️ Envie o **ID** da campanha para marcar presença:")

    def check_id(m):
        return m.author == ctx.author and m.channel == ctx.channel and m.content.isdigit()

    try:
        msg_id = await ctx.bot.wait_for('message', check=check_id, timeout=60.0)
        campanha_id = int(msg_id.content)

        campanha = next((c for c in campanhas if c.id == campanha_id), None)
        if not campanha:
            await ctx.send("⚠️ Campanha não encontrada. Digite um ID válido.")
            return

        if not campanha.players:
            await ctx.send("❌ Esta campanha não possui jogadores registrados.")
            return

        # Mostra os jogadores da campanha
        nomes_jogadores = [m.user for m in campanha.players]
        nomes_formatados = "\n".join([f"- {nome}" for nome in nomes_jogadores])
        await ctx.send(f"👥 Jogadores da campanha **{campanha.displayName}**:\n{nomes_formatados}")
        await ctx.send("✍️ Agora, envie os nomes dos **presentes**, separados por vírgula, espaço ou nova linha.")

        def check_presentes(m):
            return m.author == ctx.author and m.channel == ctx.channel

        resposta_presencas = await ctx.bot.wait_for("message", timeout=180, check=check_presentes)
        nomes_presentes = set(x.strip().lower() for x in resposta_presencas.content.replace(",", "\n").split())

        for membro in campanha.players:
            user = membro.user.lower()
            if user in nomes_presentes:
                membro.presenca.append(1)
                player = [player for player in players if user == player.username][0]
                player.addCredito(10)
            else:
                membro.presenca.append(0)
                player = [player for player in players if user == player.username][0]
                player.rmCredito(20)

        salvar_campanhas(campanhas)
        await ctx.send("✅ Presenças registradas com sucesso!")

    except asyncio.TimeoutError:
        await ctx.send("⏰ Tempo esgotado para resposta.")