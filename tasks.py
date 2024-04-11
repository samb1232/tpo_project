import threading
import time
from enum import Enum, auto


class TaskTypes(Enum):
    BASIC = auto()
    EXTENDED = auto()


class TaskStates(Enum):
    RUNNING = auto()
    READY = auto()
    SUSPENDED = auto()
    WAITING = auto()


class TaskCommands(Enum):
    DONE = auto()
    NOT_DONE = auto()
    SHOULD_WAIT = auto()


# Generate unique task IDs
def task_id_generator():
    id_counter = 1
    while True:
        yield id_counter
        id_counter += 1


class Task:
    task_id_gen = task_id_generator()

    def __init__(self, priority, execution_time: int):
        self.id: int = next(self.task_id_gen)
        self.state: TaskStates = TaskStates.SUSPENDED  # Initial state is suspended
        self.priority: int = priority
        self.execution_time: int = execution_time

        self.progress: int = 0
        self.type: str = TaskTypes.BASIC.name

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

    def execute(self) -> TaskCommands:
        assert self.state == TaskStates.RUNNING, f"Cannot execute task. Current state is {self.state.name}, not RUNNING."
        self.progress += 1

        if self.progress >= self.execution_time:
            return TaskCommands.DONE
        return TaskCommands.NOT_DONE


class ExtendedTask(Task):
    def __init__(self, priority, execution_time: int, should_wait: bool, wait_start_time: int, wait_duration: float):
        super().__init__(priority, execution_time)
        if wait_start_time >= execution_time:
            raise AttributeError("Cannot create Extended Task. wait_start_time should be lower than execution_time")

        self.should_wait: bool = should_wait
        self.has_waited: bool = False
        self.wait_start_time: int = wait_start_time  # Time at which task should start waiting
        self.wait_duration: float = wait_duration

        self.type = TaskTypes.EXTENDED.name

    def execute(self) -> TaskCommands:
        """
        Имитирует процесс выполнения задачи.

        """
        assert self.state == TaskStates.RUNNING, f"Cannot execute task. Current state is {self.state.name}, not RUNNING."
        self.progress += 1
        if self.progress == self.wait_start_time:
            if self.should_wait:
                return TaskCommands.SHOULD_WAIT
        if self.progress >= self.execution_time:
            return TaskCommands.DONE
        return TaskCommands.NOT_DONE

    def wait(self) -> None:
        """
        Переводит задачу режим ожидания.
        """
        assert self.state == TaskStates.RUNNING, f"Cannot wait task. Current state is {self.state.name}, not RUNNING."
        self.state = TaskStates.WAITING
        threading.Thread(target=self.wait_task, daemon=True).start()

    def wait_task(self):
        """
        Ждёт определённое время и запускает флаг has_waited.
        """
        self.has_waited = False
        time.sleep(self.wait_duration)
        self.has_waited = True

    def release(self) -> None:
        assert self.state == TaskStates.WAITING, f"Cannot release task. Current state is {self.state.name}, not WAITING."
        self.state = TaskStates.READY
