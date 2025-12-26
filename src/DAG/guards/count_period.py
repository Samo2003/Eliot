from typing import Literal
from pydantic import model_validator
from .base import GuardBase
from ..generators import ValueGeneratorInt

class CountPeriod(GuardBase[Literal["CountPeriod"]]):
    """Guard that checks count-based condition"""

    # Number of packets for which the guard is fulfilled
    t: int | ValueGeneratorInt

    # Number of packets for which the guard is false
    f: int | ValueGeneratorInt | None = None

    @model_validator(mode="after")
    def set_default_f(self):
        """Default value of `f` is `t`"""
        if self.f is None:
            self.f = self.t
        if isinstance(self.t, int) and self.t < 0:
                raise ValueError("t must not be negative")
            
        if isinstance(self.f, int) and self.f < 0:
                raise ValueError("f must not be negative")
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
