from abc import ABC
from pydantic import model_validator
from typing import Literal, final
from .base import ValueGeneratorBase, T, N

class SeqCountBase(ValueGeneratorBase[T, N], ABC):
    """Abstract sequential count generator base"""

    # Number of steps required to reach next value
    T: int = 1

    # Step size
    step: N

    # Handling reached max or min value
    mode: Literal["repeat", "keep", "reverse"] = "keep"

    @model_validator(mode="after")
    def check_consistency(self):
        """Validates consistency"""
        if self.step == 0:
            raise ValueError("step must be none zero")
        if self.step > 0 and self.min is None:
            raise ValueError("min is required for increasing sequence (step > 0)")
        if self.step < 0 and self.max is None:
            raise ValueError("max is required for decreasing sequence (step < 0)")
        if self.T <= 0:
            raise ValueError("T must be >= 1")

        return self
    
    @final
    def cpp_type(self) -> str:
        return f"{super().cpp_type_base()}_{self.T}_{self.N_to_int_str(self.step)}_{self.mode.upper()}_{self.once}"
    
    @final
    def is_state(self) -> bool:
        return not self.once
    
class SeqCountFloat(SeqCountBase[Literal["SeqCountFloat"], float]):
    """Sequential count float value generator"""
    
    def value(self) -> float:
        if self.step < 0:
            return self.max if self.max is not None else 0
        return self.min if self.min is not None else 0

class SeqCountInt(SeqCountBase[Literal["SeqCountInt"], int]):
    """Sequential count int value generator"""
    
    def value(self) -> int:
        if self.step < 0:
            return self.max if self.max is not None else 0
        return self.min if self.min is not None else 0
