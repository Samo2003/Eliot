from typing import Literal
from .base import GuardBase
from ..generators import ValueGeneratorInt

class EveryN(GuardBase[Literal["EveryN"]]):
    N: int | ValueGeneratorInt

    def cpp_type(self) -> str:
        return f"{super().cpp_type()}_{self.N}"
    
    def is_state(self) -> bool:
        return True
    
    def not_generator(self) -> bool:
        return isinstance(self.N, int)
