from typing import Literal
from .base import ActionBase

class Drop(ActionBase[Literal["Drop"]]):
    """
    Final action that drops the packet.
    """

    @property
    def is_final(self) -> bool:
        return True
    
    @property
    def cpp_type(self) -> str:
        return self.cpp_type_base
