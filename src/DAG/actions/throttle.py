from typing import Literal
from .base import ActionBase
from pydantic import model_validator

class Throttle(ActionBase[Literal["Throttle"]]):
    """Throttles the communication to a certain limit using token bucket or leaking bucket based on mode"""

    # Throttle value in B/s
    rate: float

    # Maximum token bucket size
    burst: float | None = None

    # Throttling mode
    mode: Literal["shaping", "policing"] = "shaping"

    @model_validator(mode="after")
    def validate_limit(self):
        if self.burst is None and self.mode == "shaping":
            raise ValueError("burst has to be set when using shaping")
        if self.burst is not None and self.mode == "policing":
            raise ValueError("burst is unnecessarily set when using policing")
        if (self.burst is not None and self.burst < 0) or self.rate <= 0:
            raise ValueError("limit and burst both have to be positive")
        return self

    def calendar(self) -> bool:
        return self.mode == "shaping"
    
    def time(self) -> bool:
        return True
    
    def is_state(self) -> bool:
        return True
    
    def cpp_type(self) -> str:
        return f"{super().cpp_type_base()}_{self.rate}_{self.burst}_{id(self)}".replace(".", "_")
    
    def init(self) -> str:
        return f" = {self.cpp_type()}(_calendar)" if self.calendar() else ""
