import socket
import struct
import time
import os
from typing import List, cast
from scapy.layers.inet import TCP, UDP, ICMP, IP
from scapy.packet import Packet, Raw
from scapy.layers.inet6 import IPv6
from ipaddress import ip_address
from dataclasses import dataclass
from .loader import Step

@dataclass
class SentPacket:
    """
    Represents a packet that was transmitted.
    """

    seq: int
    protocol: str
    send_time: float
    raw: bytes

@dataclass
class ReceivedPacket:
    """
    Represents a packet captured as a response.
    """

    recv_time: float
    raw: bytes
    ip_proto: int
    src: str
    dst: str
    sport: int | None
    dport: int | None
    seq: int | None

def build_packet(step: Step, seq: int) -> bytes:
    """
    Construct an IP packet based on step configuration.

    A 4-byte sequence number is appended to payload.
    The resulting packet is returned as raw bytes.
    """

    seq_bytes = struct.pack("!I", seq)

    # Build payload
    if step.payload:
        payload_bytes = cast(bytes, step.payload.value) + seq_bytes
    else:
        payload_len = max(step.payload_size - len(seq_bytes), 0)
        payload_bytes = os.urandom(payload_len) + seq_bytes
    payload = Raw(payload_bytes)

    header: Packet

    # Transport layer header selection
    if step.protocol == "udp":
        header = UDP(sport=step.sport, dport=step.dport)
    elif step.protocol == "tcp":
        header = TCP(sport=step.sport, dport=step.dport)
    elif step.protocol == "icmp":
        header = ICMP(type=step.icmp_type, code=step.icmp_code)
    else:
        # Only IP header with random payload when raw protocol provided
        if ip_address(step.dst).version == 6:
            if ip_address(step.src).version != 6:
                step.src = step.dst
            datagram: Packet = IPv6(src=step.src, dst=step.dst) / payload
        elif ip_address(step.src).version == 6:
            if ip_address(step.dst).version != 6:
                step.dst = step.src
            datagram = IPv6(src=step.src, dst=step.dst) / payload
        else:
            datagram = IP(src=step.src, dst=step.dst, proto=step.protocol_id) / payload
        return bytes(datagram)

    # Combines packet headers together with payload
    if ip_address(step.dst).version == 6:
        if ip_address(step.src).version != 6:
            step.src = step.dst
        datagram = IPv6(src=step.src, dst=step.dst) / header /  payload
    elif ip_address(step.src).version == 6:
        if ip_address(step.dst).version != 6:
            step.dst = step.src
        datagram = IPv6(src=step.src, dst=step.dst) / header / payload
    else:
        datagram = IP(src=step.src, dst=step.dst) / header / payload
    return bytes(datagram)

def send_packets(steps: List[Step], sock: socket.socket) -> List[SentPacket]:
    """
    Send packets defined in test steps.
    """

    sent_packets: List[SentPacket] = []
    seq = 0

    for step in steps:
        # Optional delay before sending this step
        if step.delay:
            time.sleep(step.delay / 1000.0)
        else:
            for i in range(step.count):
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
                
                # Inter-packet interval (ms)
                if i < step.count - 1 and step.interval > 0:
                    time.sleep(step.interval / 1000.0)

    return sent_packets

def receive_packets(sock: socket.socket, timeout: float) -> List[ReceivedPacket]:
    """
    Receive packets until timeout expires.
    """

    packets: List[ReceivedPacket] = []
    sock.settimeout(0.1)

    deadline = time.time() + timeout

    while time.time() < deadline:
        try:
            data, _ = sock.recvfrom(65535)
        except socket.timeout:
            continue

        recv_time = time.time()

        # Parse IPv4 / IPv6
        try:
            ip: Packet = IP(data)
            ip_proto = ip.proto
        except Exception:
            try:
                ip = IPv6(data)
                ip_proto = ip.nh
            except Exception:
                continue

        src = ip.src
        dst = ip.dst
        sport = dport = None

        # Extract transport-level payload
        if TCP in ip:
            sport, dport = ip[TCP].sport, ip[TCP].dport
            payload = bytes(ip[TCP].payload)
        elif UDP in ip:
            sport, dport = ip[UDP].sport, ip[UDP].dport
            payload = bytes(ip[UDP].payload)
        else:
            payload = bytes(ip.payload)

        # Extract appended sequence number
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
