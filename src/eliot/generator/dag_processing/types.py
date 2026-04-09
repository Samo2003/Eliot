from __future__ import annotations
from typing import Literal, TypedDict
from eliot.DAG import StateNode, Condition, Action

class CaseBase(TypedDict):
    """
    Base structure for all execution cases in the intermediate
    representation derived from the DAG.
    """
    
    id: int                             # Unique identifier of this case
    path: list[str]                     # Logical path in DAG for generating comments
    label: str                          # Node label for generating comments

class DecisionCase(CaseBase):
    """
    Represents a decision node in the flattened execution model.
    """

    type: Literal["DecisionCase"]       # Discriminator for runtime/code generation
    condition: Condition                # Condition being evaluated
    if_true: Case                       # Case executed if condition evaluates to true
    if_false: Case                      # Case executed if condition evaluates to false

class ActionCase(CaseBase):
    """
    Represents an executable action in the flattened execution model.
    """

    type: Literal["ActionCase"]         # Discriminator for runtime/code generation
    action: Action                      # Action to be executed
    final: bool                         # Indicates whether execution terminates here
    next: Case | None                   # Optional continuation case

class StateCase(CaseBase):
    """
    Represents a state machine node in the flattened execution model.

    Each StateCase encapsulates state transitions and
    links them to corresponding cases.
    """

    type: Literal["StateCase"]          # Discriminator for runtime/code generation
    state_node: StateNode               # Associated state definition
    transitions: list[tuple[str, Case]] # Each transition maps a state name to the next case

# Unified type used throughout generation pipeline
Case = DecisionCase | ActionCase | StateCase
