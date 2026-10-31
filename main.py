"""CLI demo: build an owner with pets and tasks, then print today's schedule."""

from datetime import date, time

from pawpal_system import Frequency, Owner, Pet, Priority, Scheduler, Task


def print_schedule(title: str, tasks: list[Task]) -> None:
    """Print tasks as an aligned table."""
    print(f"\n{title}")
    print("-" * 70)
    if not tasks:
        print("  (no tasks)")
        return
    print(f"  {'Time':<6} {'Pet':<7} {'Category':<9} {'Task':<18} {'Min':>4}  {'Priority':<8} Done")
    for t in tasks:
        done = "[x]" if t.completed else "[ ]"
        print(
            f"  {t.start_time:%H:%M}  {t.pet.name:<7} {t.category:<9} {t.description:<18} "
            f"{t.duration_minutes:>4}  {t.priority:<8} {done}"
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

    scheduler = Scheduler(owner)
    print(f"PawPal+ for {owner.name} -- {date.today():%A, %B %d, %Y}")
    print_schedule("Today's Schedule", scheduler.get_todays_tasks())

    scheduler.get_todays_tasks()[0].mark_complete()
    next_task = scheduler.get_next_task()
    print("\nMarked the first task complete. Next up: ", end="")
    if next_task:
        print(f"{next_task.start_time:%H:%M} {next_task.description} ({next_task.pet.name})")
    else:
        print("nothing left today!")


if __name__ == "__main__":
    main()
