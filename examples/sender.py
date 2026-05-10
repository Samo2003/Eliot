import socket
import click
from scapy.layers.inet import ICMP, IP, TCP, UDP
from scapy.packet import Raw

def build_packet(
    protocol: str,
    src_ip: str,
    dst_ip: str,
    sport: int,
    dport: int,
    payload: bytes,
) -> bytes:
    """
    Build a IPv4 packet.
    """

    ip = IP(src=src_ip, dst=dst_ip)

    if protocol == "udp":
        packet = ip / UDP(sport=sport, dport=dport) / Raw(payload)
    elif protocol == "tcp":
        packet = ip / TCP(sport=sport, dport=dport) / Raw(payload)
    elif protocol == "icmp":
        packet = ip / ICMP(type=8, code=0) / Raw(payload)
    else:
        packet = ip / Raw(payload)

    return bytes(packet)

@click.command(
    context_settings={"help_option_names": ["-h", "--help"]},
    help="Send simple IPv4 packets through mocks/mock."
)
@click.option("--eliot-ip", default="127.0.0.1", show_default=True)
@click.option("--eliot-port", default=9000, show_default=True, type=int)
@click.option("--client-ip", default="127.0.0.1", show_default=True)
@click.option("--client-port", default=9001, show_default=True, type=int)
@click.option("--src-ip", default="10.200.0.1", show_default=True)
@click.option("--dst-ip", default="10.200.0.2", show_default=True)
@click.option("--protocol", default="icmp", show_default=True, type=click.Choice(["icmp", "raw", "tcp", "udp"]))
@click.option("--sport", default=12345, show_default=True, type=int)
@click.option("--dport", default=12345, show_default=True, type=int)
@click.option("--count", default=1, show_default=True, type=int)
def main(
    eliot_ip: str,
    eliot_port: int,
    client_ip: str,
    client_port: int,
    src_ip: str,
    dst_ip: str,
    protocol: str,
    sport: int,
    dport: int,
    count: int,
) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((client_ip, client_port))
        sock.connect((eliot_ip, eliot_port))

        for i in range(count):
            payload = f"packet-{i}".encode("ascii")
            packet = build_packet(protocol, src_ip, dst_ip, sport, dport, payload)
            sock.send(packet)
            click.echo(f"sent #{i + 1}: {src_ip}->{dst_ip} proto={protocol} bytes={len(packet)}")

if __name__ == "__main__":
    main()
