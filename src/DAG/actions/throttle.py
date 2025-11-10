from typing import Literal
from ..generators import ValueGeneratorFloat
from .base import ActionBase

class Throttle(ActionBase[Literal["Throttle"]]):
    limit: float | ValueGeneratorFloat
