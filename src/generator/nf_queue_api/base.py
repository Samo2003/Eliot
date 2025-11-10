from abc import ABC

class NFQueueApiBase(ABC):
    def include(self) -> str:
        raise NotImplementedError
    
    def packet_type(self) -> str:
        raise NotImplementedError
    
    def packet_payload(self) -> str:
        raise NotImplementedError

    def type(self) -> str:
        raise NotImplementedError
    
    def get_packet(self) -> str:
        raise NotImplementedError
    
    def accept_packet(self, packet_str: str) -> str:
        raise NotImplementedError
    
    def drop_packet(self, packet_str: str) -> str:
        raise NotImplementedError
