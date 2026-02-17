from typing import Literal
from pydantic import model_validator
from .base import ActionBase
from ..generators import ValueGeneratorInt

class Replicate(ActionBase[Literal["Replicate"]]):
    """Replicates packet given amount of times"""

    # Number of times to replicate the packet
    n: int | ValueGeneratorInt

    @model_validator(mode="after")
    def validate_n(self):
        if isinstance(self.n, int):
            if self.n <= 0:
                raise ValueError("n must be a positive number")
        else:
            if self.n.min is not None and self.n.min <= 0:
                raise ValueError("n must be a positive number")
        return self
