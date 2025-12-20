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

    # Maximum number of bytes to check
    max: int | None = None

    # Initial offset
    start: int = 0

    # Start checking from L4 layer default is from IP layer
    l4: bool = False 

    @model_validator(mode="after")
    def validate_offsets(self):
        if self.max is not None and self.max < 0:
            raise ValueError("max offset must be non negative")
        if self.start < 0:
            raise ValueError("start offset must be non negative")
        if len(self.pattern) < 1 or (self.max is not None and len(self.pattern) > self.max):
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
        return f"{super().cpp_type_base()}_{hashlib.sha1(cast(bytes, self.pattern)).hexdigest()[:8]}_{self.encoding.upper()}_{self.max}_{self.start}_{self.l4}"
