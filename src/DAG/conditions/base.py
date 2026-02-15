from abc import ABC
from typing import TypeVar, Generic, final
from ..dag_base_model import DAGBaseModel

# Generic type parameter for condition identifier
T = TypeVar("T", bound=str)

class ConditionBase(DAGBaseModel, Generic[T], ABC):
    """Abstract base class for all conditions"""

    # Discriminator used by Pydantic
    conditionType: T

    # Condition value can be inverted
    invert: bool = False

    @final
    def cpp_type_base(self) -> str:
        """Returns common condition base name"""
        return f"{self.conditionType}Condition"
