from datetime import date, time

import streamlit as st

from pawpal_system import Frequency, Owner, Pet, Priority, Scheduler, Task

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

with st.expander("Scenario", expanded=False):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.
"""
    )

# Streamlit reruns this script on every interaction, so the Owner lives in
# session_state. Pets and tasks hang off the Owner; nothing else is stored.
if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan")
owner: Owner = st.session_state.owner
scheduler = Scheduler(owner)

owner.name = st.text_input("Owner name", value=owner.name)

st.divider()

st.subheader("Add a Pet")
with st.form("add_pet", clear_on_submit=True):
    col1, col2, col3 = st.columns([2, 2, 1])
    with col1:
        pet_name = st.text_input("Pet name")
    with col2:
        species = st.text_input("Species", placeholder="dog, cat, rabbit...")
    with col3:
        age = st.number_input("Age", min_value=0, max_value=50, value=0)
    if st.form_submit_button("Add pet"):
        if not pet_name.strip() or not species.strip():
            st.error("Pet name and species are required.")
        else:
            try:
                owner.add_pet(Pet(pet_name.strip(), species.strip(), int(age)))
                st.success(f"Added {pet_name.strip()}.")
            except ValueError as e:
                st.error(str(e))

if owner.pets:
    st.caption("Pets: " + ", ".join(f"{p.name} ({p.species}, {p.age})" for p in owner.pets))

st.divider()

st.subheader("Schedule a Task")
if not owner.pets:
    st.info("Add a pet first.")
else:
    with st.form("add_task", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            pet_choice = st.selectbox("Pet", [p.name for p in owner.pets])
            category = st.text_input("Category", placeholder="walk, feeding, meds...")
            description = st.text_input("Description", placeholder="Morning walk")
            duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=15)
        with col2:
            due_date = st.date_input("Date", value=date.today())
            start_time = st.time_input("Start time", value=time(8, 0))
            priority = st.selectbox("Priority", list(Priority), index=1)
            frequency = st.selectbox("Repeats", list(Frequency))
        if st.form_submit_button("Add task"):
            if not category.strip() or not description.strip():
                st.error("Category and description are required.")
            else:
                owner.get_pet(pet_choice).add_task(
                    Task(
                        category.strip(),
                        description.strip(),
                        start_time,
                        due_date=due_date,
                        duration_minutes=int(duration),
                        priority=priority,
                        frequency=frequency,
                    )
                )
                st.success(f"Scheduled {description.strip()} for {pet_choice}.")

st.divider()

st.subheader("Schedule")
day = st.date_input("Show schedule for", value=date.today())
tasks = scheduler.get_todays_tasks(day)

if not tasks:
    st.info("No tasks scheduled for this day.")
else:
    st.table(
        [
            {
                "Time": f"{t.start_time:%H:%M}",
                "Pet": t.pet.name,
                "Category": t.category,
                "Task": t.description,
                "Minutes": t.duration_minutes,
                "Priority": t.priority.value,
                "Repeats": t.frequency.value,
                "Done": "✓" if t.completed else "",
            }
            for t in tasks
        ]
    )
    next_task = scheduler.get_next_task(day)
    if next_task:
        st.info(f"Next up: {next_task.start_time:%H:%M} {next_task.description} ({next_task.pet.name})")
    else:
        st.success("Everything on this day is done!")
