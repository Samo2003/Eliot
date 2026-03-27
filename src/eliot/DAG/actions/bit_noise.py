from __future__ import annotations
from typing import Literal
from pydantic import model_validator
from eliot.DAG.generators import ValueGeneratorInt, ValueGeneratorFloat, ValueGeneratorBase
from .base import ActionBase

class BitNoise(ActionBase[Literal["BitNoise"]]):
    """
    Inserts bit noise into the packet
    """

    # Part of bits from given window to invert <0,1>
    x: float | ValueGeneratorFloat | None = None

    # Number of bits to invert
    n: int | ValueGeneratorInt | None = None

    # Offset in bits where to start inverting bits
    # (if negative bits are counted from the end)
    start: int | ValueGeneratorInt = 0

    # Offset in bits where to stop inverting bits
    # (if negative bits are counted from the end)
    # Interval is <start, end)
    end: int | ValueGeneratorInt | None = None

    # Bit selection mode
    mode: Literal["random", "first", "last"] = "random"

    # Layer to invert bits, offset are counted only in this layer
    layer: Literal["IP", "L4", "any"] = "any"

    @model_validator(mode="after")
    def check_x_or_n(self) -> BitNoise:
        """Only n or x can be provided"""
        if (
            (self.x is None and self.n is None) 
            or (self.x is not None and self.n is not None)
        ):
            raise ValueError("x or n must be provided")
        if self.x is not None and isinstance(self.x, float) and not (0 <= self.x <= 1):
            raise ValueError("x must be between 0 and 1")
        if self.x is not None and isinstance(self.x, ValueGeneratorBase):
            if not (0 <= self.x.min <= 1):
                raise ValueError("x must be between 0 and 1")
            if self.x.max is None:
                self.x.max = 1
            elif not (0 <= self.x.max <= 1):
                raise ValueError("x must be between 0 and 1")
            if self.x.min > self.x.max:
                raise ValueError("Generator cannot produce values")
        if self.n is not None:
            if isinstance(self.n, int) and self.n <= 0:
                raise ValueError("n must be > 0")
            elif isinstance(self.n, ValueGeneratorBase) and self.n.min <= 0:
                raise ValueError("n must be > 0")
        if self.end is not None:
            if isinstance(self.start, int) and isinstance(self.end, int):
                if self.start == self.end:
                    raise ValueError("start and end offsets have to be different")
                if self.start >= 0 and self.end >= 0 and self.end - self.start < 0:
                    raise ValueError("invalid window length")
                if self.start < 0 and self.end < 0 and self.end - self.start < 0:
                    raise ValueError("invalid window length")
        return self
    
    @property
    def cpp_type(self) -> str:
        type_name = (
            f"{self.cpp_type_base}_"
            f"{self.x}_"
            f"{self.n}_"
            f"{self.start}_"
            f"{self.end}_"
            f"{self.mode.upper()}_"
            f"{self.layer.upper()}"
        )

        state_x = isinstance(self.x, ValueGeneratorBase) and self.x.is_state
        state_n = isinstance(self.n, ValueGeneratorBase) and self.n.is_state
        state_start = isinstance(self.start, ValueGeneratorBase) and self.start.is_state
        state_end = isinstance(self.end, ValueGeneratorBase) and self.end.is_state
        if state_x or state_n or state_start or state_end or self.mode == "random":
            type_name += f"{id(self)}"
        return type_name.replace('-', "neg").replace('.', '_')
    
    @property
    def not_generator_x(self) -> bool:
        """Condition used in generating representing if x is a generator"""
        return isinstance(self.x, float)
    
    @property
    def not_generator_n(self) -> bool:
        """Condition used in generating representing if n is a generator"""
        return isinstance(self.n, int)
    
    @property
    def not_generator_start(self) -> bool:
        """Condition used in generating representing if start is a generator"""
        return isinstance(self.start, int)
    
    @property
    def not_generator_end(self) -> bool:
        """Condition used in generating representing if end is a generator"""
        return isinstance(self.end, int)
