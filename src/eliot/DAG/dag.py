from __future__ import annotations
from typing import Any
from pydantic import BaseModel, PrivateAttr, model_validator
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
        if self.action.is_final and self.next is not None:
            raise ValueError("Final action node can't have next")
        if not self.action.is_final and self.next is None:
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

    # Next node for this state
    next: DAGNode

    # Case ID assigned during IR generation
    _id: int | None = PrivateAttr(default=None)
    
    @property
    def id(self) -> int:
        """
        Retrieve assigned case ID.

        Raises:
            RuntimeError if ID has not been attached.
        """
        if self._id is None:
            raise RuntimeError(
                f"Transition ID not attached to transition"
            )
        return self._id
    
    @id.setter
    def id(self, value: int) -> None:
        """Assign branch ID assigned during generating"""
        self._id = value

class StateNode(DAGBaseModel):
    """
    Represents a state node in DAG.
    """

    # Identifier used for ChangeState references
    id: str

    # Initial state of the node
    initial: str

    # Transitions for each defined state
    transitions: dict[str, Transition]

    @model_validator(mode="after")
    def validate_node(self) -> StateNode:
        """
        Validate state node consistency:

        - Transition states must be unique.
        - Initial state must exist among transitions.
        - Node ID and state names are normalized to uppercase.
        """
        self.id = self.id.upper()
        self.initial = self.initial.upper()
        
        # Normalize keys
        new_transitions: dict[str, Transition] = {
            key.upper(): transition
            for key, transition in self.transitions.items()
        }
        self.transitions = new_transitions
        
        if self.initial not in self.transitions:
            raise ValueError(
                f"No transition for initial state fount in node {self.id}"
            )

        return self
    
    @property
    def states(self) -> list[str]:
        """Retrieve list of defined states in `Transition` nodes"""
        return list(self.transitions.keys())
    
    @property
    def is_state(self) -> bool:
        return True
    
    @property
    def cpp_type(self) -> str:
        return f"{self.id.upper()}StateNode"
    
    def attach_transition_ids(self, case: Any) -> None:
        """
        Attach generated case IDs to transitions.

        The provided `case` corresponds to the IR StateCase
        produced during DAG processing.
        """

        # Create state name to Transition map
        state_transition_map: dict[str, int] = {
            state: c["id"]
            for state, c in case["transitions"]
        }

        # Attach branch IDs to Transition nodes
        for state, transition in self.transitions.items():
            transition.id = state_transition_map[state]

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
