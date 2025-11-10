from typing import Literal
from .base import ActionBase

class SocketTCP(ActionBase[Literal["SocketTCP"]]):
    ip: str
    port: int
    pack_format: str = ">I"
