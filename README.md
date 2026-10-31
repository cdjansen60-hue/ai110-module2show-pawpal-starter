# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
PawPal+ for Jordan -- Saturday, October 31, 2026

Today's Schedule
----------------------------------------------------------------------
  Time   Pet     Category  Task                Min  Priority Done
  07:30  Mochi   walk      Morning walk         30  high     [ ]
  08:00  Luna    feeding   Breakfast            10  high     [ ]
  12:15  Luna    meds      Flea medication       5  high     [ ]
  18:00  Mochi   walk      Evening walk         30  medium   [ ]
  19:30  Luna    grooming  Brush coat           15  low      [ ]

Marked the first task complete. Next up: 08:00 Breakfast (Luna)
```

## 🧪 Testing PawPal+

Run from the project root:

```bash
python -m pytest
```

(Use `python -m pytest`, not bare `pytest`: the `-m` form puts the project root on the import path so the tests can import `pawpal_system`.)

### What the tests cover

The 16 tests in `tests/test_pawpal.py` exercise the backend in `pawpal_system.py`. Every test uses a fixed date (`2026-11-02`) so results don't depend on when they run.

| Area | What is verified |
|---|---|
| Basics | `mark_complete()` flips the status; `add_task()` increases a pet's task count |
| Sorting | Tasks added out of order come back chronologically; across dates, date wins (tomorrow 07:00 sorts after today 18:00) |
| Daily recurrence | Completing a daily task creates an incomplete copy dated +1 day, same time, attached to the same pet |
| Weekly / one-time | Weekly → +7 days; one-time → no copy |
| Double completion | Completing the same task twice creates only one copy |
| Conflict detection | Two tasks at the same date and time give one warning, labeled *same pet* or *different pets* |
| No false conflicts | Same time on different dates, or a completed task, is not a conflict |
| Filtering | By pet (case-insensitive), by status, and both combined |
| Empty cases | A pet with no tasks / an empty day returns `[]`; `get_next_task()` returns `None`; it skips completed tasks |
| Data integrity | Duplicate pet names are rejected (case-insensitive); a task can't belong to two pets; identical-looking tasks stay distinct |

Successful run:

```
============================= test session starts =============================
platform win32 -- Python 3.13.15, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\Caleb\Desktop\School\FAU\CEN4010 - Principles of Software Engineering\week4\ai110-module2show-pawpal-starter
plugins: anyio-4.15.1
collected 16 items

tests\test_pawpal.py ................                                    [100%]

============================= 16 passed in 0.06s ==============================
```

### Confidence level: ★★★★☆ (4/5)

The scheduling logic is well covered, including edge cases. The suite was also checked by deliberately breaking the code (sorting ignoring the date, recurrence counting from today, conflicts counting completed tasks, and others), and every break made at least one test fail. One star is held back because the Streamlit UI (`app.py`) has no automated tests, and conflict detection only catches exact start-time matches, not overlapping durations.

## 📐 Smarter Scheduling

All scheduling logic lives on the `Scheduler` class in `pawpal_system.py`. The methods take and return plain lists of `Task` objects, so they can be chained, e.g. `filter_tasks(sort_by_time(tasks), pet_name="Luna")`.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()` | Orders tasks by due date, then start time. `start_time` is a `datetime.time`, so ordering is always chronological (no `"9:00"` vs `"10:00"` string-sort bug). |
| Today's schedule | `Scheduler.get_todays_tasks()`, `Scheduler.get_next_task()` | Tasks due on a given day (default: today) in time order; the next task is the earliest one not yet completed. |
| Filtering | `Scheduler.filter_tasks()` | Filters by pet name (case-insensitive) and/or completion status. Passing `None` for a filter skips it. |
| Conflict handling | `Scheduler.detect_conflicts()` | Groups incomplete tasks by (date, start time) and returns a warning string for every slot with 2+ tasks, labeled *same pet* or *different pets*. Warns instead of raising. Only exact start-time matches count; overlapping durations are left to the owner. |
| Recurring tasks | `Scheduler.mark_task_complete()` | Completing a `daily` or `weekly` task adds the next occurrence (+1 day / +7 days, via `timedelta`) to the same pet. The next date is counted from the task's due date, so the series never skips or repeats a day. Completing a task twice does nothing. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
