import os
import json
from config import ARQUIVO_CAMPANHAS
from models.membro_campanha import MembroCampanha

class Campanha():
    def __init__(self, id: int, displayName: str, game: str, time: str, week_day: str):
        self.id = id
        self.displayName = displayName
        self.game = game
        self.time = time
        self.week_day = week_day
        self.players = []

    def to_dict(self):
        return {
            'id': self.id,
            'displayName': self.displayName,
            'game': self.game,
            'time': self.time,
            'week_day': self.week_day,
            'players': [player.to_dict() for player in self.players if player is not None]
        }
    
    def __str__(self):
        return f"Campanha de {self.game}: {self.displayName}"


def load_campanhas():
    campanhas = []

    if not os.path.exists(ARQUIVO_CAMPANHAS):
        print("Nenhuma campanha salva encontrada.")
        campanhas = []
        return campanhas
    
    with open(ARQUIVO_CAMPANHAS, 'r', encoding='utf-8') as f:
        try:
            dados = json.load(f)
            campanhas = []
            for item in dados:
                campanha = Campanha(
                    id=item['id'],
                    displayName=item['displayName'],
                    game=item['game'],
                    time=item['time'],
                    week_day=item['week_day']
                )
                lista_players = item.get('players', [])
                lista_players = [MembroCampanha.create(player) for player in lista_players]
                campanha.players = lista_players
                campanhas.append(campanha)
            print(f"{len(campanhas)} campanhas carregadas com sucesso.")
            return campanhas
        except json.JSONDecodeError:
            print("Erro ao ler o arquivo de campanhas.")
            campanhas = []
            return campanhas

campanhas = load_campanhas()