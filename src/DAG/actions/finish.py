from typing import Literal
from .base import ActionBase

class Finish(ActionBase[Literal["Finish"]]):
    def is_final(self) -> bool:
        return True
    
    def cpp_call(self) -> str:
        return "return PacketResult::Finish"
