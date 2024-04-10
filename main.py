import threading
import time

from scheduler import Scheduler
from processor import Processor
from task import Task

scheduler = Scheduler()
processor = Processor(scheduler)

if __name__ == "__main__":
    threading.Thread(target=processor.run).start()
    scheduler.activate_task(Task(0, 10))
    time.sleep(4)
    scheduler.activate_task(Task(2, 6))

