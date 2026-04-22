from __future__ import annotations
from abc import ABC
from pydantic import field_validator, model_validator
from typing import Literal, final
from eliot.DAG.dag_base_model import FACTORS
from .base import ValueGeneratorBase, T, N

class SeqBase(ValueGeneratorBase[T, N], ABC):
    """
    Abstract base class for sequential generators
    """

    # Number of steps required to reach next value
    period: int = 1

    # Step size
    step: N

    # Handling reached max or min value
    mode: Literal["repeat", "keep", "reverse"] = "keep"
    
    @field_validator("seed", mode="after")
    @classmethod
    def validate_seed(cls, seed: int | None) -> None:
        if seed is not None:
            raise ValueError(
                f"seed value has no effect in Seq generators"
            )

    @model_validator(mode="after")
    def check_consistency(self) -> SeqBase[T, N]:
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
        if self.mode == "reverse" and self.step >= 0 and self.max is None:
            raise ValueError(
                "max bound has to be defined for reverse mode with positive step"
            )
        return self
    
    @final
    def _apply_factor_inner(self, factor: int) -> None:
        self.step *= factor
    
    @property
    def cpp_type(self) -> str:
        return (
            f"{self.cpp_type_base}_"
            f"{self.period}_"
            f"{self.N_to_str(self.step)}_"
            f"{self.mode.upper()}"
        )
    
    @property
    @final
    def is_state(self) -> bool:
        return not self.once
    
class SeqCountFloat(SeqBase[Literal["SeqCountFloat"], float]):
    """Sequential count float value generator"""
    
    @property
    def value(self) -> float:
        if self.step < 0:
            return self.max if self.max is not None else 0
        return self.min

class SeqCountInt(SeqBase[Literal["SeqCountInt"], int]):
    """Sequential count int value generator"""
    
    @property
    def value(self) -> int:
        if self.step < 0:
            return self.max if self.max is not None else 0
        return self.min
    
class SeqTimeBase(SeqBase[T, N], ABC):
    """
    Abstract base class for sequential time generators
    """
    
    # Time units
    unit: Literal["ms", "s", "min", "h"] = "ms"
    
    # If `True` time is counted from starting eliot else from first generator call
    instant: bool = False
    
    @model_validator(mode="after")
    def convert_time(self) -> SeqTimeBase[T, N]:
        """Converts time based on given units"""
        self.period *= FACTORS[self.unit]
        self.unit = "ms"
        return self
    
    @property
    @final
    def time(self) -> bool:
        return True
    
    @property
    @final
    def cpp_type(self) -> str:
        return (
            f"{self.cpp_type_base}_"
            f"{self.period}_"
            f"{self.N_to_str(self.step)}_"
            f"{self.mode.upper()}_"
            f"{self.instant}"
        )

class SeqTimeFloat(SeqTimeBase[Literal["SeqTimeFloat"], float]):
    """Sequential time float value generator"""
     
    @property
    def value(self) -> float:
        if self.step < 0:
            return self.max if self.max is not None else 0
        return self.min

class SeqTimeInt(SeqTimeBase[Literal["SeqTimeInt"], int]):
    """Sequential time int value generator"""
     
    @property
    def value(self) -> int:
        if self.step < 0:
            return self.max if self.max is not None else 0
        return self.min