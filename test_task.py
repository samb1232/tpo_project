import random
import unittest
import time

from tasks import Task, TaskStates, ExtendedTask, TaskCommands


class TestTask(unittest.TestCase):
    def test_task_initialization(self):
        for _ in range(100):
            priority = random.randint(0, 3)
            execution_time = random.randint(2, 1000)
            task = Task(priority, execution_time)
            self.assertEqual(task.state, TaskStates.SUSPENDED)
            self.assertEqual(task.priority, priority)
            self.assertEqual(task.execution_time, execution_time)
            self.assertEqual(task.progress, 0)
            self.assertEqual(task.type, "BASIC")

    def test_task_activation(self):
        task = Task(1, 5)
        task.activate()
        self.assertEqual(task.state, TaskStates.READY)

    def test_task_start(self):
        task = Task(1, 5)
        task.activate()
        task.start()
        self.assertEqual(task.state, TaskStates.RUNNING)

    def test_task_preemption(self):
        task = Task(1, 5)
        task.activate()
        task.start()
        task.preempt()
        self.assertEqual(task.state, TaskStates.READY)

    def test_task_termination(self):
        task = Task(1, 5)
        task.activate()
        task.start()
        task.terminate()
        self.assertEqual(task.state, TaskStates.SUSPENDED)

    def test_task_execution(self):
        task = Task(1, 5)
        task.activate()
        task.start()
        task.execute()
        self.assertEqual(task.progress, 1)

    def test_extended_task_initialization(self):
        for _ in range(100):
            priority = random.randint(0, 3)
            execution_time = random.randint(2, 1000)
            should_wait = random.randint(0, 1) == 1
            wait_start_time = random.randint(1, execution_time - 1)
            wait_duration = random.randint(1, 1000)
            extended_task = ExtendedTask(priority, execution_time, should_wait, wait_start_time, wait_duration)
            self.assertEqual(extended_task.state, TaskStates.SUSPENDED)
            self.assertEqual(extended_task.priority, priority)
            self.assertEqual(extended_task.execution_time, execution_time)
            self.assertEqual(extended_task.progress, 0)
            self.assertEqual(extended_task.should_wait, should_wait)
            self.assertEqual(extended_task.wait_start_time, wait_start_time)
            self.assertEqual(extended_task.wait_duration, wait_duration)
            self.assertEqual(extended_task.type, "EXTENDED")

    def test_extended_task_execute_should_wait(self):
        extended_task = ExtendedTask(1, 5, True, 2, 1)
        extended_task.activate()
        extended_task.start()
        command = extended_task.execute()
        self.assertEqual(command, TaskCommands.NOT_DONE)
        command = extended_task.execute()
        self.assertEqual(command, TaskCommands.SHOULD_WAIT)

    def test_extended_task_execute_not_done(self):
        extended_task = ExtendedTask(1, 5, False, 0, 1)
        extended_task.activate()
        extended_task.start()
        command = extended_task.execute()
        self.assertEqual(command, TaskCommands.NOT_DONE)

    def test_extended_task_execute_done(self):
        extended_task = ExtendedTask(1, 5, False, 0, 1)
        extended_task.activate()
        extended_task.start()
        extended_task.execute()
        extended_task.execute()
        extended_task.execute()
        extended_task.execute()
        command = extended_task.execute()
        self.assertEqual(command, TaskCommands.DONE)

    def test_extended_task_wait(self):
        extended_task = ExtendedTask(1, 5, True, 2, 0.3)
        extended_task.activate()
        extended_task.start()
        extended_task.wait()
        self.assertFalse(extended_task.has_waited)
        time.sleep(0.5)  # Ensure waiting thread finishes
        self.assertTrue(extended_task.has_waited)

    def test_extended_task_release(self):
        extended_task = ExtendedTask(1, 5, True, 2, 0.3)
        extended_task.activate()
        extended_task.start()
        extended_task.wait()
        time.sleep(0.5)  # Ensure waiting thread finishes
        extended_task.release()
        self.assertEqual(extended_task.state, TaskStates.READY)


if __name__ == '__main__':
    unittest.main()
