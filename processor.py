from __future__ import annotations

import time

from scheduler import Scheduler


class Processor:
    def __init__(self, scheduler: Scheduler):
        self.scheduler: Scheduler = scheduler

    def run(self):
        while True:
            print("Processor clock")
            if self.scheduler.running_task is not None:
                print(f"Running task №{self.scheduler.running_task.task_id}. "
                      f"Progress: {self.scheduler.running_task.progress}/{self.scheduler.running_task.execution_time}")
                if self.scheduler.running_task.execute():
                    print(f"Task №{self.scheduler.running_task.task_id} done")
                    self.scheduler.finish_task()
            time.sleep(0.3)
