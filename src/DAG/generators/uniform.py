from abc import ABC
from typing import Literal, Tuple, cast
from pydantic import model_validator
from .base import ValueGeneratorBase, T, N
import random

class UniformBase(ValueGeneratorBase[T, N], ABC):
    @model_validator(mode="after")
    def ensure_min_max(self):
        if self.min is None or self.max is None:
            raise ValueError("min and max must be provided for UniformFloat")
        return self
    
    def get_min_max(self) -> Tuple[N, N]:
        min_val = cast(N, self.min)
        max_val = cast(N, self.max)
        return min_val, max_val
    
    def cpp_type(self) -> str:
        min_val, max_val = self.get_min_max()
        return f"{super().cpp_type()}_{self.N_to_int_str(min_val)}_{self.N_to_int_str(max_val)}_{self.once}"

class UniformFloat(UniformBase[Literal["UniformFloat"], float]):
    def value(self) -> float:
        min_val, max_val = self.get_min_max()
        return random.uniform(min_val, max_val)

class UniformInt(UniformBase[Literal["UniformInt"], int]):
    def value(self) -> int:
        min_val, max_val = self.get_min_max()
        return random.randint(min_val, max_val)
