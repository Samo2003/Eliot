from __future__ import annotations
from typing import Literal
from pydantic import field_validator
from .base import ConditionBase

class ICMP(ConditionBase[Literal["ICMP"]]):
    """
    Check ICMP packet parameters.
    """

    # ICMP type to check
    icmp_type: int

    # ICMP code to check
    icmp_code: int | None = None
    
    @field_validator("icmp_type", mode="after")
    @classmethod
    def validate_type(cls, icmp_type: int) -> int:
        if icmp_type < 0 or icmp_type > 255:
            raise ValueError("ICMP type must be in range <0,255>")
        return icmp_type
    
    @field_validator("icmp_code", mode="after")
    @classmethod
    def validate_code(cls, icmp_code: int | None) -> int | None:
        if icmp_code is not None:
            if icmp_code < 0 or icmp_code > 255:
                raise ValueError("ICMP code must be in range <0,255>")
        return icmp_code
    
    @property
    def cpp_type(self) -> str:
        parts = [self.cpp_type_base]
        parts.append(f"type_{self.type}")

        if self.icmp_code is not None:
            parts.append(f"code_{self.icmp_code}")

        return "_".join(parts)
