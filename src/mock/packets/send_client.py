import socket
import argparse
import time
from typing import Callable
from config import load_config
from packet_sequences import Step, load_sequences
import os
from typing import cast
from packet_sequences import Step
from scapy.layers.inet import TCP, UDP, ICMP, IP
from scapy.packet import Packet

DEFAULT_CONFIG = "../test_config.json"
DEFAULT_PACKETS = "packets.json"

def build_packet(step: Step) -> bytes:
    payload = os.urandom(step.payload_size)

    if step.protocol == "udp":
        header = UDP(sport=step.sport, dport=step.dport)
    elif step.protocol == "tcp":
        header = TCP(sport=step.sport, dport=step.dport)
    elif step.protocol == "icmp":
        header = ICMP(type=step.icmp_type, code=step.icmp_code)
    else:
        datagram = cast(Packet, IP(src=step.src, dst=step.dst, proto=step.protocol_id) / payload)
        return bytes(datagram)

    datagram = cast(Packet, IP(src=step.src, dst=step.dst) / header / payload)
    return bytes(datagram)

def send_step(step: Step, name: str, send: Callable[[bytes], int]) -> None:
    count = step.count
    protocol = step.protocol

    sent = 0
    start = time.time()
    for _ in range(count):
        packet = build_packet(step)
        try:
            send(packet)
            sent += 1
        except Exception as e:
            print(f"[{protocol}] send error: {e}")

    duration = time.time() - start
    print(f"[{name}] DONE protocol={protocol} sent={sent} duration_s={duration:.3f}")

def main(config_path: str, packets_path: str) -> None:
    try:
        config = load_config(config_path)
        sequences = load_sequences(packets_path)
    except:
        print("ERROR: Unable to open config files")
        return
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except Exception as e:
        print(f"ERROR: {e}")
        return
    
    try:
        anchor_addr = (config.listen_ip, config.listen_port)
        sock.bind((config.client_ip, config.client_port))
        send: Callable[[bytes], int] = lambda packet: sock.sendto(packet, anchor_addr)

        for seq in sequences:
            print(f"==== SEQUENCE: {seq.name} ====")
            for step in seq.steps:
                send_step(step, seq.name, send)
    except Exception as e:
        print(f"ERROR: {e}")
    finally:
        sock.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", "-c", default=DEFAULT_CONFIG)
    parser.add_argument("--packets", "-p", default=DEFAULT_PACKETS)
    args = parser.parse_args()
    main(args.config, args.packets)
