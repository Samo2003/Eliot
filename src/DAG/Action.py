from __future__ import annotations
from pydantic import BaseModel, Field, model_validator
from typing import Annotated, Literal, Union
import value_generator as VG

class Finish(BaseModel):
    actionType: Literal["Finish"]

class Drop(BaseModel):
    actionType: Literal["Drop"]

class Delay(BaseModel):
    actionType: Literal["Delay"]
    n: float | VG.ValueGeneratorFloat

class Reorder(BaseModel):
    actionType: Literal["Reorder"]
    n: int | VG.ValueGeneratorInt
    strategy: Literal["random", "reverse"]

class Replicate(BaseModel):
    actionType: Literal["Replicate"]
    n: int | VG.ValueGeneratorInt
    action: Finish | Drop | Delay | BitNoise | SocketTCP

class Throttle(BaseModel):
    actionType: Literal["Throttle"]
    limit: float | VG.ValueGeneratorFloat

class BitNoise(BaseModel):
    actionType: Literal["BitNoise"]
    x: float | VG.ValueGeneratorFloat | None = None
    n: int | VG.ValueGeneratorInt | None = None
    strategy: Literal["left", "right", "random"]
    layer: str | None = None

    @model_validator(mode="after")
    def check_x_or_n(self):
        if (self.x is None and self.n is None) or (self.x is not None and self.n is not None):
            raise ValueError("x or n must be provided")
        if self.x is not None and isinstance(self.x, float) and not (0 <= self.x <= 1):
            raise ValueError("x must be between 0 and 1")
        if self.n is not None and isinstance(self.n, int) and self.n < 0:
            raise ValueError("n must be >= 0")
        return self
    
class SocketTCP(BaseModel):
    actionType: Literal["SocketTCP"]
    ip: str
    port: int
    pack_format: str = ">I"


Action = Annotated[
    Union[
        Finish,
        Drop,
        Delay,
        Reorder,
        Replicate,
        Throttle,
        BitNoise,
        SocketTCP
    ],
    Field(discriminator="actionType")
]
