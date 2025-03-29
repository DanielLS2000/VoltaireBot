from discord.ext import commands
import discord
from models.campanha import campanhas
from models.player import players

INFO_CHANNEL_NAME = "info-dos-jogos"
info_message_id = None  

async def atualizar_info_jogos(bot):
    """Atualiza ou cria a mensagem fixa no canal de informações das campanhas."""
    global info_message_id

    for guild in bot.guilds:
        info_channel = discord.utils.get(guild.text_channels, name=INFO_CHANNEL_NAME)

        if info_channel is None:
            print(f"❌ Canal '{INFO_CHANNEL_NAME}' não encontrado!")
            return

        if not campanhas:
            info_text = "🚫 **Nenhuma campanha ativa no momento.**"
        else:
            info_text = ""
            for campanha in campanhas:
                organizador = campanha.players[0] if campanha.players else "Desconhecido"
                info_text += f"## {campanha.displayName}, todos os {campanha.week_day} às {campanha.time}\n"
                info_text += f"Organizador: @{organizador}\n\n"

                if campanha.players:
                    info_text += f"**{len(campanha.players)} Players:**\n"
                    for membro in campanha.players:
                        membro_campanha = next((m for m in players if m.username == membro), None)
                        if membro_campanha:
                            country = next((c.country for c in membro_campanha.campanhas if c.campanha_id == campanha.id), "Desconhecido")
                            info_text += f"@{membro} - {country}\n"
                    info_text += "\n"

        async for message in info_channel.history(limit=50):
            if message.author == bot.user:
                info_message_id = message.id
                break

        if info_message_id:
            msg = await info_channel.fetch_message(info_message_id)
            await msg.edit(content=info_text)
        else:
            msg = await info_channel.send(info_text)
            info_message_id = msg.id 

@commands.command(name="atualizar_info")
@commands.has_permissions(administrator=True)
async def atualizar_info(ctx):
    """Comando para atualizar as informações das campanhas."""
    await atualizar_info_jogos(ctx.bot)
    await ctx.send("✅ Informações das campanhas foram atualizadas!")
