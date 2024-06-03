import requests
from pprint import pprint


class Task(object):
    title: str
    description: str
    url: str
    reward: int

    def __init__(self, title: str, description: str, url: str, reward: int):
        self.title = title
        self.description = description
        self.url = url
        self.reward = reward


def get_tasks():
    response = requests.get("http://192.168.88.167:8002/api/manager/tasks")
    tasks = []
    for item in response.json():
        tasks.append(Task(title=item['title'], description=item['title'], url=item['url'], reward=item['amount']))
    return tasks


def new_task(title: str, description: str, url: str, reward: int):
    response = requests.post("http://192.168.88.167:8002/api/manager/tasks",
                             json={'amount': reward,
                                   'description': description,
                                   'link': url,
                                   'title': title},
                             headers={"Content-Type": "application/json"})

    return response.json()['status'] == "success"


class UserTask(object):
    tasks: list[Task]
    user_completed_tasks: list[int]
    pending_tasks: list[int]

    def __init__(self, completed_tasks: list[int]):
        self.tasks = get_tasks()
        self.user_completed_tasks = completed_tasks

    def completed_tasks(self):
        tasks = []
        for task in self.user_completed_tasks:
            tasks.append(self.tasks.index(self.tasks[task]))
        return tasks

    # todo: telegram integration for this method
    def set_completed(self, task_title: int):
        for task in self.tasks:
            if task.title == task_title:
                self.user_completed_tasks.append(self.tasks.index(task))
                self.pending_tasks.remove(self.tasks.index(task))
                return True
        return False

    def task_reward(self, title: id):
        for task in self.tasks:
            if task.title == title:
                return task.reward
        return None
