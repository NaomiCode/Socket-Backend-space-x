from datetime import datetime, UTC, timedelta, time
from threading import Timer


class Boost(object):
    name: str
    description: str
    upgrade_rate: list[int]
    current_level: int

    def __init__(self, current_level=1):
        self.current_level = current_level

    def upgrade_price(self):
        try:
            return self.upgrade_rate[self.current_level]
        except IndexError:
            return 0

    def upgrade(self):
        if self.upgrade_price() != 0:
            self.current_level += 1
            return True
        else:
            return False


def time_until_end_of_day():
    # type: () -> float
    """
    Get timedelta until end of day on the datetime passed, or current time.
    """
    dt = datetime.now()
    tomorrow = dt + timedelta(days=1)
    return (datetime.combine(tomorrow, time.min) - dt).total_seconds()


class SpecialBoost(object):
    name: str
    description: str
    daily_max_use: 3
    today_use: int
    next_update: float

    def __init__(self, today_use: int):
        """
        Initialize energy special boost.

        :param today_use: How many times users used this boost today



        """
        self.today_use = today_use
        self.next_update = time_until_end_of_day()
        Timer(self.next_update, self.update_daily_use).start()

    def update_daily_use(self):
        """
        a worker to update daily boost with current boost.
        :return:
        """
        self.next_update = time_until_end_of_day()
        self.today_use = 0
        Timer(self.next_update, self.update_daily_use).start()

    def activate(self) -> bool:
        """
        Activate boost.
        :return: True if boost activated
        """
        if self.daily_max_use > self.today_use:
            self.today_use += 1
            return True
        else:
            return False


class EnergySpeedBoost(Boost):
    def __init__(self, current_level=1):
        """
        Initialize energy speed boost.
        :param current_level: user level from database (empty means level 1)

        """
        super().__init__(current_level)
        self.name = 'Energy Limit'
        self.description = 'Energy speed boost'
        self.upgrade_rate = [200, 2_000, 7_000, 25_000, 150_000, 600_000, 3000000, 15_000_000]


class EnergyLimitBoost(Boost):
    def __init__(self, current_level=1):
        """
        Initialize energy limit boost.
        :param current_level: user level from database (empty means level 1)
        """
        super().__init__(current_level)
        self.name = 'Energy Limit'
        self.description = 'Energy limit boost'
        self.upgrade_rate = [200, 2_000, 7_000, 25_000, 150_000, 600_000, 3000000, 15_000_000]

    def max_energy(self) -> int:
        """
        Get the maximum energy level.
        :return: maximum energy amount at current level
        """
        return self.current_level * 500


class EnergyRefillBoost(SpecialBoost):
    def __init__(self, today_use=0):
        """
        Initialize energy refill special boost.
        :param today_use: How many times users used this boost today
        """
        super().__init__(today_use)
        self.name = 'Energy Refill'
        self.description = 'Energy refill boost'


class Energy(object):
    limit_boost: EnergyLimitBoost
    refill_boost: EnergyRefillBoost
    speed_boost: EnergySpeedBoost
    energy: int
    interval_status: bool
    updater: Timer
    freeze: bool = False

    def __init__(self, energy: int = 500, limit_boost=EnergyLimitBoost(), speed_boost=EnergySpeedBoost(),
                 energy_refill_boost=EnergyRefillBoost()):
        """
        Initialize energy instance for a user
        :param energy: current energy to assign for user
        :param limit_boost: limit boost for this user
        :param speed_boost: speed boost for this user
        :param energy_refill_boost: refill boost for this user
        """
        self.limit_boost = limit_boost
        self.refill_boost = energy_refill_boost
        self.speed_boost = speed_boost
        self.energy = energy
        self.energy_interval()

    def activate_refill(self) -> bool:
        """
        activate refill boost for this user
        :return: returns true if activated with no error
        """
        if self.refill_boost.activate():
            self.energy = self.limit_boost.max_energy()
            return True
        else:
            return False

    def energy_down(self, amount: int) -> bool:
        """
        used to subtract a value from energy
        :param amount: value to be subtracted from energy
        :return:  a boolean indicating TRue when success
        """
        if self.freeze:
            return True
        if self.energy < amount:
            return False
        self.energy -= amount
        return True

    def energy_up(self, amount: int) -> bool:
        """
        used to add a value to energy
        :param amount: value to be subtracted to energy
        :return: a boolean indicating TRue when success 
        """
        if self.freeze:
            return True
        if self.energy + amount <= self.limit_boost.max_energy():
            self.energy += amount
        else:
            self.energy = self.limit_boost.max_energy()
        return True

    def upgrade_energy_limit(self) -> bool:
        """
        upgrade limit boost
        :return: a boolean indicating TRue when success
        """
        return self.limit_boost.upgrade()

    def upgrade_energy_speed(self) -> bool:
        """
        upgrade speed boost
        :return: a boolean indicating TRue when success
        """
        return self.speed_boost.upgrade()

    def energy_interval(self):
        """
        enable energy refill interval every second
        """
        if self.energy != self.limit_boost.max_energy():
            self.energy_up(self.speed_boost.current_level)
        Timer(1, self.energy_interval).start()

    def freeze_energy_use(self, interval):
        """
        freeze use of energy for how many seconds
        :param interval: How many seconds to freeze energy
        :return: None
        """
        self.freeze = True
        Timer(interval, self.unfreeze_energy_use).start()

    def unfreeze_energy_use(self):
        """
        unfreeze use of energy
        :return: None
        """
        self.freeze = False
