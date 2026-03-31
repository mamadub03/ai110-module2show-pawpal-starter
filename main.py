from pawpal_system import Owner, Pet, Task, Constraints, Scheduler


def main():
    # Create owner
    owner = Owner(name="Alex", available_minutes=180)

    # Create pets
    dog = Pet(name="Rex", owner=owner, species="Dog", age=4, weight=22.5)
    cat = Pet(name="Mittens", owner=owner, species="Cat", age=3, weight=5.0)

    # Attach pets to owner
    owner.add_pet(dog)
    owner.add_pet(cat)

    # Add tasks
    dog.add_task(Task(id="1", name="Morning Walk", duration_minutes=30, priority=1, category="exercise", preferred_time="morning"))
    dog.add_task(Task(id="2", name="Feed Dog", duration_minutes=15, priority=0, category="care", preferred_time="morning"))
    cat.add_task(Task(id="3", name="Clean Litter", duration_minutes=20, priority=2, category="hygiene", preferred_time="afternoon"))
    cat.add_task(Task(id="4", name="Playtime", duration_minutes=25, priority=1, category="exercise", preferred_time="evening"))

    # Build schedule with constraints
    constraints = Constraints(available_minutes=120, max_tasks=4, preferred_times=["morning", "afternoon", "evening"])
    scheduler = Scheduler()
    schedule = scheduler.generate_plan(owner, constraints=constraints)

    print("Today's Schedule")
    print("===============")
    print(schedule.explain())


if __name__ == "__main__":
    main()
