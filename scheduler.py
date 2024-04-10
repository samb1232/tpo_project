from __future__ import annotations

import time

from tasks import Task, ExtendedTask


class Scheduler:
    def __init__(self):
        self.tasks_queues = {
            0: [],
            1: [],
            2: [],
            3: [],
        }
        self.waiting_tasks = []
        self.suspended_tasks = []
        self.running_task: Task | ExtendedTask | None = None

    def activate_task(self, task: Task | ExtendedTask) -> None:
        print(f"Activating new task. ID: {task.id}, Priority: {task.priority}, TTE: {task.execution_time}")
        task.activate()
        if self.running_task is None:
            task.start()
            self.running_task = task
        elif self.running_task.priority < task.priority:
            self.swap_tasks(task)
        else:
            self.tasks_queues[task.priority].append(task)

    def get_next_task(self) -> Task | ExtendedTask | None:
        for priority in range(4):
            if len(self.tasks_queues[priority]) > 0:
                task = self.tasks_queues[priority][0]
                task.start()
                del self.tasks_queues[priority][0]
                return task
        return None

    def finish_task(self) -> None:
        self.running_task.terminate()
        self.suspended_tasks.append(self.running_task)
        next_task = self.get_next_task()
        self.running_task = next_task

    def swap_tasks(self, new_task: Task | ExtendedTask) -> None:
        self.running_task.preempt()
        self.tasks_queues[self.running_task.priority].insert(0, self.running_task)
        new_task.start()
        self.running_task = new_task

    def run_waiting_tasks_listener(self) -> None:
        while True:
            index = 0
            while index < len(self.waiting_tasks):
                if self.waiting_tasks[index].has_waited:
                    self.release_task(self.waiting_tasks[index])
                    del self.waiting_tasks[index]
                    continue
                index += 1

            time.sleep(0.5)

    def wait_task(self) -> None:
        self.running_task.wait()
        self.waiting_tasks.append(self.running_task)
        next_task = self.get_next_task()
        self.running_task = next_task

    def release_task(self, task: ExtendedTask) -> None:
        task.release()
        if self.running_task is None:
            task.start()
            self.running_task = task
        elif self.running_task.priority < task.priority:
            self.swap_tasks(task)
        else:
            self.tasks_queues[task.priority].append(task)
