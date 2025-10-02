from __future__ import annotations
from typing import Annotated, Literal, Union
from pydantic import BaseModel, Field, model_validator

class ValueGeneratorBase(BaseModel):
    once: bool = False
    generatorType: str

class SeqCountBase(BaseModel):
    T: int = 1
    mode: Literal["repeat", "keep", "reverse"]

    @model_validator(mode="after")
    def check_consistency(self):
        if self.step == 0:
            raise ValueError("step must not be 0")

        if self.step > 0:
            if self.min is None:
                raise ValueError("min is required for increasing sequence (step > 0)")
        elif self.step < 0:
            if self.max is None:
                raise ValueError("max is required for decreasing sequence (step < 0)")

        return self

class ValueGeneratorBaseInt(ValueGeneratorBase):
    min: int | None = None
    max: int | None = None

class NormalInt(ValueGeneratorBaseInt):
    generatorType: Literal["NormalInt"]
    m: float
    s: float

class UniformInt(ValueGeneratorBaseInt):
    generatorType: Literal["UniformInt"]
    min: int
    max: int

class SeqCountInt(SeqCountBase, ValueGeneratorBaseInt):
    generatorType: Literal["SeqCountInt"]
    step: int

ValueGeneratorInt = Annotated[
    Union[
        NormalInt,
        UniformInt,
        SeqCountInt
    ],
    Field(discriminator="generatorType")
]

class ValueGeneratorBaseFloat(ValueGeneratorBase):
    min: float | None = None
    max: float | None = None

class NormalFloat(ValueGeneratorBaseFloat):
    generatorType: Literal["NormalFloat"]
    m: float
    s: float

class UniformFloat(ValueGeneratorBaseFloat):
    generatorType: Literal["UniformFloat"]
    min: float
    max: float

class SeqCountFloat(ValueGeneratorBaseFloat, SeqCountBase):
    generatorType: Literal["SeqCountFloat"]
    step: float

ValueGeneratorFloat = Annotated[
    Union[
        NormalFloat,
        UniformFloat,
        SeqCountFloat
    ],
    Field(discriminator="generatorType")
]
