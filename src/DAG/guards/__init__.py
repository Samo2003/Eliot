from typing import Annotated, Union
from pydantic import Field
from .icmp import ICMP
from .ip import IP
from .protocol import Protocol
from .port import Port
from .size import Size
from .every_n import EveryN
from .prob import Prob
from .time import Time
from .count import Count
from .time_period import TimePeriod
from .count_period import CountPeriod
from .payload import Payload
from .ip_version import IPVersion

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
        CountPeriod,
        Payload,
        IPVersion
    ],
    Field(discriminator="guardType")
]
