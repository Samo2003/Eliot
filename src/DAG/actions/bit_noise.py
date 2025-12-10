from typing import Literal
from pydantic import model_validator
from ..generators import ValueGeneratorInt, ValueGeneratorFloat
from .base import ActionBase

class BitNoise(ActionBase[Literal["BitNoise"]]):
    """Inserts bit noise into the packet"""

    # Part of bits to invert <0,1>
    x: float | ValueGeneratorFloat | None = None

    # Number of bits to invert
    n: int | ValueGeneratorInt | None = None

    # Strategy to choose bits to invert
    strategy: Literal["left", "right", "random"]

    @model_validator(mode="after")
    def check_x_or_n(self):
        """Only n or x can be provided"""
        if (self.x is None and self.n is None) or (self.x is not None and self.n is not None):
            raise ValueError("x or n must be provided")
        if self.x is not None and isinstance(self.x, float) and not (0 <= self.x <= 1):
            raise ValueError("x must be between 0 and 1")
        if self.n is not None and isinstance(self.n, int) and self.n < 0:
            raise ValueError("n must be >= 0")
        return self
