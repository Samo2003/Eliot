from abc import ABC, abstractmethod
from typing import final
from pydantic import BaseModel

class DAGBaseModel(BaseModel, ABC):
    """Abstract base class for all DAG nodes"""

    @final
    def __hash__(self) -> int:
        """Allows DAG nodes to be used in sets"""
        return hash(self.cpp_type())
    
    @abstractmethod
    def cpp_type(self) -> str:
        """Returns C++ type name"""
        pass

    @final  
    def hpp_define(self) -> str:
        """Returns C++ header define"""
        return f"NETLOITER_{self.cpp_type().upper()}_H"
    
    @final
    def cpp_name(self) -> str:
        """Return C++ variable name"""
        return self.cpp_type().lower()
    
    def cpp_call(self) -> str:
        """Defines C++ formated call based on state"""
        if self.is_state():
            return f"({self.cpp_name()}, "
        return f"<{self.cpp_type()}>("
    
    def is_state(self) -> bool:
        """Defines if node is state or not"""
        return False
    
    def init(self) -> str:
        """Initialization if required"""
        return ""
