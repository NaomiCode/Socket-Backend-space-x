class Energy(object):
    speed: int
    limit: int
    state: bool

    def __init__(self, initial_energy: int, initial_limit: int, initial_speed: int):
        self.state = True
        self.energy = initial_energy
        self.limit = initial_limit
        self.speed = initial_speed

    def set_speed(self, speed: int):
        self.speed = speed
        return True

    def set_limit(self, limit: int):
        self.limit = limit
        return True

    def energy_modifier(self, amount_out: int = None, amount_in: int = None):
        if amount_out:
            if amount_out >= 0:
                return self.energy - amount_out >= 0
        elif amount_in:
            if amount_in + self.energy >= self.limit * 500:
                return self.limit * 500
            else:
                return self.energy + amount_in >= 0

    def transaction_out(self, amount_out: int):
        if self.energy_modifier(amount_out=amount_out):
            self.energy -= amount_out
            return True
        return False

    def transaction_in(self, amount_in: int):
        if self.energy_modifier(amount_in=amount_in) == self.limit * 500:
            self.energy = self.limit * 500
        elif self.energy_modifier(amount_in=amount_in) and amount_in + self.energy <= self.limit * 500:
            self.energy += amount_in
        else:
            self.energy += amount_in
        return True

    def refill(self):
        self.energy = self.limit * 500
        return True

    def auto_increment(self):
        self.transaction_in(self.speed)
