from typing import Literal
from .base import ActionBase

class Finish(ActionBase[Literal["Finish"]]):
    """Final action that accepts the packet"""

    def is_final(self) -> bool:
        return True
    
    def cpp_call(self) -> str:
        return "return PacketResult::Finish"
    
    def cpp_type(self) -> str:
        """Defined only to silence Pylance warning"""
        return ""
