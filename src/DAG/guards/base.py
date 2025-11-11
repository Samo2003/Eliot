from abc import ABC
from typing import TypeVar, Generic, final
from ..dag_base_model import DAGBaseModel

# Generic type parameter for guard identifier
T = TypeVar("T", bound=str)

class GuardBase(DAGBaseModel, Generic[T], ABC):
    """Abstract base class for all Guard nodes"""

    # Disciminator used by Pydantic
    guardType: T

    # Guard value can be inverted
    invert: bool = False

    @final
    def cpp_type_base(self) -> str:
        """Returns common guard base name"""
        return f"{self.guardType}Guard"
