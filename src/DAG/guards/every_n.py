from typing import Literal
from .base import GuardBase
from ..generators import ValueGeneratorInt

class EveryN(GuardBase[Literal["EveryN"]]):
    """Guard that is fullfilled every nth packet"""

    N: int | ValueGeneratorInt

    def cpp_type(self) -> str:
        return f"{super().cpp_type_base()}_{self.N}"
    
    def is_state(self) -> bool:
        return True
    
    def not_generator(self) -> bool:
        """Condition used in generating representing if N is a generator"""
        return isinstance(self.N, int)
