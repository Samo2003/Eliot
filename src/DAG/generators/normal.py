from abc import ABC
from typing import Literal, final
from pydantic import model_validator
from .base import ValueGeneratorBase, T, N
import random

class NormalBase(ValueGeneratorBase[T, N], ABC):
    """Abstract normal generator base"""

    # Mean value
    m: float

    # Standard deviation
    s: float

    @model_validator(mode="after")
    def check_params(self):
        """Check generator parameters"""
        if self.s < 0 or self.m < 0:
            raise ValueError("Standard deviation s and m must be greater than 0")
        if (self.min is not None and self.min > self.m + 3 * self.s) or (self.max is not None and self.max < self.m - 3 * self.s):
            raise ValueError("Unreachable interval in normal generator")
        return self
    
    @final
    def cpp_type(self) -> str:
        return f"{self.cpp_type_base()}_{self.N_to_str(self.m)}_{self.N_to_str(self.s)}_{self.once}"
    
    @final
    def clamp(self, x: float) -> float:
        """Clamps given value based on min and max"""
        if self.min is not None and x < self.min:
            x = self.min
        if self.max is not None and x > self.max:
            x = self.max
        return x

class NormalFloat(NormalBase[Literal["NormalFloat"], float]):
    """Normal Float value generator"""
    
    def value(self) -> float:
        x = random.gauss(self.m, self.s)
        return self.clamp(x)

class NormalInt(NormalBase[Literal["NormalInt"], int]):
    """Normal Int value generator"""
    
    def value(self) -> int:
        x = random.gauss(self.m, self.s)
        x = self.clamp(x)
        return int(round(x))
