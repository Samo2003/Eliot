from typing import Literal
from .base import ActionBase

class SocketTCP(ActionBase[Literal["SocketTCP"]]):
    """Sends packet to an external aplication for analyzing"""

    # App IP address
    ip: str

    # App port
    port: int

    # Segment packing format
    pack_format: str = ">I"
