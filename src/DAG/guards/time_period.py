from typing import Literal
from pydantic import model_validator
from ..generators import ValueGeneratorInt
from .base import GuardBase
from ..dag_base_model import FACTORS

class TimePeriod(GuardBase[Literal["TimePeriod"]]):
    """Guard that check time-periods"""

    # Time for which the guard is fulfilled
    t: int | ValueGeneratorInt

    # Time for which the guard is false
    f: int | ValueGeneratorInt | None = None

    # If `True` time is counted from starting eliot else from first packet checked by guard
    instant: bool = False

    # Time units, also applied for generator
    unit: Literal["ms", "s", "min", "h"] = "ms"

    @model_validator(mode="after")
    def set_default_f_and_convert_time(self):
        """Default value of `f` is `t`, and converts time based on given units"""
        if isinstance(self.t, int):
            self.t *= FACTORS[self.unit]
        else:
            if self.t.min is not None:
                self.t.min *= FACTORS[self.unit]
            if self.t.max is not None:
                self.t.max *= FACTORS[self.unit]
        if self.f is None:
            self.f = self.t
        self.unit = "ms"
        return self
    
    def cpp_type(self) -> str:
        return f"{self.cpp_type_base()}_{self.t}_{self.f}"
    
    def is_state(self) -> bool:
        return True
    
    def time(self) -> bool:
        return True
    
    def not_generator_t(self) -> bool:
        """Condition used in generating representing if t is a generator"""
        return isinstance(self.t, int)
    
    def not_generator_f(self) -> bool:
        """Condition used in generating representing if f is a generator"""
        return isinstance(self.f, int)
