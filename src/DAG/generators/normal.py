from abc import ABC
from typing import Literal
from .base import ValueGeneratorBase, T, N

class NormalBase(ValueGeneratorBase[T, N], ABC):
    """Abstract normal generator base"""
    m: float
    s: float

class NormalFloat(NormalBase[Literal["NormalFloat"], float]):
    """Normal Float value generator"""
    pass

class NormalInt(NormalBase[Literal["NormalInt"], int]):
    """Normal Int value generator"""
    pass

