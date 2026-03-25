import unittest
from pawpal_system import Task, Pet

class TestPawPalSystem(unittest.TestCase):

    def test_task_completion(self):
        """
        Verify that calling mark_as_complete() changes the task's status.
        """
        # Setup: Create a pet and a task
        pet = Pet(name="Test Pet", breed="N/A", age=1)
        task = Task(name="Test Task", time=10, priority=1, frequency='daily')
        
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
        task = Task(name="New Task", time=15, priority=2, frequency='daily')
        pet.add_task(task)
        
        # Post-condition: Assert the pet's task count has increased to 1
        self.assertEqual(len(pet.tasks), 1, "Pet's task count should be 1 after adding a task.")
        self.assertIn(task, pet.tasks, "The new task should be in the pet's task list.")

if __name__ == '__main__':
    unittest.main()
