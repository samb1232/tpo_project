import threading
import time

from scheduler import Scheduler
from processor import Processor
from task import Task
from task_generator import TaskGenerator

scheduler = Scheduler()
processor = Processor(scheduler)
task_generator = TaskGenerator(scheduler)

if __name__ == "__main__":
    threading.Thread(target=processor.run).start()
    threading.Thread(target=task_generator.start_generating).start()
