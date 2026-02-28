from tests.stats import ExchangeStats

def check(stats: ExchangeStats) -> None:
    udp_count = 0
    tcp_count = 0

    for packet in stats.received:
        if packet.ip_proto == 17:
            udp_count += 1
        elif packet.ip_proto == 6:
            tcp_count += 1

    assert tcp_count == 5
    assert udp_count == 10
