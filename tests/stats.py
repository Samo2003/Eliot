from dataclasses import dataclass
from typing import Dict, List, Set
from tests.comm import ReceivedPacket, SentPacket

@dataclass
class PacketExchange:
    sent: SentPacket
    received: ReceivedPacket | None

    @property
    def has_response(self) -> bool:
        return self.received is not None

    @property
    def rtt(self) -> float | None:
        if not self.received:
            return None
        return self.received.recv_time - self.sent.send_time
    
class ExchangeStats():
    def __init__(self, sent: List[SentPacket], received: List[ReceivedPacket]):
        self.sent_count = len(sent)
        self.sent = sent
        self.received_count = len(received)
        self.received = received

        sent_by_seq: Dict[int, SentPacket] = {
            s.seq: s for s in sent
        }

        recv_by_seq: Dict[int, ReceivedPacket] = {}
        for r in received:
            if r.seq is not None and r.seq not in recv_by_seq:
                recv_by_seq[r.seq] = r

        self.exchanges: List[PacketExchange] = []
        for s in sent:
            self.exchanges.append(
                PacketExchange(
                    sent=s,
                    received=recv_by_seq.get(s.seq)
                )
            ) 

        used_seqs: Set[int] = {
            r.seq for r in recv_by_seq.values()
            if r.seq in sent_by_seq
        }

        self.extra = [
            r for r in received
            if r.seq is None or r.seq not in sent_by_seq or r.seq not in used_seqs
        ]

    def no_losses(self) -> bool:
        return self.sent_count == self.received_count
    
    def only_first_n_have_response(self, n: int) -> bool:
        return all(e.has_response for e in self.exchanges[:n]) and all(not e.has_response for e in self.exchanges[n:])
    
    def bit_diff(self, a: bytes, b: bytes) -> List[int]:
        out: List[int] = []
        for i, (x, y) in enumerate(zip(a, b)):
            d = x ^ y
            for bit in range(8):
                if d & (1 << (7 - bit)):
                    out.append(i * 8 + bit)
        return out
