from .base import NFQueueApiBase

class EchoApi(NFQueueApiBase):
    """NFQueue Echo API definition"""

    def include(self) -> str:
        return "<nf_queue_echo.hpp>"

    def type(self) -> str:
        return "nf_queue_echo::NFQueue"
    
    def get_packet(self) -> str:
        return ".get_packet()"
    
    def accept_packet(self, packet_str: str) -> str:
        return f".accept_packet({packet_str})"
    
    def drop_packet(self, packet_str: str) -> str:
        return f".drop_packet({packet_str})"
    
    def packet_type(self) -> str:
        return "nf_queue_echo::NFQueuePacket"
    
    def packet_payload(self) -> str:
        return "get_payload()"
    