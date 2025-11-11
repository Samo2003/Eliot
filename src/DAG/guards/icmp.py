from typing import Literal
from .base import GuardBase

class ICMP(GuardBase[Literal["ICMP"]]):
    """Check ICMP packets"""

    # ICMP type to check
    type: int | None = None

    # ICMP code to check
    code: int | None = None
