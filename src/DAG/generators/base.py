from abc import ABC
from typing import TypeVar, Generic
from ..dag_base_model import DAGBaseModel

T = TypeVar("T", bound=str)
N = TypeVar("N", int, float)

class ValueGeneratorBase(DAGBaseModel, Generic[T, N], ABC):
    # Add hash method from parent class because it was deleted by Generic
    __hash__ = DAGBaseModel.__hash__

    generatorType: T
    min: N | None = None
    max: N | None = None
    once: bool = False

    def __str__(self) -> str:
        return self.cpp_type()
    
    def cpp_type(self) -> str:
        return f"{self.generatorType}Generator"
    
    def value(self) -> N:
        raise NotImplementedError
    
    def N_to_int_str(self, x: N) -> str:
        return str(int(round(float(x))))
