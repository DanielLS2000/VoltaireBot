from discord.ext import commands
import discord
from models.campanha import campanhas
from models.player import players

@commands.command(name="ping")
async def ping(ctx):
    await ctx.send("Pong")

@commands.command(name="help", aliases=["ajuda", "comandos"])
async def help_command(ctx):
    help_text = """
📘 **Comandos Disponíveis**

### 🎲 Campanhas
- `!addCampanha` — Cria uma nova campanha.
- `!listarCampanhas` — Lista todas as campanhas existentes.
- `!analisarCampanha` — Mostra detalhes de uma campanha específica.
- `!editarCampanha` — Edita os dados de uma campanha.
- `!deletarCampanha` — Remove uma campanha existente.

### 👥 Jogadores
- `!joinCampanha` — Entra em uma campanha como jogador.
- `!meuPerfil` — Mostra suas campanhas e seu crédito social.
- `!removePlayer` — Remove um jogador de uma campanha (ADM).
- `!addPlayer` — Adiciona manualmente um player a uma campanha (ADM).
- `!verPerfil` — Mostra o perfil de outro jogador (ADM).

### 🕒 Presença
- `!registrarPresenca ou mp` — Marca a presença de jogadores em uma campanha (ADM).

### 💰 Crédito Social
- `!addCredito` — Adiciona crédito social para um jogador (ADM).

### 📢 Informações Públicas
- `!atualizarInfoCampanhas` — Atualiza o post no canal `#info-dos-jogos` com os dados das campanhas (ADM).

---

🛡️ *Comandos marcados como (ADM) só podem ser usados por administradores ou pessoas com cargos autorizados.*
"""
    await ctx.send(help_text)

