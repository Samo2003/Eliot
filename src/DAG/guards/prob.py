from typing import Literal
from .base import GuardBase
from ..generators import ValueGeneratorFloat

class Prob(GuardBase[Literal["Prob"]]):
    x: float | ValueGeneratorFloat
