from datetime import date, time, timedelta

import pytest

from pawpal_system import Frequency, Owner, Pet, Scheduler, Task

# Fixed date so results never depend on when the tests run.
DAY = date(2026, 11, 2)


@pytest.fixture
def household():
    """An owner with two pets (no tasks) and a scheduler over them."""
    owner = Owner("Jordan")
    mochi = Pet("Mochi", "dog")
    luna = Pet("Luna", "cat")
    owner.add_pet(mochi)
    owner.add_pet(luna)
    return owner, mochi, luna, Scheduler(owner)


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


# --- Sorting ---------------------------------------------------------------


def test_tasks_added_out_of_order_are_returned_chronologically(household):
    _, mochi, luna, scheduler = household
    mochi.add_task(Task("walk", "Evening walk", time(18, 0), DAY))
    luna.add_task(Task("meds", "Pill", time(12, 15), DAY))
    mochi.add_task(Task("walk", "Morning walk", time(7, 30), DAY))
    luna.add_task(Task("feeding", "Breakfast", time(9, 0), DAY))

    times = [t.start_time for t in scheduler.get_todays_tasks(DAY)]

    assert times == [time(7, 30), time(9, 0), time(12, 15), time(18, 0)]


def test_sort_orders_by_date_before_time(household):
    _, mochi, _, scheduler = household
    tomorrow_early = Task("walk", "Tomorrow 07:00", time(7, 0), DAY + timedelta(days=1))
    today_late = Task("walk", "Today 18:00", time(18, 0), DAY)
    mochi.add_task(tomorrow_early)
    mochi.add_task(today_late)

    assert scheduler.sort_by_time(scheduler.get_all_tasks()) == [today_late, tomorrow_early]


# --- Recurrence ------------------------------------------------------------


def test_completing_daily_task_creates_next_day_task(household):
    _, mochi, _, scheduler = household
    walk = Task("walk", "Morning walk", time(7, 30), DAY, frequency=Frequency.DAILY)
    mochi.add_task(walk)

    next_walk = scheduler.mark_task_complete(walk)

    assert walk.completed is True
    assert next_walk is not None and next_walk is not walk
    assert next_walk.due_date == DAY + timedelta(days=1)
    assert next_walk.completed is False
    assert next_walk.start_time == walk.start_time
    assert next_walk.pet is mochi
    assert next_walk in mochi.tasks
    assert scheduler.get_todays_tasks(DAY + timedelta(days=1)) == [next_walk]


def test_weekly_task_recurs_in_seven_days_and_once_task_does_not(household):
    _, _, luna, scheduler = household
    flea = Task("meds", "Flea medication", time(12, 0), DAY, frequency=Frequency.WEEKLY)
    vet = Task("vet", "Vet checkup", time(15, 0), DAY)  # frequency defaults to ONCE
    luna.add_task(flea)
    luna.add_task(vet)

    assert scheduler.mark_task_complete(flea).due_date == DAY + timedelta(weeks=1)
    assert scheduler.mark_task_complete(vet) is None
    assert len(luna.tasks) == 3


def test_completing_same_task_twice_creates_only_one_copy(household):
    _, mochi, _, scheduler = household
    walk = Task("walk", "Morning walk", time(7, 30), DAY, frequency=Frequency.DAILY)
    mochi.add_task(walk)

    scheduler.mark_task_complete(walk)
    second = scheduler.mark_task_complete(walk)

    assert second is None
    assert len(mochi.tasks) == 2


# --- Conflict detection ----------------------------------------------------


def test_tasks_at_same_time_are_flagged_as_conflict(household):
    _, mochi, luna, scheduler = household
    mochi.add_task(Task("walk", "Walk", time(8, 0), DAY))
    luna.add_task(Task("feeding", "Breakfast", time(8, 0), DAY))
    luna.add_task(Task("meds", "Pill", time(9, 0), DAY))

    warnings = scheduler.detect_conflicts(scheduler.get_all_tasks())

    assert len(warnings) == 1
    assert "08:00" in warnings[0]
    assert "different pets" in warnings[0]
    assert "Walk" in warnings[0] and "Breakfast" in warnings[0]


