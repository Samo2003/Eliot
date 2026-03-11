from __future__ import annotations
import math
import random
from abc import ABC
from typing import Literal, final
from pydantic import model_validator
from .base import ValueGeneratorBase, T, N

class ExponentialBase(ValueGeneratorBase[T, N], ABC):
    """
    Abstract base class for exponential distribution generators.
    """

    # Mean of exponential distribution
    mean: float | None = None

    # Rate parameter
    rate: float | None = None

    @model_validator(mode="after")
    def validate_parameters(self) -> ExponentialBase[T, N]:
        """
        Validate parameters.
        """
        if self.mean is None and self.rate is None:
            raise ValueError(
                "Either mean or rate must be specified"
            )
        if self.mean is not None and self.rate is not None:
            raise ValueError(
                "Specify either mean or rate, not both"
            )
        if self.mean is not None and self.mean <= 0:
            raise ValueError(
                "Mean value for exponential distribution has to be positive"
            )
        if self.rate is not None and self.rate <= 0:
            raise ValueError(
                "Mean value for exponential distribution has to be positive"
            )
        if self.max is not None and self.max < 0:
            raise ValueError(
                "Exponential distribution cannot generate negative values"
            )
        return self
    
    @final
    def _apply_factor_inner(self, factor: int) -> None:
        if self.mean is not None:
            self.mean *= factor
        if self.rate is not None:
            self.rate /= factor
    
    @final
    def cpp_type(self) -> str:
        return (
            f"{self.cpp_type_base()}_"
            f"{self.N_to_str(self.mean)}_"
            f"{self.N_to_str(self.rate)}"
        )
    
class ExponentialFloat(ExponentialBase[Literal["ExponentialFloat"], float]):
    """Exponential Float value generator"""
    
    def value(self) -> float:
        if self.seed is not None:
            u = random.Random(self.seed).random()
        else:
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
        if self.seed is not None:
            u = random.Random(self.seed).random()
        else:
            u = random.random()
        x = 0.0
        if self.mean is not None:
            x = -self.mean * math.log(u)
        if self.rate is not None:
            x = -math.log(u) / self.rate
        return int(self.clamp(x))
    