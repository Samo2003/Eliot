from typing import Literal
from .base import ActionBase
from ..generators import ValueGeneratorInt

class Replicate(ActionBase[Literal["Replicate"]]):
    n: int | ValueGeneratorInt
