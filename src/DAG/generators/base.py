from abc import ABC, abstractmethod
from typing import TypeVar, Generic, final
from pydantic import model_validator
from ..dag_base_model import DAGBaseModel

# Generic type parameter for generator identifier
T = TypeVar("T", bound=str)

# Generic type parameter for generator type
N = TypeVar("N", bound=float)

class ValueGeneratorBase(DAGBaseModel, Generic[T, N], ABC):
    """Abstract base class for value generators"""

    # Add hash method from parent class because it was deleted by Generic
    __hash__ = DAGBaseModel.__hash__

    # Discriminator used by Pydantic
    generatorType: T

    # Value range
    min: N | None = None
    max: N | None = None

    # If `True` value is generated only once and does not change
    once: bool = False

    @model_validator(mode="after")
    def check_min(self):
        if self.min is None:
            self.min = 0    # type: ignore
        if self.min < 0:    # type: ignore
            raise ValueError(f"minimum value has to be 0 or greater")
        return self

    @final
    def __str__(self) -> str:
        """Returns string representations of generator"""
        return self.cpp_type()
    
    @final
    def cpp_type_base(self) -> str:
        """Returns common generator base name"""
        return f"{self.generatorType}Generator"
    
    @abstractmethod
    def value(self) -> N:
        """Specify generator value used when `once` is `True`"""
        pass

    @final
    def N_to_int_str(self, x: float | int) -> str:
        """Converts generic type to string representation for C++ type names"""
        return str(int(round(float(x))))
