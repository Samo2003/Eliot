from __future__ import annotations
import hashlib
import re
from typing import Literal
from pydantic import model_validator
from .base import ConditionBase

class Payload(ConditionBase[Literal["Payload"]]):
    """
    Check packets payload
    """

    # Pattern to match
    pattern: bytes | str

    # Pattern type
    pattern_type: Literal["raw", "ascii", "hex", "regex"] = "raw"

    # Initial offset (if negative, counted from the end)
    start: int = 0

    # Offset where to stop checking payload (if negative, counted from the end)
    # Interval is <start, end) 
    end: int | None = None

    # Start checking from L4 layer default is from IP layer
    l4: bool = False 

    @model_validator(mode="after")
    def normalize_pattern(self) -> Payload:
        if self.pattern_type == "regex":
            if not isinstance(self.pattern, str):
                raise TypeError("regex pattern must be a string")
            try:
                re.compile(self.pattern, re.ASCII)
            except re.error as e:
                raise ValueError(f"invalid regex pattern: {e}")
            return self
            
        if isinstance(self.pattern, (bytes, bytearray)):
            self.pattern = bytes(self.pattern)
            return self

        if not isinstance(self.pattern, str):
            raise TypeError("pattern must be str or bytes")
        
        if self.pattern_type == "hex":
            try:
                self.pattern = bytes.fromhex(self.pattern)
            except ValueError:
                raise ValueError("invalid hex pattern")
        elif self.pattern_type == "ascii":
            try:
                self.pattern = self.pattern.encode("ascii")
            except UnicodeEncodeError:
                raise ValueError("pattern is not valid ASCII")
        else:
            self.pattern = self.pattern.encode("latin1")

        return self

    @model_validator(mode="after")
    def validate_offsets(self) -> Payload:
        if self.start == self.end:
            raise ValueError("start and end offsets have to be different")
        if self.pattern_type != "regex":
            if len(self.pattern) < 1:
                raise ValueError("invalid pattern")
            if self.end is not None:
                if self.start >= 0 and self.end >= 0 and self.end - self.start < len(self.pattern):
                    raise ValueError("invalid pattern length")
                if self.start < 0 and self.end < 0 and self.end - self.start < len(self.pattern):
                    raise ValueError("invalid pattern length")
        return self

    @property
    def regex_pattern(self) -> str:
        if self.pattern_type != "regex":
            raise TypeError("regex_pattern used for non-regex type")
        if not isinstance(self.pattern, str):
            raise TypeError("regex pattern must be string")

        return self.pattern.encode("unicode_escape").decode("ascii")

    @property
    def cpp_type(self) -> str:
        if isinstance(self.pattern, bytes):
            pattern_bytes = self.pattern
        elif isinstance(self.pattern, str):
            pattern_bytes = self.pattern.encode("utf-8")
        else:
            raise TypeError("invalid pattern type")

        return (
            f"{self.cpp_type_base}_"
            f"{hashlib.sha1(pattern_bytes).hexdigest()[:8]}_"
            f"{self.pattern_type.upper()}_"
            f"{self.end}_"
            f"{self.start}_"
            f"{self.l4}"
        ).replace('-', 'neg')
