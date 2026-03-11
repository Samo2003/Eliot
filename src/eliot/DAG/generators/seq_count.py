from __future__ import annotations
from abc import ABC
from pydantic import model_validator
from typing import Literal, final
from .base import ValueGeneratorBase, T, N

class SeqCountBase(ValueGeneratorBase[T, N], ABC):
    """
    Abstract base class for sequential count generators
    """

    # Number of steps required to reach next value
    period: int = 1

    # Step size
    step: N

    # Handling reached max or min value
    mode: Literal["repeat", "keep", "reverse"] = "keep"

    @model_validator(mode="after")
    def check_consistency(self) -> SeqCountBase[T, N]:
        """Validates consistency"""
        if self.step == 0:
            raise ValueError(
                "step must be none zero"
            )
        if self.step < 0 and self.max is None:
            raise ValueError(
                "max is required for decreasing sequence (step < 0)"
            )
        if self.period <= 0:
            raise ValueError(
                "T must be >= 1"
            )
        if self.seed is not None:
            raise ValueError(
                f"Seed value has no effect in {self.generatorType}"
            )
        if self.mode == "reverse" and self.step >= 0 and self.max is None:
            raise ValueError(
                "max bound has to be defined for reverse mode with positive step"
            )
        return self
    
    @final
    def _apply_factor_inner(self, factor: int) -> None:
        self.step *= factor
    
    @final
    def cpp_type(self) -> str:
        return (
            f"{self.cpp_type_base()}_"
            f"{self.period}_"
            f"{self.N_to_str(self.step)}_"
            f"{self.mode.upper()}"
        )
    
    @final
    def is_state(self) -> bool:
        return not self.once
    
class SeqCountFloat(SeqCountBase[Literal["SeqCountFloat"], float]):
    """Sequential count float value generator"""
    
    def value(self) -> float:
        if self.step < 0:
            return self.max if self.max is not None else 0
        return self.min

class SeqCountInt(SeqCountBase[Literal["SeqCountInt"], int]):
    """Sequential count int value generator"""
    
    def value(self) -> int:
        if self.step < 0:
            return self.max if self.max is not None else 0
        return self.min
