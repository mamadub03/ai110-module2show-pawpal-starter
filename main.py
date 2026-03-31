from pawpal_system import Owner, Pet, Task, Constraints, Scheduler, ScheduleEntry


def main():
    # Create owner
    owner = Owner(name="Alex", available_minutes=180)

    # Create pets
    dog = Pet(name="Rex", owner=owner, species="Dog", age=4, weight=22.5)
    cat = Pet(name="Mittens", owner=owner, species="Cat", age=3, weight=5.0)

    # Attach pets to owner
    owner.add_pet(dog)
    owner.add_pet(cat)

    # Add tasks out of order to verify sorting works
    cat.add_task(Task(id="5", name="Evening Brush", duration_minutes=10, priority=2, category="hygiene", preferred_time="evening"))
    dog.add_task(Task(id="2", name="Feed Dog", duration_minutes=15, priority=0, category="care", preferred_time="morning"))
    cat.add_task(Task(id="3", name="Clean Litter", duration_minutes=20, priority=2, category="hygiene", preferred_time="afternoon"))
    dog.add_task(Task(id="1", name="Morning Walk", duration_minutes=30, priority=1, category="exercise", preferred_time="morning"))
    cat.add_task(Task(id="4", name="Playtime", duration_minutes=25, priority=1, category="exercise", preferred_time="evening"))

    # Mark one task done so filter can show it
    dog.tasks[0].mark_done()  # Feed Dog done

    # Demonstrate filter by completion and pet name
    print("\nFiltered tasks: incomplete tasks")
    for task in owner.filter_tasks(done=False):
        print(f"- {task.id}: {task.name} ({task.duration_minutes}m, priority={task.priority})")

    print("\nFiltered tasks: Buddy-equivalent tag not used, so using 'Rex'")
    for task in owner.filter_tasks(pet_name="Rex"):
        print(f"- {task.id}: {task.name} done={task.done}")

    # Build schedule with constraints
    constraints = Constraints(available_minutes=120, max_tasks=4, preferred_times=["morning", "afternoon", "evening"])
    scheduler = Scheduler()
    schedule = scheduler.generate_plan(owner, constraints=constraints)

    print("\nToday's Schedule")
    print("===============")
    print(schedule.explain())

    # Conflict detection example: two tasks at same time
    conflict_schedule = Schedule()
    # use first two tasks for conflict example
    if len(dog.tasks) >= 1 and len(cat.tasks) >= 1:
        conflict_schedule.scheduled_tasks.append(
            ScheduleEntry(task=dog.tasks[0], pet_name=dog.name, start_time=9 * 60, end_time=9 * 60 + 15)
        )
        conflict_schedule.scheduled_tasks.append(
            ScheduleEntry(task=cat.tasks[0], pet_name=cat.name, start_time=9 * 60, end_time=9 * 60 + 20)
        )

    warnings = scheduler.detect_conflicts(conflict_schedule)
    print("\nConflict detection results:")
    if warnings:
        for w in warnings:
            print("WARNING:", w)
    else:
        print("No conflicts detected.")


if __name__ == "__main__":
    main()
