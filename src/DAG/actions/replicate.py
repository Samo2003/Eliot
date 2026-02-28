from typing import Literal
from pydantic import model_validator
from src.DAG.generators import ValueGeneratorInt, ValueGeneratorBase
from .base import ActionBase

class Replicate(ActionBase[Literal["Replicate"]]):
    """
    Replicates packet given amount of times.
    """

    # Number of times to replicate the packet
    n: int | ValueGeneratorInt

    @model_validator(mode="after")
    def validate_n(self):
        if isinstance(self.n, int):
            if self.n <= 0:
                raise ValueError("n must be a positive number")
        else:
            if self.n.min <= 0:
                raise ValueError("n must be a positive number")
        return self
    
    def cpp_type(self) -> str:
        return (
            f"{self.cpp_type_base()}_"
            f"{self.n}"
            f"{'_' + str(id(self)) if isinstance(self.n, ValueGeneratorBase) and self.n.is_state() else ''}"
        )
    
    def is_state(self) -> bool:
        return True

    def calendar(self) -> bool:
        return True
    
    def not_generator_n(self) -> bool:
        """Condition used in generating representing if n is a generator"""
        return isinstance(self.n, int)
