import threading

from processor import Processor
from scheduler import Scheduler
from task_generator import TaskGenerator

scheduler = Scheduler()
processor = Processor(scheduler, 0.1)
task_generator = TaskGenerator(scheduler)

if __name__ == "__main__":
    # Запуск потока, который следит за задачами в состоянии ожидания
    threading.Thread(target=scheduler.run_waiting_tasks_listener, daemon=True).start()

    # Запуск потока, который генерирует новые задачи
    threading.Thread(target=task_generator.start_generating, daemon=True).start()

    # Запуск работы процессора
    processor.run()
