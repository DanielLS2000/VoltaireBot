import os
import json
from config import ARQUIVO_PLAYERS


class Player():
    def __init__(self, username: str, credito_social=0):
        self.username = username
        self.credito_social = credito_social
        self.campanhas = []

    def to_dict(self):
        return {
            'username': self.username,
            'credito_social': self.credito_social,
            'campanhas': self.campanhas
        }
    

def load_players():
    players = []

    if not os.path.exists(ARQUIVO_PLAYERS):
        print("Nenhum player foi encontrado.")
        return players
    
    with open(ARQUIVO_PLAYERS, 'r', encoding='utf-8') as f:
        try:
            dados = json.load(f)
            for item in dados:
                player = Player(
                    username=item['username'],
                    credito_social=item['credito_social']
                )
                player.campanhas = item.get('campanhas', [])
                players.append(player)
            print(f"{len(players)} players carregados com sucesso.")
            return players
        except json.JSONDecodeError:
            print("Erro ao ler o arquivo de players.")
            return players
        
players = load_players()