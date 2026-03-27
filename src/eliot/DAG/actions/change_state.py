from __future__ import annotations
from typing import Literal
from pydantic import PrivateAttr, model_validator
from .base import ActionBase

class ChangeState(ActionBase[Literal["ChangeState"]]):
    """
    Action that changes state of a given state node by ID reference.
    s"""

    # Target state node ID
    target: str

    # State to set
    state: str

    # `StateNode` cpp_type assigned during generating
    _state_cpp_type: str | None = PrivateAttr(default=None)

    @model_validator(mode="after")
    def upper_state(self) -> ChangeState:
        self.target = self.target.upper()
        self.state = self.state.upper()
        return self

    @property
    def cpp_type(self) -> str:
        return f"{self.cpp_type_base}_{self.target}_{self.state}"
    
    @property
    def is_state(self) -> bool:
        return True

    @property
    def state_cpp_type(self) -> str:
        """Retrieve and validate `StateNode` C++ type was attached"""
        if self._state_cpp_type is None:
            raise RuntimeError(f"StateNode with id: {self.target} not attached to action node")
        return self._state_cpp_type

    @state_cpp_type.setter
    def state_cpp_type(self, state_cpp_type: str) -> None:
        """Attaches `StateNode` C++ type used for node referencing in generated code"""
        self._state_cpp_type = state_cpp_type
    
    @property
    def init(self) -> str:
        return f" = {self.cpp_type}({self.state_cpp_type.lower()})"
