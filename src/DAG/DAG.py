from __future__ import annotations
from typing import Any, Dict, List, Optional, Set
from pydantic import BaseModel, model_validator
from .dag_base_model import DAGBaseModel
from .conditions import Condition
from .actions import Action

class ActionNode(BaseModel):
    """Represents an Action node in DAG"""

    # Indicates if action is final
    final: bool = False

    # Contains action to perform
    action: Action

    # Next node in DAG
    next: DAGNode | None = None

    @model_validator(mode="after")
    def check_next_vs_final(self):
        """Final node cannot have next and non final node must have next"""
        if self.final and self.next is not None:
            raise ValueError("Final action node can't have next")
        if not self.final and self.next is None:
            raise ValueError("Non final action node requires next node")
        return self

class DecisionNode(BaseModel):
    """Represents a decision node in DAG"""

    # Contains condition to check
    condition: Condition

    # True branch
    if_true: DAGNode

    # False branch
    if_false: DAGNode

class Transition(BaseModel):
    """Represents a transition node for `StateNone`"""

    # State when the node goes in this branch
    state: str

    # Next node in the branch
    next: DAGNode

    # ID of target case assigned during generation
    id: Optional[int] = None

    @model_validator(mode="after")
    def upper_state(self):
        self.state = self.state.upper()
        return self

    def attach_id(self, id: int) -> None:
        """Assign branch ID assigned during generating"""
        self.id = id

    def get_id(self) -> int:
        """Retrieve and validate branch ID was assigned"""
        if self.id is None:
            raise RuntimeError(f"Transition ID not attached to transition with state: {self.state}")
        return self.id

class StateNode(DAGBaseModel):
    """Represents a state node in DAG"""

    # Node ID used to reference from `ChangeState` action node (has to be unique)
    id: str

    # Node initial state
    initial: str

    # Next nodes based on current state
    transitions: List[Transition]

    @model_validator(mode="after")
    def validate_node(self) -> StateNode:
        used: Set[str] = set()
        for transition in self.transitions:
            if transition.state in used:
                raise ValueError(f"State {transition.state} used multiple times in node {self.id}")
            used.add(transition.state)
        self.id = self.id.upper()
        self.initial = self.initial.upper()
        if self.initial not in used:
            raise ValueError(f"No transition for initial state fount in node {self.id}")

        return self
    
    def states(self) -> List[str]:
        """Retrieve list of defined states in `Transition` nodes"""
        states: List[str] = []
        for transition in self.transitions:
            states.append(transition.state)
        return states
    
    def is_state(self) -> bool:
        return True
    
    def cpp_type(self) -> str:
        return f"{self.id.upper()}StateNode"
    
    def attach_transition_ids(self, case: Any) -> None:
        """Add branch ID to `Transition` nodes for generating"""
        # Any used to fix circular imports case has type `StateCase` from src.DAG.generator.utils

        # Create state name to Transition map
        state_transition_map: Dict[str, int] = {}
        for state, c in case["transitions"]:
            state_transition_map[state] = c["id"]

        # Attach branch IDs to Transition nodes
        for transition in self.transitions:
            transition.attach_id(state_transition_map[transition.state])

# Define DAGNode Union type
DAGNode = ActionNode | DecisionNode | StateNode

class DAG(BaseModel):
    """DAG root container containing Action node, Condition node or State node"""

    # DAG root node
    root: DAGNode
