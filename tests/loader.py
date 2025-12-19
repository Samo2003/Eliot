from pathlib import Path
from pydantic import BaseModel
import yaml
from typing import List, Literal
from src.test_case.test_case import TestCase

class Step(BaseModel):
    """Packet step configuration representation"""
    protocol: Literal["udp", "tcp", "icmp", "raw"] = "raw"
    protocol_id: int = 99
    src: str = "10.10.10.1"
    dst: str = "10.10.10.2"
    count: int = 1
    payload_size: int = 256
    sport: int = 12345
    dport: int = 54321
    icmp_type: int = 8
    icmp_code: int = 0

class Case(BaseModel):
    """Test case representation"""
    name: str
    timeout: int = 1
    send: List[Step]
    build: TestCase

def load_case(path: Path):
    with open(path) as f:
        data = yaml.safe_load(f)
    return Case.model_validate(data)
