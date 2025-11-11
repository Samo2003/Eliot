from typing import Literal
from pydantic import model_validator
from ..generators import ValueGeneratorInt
from .base import GuardBase

class TimePeriod(GuardBase[Literal["TimePeriod"]]):
    """Guard that check time-preriods"""

    # Time for which the guard is fullfiled
    t: int | ValueGeneratorInt

    # Time for which the guard is false
    f: int | ValueGeneratorInt | None = None

    # If `True` time is counted from starting Netloiter else from first packet checked by guard
    instant: bool = False

    @model_validator(mode="after")
    def set_default_f(self):
        """Default value of `f` is `t`"""
        if self.f is None:
            self.f = self.t
        return self
    
    def cpp_type(self) -> str:
        return f"{super().cpp_type_base()}_{self.t}_{self.f}"
    
    def is_state(self) -> bool:
        return True
