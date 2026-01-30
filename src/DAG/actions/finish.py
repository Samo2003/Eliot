from typing import Literal
from .base import ActionBase

class Finish(ActionBase[Literal["Finish"]]):
    """Final action that accepts the packet"""

    def is_final(self) -> bool:
        return True
    
    def cpp_type(self) -> str:
        return super().cpp_type_base()
