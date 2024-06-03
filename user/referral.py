from typing import TypedDict

# todo: ref link need modifications
base_link = "https://t.me/"

referral_reward_fix = 25000
task_referral_reward = [(3, 25000), (10, 600000), (20, 600000), (25, 600000), (50, 600000)]


class Referral(object):
    # referrals: list[int]

    def __init__(self, user_id: int, claimed: list[int], referrals: list[int]) -> None:
        self.referral_link = base_link + str(user_id)
        self.referrals = referrals
        self.claimed_referrals = []
        self.claimed_referrals_index = []

        for i in claimed:
            self.claimed_referrals.append(task_referral_reward[i])
            self.claimed_referrals_index.append(task_referral_reward.index(task_referral_reward[i]))

    def get_claimed_referrals_index(self):
        return self.claimed_referrals_index

    @staticmethod
    def get_reward_tier():
        return task_referral_reward

    def achieved_referrals(self):
        achieved = task_referral_reward[:self.referral_count()]
        return achieved

    def add_referral(self, referral: int):
        self.referrals.append(referral)
        self.referrals.sort()
        return True

    def referral_count(self):
        return len(self.referrals)

    def referral_link(self):
        return self.referral_link

    @staticmethod
    def referral_reward():
        return referral_reward_fix

    def referral_reward_task_complete(self, task_index: int):
        if (task_referral_reward[task_index][0] < self.referral_count() and
                task_referral_reward[task_index] not in self.claimed_referrals and
                task_referral_reward[task_index] in self.achieved_referrals()):
            self.claimed_referrals.append(task_referral_reward[task_index])
            return task_referral_reward[task_index][1]
        return False
