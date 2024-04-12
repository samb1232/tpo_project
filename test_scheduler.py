import random
import unittest

from processor import Processor
from scheduler import Scheduler
from tasks import Task, ExtendedTask, TaskStates


class TestScheduler(unittest.TestCase):
    def test_activate_task(self):
        scheduler = Scheduler()
        task = Task(0, 5)
        self.assertIsNone(scheduler.running_task)
        scheduler.activate_task(task)
        self.assertEqual(scheduler.running_task, task)

    def test_activate_extended_task(self):
        scheduler = Scheduler()
        task = ExtendedTask(0, 5)
        self.assertIsNone(scheduler.running_task)
        scheduler.activate_task(task)
        self.assertEqual(scheduler.running_task, task)

    def test_get_next_task(self):
        scheduler = Scheduler()
        task1 = Task(0, 2)
        task2 = ExtendedTask(0, 3)
        scheduler.activate_task(task1)
        scheduler.activate_task(task2)
        next_task = scheduler.get_next_task()
        self.assertEqual(next_task, task2)

    def test_finish_task(self):
        scheduler = Scheduler()
        task1 = Task(0, 2)
        task2 = ExtendedTask(0, 3)
        scheduler.activate_task(task1)
        scheduler.activate_task(task2)
        scheduler.finish_task()

        self.assertEqual(scheduler.suspended_tasks[0], task1)
        self.assertEqual(scheduler.running_task, task2)

    def test_finish_none_task(self):
        scheduler = Scheduler()
        self.assertRaises(ValueError, scheduler.finish_task)

    def test_swap_tasks(self):
        scheduler = Scheduler()
        task1 = Task(0, 2)
        task2 = ExtendedTask(1, 3)
        scheduler.activate_task(task1)
        self.assertEqual(scheduler.running_task, task1)
        scheduler.activate_task(task2)
        self.assertEqual(scheduler.running_task, task2)

    def test_wait_task(self):
        scheduler = Scheduler()
        task1 = ExtendedTask(0, 5, True, 2, 0.5)
        scheduler.activate_task(task1)
        scheduler.wait_task()
        self.assertIsNone(scheduler.running_task)
        self.assertEqual(task1.state, TaskStates.WAITING)
        self.assertEqual(scheduler.waiting_tasks[0], task1)

    def test_release_task(self):
        scheduler = Scheduler()
        task1 = ExtendedTask(0, 5, True, 2, 0.5)
        scheduler.activate_task(task1)
        scheduler.wait_task()
        scheduler.release_task(task1)
        self.assertEqual(scheduler.running_task, task1)
        self.assertEqual(task1.state, TaskStates.RUNNING)

    def test_execute_task(self):
        for _ in range(50):
            scheduler = Scheduler()
            processor = Processor(scheduler)
            execution_time = random.randint(5, 100)
            task = Task(0, execution_time)
            scheduler.activate_task(task)
            for i in range(execution_time):
                self.assertTrue(scheduler.running_task.progress == i)
                processor.process_task()
            self.assertIsNone(scheduler.running_task)
            self.assertTrue(scheduler.suspended_tasks[0] == task)

        for _ in range(50):
            scheduler = Scheduler()
            processor = Processor(scheduler)
            execution_time = random.randint(5, 100)
            task = ExtendedTask(0, execution_time, False, 0, 0)
            scheduler.activate_task(task)
            for i in range(execution_time):
                self.assertTrue(scheduler.running_task.progress == i)
                processor.process_task()
            self.assertIsNone(scheduler.running_task)
            self.assertTrue(scheduler.suspended_tasks[0] == task)

    def test_preempt_task(self):
        scheduler = Scheduler()
        processor = Processor(scheduler)
        task_1 = Task(0, 10)
        task_2 = Task(1, 3)

        scheduler.activate_task(task_1)

        for i in range(5):
            processor.process_task()

        self.assertEqual(task_1.progress, 5)

        self.assertTrue(scheduler.running_task == task_1)

        scheduler.activate_task(task_2)

        self.assertTrue(scheduler.running_task == task_2)
        self.assertTrue(len(scheduler.tasks_queues[0]) > 0)
        self.assertTrue(scheduler.tasks_queues[0][0] == task_1)

        for i in range(3):
            processor.process_task()

        self.assertTrue(scheduler.running_task == task_1)
        self.assertTrue(len(scheduler.suspended_tasks) == 1)


