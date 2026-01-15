from pathlib import Path
from pydantic import BaseModel, model_validator
import yaml
from typing import Any, Dict, List, Literal, cast
from src.DAG.dag import DAG
from src.test_case.test_case import TestCase

class Payload(BaseModel):
    value: bytes | str
    encoding: Literal["raw", "ascii", "hex"] = "raw"

    @model_validator(mode="after")
    def normalize_pattern(self):
        if isinstance(self.value, (bytes, bytearray)):
            self.value = bytes(self.value)
            return self

        if not isinstance(self.value, str):
            raise TypeError("value must be str or bytes")
        
        if self.encoding == "hex":
            try:
                self.value = bytes.fromhex(self.value)
            except ValueError:
                raise ValueError("invalid hex pattern")
        elif self.encoding == "ascii":
            try:
                self.value = self.value.encode("ascii")
            except UnicodeEncodeError:
                raise ValueError("value is not valid ASCII")
        else:
            self.value = self.value.encode("latin1")

        return self

class Step(BaseModel):
    """Packet step configuration representation"""
    protocol: Literal["udp", "tcp", "icmp", "raw"] = "raw"
    protocol_id: int = 99
    src: str = "10.10.10.1"
    dst: str = "10.10.10.2"
    count: int = 1
    payload_size: int = 256
    payload: Payload | None = None
    sport: int = 12345
    dport: int = 54321
    icmp_type: int = 8
    icmp_code: int = 0
    delay: float | None = None

class Case(BaseModel):
    """Test case representation"""
    name: str
    timeout: int = 1
    send: List[Step]
    build: TestCase | DAG

    @model_validator(mode="before")
    @classmethod
    def resolve_build(cls, data: Any):
        if not isinstance(data, dict):
            return data
        
        raw = cast(Dict[str, Any], data)

        build = raw.get("build")
        if not isinstance(build, dict):
            return raw

        if "rules" in build or "defaultAction" in build:
            raw["build"] = TestCase.model_validate(build)
            return raw

        if "root" in build:
            raw["build"] = DAG.model_validate(build)
            return raw

        raise ValueError("Unknown build format, expected TestCase or DAG")

def load_case(path: Path):
    with open(path) as f:
        data = yaml.safe_load(f)
    return Case.model_validate(data)
