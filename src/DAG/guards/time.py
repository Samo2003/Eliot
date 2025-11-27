from typing import Literal
from .base import GuardBase
from ..generators import ValueGeneratorInt

class Time(GuardBase[Literal["Time"]]):
    """Guard that measures time"""

    # Time after which the guard is fullfiled
    after: int | ValueGeneratorInt = 0

    #Time for which the guard is fullfiled if missing guard stays fullfiled
    duration: int | ValueGeneratorInt | None = None

    # If `True` time is counted from starting eliot else from first packet checked by guard
    instant: bool = False

    def cpp_type(self) -> str:
        return f"{self.cpp_type_base()}_{self.after}_{self.duration}"
    
    def is_state(self) -> bool:
        return True
    
    def time(self) -> bool:
        return True
