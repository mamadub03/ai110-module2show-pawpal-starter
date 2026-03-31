from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional


@dataclass
class Owner:
    name: str
    available_minutes: int
    preferences: Dict[str, object] = field(default_factory=dict)
    pets: List[Pet] = field(default_factory=list)

    def update_preferences(self, preferences: Dict[str, object]) -> None:
        """Update owner preferences and merge with existing values."""
        self.preferences.update(preferences)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner."""
        self.pets.append(pet)

    def get_all_tasks(self) -> List[Task]:
        """Retrieve tasks from all owned pets."""
        tasks: List[Task] = []
        for pet in self.pets:
            tasks.extend(pet.tasks)
        return tasks


@dataclass
class Task:
    id: str
    name: str
    duration_minutes: int
    priority: int
    category: Optional[str] = None
    is_required: bool = True
    preferred_time: Optional[str] = None
    done: bool = False

    def as_dict(self) -> Dict[str, object]:
        """Return task data as a dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "duration_minutes": self.duration_minutes,
            "priority": self.priority,
            "category": self.category,
            "is_required": self.is_required,
            "preferred_time": self.preferred_time,
            "done": self.done,
        }

    def update(
        self,
        duration: Optional[int] = None,
        priority: Optional[int] = None,
        preferred_time: Optional[str] = None,
    ) -> None:
        """Update task fields with provided values."""
        if duration is not None:
            self.duration_minutes = duration
        if priority is not None:
            self.priority = priority
        if preferred_time is not None:
            self.preferred_time = preferred_time

    def mark_done(self) -> None:
        """Mark the task as completed."""
        self.done = True


