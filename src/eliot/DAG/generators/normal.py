from __future__ import annotations
import random
from abc import ABC
from typing import Literal, final
from pydantic import model_validator
from .base import ValueGeneratorBase, T, N

class NormalBase(ValueGeneratorBase[T, N], ABC):
    """
    Abstract base class for normal distribution generators.
    """

    # Mean of normal distribution
    m: float

    # Standard deviation
    s: float

    @model_validator(mode="after")
    def validate_parameters(self) -> NormalBase[T, N]:
        """
        Validate parameters.
        """
        if self.s < 0 or self.m < 0:
            raise ValueError(
                "Standard deviation s and m must be greater than 0"
            )
        if (
            (self.min > self.m + 3 * self.s) 
            or (self.max is not None and self.max < self.m - 3 * self.s)
        ):
            raise ValueError(
                "Unreachable interval in normal generator"
            )
        return self
    
    @final
    def _apply_factor_inner(self, factor: int) -> None:
        self.m *= factor
        self.s *= factor
    
    @final
    def cpp_type(self) -> str:
        return (
            f"{self.cpp_type_base()}_"
            f"{self.N_to_str(self.m)}_"
            f"{self.N_to_str(self.s)}"
        )

class NormalFloat(NormalBase[Literal["NormalFloat"], float]):
    """Normal Float value generator"""
    
    def value(self) -> float:
        if self.seed is not None:
            x = random.Random(self.seed).gauss(self.m, self.s)
        else:
            x = random.gauss(self.m, self.s)
        return self.clamp(x)

class NormalInt(NormalBase[Literal["NormalInt"], int]):
    """Normal Int value generator"""
    
    def value(self) -> int:
        if self.seed is not None:
            x = random.Random(self.seed).gauss(self.m, self.s)
        else:
            x = random.gauss(self.m, self.s)
        x = self.clamp(x)
        return int(round(x))
