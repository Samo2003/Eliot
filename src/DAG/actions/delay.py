from typing import Literal
from ..generators import ValueGeneratorInt
from .base import ActionBase

class Delay(ActionBase[Literal["Delay"]]):
    """Action that delays packet"""
    
    # Time in ms for which the packet is delayed
    n: int | ValueGeneratorInt

    def cpp_type(self) -> str:
        return f"{self.cpp_type_base()}_{self.n}"

    def calendar(self) -> bool:
        return True
    
    def is_state(self) -> bool:
        return True
    
    def init(self) -> str:
        return f" = {self.cpp_type()}(calendar)"
    
    def not_generator_n(self) -> bool:
        """Condition used in generating representing if n is a generator"""
        return isinstance(self.n, int)
