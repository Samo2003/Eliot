from typing import Literal
from .base import GuardBase
from ..generators import ValueGeneratorFloat

class Prob(GuardBase[Literal["Prob"]]):
    """Fullfils based on propability"""

    # Propability <0,1>
    x: float | ValueGeneratorFloat
