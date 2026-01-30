from typing import Literal
from .base import ActionBase

class Drop(ActionBase[Literal["Drop"]]):
    """Final action that drops the packet"""

    def is_final(self) -> bool:
        return True
    
    def cpp_type(self) -> str:
        return super().cpp_type_base()
