from typing import Literal
from .base import GuardBase

class ICMP(GuardBase[Literal["ICMP"]]):
    type: int | None = None
    code: int | None = None
