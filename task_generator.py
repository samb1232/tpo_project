import random
import time

from scheduler import Scheduler
from tasks import Task, ExtendedTask


class TaskGenerator:

    def __init__(self, scheduler: Scheduler):
        self.scheduler = scheduler  # Ссылка на планировщик

    def start_generating(self):
        """
        В бесконечном цикле генерирует задачи и передаёт их в scheduler с помощью функции scheduler.activate_task.

        Следует запускать в отдельном потоке.
        """
        while True:
            is_extended: bool = random.randint(0, 1) == 1
            if is_extended:
                execution_time = random.randint(3, 50)
                wait_start_time = random.randint(2, execution_time - 1)
                new_task = ExtendedTask(
                    priority=random.randint(0, 3),
                    execution_time=execution_time,
                    should_wait=random.randint(0, 10) > 3,  # Для большего шанса выведения задачи в waiting
                    wait_start_time=wait_start_time,
                    wait_duration=random.randint(1, 15)
                )
                self.scheduler.activate_task(new_task)
            else:
                new_task = Task(
                    priority=random.randint(0, 3),
                    execution_time=random.randint(3, 50)
                )
                self.scheduler.activate_task(new_task)
            time.sleep(random.randint(3, 10))
