from typing import List, Literal
from pydantic import model_validator
from .base import GuardBase

class Protocol(GuardBase[Literal["Protocol"]]):
    """Check protocol in IP header"""

    # Protocol identifier
    id: int | List[int]

    @model_validator(mode="after")
    def validate_protocol(self):
        ids = [self.id] if isinstance(self.id, int) else self.id

        if len(ids) < 1:
            raise ValueError("no protocol id provided")
        
        for id in ids:
            if id < 0 or id > 0xFF:
                raise ValueError("id has to be in range <0, 255>")
        
        self.id = sorted(ids)
        return self
    
    def cpp_type(self) -> str:
        # Just for pylance should never happen thanks to model validator
        if not isinstance(self.id, List):
            return ""
        ids = "_".join(str(i) for i in self.id)
        return f"{super().cpp_type_base()}_{ids}"