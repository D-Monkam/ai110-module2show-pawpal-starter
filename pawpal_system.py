from dataclasses import dataclass, field
from typing import List, Dict


@dataclass
class Task:
    """Represents a single care task for a pet."""
    name: str  # Description of the task
    time: int  # Duration in minutes
    priority: int # e.g., 1-5 (1 is lowest)
    frequency: str # e.g., 'daily', 'weekly'
    is_completed: bool = False

    def mark_as_complete(self):
        """Marks this task as complete."""
        self.is_completed = True

    def edit_name(self, name: str):
        """Updates the name of this task."""
        self.name = name

@dataclass
class Pet:
    """Represents a pet, its details, and its list of tasks."""
    name: str
    breed: str
    age: int
    tasks: List[Task] = field(default_factory=list)
    diet: List[str] = field(default_factory=list)
    medication: List[str] = field(default_factory=list)
    satisfactoryLevel: float = 0.0

    def add_task(self, task: Task):
        """Adds a new task to this pet's task list."""
        self.tasks.append(task)

    def add_to_diet(self, item: str):
        """Adds a new food item to this pet's diet."""
        self.diet.append(item)

    def add_to_medication(self, item: str):
        """Adds a new medication to this pet's medication list."""
        self.medication.append(item)

    def calculate_satisfaction(self) -> float:
        """Calculates this pet's satisfaction level based on completed tasks."""
        completed_tasks = [task for task in self.tasks if task.is_completed]
        if not self.tasks:
            return 100.0  # No tasks, so pet is satisfied
        
        satisfaction = (len(completed_tasks) / len(self.tasks)) * 100
        self.satisfactoryLevel = satisfaction
        return self.satisfactoryLevel

class Owner:
    """Manages multiple pets and provides access to all their tasks."""
    def __init__(self, name: str):
        self.name = name
        self.pets: List[Pet] = []

    def add_pet(self, pet: Pet):
        """Adds a new pet to this owner's pet list."""
        self.pets.append(pet)

    def get_all_tasks(self) -> List[Task]:
        """Returns a combined list of all tasks for all of this owner's pets."""
        all_tasks = []
        for pet in self.pets:
            all_tasks.extend(pet.tasks)
        return all_tasks

class Scheduler:
    """The 'Brain' that retrieves, organizes, and manages tasks across pets."""
    def __init__(self, owner: Owner):
        self.owner = owner

    def generate_plan(self, available_time: int) -> List[Task]:
        """Generates a schedule of tasks that fits within the owner's available time."""
        all_tasks = self.owner.get_all_tasks()
        
        # 1. Filter out completed tasks and sort by priority (higher first)
        uncompleted_tasks = [t for t in all_tasks if not t.is_completed]
        sorted_tasks = sorted(uncompleted_tasks, key=lambda t: t.priority, reverse=True)
        
        # 2. Build the plan within the available time
        plan = []
        time_spent = 0
        for task in sorted_tasks:
            if time_spent + task.time <= available_time:
                plan.append(task)
                time_spent += task.time
                
        return plan
