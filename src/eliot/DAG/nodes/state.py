from typing import Any
from pydantic import BaseModel, PrivateAttr, model_validator
from eliot.DAG.dag_base_model import DAGBaseModel
from .node import DAGNode

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
        """Assign branch ID used during generating"""
        self._id = value

class StateNode(DAGBaseModel, DAGNode):
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

        - Node ID and state names are normalized to uppercase.
        - Initial state must exist among transitions.
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
