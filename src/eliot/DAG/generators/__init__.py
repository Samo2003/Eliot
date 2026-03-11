from pydantic import Field
from typing import Annotated, TypeAlias, Union
from .base import ValueGeneratorBase
from . import normal, seq_count, uniform, exponential

ValueGeneratorInt = Annotated[
    Union[
        normal.NormalInt, 
        seq_count.SeqCountInt,
        uniform.UniformInt,
        exponential.ExponentialInt
    ],
    Field(discriminator="generatorType")
]

ValueGeneratorFloat = Annotated[
    Union[
        normal.NormalFloat, 
        seq_count.SeqCountFloat,
        uniform.UniformFloat,
        exponential.ExponentialFloat
    ],
    Field(discriminator="generatorType")
]

ValueGenerator: TypeAlias = ValueGeneratorBase[str, int] | ValueGeneratorBase[str, float]

__all__ = ["ValueGeneratorInt", "ValueGeneratorFloat", "ValueGeneratorBase", "ValueGenerator"]
