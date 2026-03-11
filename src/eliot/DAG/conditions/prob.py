from __future__ import annotations
from typing import Literal
from pydantic import model_validator
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

    @model_validator(mode="after")
    def validate_x(self) -> Prob:
        if isinstance(self.x, float) and (self.x < 0 or self.x > 1):
            raise ValueError("x must be in range <0,1>")
        elif isinstance(self.x, ValueGeneratorBase):
            if self.x.min < 0:
                raise ValueError("min must be non negative")

            if self.x.max is None:
                self.x.max = 1
            elif self.x.max > 1:
                raise ValueError("max must be smaller than 1")
            
            if self.x.max < self.x.min:
                raise ValueError("max must be bigger than min")
            
        if self.seed is not None and self.seed < 0:
            raise ValueError("Seed value has to be a positive integer")
        return self
    
    def cpp_type(self) -> str:
        if isinstance(self.x, float):
            return f"{self.cpp_type_base()}_{str(self.x).replace('.', '_')}"
        return (
            f"{self.cpp_type_base()}_"
            f"{self.x}"
            f"{'_' + str(id(self)) if isinstance(self.x, ValueGeneratorBase) and self.x.is_state() else ''}"
        )
    
    def not_generator_x(self) -> bool:
        """Condition used in generating representing if x is a generator"""
        return isinstance(self.x, float)
    
    def seed_value(self) -> int:
        if self.seed is not None:
            return self.seed
        return super().seed_value()
