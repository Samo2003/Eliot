from __future__ import annotations
from typing import Literal
from pydantic import model_validator
from eliot.DAG.generators import ValueGeneratorInt
from .base import ActionBase

# Minimal allowed n value
MIN_N = 2
# Maximal allowed n value
MAX_N = 2048

class Reorder(ActionBase[Literal["Reorder"]]):
    """
    Action that reorders given number of packets based on a certain strategy.
    """

    # Packets to reorder
    n: int | ValueGeneratorInt

    # Reorder strategy
    strategy: Literal["random", "reverse"] = "random"

    @model_validator(mode="after")
    def check_n_bounds(self) -> Reorder:
        """Validates possible n values"""
        if isinstance(self.n, int):
            if self.n < MIN_N or self.n > MAX_N:
                raise ValueError(f"n must be from {MIN_N} to {MAX_N}")
        else:
            if self.n.max is None:
                self.n.max = MAX_N
            if self.n.min < MIN_N or self.n.max > MAX_N:
                raise ValueError(f"n must be from {MIN_N} to {MAX_N}")
        return self

    @property
    def cpp_type(self) -> str:
        return f"{self.cpp_type_base}_{self.n}_{self.strategy}_{id(self)}"

    @property
    def is_state(self) -> bool:
        return True
    
    @property
    def calendar(self) -> bool:
        return True
    
    @property
    def not_generator_n(self) -> bool:
        """Condition used in generating representing if n is a generator"""
        return isinstance(self.n, int)
