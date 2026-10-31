"""CLI demo: build an owner with pets and tasks, then exercise the scheduler."""

from datetime import date, time, timedelta

from pawpal_system import Frequency, Owner, Pet, Priority, Scheduler, Task


def print_schedule(title: str, tasks: list[Task]) -> None:
    """Print tasks as an aligned table."""
    print(f"\n{title}")
    print("-" * 78)
    if not tasks:
        print("  (no tasks)")
        return
    print(f"  {'Date':<10} {'Time':<5} {'Pet':<6} {'Category':<9} {'Task':<16} {'Min':>3}  "
          f"{'Priority':<8} {'Repeats':<7} Done")
    for t in tasks:
        done = "[x]" if t.completed else "[ ]"
        print(
            f"  {t.due_date:%Y-%m-%d} {t.start_time:%H:%M} {t.pet.name:<6} {t.category:<9} "
            f"{t.description:<16} {t.duration_minutes:>3}  {t.priority:<8} {t.frequency:<7} {done}"
        )


def main() -> None:
    owner = Owner("Jordan")
    mochi = Pet("Mochi", "dog", age=3)
    luna = Pet("Luna", "cat", age=5)
    owner.add_pet(mochi)
    owner.add_pet(luna)

    # Added out of time order on purpose so the schedule shows sorting at work.
    mochi.add_task(Task("walk", "Evening walk", time(18, 0), duration_minutes=30,
                        frequency=Frequency.DAILY))
    luna.add_task(Task("meds", "Flea medication", time(12, 15), duration_minutes=5,
                       priority=Priority.HIGH, frequency=Frequency.WEEKLY))
    mochi.add_task(Task("walk", "Morning walk", time(7, 30), duration_minutes=30,
                        priority=Priority.HIGH, frequency=Frequency.DAILY))
    luna.add_task(Task("feeding", "Breakfast", time(8, 0), duration_minutes=10,
                       priority=Priority.HIGH, frequency=Frequency.DAILY))
    luna.add_task(Task("grooming", "Brush coat", time(19, 30), duration_minutes=15,
                       priority=Priority.LOW))
    # Two tasks booked at the same time, to trigger a conflict warning.
    luna.add_task(Task("vet", "Vet checkup", time(8, 0), duration_minutes=45,
                       priority=Priority.HIGH))

    scheduler = Scheduler(owner)
    today = date.today()
    print(f"PawPal+ for {owner.name} -- {today:%A, %B %d, %Y}")
    print_schedule("Today's Schedule (sorted by time)", scheduler.get_todays_tasks())

    print("\nConflict check")
    print("-" * 78)
    warnings = scheduler.detect_conflicts(scheduler.get_all_tasks())
    for warning in warnings:
        print(f"  WARNING: {warning}")
    if not warnings:
        print("  No conflicts.")

    morning_walk = scheduler.get_next_task()
    new_task = scheduler.mark_task_complete(morning_walk)
    print(f"\nCompleted '{morning_walk.description}' ({morning_walk.frequency}). "
          f"Next occurrence created for {new_task.due_date:%Y-%m-%d}.")
    next_task = scheduler.get_next_task()
    print(f"Next up today: {next_task.start_time:%H:%M} {next_task.description} ({next_task.pet.name})")

    all_sorted = scheduler.sort_by_time(scheduler.get_all_tasks())
    print_schedule("Filter: Luna's tasks", scheduler.filter_tasks(all_sorted, pet_name="Luna"))
    print_schedule("Filter: completed tasks", scheduler.filter_tasks(all_sorted, completed=True))
    print_schedule("Filter: Mochi's incomplete tasks",
                   scheduler.filter_tasks(all_sorted, pet_name="mochi", completed=False))
    print_schedule("Tomorrow's Schedule", scheduler.get_todays_tasks(today + timedelta(days=1)))


if __name__ == "__main__":
    main()
