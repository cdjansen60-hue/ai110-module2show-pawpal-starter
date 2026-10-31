"""PawPal+ logic layer: owners, pets, care tasks, and the scheduler."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field, replace
from datetime import date, time, timedelta
from enum import StrEnum


class Priority(StrEnum):
    """How important a task is."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Frequency(StrEnum):
    """How often a task repeats."""

    ONCE = "once"
    DAILY = "daily"
    WEEKLY = "weekly"


# How far ahead the next occurrence of a recurring task is scheduled.
RECURRENCE_INTERVALS = {
    Frequency.DAILY: timedelta(days=1),
    Frequency.WEEKLY: timedelta(weeks=1),
}


# eq=False: tasks compare by identity, so two identical-looking tasks stay distinct
# in `in` and list.remove().
@dataclass(eq=False)
class Task:
    """A single pet-care activity scheduled for a date and time."""

    category: str  # e.g. walk, feeding, meds, grooming
    description: str
    start_time: time
    due_date: date = field(default_factory=date.today)
    duration_minutes: int = 15
    priority: Priority = Priority.MEDIUM
    frequency: Frequency = Frequency.ONCE
    completed: bool = False
    # Set by Pet.add_task. Excluded from repr so Pet <-> Task doesn't recurse forever.
    pet: Pet | None = field(default=None, repr=False)

    def mark_complete(self) -> None:
        """Mark this task as done."""
        self.completed = True


@dataclass
class Pet:
    """A pet and the care tasks that belong to it."""

    name: str
    species: str
    age: int = 0
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Attach a task to this pet; ignores repeats, rejects another pet's task."""
        if task.pet is not None and task.pet is not self:
            raise ValueError(f"Task already belongs to {task.pet.name}")
        if task in self.tasks:
            return
        task.pet = self
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Detach a task from this pet."""
        self.tasks.remove(task)  # raises ValueError if it isn't this pet's task
        task.pet = None


@dataclass
class Owner:
    """A pet owner who manages one or more pets."""

    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet, rejecting a name already in use (case-insensitive)."""
        if self.get_pet(pet.name) is not None:
            raise ValueError(f"{self.name} already has a pet named {pet.name!r}")
        self.pets.append(pet)

    def get_pet(self, name: str) -> Pet | None:
        """Return the pet with this name (case-insensitive), or None."""
        for pet in self.pets:
            if pet.name.lower() == name.lower():
                return pet
        return None

    def get_all_tasks(self) -> list[Task]:
        """Return every task across all of this owner's pets."""
        return [task for pet in self.pets for task in pet.tasks]


class Scheduler:
    """Retrieves and organizes tasks across all of an owner's pets."""

    def __init__(self, owner: Owner) -> None:
        """Create a scheduler that reads tasks through the given owner."""
        self.owner = owner

    def get_all_tasks(self) -> list[Task]:
        """Return every task the owner's pets have."""
        return self.owner.get_all_tasks()

    def sort_by_time(self, tasks: list[Task]) -> list[Task]:
        """Return the tasks ordered by date, then start time, earliest first."""
        return sorted(tasks, key=lambda t: (t.due_date, t.start_time))

    def get_todays_tasks(self, day: date | None = None) -> list[Task]:
        """Return tasks due on `day` (default: today), sorted by start time."""
        day = day or date.today()
        return self.sort_by_time([t for t in self.get_all_tasks() if t.due_date == day])

    def get_next_task(self, day: date | None = None) -> Task | None:
        """Return the earliest incomplete task due on `day`, or None."""
        for task in self.get_todays_tasks(day):
            if not task.completed:
                return task
        return None

    def filter_tasks(
        self, tasks: list[Task], pet_name: str | None = None, completed: bool | None = None
    ) -> list[Task]:
        """Return the tasks matching a pet name and/or completion status; None skips that filter."""
        return [
            t
            for t in tasks
            if (pet_name is None or t.pet.name.lower() == pet_name.lower())
            and (completed is None or t.completed == completed)
        ]

    def mark_task_complete(self, task: Task) -> Task | None:
        """Complete a task; for daily/weekly tasks, schedule and return the next occurrence.

        The next due date is counted from the task's own due date (not today), so a
        series never skips or duplicates a day. Completing an already-completed task
        does nothing.
        """
        if task.completed:
            return None
        task.mark_complete()
        interval = RECURRENCE_INTERVALS.get(task.frequency)
        if interval is None:
            return None
        next_task = replace(task, due_date=task.due_date + interval, completed=False, pet=None)
        task.pet.add_task(next_task)
        return next_task

    def detect_conflicts(self, tasks: list[Task]) -> list[str]:
        """Return a warning for each date/time shared by two or more incomplete tasks.

        Only exact start-time matches count; overlapping durations are not checked.
        """
        slots: dict[tuple[date, time], list[Task]] = defaultdict(list)
        for task in tasks:
            if not task.completed:
                slots[(task.due_date, task.start_time)].append(task)

        warnings = []
        for (day, start), clashing in sorted(slots.items()):
            if len(clashing) < 2:
                continue
            names = ", ".join(f"{t.pet.name}: {t.description}" for t in clashing)
            same_pet = len({id(t.pet) for t in clashing}) == 1
            scope = "same pet" if same_pet else "different pets"
            warnings.append(f"Conflict on {day} at {start:%H:%M} [{scope}]: {names}")
        return warnings
