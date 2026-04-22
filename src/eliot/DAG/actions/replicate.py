from __future__ import annotations
from typing import Literal
from pydantic import field_validator
from eliot.DAG.generators import ValueGeneratorInt, ValueGeneratorBase
from .base import ActionBase

class Replicate(ActionBase[Literal["Replicate"]]):
    """
    Replicates packet given amount of times.
    """

    # Number of times to replicate the packet
    n: int | ValueGeneratorInt
    
    @field_validator("n", mode="after")
    @classmethod
    def validate_n(cls, n: int | ValueGeneratorInt) -> int | ValueGeneratorInt:
        if isinstance(n, int):
            if n <= 0:
                raise ValueError("n must be a positive number")
        else:
            if n.min <= 0:
                raise ValueError("n must be a positive number")
        return n
    
    @property
    def cpp_type(self) -> str:
        return (
            f"{self.cpp_type_base}_"
            f"{self.n}"
            f"{'_' + str(id(self)) if isinstance(self.n, ValueGeneratorBase) and self.n.is_state else ''}"
        )
    
    @property
    def is_state(self) -> bool:
        return True

    @property
    def calendar(self) -> bool:
        return True
    
    @property
    def not_generator_n(self) -> bool:
        """Condition used in generating representing if n is a generator"""
        return isinstance(self.n, int)
