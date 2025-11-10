from abc import ABC
from typing import Literal
from .base import ValueGeneratorBase, T, N

class NormalBase(ValueGeneratorBase[T, N], ABC):
    m: float
    s: float

class NormalFloat(NormalBase[Literal["NormalFloat"], float]):
    pass

class NormalInt(NormalBase[Literal["NormalInt"], int]):
    pass

