LEAGUES = [("Wooden League", 0, 0), ("Metal League", 10000, 10), ("Bronze League", 10000, 50),
           ("Silver League", 10000, 400),
           ("Gold League", 100000, 1222), ("Platinum League", 1000000, 1323213), ]


class League(object):
    def __init__(self, current_amount: int, claimed: list[int]) -> None:
        self.claimed = []
        for item in claimed:
            self.claimed.append(LEAGUES.index(item))
        self.amount = current_amount
        for item in range(len(LEAGUES)):
            if LEAGUES[item][1] <= self.amount:
                try:
                    if self.amount <= LEAGUES[item + 1][1]:
                        self.league = LEAGUES[item]
                        break
                except:
                    self.league = LEAGUES[-1]
                    break

        self.unclaimed = list(set(LEAGUES) - set(claimed))

    def claim_reward(self, league: int) -> (int, bool):
        if LEAGUES.index(self.league) < league and LEAGUES[league] not in self.claimed:
            self.claimed.append(LEAGUES[league])
            return LEAGUES[league][2], True
        return 0, False

    def add_amount(self, amount: int):
        self.amount += amount

    def get_claimable(self) -> list[tuple[str, int, int]]:
        claimable = []
        for league in LEAGUES:
            if league not in self.claimed and league[1] < self.league[1]:
                claimable.append(league)
        return claimable

    def get_not_claimable(self) -> list[tuple[str, int, int]]:
        return list(set(a.unclaimed) - set(a.get_claimable()))


a = League(current_amount=200000, claimed=[("Wooden League", 0, 0)])

