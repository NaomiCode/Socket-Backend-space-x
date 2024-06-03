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
