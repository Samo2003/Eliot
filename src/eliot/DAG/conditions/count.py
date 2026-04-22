from __future__ import annotations
from typing import Literal
from pydantic import field_validator
from .base import ConditionBase

class Count(ConditionBase[Literal["Count"]]):
    """
    Condition that counts packets.
    """

    # Number of packets after which the condition is fulfilled
    after: int = 0

    # Number of packets for which the condition is fulfilled if missing condition stays fulfilled
    duration: int | None = None
    
    @field_validator("after", mode="after")
    @classmethod
    def validate_after(cls, after: int) -> int:
        if after < 0:
            raise ValueError("after must not be negative")
        return after
    
    @field_validator("after", mode="after")
    @classmethod
    def validate_duration(cls, duration: int | None) -> int | None:
        if duration and duration <= 0:
            raise ValueError("duration must not be negative")
        return duration

    @property
    def is_state(self) -> bool:
        return True
    
    @property
    def cpp_type(self) -> str:
        return (
            f"{self.cpp_type_base}_"
            f"{self.after}_"
            f"{id(self)}"
            f"{'_' + str(self.duration) if self.duration else '' }"
        )
