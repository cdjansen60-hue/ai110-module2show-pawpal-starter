# PawPal+ (Module 2 Project)

**PawPal+** is a pet-care planner for a busy owner with one or more pets. It tracks care tasks (walks, feeding, medication, vet visits, grooming), builds each day's schedule in time order, repeats daily and weekly tasks automatically, and warns when two tasks are booked at the same time.

## ✨ Features

- **Multiple pets per owner.** Pet names are unique (case-insensitive), so "Mochi" and "mochi" can't both exist.
- **Rich tasks.** Each task has a category, a description, a date, a start time, a duration, a priority (low/medium/high), and a frequency (once/daily/weekly).
- **Sorting by time.** Schedules are always chronological, ordered by date and then start time.
- **Daily schedule and "next up".** View any day's tasks and see the earliest one that isn't done yet.
- **Filtering.** Narrow the schedule by pet, by status (to do / done), or both.
- **Daily and weekly recurrence.** Completing a recurring task automatically schedules its next occurrence (+1 day or +7 days).
- **Conflict warnings.** Tasks booked at the same date and time are flagged, labeled *same pet* or *different pets*. They're shown as warnings, so the app never crashes or blocks you.
- **Session memory.** The Streamlit app keeps your owner, pets, and tasks while the browser session is open.

## 🚀 Getting started

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

streamlit run app.py   # the web app
python main.py         # CLI demo of the backend
python -m pytest       # test suite
```

## 🗂️ Project structure

| File | Purpose |
|---|---|
| `pawpal_system.py` | Logic layer: `Owner`, `Pet`, `Task`, `Scheduler`, and the `Priority` / `Frequency` enums |
| `app.py` | Streamlit UI; stores the `Owner` in `st.session_state` and calls the classes above |
| `main.py` | CLI demo that exercises every scheduler feature |
| `tests/test_pawpal.py` | pytest suite (16 tests) |
| `diagrams/uml_final.mmd` | Final UML class diagram (Mermaid). `diagrams/uml.mmd` is the working copy, and its git history shows how it changed from the first draft |
| `reflection.md` | Design and AI-collaboration reflection |

## 📸 Demo Walkthrough

### What you can do in the app

1. **Name the owner** at the top of the page. The name defaults to "Jordan".
2. **Add a pet** with a name, a species, and an age. Adding a duplicate name shows an error instead of creating a second pet.
3. **Schedule a task.** Pick the pet and enter the category, description, date, start time, duration, priority, and how often it repeats. The pet list comes from the pets you've added.
4. **View the schedule** for any date. The default is today, and the tasks are shown in a table sorted by time.
5. **Filter** the schedule by pet and by status (All / To do / Done).
6. **Read the conflict warnings.** They appear above the table for any two tasks at the same time on the selected day. They are checked on the whole day, so a filter can never hide one.
7. **Mark a task complete** from the "Task to complete" dropdown. A ✓ appears, "Next up" moves to the next task, and for a daily or weekly task a message confirms when the next occurrence is scheduled.

### Example workflow

1. Add **Mochi** (dog, 3) and **Luna** (cat, 5).
2. Schedule Mochi's *Morning walk* at 07:30 (daily), Luna's *Breakfast* at 08:00 (daily), and Luna's *Vet checkup* at 08:00 (once).
3. Open today's schedule. The tasks are listed 07:30 → 08:00 → 08:00, and a warning says Luna has two tasks at 08:00.
4. Mark *Morning walk* complete. It gets a ✓, "Next up" changes to *Breakfast*, and the message says the next walk is scheduled for tomorrow.
5. Switch the date to tomorrow. The new *Morning walk* is already there.

### Key scheduler behaviors shown

- **Sorting:** tasks are entered out of order and displayed chronologically (`sort_by_time`).
- **Conflict warnings:** two 08:00 tasks for Luna are flagged (`detect_conflicts`).
- **Recurrence:** completing a daily task creates tomorrow's copy (`mark_task_complete`).
- **Filtering:** by pet, by status, and both combined (`filter_tasks`).

### 🖥️ Sample Output

Output of `python main.py`. The tasks are added out of order on purpose, and Luna has two tasks at 08:00.

```
PawPal+ for Jordan -- Saturday, October 31, 2026

Today's Schedule (sorted by time)
------------------------------------------------------------------------------
  Date       Time  Pet    Category  Task             Min  Priority Repeats Done
  2026-10-31 07:30 Mochi  walk      Morning walk      30  high     daily   [ ]
  2026-10-31 08:00 Luna   feeding   Breakfast         10  high     daily   [ ]
  2026-10-31 08:00 Luna   vet       Vet checkup       45  high     once    [ ]
  2026-10-31 12:15 Luna   meds      Flea medication    5  high     weekly  [ ]
  2026-10-31 18:00 Mochi  walk      Evening walk      30  medium   daily   [ ]
  2026-10-31 19:30 Luna   grooming  Brush coat        15  low      once    [ ]

Conflict check
------------------------------------------------------------------------------
  WARNING: Conflict on 2026-10-31 at 08:00 [same pet]: Luna: Breakfast, Luna: Vet checkup

Completed 'Morning walk' (daily). Next occurrence created for 2026-11-01.
Next up today: 08:00 Breakfast (Luna)

Filter: Luna's tasks
------------------------------------------------------------------------------
  Date       Time  Pet    Category  Task             Min  Priority Repeats Done
  2026-10-31 08:00 Luna   feeding   Breakfast         10  high     daily   [ ]
  2026-10-31 08:00 Luna   vet       Vet checkup       45  high     once    [ ]
  2026-10-31 12:15 Luna   meds      Flea medication    5  high     weekly  [ ]
  2026-10-31 19:30 Luna   grooming  Brush coat        15  low      once    [ ]

Filter: completed tasks
------------------------------------------------------------------------------
  Date       Time  Pet    Category  Task             Min  Priority Repeats Done
  2026-10-31 07:30 Mochi  walk      Morning walk      30  high     daily   [x]

Filter: Mochi's incomplete tasks
------------------------------------------------------------------------------
  Date       Time  Pet    Category  Task             Min  Priority Repeats Done
  2026-10-31 18:00 Mochi  walk      Evening walk      30  medium   daily   [ ]
  2026-11-01 07:30 Mochi  walk      Morning walk      30  high     daily   [ ]

Tomorrow's Schedule
------------------------------------------------------------------------------
  Date       Time  Pet    Category  Task             Min  Priority Repeats Done
  2026-11-01 07:30 Mochi  walk      Morning walk      30  high     daily   [ ]
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
