import socket
import time
import click
from scapy.layers.inet import IP, TCP, UDP
from scapy.packet import Raw
from config import load_config

PROTO_NAMES = {
    1: "icmp",
    6: "tcp",
    17: "udp",
}

def describe_packet(data: bytes) -> str | None:
    """
    Parse a IPv4 packet and return a short description.
    """

    try:
        packet = IP(data)
    except Exception:
        return None

    proto = PROTO_NAMES.get(packet.proto, str(packet.proto))
    extra = ""
    payload = ""

    if TCP in packet:
        extra = f" ports={packet[TCP].sport}->{packet[TCP].dport}"
    elif UDP in packet:
        extra = f" ports={packet[UDP].sport}->{packet[UDP].dport}"

    if Raw in packet:
        raw_payload = bytes(packet[Raw].load)
        try:
            payload = f" payload={raw_payload.decode('ascii')}"
        except UnicodeDecodeError:
            payload = f" payload=0x{raw_payload.hex()}"

    return f"{packet.src}->{packet.dst} proto={proto}{extra}{payload} bytes={len(data)}"

@click.command(
    context_settings={"help_option_names": ["-h", "--help"]},
    help="Receive packets forwarded by mocks/mock."
)
@click.option("--timeout", default=30.0, show_default=True, type=float)
def main(timeout: float) -> None:
    config = load_config()
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((config.server_ip, config.server_port))
        sock.settimeout(0.1)

        click.echo(f"receiver listening on {config.server_ip}:{config.server_port}")
        deadline = time.time() + timeout
        received = 0

        while time.time() < deadline:
            try:
                data, _ = sock.recvfrom(65535)
            except socket.timeout:
                continue

            description = describe_packet(data)
            if description is None:
                continue

            received += 1
            click.echo(f"recv #{received}: {description}")

    click.echo(f"received={received}")

if __name__ == "__main__":
    main()
