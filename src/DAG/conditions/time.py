from typing import Literal
from pydantic import model_validator
from src.DAG.dag_base_model import FACTORS
from .base import ConditionBase

class Time(ConditionBase[Literal["Time"]]):
    """Condition that measures time"""

    # Time after which the condition is fulfilled
    after: int = 0

    #Time for which the condition is fulfilled if missing condition stays fulfilled
    duration: int | None = None

    # If `True` time is counted from starting eliot else from first packet checked by condition
    instant: bool = False

    # Time units
    unit: Literal["ms", "s", "min", "h"] = "ms"

    @model_validator(mode="after")
    def convert_time(self):
        """Converts time based on given units"""
        self.after *= FACTORS[self.unit]
        if self.duration is not None:
            self.duration *= FACTORS[self.unit]
        if self.after < 0 or (self.duration and self.duration <= 0):
            raise ValueError("after and duration have to be both positive")
        self.unit = "ms"
        return self

    def cpp_type(self) -> str:
        return f"{self.cpp_type_base()}_{self.after}_{self.duration}_{self.instant}_{id(self)}"
    
    def is_state(self) -> bool:
        return self.instant
    
    def time(self) -> bool:
        return True
