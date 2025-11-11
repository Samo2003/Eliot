from typing import Literal
from ..generators import ValueGeneratorInt
from .base import GuardBase

class Count(GuardBase[Literal["Count"]]):
    """Guard that counts packets"""

    # Number of packets after which the guard is fullfiled
    after: int | ValueGeneratorInt = 0

    # Number of packets for which the guard is fullfiled if missing guard stays fullfiled
    duration: int | ValueGeneratorInt | None = None

    def is_state(self) -> bool:
        return True
    
    def cpp_type(self) -> str:
        return f"{super().cpp_type_base()}_{self.after}{'_' + str(self.duration) if self.duration else '' }"
