import socket
import argparse
from collections import defaultdict
from typing import Dict
from scapy.layers.inet import IP, TCP, UDP, ICMP
from config import load_config

class Stats():
    def __init__(self) -> None:
        self.__total_packets: int = 0
        self.__parse_errors: int = 0
        self.__by_protocol: Dict[int, int] =  defaultdict(int)

    def __protocol(self, protocol: int) -> str:
        if protocol == 1:
            return "ICMP"
        if protocol == 6:
            return "TCP"
        if protocol == 17:
            return "UDP"
        return "RAW"

    def print(self) -> None:
        print("==== STATS ====")
        print(f"  Packets: {self.__total_packets}")
        print(f"  Parse errors: {self.__parse_errors}")
        for protocol, count in self.__by_protocol.items():
            print(f"    {self.__protocol(protocol)}: {count}")

    def inc_packets(self) -> None:
        self.__total_packets += 1
    
    def inc_errors(self) -> None:
        self.__parse_errors += 1

    def inc_protocol(self, protocol: int) -> None:
        self.__by_protocol[protocol] += 1

def main(config_path: str, verbose: bool) -> None:
    try:
        config = load_config(config_path)
    except:
        print("ERROR: Failed to load config file")
        return
    
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except Exception as e:
        print(f"ERROR: {e}")
        return
    
    stats = Stats()

    try:
        sock.bind((config.server_ip, config.server_port))
        sock.settimeout(1.0)
        print(f"[Server] listening on {config.server_ip}:{config.server_port}")
        while True:
            try: 
                data, _ = sock.recvfrom(65535)
            except socket.timeout:
                continue

            stats.inc_packets()
            try:
                packet = IP(data)
            except:
                stats.inc_errors()
                continue

            if IP not in packet:
                if verbose:
                    print("ERROR: while parsing missing IP header")
                stats.inc_errors()
                continue
            
            if verbose:
                print("Received packet:")
                print(f"    src_ip: {packet[IP].src} dst_ip: {packet[IP].dst} protocol: {packet[IP].proto} length: {len(data)}")
            
            stats.inc_protocol(packet[IP].proto)

            if verbose:
                if TCP in packet:
                    print(f"    [TCP] sport: {packet[TCP].sport} dport: {packet[TCP].dport}")

                elif UDP in packet:
                    print(f"    [UDP] sport: {packet[UDP].sport} dport: {packet[UDP].dport}")

                elif ICMP in packet:
                    print(f"    [ICMP] type: {packet[ICMP].type} code: {packet[ICMP].code}")

                else:
                    print(f"    [RAW]")
            
    except KeyboardInterrupt:
        print("\nKEYBOARD INTERRUPT")
        stats.print()
    finally:
        sock.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", "-c", default="../test_config.json")
    parser.add_argument("--verbose", "-v", action="store_true", default=False)
    args = parser.parse_args()

    main(args.config, args.verbose)
