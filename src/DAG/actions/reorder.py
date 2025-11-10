from typing import Literal
from ..generators import ValueGeneratorInt
from .base import ActionBase

class Reorder(ActionBase[Literal["Reorder"]]):
    n: int | ValueGeneratorInt
    strategy: Literal["random", "reverse"] = "random"

    def cpp_type(self) -> str:
        return f"{super().cpp_type()}_{self.n}_{self.strategy}"

    def is_state(self) -> bool:
        return True
    
    def calendar(self) -> bool:
        return True
    
    def init(self) -> str:
        return f" = {self.cpp_type()}(_calendar)"
