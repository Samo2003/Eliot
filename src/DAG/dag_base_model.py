from pydantic import BaseModel

class DAGBaseModel(BaseModel):
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self.cpp_type() == other.cpp_type()

    def __hash__(self) -> int:
        return hash(self.cpp_type())
    
    def cpp_type(self) -> str:
        raise NotImplementedError
    
    def hpp_define(self) -> str:
        return f"NETLOITER_{self.cpp_type().upper()}_H"
    
    def cpp_name(self) -> str:
        return self.cpp_type().lower()
    
    def cpp_call(self) -> str:
        if self.is_state():
            return f"({self.cpp_name()}, "
        return f"<{self.cpp_type()}>("
    
    def is_state(self) -> bool:
        return False
    
    def init(self) -> str:
        return ""
