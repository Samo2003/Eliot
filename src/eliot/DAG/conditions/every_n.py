from __future__ import annotations
from typing import Literal
from pydantic import field_validator
from eliot.DAG.generators import ValueGeneratorInt
from .base import ConditionBase

class EveryN(ConditionBase[Literal["EveryN"]]):
    """
    Condition that is fulfilled for every nth packet
    """

    # Every `N`th packet the condition is fulfilled
    N: int | ValueGeneratorInt

    @field_validator("N", mode="after")
    @classmethod
    def validate_n(cls, N: int | ValueGeneratorInt) -> int | ValueGeneratorInt:
        if isinstance(N, int) and N < 0:
            raise ValueError("after must not be negative")
        return N

    @property
    def cpp_type(self) -> str:
        return f"{self.cpp_type_base}_{self.N}_{id(self)}"
    
    @property
    def is_state(self) -> bool:
        return True
    
    @property
    def not_generator_N(self) -> bool:
        """Condition used in generating representing if N is a generator"""
        return isinstance(self.N, int)
