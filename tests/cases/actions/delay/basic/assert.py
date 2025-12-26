from tests.stats import ExchangeStats

def check(stats: ExchangeStats) -> None:
    assert stats.no_losses()
    assert all(e.rtt and e.rtt >= 0.099 and e.rtt <= 0.101 for e in stats.exchanges)

    # No reordering
    times = [e.received.recv_time for e in stats.exchanges if e.received]
    assert times == sorted(times)
    