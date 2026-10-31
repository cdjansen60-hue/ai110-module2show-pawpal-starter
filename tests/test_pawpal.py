from datetime import time

from pawpal_system import Pet, Task


def test_mark_complete_changes_status():
    task = Task("walk", "Morning walk", time(7, 30))
    assert task.completed is False

    task.mark_complete()

    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet("Mochi", "dog")
    assert len(pet.tasks) == 0

    pet.add_task(Task("feeding", "Breakfast", time(8, 0)))

    assert len(pet.tasks) == 1
