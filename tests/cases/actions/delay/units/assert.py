from tests.stats import ExchangeStats

def check(stats: ExchangeStats) -> None:
    assert stats.no_losses()
    assert all(e.rtt and e.rtt >= 0.99 and e.rtt <= 1.01 for e in stats.exchanges)
    