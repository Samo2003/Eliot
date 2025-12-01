from typing import Literal
from ..generators import ValueGeneratorFloat
from .base import ActionBase

class Throttle(ActionBase[Literal["Throttle"]]):
    """Throttles the communication to certain limit"""

    # Throttle value in B/s
    limit: float | ValueGeneratorFloat
