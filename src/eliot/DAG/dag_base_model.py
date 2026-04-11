from abc import ABC, abstractmethod
import random
from typing import final
from pydantic import BaseModel

# Unit scale factors for time conversion to milliseconds
FACTORS = {
    "ms": 1,
    "s": 1000,
    "min": 60000,
    "h": 3600000
}

class DAGBaseModel(BaseModel, ABC):
    """
    Abstract base class for all semantic DAG elements.
    """

    def __hash__(self) -> int:
        """
        Allows DAG elements to be used in sets.
        """

        return hash(self.cpp_type)
    
    @property
    @abstractmethod
    def cpp_type(self) -> str:
        """
        Return the C++ type name.

        Must be implemented by each concrete DAG element.
        """
        pass

    @property
    @final  
    def hpp_define(self) -> str:
        """
        Returns C++ header define.
        """

        return f"ELIOT_{self.cpp_type.upper()}_H"
    
    @property
    @final
    def cpp_name(self) -> str:
        """
        Return standardized C++ variable name derived from type.
        """

        return self.cpp_type.lower()
    
    @property
    def cpp_call(self) -> str:
        """
        Defines C++ formatted call based on state.
        """
        if self.is_state:
            return f"({self.cpp_name}, "
        return f"<{self.cpp_type}>("
    
    @property
    def is_state(self) -> bool:
        """Defines if node is state or not"""
        return False
    
    @property
    def init(self) -> str:
        """Initialization if required"""
        return ""
    
    @property
    def time(self) -> bool:
        """
        Signal whether the element requires time-related support.

        Used to conditionally include time utilities
        in the generated code.
        """

        return False
    
    @property
    def seed_value(self) -> int:
        """
        Generate a 32-bit random seed value.
        """

        return random.getrandbits(32)
