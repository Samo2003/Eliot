from typing import Literal
from .base import GuardBase

class IP(GuardBase[Literal["IP"]]):
    ip: str | None = None
    src: str | None = None
    dst: str | None = None
