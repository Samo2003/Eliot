from typing import Literal

from pydantic import model_validator
from .base import GuardBase

class Port(GuardBase[Literal["Port"]]):
    """Checks port numbers"""

    # Source or destination port
    port: int | None = None

    # Source port
    src: int | None = None

    # Destination port
    dst: int | None = None

    @model_validator(mode="after")
    def validate_ports(self):
        if self.port is None and self.src is None and self.dst is None:
            raise ValueError("no port provided")

        if self.port is not None:
            if self.src is not None or self.dst is not None:
                raise ValueError("when port is provided, src and dst cannot be given")
            self.src = self.port
            self.dst = self.port
            self.port = None

        for p in [self.src, self.dst]:
            if p is not None:
                if p < 0 or p > 65535:
                    raise ValueError(f"invalid port number: {p}")

        return self
    
    def cpp_type(self) -> str:
        parts = [super().cpp_type_base()]

        if self.src is not None:
            parts.append(f"src_{self.src}")

        if self.dst is not None:
            parts.append(f"dst_{self.dst}")

        return "_".join(parts)