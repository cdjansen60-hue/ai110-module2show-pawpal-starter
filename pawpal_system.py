"""PawPal+ logic layer: owners, pets, care tasks, and the scheduler."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date


@dataclass
class Task:
    category: str  # e.g. walk, feeding, meds, grooming
    description: str
    time: str  # "HH:MM", 24-hour
    due_date: date = field(default_factory=date.today)
    duration_minutes: int = 15
    priority: str = "medium"  # low | medium | high
    frequency: str = "once"  # once | daily | weekly
    completed: bool = False

    def mark_complete(self) -> None:
        pass


@dataclass
class Pet:
    name: str
    species: str
    age: int = 0
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        pass

    def remove_task(self, task: Task) -> None:
        pass


@dataclass
class Owner:
    name: str
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        pass

    def get_all_tasks(self) -> list[Task]:
        pass


class Scheduler:
    def __init__(self, owner: Owner) -> None:
        self.owner = owner

    def get_all_tasks(self) -> list[Task]:
        pass

    def get_todays_tasks(self) -> list[Task]:
        pass

    def get_next_task(self) -> Task | None:
        pass
