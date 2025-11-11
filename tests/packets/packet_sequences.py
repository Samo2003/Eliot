from pydantic import BaseModel
from typing import List, Literal
import json

class Step(BaseModel):
    """Packet step configuration representation"""
    protocol: Literal["udp", "tcp", "icmp", "raw"]
    protocol_id: int = 99
    src: str = "10.10.10.1"
    dst: str = "10.10.10.2"
    count: int = 1
    payload_size: int = 256
    sport: int = 12345
    dport: int = 54321
    icmp_type: int = 8
    icmp_code: int = 0

class Sequence(BaseModel):
    """Packet sequence configuration representation"""
    name: str
    steps: List[Step]

def load_sequences(sequences_path: str) -> List[Sequence]:
    """Loads sequences from `sequences_path`"""
    try:
        with open(sequences_path, "r") as file:
            data = json.load(file)
        sequences = [Sequence.model_validate(seq) for seq in data]
    except:
        raise RuntimeError("Unable to load packets config")
    
    return sequences
    