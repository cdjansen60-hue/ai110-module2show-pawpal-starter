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

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

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
