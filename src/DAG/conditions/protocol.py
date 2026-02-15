from typing import Literal
from pydantic import model_validator
from .base import ConditionBase

class Protocol(ConditionBase[Literal["Protocol"]]):
    """Check protocol in IP header"""

    # Protocol identifier
    id: int

    # Check next header field only for IPv6 default is L4 protocol
    nh: bool = False

    @model_validator(mode="after")
    def validate_protocol(self):
        if self.id < 0 or self.id > 0xFF:
            raise ValueError("id has to be in range <0, 255>")
        
        return self
    
    def cpp_type(self) -> str:
        return f"{super().cpp_type_base()}_{self.id}"
    
    def get_nh(self) -> str:
        return "true" if self.nh else "false"
