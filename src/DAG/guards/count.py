from typing import Literal

from pydantic import model_validator
from .base import GuardBase

class Count(GuardBase[Literal["Count"]]):
    """Guard that counts packets"""

    # Number of packets after which the guard is fulfilled
    after: int = 0

    # Number of packets for which the guard is fulfilled if missing guard stays fulfilled
    duration: int | None = None

    @model_validator(mode="after")
    def validate_counts(self):
        if self.after < 0:
            raise ValueError("after must not be negative")
        if self.duration and self.duration <= 0:
            raise ValueError("duration must not be negative")
        return self

    def is_state(self) -> bool:
        return True
    
    def cpp_type(self) -> str:
        return f"{self.cpp_type_base()}_{self.after}{'_' + str(self.duration) if self.duration else '' }"
