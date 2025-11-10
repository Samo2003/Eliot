from typing import Literal
from pydantic import model_validator
from .base import GuardBase
from ..generators import ValueGeneratorInt

class CountPeriod(GuardBase[Literal["CountPeriod"]]):
    t: int | ValueGeneratorInt
    f: int | ValueGeneratorInt | None = None

    @model_validator(mode="after")
    def set_default_f(self):
        if self.f is None:
            self.f = self.t
        return self

    def cpp_type(self) -> str:
        return f"{super().cpp_type()}_{self.t}_{self.f}"
    
    def is_state(self) -> bool:
        return True
