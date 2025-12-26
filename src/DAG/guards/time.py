from typing import Literal
from pydantic import model_validator
from .base import GuardBase
from ..dag_base_model import FACTORS

class Time(GuardBase[Literal["Time"]]):
    """Guard that measures time"""

    # Time after which the guard is fulfilled
    after: int = 0

    #Time for which the guard is fulfilled if missing guard stays fulfilled
    duration: int | None = None

    # If `True` time is counted from starting eliot else from first packet checked by guard
    instant: bool = False

    # Time units, also applied for generator
    unit: Literal["ms", "s", "min", "h"] = "ms"

    @model_validator(mode="after")
    def convert_time(self):
        """Converts time based on given units"""
        self.after *= FACTORS[self.unit]
        if self.duration is not None:
            self.duration *= FACTORS[self.unit]
        if self.after <= 0 or (self.duration and self.duration <= 0):
            raise ValueError("after and duration have to be both positive")
        self.unit = "ms"
        return self

    def cpp_type(self) -> str:
        return f"{self.cpp_type_base()}_{self.after}_{self.duration}_{self.instant}"
    
    def is_state(self) -> bool:
        return True
    
    def time(self) -> bool:
        return True
