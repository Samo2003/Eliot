from typing import Literal
from .base import GuardBase

class Port(GuardBase[Literal["Port"]]):
    port: int | None = None
    src: int | None = None
    dst: int | None = None
