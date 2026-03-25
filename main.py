from pawpal_system import Owner, Pet, Task, Scheduler

def main():
    """
    A script to demonstrate the core functionality of the PawPal system.
    """
    # 1. Create an Owner
    owner = Owner(name="Alex")

    # 2. Create two Pets
    pet1 = Pet(name="Buddy", breed="Golden Retriever", age=5)
    pet2 = Pet(name="Lucy", breed="Siamese Cat", age=3)

    # 3. Add tasks to the pets
    # Tasks for Buddy
    task1 = Task(name="Morning Walk", time=30, priority=5, frequency='daily')
    task2 = Task(name="Evening Feed", time=15, priority=4, frequency='daily')
    task3 = Task(name="Play fetch", time=20, priority=3, frequency='daily')
    
    pet1.add_task(task1)
    pet1.add_task(task2)
    pet1.add_task(task3)

    # Tasks for Lucy
    task4 = Task(name="Administer Medication", time=5, priority=5, frequency='daily')
    task5 = Task(name="Grooming", time=25, priority=2, frequency='daily')
    task6 = Task(name="Clean litter box", time=10, priority=4, frequency='daily')

    pet2.add_task(task4)
    pet2.add_task(task5)
    pet2.add_task(task6)

    # 4. Add pets to the owner
    owner.add_pet(pet1)
    owner.add_pet(pet2)

    # 5. Create a Scheduler and generate a plan
    scheduler = Scheduler(owner)
    available_time = 120  # Owner has 2 hours available today
    todays_plan = scheduler.generate_plan(available_time)

    # 6. Print the schedule to the terminal
    print("--- Today's Schedule ---")
    if not todays_plan:
        print("No tasks scheduled for today.")
    else:
        total_time = 0
        for task in todays_plan:
            print(f"- {task.name} ({task.time} mins) - Priority: {task.priority}")
            total_time += task.time
        print("------------------------")
        print(f"Total estimated time: {total_time} minutes")

if __name__ == "__main__":
    main()
