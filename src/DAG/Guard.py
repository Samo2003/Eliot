from __future__ import annotations
from pydantic import BaseModel, model_validator, Field
from typing import Literal, Annotated, Union
import ValueGenerator as VG

class GuardBase(BaseModel):
    guardType: str
    invert: bool = False

class Protocol(GuardBase):
    guardType: Literal["protocol"]
    id: int

class ICMP(GuardBase):
    guardType:  Literal["ICMP"]
    type: int | None = None
    code: int | None = None

class IP(GuardBase):
    guardType: Literal["IP"]
    ip: str | None = None
    src: str | None = None
    dst: str | None = None

class Port(GuardBase):
    guardType: Literal["Port"]
    port: int | None = None
    src: int | None = None
    dst: int | None = None

class Size(GuardBase):
    guardType: Literal["Size"]
    size: int
    op: Literal["lt", "le", "eq", "ge", "gt"]

class EveryN(GuardBase):
    guardType: Literal["EveryN"]
    N: int | VG.ValueGeneratorInt

class Prob(GuardBase):
    guardType: Literal["prob"]
    x: float | VG.ValueGeneratorFloat

class Time(GuardBase):
    guardType: Literal["Time"]
    after: float | VG.ValueGeneratorFloat = 0
    duration: float | VG.ValueGeneratorFloat | None = None
    instant: float | VG.ValueGeneratorFloat | None = None

class Count(GuardBase):
    guardType: Literal["Count"]
    after: int | VG.ValueGeneratorInt = 0
    duration: int | VG.ValueGeneratorInt | None = None

class TimePeriod(GuardBase):
    guardType: Literal["TimePeriod"]
    t: float | VG.ValueGeneratorFloat
    f: float | VG.ValueGeneratorFloat | None

    @model_validator(mode="after")
    def set_default_f(self):
        if self.f is None:
            self.f = self.t
        return self
    
class CountPeriod(GuardBase):
    guardType: Literal["CountPeriod"]
    t: int | VG.ValueGeneratorInt
    f: int | VG.ValueGeneratorInt | None

    @model_validator(mode="after")
    def set_default_f(self):
        if self.f is None:
            self.f = self.t
        return self
    

Guard = Annotated[
    Union[
        Protocol,
        ICMP,
        IP,
        Port,
        Size,
        EveryN,
        Prob,
        Time,
        Count,
        TimePeriod,
        CountPeriod
    ],
    Field(discriminator="guardType")
]
