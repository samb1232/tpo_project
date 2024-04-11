import unittest

from scheduler import Scheduler
from task_generator import TaskGenerator


class TestTaskGenerator(unittest.TestCase):
    def test_generate_and_activate_task(self):
        for _ in range(50):
            scheduler = Scheduler()
            task_generator = TaskGenerator(scheduler)
            new_task = task_generator.generate_task()
            scheduler.activate_task(new_task)
            self.assertTrue(new_task == scheduler.running_task)


