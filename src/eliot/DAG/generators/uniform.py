from __future__ import annotations
from abc import ABC
import random
from typing import Literal, cast, final
from pydantic import model_validator
from .base import ValueGeneratorBase, T, N

class UniformBase(ValueGeneratorBase[T, N], ABC):
    """
    Abstract base class for uniform distribution generators
    """

    @model_validator(mode="after")
    def ensure_min_max(self) -> UniformBase[T, N]:
        """Max interval must be defined"""
        if self.max is None:
            raise ValueError("min and max must be provided for UniformFloat")
        return self
    
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
