import asyncio


class Balance(object):
    def __init__(self, initial_balance):
        self.balance = initial_balance
        self.auto_state = False

    def modifier(self, amount_out):
        return self.balance - amount_out > 0

    def transaction_in(self, amount_in: int) -> bool:
        assert amount_in > 0
        self.balance += amount_in
        return self.balance

    def transaction_out(self, amount_out: int) -> bool:
        assert amount_out > 0
        self.balance -= amount_out
        return self.balance

    def auto_increment(self, amount_in: int):
        self.balance += amount_in
