from __future__ import annotations
from typing import Literal
from pydantic import model_validator
from .base import ConditionBase

class Port(ConditionBase[Literal["Port"]]):
    """
    Checks port numbers
    """

    # Source or destination port
    port: int | None = None

    # Source port
    src: int | None = None

    # Destination port
    dst: int | None = None

    @model_validator(mode="after")
    def validate_ports(self) -> Port:
        ports = [port for port in [self.port, self.src, self.dst] if port is not None]

        if not ports:
            raise ValueError("no port provided")
        
        if self.port is not None:
            if self.src is not None or self.dst is not None:
                raise ValueError("when port is provided, src and dst cannot be given")

        for port in ports:
            if port < 0 or port > 65535:
                raise ValueError(f"invalid port number: {port}")
        return self
    
    def cpp_type(self) -> str:
        parts = [super().cpp_type_base()]

        if self.port is not None:
            parts.append(f"any_{self.port}")

        if self.src is not None:
            parts.append(f"src_{self.src}")

        if self.dst is not None:
            parts.append(f"dst_{self.dst}")

        return "_".join(parts)