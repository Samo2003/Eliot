import socket
import struct
import time
from typing import List, cast
from tests.loader import Step
import os
from scapy.layers.inet import TCP, UDP, ICMP, IP
from scapy.packet import Packet, Raw
from scapy.layers.inet6 import IPv6
import ipaddress
from dataclasses import dataclass
from typing import Optional

@dataclass
class SentPacket:
    seq: int
    protocol: str
    send_time: float
    raw: bytes

@dataclass
class ReceivedPacket:
    recv_time: float
    raw: bytes
    ip_proto: int
    src: str
    dst: str
    sport: Optional[int]
    dport: Optional[int]
    seq: int | None

def build_packet(step: Step, seq: int) -> bytes:
    """
    Constructs an IP packet based on the given step

    Payload is randomly filled with specified size
    
    Packet is returned in raw bytes form
    """

    seq_bytes = struct.pack("!I", seq)
    payload_len = max(step.payload_size - len(seq_bytes), 0)
    payload = Raw(os.urandom(payload_len) + seq_bytes)

    header: Packet

    if step.protocol == "udp":
        header = UDP(sport=step.sport, dport=step.dport)
    elif step.protocol == "tcp":
        header = TCP(sport=step.sport, dport=step.dport)
    elif step.protocol == "icmp":
        header = ICMP(type=step.icmp_type, code=step.icmp_code)
    else:
        # Only IP header with random payload when raw protocol provided
        if ipaddress.ip_address(step.dst).version == 6:
            if ipaddress.ip_address(step.src).version != 6:
                step.src = step.dst
            datagram = cast(Packet, IPv6(src=step.src, dst=step.dst) / payload)
        elif ipaddress.ip_address(step.src).version == 6:
            if ipaddress.ip_address(step.dst).version != 6:
                step.dst = step.src
            datagram = cast(Packet, IPv6(src=step.src, dst=step.dst) / payload)
        else:
            datagram = cast(Packet, IP(src=step.src, dst=step.dst, proto=step.protocol_id) / payload)

        # datagram = cast(Packet, IP(src=step.src, dst=step.dst, proto=step.protocol_id) / payload)
        return bytes(datagram)

    # Combines packet headers together with payload
    if ipaddress.ip_address(step.dst).version == 6:
        if ipaddress.ip_address(step.src).version != 6:
            step.src = step.dst
        datagram = cast(Packet, IPv6(src=step.src, dst=step.dst) / header /  payload)
    elif ipaddress.ip_address(step.src).version == 6:
        if ipaddress.ip_address(step.dst).version != 6:
            step.dst = step.src
        datagram = cast(Packet, IPv6(src=step.src, dst=step.dst) / header / payload)
    else:
        datagram = cast(Packet, IP(src=step.src, dst=step.dst) / header / payload)
    return bytes(datagram)

def send_packets(steps: List[Step], sock: socket.socket) -> List[SentPacket]:
    sent_packets: List[SentPacket] = []
    seq = 0

    for step in steps:

        for _ in range(step.count):
            try:
                packet = build_packet(step, seq)
                now = time.time()
                sock.send(packet)

                sent_packets.append(
                    SentPacket(
                        seq=seq,
                        protocol=step.protocol,
                        send_time=now,
                        raw=packet,
                    )
                )

                seq += 1

            except Exception as e:
                raise RuntimeError(f"Send failed: {e}")

    return sent_packets

def receive_packets(sock: socket.socket, timeout: float) -> List[ReceivedPacket]:
    packets: List[ReceivedPacket] = []
    sock.settimeout(0.1)

    deadline = time.time() + timeout

    while time.time() < deadline:
        try:
            data, _ = sock.recvfrom(65535)
        except socket.timeout:
            continue

        recv_time = time.time()
        try:
            ip = IP(data)
        except Exception:
            continue

        src = ip.src
        dst = ip.dst
        ip_proto = ip.proto
        sport = dport = None

        if TCP in ip:
            sport, dport = ip[TCP].sport, ip[TCP].dport
            payload = bytes(ip[TCP].payload)
        elif UDP in ip:
            sport, dport = ip[UDP].sport, ip[UDP].dport
            payload = bytes(ip[UDP].payload)
        else:
            payload = bytes(ip.payload)

        seq = None
        if len(payload) >= 4:
            try:
                seq = int(struct.unpack("!I", payload[-4:])[0])
            except struct.error:
                pass

        packets.append(
            ReceivedPacket(
                recv_time=recv_time,
                raw=data,
                ip_proto=ip_proto,
                src=src,
                dst=dst,
                sport=sport,
                dport=dport,
                seq=seq,
            )
        )

    assert all(p.seq is not None for p in packets)

    return packets
