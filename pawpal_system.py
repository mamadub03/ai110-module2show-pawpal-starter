from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Dict, Tuple, Optional


@dataclass
class Pet:
    name: str
    owner: str
    species: str
    age: int
    weight: float
    breed: Optional[str] = None
    energy_level: Optional[str] = "normal"

    def feed(self) -> str:
        # TODO: implement feed behavior
        pass

    def walk(self) -> str:
        # TODO: implement walk behavior
        pass

    def medicate(self) -> str:
        # TODO: implement medicate behavior
        pass

    def groom(self) -> str:
        # TODO: implement groom behavior
        pass

    def rest(self) -> str:
        # TODO: implement rest behavior
        pass


@dataclass
class Task:
    id: str
    name: str
    duration_minutes: int
    priority: int
    type: Optional[str] = None
    is_required: bool = True
    preferred_time: Optional[str] = None
    done: bool = False

    def as_dict(self) -> Dict[str, object]:
        # TODO: return serializable representation
        pass

    def update(self, duration: Optional[int] = None, priority: Optional[int] = None, preferred_time: Optional[str] = None) -> None:
        # TODO: update task fields
        pass

    def mark_done(self) -> None:
        # TODO: set task completion state
        pass


@dataclass
class Constraints:
    available_minutes: int
    max_tasks: Optional[int] = None
    preferred_times: List[str] = field(default_factory=list)
    blocked_periods: List[Tuple[str, str]] = field(default_factory=list)
    pet_preferences: Dict[str, object] = field(default_factory=dict)

    def is_feasible(self, task: Task) -> bool:
        # TODO: check if task can be fit
        pass

    def apply(self, task_list: List[Task]) -> List[Task]:
        # TODO: apply constraints and return filtered list
        pass


@dataclass
class Schedule:
    scheduled_tasks: List[Task] = field(default_factory=list)
    total_duration: int = 0
    explanation: Optional[str] = None

    def add_task(self, task: Task) -> None:
        # TODO: add and recalc total_duration
        pass

    def remove_task(self, task_id: str) -> None:
        # TODO: remove by id and recalc
        pass

    def build(self, tasks: List[Task], constraints: Constraints) -> None:
        # TODO: generate schedule from tasks plus constraints
        pass

    def explain(self) -> str:
        # TODO: generate reasoning string
        pass


class Scheduler:
    def generate_plan(self, tasks: List[Task], constraints: Constraints) -> Schedule:
        # TODO: prioritize tasks and fill schedule
        return Schedule()

    def prioritize(self, tasks: List[Task]) -> List[Task]:
        # TODO: order tasks by priority, required and duration
        return []

    def fill_day(self, tasks: List[Task], constraints: Constraints) -> List[Task]:
        # TODO: fit tasks under constraints
        return []

    def balance_priority_vs_time(self, tasks: List[Task], constraints: Constraints) -> Schedule:
        # TODO: resolve trade-offs and build final plan
        return Schedule()
