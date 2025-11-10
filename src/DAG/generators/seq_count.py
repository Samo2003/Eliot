from abc import ABC
from pydantic import model_validator
from typing import Literal
from .base import ValueGeneratorBase, T, N

class SeqCountBase(ValueGeneratorBase[T, N], ABC):
    T: int = 1
    step: N
    mode: Literal["repeat", "keep", "reverse"]

    @model_validator(mode="after")
    def check_consistency(self):
        if self.step > 0 and self.min is None:
            raise ValueError("min is required for increasing sequence (step > 0)")
        if self.step < 0 and self.max is None:
            raise ValueError("max is required for decreasing sequence (step < 0)")

        return self
    
class SeqCountInt(SeqCountBase[Literal["SeqCountInt"], int]):
    pass

class SeqCountFloat(SeqCountBase[Literal["SeqCountFloat"], float]):
    pass
