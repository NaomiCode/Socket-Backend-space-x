from user.boost import Boost


class MultiTap(Boost):
    def __init__(self,current_level=1):
        super().__init__()
        self.name = "Multi-Tap"
        self.description = "Multi-Tap boost"
        self.upgrade_rate = [200, 400, 1000, 2000, 4000, 10000, 20000]
        self.current_level = current_level
