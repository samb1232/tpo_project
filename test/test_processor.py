import random
import unittest

from processor import Processor
from scheduler import Scheduler
from tasks import Task, ExtendedTask


class TestProcessor(unittest.TestCase):
    def test_execute_task(self):
        for _ in range(50):
            scheduler = Scheduler()
            processor = Processor(scheduler)

            execution_time = random.randint(2, 20)
            new_task = Task(0, execution_time)
            scheduler.activate_task(new_task)

            self.assertIsNotNone(scheduler.running_task)
            for i in range(execution_time):
                self.assertEqual(new_task.progress, i)
                processor.process_task()
            self.assertIsNone(scheduler.running_task)

    def test_execute_extended_task(self):
        for _ in range(50):
            scheduler = Scheduler()
            processor = Processor(scheduler)

            execution_time = random.randint(2, 20)
            new_task = ExtendedTask(0, execution_time, False, execution_time - 1, 2)
            scheduler.activate_task(new_task)

            self.assertIsNotNone(scheduler.running_task)
            for i in range(execution_time):
                self.assertEqual(new_task.progress, i)
                processor.process_task()
            self.assertIsNone(scheduler.running_task)
