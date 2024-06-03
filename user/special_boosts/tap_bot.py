from user.special_boost import SpecialBoost


class AutoBot(SpecialBoost):
    def __init__(self,state=False):
        super().__init__(interval=0)
        self.name = "TapBot"
        self.description = "TapBot"
        self.state = state

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
