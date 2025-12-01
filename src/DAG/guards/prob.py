from typing import Literal
from .base import GuardBase
from ..generators import ValueGeneratorFloat

class Prob(GuardBase[Literal["Prob"]]):
    """Fulfils based on probability"""

    # Probability <0,1>
    x: float | ValueGeneratorFloat
