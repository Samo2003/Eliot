from __future__ import annotations
from typing import Any, Dict, List, Set
from pydantic import BaseModel, model_validator
from .dag_base_model import DAGBaseModel
from .conditions import Condition
from .actions import Action

class ActionNode(BaseModel):
    """
    Represents an executable action node in the DAG.

    ActionNode encapsulates a concrete Action instance and optionally
    references the next node in the execution chain.
    """

    # Action to be executed
    action: Action

    # Continuation node (None only if action is final)
    next: DAGNode | None = None

    @model_validator(mode="after")
    def check_next_vs_final(self) -> ActionNode:
        """
        Enforce structural invariant:

        - Final actions must NOT have a next node.
        - Non-final actions MUST have a next node.
        """
        if self.action.is_final() and self.next is not None:
            raise ValueError("Final action node can't have next")
        if not self.action.is_final() and self.next is None:
            raise ValueError("Non final action node requires next node")
        return self

class DecisionNode(BaseModel):
    """
    Represents a conditional branching node in the DAG.

    A DecisionNode evaluates a Condition and selects one of two branches.
    """

    # Condition to evaluate
    condition: Condition

    # Branch taken if condition evaluates to true
    if_true: DAGNode

    # Branch taken if condition evaluates to false
    if_false: DAGNode

class Transition(BaseModel):
    """
    Represents a single transition in a StateNode.

    Each transition maps a state name to the next DAG node.
    During generation, a unique case ID is attached for
    switch-based dispatch.
    """

    # State triggering this transition
    state: str

    # Next node for this state
    next: DAGNode

    # Case ID assigned during IR generation
    id: int | None = None

    @model_validator(mode="after")
    def upper_state(self) -> Transition:
        """
        Normalize state identifier to uppercase
        to ensure case-insensitive consistency.
        """
        self.state = self.state.upper()
        return self

    def attach_id(self, id: int) -> None:
        """Assign branch ID assigned during generating"""
        self.id = id

    def get_id(self) -> int:
        """
        Retrieve assigned case ID.

        Raises:
            RuntimeError if ID has not been attached.
        """
        if self.id is None:
            raise RuntimeError(
                f"Transition ID not attached to transition with state: {self.state}"
            )
        return self.id

class StateNode(DAGBaseModel):
    """
    Represents a state node in DAG.
    """

    # Identifier used for ChangeState references
    id: str

    # Initial state of the node
    initial: str

    # Transitions for each defined state
    transitions: List[Transition]

    @model_validator(mode="after")
    def validate_node(self) -> StateNode:
        """
        Validate state node consistency:

        - Transition states must be unique.
        - Initial state must exist among transitions.
        - Node ID and state names are normalized to uppercase.
        """
        used: Set[str] = set()
        for transition in self.transitions:
            if transition.state in used:
                raise ValueError(
                    f"State {transition.state} used multiple times in node {self.id}"
                )
            used.add(transition.state)
        self.id = self.id.upper()
        self.initial = self.initial.upper()
        if self.initial not in used:
            raise ValueError(
                f"No transition for initial state fount in node {self.id}"
            )

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
        """
        Attach generated case IDs to transitions.

        The provided `case` corresponds to the IR StateCase
        produced during DAG processing.
        """

        # Create state name to Transition map
        state_transition_map: Dict[str, int] = {}
        for state, c in case["transitions"]:
            state_transition_map[state] = c["id"]

        # Attach branch IDs to Transition nodes
        for transition in self.transitions:
            transition.attach_id(state_transition_map[transition.state])

# Union type representing any valid DAG node
DAGNode = ActionNode | DecisionNode | StateNode

class DAG(BaseModel):
    """
    Root container for the DAG specification.

    The root node may be:
    - an ActionNode,
    - a DecisionNode,
    - or a StateNode.
    """

    # DAG root node
    root: DAGNode
