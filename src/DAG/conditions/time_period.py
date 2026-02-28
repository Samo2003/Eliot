from typing import Literal
from pydantic import model_validator
from src.DAG.generators import ValueGeneratorInt
from src.DAG.dag_base_model import FACTORS
from .base import ConditionBase

class TimePeriod(ConditionBase[Literal["TimePeriod"]]):
    """
    Condition that periodically changes state based on elapsed time
    """

    # Time for which the condition is fulfilled
    t: int | ValueGeneratorInt

    # Time for which the condition is false
    f: int | ValueGeneratorInt | None = None

    # If `True` time is counted from starting eliot else from first packet checked by condition
    instant: bool = False

    # Time units, also applied for generator
    unit: Literal["ms", "s", "min", "h"] = "ms"

    @model_validator(mode="after")
    def set_default_f_and_convert_time(self):
        """Default value of `f` is `t`, and converts time based on given units"""
        if isinstance(self.t, int):
            self.t *= FACTORS[self.unit]
            if self.t <= 0:
                raise ValueError("t must be greater that zero")
        else:
            self.t.apply_factor(FACTORS[self.unit])
            if self.t.min <= 0:
                raise ValueError("t must be greater that zero")
        
        if self.f is None:
            self.f = self.t
        elif isinstance(self.f, int):
            self.f *= FACTORS[self.unit]
            if self.f <= 0:
                raise ValueError("f must be greater that zero")
        else:
            self.f.apply_factor(FACTORS[self.unit])
            if self.f.min <= 0:
                raise ValueError("f must be greater that zero")
        self.unit = "ms"
        return self
    
    def cpp_type(self) -> str:
        return f"{self.cpp_type_base()}_{self.t}_{self.f}_{self.instant}_{id(self)}"
    
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
