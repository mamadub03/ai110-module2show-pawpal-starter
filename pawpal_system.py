from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional


@dataclass
class Owner:
    name: str
    available_minutes: int
    preferences: Dict[str, object] = field(default_factory=dict)

    def update_preferences(self, preferences: Dict[str, object]) -> None:
        pass


@dataclass
class Pet:
    name: str
    owner: Owner
    species: str
    age: int
    weight: float
    breed: Optional[str] = None
    energy_level: Optional[str] = "normal"

    def feed(self) -> None:
        pass

    def walk(self) -> None:
        pass

    def medicate(self) -> None:
        pass

    def groom(self) -> None:
        pass

    def rest(self) -> None:
        pass


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
        pass

    def update(self, duration: Optional[int] = None, priority: Optional[int] = None, preferred_time: Optional[str] = None) -> None:
        pass

    def mark_done(self) -> None:
        pass


@dataclass
class Constraints:
    available_minutes: int
    max_tasks: Optional[int] = None
    preferred_times: List[str] = field(default_factory=list)
    blocked_periods: List[Tuple[str, str]] = field(default_factory=list)
    pet_preferences: Dict[str, object] = field(default_factory=dict)

    def is_feasible(self, task: Task) -> bool:
        pass

    def apply(self, task_list: List[Task]) -> List[Task]:
        pass


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
        pass

    def remove_task(self, task_id: str) -> None:
        pass

    def build(self, tasks: List[Task], constraints: Constraints) -> None:
        pass

    def explain(self) -> str:
        pass


class Scheduler:
    def generate_plan(self, pet: Pet, tasks: List[Task], constraints: Constraints) -> Schedule:
        pass

    def prioritize(self, tasks: List[Task]) -> List[Task]:
        pass

    def fill_day(self, tasks: List[Task], constraints: Constraints) -> List[ScheduleEntry]:
        pass

    def balance_priority_vs_time(self, tasks: List[Task], constraints: Constraints) -> Schedule:
        pass

