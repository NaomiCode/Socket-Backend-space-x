from user.special_boost import SpecialBoost


class EnergyRefillBoost(SpecialBoost):
    def __init__(self, today_use=0):
        """
        Initialize energy refill special boost.
        :param today_use: How many times users used this boost today
        """
        super().__init__(today_use)
        self.name = 'Energy Refill'
        self.description = 'Energy refill boost'
        self.interval = 0
