from user.boost import Boost

class EnergySpeedBoost(Boost):
    def __init__(self, current_level=1):
        """
        Initialize energy speed boost.
        :param current_level: user level from database (empty means level 1)

        """
        super().__init__(current_level)
        self.name = 'Energy speed'
        self.description = 'Energy speed boost'
        self.upgrade_rate = [200, 2_000, 7_000, 25_000, 150_000, 600_000, 3000000, 15_000_000]
