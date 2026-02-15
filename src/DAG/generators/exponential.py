from abc import ABC
from typing import Literal, final
from pydantic import model_validator
from .base import ValueGeneratorBase, T, N
import random
import math

class ExponentialBase(ValueGeneratorBase[T, N], ABC):
    """Abstract exponential generator base"""

    # Mean distribution value
    mean: float | None = None

    # Rate distribution value
    rate: float | None = None

    @model_validator(mode="after")
    def validate_mean(self):
        if self.mean is None and self.rate is None:
            raise ValueError("Either mean or rate must be specified")
        if self.mean is not None and self.rate is not None:
            raise ValueError("Specify either mean or rate, not both")
        if self.mean is not None and self.mean <= 0:
            raise ValueError("Mean value for exponential distribution has to be positive")
        if self.rate is not None and self.rate <= 0:
            raise ValueError("Mean value for exponential distribution has to be positive")
        if self.max is not None and self.max < 0:
            raise ValueError("Exponential distribution cannot generate negative values")
        if self.min is not None and self.min < 0:
            raise ValueError("Exponential distribution only generates positive values")
        return self
    
    @final
    def cpp_type(self) -> str:
        return f"{self.cpp_type_base()}_{str(self.mean).replace('.', '_')}_{str(self.rate).replace('.', '_')}_{self.once}"
    
class ExponentialFloat(ExponentialBase[Literal["ExponentialFloat"], float]):
    """Exponential Float value generator"""
    
    def value(self) -> float:
        u = random.random()
        x = 0.0
        if self.mean is not None:
            x = -self.mean * math.log(u)
        if self.rate is not None:
            x = -math.log(u) / self.rate
        return self.clamp(x)

class ExponentialInt(ExponentialBase[Literal["ExponentialInt"], int]):
    """Exponential Int value generator"""
    
    def value(self) -> int:
        u = random.random()
        x = 0.0
        if self.mean is not None:
            x = -self.mean * math.log(u)
        if self.rate is not None:
            x = -math.log(u) / self.rate
        return int(self.clamp(x))
    