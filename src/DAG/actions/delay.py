from typing import Literal
from pydantic import model_validator
from src.DAG.generators import ValueGeneratorInt
from src.DAG.dag_base_model import FACTORS
from .base import ActionBase

# Calendar max delay in ms
MAX_DELAY = 16777215

class Delay(ActionBase[Literal["Delay"]]):
    """Action that delays packet"""
    
    # Time in ms for which the packet is delayed
    n: int | ValueGeneratorInt

    # Time units, also applied for generator
    unit: Literal["ms", "s", "min", "h"] = "ms"

    @model_validator(mode="after")
    def convert_and_check_n(self):
        """Converts n to ms based on provided units and validates its value"""
        if isinstance(self.n, int):
            self.n *= FACTORS[self.unit]

            if self.n < 0 or self.n > MAX_DELAY:
                raise ValueError(
                    f"n must be from 0 to {MAX_DELAY} in ms got: {self.n}"
                )
        else:
            self.n.apply_factor(FACTORS[self.unit])
            if self.n.max is None:
                self.n.max = MAX_DELAY
            if self.n.min < 0 or self.n.max > MAX_DELAY:
                raise ValueError(f"n must be from 0 to {MAX_DELAY} in ms")
        self.unit = "ms"
        return self

    def cpp_type(self) -> str:
        return f"{self.cpp_type_base()}_{self.n}_{id(self)}"

    def calendar(self) -> bool:
        return True
    
    def is_state(self) -> bool:
        return True
    
    def not_generator_n(self) -> bool:
        """Condition used in generating representing if n is a generator"""
        return isinstance(self.n, int)
