from user.special_boost import SpecialBoost


class TapGuru(SpecialBoost):
    def __init__(self, today_use: int = 0):
        super().__init__(today_use=today_use)
        self.name = "TapGuru"
        self.description = "TapGuru"
        self.state = False
