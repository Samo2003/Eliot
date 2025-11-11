from typing import Literal
from .base import GuardBase

class Port(GuardBase[Literal["Port"]]):
    """Checks port nubers"""

    # Surce or destination port
    port: int | None = None

    # Source port
    src: int | None = None

    # Destination port
    dst: int | None = None
