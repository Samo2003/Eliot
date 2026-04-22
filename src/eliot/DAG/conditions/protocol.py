from __future__ import annotations
from typing import Literal
from pydantic import field_validator
from .base import ConditionBase

class Protocol(ConditionBase[Literal["Protocol"]]):
    """
    Check protocol in IP header
    """

    # Protocol identifier
    id: int

    # Check next header field only for IPv6 default is L4 protocol
    nh: bool = False

    @field_validator("id", mode="after")
    @classmethod
    def validate_id(cls, id: int) -> int:
        if id < 0 or id > 0xFF:
            raise ValueError("id has to be in range <0, 255>")
        return id
    
    @property
    def cpp_type(self) -> str:
        return f"{self.cpp_type_base}_{self.id}_{self.nh}"
    
    @property
    def nh_str(self) -> str:
        return "true" if self.nh else "false"
