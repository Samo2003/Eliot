from typing import Literal
from .base import ActionBase

class Drop(ActionBase[Literal["Drop"]]):
    """Final action that drops the packet"""

    def is_final(self) -> bool:
        return True
    
    def cpp_call(self) -> str:
        return "return PacketResult::Drop"
    
    def cpp_type(self) -> str:
        """Defined only to silence Pylance warning"""
        return ""
