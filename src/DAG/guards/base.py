from abc import ABC
from typing import TypeVar, Generic
from ..dag_base_model import DAGBaseModel

T = TypeVar("T", bound=str)

class GuardBase(DAGBaseModel, Generic[T], ABC):
    guardType: T
    invert: bool = False

    def cpp_type(self) -> str:
        return f"{self.guardType}Guard"
