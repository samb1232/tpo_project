import threading
import time
from enum import Enum, auto


class TaskStates(Enum):
    RUNNING = auto()
    READY = auto()
    SUSPENDED = auto()
    WAITING = auto()


class ReturnCommands(Enum):
    DONE = auto()
    NOT_DONE = auto()
    SHOULD_WAIT = auto()


def task_id_generator():
    id_counter = 1
    while True:
        yield id_counter
        id_counter += 1


class Task:
    task_id_gen = task_id_generator()

    def __init__(self, priority, execution_time: int):
        self.id = next(self.task_id_gen)
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
    #   TODO: Тут можно сбросить параметры задачи, чтобы потом её можно было запустить снова

    def execute(self) -> ReturnCommands:
        assert self.state == TaskStates.RUNNING, f"Cannot execute task. Current state is {self.state.name}, not RUNNING."
        self.progress += 1

        if self.progress >= self.execution_time:
            return ReturnCommands.DONE
        return ReturnCommands.NOT_DONE


class ExtendedTask(Task):
    def __init__(self, priority, execution_time: int, should_wait: bool, wait_start_time: int, wait_duration: int):
        super().__init__(priority, execution_time)
        if wait_start_time >= execution_time:
            raise AttributeError("Cannot create Extended Task. wait_start_time should be lower than execution_time")

        self.should_wait = should_wait
        self.has_waited = False
        self.wait_start_time = wait_start_time
        self.wait_duration = wait_duration

    def execute(self) -> ReturnCommands:
        assert self.state == TaskStates.RUNNING, f"Cannot execute task. Current state is {self.state.name}, not RUNNING."
        self.progress += 1
        if self.progress == self.wait_start_time:
            if self.should_wait:
                return ReturnCommands.SHOULD_WAIT
        if self.progress >= self.execution_time:
            return ReturnCommands.DONE
        return ReturnCommands.NOT_DONE

    def wait(self) -> None:
        assert self.state == TaskStates.RUNNING, f"Cannot wait task. Current state is {self.state.name}, not RUNNING."
        self.state = TaskStates.WAITING
        threading.Thread(target=self.wait_task, daemon=True).start()

    def wait_task(self):
        self.has_waited = False
        time.sleep(self.wait_duration)
        self.has_waited = True

    def release(self) -> None:
        assert self.state == TaskStates.WAITING, f"Cannot release task. Current state is {self.state.name}, not WAITING."
        self.state = TaskStates.READY
