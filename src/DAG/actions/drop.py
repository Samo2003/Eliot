from typing import Literal
from .base import ActionBase

class Drop(ActionBase[Literal["Drop"]]):
    def is_final(self) -> bool:
        return True
    
    def cpp_call(self) -> str:
        return "return PacketResult::Drop"
