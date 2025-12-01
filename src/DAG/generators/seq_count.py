from abc import ABC
from pydantic import model_validator
from typing import Literal
from .base import ValueGeneratorBase, T, N

class SeqCountBase(ValueGeneratorBase[T, N], ABC):
    """Abstract sequential count generator base"""

    # Number of steps required to reach next value
    T: int = 1

    # Step size
    step: N

    # Handling reached max or min value
    mode: Literal["repeat", "keep", "reverse"]

    @model_validator(mode="after")
    def check_consistency(self):
        """Validates consistency"""
        if self.step > 0 and self.min is None:
            raise ValueError("min is required for increasing sequence (step > 0)")
        if self.step < 0 and self.max is None:
            raise ValueError("max is required for decreasing sequence (step < 0)")

        return self
    
class SeqCountFloat(SeqCountBase[Literal["SeqCountFloat"], float]):
    """Sequential count float value generator"""
    pass

class SeqCountInt(SeqCountBase[Literal["SeqCountInt"], int]):
    """Sequential count int value generator"""
    pass
