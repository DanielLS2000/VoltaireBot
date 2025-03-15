import discord

class GameSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="CK3", description="Crusader Kings III"),
            discord.SelectOption(label="EU4", description="Europa Universalis IV"),
            # discord.SelectOption(label="EU5", description="Europa Universalis V"),
            discord.SelectOption(label="VIC2", description="Victoria II"),
            discord.SelectOption(label="VIC3", description="Victoria 3"),
            discord.SelectOption(label="HOI4", description="Hearts of Iron IV"),
        ]
        super().__init__(placeholder="Escolha o jogo...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        self.view.game = self.values[0]
        await interaction.response.send_message(f"🎮 Você escolheu **{self.values[0]}**", ephemeral=True)
        self.view.stop()

class GameView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.game = None
        self.add_item(GameSelect())


class WeekDaySelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Domingo"),
            discord.SelectOption(label="Segunda"),
            discord.SelectOption(label="Terça"),
            discord.SelectOption(label="Quarta"),
            discord.SelectOption(label="Quinta"),
            discord.SelectOption(label="Sexta"),
            discord.SelectOption(label="Sabado")
        ]
        super().__init__(placeholder="Escolha o dia da semana...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        self.view.week_day = self.values[0]
        await interaction.response.send_message(f"📅 Você escolheu **{self.values[0]}**", ephemeral=True)
        self.view.stop()

class WeekDayView(discord.ui.View):
    def __init__(self):
        super().__init__()
        self.week_day = None
        self.add_item(WeekDaySelect())