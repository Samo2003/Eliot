from typing import Literal
from ..generators.base import ValueGeneratorBase
from ..generators import ValueGeneratorInt
from .base import GuardBase

class Size(GuardBase[Literal["Size"]]):
    """Guard that checks packet size"""

    # Threshold size
    size: int | ValueGeneratorInt

    # Compare operation
    op: Literal["lt", "le", "eq", "ge", "gt"]

    def cpp_type(self) -> str:
        return f"{self.cpp_type_base()}_{self.size}_{self.op}{'_' + str(id(self)) if self.is_state() else ''}"

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
    
    def is_state(self) -> bool:
        return isinstance(self.size, ValueGeneratorBase) and self.size.is_state()
