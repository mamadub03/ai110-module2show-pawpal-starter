# -*- coding: utf-8 -*-
import streamlit as st
from pawpal_system import Owner, Pet, Task, Constraints, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to the PawPal+ starter app.

This file is intentionally thin. It gives you a working Streamlit app so you can start quickly,
but **it does not implement the project logic**. Your job is to design the system and build it.

Use this app as your interactive demo once your backend classes/functions exist.
"""
)

if "owner" not in st.session_state:
    st.session_state.owner = Owner(name="Jordan", available_minutes=240)

if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler()

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.
"""
    )

with st.expander("What you need to build", expanded=True):
    st.markdown(
        """
At minimum, your system should:
- Represent pet care tasks (what needs to happen, how long it takes, priority)
- Represent the pet and the owner (basic info and preferences)
- Build a plan/schedule for a day that chooses and orders tasks based on constraints
- Explain the plan (why each task was chosen and when it happens)
"""
    )

st.divider()

st.subheader("Quick Demo Inputs")

owner = st.session_state.owner

st.markdown(f"**Owner**: {owner.name} | **Available minutes**: {owner.available_minutes}")

with st.form(key="add_pet_form"):
    col1, col2 = st.columns(2)
    with col1:
        pet_name = st.text_input("Pet name", value="Mochi")
    with col2:
        species = st.selectbox("Species", ["dog", "cat", "other"])

    age = st.number_input("Age", min_value=0, max_value=30, value=2)
    weight = st.number_input("Weight (kg)", min_value=0.1, max_value=100.0, value=4.5)

    if st.form_submit_button("Add pet"):
        new_pet = Pet(name=pet_name, owner=owner, species=species, age=int(age), weight=float(weight))
        owner.add_pet(new_pet)
        st.success(f"Added pet '{new_pet.name}'")

pet_names = [pet.name for pet in owner.pets]

if pet_names:
    selected_pet_name = st.selectbox("Select pet to assign task", pet_names)
    selected_pet = next((p for p in owner.pets if p.name == selected_pet_name), None)

    with st.form(key="add_task_form"):
        task_name = st.text_input("Task title", value="Morning walk")
        duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
        priority_value = st.selectbox("Priority", ["low", "medium", "high"], index=2)

        if st.form_submit_button("Add task"):
            if selected_pet is not None:
                priority_map = {"low": 3, "medium": 2, "high": 1}
                priority_int = priority_map.get(priority_value, 2)
                task = Task(
                    id=f"{selected_pet.name}-{len(selected_pet.tasks)+1}",
                    name=task_name,
                    duration_minutes=int(duration),
                    priority=priority_int,
                    preferred_time=None,
                )
                selected_pet.add_task(task)
                st.success(f"Added task '{task.name}' to {selected_pet.name}")
else:
    st.info("Add a pet first to assign tasks.")

st.divider()

st.subheader("Pet Tasks")

for pet in owner.pets:
    st.write(f"**{pet.name}** ({pet.species})")
    if pet.tasks:
        for t in pet.tasks:
            st.write(f"- {t.name}, {t.duration_minutes} min, priority {t.priority}, done={t.done}")
    else:
        st.write("- No tasks yet.")

st.divider()

st.subheader("Build Schedule")

available_minutes = st.number_input("Total available minutes for schedule", min_value=1, max_value=1440, value=owner.available_minutes)
max_tasks = st.number_input("Max tasks", min_value=1, max_value=50, value=10)

if st.button("Generate schedule"):
    constraints = Constraints(available_minutes=int(available_minutes), max_tasks=int(max_tasks), preferred_times=[])
    schedule = st.session_state.scheduler.generate_plan(owner, constraints=constraints)
    st.success("Schedule generated")
    st.markdown("### Today's Schedule")
    st.text(schedule.explain())

    for entry in schedule.scheduled_tasks:
        st.write(f"- {entry.task.name} ({entry.task.duration_minutes}m) [{entry.task.priority}]")
