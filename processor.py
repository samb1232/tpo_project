from __future__ import annotations

import time

from scheduler import Scheduler
from tasks import TaskCommands


class Processor:
    def __init__(self, scheduler: Scheduler, speed: float):
        self.scheduler: Scheduler = scheduler
        self.speed = speed  # Период работы процессора, в секундах

    def run(self):
        while True:
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
            time.sleep(self.speed)
