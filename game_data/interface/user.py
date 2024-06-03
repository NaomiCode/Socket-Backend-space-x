from game_data.interface import Token
from game_data.interface.energy import Energy


class User(object):
    def __init__(self, user_id: int, token=Token, energy=Energy()):
        self.id = user_id
        self.energy = energy
        self.token = token


a = User(user_id=1)
