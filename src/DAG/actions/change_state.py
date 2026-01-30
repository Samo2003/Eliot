from typing import Literal, Optional

from pydantic import model_validator
from .base import ActionBase

class ChangeState(ActionBase[Literal["ChangeState"]]):
    """Action that changes state of a given state node by ID reference"""

    # Target state node ID
    target: str

    # State to set
    state: str

    # `StateNode` cpp_type assigned during generating
    state_cpp_type: Optional[str] = None

    @model_validator(mode="after")
    def upper_state(self):
        self.target = self.target.upper()
        self.state = self.state.upper()
        return self

    def cpp_type(self) -> str:
        return f"{self.cpp_type_base()}_{self.target}_{self.state}"
    
    def is_state(self) -> bool:
        return True

    def attach_state_node_type(self, state_cpp_type: str) -> None:
        """Attaches `StateNode` C++ type used for node referencing in generated code"""
        self.state_cpp_type = state_cpp_type
    
    def get_state_cpp_type(self) -> str:
        """Retrieve and validate `StateNode` C++ type was attached"""
        if self.state_cpp_type is None:
            raise RuntimeError(f"StateNode with id: {self.target} not attached to action node")
        return self.state_cpp_type
    
    def init(self) -> str:
        return f" = {self.cpp_type()}({self.get_state_cpp_type().lower()})"
