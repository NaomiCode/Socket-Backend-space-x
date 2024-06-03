import time
import threading
import schedule
import queue
from user.tasks import Task
from user.user import User
import requests

online_users_queue = queue.Queue()
auto_bot_queue = queue.Queue()


def run_continuously(interval=1):
    cease_continuous_run = threading.Event()

    class ScheduleThread(threading.Thread):
        @classmethod
        def run(cls):
            while not cease_continuous_run.is_set():
                schedule.run_pending()
                time.sleep(interval)

    continuous_thread = ScheduleThread()
    continuous_thread.start()
    return cease_continuous_run


#todo: implement backend database
def get_tasks() -> list[Task]:
    return []


class Game(object):
    Tasks: list[Task]
    OnlineUsers: list[User]
    AutoBotsUser: list[User]

    def __init__(self):
        self.Tasks = get_tasks()
        self.OnlineUsers = []
        self.AutoBotsUser = []
        auto_bot_thread = threading.Thread(target=self.worker_main_auto_bot)
        auto_bot_thread.start()
        energy_thread = threading.Thread(target=self.worker_main_energy)
        energy_thread.start()
        schedule.every().second.do(online_users_queue.put, self.OnlineUsers)
        schedule.every().second.do(auto_bot_queue.put, self.AutoBotsUser)

    def user_go_online(self, user: User):
        print(user.user_id)
        self.OnlineUsers.append(user)
        if user.auto_bot.is_activated():
            self.AutoBotsUser.append(user)
        return True

    # todo: backend migration
    def user_go_offline(self, user: User):
        self.OnlineUsers.remove(user)
        if user.auto_bot.is_activated():
            self.AutoBotsUser.remove(user)
        return True

    def activate_auto_bot(self, index: int):
        if self.OnlineUsers[index].activate_bot():
            self.AutoBotsUser.append(self.OnlineUsers[index])
            return True
        return False

    def activate_refill(self, index: int):
        if self.OnlineUsers[index].activate_refill():
            return True
        return False

    def activate_guru(self, index: int):
        if self.OnlineUsers[index].activate_guru():
            return True
        return False

    def upgrade_limit(self, index: int):
        if self.OnlineUsers[index].upgrade_limit():
            return True
        return False

    def upgrade_speed(self, index: int):
        if self.OnlineUsers[index].upgrade_speed():
            return True
        return False

    def upgrade_multi_tap(self, index: int):
        if self.OnlineUsers[index].upgrade_multi_tap():
            return True
        return False

    def balance(self, index: int):
        return self.OnlineUsers[index].balance.balance

    def energy(self, index: int):
        return self.OnlineUsers[index].energy.energy

    def energy_limit(self, index: int):
        return self.OnlineUsers[index].energy_limit.current_level

    def energy_speed(self, index: int):
        return self.OnlineUsers[index].energy_speed.current_level

    def multi_tap(self, index: int):
        return self.OnlineUsers[index].multi_tap.current_level

    @staticmethod
    def run_forever():
        run_continuously()

    @staticmethod
    def worker_main_energy():
        while 1:
            online_queue_data: list[User] = online_users_queue.get()
            for user in online_queue_data:
                user.energy.auto_increment()
            online_users_queue.task_done()

    @staticmethod
    def worker_main_auto_bot():
        while 1:
            auto_bot_queue_data: list[User] = auto_bot_queue.get()
            for user in auto_bot_queue_data:
                if user.energy.energy == user.energy_limit.value():
                    user.balance.transaction_in(user.energy.speed)
            auto_bot_queue.task_done()

    def ref_link(self, index: int):
        return self.OnlineUsers[index].get_ref_link()

#
# game = Game()
#
#
# game.user_go_online(User(2))
#
# game.run_forever()
# time.sleep(3)
# print("energy", game.OnlineUsers[0].energy.energy)
# print("balance before", game.balance(0))
#
# game.activate_auto_bot(0)
# game.upgrade_speed(0)
# game.upgrade_speed(0)
# game.upgrade_speed(0)
# print("new energy speed",game.energy_speed(0))
# time.sleep(10)
# print("balance after 10", game.balance(0))
# print("energy after 10", game.energy(0))
# game.activate_refill(0)
# print("refill activated!")
# print("energy after refill", game.energy(0))
# time.sleep(10)
# print("balance after 20", game.balance(0))
# game.upgrade_limit(0)
# print("limit upgraded!")
# time.sleep(10)
# print("balance after 30", game.balance(0))
