from abc import ABC
from typing import TypeVar, Generic, final
from eliot.DAG.dag_base_model import DAGBaseModel

# Generic type parameter for action identifier
T = TypeVar("T", bound=str)

class ActionBase(DAGBaseModel, Generic[T], ABC):
    """
    Abstract base class for Action nodes
    """

    # Discriminator used by Pydantic
    type: T

    @property
    @final
    def cpp_type_base(self) -> str:
        """Returns common action base name"""
        return f"{self.type}Action"
    
    @property
    def is_final(self) -> bool:
        """Signalizes if action is final"""
        return False
    
    @property
    def calendar(self) -> bool:
        """Signalizes that action needs calendar"""
        return False
    
    @property
    def init(self) -> str:
        if self.calendar:
            return f" = {self.cpp_type}(_calendar)"
        return super().init
