import socket
import click
from typing import cast
from config import load_config, DEFAULT_CONFIG, DEFAULT_PACKETS
from packet_sequences import Step, load_sequences
import os
from scapy.layers.inet import TCP, UDP, ICMP, IP
from scapy.packet import Packet

def build_packet(step: Step) -> bytes:
    """
    Constructs an IP packet based on the given step

    Payload is randomly filled with specified size
    
    Packet is returned in raw bytes form
    """

    payload = os.urandom(step.payload_size)

    if step.protocol == "udp":
        header = UDP(sport=step.sport, dport=step.dport)
    elif step.protocol == "tcp":
        header = TCP(sport=step.sport, dport=step.dport)
    elif step.protocol == "icmp":
        header = ICMP(type=step.icmp_type, code=step.icmp_code)
    else:
        # Only IP header with random payload when raw protocol provided
        datagram = cast(Packet, IP(src=step.src, dst=step.dst, proto=step.protocol_id) / payload)
        return bytes(datagram)

    # Combines packet headers together with payload
    datagram = cast(Packet, IP(src=step.src, dst=step.dst) / header / payload)
    return bytes(datagram)

def send_step(step: Step, name: str, sock: socket.socket) -> None:
    """
    Sends all packets from a single step

    If send fails step is aborted
    """

    sent = 0
    packet = build_packet(step)

    # Send predefined number od packets
    for _ in range(step.count):
        try:
            sock.send(packet)
            sent += 1
        except Exception as e:
            print(f"[{name}] FAIL protocol={step.protocol} error: {e}")
            return

    print(f"[{name}] DONE protocol={step.protocol} sent={sent}")

@click.command()
@click.option("--config", "-c", type=click.Path(exists=True), default=DEFAULT_CONFIG, help="Test configuration file")
@click.option("--packets", "-p", type=click.Path(exists=True), default=DEFAULT_PACKETS, help="Packets configuration")
def main(config: str, packets: str) -> None:
    """UDP packet sender based on packet specification"""

    try:
        # Load test configurations
        config_model = load_config(config)
        sequences = load_sequences(packets)
    except:
        print("ERROR: Unable to open config files")
        return
    
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        try:
            sock.bind((config_model.client_ip, config_model.client_port))
            sock.connect((config_model.listen_ip, config_model.listen_port))

            # Send all defined sequences
            for seq in sequences:
                print(f"==== SEQUENCE: {seq.name} ====")
                for step in seq.steps:
                    send_step(step, seq.name, sock)
        except Exception as e:
            print(f"ERROR: {e}")

if __name__ == "__main__":
    main()
