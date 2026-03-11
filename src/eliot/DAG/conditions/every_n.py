from __future__ import annotations
from typing import Literal
from pydantic import model_validator
from eliot.DAG.generators import ValueGeneratorInt
from .base import ConditionBase

class EveryN(ConditionBase[Literal["EveryN"]]):
    """
    Condition that is fulfilled for every nth packet
    """

    # Every `N`th packet the condition is fulfilled
    N: int | ValueGeneratorInt

    @model_validator(mode="after")
    def validate_n(self) -> EveryN:
        if isinstance(self.N, int) and self.N < 0:
            raise ValueError("after must not be negative")
        return self

    def cpp_type(self) -> str:
        return f"{self.cpp_type_base()}_{self.N}_{id(self)}"
    
    def is_state(self) -> bool:
        return True
    
    def not_generator_N(self) -> bool:
        """Condition used in generating representing if N is a generator"""
        return isinstance(self.N, int)
