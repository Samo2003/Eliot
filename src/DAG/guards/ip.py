from typing import Literal
from .base import GuardBase

class IP(GuardBase[Literal["IP"]]):
    """Check IP address"""

    # Destination or source IP address
    ip: str | None = None

    # Source IP address
    src: str | None = None

    # Destination IP address
    dst: str | None = None
