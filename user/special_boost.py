from user.util.end_day_time import time_until_end_of_day
from threading import Timer


class SpecialBoost(object):
    name: str
    description: str
    daily_max_use: int
    today_use: int
    next_update: float
    state: bool

    def __init__(self, today_use: int = 0, interval: int = 20, max_use=3):
        """
        Initialize energy special boost.

        :param today_use: How many times users used this boost today



        """
        self.interval = interval
        self.today_use = today_use
        self.next_update = time_until_end_of_day()
        self.daily_max_use = max_use
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
            self.state = True
            if self.interval:
                Timer(self.interval, self.deactivate).start()
            return True
        else:
            return False

    def deactivate(self):
        self.state = False
