from pydantic import Field
from typing import Annotated, Union
from .base import ValueGeneratorBase
from . import normal, seq_count, uniform

ValueGeneratorInt = Annotated[
    Union[
        normal.NormalInt, 
        seq_count.SeqCountInt,
        uniform.UniformInt
    ],
    Field(discriminator="generatorType")
]

ValueGeneratorFloat = Annotated[
    Union[
        normal.NormalFloat, 
        seq_count.SeqCountFloat,
        uniform.UniformFloat
    ],
    Field(discriminator="generatorType")
]

__all__ = ["ValueGeneratorInt", "ValueGeneratorFloat", "ValueGeneratorBase"]
