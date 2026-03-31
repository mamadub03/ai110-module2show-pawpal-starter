import pytest
from pawpal_system import Pet, Owner, Task, Schedule, ScheduleEntry


def test_task_completion_marks_done():
    task = Task(id="t1", name="Feed", duration_minutes=10, priority=1)
    assert not task.done

    task.mark_done()

    assert task.done


def test_adding_task_increases_pet_task_count():
    owner = Owner(name="Alex", available_minutes=60)
    pet = Pet(name="Buddy", owner=owner, species="Dog", age=2, weight=10.0)
    owner.add_pet(pet)

    assert len(pet.tasks) == 0

    new_task = Task(id="t2", name="Walk", duration_minutes=30, priority=1)
    pet.add_task(new_task)

    assert len(pet.tasks) == 1
    assert pet.tasks[0] is new_task


def test_daily_task_recurring_auto_creates_next():
    owner = Owner(name="Alex", available_minutes=180)
    pet = Pet(name="Buddy", owner=owner, species="Dog", age=2, weight=10.0)
    owner.add_pet(pet)

    recurring = Task(
        id="t-daily", name="Feed", duration_minutes=10, priority=1, recurrence="daily"
    )
    pet.add_task(recurring)

    next_task = recurring.mark_done(pet=pet)

    assert recurring.done is True
    assert next_task is not None
    assert next_task.id == "t-daily-next"
    assert next_task.done is False
    assert next_task.recurrence == "daily"
    assert len(pet.tasks) == 2


def test_scheduler_detects_time_conflict():
    owner = Owner(name="Alex", available_minutes=240)
    dog = Pet(name="Buddy", owner=owner, species="Dog", age=4, weight=15.0)
    cat = Pet(name="Mittens", owner=owner, species="Cat", age=3, weight=5.0)
    owner.add_pet(dog)
    owner.add_pet(cat)

    task_dog = Task(id="t1", name="Walk", duration_minutes=30, priority=1)
    task_cat = Task(id="t2", name="Play", duration_minutes=20, priority=1)
    dog.add_task(task_dog)
    cat.add_task(task_cat)

    schedule = Schedule()
    schedule.scheduled_tasks.append(ScheduleEntry(task=task_dog, pet_name=dog.name, start_time=540, end_time=570))
    schedule.scheduled_tasks.append(ScheduleEntry(task=task_cat, pet_name=cat.name, start_time=540, end_time=560))

    scheduler = Scheduler()
    warnings = scheduler.detect_conflicts(schedule)

    assert len(warnings) == 1
    assert "overlaps" in warnings[0]


def test_owner_filter_tasks_by_completion_and_pet_name():
    owner = Owner(name="Alex", available_minutes=120)
    pet1 = Pet(name="Buddy", owner=owner, species="Dog", age=2, weight=10.0)
    pet2 = Pet(name="Milo", owner=owner, species="Cat", age=3, weight=4.0)
    owner.add_pet(pet1)
    owner.add_pet(pet2)

    task1 = Task(id="t1", name="Feed", duration_minutes=10, priority=1)
    task2 = Task(id="t2", name="Walk", duration_minutes=30, priority=1)
    task3 = Task(id="t3", name="Groom", duration_minutes=20, priority=2)
    pet1.add_task(task1)
    pet1.add_task(task2)
    pet2.add_task(task3)

    task2.mark_done()

    # By completion status
    incomplete = owner.filter_tasks(done=False)
    assert set([t.id for t in incomplete]) == {"t1", "t3"}

    completed = owner.filter_tasks(done=True)
    assert [t.id for t in completed] == ["t2"]

    # By pet name
    buddy_tasks = owner.filter_tasks(pet_name="Buddy")
    assert set([t.id for t in buddy_tasks]) == {"t1", "t2"}

    # Combined
    buddy_incomplete = owner.filter_tasks(done=False, pet_name="Buddy")
    assert [t.id for t in buddy_incomplete] == ["t1"]
