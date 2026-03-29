import unittest
from unittest.mock import patch
import io
from datetime import date, timedelta
from pawpal_system import Task, Pet, Owner, Scheduler

class TestPawPalSystem(unittest.TestCase):

    def test_task_completion(self):
        """
        Verify that calling mark_as_complete() changes the task's status.
        """
        # Setup: Create a pet and a task
        pet = Pet(name="Test Pet", breed="N/A", age=1)
        task = Task(name="Test Task", duration="00:10", time="10:00", priority=1, frequency='daily')
        
        # Pre-condition: Assert the task is not completed initially
        self.assertFalse(task.is_completed, "Task should initially be incomplete.")
        
        # Action: Mark the task as complete
        task.mark_as_complete()
        
        # Post-condition: Assert the task is now complete
        self.assertTrue(task.is_completed, "Task should be marked as complete.")

    def test_task_addition(self):
        """
        Verify that adding a task to a Pet increases that pet's task count.
        """
        # Setup: Create a pet
        pet = Pet(name="Test Pet", breed="N/A", age=1)
        
        # Pre-condition: Assert the pet has no tasks initially
        self.assertEqual(len(pet.tasks), 0, "Pet should have no tasks initially.")
        
        # Action: Add a task to the pet
        task = Task(name="New Task", duration="00:15", time="15:00", priority=2, frequency='daily')
        pet.add_task(task)
        
        # Post-condition: Assert the pet's task count has increased to 1
        self.assertEqual(len(pet.tasks), 1, "Pet's task count should be 1 after adding a task.")
        self.assertIn(task, pet.tasks, "The new task should be in the pet's task list.")

    def test_sort_by_start_time(self):
        """
        Verify tasks are returned in chronological order by start time.
        """
        owner = Owner("Test Owner")
        scheduler = Scheduler(owner)
        pet = Pet(name="Test Pet", breed="N/A", age=1)
        owner.add_pet(pet)

        task1 = Task(name="Morning Walk", duration="00:30", time="08:00", priority=3, frequency='daily', due_date=date(2024, 1, 1))
        task2 = Task(name="Evening Feed", duration="00:15", time="18:00", priority=4, frequency='daily', due_date=date(2024, 1, 1))
        task3 = Task(name="Midday Play", duration="00:20", time="12:00", priority=2, frequency='daily', due_date=date(2024, 1, 1))
        
        pet.add_task(task1)
        pet.add_task(task2)
        pet.add_task(task3)

        sorted_tasks = scheduler.sort_by_start_time()
        
        self.assertEqual(len(sorted_tasks), 3)
        self.assertEqual(sorted_tasks[0].name, "Morning Walk")
        self.assertEqual(sorted_tasks[1].name, "Midday Play")
        self.assertEqual(sorted_tasks[2].name, "Evening Feed")

    def test_daily_task_recurrence(self):
        """
        Confirm that marking a daily task complete creates a new task for the following day.
        """
        owner = Owner("Test Owner")
        scheduler = Scheduler(owner)
        pet = Pet(name="Test Pet", breed="N/A", age=1)
        owner.add_pet(pet)
        
        today = date.today()
        task = Task(name="Daily Feed", duration="00:15", time="08:00", priority=5, frequency='daily', due_date=today)
        pet.add_task(task)
        
        scheduler.complete_task(task)
        
        self.assertTrue(task.is_completed)
        self.assertEqual(len(pet.tasks), 2)
        
        new_task = pet.tasks[1]
        self.assertFalse(new_task.is_completed)
        self.assertEqual(new_task.name, "Daily Feed")
        self.assertEqual(new_task.due_date, today + timedelta(days=1))

    def test_conflict_detection(self):
        """
        Verify that the Scheduler flags duplicate times.
        """
        owner = Owner("Test Owner")
        scheduler = Scheduler(owner)
        pet = Pet(name="Test Pet", breed="N/A", age=1)
        owner.add_pet(pet)

        task1 = Task(name="Walk", duration="00:30", time="09:00", priority=3, frequency='daily')
        task2 = Task(name="Feed", duration="00:15", time="09:00", priority=4, frequency='daily')
        pet.add_task(task1)
        pet.add_task(task2)

        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            scheduler.generate_plan(available_time=60)
            output = mock_stdout.getvalue()
            self.assertIn("Warning: Multiple tasks are scheduled for 09:00", output)
            self.assertIn("'Walk'", output)
            self.assertIn("'Feed'", output)

if __name__ == '__main__':
    unittest.main()
