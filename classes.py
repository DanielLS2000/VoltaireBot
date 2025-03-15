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
            'players': self.players
        }

class Player():
    def __init__(self, username: str):
        self.username = username
        self.credito_social = 0
        self.campanhas = []

    def to_dict(self):
        return {
            'username': self.username,
            'credito_social': self.credito_social,
            'campanhas': self.campanhas
        }

class MembroCampanha():
    def __init__(self, campanha_id: int, user: str, country: str):
        self.campanha_id = campanha_id
        self.user = user
        self.country = country
        self.presenca = []

    def to_dict(self):
        return {
            'campanha_id': self.campanha_id,
            'user': self.user,
            'country': self.country,
            'presenca': self.presenca
        }
