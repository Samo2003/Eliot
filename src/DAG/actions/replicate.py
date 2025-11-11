from typing import Literal
from .base import ActionBase
from ..generators import ValueGeneratorInt

class Replicate(ActionBase[Literal["Replicate"]]):
    """Replicates packet given amount of times"""

    # Number of times to replicate the packet
    n: int | ValueGeneratorInt
