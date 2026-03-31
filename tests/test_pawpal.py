import pytest
from pawpal_system import Pet, Owner, Task


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
