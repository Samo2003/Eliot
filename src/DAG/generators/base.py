from abc import ABC, abstractmethod
from typing import TypeVar, Generic, final
from ..dag_base_model import DAGBaseModel

# Generic type parameter for generator identifier
T = TypeVar("T", bound=str)

# Generic type parameter for generator type
N = TypeVar("N", int, float)

class ValueGeneratorBase(DAGBaseModel, Generic[T, N], ABC):
    """Abstract base class for value generators"""

    # Add hash method from parent class because it was deleted by Generic
    __hash__ = DAGBaseModel.__hash__

    # Disciminator used by Pydantic
    generatorType: T

    # Value range
    min: N | None = None
    max: N | None = None

    # If `True` valua is generated only once and does not change
    once: bool = False

    @final
    def __str__(self) -> str:
        """Returns string representations of generator"""
        return self.cpp_type()
    
    @final
    def cpp_type_base(self) -> str:
        """Returns common generator basee name"""
        return f"{self.generatorType}Generator"
    
    @abstractmethod
    def value(self) -> N:
        """Specify generator value used when `once` is `True`"""
        pass

    @final
    def N_to_int_str(self, x: N) -> str:
        """Converts generic type to string representation for C++ type names"""
        return str(int(round(float(x))))
