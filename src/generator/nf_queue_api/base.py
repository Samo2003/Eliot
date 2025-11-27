from abc import ABC, abstractmethod

class NFQueueApiBase(ABC):
    """
    Abstract base class defining mandatory functions to define 
    for NFQueue API implementation to use in generator
    """

    @abstractmethod
    def include(self) -> str:
        """Library name to include in source code"""
        pass

    @abstractmethod
    def type(self) -> str:
        """Implemented queue type"""
        pass
    
    @abstractmethod
    def get_packet(self) -> str:
        """
        Method to receive packet from queue

        Example: .get()
        """
        pass
    
    @abstractmethod
    def accept_packet(self, packet_str: str) -> str:
        """
        Method to accept packet with move parameter

        Example: .accept({packet_str})
        """
        pass
    
    @abstractmethod
    def drop_packet(self, packet_str: str) -> str:
        """
        Method to drop packet with move parameter

        Example: .drop({packet_str})
        """
        pass

    @abstractmethod
    def packet_type(self) -> str:
        """Implemented packet type"""
        pass
    
    @abstractmethod
    def packet_payload(self) -> str:
        """
        Method to access packet payload
        
        Example: get()
        """
        pass

    def returns_optional(self) -> bool:
        """
        Defines if get_packet return optional packet or reference
        
        Used for profiling
        """
        return True
