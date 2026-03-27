from dataclasses import dataclass
from typing import Dict, List, Set
from .comm import ReceivedPacket, SentPacket

@dataclass
class PacketExchange:
    """
    Represents a single request-response pair.

    Each exchange consists of one sent packet and an optional
    received response packet.
    """

    sent: SentPacket
    received: ReceivedPacket | None

    @property
    def has_response(self) -> bool:
        """
        Indicates whether a response was received.
        """
        return self.received is not None

    @property
    def rtt(self) -> float | None:
        """
        Computes round-trip time (RTT) in seconds.

        Returns:
            None if no response was received.
        """
        if not self.received:
            return None
        return self.received.recv_time - self.sent.send_time
    
class ExchangeStats:
    """
    Computes statistics and relationships between sent and received packets.
    """

    def __init__(self, sent: List[SentPacket], received: List[ReceivedPacket]):
        self.sent_count = len(sent)
        self.sent = sent
        self.received_count = len(received)
        self.received = received

        # Map sent packets by sequence number for quick lookup
        sent_by_seq: Dict[int, SentPacket] = {
            s.seq: s for s in sent
        }

        # Map first received packet per sequence number
        recv_by_seq: Dict[int, ReceivedPacket] = {}
        for r in received:
            if r.seq is not None and r.seq not in recv_by_seq:
                recv_by_seq[r.seq] = r

        # Build request-response exchanges
        self.exchanges = [
            PacketExchange(
                sent=s,
                received=recv_by_seq.get(s.seq)
            )
            for s in sent
        ]

        # Track sequence numbers that were successfully matched
        used_seqs: Set[int] = {
            r.seq for r in recv_by_seq.values()
            if r.seq in sent_by_seq
        }

        self.extra = [
            r for r in received
            if r.seq is None or r.seq not in sent_by_seq or r.seq not in used_seqs
        ]

    @property
    def no_losses(self) -> bool:
        """
        Returns True all exchanges have response
        """
        return all(e.has_response for e in self.exchanges)
    
    def only_first_n_have_response(self, n: int) -> bool:
        """
        Checks whether only the first n exchanges have responses,
        and all remaining exchanges are missing responses.
        """
        return (
            all(e.has_response for e in self.exchanges[:n]) 
            and all(not e.has_response for e in self.exchanges[n:])
        )
    
    def bit_diff(self, a: bytes, b: bytes) -> List[int]:
        """
        Computes bit-level differences between two byte sequences.

        Returns:
            List of bit indices (0-based) that differ.
        """
        out: List[int] = []
        for i, (x, y) in enumerate(zip(a, b)):
            d = x ^ y
            for bit in range(8):
                if d & (1 << (7 - bit)):
                    out.append(i * 8 + bit)
        return out
