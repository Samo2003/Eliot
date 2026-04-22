from __future__ import annotations
from typing import Literal
from pydantic import field_validator
from eliot.DAG.generators import ValueGeneratorBase, ValueGeneratorFloat
from .base import ConditionBase

class Prob(ConditionBase[Literal["Prob"]]):
    """
    Fulfills based on probability
    """

    # Probability <0,1>
    x: float | ValueGeneratorFloat

    # Set generator seed to ensure determinism
    seed: int | None = None
    
    @field_validator("x", mode="after")
    @classmethod
    def validate_x(cls, x: float | ValueGeneratorFloat) -> float | ValueGeneratorFloat:
        if isinstance(x, float) and (x < 0 or x > 1):
            raise ValueError("x must be in range <0,1>")
        elif isinstance(x, ValueGeneratorBase):
            if x.min < 0:
                raise ValueError("min must be non negative")

            if x.max is None:
                x.max = 1.0
            elif x.max > 1:
                raise ValueError("max must be smaller than 1")
            
            if x.max < x.min:
                raise ValueError("max must be bigger than min")
        return x
    
    @field_validator("seed", mode="after")
    @classmethod
    def validate_seed(cls, seed: int | None) -> int | None:
        if seed is not None and seed < 0:
            raise ValueError("seed value has to be a positive integer")
        return seed
    
    @property
    def cpp_type(self) -> str:
        if isinstance(self.x, float):
            return f"{self.cpp_type_base}_{str(self.x).replace('.', '_')}"
        return (
            f"{self.cpp_type_base}_"
            f"{self.x}"
            f"{'_' + str(id(self)) if isinstance(self.x, ValueGeneratorBase) and self.x.is_state else ''}"
        )
    
    @property
    def not_generator_x(self) -> bool:
        """Condition used in generating representing if x is a generator"""
        return isinstance(self.x, float)
    
    @property
    def seed_value(self) -> int:
        if self.seed is not None:
            return self.seed
        return super().seed_value
