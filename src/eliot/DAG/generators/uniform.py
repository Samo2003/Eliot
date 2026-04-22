from __future__ import annotations
from abc import ABC
import random
from typing import Literal, cast, final
from pydantic import field_validator
from .base import ValueGeneratorBase, T, N

class UniformBase(ValueGeneratorBase[T, N], ABC):
    """
    Abstract base class for uniform distribution generators
    """

    @field_validator("max", mode="after")
    @classmethod
    def validate_max(cls, max: N | None) -> N:
        """Max interval must be defined"""
        if max is None:
            raise ValueError("max must be provided for Uniform generator")
        return max
    
    @final
    def _apply_factor_inner(self, factor: int) -> None:
        """Just to implement abstract method nothing to do"""
    
    @property
    @final
    def min_max(self) -> tuple[N, N]:
        """Convert interval range to specified type for Pylance"""
        min_val = self.min
        max_val = cast(N, self.max)
        return min_val, max_val
    
    @property
    @final
    def cpp_type(self) -> str:
        return self.cpp_type_base

class UniformFloat(UniformBase[Literal["UniformFloat"], float]):
    """Uniform Float value generator"""

    @property
    def value(self) -> float:
        min_val, max_val = self.min_max
        if self.seed is not None:
            return random.Random(self.seed).uniform(min_val, max_val)
        return random.uniform(min_val, max_val)

class UniformInt(UniformBase[Literal["UniformInt"], int]):
    """Uniform int value generator"""

    @property
    def value(self) -> int:
        min_val, max_val = self.min_max
        if self.seed is not None:
            return random.Random(self.seed).randint(min_val, max_val)
        return random.randint(min_val, max_val)
