from .base import NFQueueApiBase

class ProfilingApi(NFQueueApiBase):
    """NFQueue Profiling API definition"""
    def include(self) -> str:
        return "<nf_queue_profiling.hpp>"

    def type(self) -> str:
        return "nf_queue_profiling::NFQueue"
    
    def get_packet(self) -> str:
        return ".get_packet()"
    
    def accept_packet(self, packet_str: str) -> str:
        return f".accept_packet({packet_str})"
    
    def drop_packet(self, packet_str: str) -> str:
        return f".drop_packet({packet_str})"
    
    def packet_type(self) -> str:
        return "nf_queue_profiling::NFQueuePacket"
    
    def packet_payload(self) -> str:
        return "get_payload()"
    
    def returns_optional(self) -> bool:
        return False