from typing import Literal

from pydantic import model_validator
from ..generators.base import ValueGeneratorBase
from ..generators import ValueGeneratorInt
from .base import ConditionBase

class Size(ConditionBase[Literal["Size"]]):
    """Condition that checks packet size"""

    # Threshold size
    size: int | ValueGeneratorInt

    # Compare operation
    op: Literal["lt", "le", "eq", "ge", "gt"]

    @model_validator(mode="after")
    def validate_size(self):
        if isinstance(self.size, int) and self.size < 0:
            raise ValueError("Size has to be a positive integer")
        return self

    def cpp_type(self) -> str:
        return f"{self.cpp_type_base()}_{self.size}_{self.op}{'_' + str(id(self)) if isinstance(self.size, ValueGeneratorBase) and self.size.is_state() else ''}"

    def get_op(self) -> str:
        """Maps operation to C++ operator"""
        ops = {
            "lt": "<",
            "le": "<=",
            "eq": "==",
            "ge": ">=",
            "gt": ">"
        }
        return ops[self.op]
    
    def not_generator_size(self) -> bool:
        """Condition used in generating representing if size is a generator"""
        return isinstance(self.size, int)
