from __future__ import annotations
from typing import Literal
from pydantic import model_validator
from .base import ConditionBase

class ICMP(ConditionBase[Literal["ICMP"]]):
    """
    Check ICMP packet parameters.
    """

    # ICMP type to check
    icmp_type: int

    # ICMP code to check
    icmp_code: int | None = None

    @model_validator(mode="after")
    def validate_icmp(self) -> ICMP:
        if self.icmp_type < 0 or self.icmp_type > 255:
            raise ValueError("ICMP type must be in range <0,255>")

        if self.icmp_code is not None:
            if self.icmp_code < 0 or self.icmp_code > 255:
                raise ValueError("ICMP code must be in range <0,255>")

        return self
    
    @property
    def cpp_type(self) -> str:
        parts = [self.cpp_type_base]
        parts.append(f"type_{self.type}")

        if self.icmp_code is not None:
            parts.append(f"code_{self.icmp_code}")

        return "_".join(parts)
