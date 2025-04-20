from discord.ext import commands
from models.player import players
from utils.utils import admin_only, salvar_players

@commands.command(name="addCredito", aliases=["add_credito", "adicionarCredito"])
@admin_only()
async def add_credito(ctx):
    await ctx.send("📌 Qual o nome do jogador que deve receber crédito?")

    def check_user(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        user_msg = await ctx.bot.wait_for("message", timeout=60.0, check=check_user)
        if not user_msg.mentions:
            await ctx.send("❌ Você precisa mencionar um usuário!")
            return

        member = user_msg.mentions[0]
        username = member.name

        player = next((p for p in players if p.username == username.lower()), None)

        if not player:
            await ctx.send("❌ Jogador não encontrado!")
            return

        await ctx.send(f"💰 Quantos créditos deseja adicionar para **{username}**?")

        def check_value(m):
            return m.author == ctx.author and m.channel == ctx.channel

        value_msg = await ctx.bot.wait_for("message", timeout=60.0, check=check_value)
        try:
            credito = int(value_msg.content.strip())
            if credito <= 0:
                raise ValueError

            player.addCredito(credito)
            salvar_players(players)
            await ctx.send(f"✅ Créditos adicionados! {username} agora tem **{player.credito_social}** créditos sociais.")

        except ValueError:
            await ctx.send("❌ Valor inválido. Digite um número inteiro positivo.")
    except TimeoutError:
        await ctx.send("⌛ Tempo esgotado. Tente novamente.")

@commands.command(name="rmCredito", aliases=["rm_credito", "removerCredito"])
@admin_only()
async def rm_credito(ctx):
    await ctx.send("📌 Qual o nome do jogador que deve perder crédito?")

    def check_user(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        user_msg = await ctx.bot.wait_for("message", timeout=60.0, check=check_user)
        if not user_msg.mentions:
            await ctx.send("❌ Você precisa mencionar um usuário!")
            return

        member = user_msg.mentions[0]
        username = member.name

        player = next((p for p in players if p.username == username.lower()), None)

        if not player:
            await ctx.send("❌ Jogador não encontrado!")
            return

        await ctx.send(f"💰 Quantos créditos deseja remover para **{username}**?")

        def check_value(m):
            return m.author == ctx.author and m.channel == ctx.channel

        value_msg = await ctx.bot.wait_for("message", timeout=60.0, check=check_value)
        try:
            credito = int(value_msg.content.strip())
            if credito <= 0:
                raise ValueError

            player.rmCredito(credito)
            salvar_players(players)
            await ctx.send(f"✅ Créditos removidos! {username} agora tem **{player.credito_social}** créditos sociais.")

        except ValueError:
            await ctx.send("❌ Valor inválido. Digite um número inteiro positivo.")
    except TimeoutError:
        await ctx.send("⌛ Tempo esgotado. Tente novamente.")
