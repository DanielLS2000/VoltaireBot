class MembroCampanha():
    def __init__(self, campanha_id: int, user: str, country: str, presenca=[]):
        self.campanha_id = campanha_id
        self.user = user
        self.country = country
        self.presenca = presenca

    def to_dict(self):
        return {
            'campanha_id': self.campanha_id,
            'user': self.user,
            'country': self.country,
            'presenca': self.presenca
        }
    
    @classmethod
    def create(cls, membro):
        return cls(
            campanha_id=membro["campanha_id"],
            user=membro["user"],
            country=membro["country"],
            presenca=membro["presenca"]
        )
