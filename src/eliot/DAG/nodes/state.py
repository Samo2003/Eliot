from typing import Any
from pydantic import PrivateAttr, model_validator
from eliot.DAG.dag_base_model import DAGBaseModel
from .node import DAGNode

class StateNode(DAGBaseModel, DAGNode):
    """
    Represents a state node in DAG.
    """

    # Identifier used for SetState references
    id: str

    # Initial state of the node
    initial: str

    # Transitions for each defined state
    transitions: dict[str, DAGNode]
    
    # Maps state to transition id
    _state_map: dict[str, int] = PrivateAttr(default={})

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
        new_transitions: dict[str, DAGNode] = {
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
        """Retrieve list of defined states"""
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
        
        self._state_map = {
            state: c["id"]
            for state, c in case["transitions"]
        }
