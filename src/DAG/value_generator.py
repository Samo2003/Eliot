from __future__ import annotations
from typing import Annotated, Literal, Union
from pydantic import BaseModel, Field, model_validator

class ValueGeneratorBase(BaseModel):
    once: bool = False

class SeqCountBase(BaseModel):
    T: int = 1
    mode: Literal["repeat", "keep", "reverse"]

    @model_validator(mode="after")
    def check_consistency(self):
        step = getattr(self, "step", None)
        minv = getattr(self, "min", None)
        maxv = getattr(self, "max", None)
        if step is None or step == 0:
            raise ValueError("step must not be 0")

        if step > 0:
            if minv is None:
                raise ValueError("min is required for increasing sequence (step > 0)")
        elif step < 0:
            if maxv is None:
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

    @model_validator(mode="after")
    def ensure_min_max(self):
        if self.min is None or self.max is None:
            raise ValueError("min and max must be provided for UniformInt")
        return self

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

    @model_validator(mode="after")
    def ensure_min_max(self):
        if self.min is None or self.max is None:
            raise ValueError("min and max must be provided for UniformFloat")
        return self

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
