from tests.stats import ExchangeStats

def check(stats: ExchangeStats) -> None:
    assert stats.no_losses

    assert all(e.rtt and e.rtt < 0.01 for e in stats.exchanges[:5])

    total_time = stats.received[-1].recv_time - stats.sent[0].send_time
    total_bytes = sum(len(r.raw) for r in stats.received[5:])

    assert abs(total_bytes / total_time - 1000) <= 10
    