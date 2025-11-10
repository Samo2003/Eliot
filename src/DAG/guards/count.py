from typing import Literal
from ..generators import ValueGeneratorInt
from .base import GuardBase

class Count(GuardBase[Literal["Count"]]):
    after: int | ValueGeneratorInt = 0
    duration: int | ValueGeneratorInt | None = None

    def is_state(self) -> bool:
        return True
    
    def cpp_type(self) -> str:
        return f"{super().cpp_type()}_{self.after}{'_' + str(self.duration) if self.duration else '' }"
