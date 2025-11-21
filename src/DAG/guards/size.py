from typing import Literal
from .base import GuardBase

class Size(GuardBase[Literal["Size"]]):
    """Guard that checks packet size"""

    # Threshold size
    size: int

    # Compare operation
    op: Literal["lt", "le", "eq", "ge", "gt"]

    def cpp_type(self) -> str:
        return f"{self.cpp_type_base()}_{self.size}_{self.op}"

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
