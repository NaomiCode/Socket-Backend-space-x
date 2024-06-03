import time
import threading
import schedule
import queue

job_queue = queue.Queue()

users = [1, 2, 3, 4]


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


stop_run_continuously = run_continuously()


def job(job_func):
    print(job_func)


def worker_main():
    while 1:
        job_func = job_queue.get()
        job(job_func)
        job_queue.task_done()


worker_thread = threading.Thread(target=worker_main)
worker_thread.start()

schedule.every(1).seconds.do(job_queue.put, users)

while 1:
    time.sleep(2)
    users.append(str(time.time())[-3:])
