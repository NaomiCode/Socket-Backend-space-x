import time
from typing import TypedDict

import requests

from user.boosts.energy_limit import EnergyLimitBoost
from user.boosts.energy_speed import EnergySpeedBoost
from user.boosts.multi_tap import MultiTap
from user.energy import Energy
from user.balance import Balance
from user.league import League
from user.referral import Referral
from user.special_boosts.guru import TapGuru
from user.special_boosts.refill import EnergyRefillBoost
from user.special_boosts.tap_bot import AutoBot
from user.tasks import Task, UserTask


#
# "/api/store" -> "POST, GET"
# "store"


class UserData(TypedDict):
    user_id: int
    energy: int
    balance: int
    total_amount: int
    total_clicks: int
    last_clicks: int
    limit_level: int
    speed_level: int
    multi_tap_level: int
    auto_bot: bool
    guru_used: int
    refill_used: int
    claimed_tasks: list[Task]
    claimed_leagues: list[int]
    claimed_ref: list[int]
    referrals: list[int]


def update_data(data: UserData):
    resp = requests.post("http://192.168.88.167:8002/api/store",
                         json=data,
                         headers={"Content-Type": "application/json"})
    return resp.json()["message"] == "success"


def get_user_data(user_id: int) -> UserData:
    resp = requests.get("http://192.168.88.167:8002/api/store/{}".format(user_id))
    data = resp.json()
    return UserData(
        user_id=data['user_id'],
        energy=data['energy'],
        balance=data['balance'],
        total_amount=data['total_amount'],
        total_clicks=data['total_clicks'],
        last_clicks=data['last_clicks'],
        limit_level=data['limit_level'],
        speed_level=data['speed_level'],
        multi_tap_level=data['multi_tap_level'],
        auto_bot=data['auto_bot'],
        guru_used=data['guru_used'],
        refill_used=data['refill_used'],
        claimed_tasks=data['claimed_tasks'],
        claimed_leagues=data['claimed_leagues'],
        claimed_ref=data['claimed_ref'],
        referrals=data['referral'],
    )


class User:
    def __init__(self, user_id: int) -> None:
        data = get_user_data(user_id)
        self.user_id: int = user_id
        self.total_clicks = data['total_clicks']
        self.last_clicks = data["last_clicks"]

        self.energy = Energy(data['energy'], data['limit_level'], data['speed_level'])
        self.balance = Balance(data['balance'])

        self.energy_limit = EnergyLimitBoost(current_level=data['limit_level'])
        self.energy_speed = EnergySpeedBoost(current_level=data['speed_level'])
        self.multi_tap = MultiTap(current_level=data['multi_tap_level'])

        self.auto_bot = AutoBot(state=data['auto_bot'])
        self.guru = TapGuru(today_use=data['guru_used'])
        self.refill = EnergyRefillBoost(today_use=data['refill_used'])
        # todo: this is false
        self.league = League(current_amount=data['total_amount'], claimed=data['claimed_leagues'])
        self.referral = Referral(user_id=data['user_id'], claimed=data['claimed_ref'], referrals=data['referrals'])
        self.tasks = UserTask(completed_tasks=data['claimed_tasks'])

    def multiplier_balance_energy(self):
        if self.guru.state:
            return 5, 0
        return 1, 1

    def tap(self):
        balance_mul, energy_mul = self.multiplier_balance_energy()
        if self.energy.transaction_out(self.multi_tap.current_level * energy_mul):
            self.balance.transaction_in(self.multi_tap.current_level * balance_mul)
            self.league.add_amount(self.multi_tap.current_level * balance_mul)
            self.last_clicks = int(time.time() / 1000)
            self.total_clicks += 1
            return True
        return False

    def upgrade_speed(self):
        price = self.energy_speed.upgrade_price()
        if price:
            if self.balance.transaction_out(price):
                self.energy_speed.upgrade()
                self.energy.set_speed(self.energy_speed.value())
                return True
        return False

    def upgrade_limit(self):
        price = self.energy_limit.upgrade_price()
        if price:
            if self.balance.transaction_out(price):
                self.energy_limit.upgrade()
                self.energy.set_limit(self.energy_limit.current_level)
                return True
        return False

    def upgrade_multi_tap(self):
        price = self.multi_tap.upgrade_price()
        if price:
            if self.balance.transaction_out(price):
                self.multi_tap.upgrade()
                return True
        return False

    def activate_bot(self):
        price = self.auto_bot.price()
        if price:
            if self.balance.transaction_out(price):
                self.auto_bot.activate()
                return True

    def activate_refill(self):
        if self.refill.activate():
            self.energy.refill()
            return True
        return False

    def activate_guru(self):
        if self.guru.activate():
            return True
        return False

    def get_ref_link(self):
        return self.referral.referral_link()

    def get_ref_tasks(self):
        claimed_task = self.referral.claimed_referrals
        all_tasks = self.referral.get_reward_tier()
        achieved = self.referral.achieved_referrals()

        return all_tasks, achieved, claimed_task

    def claim_ref_task(self, tier: int):
        reward = self.referral.referral_reward_task_complete(tier)
        if reward:
            self.balance.transaction_in(reward)
            return True
        return False

    def claim_league(self, league_index: int):
        reward, status = self.league.claim_reward(league_index)
        if status:
            self.balance.transaction_in(reward)
            self.league.add_amount(reward)
            return True
        return False

    def claim_task(self, task_id: int):
        if self.tasks.set_completed(task_id):
            self.balance.transaction_in(self.tasks.task_reward(task_id))
            self.league.add_amount(self.tasks.task_reward(task_id))
            return True
        return False

    def get_tasks(self):
        claimed_task = self.tasks.user_completed_tasks
        not_claimed_tasks = list(set(self.tasks.tasks) - set(self.tasks.user_completed_tasks))
        return claimed_task, not_claimed_tasks

    def get_league(self):
        claimed_league = self.league.claimed
        not_claimable_league = self.league.get_not_claimable()
        claimable_league = self.league.get_claimable()
        current_league = self.league.league
        return claimed_league, not_claimable_league, claimable_league, current_league

    def disconnect(self):
        update_data(data=UserData(
            user_id=self.user_id,
            energy=self.energy.energy,
            balance=self.balance.balance,
            total_amount=self.league.amount,
            total_clicks=self.total_clicks,
            last_clicks=self.last_clicks,
            limit_level=self.energy_limit.current_level,
            speed_level=self.energy_speed.current_level,
            multi_tap_level=self.multi_tap.current_level,
            auto_bot=self.auto_bot.is_activated(),
            guru_used=self.guru.today_use,
            refill_used=self.refill.today_use,
            claimed_tasks=self.tasks.completed_tasks(),
            claimed_leagues=self.league.claimed,
            claimed_ref=self.referral.get_claimed_referrals_index(),
            referrals=self.referral.referrals,
            tasks=self.tasks.tasks
        ))
