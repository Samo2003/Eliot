from typing import Literal
from .base import ActionBase

class Finish(ActionBase[Literal["Finish"]]):
    """
    Final action that accepts the packet.
    """

    @property
    def is_final(self) -> bool:
        return True
    
    @property
    def cpp_type(self) -> str:
        return self.cpp_type_base