@dataclass
class Pet:
    name: str
    owner: Owner
    species: str
    age: int
    weight: float
    breed: Optional[str] = None
    energy_level: Optional[str] = "normal"
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet."""
        self.tasks.append(task)

    def feed(self) -> Task:
        """Create and add a feeding task."""
        task = Task(
            id=f"{self.name}-feed",
            name="Feed",
            duration_minutes=10,
            priority=1,
            category="care",
        )
        self.add_task(task)
        return task

    def walk(self) -> Task:
        """Create and add a walking task."""
        task = Task(
            id=f"{self.name}-walk",
            name="Walk",
            duration_minutes=30,
            priority=1,
            category="exercise",
        )
        self.add_task(task)
        return task

    def medicate(self) -> Task:
        """Create and add a medicating task."""
        task = Task(
            id=f"{self.name}-medicate",
            name="Medicate",
            duration_minutes=15,
            priority=1,
            category="health",
        )
        self.add_task(task)
        return task

    def groom(self) -> Task:
        """Create and add a grooming task."""
        task = Task(
            id=f"{self.name}-groom",
            name="Groom",
            duration_minutes=20,
            priority=2,
            category="hygiene",
        )
        self.add_task(task)
        return task

    def rest(self) -> Task:
        """Create and add a resting task."""
        task = Task(
            id=f"{self.name}-rest",
            name="Rest",
            duration_minutes=60,
            priority=3,
            category="rest",
        )
        self.add_task(task)
        return task


@dataclass
class Constraints:
    available_minutes: int
    max_tasks: Optional[int] = None
    preferred_times: List[str] = field(default_factory=list)
    blocked_periods: List[Tuple[str, str]] = field(default_factory=list)
    pet_preferences: Dict[str, object] = field(default_factory=dict)

    def is_feasible(self, task: Task) -> bool:
        """Check if a task meets the constraint criteria."""
        if task.done:
            return False
        if task.duration_minutes > self.available_minutes:
            return False
        if self.max_tasks is not None and self.max_tasks <= 0:
            return False
        if self.preferred_times and task.preferred_time and task.preferred_time not in self.preferred_times:
            return False
        return True

    def apply(self, task_list: List[Task]) -> List[Task]:
        """Filter a list of tasks according to constraints."""
        filtered: List[Task] = []
        remaining_minutes = self.available_minutes
        remaining_tasks = self.max_tasks if self.max_tasks is not None else len(task_list)

        for task in task_list:
            if remaining_tasks == 0:
                break
            if task.done:
                continue
            if task.duration_minutes > remaining_minutes:
                continue
            if self.preferred_times and task.preferred_time and task.preferred_time not in self.preferred_times:
                continue
            filtered.append(task)
            remaining_minutes -= task.duration_minutes
            if self.max_tasks is not None:
                remaining_tasks -= 1

        return filtered


@dataclass
class ScheduleEntry:
    task: Task
    start_time: Optional[str] = None
    end_time: Optional[str] = None


@dataclass
class Schedule:
    pet: Optional[Pet] = None
    scheduled_tasks: List[ScheduleEntry] = field(default_factory=list)
    total_duration: int = 0
    explanation: Optional[str] = None

    def add_task(self, entry: ScheduleEntry) -> None:
        """Add an entry to the schedule."""
        self.scheduled_tasks.append(entry)
        self.total_duration += entry.task.duration_minutes

    def remove_task(self, task_id: str) -> None:
        """Remove an entry from the schedule by task ID."""
        new_tasks = []
        new_total = 0
        for entry in self.scheduled_tasks:
            if entry.task.id != task_id:
                new_tasks.append(entry)
                new_total += entry.task.duration_minutes
        self.scheduled_tasks = new_tasks
        self.total_duration = new_total

    def build(self, tasks: List[Task], constraints: Constraints) -> None:
        """Build a schedule from filtered tasks and constraints."""
        self.scheduled_tasks = []
        self.total_duration = 0

        remaining = constraints.available_minutes
        for task in tasks:
            if constraints.is_feasible(task) and not task.done and task.duration_minutes <= remaining:
                self.add_task(ScheduleEntry(task=task))
                remaining -= task.duration_minutes

        self.explanation = f"Built schedule with {len(self.scheduled_tasks)} tasks, using {self.total_duration} minutes."

    def explain(self) -> str:
        """Generate a text explanation of the schedule."""
        lines = [self.explanation or "Schedule explanation:"]
        for entry in self.scheduled_tasks:
            lines.append(f"- {entry.task.name} ({entry.task.duration_minutes}m) - done: {entry.task.done}")
        return "\n".join(lines)


class Scheduler:
    def get_tasks_from_owner(self, owner: Owner) -> List[Task]:
        """Retrieve all tasks from an owner through their pets."""
        return owner.get_all_tasks()

    def generate_plan(self, owner: Owner, constraints: Optional[Constraints] = None) -> Schedule:
        """Generate a schedule plan for an owner with optional constraints."""
        task_list = self.get_tasks_from_owner(owner)
        prioritized = self.prioritize(task_list)
        used_constraints = constraints or Constraints(available_minutes=owner.available_minutes)
        ready_tasks = used_constraints.apply(prioritized)

        schedule = Schedule()
        schedule.build(ready_tasks, used_constraints)
        schedule.explanation = (
            f"Generated plan for owner {owner.name} with {len(schedule.scheduled_tasks)} tasks "
            f"and {schedule.total_duration} total minutes."
        )
        return schedule

    def prioritize(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by completion, requirement, priority, and duration."""
        return sorted(
            tasks,
            key=lambda t: (t.done, not t.is_required, t.priority, t.duration_minutes),
        )

    def fill_day(self, tasks: List[Task], constraints: Constraints) -> List[ScheduleEntry]:
        """Select tasks to fill the day based on constraints."""
        entries: List[ScheduleEntry] = []
        remaining_minutes = constraints.available_minutes
        remaining_tasks = constraints.max_tasks if constraints.max_tasks is not None else len(tasks)

        for task in self.prioritize(tasks):
            if remaining_tasks == 0:
                break
            if not constraints.is_feasible(task):
                continue
            if task.duration_minutes > remaining_minutes:
                continue
            entries.append(ScheduleEntry(task=task))
            remaining_minutes -= task.duration_minutes
            remaining_tasks -= 1

        return entries

    def balance_priority_vs_time(self, tasks: List[Task], constraints: Constraints) -> Schedule:
        """Build schedule balancing priority and available time."""
        sorted_tasks = sorted(
            tasks,
            key=lambda t: (-t.priority, t.duration_minutes),
        )

        schedule = Schedule()
        remaining = constraints.available_minutes

        for task in sorted_tasks:
            if task.done:
                continue
            if task.duration_minutes > remaining:
                continue
            if constraints.max_tasks is not None and len(schedule.scheduled_tasks) >= constraints.max_tasks:
                break
            schedule.add_task(ScheduleEntry(task=task))
            remaining -= task.duration_minutes

        schedule.explanation = (
            "Balanced schedule by selecting highest priority tasks "
            f"within {constraints.available_minutes} available minutes."
        )
        return schedule
