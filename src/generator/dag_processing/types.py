from __future__ import annotations
from typing import List, Literal, Tuple, TypedDict
from src.DAG import StateNode, Condition, Action

class DecisionCase(TypedDict):
    """Class representing Decision context for generating"""

    id: int
    type: Literal["DecisionCase"]
    condition: Condition
    if_true: Case
    if_false: Case
    path: List[str]
    label: str

class ActionCase(TypedDict):
    """Class representing Action context for generating"""

    id: int
    type: Literal["ActionCase"]
    action: Action
    final: bool
    next: Case | None
    path: List[str]
    label: str

class StateCase(TypedDict):
    """Class representing State context for generating"""

    id: int
    type: Literal["StateCase"]
    state_node: StateNode
    transitions: List[Tuple[str, Case]]
    path: List[str]
    label: str

Case = DecisionCase | ActionCase | StateCase
