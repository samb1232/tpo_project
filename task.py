from enum import Enum, auto


class TaskStates(Enum):
    RUNNING = auto()
    READY = auto()
    SUSPENDED = auto()
    WAITING = auto()


def task_id_generator():
    id_counter = 1
    while True:
        yield id_counter
        id_counter += 1


class Task:
    task_id_gen = task_id_generator()

    def __init__(self, priority, execution_time: int):
        self.task_id = next(self.task_id_gen)
        self.state = TaskStates.SUSPENDED
        self.priority = priority
        self.execution_time = execution_time

        self.progress = 0

    def activate(self) -> None:
        assert self.state == TaskStates.SUSPENDED, f"Cannot activate task. Current state is {self.state.name}, not SUSPENDED."
        self.state = TaskStates.READY

    def start(self) -> None:
        assert self.state == TaskStates.READY, f"Cannot start task. Current state is {self.state.name}, not READY."
        self.state = TaskStates.RUNNING

    def preempt(self) -> None:
        assert self.state == TaskStates.RUNNING, f"Cannot preempt task. Current state is {self.state.name}, not RUNNING."
        self.state = TaskStates.READY

    def terminate(self) -> None:
        assert self.state == TaskStates.RUNNING, f"Cannot terminate task. Current state is {self.state.name}, not RUNNING."
        self.state = TaskStates.SUSPENDED

    def execute(self) -> bool:
        assert self.state == TaskStates.RUNNING, f"Cannot execute task. Current state is {self.state.name}, not RUNNING."
        self.progress += 1

        if self.progress >= self.execution_time:
            return True
        return False

#
#
# class ExtendedTask(Task):
#
#     def __init__(self, priority, execution_time: int, wait_time: int):
#         super.__init__(priority, execution_time)
#
#
#
#     def wait(self) -> bool:
#         if self.task_type != TaskTypes.EXTENDED:
#             raise RuntimeError(f"Task {self.task_id} is not an extended task and cannot wait.")
#
#         if self.state == TaskStates.RUNNING:
#             self.state = TaskStates.WAITING
#             return True
#         return False
#
#     def release(self) -> bool:
#         if self.task_type != TaskTypes.EXTENDED:
#             raise RuntimeError(f"Task {self.task_id} is not an extended task and cannot be released.")
#
#         if self.state == TaskStates.WAITING:
#             self.state = TaskStates.READY
#             return True
#         return False
