from __future__ import annotations
from typing import Literal
from pydantic import model_validator
from eliot.DAG.generators import ValueGeneratorInt
from .base import ConditionBase

class CountPeriod(ConditionBase[Literal["CountPeriod"]]):
    """
    Periodic count-based condition.

    The condition alternates between two states.
    """

    # Number of packets where condition is fulfilled
    t: int | ValueGeneratorInt

    # Number of packets where condition is false
    f: int | ValueGeneratorInt | None = None

    @model_validator(mode="after")
    def set_default_f(self) -> CountPeriod:
        """Default value of `f` is `t`"""
        if self.f is None:
            self.f = self.t
        if isinstance(self.t, int):
            if self.t <= 0:
                raise ValueError("t must be greater than zero")
        else:
            if self.t.min <= 0:
                raise ValueError("t must be greater than zero")
            
        if isinstance(self.f, int):
            if self.f <= 0:
                raise ValueError("f must be greater than zero")
        else: 
            if self.f.min <= 0:
                raise ValueError("f must be greater than zero")
        return self

    def cpp_type(self) -> str:
        return f"{self.cpp_type_base()}_{self.t}_{self.f}_{id(self)}"
    
    def is_state(self) -> bool:
        return True
    
    def not_generator_t(self) -> bool:
        """Condition used in generating representing if t is a generator"""
        return isinstance(self.t, int)
    
    def not_generator_f(self) -> bool:
        """Condition used in generating representing if f is a generator"""
        return isinstance(self.f, int)
