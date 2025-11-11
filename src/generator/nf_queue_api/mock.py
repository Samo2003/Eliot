from .base import NFQueueApiBase

class MockApi(NFQueueApiBase):
    """NFQueue Mock API definition"""

    def include(self) -> str:
        return "<nf_queue_mock.hpp>"

    def type(self) -> str:
        return "nf_queue_mock::NFQueue"
    
    def get_packet(self) -> str:
        return ".get_packet()"
    
    def accept_packet(self, packet_str: str) -> str:
        return f".accept_packet({packet_str})"
    
    def drop_packet(self, packet_str: str) -> str:
        return f".drop_packet({packet_str})"
    
    def packet_type(self) -> str:
        return "nf_queue_mock::NFQueuePacket"
    
    def packet_payload(self) -> str:
        return "get_payload()"
    