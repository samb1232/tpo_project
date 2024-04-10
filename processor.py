from __future__ import annotations

import time

from scheduler import Scheduler
from tasks import ReturnCommands


class Processor:
    def __init__(self, scheduler: Scheduler):
        self.scheduler: Scheduler = scheduler

    def run(self):
        while True:
            print("Processor clock:", sep=" ")
            if self.scheduler.running_task is not None:
                print(f"Running task №{self.scheduler.running_task.id}. "
                      f"Progress: {self.scheduler.running_task.progress}/{self.scheduler.running_task.execution_time}")
                command: ReturnCommands = self.scheduler.running_task.execute()
                if command == ReturnCommands.DONE:
                    print(f"Task №{self.scheduler.running_task.id} done")
                    self.scheduler.finish_task()
                if command == ReturnCommands.SHOULD_WAIT:
                    print(f"Putting task №{self.scheduler.running_task.id} to wait state")
                    self.scheduler.wait_task()
            time.sleep(1.5)
