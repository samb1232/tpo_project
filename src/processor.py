from __future__ import annotations

import time

from scheduler import Scheduler
from tasks import TaskCommands


class Processor:
    def __init__(self, scheduler: Scheduler, speed: float = 1.0):
        self.scheduler: Scheduler = scheduler
        self.speed = speed  # Период работы процессора, в секундах

    def run(self):
        """
        Главный цикл процессора.
        В бесконечном цикле, в зависимости от состояния sceduler.current_task выполняется задача.
        Если задача выполнена или уходит в ожидание, вызывает соответствующие функции в sceduler.

        Следует запускать в отдельном потоке.
        """
        while True:
            self.process_task()
            time.sleep(self.speed)

    def process_task(self):
        print("Processor clock:", end=" ")
        if self.scheduler.running_task is not None:
            print(f"Running task №{self.scheduler.running_task.id}. "
                  f"Progress: {self.scheduler.running_task.progress}/{self.scheduler.running_task.execution_time}")
            command: TaskCommands = self.scheduler.running_task.execute()
            if command == TaskCommands.DONE:
                print(f"Task №{self.scheduler.running_task.id} done")
                self.scheduler.finish_task()
            if command == TaskCommands.SHOULD_WAIT:
                print(f"Putting task №{self.scheduler.running_task.id} to wait state")
                self.scheduler.wait_task()
        else:
            print("IDLE")
