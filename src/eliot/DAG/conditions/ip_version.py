from typing import Literal
from .base import ConditionBase

class IPVersion(ConditionBase[Literal["IPVersion"]]):
    """
    Check packets IP version
    """

    # IP version to check
    v: Literal[4, 6] = 4

    @property
    def cpp_type(self) -> str:
        return f"{self.cpp_type_base}_{self.v}"
