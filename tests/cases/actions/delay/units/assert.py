from tests.stats import ExchangeStats

def check(stats: ExchangeStats) -> None:
    assert stats.no_losses()
    assert all(e.rtt and e.rtt >= 0.999 and e.rtt <= 1.001 for e in stats.exchanges)
    