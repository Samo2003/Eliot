from typing import Any, Literal
from pydantic import field_validator, model_validator
from .base import GuardBase
import hashlib

class Payload(GuardBase[Literal["Payload"]]):
    """Check packets payload"""

    # Pattern to match
    pattern: bytes

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
        if len(self.pattern) < 1:
            raise ValueError("invalid pattern length")
        return self
    
    @field_validator("pattern", mode="before")
    @classmethod
    def convert_pattern(cls, v: Any, info: Any) -> bytes:
        if isinstance(v, (bytes, bytearray)):
            return bytes(v)
        
        if not isinstance(v, str):
            raise TypeError("pattern must be str or bytes")
        
        encoding = info.data.get("encoding", "raw")
        
        if encoding == "hex":
            try:
                return bytes.fromhex(v)
            except ValueError:
                raise ValueError("invalid hex pattern")

        if encoding == "ascii":
            try:
                return v.encode("ascii")
            except UnicodeEncodeError:
                raise ValueError("pattern is not valid ASCII")

        if encoding == "raw":
            return v.encode("latin1")

        raise ValueError(f"unknown encoding: {encoding}")
    
    def cpp_type(self) -> str:
        return f"{super().cpp_type_base()}_{hashlib.sha1(self.pattern).hexdigest()[:8]}_{self.encoding.upper()}_{self.max}_{self.start}_{self.l4}"
