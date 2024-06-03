import datetime
from threading import Timer

from game_data.interface.energy import Energy, Boost, time_until_end_of_day


class TapSpecialBoost(object):
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


class MultiTap(Boost):
    def __init__(self):
        super().__init__()
        self.name = "Multi-Tap"
        self.description = "Multi-Tap boost"
        self.upgrade_rate = [200, 400, 1000, 2000, 4000, 10000, 20000]


class TapGuru(TapSpecialBoost):
    def __init__(self, today_use: int = 0):
        super().__init__(today_use=today_use)
        self.name = "TapGuru"
        self.description = "TapGuru"


class AutoBot(TapSpecialBoost):
    def __init__(self):
        super().__init__(interval=0)
        self.name = "TapGuru"
        self.description = "TapGuru"
        self.state = False

    def is_activated(self) -> bool:
        return self.state

    def price(self):
        if self.is_activated():
            return 0
        else:
            return 200_000

    def activate(self):
        if not self.is_activated():
            self.state = True
            return True
        else:
            return False


class Token(object):
    balance: int
    total_mined: int
    total_click: int
    multi_tap: MultiTap
    energy: Energy
    tap_guru: TapGuru
    auto_bot: AutoBot
    last_click: datetime.datetime

    def __init__(self, balance: int, total_mined: int, total_click: int, multi_tap: MultiTap, energy=Energy(),
                 tap_guru=TapGuru(), auto_bot=AutoBot()):
        self.balance = balance
        self.total_mined = total_mined
        self.total_click = total_click
        self.multi_tap = multi_tap
        self.energy = energy
        self.tap_guru = tap_guru
        self.auto_bot = auto_bot

    def multiplier_balance(self):
        if self.tap_guru:
            return 5
        return 1

    def multiplier_energy(self):
        if self.tap_guru:
            return 0
        return 1

    def balance_up(self, amount: int):
        self.balance += amount
        return True

    def balance_down(self, amount: int) -> bool:
        if self.balance >= amount:
            self.balance -= amount
            return True
        return False

    def mine_up(self, amount: int):
        self.total_mined += amount
        return True

    def click_up(self):
        self.total_click += 1
        return True

    def tap(self):
        self.last_click = datetime.datetime.now(datetime.UTC)
        amount = self.multi_tap.current_level
        mul_en = self.multiplier_energy()
        if self.energy.energy_down(amount * mul_en):
            mul_ba = self.multiplier_balance()
            self.mine_up(amount * mul_ba)
            self.balance_up(amount * mul_ba)
            self.click_up()
            return True
        return False

    def activate_bot(self):
        if self.balance >= self.auto_bot.price():
            self.balance -= self.auto_bot.price()
            self.auto_bot.activate()
            state = self.increase_bot_tap()
            return state
        return False

    def increase_bot_tap(self):
        if self.auto_bot.is_activated() and self.energy.energy == self.energy.limit_boost.max_energy():
            self.balance_up(self.energy.speed_boost.current_level)
            Timer(1, self.increase_bot_tap)
            return True
        return False

    def upgrade_multi_tap(self):
        price = Token.price_up(self.multi_tap)
        if self.balance >= price and price:
            self.balance_down(price)
            self.multi_tap.upgrade()
            return True
        return False

    @staticmethod
    def price_up(instance):
        return instance.upgrade_price()

    def upgrade_energy_limit(self):
        price = Token.price_up(self.energy.limit_boost)
        if self.balance >= price and price:
            self.balance_down(price)
            self.energy.limit_boost.upgrade()
            return True
        return False

    def upgrade_energy_speed(self):
        price = Token.price_up(self.energy.speed_boost)
        if self.balance >= price and price:
            self.balance_down(price)
            self.energy.speed_boost.upgrade()
            return True
        return False

    def activate_tap_guru(self):
        state = self.tap_guru.activate()
        return state

    def activate_energy_refill(self):
        state = self.energy.refill_boost.activate()
        return state
