from __future__ import annotations
from typing import Literal
from pydantic import field_validator
from eliot.DAG.generators import ValueGeneratorBase, ValueGeneratorInt
from .base import ConditionBase

class Size(ConditionBase[Literal["Size"]]):
    """
    Condition that checks packet size
    """

    # Threshold size
    size: int | ValueGeneratorInt

    # Compare operation
    op: Literal["lt", "le", "eq", "ge", "gt"]

    @field_validator("size", mode="after")
    @classmethod
    def validate_size(cls, size: int | ValueGeneratorInt) -> int | ValueGeneratorInt:
        if isinstance(size, int) and size < 0:
            raise ValueError("size has to be a positive integer")
        return size

    @property
    def cpp_type(self) -> str:
        return (
            f"{self.cpp_type_base}_"
            f"{self.size}_"
            f"{self.op}"
            f"{'_' + str(id(self)) if isinstance(self.size, ValueGeneratorBase) and self.size.is_state else ''}"
        )

    @property
    def op_str(self) -> str:
        """Maps operation to C++ operator"""
        ops = {
            "lt": "<",
            "le": "<=",
            "eq": "==",
            "ge": ">=",
            "gt": ">"
        }
        return ops[self.op]
    
    @property
    def not_generator_size(self) -> bool:
        """Condition used in generating representing if size is a generator"""
        return isinstance(self.size, int)
