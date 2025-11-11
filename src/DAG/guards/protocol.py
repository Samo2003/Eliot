from typing import Literal
from .base import GuardBase

class Protocol(GuardBase[Literal["Protocol"]]):
    """Check protocol in IP header"""

    # Protocol identifier
    id: int
