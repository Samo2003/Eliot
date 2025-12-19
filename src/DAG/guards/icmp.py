from typing import Literal
from pydantic import model_validator
from .base import GuardBase

class ICMP(GuardBase[Literal["ICMP"]]):
    """Check ICMP packets"""

    # ICMP type to check
    type: int

    # ICMP code to check
    code: int | None = None

    @model_validator(mode="after")
    def validate_icmp(self):
        if self.type < 0 or self.type > 255:
            raise ValueError("ICMP type must be in range <0,255>")

        if self.code is not None:
            if self.code < 0 or self.code > 255:
                raise ValueError("ICMP code must be in range <0,255>")

        return self
    
    def cpp_type(self) -> str:
        parts = [super().cpp_type_base()]
        parts.append(f"type_{self.type}")

        if self.code is not None:
            parts.append(f"code_{self.code}")

        return "_".join(parts)
