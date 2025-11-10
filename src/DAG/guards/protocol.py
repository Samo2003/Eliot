from typing import Literal
from .base import GuardBase

class Protocol(GuardBase[Literal["Protocol"]]):
    id: int
