from abc import ABC
from typing import TypeVar, Generic
from ..dag_base_model import DAGBaseModel

T = TypeVar("T", bound=str)

class ActionBase(DAGBaseModel, Generic[T], ABC):
    actionType: T

    def cpp_type(self) -> str:
        return f"{self.actionType}Action"
    
    def is_final(self) -> bool:
        return False
    
    def calendar(self) -> bool:
        return False
    
    def cpp_call(self) -> str:
        if self.is_final():
            raise NotImplementedError
        return super().cpp_call()
