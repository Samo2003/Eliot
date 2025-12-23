from typing import Literal
from .base import GuardBase

class IPVersion(GuardBase[Literal["IPVersion"]]):
    """Check packets IP version"""

    # IP version to check
    v: Literal[4, 6] = 4

    def cpp_type(self) -> str:
        return super().cpp_type_base()
