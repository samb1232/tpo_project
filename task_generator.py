import random
import time

from scheduler import Scheduler
from task import Task


class TaskGenerator:

    def __init__(self, scheduler: Scheduler):
        self.scheduler = scheduler

    def start_generating(self):
        while True:
            is_extended: bool = random.randint(0, 1) == 1
            if is_extended:
                pass
                # TODO: Сделать генерацию расширенных задач
            else:
                new_task = Task(random.randint(0, 3), random.randint(3, 50))
                self.scheduler.activate_task(new_task)
            time.sleep(random.randint(3, 10))
