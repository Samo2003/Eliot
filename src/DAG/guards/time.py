from typing import Literal
from .base import GuardBase
from ..generators import ValueGeneratorInt

class Time(GuardBase[Literal["Time"]]):
    after: int | ValueGeneratorInt = 0
    duration: int | ValueGeneratorInt | None = None
    instant: bool = False

    def cpp_type(self) -> str:
        return f"{super().cpp_type()}_{self.after}_{self.duration}"
    
    def is_state(self) -> bool:
        return True
