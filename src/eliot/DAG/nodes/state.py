from __future__ import annotations
from typing import Any
from pydantic import PrivateAttr, field_validator, model_validator
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
    
    @field_validator("id", mode="after")
    @classmethod
    def validate_id(cls, id: str) -> str:
        if id != id.upper():
            raise ValueError("id has to be upper case")
        return id
    
    @field_validator("initial", mode="after")
    @classmethod
    def validate_initial(cls, initial: str) -> str:
        if initial != initial.upper():
            raise ValueError("initial has to be upper case")
        return initial
    
    @field_validator("transitions", mode="after")
    @classmethod
    def validate_transitions(cls, transitions: dict[str, DAGNode]) -> dict[str, DAGNode]:
        for key in transitions.keys():
            if key != key.upper():
                raise ValueError("state values have to be upper case")
        return transitions

    @model_validator(mode="after")
    def validate_node(self) -> StateNode:
        """
        Validates state node contains transition for initial state.
        """
        if self.initial not in self.transitions:
            raise ValueError(
                f"no transition for initial state fount in node {self.id}"
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
