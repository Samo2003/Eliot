from typing import Literal
from .base import GuardBase

class Size(GuardBase[Literal["Size"]]):
    size: int
    op: Literal["lt", "le", "eq", "ge", "gt"]

    def cpp_type(self) -> str:
        return f"{super().cpp_type()}_{self.size}_{self.op}"

    def get_op(self) -> str:
        ops = {
            "lt": "<",
            "le": "<=",
            "eq": "==",
            "ge": ">=",
            "gt": ">"
        }
        return ops[self.op]
