from pydantic import Field
from typing import Annotated, TypeAlias, Union
from .base import ValueGeneratorBase
from . import normal, seq, uniform, exponential

ValueGeneratorInt = Annotated[
    Union[
        normal.NormalInt, 
        seq.SeqCountInt,
        seq.SeqTimeInt,
        uniform.UniformInt,
        exponential.ExponentialInt
    ],
    Field(discriminator="type")
]

ValueGeneratorFloat = Annotated[
    Union[
        normal.NormalFloat, 
        seq.SeqCountFloat,
        seq.SeqTimeFloat,
        uniform.UniformFloat,
        exponential.ExponentialFloat
    ],
    Field(discriminator="type")
]

ValueGenerator: TypeAlias = ValueGeneratorBase[str, int] | ValueGeneratorBase[str, float]

__all__ = ["ValueGeneratorInt", "ValueGeneratorFloat", "ValueGeneratorBase", "ValueGenerator"]
