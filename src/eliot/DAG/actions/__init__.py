from typing import Annotated, Union
from pydantic import Field
from .bit_noise import BitNoise
from .set_state import SetState
from .delay import Delay
from .drop import Drop
from .finish import Finish
from .reorder import Reorder
from .replicate import Replicate
from .throttle import Throttle

Action = Annotated[
    Union[
        Finish,
        Drop,
        Delay,
        Reorder,
        Replicate,
        Throttle,
        BitNoise,
        SetState
    ],
    Field(discriminator="type")
]
