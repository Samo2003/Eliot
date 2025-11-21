from typing import Literal
from pydantic import model_validator
from .base import GuardBase
from ..generators import ValueGeneratorInt

class CountPeriod(GuardBase[Literal["CountPeriod"]]):
    """Guard that checks count-based condition"""

    # Number of packets for which the guard is fullfiled
    t: int | ValueGeneratorInt

    # Number of packets for which the guard is false
    f: int | ValueGeneratorInt | None = None

    @model_validator(mode="after")
    def set_default_f(self):
        """Default value of `f` is `t`"""
        if self.f is None:
            self.f = self.t
        return self

    def cpp_type(self) -> str:
        return f"{self.cpp_type_base()}_{self.t}_{self.f}"
    
    def is_state(self) -> bool:
        return True