def test_same_pet_conflict_is_labeled(household):
    _, _, luna, scheduler = household
    luna.add_task(Task("feeding", "Breakfast", time(8, 0), DAY))
    luna.add_task(Task("vet", "Vet checkup", time(8, 0), DAY))

    warnings = scheduler.detect_conflicts(scheduler.get_all_tasks())

    assert len(warnings) == 1 and "same pet" in warnings[0]


def test_no_conflict_on_different_dates_or_when_one_task_is_done(household):
    _, mochi, luna, scheduler = household
    mochi.add_task(Task("walk", "Walk", time(8, 0), DAY))
    luna.add_task(Task("feeding", "Breakfast", time(8, 0), DAY + timedelta(days=1)))
    assert scheduler.detect_conflicts(scheduler.get_all_tasks()) == []

    done = Task("meds", "Pill", time(8, 0), DAY)
    luna.add_task(done)
    assert len(scheduler.detect_conflicts(scheduler.get_all_tasks())) == 1
    done.mark_complete()
    assert scheduler.detect_conflicts(scheduler.get_all_tasks()) == []


# --- Filtering -------------------------------------------------------------


def test_filter_by_pet_and_status(household):
    _, mochi, luna, scheduler = household
    walk = Task("walk", "Walk", time(8, 0), DAY)
    dinner = Task("feeding", "Dinner", time(18, 0), DAY)
    breakfast = Task("feeding", "Breakfast", time(7, 0), DAY)
    mochi.add_task(walk)
    mochi.add_task(dinner)
    luna.add_task(breakfast)
    walk.mark_complete()
    tasks = scheduler.get_all_tasks()

    assert scheduler.filter_tasks(tasks, pet_name="MOCHI") == [walk, dinner]
    assert scheduler.filter_tasks(tasks, completed=True) == [walk]
    assert scheduler.filter_tasks(tasks, pet_name="mochi", completed=False) == [dinner]
    assert scheduler.filter_tasks(tasks) == tasks


# --- Empty cases -----------------------------------------------------------


def test_pet_with_no_tasks_and_empty_day(household):
    _, mochi, luna, scheduler = household
    luna.add_task(Task("feeding", "Breakfast", time(7, 0), DAY))

    assert scheduler.filter_tasks(scheduler.get_all_tasks(), pet_name="Mochi") == []
    assert scheduler.get_todays_tasks(DAY + timedelta(days=1)) == []
    assert scheduler.get_next_task(DAY + timedelta(days=1)) is None
    assert scheduler.detect_conflicts([]) == []


def test_next_task_skips_completed(household):
    _, mochi, _, scheduler = household
    first = Task("walk", "Walk", time(7, 0), DAY)
    second = Task("feeding", "Breakfast", time(8, 0), DAY)
    mochi.add_task(first)
    mochi.add_task(second)

    first.mark_complete()

    assert scheduler.get_next_task(DAY) is second


# --- Data integrity --------------------------------------------------------


def test_duplicate_pet_name_rejected_case_insensitive(household):
    owner, _, _, _ = household

    with pytest.raises(ValueError):
        owner.add_pet(Pet("mochi", "cat"))
    assert len(owner.pets) == 2


def test_task_cannot_belong_to_two_pets(household):
    _, mochi, luna, _ = household
    walk = Task("walk", "Walk", time(8, 0), DAY)
    mochi.add_task(walk)

    with pytest.raises(ValueError):
        luna.add_task(walk)
    assert walk.pet is mochi and luna.tasks == []


def test_identical_looking_tasks_stay_distinct(household):
    _, mochi, _, _ = household
    a = Task("walk", "Walk", time(8, 0), DAY)
    b = Task("walk", "Walk", time(8, 0), DAY)
    mochi.add_task(a)
    mochi.add_task(b)
    mochi.add_task(a)  # repeat add is ignored

    mochi.remove_task(b)

    assert mochi.tasks == [a]
    assert a.pet is mochi and b.pet is None
