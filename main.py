import threading

from processor import Processor
from scheduler import Scheduler
from tasks import Task, ExtendedTask
from task_generator import TaskGenerator

scheduler = Scheduler()
processor = Processor(scheduler)
task_generator = TaskGenerator(scheduler)

if __name__ == "__main__":
    threading.Thread(target=scheduler.run_waiting_tasks_listener, daemon=True).start()
    threading.Thread(target=task_generator.start_generating, daemon=True).start()
    processor.run()
