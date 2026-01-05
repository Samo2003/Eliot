from typing import Literal, cast
from pydantic import model_validator
from .base import GuardBase
import hashlib

class Payload(GuardBase[Literal["Payload"]]):
    """Check packets payload"""

    # Pattern to match
    pattern: bytes | str

    # Pattern encoding
    encoding: Literal["raw", "ascii", "hex"] = "raw"

    # Initial offset (if negative, counted from the end)
    start: int = 0

    # Offset where to stop checking payload (if negative, counted from the end)
    # Interval is <start, end) 
    end: int | None = None

    # Start checking from L4 layer default is from IP layer
    l4: bool = False 

    @model_validator(mode="after")
    def validate_offsets(self):
        if self.start == self.end:
            raise ValueError("start and end offsets have to be different")
        if len(self.pattern) < 1:
            raise ValueError("invalid pattern")
        if self.end is not None:
            if self.start >= 0 and self.end >= 0 and self.end - self.start < len(self.pattern):
                raise ValueError("invalid pattern length")
            if self.start < 0 and self.end < 0 and self.end - self.start < len(self.pattern):
                raise ValueError("invalid pattern length")
        return self
    
    @model_validator(mode="after")
    def normalize_pattern(self):
        if isinstance(self.pattern, (bytes, bytearray)):
            self.pattern = bytes(self.pattern)
            return self

        if not isinstance(self.pattern, str):
            raise TypeError("pattern must be str or bytes")
        
        if self.encoding == "hex":
            try:
                self.pattern = bytes.fromhex(self.pattern)
            except ValueError:
                raise ValueError("invalid hex pattern")
        elif self.encoding == "ascii":
            try:
                self.pattern = self.pattern.encode("ascii")
            except UnicodeEncodeError:
                raise ValueError("pattern is not valid ASCII")
        else:
            self.pattern = self.pattern.encode("latin1")

        return self
    
    def cpp_type(self) -> str:
        return f"{super().cpp_type_base()}_{hashlib.sha1(cast(bytes, self.pattern)).hexdigest()[:8]}_{self.encoding.upper()}_{self.end}_{self.start}_{self.l4}".replace('.', '_').replace('-', 'neg')
